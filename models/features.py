import os
import sys
import pandas as pd

# indicators.py lives in the project root, one level above this file's
# directory (models/). Add the root to sys.path so this import works
# regardless of the working directory the script is launched from.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    # Percentage change over 5 days rather than raw price difference, so the
    # feature means the same thing for a $20 stock and a $500 stock.
    df["Momentum"] = df["Close"].pct_change(periods=5)
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


def chronological_split(df: pd.DataFrame, train_frac: float = 0.8):
    """
    Splits a (feature-engineered) DataFrame into train/test by time order -
    no shuffling, since shuffling time series leaks future rows into training.

    Use the same split here for both train.py and backtest.py so that
    "backtest performance" means "performance on data the model never saw
    during fitting" rather than in-sample performance, which is
    systematically inflated (the model has partially memorized that data).
    """
    split = int(len(df) * train_frac)
    return df.iloc[:split], df.iloc[split:]
