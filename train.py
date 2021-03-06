#!/usr/bin/env python
import datetime
import os
import sys
import pandas as pd

from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.externals import joblib

from models.params import *
from models.preprocess import PreprocessBoxscore
from models.sklearn.moneyline import MoneylineClassifier
from models.sklearn.spread_and_total import SpreadAndTotalRegressor


season = now.year if now.month in range(1, 7) else now.year + 1

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
sys.stdout.write("[%s]: Training spread regressor...\n" % datetime.datetime.now().strftime("%x %X"))
sys.stdout.flush()
SR.train()
joblib.dump(SR, "resources/SR.pkl")

X_total, y_total = pp.total()
GBR_total = GradientBoostingRegressor(**TOTAL_PARAMS)
TR = SpreadAndTotalRegressor(features=X_total, response=y_total,
  model=GBR_total)
sys.stdout.write("[%s]: Training total regressor...\n" % datetime.datetime.now().strftime("%x %X"))
sys.stdout.flush()
TR.train()
joblib.dump(TR, "resources/TR.pkl")

X_moneyline, y_moneyline = pp.moneyline()
GBC_moneyline = GradientBoostingClassifier(**MONEYLINE_PARAMS)
ML = MoneylineClassifier(features=X_moneyline, response=y_moneyline,
  model=GBC_moneyline)
sys.stdout.write("[%s]: Training moneyline classifier...\n" % datetime.datetime.now().strftime("%x %X"))
sys.stdout.flush()
ML.train()
joblib.dump(ML, "resources/ML.pkl")

# record cv scores
sr_mae = -1*SR.cv_score(n_folds=5)
tr_mae = -1*TR.cv_score(n_folds=5)
ml_acc = ML.cv_score(n_folds=5)
metric_df = pd.DataFrame({"spread_mae": [sr_mae], "total_mae": [tr_mae], "ml_acc": [ml_acc]})
metric_df.to_csv(project_dir + "data/metrics.csv", index=False)
