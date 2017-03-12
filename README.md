`pip install -r requirements.txt`

Scraper example usage:

To get all games in May 2008
`scrapy crawl boxscore -a season=2008 -a month=may --set FEED_URI=data/may-2008.json --set FEED_FORMAT=jsonlines` 

or to get all games on January 29th, 2017

`scrapy crawl boxscore -a season=2017 -a month=january -a today=20170129 --set FEED_URI=data/20170129.json --set FEED_FORMAT=jsonlines`