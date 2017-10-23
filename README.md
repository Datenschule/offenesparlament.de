# offenesparlament.de

This projects contains the API for offenesparlament.de. The Scrapers for offenesparlament.de can be found here:
 
 * [PLPR Scraper](https://github.com/Datenschule/plpr-scraper) for the protocols of the Bundestag
 * [Topscraper](https://github.com/Datenschule/topscraper) for all the TOPs with speaker lists
 * [Agenda Scraper](https://github.com/Datenschule/agendas) for all TOPs with meta information
 
 # Setup
 To Setup the Database the following steps need to be performed:
 
1. setup the database from [Pretty Session Protocols](https://github.com/Datenschule/pretty_session_protocols) the get 
 the right schema

2. clone PLPR scraper repository and scrape the session protocols via the PLPR Scraper with
  
  ```bash
DATABSE_URI=<db_url> python views.py
#e.g.: DATABSE_URL=sqlite:////home/user/db.sqlite python scraper/scraper.py
```

3. scrape TOPs with [Topscraper](https://github.com/Datenschule/topscraper) and [AgendaScraper](https://github.com/Datenschule/agendas)
4. merge scraped Tops into the Database with the [Topmerger](https://github.com/Datenschule/topmerger)
5. merge MDBs for [MdB Merger](https://github.com/Datenschule/mdb-merger)
6. start the server with 
  ```bash
DATABSE_URI=<db_url> python views.py
#e.g.: DATABSE_URL=sqlite:////home/user/db.sqlite python3 plenartracker.py
```
