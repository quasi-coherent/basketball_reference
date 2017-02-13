import numpy as np

GBT_PARAM_GRID = {"learning_rate": np.linspace(.01, .1, 5), 
  "n_estimators": np.linspace(100, 1000, 10, dtype=int), 
  "max_depth": np.arange(2, 9, 2, dtype=int),
  "min_samples_leaf": np.arange(3, 13, 3, dtype=int)}

GBT_PARAMS = {"n_estimators": 700, 
  "learning_rate": 0.1, 
  "max_depth": 3, 
  "min_samples_leaf": 6}