import os
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import joblib
from pathlib import Path
from urllib.parse import urlparse
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from pipeline.entity import ModelEvaluationConfig
from pipeline.common_utils import save_json

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2
    
    def log_into_mlflow(self):
        X_test = pd.read_csv(self.config.X_test_path)
        y_test = pd.read_csv(self.config.y_test_path)
        model = joblib.load(self.config.model_path)

        mlflow.set_registry_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            predicted_qualities = model.predict(X_test)

            (rmse, mae, r2) = self.eval_metrics(y_test, predicted_qualities)

            # Saving metrics as local
            scores = {"rmse": rmse, "mae": mae, "r2": r2}
            save_json(path=Path(self.config.metric_file_name), data=scores)

            mlflow.log_params(self.config.all_params)

            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("r2", r2)

            # Model registry does not work with file store
            if tracking_url_type_store != "file":

                # Register the model
                # There are other ways to use the Model Registry, which depends on the use case.

                mlflow.sklearn.log_model(model, "model", registered_model_name="ElasticnetModel")

            else:
                mlflow.sklearn.log_model(model, "model")           
