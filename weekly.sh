#!/usr/bin/env bash
set -e

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Syncing data dir..."
aws s3 sync s3://donohue/nba/data/ data/

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Training models..."
./train.py 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Syncing resource dirs..."
aws s3 sync resources/ s3://donohue/nba/models/ 2>&1
