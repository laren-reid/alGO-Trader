import pandas as pd
import joblib

from features import add_features
from model import train_model


def train(ticker):

    df = pd.read_csv(f"data/{ticker}.csv")

    df = add_features(df)

    features = ["SMA10", "SMA20", "Return", "Volatility", "Momentum"]

    split = int(len(df) * 0.8)

    X_train = df[features][:split]
    y_train = df["Target"][:split]

    model = train_model(X_train, y_train)

    joblib.dump(model, f"models/{ticker}_model.pkl")

    return model
