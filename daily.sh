#!/usr/bin/env bash

set -e -x 

echo "Archiving data directory..."
for f in `ls data`; do cp data/$f archive/`date +'%Y%m%d' --date='-2 days'`_$f; done

echo "Preparing new data..."
./prepare_data.py 2>&1

echo "Training models and making predictions..."
./train_and_predict.py 2>&1

echo "Sending emails..."
./send_emails.py 2>&1

echo "Syncing directories with s3..."
aws s3 sync data/ s3://donohue/nba/data/ 2>&1
aws s3 sync archive/ s3://donohue/nba/archive/snapshot/ 2>&1
aws s3 sync . s3://donohue/nba/project/basketball_reference/ --exclude "*.pyc" 2>&1

echo "Done!"