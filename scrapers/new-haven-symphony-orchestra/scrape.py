import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Set the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept' : 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language' : 'en-US,en;q=0.5',
    'Accept-Encoding' : 'gzip, deflate'
}

# Send a GET request with headers
response = requests.get('https://newhavensymphony.org/events/', headers=headers)

print('Beginning scrape ... ')

#print(response.content)

html_content = response.content

# Use Beautiful Soup to parse the HTML
soup = BeautifulSoup(html_content, "html.parser")


#print(html_content)


#eventItem

eventItems = soup.find_all("_event-details")

print(len(eventItems))

#^This shows a zero.
# TODO: Use technique described here ...
#       https://www.reddit.com/r/learnpython/comments/s20v6w/easy_way_to_extract_json_part_of_a_string/
#       ... to parse the JSON in the minified ball of crap returned by our initial request.
#       ... then use that JSON to get event inforamtion.


for eventItem in eventItems:
    something = eventItem.contents
    print(type(something));
    if(len(something)) == 1:
        print("It's one.")
    else:
        print("It's something else.")
        print(len(something))
        seriesOuter = eventItem.find_all(class_="event-series")
        print("The series:")
        print(seriesOuter[0].contents[0].strip())
        titleOuter = eventItem.find_all(class_="event-title")
        linkAndTitle = titleOuter[0].find('a')
        url = linkAndTitle.get("href")
        print("The url:")
        print(url)
        print("The title:")
        print(linkAndTitle.contents[0])
        dateOuter = eventItem.find_all(class_="cs-light-it")
        # Convert the date string to proper format for parsing
        date_str = dateOuter[0].contents[0].strip()
        # Format: "MONTH DD, YYYY AT H:MM AM/PM"
        dateObject = datetime.strptime(date_str, '%B %d, %Y AT %I:%M %p')
        isoText = dateObject.isoformat()
        print("The date:")
        print(isoText)
        venueOuter = eventItem.find('h3')
        if (venueOuter is None):
            print('VenueOuter is none. But if this is the mainstage series, we know the venue.')
        else:
            print("The venue:")
            print(venueOuter.findChild('a').contents[0].strip())
    #print(something)
    print("============")

print('... scrape finished')
