import os
import json
import joblib
import pandas as pd
import numpy as np
import xgboost as xgb
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal
from backend.app.db.models import PostAnalytics
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

MODEL_DIR = "ml/models"
MODEL_PATH = os.path.join(MODEL_DIR, "best_time_predictor.pkl")
COLUMNS_PATH = os.path.join(MODEL_DIR, "best_time_columns.json")


class BestTimePredictor:
    def __init__(self):
        self.model = None
        self.columns = None

        if os.path.exists(MODEL_PATH) and os.path.exists(COLUMNS_PATH):
            self.load_trained_model()

    def load_data_from_db(self):
        db: Session = SessionLocal()
        posts = db.query(PostAnalytics).all()
        db.close()

        if not posts:
            raise ValueError("No PostAnalytics records found in database")

        rows = []
        for p in posts:
            rows.append({
                "posted_at": p.posted_at,
                "likes": p.likes,
                "comments": p.comments,
                "views": p.views
            })

        df = pd.DataFrame(rows)

        # Convert timestamps
        df["posted_at"] = pd.to_datetime(df["posted_at"], unit="s")
        df["published_hour"] = df["posted_at"].dt.hour
        df["publish_dayofweek"] = df["posted_at"].dt.dayofweek

        # Correct engagement formula
        df["engagement"] = df["likes"] * 5 + df["comments"] * 10

        df.dropna(inplace=True)

        return df

    def train(self):
        df = self.load_data_from_db()

        X = df[["published_hour", "publish_dayofweek"]]
        X = pd.get_dummies(X)
        y = df["engagement"]

        os.makedirs(MODEL_DIR, exist_ok=True)

        # Save columns order
        with open(COLUMNS_PATH, "w") as f:
            json.dump(list(X.columns), f)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, shuffle=True
        )

        model = xgb.XGBRegressor(
            n_estimators=350,
            max_depth=6,
            learning_rate=0.05,
            verbosity=0
        )

        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)

        joblib.dump(model, MODEL_PATH)
        self.model = model
        self.columns = list(X.columns)

        print("Model trained successfully | MAE:", mae)
        return MODEL_PATH, mae

    def load_trained_model(self):
        self.model = joblib.load(MODEL_PATH)
        self.columns = json.load(open(COLUMNS_PATH, "r"))

    def predict_best_hour_and_schedule(self):
        if self.model is None:
            raise RuntimeError("Model not trained or loaded.")

        hourly_scores = []

        for day in range(7):
            for hour in range(24):
                row = pd.DataFrame([[hour, day]], columns=["published_hour", "publish_dayofweek"])
                row = pd.get_dummies(row)

                for col in self.columns:
                    if col not in row.columns:
                        row[col] = 0

                row = row[self.columns]
                pred = self.model.predict(row)[0]
                hourly_scores.append((day, hour, pred))

        best = max(hourly_scores, key=lambda x: x[2])

        return {
            "best_day": best[0],
            "best_hour": best[1],
            "expected_engagement": float(best[2])
        }
