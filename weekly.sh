#!/usr/bin/env bash
set -e -x

TODAY=date +"%Y%m%d"

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Training models..."
./train.py $TODAY 2>&1 

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Syncing resource dirs..."
aws s3 sync resources/ s3://donohue/nba/project/basketball_reference/resources/ 2>&1