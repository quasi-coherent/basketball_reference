#!/usr/bin/env bash
set -e

source /home/ubuntu/.profile

YESTERDAY=$(date +"%Y%m%d" -d "yesterday")

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Scraping monthly data for archiving..."
./scrape_monthly_boxscores.py $YESTERDAY 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Moving monthly data to s3..."
aws s3 cp --recursive tmp/ s3://donohue/nba/archive/ 2>&1

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Cleaning up tmp dir..."
rm tmp/*

echo "$(date +"%Y-%m-%d %H:%M:%S %Z"): Done!"