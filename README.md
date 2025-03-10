# orchestra-daily-event-scrapers
I'm going to put together four or five regional scrapers for orchestra events, then use AI to write weekly email newsletters about upcoming performances

TODO items: 

* While waiting for the import script to run at work, put together a list of orchestras to scrape events for, focusing initially on the Northeast Corridor
  * Wilmington
    * https://www.delawaresymphony.org/events/upcoming-events/
    * Second pass: https://www.udel.edu/academics/colleges/cas/units/departments/school-of-music/events/
  * Providence
    * https://www.riphil.org/events
    * Second pass: Add university groups 
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
  * Trenton
  * Baltimore
  * Philadelphia
  * Boston
  * DC
  * New York 
* Use pyspider to **quickly** build scrapers for the list above 
* Set up a demo email solution that doesn't use generative AI at all, setting up the demo on your personal server behind basic auth 
* Once you've tested everything in basic form, buy the domain and set up the app with a "beta" label using a DigitalOcean droplet 
* Set up generative AI. For environmental reasons, be sure to use a small language model (SLM) like the ones described here: https://winder.ai/exploring-small-language-models/
* Do a second pass to add university musical events, breaking the event categorizations into smaller subregions. Be sure to have an attribute that marks events as either pro or uni events, allowing more specific searches
* Add a way for groups in the Northeast to ask for inclusion of their events on the calendar  
* 
* 
* etc.,.
* 
