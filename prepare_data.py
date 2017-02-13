#!/usr/bin/env python
import datetime
import os
import subprocess
import sys
import pandas as pd

def launch_spider(spider_name, season, month, today, project_dir, data_dir):
  subprocess.call(["scrapy", "crawl", spider_name,
      "-a", "season=%s" % season, 
      "-a", "month=%s" % month,
      "-a" , "today=%s" % today,
      "--set", "FEED_URI=%s%s%s.json" % (project_dir, data_dir, today),
      "--set", "FEED_FORMAT=jsonlines"],
    cwd=project_dir + "scrapers/" + spider_name +"/")

s3_uri = "s3://donohue/nba/"
project_dir = os.getcwd() + "/"
all_boxscores = "all_boxscores_2001-2017.json"

# get all_boxscores/historical predictions from s3
sys.stdout.write("Fetching historical data from s3...\n")
sys.stdout.flush()
subprocess.call(["aws", "s3", "sync",
  s3_uri + "data/", project_dir + "data/"])

# get inputs to scrapers
now = datetime.datetime.now()
today = now.strftime("%Y%m%d")
yesterday = (now - datetime.timedelta(days=1)).strftime("%Y%m%d")
month_today = now.strftime("%B").lower()
month_yesterday = (now - datetime.timedelta(days=1)).strftime("%B").lower()
season = now.year if now.month in range(1, 7) else now.year + 1

# scrape last month's data if today is the start
# of a new month, for archiving
if month_today != month_yesterday:
  sys.stdout.write("Scraping last month's data for archiving...\n")
  sys.stdout.flush()
  subprocess.call(["scrapy", "crawl", "advanced_boxscore", 
      "-a", "season=%s" % season, 
      "-a", "month=%s" % month_yesterday,
      "--set", "FEED_URI=%s%s%s_%s.json" % (project_dir, "resources/", season, month_yesterday), 
      "--set", "FEED_FORMAT=jsonlines"],
    cwd=project_dir + "scrapers/advanced_boxscore/")
  sys.stdout.write("Persisting last month's data...\n")
  sys.stdout.flush()
  subprocess.call(["aws", "s3", "cp", 
    project_dir + "resources/" + season + "_" + month_yesterday + ".json", 
    s3_uri + "archive/"])

# scrape yesterday's results
sys.stdout.write("Scraping the results of yesterday's games...\n")
sys.stdout.flush()
launch_spider(spider_name="advanced_boxscore", 
  season=season, month=month_yesterday, today=yesterday,
  project_dir=project_dir,
  data_dir="resources/")

# scrape today's matchups
sys.stdout.write("Scraping today's matchups...\n")
sys.stdout.flush()
launch_spider(spider_name="upcoming_games",
  season=season, month=month_today, today=today,
  project_dir=project_dir, 
  data_dir="resources/")

# merge yesterday's scores with historical scores
sys.stdout.write("Merging yesterday's scores with historical data...\n")
sys.stdout.flush()
all_df = pd.read_json(project_dir + "data/" + all_boxscores, lines=True)
yesterday_df = pd.read_json(project_dir + "resources/%s.json" % yesterday, lines=True)
merged = pd.concat([all_df, yesterday_df])
merged.to_json("data/" + all_boxscores, lines=True, orient="records")