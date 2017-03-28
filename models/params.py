SPREAD_PARAMS = {
  "n_estimators": 8838,
  "learning_rate": 0.025,
  "max_depth": 3,
  "min_samples_split": 200,
  "min_samples_leaf": 16,
  "max_features": 18,
  "subsample": 0.8
  } # 10-fold cv mae = 2.1364707559295621

TOTAL_PARAMS = {
  "n_estimators": 14383, 
  "learning_rate": 0.025, 
  "max_depth": 11,
  "min_samples_split": 1500, 
  "min_samples_leaf": 7,
  "max_features": 21,
  "subsample": 0.8
  } # 10-fold cv mae = 6.55831769692

MONEYLINE_PARAMS = {
  "n_estimators": 5734, 
  "learning_rate": 0.025, 
  "max_depth": 3,
  "min_samples_split": 950, 
  "min_samples_leaf": 8,
  "max_features": 8,
  "subsample": 0.8
  } # 10-fold cv acc = .95740714851577424

WEIGHTS = {
  "season": 0.00,
  "last_ten": 0.15,  
  "last_five": 0.40,
  "last_three": 0.30,
  "last_one": 0.10,
  "hca": 0.10
}