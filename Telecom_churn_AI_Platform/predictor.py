
import os

import numpy as np
import joblib
import pandas as pd

class ChurnPredictor(object):

  _COLUMN_NAMES=['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling','PaymentMethod', 'MonthlyCharges', 'TotalCharges']

  def __init__(self, model):
    self._model = model

  def predict(self, instances, **kwargs):
    inputs = pd.DataFrame(data=[instances], columns=self._COLUMN_NAMES)
    outputs = self._model.predict(inputs)
    return outputs.tolist()

  @classmethod
  def from_path(cls, model_dir):
    model_path = os.path.join(model_dir, 'model.joblib')
    model = joblib.load(model_path)
    return cls(model)
