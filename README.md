# orchestra-daily-event-scrapers

I'm going to put together four or five regional scrapers for orchestra events, then use AI to write weekly email newsletters about upcoming performances. 

## Setup instructions 

```
cd path/to/named-scraper
source bin/activate
python3 -m pip install -r requirements.txt
python3 scrape.py 
```

## Todo items:

* While waiting for the import script to run at work, put together a list of orchestras to scrape events for, focusing initially on the Northeast Corridor
  * Wilmington
    * https://www.delawaresymphony.org/events/upcoming-events/ -- **partially built, skipping for now because of a js human-user check** 
    * Second pass: https://www.udel.edu/academics/colleges/cas/units/departments/school-of-music/events/
  * Providence
    * https://www.riphil.org/events
    * Second pass: Add university groups
    * **Current todo items:**
      * Clone the Delaware Symfony scraper and adapt it
      * 
      * 
  * Stamford
    * Second pass: Orchestra Lumos has a website that's an unscrapable mess. Maybe ask them to upload a cleaned-up CSV file or something
    * Second pass: Add university groups
  * New Haven
    * https://newhavensymphony.org/events/
    * Second pass: Add university groups
  * Bridgeport
    * https://gbs.org/events/
    * Second pass: Add university groups
  * Newark
    * https://www.njsymphony.org/concerts-and-events/concert-listing
    * Second pass: Add university groups
  * Baltimore
    * https://my.bsomusic.org/events
    * Second pass: Add university groups
  * Philadelphia
    * https://philorch.ensembleartsphilly.org/tickets-and-events/events
    * https://chamberorchestra.org/season-24-25-60th-anniversary/
    * Second pass: Add university groups
  * Boston
    * https://www.bso.org/events?view=byDate&brands=12057%2C12058%2C12059
    * Second pass: Add university groups
  * DC
    * https://www.kennedy-center.org/nso/home/concerts-and-tickets/
    * https://nationalphilharmonic.org/2024-2025-concerts/
    * Second pass: Add university groups
  * New York
    * https://www.americancomposers.org/performances-events
    * https://americansymphony.org/current-season/
    * https://www.nyphil.org/concerts-tickets/
    * Second pass: Add university groups
* Use the requests library and your smart terminal (which I believe uses Claude) to **quickly** build scrapers for the list above. Scrapers should run once every day, but no more than that. And they should be respectful by not hammering sites, using randomized sleeps to avoid that outcome
* Set up a demo email solution that doesn't use generative AI at all, setting up the demo on your personal server behind basic auth
* Once you've tested everything in basic form, buy the domain and set up the app with a "beta" label using a DigitalOcean droplet
* Set up generative AI. For environmental reasons, be sure to use a small language model (SLM) like the ones described here: https://winder.ai/exploring-small-language-models/
* Check over the course of a month to see whether we need to somehow work to avoid having any one or two orchestras dominate the newsletters
* Do a second pass to add university musical events, breaking the event categorizations into smaller subregions -- maybe even allowing state-by-state searches, so long as adjoining states are also included in results. Be sure to have an attribute that marks events as either pro or uni events, allowing more specific searches
* Be sure to include a mention on the newsletter of how readers can "let your friends in ____ know about the event by forwarding this email. Be sure to ask them how they're doing and what they're <cooking/eating/reading/listening to/whatever>."
* Build a bit of logic that highlights a performance that does **not** have any of the top 20 composers from the 1700s and 1800s in the title, in order to promote less-played composers
*
*
*
*
* Hire a few freelancers to write **very** occasional freelance pieces, using a custom Gmail forwarder to avoid having your main account spammed
*
*
* Add a way for groups in the Northeast to ask for inclusion of their events on the calendar, emphasizing that a group must provide a CSV if they don't have an easily scrapable website
*
*
*
*
*
* Gradually add scrapers for more adjoining states
*
*
*
*
* Once at least 35 states are covered, add opera listings from https://www.operaamerica.org/calendar/ ... but you'll eventually divide these out into the MajorLeagueCities project
*
*
*
*
* Re-enable your orchestra tour Google Alert and start writing occasional blog posts about performances of American orchestras in Europe
*
*
*
* Once you've done freelance stuff with at least a half-dozen people and have their bios, add a page that includes your list of contributors (including yourself!)
*
*
* Enable ads
*
*
* Clone the project, add the five major sports leagues in the clone and launch MajorLeagueCities.com
*
*
*
* etc.,.
*
