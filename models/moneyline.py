from sklearn.model_selection import cross_val_score, GridSearchCV

class MoneylineClassifier(object):
  def __init__(self, features, response, model):
    self.features = features
    self.response = response
    self.model = model

  def grid_search(self, param_space):
    assert isinstance(param_space, dict)
    clf = GridSearchCV(self.model, param_space)
    clf.fit(self.features, self.response)
    return clf.best_params_

  def cv_score(self, n_folds=10):
    score = cross_val_score(self.model, self.features, self.response, n_jobs=-1)
    return score.mean()

  def train(self):
    self.model.fit(self.features, self.response)
    return self.model
    
  def predict(self, inputs):
    return self.model.predict(inputs)[0]

  def predict_prob(self, inputs):
    return self.model.predict_proba(inputs)[0]

  def predict_historical(self):
    return self.model.predict(self.features)