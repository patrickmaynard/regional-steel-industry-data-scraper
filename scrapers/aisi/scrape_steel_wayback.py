import re
import argparse
import requests
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup
from collections import defaultdict
from tqdm import tqdm
import matplotlib.pyplot as plt


CDX_URL = "https://web.archive.org/cdx/search/cdx"
TARGET = "https://www.steel.org/industry-data/"


# Regex to find the district breakdown line used on steel.org, e.g.
# "Broken down by districts, here’s production for the week ending November 29, 2025, in thousands of net tons: North East: 115; Great Lakes: 513; Midwest: 254; Southern: 794 and Western: 60 for a total of 1736."
DIST_PATTERN = re.compile(
    r"Broken down by districts[\s\S]*?week ending\s+(?P<date>[^,\n]+),[\s\S]*?:\s*(?P<body>.+?)for a total",
    re.IGNORECASE
)
# Another fallback pattern: look for sequences "North East: 115; Great Lakes: 513; Midwest: 254; Southern: 794 and Western: 60"
NUMS_PATTERN = re.compile(
    r"North\s*East[:\s]+(?P<NE>[\d,]+)\D+Great\s*Lakes[:\s]+(?P<GL>[\d,]+)\D+Midwest[:\s]+(?P<MW>[\d,]+)\D+Southern[:\s]+(?P<SOU>[\d,]+)\D+Western[:\s]+(?P<W>[\d,]+)",
    re.IGNORECASE
)

def query_cdx(start_year, end_year, limit=10000):
    params = {
        'url': TARGET,
        'output': 'json',
        'from': str(start_year),
        'to': str(end_year),
        'filter': 'statuscode:200',
        'limit': str(limit),
        'collapse': 'timestamp:8'
    }
    r = requests.get(CDX_URL, params=params, timeout=120)
    r.raise_for_status()
    data = r.json()
    # first row is header
    if len(data) <= 1:
        return []
    keys = data[0]
    rows = [dict(zip(keys, row)) for row in data[1:]]
    return rows

def fetch_snapshot_html(timestamp):
    url = f"https://web.archive.org/web/{timestamp}/{TARGET}"
    r = requests.get(url, timeout=120)
    if r.status_code != 200:
        return None
    return r.text

def extract_from_html(html):
    if not html:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    # first try DIST_PATTERN
    m = DIST_PATTERN.search(text)
    if m:
        date_str = m.group('date').strip()
        body = m.group('body')
        # try to capture numbers from body
        m2 = NUMS_PATTERN.search(body)
        if m2:
            return date_str, {
                'North East': int(m2.group('NE').replace(',', '')),
                'Great Lakes': int(m2.group('GL').replace(',', '')),
                'Midwest': int(m2.group('MW').replace(',', '')),
                'Southern': int(m2.group('SOU').replace(',', '')),
                'Western': int(m2.group('W').replace(',', ''))
            }
    # fallback: try to find numbers anywhere in the page using NUMS_PATTERN
    m3 = NUMS_PATTERN.search(text)
    if m3:
        # we may not have explicit "week ending" date, so fall back to the snapshot timestamp (handled externally)
        return None, {
            'North East': int(m3.group('NE').replace(',', '')),
            'Great Lakes': int(m3.group('GL').replace(',', '')),
            'Midwest': int(m3.group('MW').replace(',', '')),
            'Southern': int(m3.group('SOU').replace(',', '')),
            'Western': int(m3.group('W').replace(',', ''))
        }
    return None

def parse_cdx_rows(rows):
    records = []
    for r in rows:
        ts = r.get('timestamp')
        if not ts:
            continue
        try:
            t = dt.datetime.strptime(ts, '%Y%m%d%H%M%S')
        except Exception:
            # try shorter timestamp
            t = dt.datetime.strptime(ts[:8], '%Y%m%d')
        html = fetch_snapshot_html(ts)
        parsed = extract_from_html(html)
        if parsed is None:
            continue
        date_str, numbers = parsed
        if date_str:
            # try to parse the human date, e.g. "November 29, 2025"
            try:
                parsed_date = dt.datetime.strptime(date_str, '%B %d %Y')
            except Exception:
                try:
                    parsed_date = dt.datetime.strptime(date_str, '%B %d, %Y')
                except Exception:
                    parsed_date = t
        else:
            parsed_date = t
        if numbers:
            rec = {
                'snapshot_ts': t,
                'date_reported': parsed_date,
                **numbers
            }
            records.append(rec)
    return records

def aggregate_monthly(records):
    df = pd.DataFrame(records)
    if df.empty:
        return df
    df['yearmonth'] = df['date_reported'].apply(lambda d: d.replace(day=1))
    # group by month and average
    agg = df.groupby('yearmonth')[['North East','Great Lakes','Midwest','Southern','Western']].mean()
    agg = agg.sort_index()
    return agg

def plot_regions(agg_df, out_png):
    plt.figure(figsize=(12,6))
    for col in agg_df.columns:
        plt.plot(agg_df.index, agg_df[col], label=col)
    plt.legend()
    plt.title('Monthly average regional net tons (from Wayback snapshots)')
    plt.xlabel('Month')
    plt.ylabel('Net tons (thousands)')
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--from', dest='from_year', type=int, default=2020)
    parser.add_argument('--to', dest='to_year', type=int, default=2025)
    parser.add_argument('--out', dest='out_csv', default='monthly_region.csv')
    parser.add_argument('--plot', dest='out_png', default='region_plot.png')
    args = parser.parse_args()

    print(f"Querying Wayback CDX for {TARGET} from {args.from_year} to {args.to_year}...")
    rows = query_cdx(args.from_year, args.to_year)
    print(f"Found {len(rows)} snapshots (after collapsing). Will try to parse each snapshot.")

    records = []
    for r in tqdm(rows):
        ts = r.get('timestamp')
        try:
            t = dt.datetime.strptime(ts, '%Y%m%d%H%M%S')
        except Exception:
            t = dt.datetime.strptime(ts[:8], '%Y%m%d')
        html = fetch_snapshot_html(ts)
        parsed = extract_from_html(html)
        if parsed is None:
            continue
        date_str, numbers = parsed
        if date_str:
            # try parsing human date
            parsed_date = None
            for fmt in ('%B %d %Y', '%B %d, %Y', '%b %d %Y', '%b %d, %Y'):
                try:
                    parsed_date = dt.datetime.strptime(date_str, fmt)
                    break
                except Exception:
                    continue
            if parsed_date is None:
                parsed_date = t
        else:
            parsed_date = t
        rec = {
            'snapshot_ts': t,
            'date_reported': parsed_date,
            **numbers
        }
        records.append(rec)

    if not records:
        print('No regional numbers were extracted from snapshots. Try widening the date range or run with debug to inspect snapshot HTML content.')
        return

    agg = aggregate_monthly(records)
    print(f"Saving CSV to {args.out_csv} and plot to {args.out_png} ...")
    agg.to_csv(args.out_csv, float_format='%.2f')
    plot_regions(agg, args.out_png)
    print('Done.')

if __name__ == '__main__':
    main()

