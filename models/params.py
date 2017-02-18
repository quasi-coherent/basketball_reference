SPREAD_PARAMS = {
  "n_estimators": 3200,
  "learning_rate": 0.05,
  "max_depth": 3,
  "min_samples_split": 200,
  "min_samples_leaf": 16,
  "max_features": 18,
  "subsample": 0.8
  } # 10-fold cv mae = 2.1245224337570034

TOTAL_PARAMS = {
  "n_estimators": 4800, 
  "learning_rate": 0.05, 
  "max_depth": 11,
  "min_samples_split": 1500, 
  "min_samples_leaf": 7,
  "max_features": 21,
  "subsample": 0.8
  } # 10-fold cv mae = 6.6020127663620887

MONEYLINE_PARAMS = {
  "n_estimators": 2900, 
  "learning_rate": 0.05, 
  "max_depth": 3,
  "min_samples_split": 950, 
  "min_samples_leaf": 8,
  "max_features": 8,
  "subsample": 0.8
  } # 10-fold cv acc = 0.95694114357612181