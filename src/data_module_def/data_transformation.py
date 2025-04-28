import os
import pandas as pd
from sklearn.model_selection import train_test_split
from custom_logger import logger
from src.entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def train_test_splitting(self):
        data = pd.read_csv(self.config.data_path)

        X = data.drop(columns=["quality"])
        y = data["quality"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train.to_csv(os.path.join(self.config.root_dir, "X_train.csv"), index = False)
        y_train.to_csv(os.path.join(self.config.root_dir, "y_train.csv"), index = False)
        X_test.to_csv(os.path.join(self.config.root_dir, "X_test.csv"), index = False)
        y_test.to_csv(os.path.join(self.config.root_dir, "y_test.csv"), index = False)

        logger.info("Splitted data into training and test sets")
        logger.info(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
        logger.info(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")

        print(X_train.shape, y_train.shape)
        print(X_test.shape, y_test.shape)