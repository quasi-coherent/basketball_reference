#!/usr/bin/env python
import os
import pickle
import sys
import pandas as pd

from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier

from models.moneyline import MoneylineClassifier
from models.preprocess import PreprocessBoxscore
from models.spread_and_total import SpreadAndTotalRegressor
from models.params import *

from util.util import prepare_dates

try:
  _, _, season = prepare_dates(sys.argv[1])
except IndexError:
  sys.stdout.write("Usage: python predict.py date")
  sys.exit(1)

# inputs
project_dir = os.environ["PROJECT_DIR"]
all_boxscores = os.environ["ALL_BOXSCORES"]
path = project_dir + "data/" + all_boxscores

# preprocessing object
pp = PreprocessBoxscore(path, season)

# train and pickle models
X_spread, y_spread = pp.spread()
GBR_spread = GradientBoostingRegressor(**SPREAD_PARAMS)
SR = SpreadAndTotalRegressor(features=X_spread, response=y_spread, 
  model=GBR_spread)
SR.train()
pickle.dump(SR, open("resources/SR.pkl", "wb"))

X_total, y_total = pp.total()
GBR_total = GradientBoostingRegressor(**TOTAL_PARAMS)
TR = SpreadAndTotalRegressor(features=X_total, response=y_total, 
  model=GBR_total)
TR.train()
pickle.dump(TR, open("resources/TR.pkl", "wb"))

X_moneyline, y_moneyline = pp.moneyline()
GBC_moneyline = GradientBoostingClassifier(**MONEYLINE_PARAMS)
ML = MoneylineClassifier(features=X_moneyline, response=y_moneyline,
  model=GBC_moneyline)
ML.train()
pickle.dump(ML, open("resources/ML.pkl", "wb"))

# record cv scores
sr_mae = -1*SR.cv_score(n_folds=5)
tr_mae = -1*TR.cv_score(n_folds=5)
ml_acc = ML.cv_score(n_folds=5)
metric_df = pd.DataFrame({"spread_mae": [sr_mae], "total_mae": [tr_mae], "ml_acc": [ml_acc]})
metric_df.to_csv(project_dir + "data/metrics.csv", index=False)