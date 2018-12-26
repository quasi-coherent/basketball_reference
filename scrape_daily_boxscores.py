#!/usr/bin/env python
import os
import sys
import pandas as pd

from util.util import launch_spider, prepare_dates

try:
  today, month, season = prepare_dates(sys.argv[1])
except IndexError:
  sys.stdout.write("Usage: python scrape_daily_boxscores.py date")
  sys.exit(1)

project_dir = os.environ["PROJECT_DIR"]
all_boxscores = os.environ["ALL_BOXSCORES"]

launch_spider(spider_name="advanced_boxscore",
  season=season, month=month, today=today,
  project_dir=project_dir, data_dir="tmp/")

all_df = pd.read_json(project_dir + "data/" + all_boxscores, lines=True)
daily_df = pd.read_json(project_dir +
  "tmp/%s.json" % ("advanced_boxscore" + "_" + today), lines=True)
merged = pd.concat([all_df, daily_df]).drop_duplicates()
merged.to_json("data/" + all_boxscores, lines=True, orient="records")
