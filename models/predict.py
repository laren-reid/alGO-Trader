import joblib
import pandas as pd

from features import add_features
from train import FEATURE_COLUMNS


def generate_signal(prediction: int, confidence: float) -> str:

    CONFIDENCE_THRESHOLD = 0.70

    if confidence < CONFIDENCE_THRESHOLD:
        return "HOLD"

    if prediction == 1:
        return "BUY"
    else:
        return "SELL"


def predict(df: pd.DataFrame):

    # ---------------------------
    # Feature engineering
    # ---------------------------
    df = add_features(df)

    # ---------------------------
    # Load trained model
    # ---------------------------
    model = joblib.load("stock_model.pkl")

    # ---------------------------
    # Get latest data point ONLY
    # ---------------------------
    X = df[FEATURE_COLUMNS].iloc[[-1]]

    # ---------------------------
    # Prediction
    # ---------------------------
    prediction = model.predict(X)[0]

    confidence = max(model.predict_proba(X)[0])

    # ---------------------------
    # Convert to trading signal
    # ---------------------------
    signal = generate_signal(prediction, confidence)

    return {
        "prediction": int(prediction),
        "confidence": float(confidence),
        "signal": signal
    }
