`pip install -r requirements.txt`

Scraper example usage:

To get all games in May 2008
`scrapy crawl boxscore -a season=2008 -a month=may --set FEED_URI=data/may-2008.json --set FEED_FORMAT=jsonlines` 

or to get all games on January 29th, 2017

`scrapy crawl boxscore -a season=2017 -a month=january -a today=20170129 --set FEED_URI=data/20170129.json --set FEED_FORMAT=jsonlines`

Workflow:
  1. `prepare_data.py`: 
    * Fetch historical boxscore data and predictions from `s3://donohue/nba/data/` and sync with `$PROJECT_DIR/data/`.
    * If it's the first of the month, scrape all of last month's boxscore data for archiving and dump to `s3://donohue/nba/archive/`.
    * Scrape yesterday's boxscores and scrape today's matchups, and save these in `$PROJECT_DIR/resources/` as `$yesterday.json` and `$today.json`, respectively, in YYYYMMDD format.  
    * Append yesterday's boxscores to historical boxscores.  
  2. `train_and_predict.py`:
    * Train spread/total regressors and moneyline classifier on historical data (2001-yesterday).  
    * Read in today's matchups and feed these into the `models.preprocess.PreprocessBoxscore`'s `input` method to aggregate teams' season, last 10, last 3, and home/away statistics, and pass to trained models' `predict` methods. 
    * Append today's prediction to historical predictions `$PROJECT_DIR/data/predictions.csv`, write this also to `$PROJECT_DIR/resources/predictions_$today.csv` to be sent in an email body, and write model metrics (MAE, accuracy) to `$PROJECT_DIR/data/metrics.csv`.  
  3. `send_emails.py`:
    * Send an email with today's predictions `$PROJECT_DIR/resources/predictions_$today.csv` and historical model metrics.  
  4. Sync `$PROJECT_DIR/data/` with `s3://donohue/nba/data` and clear `$PROJECT_DIR/resources/`.  
