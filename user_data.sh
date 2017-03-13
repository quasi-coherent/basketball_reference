#!/bin/bash
set -e -x
apt-get update
apt-get install -y awscli
apt-get install -y python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
pip install scrapy bs4 pandas numpy scipy scikit-learn
mkdir /home/ubuntu/.aws; aws s3 cp --recursive s3://donohue/.aws/ /home/ubuntu/.aws/
aws s3 cp --recursive s3://donohue/nba/project/ /home/ubuntu/
aws s3 sync s3://donohue/nba/data/ /home/ubuntu/basketball_reference/data/
chmod 700 /home/ubuntu/basketball_reference/*.py
source /home/ubuntu/.profile
# chown -R ubuntu /home/ubuntu/basketball_reference/
cd /home/ubuntu/basketball_reference/
./scrape_daily_boxscores.py
./train.py
aws s3 cp --recursive resources/ s3://donohue/nba/models/
aws ec2 terminate-instances --instance-ids `ec2metadata --instance-id`