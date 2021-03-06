import datetime
import pandas as pd

from sklearn.preprocessing import scale

class PreprocessBoxscore(object):
  def __init__(self, path, season):
    _all = pd.read_json(path, convert_dates=["date"], lines=True)
    start = datetime.datetime(year=season - 1, month=10, day=1)
    end = datetime.datetime(year=season, month=6, day=30)
    # avoid data leakage by dropping features that implicitly incorporate points scored
    self.all_boxscores = _all.drop(["home_ortg", "home_drtg", "away_ortg", "away_drtg"], axis=1)
    mask = (self.all_boxscores.date > start) & (self.all_boxscores.date < end)
    self.season = self.all_boxscores.loc[mask]

  def spread(self, scale_features=False):
    df = self.all_boxscores.copy()\
      .drop(["home_team", "away_team", "date"], axis=1)
    df["spread"] = df["home_score"] - df["away_score"]
    df["spread"] = df["spread"].apply(float)
    df = df.drop(["home_score", "away_score"], axis=1)
    X, y = df.ix[:, df.columns != "spread"], df["spread"]
    X = scale(X) if scale_features else X
    return X, y

  def moneyline(self, scale_features=False):
    df = self.all_boxscores.copy()\
      .drop(["home_team", "away_team", "date"], axis=1)
    df["outcome"] = (df["home_score"] - df["away_score"] > 0)
    df["outcome"] = df["outcome"].apply(int)
    df = df.drop(["home_score", "away_score"], axis=1)
    X, y = df.ix[:, df.columns != "outcome"], df["outcome"]
    X = scale(X) if scale_features else X
    return X, y

  def total(self, scale_features=False):
    df = self.all_boxscores.copy()\
      .drop(["home_team", "away_team", "date"], axis=1)
    df["total"] = df["home_score"] + df["away_score"]
    df["total"] = df["total"].apply(float)
    df = df.drop(["home_score", "away_score"], axis=1)
    X, y = df.ix[:, df.columns != "total"], df["total"]
    X = scale(X) if scale_features else X
    return X, y

  @staticmethod
  def split_home_and_away(df):
    home_cols = filter(lambda col: "home" in col or col == "date", df.columns)
    away_cols = filter(lambda col: "away" in col or col == "date", df.columns)
    home_df, away_df = df[home_cols], df[away_cols]
    home_df.columns = map(lambda col: col.replace("home_", ""), home_df.columns)
    away_df.columns = map(lambda col: col.replace("away_", ""), away_df.columns)
    return home_df, away_df

  @staticmethod
  def get_averages(df, n_last=None):
    if n_last:
      return df.sort_values(by="date").tail(n_last).drop(["team", "date"], axis=1).mean()
    else:
      return df.drop(["team", "date"], axis=1).mean()

  def input(self, home_team, away_team, weights, scale_features=False):
    home_df, away_df = self.split_home_and_away(self.season.copy())
    home_df = home_df.drop("score", axis=1)
    away_df = away_df.drop("score", axis=1)
    home_team_df = pd.concat([home_df[home_df["team"] == home_team], away_df[away_df["team"] == home_team]])
    away_team_df = pd.concat([home_df[home_df["team"] == away_team], away_df[away_df["team"] == away_team]])
    home_season, home_last_ten, home_last_five, home_last_three, home_last_one, home_at_home = \
      self.get_averages(home_team_df), self.get_averages(home_team_df, 10), self.get_averages(home_team_df, 5), self.get_averages(home_team_df, 3), self.get_averages(home_team_df, 1),\
      self.get_averages(home_df[home_df["team"] == home_team])
    away_season, away_last_ten, away_last_five, away_last_three, away_last_one, away_at_away = \
      self.get_averages(away_team_df), self.get_averages(away_team_df, 10), self.get_averages(away_team_df, 5), self.get_averages(away_team_df, 3), self.get_averages(home_team_df, 1),\
      self.get_averages(away_df[away_df["team"] == away_team])
    home_input = weights["season"]*home_season + weights["last_ten"]*home_last_ten + weights["last_five"]*home_last_five \
      + weights["last_three"]*home_last_three + weights["last_one"]*home_last_one + weights["hca"]*home_at_home
    away_input = weights["season"]*away_season + weights["last_ten"]*away_last_ten + weights["last_five"]*home_last_five + \
      weights["last_three"]*away_last_three + weights["last_one"]*away_last_one + weights["hca"]*away_at_away
    input_ = away_input.append(home_input)
    return scale(input_.values.reshape(1, -1)) if scale_features else input_.values.reshape(1, -1)
