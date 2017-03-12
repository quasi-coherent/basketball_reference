#!/usr/bin/env python
import os
import pickle
import sys
import pandas as pd

from sklearn.externals import joblib

from models.preprocess import PreprocessBoxscore
from util.util import prepare_dates

try:
  today, _, season = prepare_dates(sys.argv[1])
except IndexError:
  sys.stdout.write("Usage: python predict.py date")
  sys.exit(1)

upcoming_games = "upcoming_games_" + today + ".json"

if not os.path.isfile("tmp/%s" % upcoming_games):
  sys.stdout.write("upcoming_games_%s.json doesn't exist..." % today)
  sys.exit(1)

# load already trained models
try:
  SR = joblib.load("resources/SR.pkl")
  TR = joblib.load("resources/TR.pkl")
  ML = joblib.load("resources/ML.pkl")
except IOError:
  sys.stdout.write("Pickled models don't exist...")
  sys.exit(1)

project_dir = os.environ["PROJECT_DIR"]
all_boxscores = os.environ["ALL_BOXSCORES"]
path = project_dir + "data/" + all_boxscores

# preprocessing object
pp = PreprocessBoxscore(path, season)

# predict on today's games
upcoming_games_df = pd.read_json(project_dir + "tmp/%s" % upcoming_games, lines=True)
predictions = []
for _, row in upcoming_games_df.iterrows():
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

# write to file
pred_df = pd.DataFrame(predictions, 
    columns=["date", "home_team", "away_team", "spread", "total", "moneyline", "away_prob", "home_prob"])\
  .drop_duplicates(subset=["date", "home_team", "away_team"])
pred_df.to_csv(project_dir + "tmp/predictions_%s.csv" % today, index=False)
pred_df.to_csv(project_dir + "data/predictions.csv", header=False, mode="a", index=False)