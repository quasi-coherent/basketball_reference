#!/bin/bash
set -e -x
apt-get update
apt-get install -y awscli
apt-get install -y python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
pip install scrapy bs4 pandas numpy scipy scikit-learn
mkdir /home/ubuntu/.aws; aws s3 cp --recursive s3://donohue/.aws/ /home/ubuntu/
aws s3 cp --recursive s3://donohue/nba/project/ /home/ubuntu/
aws s3 sync s3://donohue/nba/data/ /home/ubuntu/basketball_reference/data/
chmod 700 /home/ubuntu/basketball_reference/*.py /home/ubuntu/basketball_reference/*.sh
# chown -R ubuntu /home/ubuntu/basketball_reference/
echo "export SMTP_ENDPOINT='email-smtp.us-east-1.amazonaws.com'" >> /home/ubuntu/.profile
echo "export SMTP_PORT=587" >> /home/ubuntu/.profile
echo "export SMTP_USER='AKIAIHBIB5SQUWF77FUQ'" >> /home/ubuntu/.profile
echo "export SMTP_PASS='AmuZFyh/kL5l1lunYlVA3DNX1eWUGj0Eii9UMYFrthP0'" >> /home/ubuntu/.profile
source /home/ubuntu/.profile
cd /home/ubuntu/basketball_reference/
./daily.sh
aws ec2 terminate-instances --instance-ids `ec2metadata --instance-id`