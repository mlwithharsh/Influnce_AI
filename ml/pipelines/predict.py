import joblib
import pandas as pd
import math
import yaml

CONFIG_PATH = "ml/config/model_config.yaml"


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def load_model():
    cfg = load_config()
    return joblib.load(cfg["model_path"])


def predict_best_time(platform="instagram"):
    model = load_model()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    rows = []
    for day in days:
        for hour in range(24):
            hour_sin = math.sin(2 * math.pi * hour / 24)
            hour_cos = math.cos(2 * math.pi * hour / 24)
            rows.append({"day": day, "platform": platform, "hour_sin": hour_sin, "hour_cos": hour_cos})

    df = pd.DataFrame(rows)
    preds = model.predict(df)

    best_idx = preds.argmax()
    best_day = df.iloc[best_idx]["day"]
    best_hour = best_idx % 24

    return {
        "best_day": best_day,
        "best_hour": best_hour,
        "predicted_engagement": float(preds[best_idx])
    }
