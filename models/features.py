import pandas as pd

from indicators import (
    add_sma,
    add_ema,
    add_rsi,
    add_macd,
    add_bollinger
)


def add_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # ---------------------------
    # BASIC FEATURES
    # ---------------------------
    df["Return"] = df["Close"].pct_change()
    df["Momentum"] = df["Close"] - df["Close"].shift(5)
    df["Volatility"] = df["Return"].rolling(10).std()

    # ---------------------------
    # TECHNICAL INDICATORS
    # ---------------------------
    df = add_sma(df, 10)
    df = add_sma(df, 20)
    df = add_ema(df, 10)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_bollinger(df)

    # ---------------------------
    # TARGET LABEL
    # ---------------------------
    df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

    return df.dropna()
