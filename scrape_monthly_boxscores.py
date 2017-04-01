#!/usr/bin/env python
import os
import sys
import pandas as pd

from util.util import launch_spider, prepare_dates

try:
  _, month, season = prepare_dates(sys.argv[1])
except IndexError:
  sys.stdout.write("Example usage: python scrape_monthly_boxscores.py 2017 may")
  sys.exit(1)

project_dir = os.environ["PROJECT_DIR"]

launch_spider(spider_name="advanced_boxscore", 
  season=season, month=month,
  project_dir=project_dir, data_dir="tmp/")