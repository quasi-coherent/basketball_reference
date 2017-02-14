#!/usr/bin/env bash

set -e

echo "Archiving data directory and syncing with s3..."
for f in `ls data`; do mv data/$f archive/`date +%Y%m%d`_$f; done
aws s3 sync s3://donohue/nba/data/ data/ 2>&1

echo "Preparing new data..."
./prepare_data.py 2>&1

echo "Training models and making predictions..."
./train_and_predict.py 2>&1

echo "Sending emails..."
./send_emails.py 2>&1

echo "Syncing data directories..."
aws s3 sync data/ s3://donohue/nba/data/ 2>&1

echo "Cleaning up resources..."
rm resources/*

echo "Done!"