#!/usr/bin/env python
import datetime
import os
import sys
import pandas as pd

from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.externals import joblib

from models.moneyline import MoneylineClassifier
from models.spread_and_total import SpreadAndTotalRegressor
from models.stacked_preprocess import StackedPreprocessor
from models.params import *

project_dir = os.environ["PROJECT_DIR"]
all_boxscores = os.environ["ALL_BOXSCORES"]
path = project_dir + "data/" + all_boxscores

windows = [1, 3, 5, 10, 105]
pp = StackedPreprocessor(path)


# spread
GBR_spread = GradientBoostingRegressor(**SPREAD_PARAMS)
for window in windows:
  min_periods = None
  if window == 105:
    min_periods = 1
  X_spread, y_spread = pp.spread_train(window, min_periods)
  SR = SpreadAndTotalRegressor(features=X_spread, response=y_spread,
  model=GBR_spread)
  now = datetime.datetime.now()
  sys.stdout.write("[%s]: SR %s train...\n" % (now.strftime("%x %X"), window)); sys.stdout.flush()
  SR.train()
  joblib.dump(SR, "resources/SR/SR_%s.pkl" % window)

X_spread, y_spread = pp.spread_train(window=105, min_periods=1, location=True)
SR = SpreadAndTotalRegressor(features=X_spread, response=y_spread,
  model=GBR_spread)
now = datetime.datetime.now()
sys.stdout.write("[%s]: SR location train...\n" % now.strftime("%x %X")); sys.stdout.flush()
SR.train()
joblib.dump(SR, "resources/SR/SR_location.pkl")


# total
GBR_total = GradientBoostingRegressor(**TOTAL_PARAMS)
for window in windows:
  min_periods = None
  if window == 105:
    min_periods = 1
  X_total, y_total = pp.total_train(window, min_periods)
  TR = SpreadAndTotalRegressor(features=X_total, response=y_total,
  model=GBR_total)
  sys.stdout.write("[%s]: TR %s train...\n" % (now.strftime("%x %X"), window)); sys.stdout.flush()
  TR.train()
  joblib.dump(TR, "resources/TR/TR_%s.pkl" % window)

X_total, y_total = pp.total_train(window=105, min_periods=1, location=True)
TR = SpreadAndTotalRegressor(features=X_total, response=y_total,
  model=GBR_total)
sys.stdout.write("[%s]: TR location train...\n" % now.strftime("%x %X")); sys.stdout.flush()
TR.train()
joblib.dump(TR, "resources/TR/TR_location.pkl")


# moneyline
GBC_moneyline = GradientBoostingClassifier(**MONEYLINE_PARAMS)
for window in windows:
  min_periods = None
  if window == 105:
    min_periods = 1
  X_moneyline, y_moneyline = pp.moneyline_train(window, min_periods)
  ML = MoneylineClassifier(features=X_moneyline, response=y_moneyline,
    model=GBC_moneyline)
  sys.stdout.write("[%s]: ML %s train...\n" % (now.strftime("%x %X"), window)); sys.stdout.flush()
  ML.train()
  joblib.dump(ML, "resources/ML/ML_%s.pkl" % window)

X_moneyline, y_moneyline = pp.moneyline_train(window=105, min_periods=1, location=True)
ML = MoneylineClassifier(features=X_moneyline, response=y_moneyline,
  model=GBC_moneyline)
sys.stdout.write("[%s]: ML location train...\n" % now.strftime("%x %X")); sys.stdout.flush()
ML.train()
joblib.dump(ML, "resources/ML/ML_location.pkl")