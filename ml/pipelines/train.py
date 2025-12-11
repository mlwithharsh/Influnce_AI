import os
import yaml
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error


CONFIG_PATH = "ml/config/model_config.yaml"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def train_best_time_model():
    cfg = load_config()

    df = pd.read_csv(cfg["feature_csv"])

    # Clean numeric features
    df = df.dropna(subset=["hour_sin", "hour_cos", "engagement_score"])

    X = df[["day", "platform", "hour_sin", "hour_cos"]]
    y = df["engagement_score"]

    pre = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["day", "platform"]),
        ],
        remainder="passthrough"
    )

    model = xgb.XGBRegressor(
        n_estimators=cfg["n_estimators"],
        max_depth=cfg["max_depth"],
        learning_rate=cfg["learning_rate"],
        random_state=cfg["random_state"]
    )

    pipeline = Pipeline([("pre", pre), ("model", model)])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=cfg["test_size"],
        random_state=cfg["random_state"]
    )

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    mae = float(mean_absolute_error(y_test, preds))

    os.makedirs("ml/models", exist_ok=True)

    joblib.dump(pipeline, cfg["model_path"])
    json.dump({"MAE": mae}, open(cfg["meta_path"], "w"))

    return {"message": "Training complete", "MAE": mae, "model_path": cfg["model_path"]}

if __name__ == "__main__":
    print(train_best_time_model())
