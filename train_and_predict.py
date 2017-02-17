#!/usr/bin/env python
import datetime
import os
import sys
import pandas as pd

from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier

from models.moneyline import MoneylineClassifier
from models.preprocess import PreprocessBoxscore
from models.spread_and_total import SpreadAndTotalRegressor
from models.params import *

# inputs
project_dir = os.getcwd() + "/"
now = datetime.datetime.now()
if len(sys.argv) > 1:
  today = sys.argv[1]
else:
  today = now.strftime("%Y%m%d")
path = project_dir + "data/all_boxscores_2001-2017.json"
season = now.year if now.month in range(1, 7) else now.year + 1

# preprocessing object
pp = PreprocessBoxscore(path, season)

# re-train models on historical boxscores + yesterday's boxscores
# and get historical performance
X_spread, y_spread = pp.spread()
GBR_spread = GradientBoostingRegressor(**SPREAD_PARAMS)
SR = SpreadAndTotalRegressor(features=X_spread, response=y_spread, 
  model=GBR_spread)
SR.train()
sr_mae = -1*SR.cv_score(n_folds=3)

X_total, y_total = pp.total()
GBR_total = GradientBoostingRegressor(**TOTAL_PARAMS)
TR = SpreadAndTotalRegressor(features=X_total, response=y_total, 
  model=GBR_total)
TR.train()
tr_mae = -1*TR.cv_score(n_folds=3)

X_moneyline, y_moneyline = pp.moneyline()
GBC_moneyline = GradientBoostingClassifier(**MONEYLINE_PARAMS)
ML = MoneylineClassifier(features=X_moneyline, response=y_moneyline,
  model=GBC_moneyline)
ML.train()
ml_acc = ML.cv_score(n_folds=3)

# predict on today's games
matchups = pd.read_json(project_dir + "resources/%s.json" % today, lines=True)
predictions = []
for _, row in matchups.iterrows():
  date = row.get("date")
  home_team = row.get("home_team")
  away_team = row.get("away_team")
  sr_inputs = pp.input(home_team, away_team)
  tr_inputs = pp.input(home_team, away_team)
  ml_inputs = pp.input(home_team, away_team)
  sr_pred = SR.predict(sr_inputs)
  tr_pred = TR.predict(tr_inputs)
  ml_pred = ML.predict(ml_inputs)
  ml_pred_prob = ML.predict_prob(ml_inputs)
  predictions.append([date, home_team, away_team, sr_pred, tr_pred, ml_pred, ml_pred_prob[0], ml_pred_prob[1]])

# write to files
pred_df = pd.DataFrame(predictions, 
  columns=["date", "home_team", "away_team", "spread", "total", "moneyline", "away_prob", "home_prob"])
metric_df = pd.DataFrame({"spread_mae": [sr_mae], "total_mae": [tr_mae], "ml_acc": [ml_acc]})
pred_df.to_csv(project_dir + "resources/predictions_%s.csv" % today, index=False)
metric_df.to_csv(project_dir + "data/metrics.csv", index=False)

if len(sys.argv) == 1: # running daily, so append to historical predictions
  pred_df.to_csv(project_dir + "data/predictions.csv", header=False, mode="a", index=False)