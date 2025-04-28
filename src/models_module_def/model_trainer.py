import os
import joblib
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd

from sklearn.linear_model import ElasticNet
from src.entity import ModelTrainerConfig
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
        mlflow.set_experiment("Wine Quality Prediction")
    
    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def train(self):
        X_train = pd.read_csv(self.config.X_train_path)
        y_train = pd.read_csv(self.config.y_train_path)
        X_test = pd.read_csv(self.config.X_test_path)
        y_test = pd.read_csv(self.config.y_test_path)

        lr = ElasticNet(alpha = self.config.alpha, l1_ratio = self.config.l1_ratio, random_state=42)
        lr.fit(X_train, y_train)

        (rmse, mae, r2) = self.eval_metrics(y_test, lr.predict(X_test))
        joblib.dump(lr, os.path.join(self.config.root_dir, self.config.model_name))