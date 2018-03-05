#!/usr/bin/env python
import os
import sys

from util.util import launch_spider, prepare_dates

try:
  today, month, season = prepare_dates(sys.argv[1])
except IndexError:
  sys.stdout.write("Usage: python scrape_upcoming.py date")
  sys.exit(1)

project_dir = os.environ["PROJECT_DIR"]

launch_spider(spider_name="upcoming_games",
  season=season, month=month, today=today,
  project_dir=project_dir, data_dir="tmp/")
