import os
from datetime import datetime
from typing import Tuple
import joblib
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier


class Machine:
    """ Training, predicting and save/loading machine learning models"""

    def __init__(self, df: DataFrame, model_type="rfc"):
        """Train a model
        
        Args:
            df = Dataframe with monster data
            model_type = lr, rfc, or xgb"""
    
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #encode the target
        self.encoder = LabelEncoder()
        df["rarity"] = self.encoder.fit_transform(df["rarity"])

        #name each model
        if model_type == "lr":
            self.name = "LogisticRegression"
            self.model = LogisticRegression(max_iter=1000, random_state=42)
        elif model_type == "xgb":
            self.name = "XGBoostClassifier"
            self.model = XGBClassifier(eval_metric="logloss", random_state=42)
        elif model_type == "rfc":
            self.name = "RandomForestClassifier"
            self.model = RandomForestClassifier(random_state=42)

        self.target = df["rarity"]
        self.features = df.drop(columns=["rarity"])

        #scale features
        self.scaler = StandardScaler()
        self.features_scaled = self.scaler.fit_transform(self.features)

        #train model
        self.model.fit(self.features_scaled, self.target)

    def __call__(self, input_data) -> Tuple[str, float]:
        """Make a prediction"""
        if isinstance(input_data, dict):
            input_df = pd.DataFrame([input_data])
        else:
            input_df = input_data
        
        #apply scaling
        input_scaled = self.scaler.transform(input_df)

        pred_numeric = self.model.predict(input_scaled)[0]
        pred_label= self.encoder.inverse_transform([pred_numeric])[0]
        prob = float(self.model.predict_proba(input_scaled).max())
        
        return pred_label, prob

    def save(self, filepath:str):
        """Save model and encoder"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump((self.model, self.encoder, self.scaler, self.name, self.timestamp), filepath)

    @staticmethod
    def open(filepath:str):
        """Load model and encoder"""
        model, encoder, scaler, name, timestamp = joblib.load(filepath)

        #recreate model instance without retraining
        instance = Machine.__new__(Machine)
        instance.model = model
        instance.encoder = encoder
        instance.scaler = scaler
        instance.name = name
        instance.timestamp = timestamp
        return instance

    def info(self):
        return (f"Model: {self.name}, Trained: {self.timestamp}")
