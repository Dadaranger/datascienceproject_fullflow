import joblib
import numpy as np
import pandas as pd
from pathlib import Path


class PredictionPipeline:
    def __init__(self):
        self.model_path = joblib.load('artifacts/model_training/model.joblib')

    def prediction(self,data):
        prediction=self.model_path.predict(data)
        return prediction