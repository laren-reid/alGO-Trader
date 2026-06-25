import pandas as pd
import joblib

from features import add_features


def predict(ticker):

    model = joblib.load(f"models/{ticker}_model.pkl")

    df = pd.read_csv(f"data/{ticker}.csv")

    df = add_features(df)

    features = ["SMA10", "SMA20", "Return", "Volatility", "Momentum"]

    latest = df[features].iloc[[-1]]

    prediction = model.predict(latest)[0]

    confidence = model.predict_proba(latest)[0][1]

    return {
        "prediction": int(prediction),
        "confidence": float(confidence)
    }
