import pandas as pd
import numpy as np

from train import FEATURE_COLUMNS
from features import add_features


def backtest(model, df: pd.DataFrame):

    df = add_features(df).copy()

    predictions = model.predict(df[FEATURE_COLUMNS])

    # ---------------------------
    # Map signals
    # ---------------------------
    df["Signal"] = predictions

    df["Position"] = df["Signal"].map({
        1: 1,     # BUY → long
        0: -1     # SELL → short
    })

    # HOLD = 0 position
    df["Position"] = df["Position"].fillna(0)

    # ---------------------------
    # Market returns
    # ---------------------------
    df["MarketReturn"] = df["Close"].pct_change()

    # ---------------------------
    # Strategy returns
    # ---------------------------
    df["StrategyReturn"] = df["Position"].shift(1) * df["MarketReturn"]

    df["CumulativeReturn"] = (1 + df["StrategyReturn"].fillna(0)).cumprod()

    return {
        "final_return": float(df["CumulativeReturn"].iloc[-1]),
        "data": df
    }
