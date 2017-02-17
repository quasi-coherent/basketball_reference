import numpy as np

GBT_PARAM_GRID = {
"learning_rate": np.linspace(.01, .1, 5), 
  "n_estimators": np.linspace(100, 1000, 10, dtype=int), 
  "max_depth": np.arange(2, 9, 2, dtype=int),
  "min_samples_leaf": np.arange(3, 13, 3, dtype=int)
  }

SPREAD_PARAMS = {
  "n_estimators": 1000, 
  "learning_rate": 0.077499999999999999, 
  "max_depth": 4, 
  "min_samples_leaf": 9
  } # 10-fold cv mse = 2.2195449662105586

TOTAL_PARAMS = {
  "n_estimators": 1000, 
  "learning_rate": 0.10000000000000001, 
  "max_depth": 6, 
  "min_samples_leaf": 3
  } # 10-fold cv mse = 6.8113635379557733

MONEYLINE_PARAMS = {
  "n_estimators": 1000, 
  "learning_rate": 0.10000000000000001, 
  "max_depth": 2, 
  "min_samples_leaf": 12
  } # 10-fold cv acc = 0.95692757982276833

# MONEYLINE_PARAMS = {
#   'n_estimators': 1250, 
#   'learning_rate': 0.077499999999999999, 
#   'max_depth': 2, 
#   'min_samples_leaf': 6
#   }

# SPREAD_PARAMS2 = {
#   'n_estimators': 2000, 
#   'learning_rate': 0.10000000000000001, 
#   'max_depth': 2, 
#   'min_samples_leaf': 12
#   }

# TOTAL_PARAMS2 = {
#   'n_estimators': 1500, 
#   'learning_rate': 0.10000000000000001, 
#   'max_depth': 6, 
#   'min_samples_leaf': 3
#   } # 10-fold cv mae = 6.7273007001488194

# TOTAL_PARAMS3 = {
#   'n_estimators': 2000, 
#   'learning_rate': 0.10000000000000001, 
#   'max_depth': 4, 
#   'min_samples_leaf': 3
#   } # 10-fold cv: mae = 6.6539591890139587