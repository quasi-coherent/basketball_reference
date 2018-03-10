#!/usr/bin/env bash
set -e

source /home/ubuntu/.profile

TODAY=$(date +"%Y%m%d")
YESTERDAY=$(date +"%Y%m%d" -d "yesterday")

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Fetching data dir..."
aws s3 sync s3://donohue/nba/data/ data/

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Scraping yesterday's games..."
./scrape_daily_boxscores.py $YESTERDAY 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Scraping today's matchups..."
./scrape_upcoming.py $TODAY 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Fetching trained models..."
aws s3 sync s3://donohue/nba/models/ resources/ 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Making predictions..."
./predict.py $TODAY 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Sending emails..."
./send_emails.py $TODAY 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Syncing data directory with s3 and remote repo..."
aws s3 sync data/ s3://donohue/nba/data/ 2>&1
git add data/
git commit -m "New data"
git push origin master

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Cleaning up tmp dir..."
rm tmp/* 2>&1 

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Done!"