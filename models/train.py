import joblib

from features import add_features
from model import create_model


FEATURE_COLUMNS = [
    "SMA10",
    "SMA20",
    "Return",
    "Volatility",
    "Momentum"
]


def train(df):

    df = add_features(df)

    split = int(len(df) * 0.8)

    train_df = df.iloc[:split]

    X_train = train_df[FEATURE_COLUMNS]
    y_train = train_df["Target"]

    model = create_model()

    model.fit(X_train, y_train)

    joblib.dump(model, "stock_model.pkl")

    return model
