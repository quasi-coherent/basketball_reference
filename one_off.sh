#!/usr/bin/env bash

set -e
set -u
echo $1

if [ $# -eq 0 ]
  then echo "No date supplied..."
  exit;
fi

if [[ $1 != [0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9] ]]
  then echo "Date format is not yyyymmdd..."
fi

echo "Fetching most recent historical data..."
aws s3 sync s3://donohue/nba/data/ data/ 2>&1

echo "Scraping matchups for the supplied date..."
./prepare_data.py $1 2>&1

echo "Training models and making predictions..."
./train_and_predict.py $1 2>&1

echo "Sending emails..."
./send_emails.py $1 2>&1

echo "Cleaning up resources..."
rm resources/*

echo "Done!"