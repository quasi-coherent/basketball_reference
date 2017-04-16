from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import make_scorer, mean_absolute_error

class SpreadAndTotalRegressor(object):
  def __init__(self, features, response, model):
    self.features = features
    self.response = response
    self.model = model

  def grid_search(self, param_space):
    assert isinstance(param_space, dict)
    rgr = GridSearchCV(self.model, param_space)
    rgr.fit(self.features, self.response)
    return rgr.best_params_

  def cv_score(self, n_folds=10):
    score = cross_val_score(self.model, self.features, self.response, 
      cv=n_folds, scoring=make_scorer(mean_absolute_error, greater_is_better=False),
      n_jobs=-1)
    return score.mean()

  def train(self):
    self.model.fit(self.features, self.response)
    return self.model

  def predict(self, inputs):
    return self.model.predict(inputs)[0]

  def predict_historical(self):
    return self.model.predict(self.features)