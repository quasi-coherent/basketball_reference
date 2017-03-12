#!/usr/bin/env bash
set -e -x 

TODAY=date +"%Y%m%d"
YESTERDAY=date +"%Y%m%d" -d "yesterday"

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Archiving data directory..."
for f in `ls data`; do cp data/$f archive/`date +'%Y%m%d' --date='-2 days'`_$f; done

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Scraping yesterday's games..."
./scrape_daily_boxscores.py $YESTERDAY 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Making predictions..."
./predict.py $TODAY 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Sending emails..."
./send_emails.py $TODAY 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Syncing data directory with s3..."
aws s3 sync data/ s3://donohue/nba/data/ 2>&1 

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Cleaning up tmp dir..."
rm tmp/* 2>&1 

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Done!"