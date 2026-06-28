import joblib

from features import add_features
from train import FEATURE_COLUMNS


def predict(df):

    df = add_features(df)

    model = joblib.load("stock_model.pkl")

    latest = df[FEATURE_COLUMNS].iloc[[-1]]

    prediction = model.predict(latest)[0]

    confidence = model.predict_proba(latest)[0][1]

    return {
        "prediction": int(prediction),
        "confidence": float(confidence)
    }
