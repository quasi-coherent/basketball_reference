import pandas as pd

class StackedPreprocessor(object):
  def __init__(self, path):
    _all = pd.read_json(path, convert_dates=["date"], lines=True)\
      .sort_values(by="date").reset_index()\
      .rename(columns={"index": "gid"})
    _all["season"] = _all.date.apply(lambda x: x.year if x.month in range(1, 7) else x.year + 1)
    self.scores = _all[["date", "gid", "home_score", "away_score"]]
    # avoid data leakage by dropping features that implicitly incorporate points scored
    self.all_boxscores = _all.drop(
      ["home_ortg", "home_drtg", "away_ortg", "away_drtg", "home_score", "away_score"], axis=1)

  @staticmethod
  def home_and_away(df):
    home_cols = filter(lambda col: "home" in col, df.columns) + ["season", "date", "gid"]
    away_cols = filter(lambda col: "away" in col, df.columns) + ["season", "date", "gid"]
    home_df, away_df = df[home_cols], df[away_cols]
    home_df.columns = map(lambda col: col.replace("home_", ""), home_df.columns)
    away_df.columns = map(lambda col: col.replace("away_", ""), away_df.columns)
    return home_df, away_df

  @staticmethod
  def windowed_average(df, window, min_periods=None):
    averages = df.groupby(["season", "team"])\
      .apply(lambda x: x.shift(1).rolling(window=window, min_periods=min_periods).mean())
    return averages

  def last_n_average(self, window, min_periods=None):
    home_df, away_df = self.home_and_away(self.all_boxscores.copy())
    home_df["is_home"] = 1
    away_df["is_home"] = 0
    team_stats = pd.concat([home_df, away_df])\
      .sort_values(by="date")\
      .reset_index(drop=True)
    gid = team_stats[["gid", "is_home"]]
    last_n_avg = self.windowed_average(
        team_stats.drop(["date", "gid", "is_home"], axis=1), window, min_periods)\
      .drop("season", axis=1)
    joined = gid.merge(last_n_avg, left_index=True, right_index=True)\
      .dropna()
    home_last_n = joined[joined["is_home"] == 1].drop("is_home", axis=1)
    away_last_n = joined[joined["is_home"] == 0].drop("is_home", axis=1)
    df = home_last_n.merge(away_last_n, on="gid", suffixes=("_home", "_away"))
    df.columns = map(lambda col: col.split("_")[1] + "_" + col.split("_")[0] if col != "gid" else col, df.columns)
    return df.merge(self.scores, on="gid").drop("gid", axis=1)

  def location_average(self, window=105, min_periods=1):
    home_df, away_df = self.home_and_away(self.all_boxscores.copy())
    home_gid, away_gid = pd.DataFrame(home_df["gid"]), pd.DataFrame(away_df["gid"])
    home_season_avg = home_gid.merge(
      self.windowed_average(home_df.drop(["date", "gid"], axis=1), window, min_periods),
      left_index=True, right_index=True)
    away_season_avg = away_gid.merge(
      self.windowed_average(away_df.drop(["date", "gid"], axis=1), window, min_periods),
      left_index=True, right_index=True)
    df = home_season_avg.merge(away_season_avg, on="gid", suffixes=("_home", "_away"))\
      .dropna()
    df.columns = map(lambda col: col.split("_")[1] + "_" + col.split("_")[0] if col != "gid" else col, df.columns)
    return df.merge(self.scores, on="gid").drop("gid", axis=1)

  def moneyline_train(self, window, min_periods=None):
    last_n = self.last_n_average(window, min_periods)
    last_n["outcome"] = last_n["home_score"] - last_n["away_score"] > 0
    last_n["outcome"] = last_n["outcome"].apply(int)
    last_n = last_n.drop(["home_score", "away_score"], axis=1)
    return last_n.ix[:, last_n.columns != "outcome"], last_n["outcome"]

  def spread_train(self, window, min_periods=None):
    last_n = self.last_n_average(window, min_periods)
    last_n["spread"] = last_n["home_score"] - last_n["away_score"]
    last_n["spread"] = last_n["spread"].apply(float)
    last_n = last_n.drop(["home_score", "away_score"], axis=1)    
    return last_n.ix[:, last_n.columns != "spread"], last_n["spread"]

  def total_train(self, window, min_periods=None):
    last_n = self.last_n_average(window, min_periods)
    last_n["total"] = last_n["home_score"] + last_n["away_score"]
    last_n["total"] = last_n["total"].apply(float)
    last_n = last_n.drop(["home_score", "away_score"], axis=1)
    return last_n.ix[:, last_n.columns != "total"], last_n["total"]