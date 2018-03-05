#!/bin/bash

declare -a months17=(10 11 12)

for month in "${months17[@]}"; do
  python scrape_monthly_boxscores.py "2017${month}01"
done

declare -a months18=(01 02)
for month in "${months18[@]}"; do
  python scrape_monthly_boxscores.py "2018${month}01"
done

aws s3 cp --recursive tmp/ s3://donohue/nba/archive/
python concat_results.py

mv data/all_boxscores_2001-2018.json /home/ubuntu/
mv all_boxscores_2001-2018_tmp.json all_boxscores_2001-2018.json; mv all_boxscores_2001-2018.json data/

declare -a dates=("20180301" "20180302" "20180303" "20180304")
for date in "${dates[@]}"; do
  python scrape_daily_boxscores.py $date
done

aws s3 sync data/ s3://donohue/nba/data/
git add data/; git commit -m "New data"; git push