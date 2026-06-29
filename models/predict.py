import joblib
import pandas as pd

from features import add_features
from train import FEATURE_COLUMNS


def generate_signal(prediction: int, confidence: float) -> str:

    BUY_THRESHOLD = 0.60
    SELL_THRESHOLD = 0.60
    HOLD_THRESHOLD = 0.60

    # If model is not confident → HOLD
    if confidence < HOLD_THRESHOLD:
        return "HOLD"

    # Confident prediction
    if prediction == 1:
        return "BUY"
    else:
        return "SELL"


def predict(df: pd.DataFrame):

    df = add_features(df)

    model = joblib.load("stock_model.pkl")

    X = df[FEATURE_COLUMNS].iloc[[-1]]

    prediction = model.predict(X)[0]
    confidence = max(model.predict_proba(X)[0])

    signal = generate_signal(prediction, confidence)

    return {
        "prediction": int(prediction),
        "confidence": float(confidence),
        "signal": signal
    }
