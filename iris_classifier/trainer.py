import os

import joblib
import pandas as pd
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler

from config import config

FEATURES_NAMES = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
FEATURES_TO_NORMALIZE = ['sepal_length', 'sepal_width', 'petal_length']

MODEL_FILE_NAME = 'model.pkl'
NORMALIZER_FILE_NAME = 'normalizer.pkl'


class ModelTrainer:
    def __init__(self, penalty='l2', tol=1e-4, C=1.0, max_iter=100):
        # Model artifacts
        self.model = None
        self.normalizer = MinMaxScaler()
        # Hyper params
        self.penalty = penalty
        self.tol = tol
        self.C = C
        self.max_iter = max_iter
        # Data
        self.train_df = None
        self.target = None

    def prepare_data(self):
        dataset = datasets.load_iris()
        self.train_df = pd.DataFrame(dataset.data, columns=FEATURES_NAMES)
        self.train_df[FEATURES_TO_NORMALIZE] = self.normalizer.fit_transform(self.train_df[FEATURES_TO_NORMALIZE])
        self.target = dataset.target

    def fit(self):
        self.model = LogisticRegression(penalty=self.penalty,
                                        tol=self.tol,
                                        C=self.C,
                                        max_iter=self.max_iter)
        self.model.fit(self.train_df, self.target)

    def eval(self):
        # Not implemented for this example...
        pass

    def save(self):
        if not os.path.isdir(config.LOCAL_MODEL_DIR):
            os.mkdir(config.LOCAL_MODEL_DIR)

        model_path = os.path.join(config.LOCAL_MODEL_DIR, MODEL_FILE_NAME)
        joblib.dump(self.model, model_path)

        normalizer_path = os.path.join(config.LOCAL_MODEL_DIR, NORMALIZER_FILE_NAME)
        joblib.dump(self.normalizer, normalizer_path)

    def run(self):
        self.prepare_data()
        self.fit()
        self.eval()
        self.save()
