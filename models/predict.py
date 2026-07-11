import os
import sys

import joblib
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import FEATURE_COLUMNS, MODEL_PATH, CONFIDENCE_THRESHOLD
from features import add_features


def generate_signal(prediction: int, confidence: float) -> str:
    # If model is not confident -> HOLD
    if confidence < CONFIDENCE_THRESHOLD:
        return "HOLD"

    # Confident prediction
    return "BUY" if prediction == 1 else "SELL"


def predict(df: pd.DataFrame):

    df = add_features(df)

    if df.empty:
        raise ValueError(
            "No rows left after feature engineering - not enough price history "
            "was provided (indicators like SMA20/MACD need warm-up data before "
            "the first row is usable)."
        )

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"No trained model found at {MODEL_PATH}. Run train.py first."
        )

    model = joblib.load(MODEL_PATH)

    X = df[FEATURE_COLUMNS].iloc[[-1]]

    prediction = model.predict(X)[0]
    confidence = max(model.predict_proba(X)[0])

    signal = generate_signal(prediction, confidence)

    return {
        "prediction": int(prediction),
        "confidence": float(confidence),
        "signal": signal
    }

