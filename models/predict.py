import joblib
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


def predict(df):

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
