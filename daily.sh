#!/usr/bin/env bash

set -e -x 

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Archiving data directory..."
for f in `ls data`; do cp data/$f archive/`date +'%Y%m%d' --date='-2 days'`_$f; done

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Preparing new data..."
./prepare_data.py 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Training models and making predictions..."
./train_and_predict.py 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Sending emails..."
./send_emails.py 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Syncing directories with s3..."
aws s3 sync data/ s3://donohue/nba/data/ 2>&1
aws s3 sync archive/ s3://donohue/nba/archive/snapshot/ 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Logging..."
aws s3 cp /var/log/cloud-init-output.log s3://donohue/nba/log/`date +%Y-%m-%d`.log

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Done!"