from fastapi import APIRouter
from ml.models.best_time_predictor import BestTimePredictor

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

@router.post("/train/best-time")
def train_best_time():
    model = BestTimePredictor()
    path, mae = model.train()
    return {"status": "trained", "model_path": path, "mae": mae}


@router.get("/predict/best-time")
def predict_best_time():
    model = BestTimePredictor()
    result = model.predict_best_hour_and_schedule()
    return result
