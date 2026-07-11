import os
import sys

import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import FEATURE_COLUMNS, CONFIDENCE_THRESHOLD
from features import add_features


def backtest(model, df: pd.DataFrame, confidence_threshold: float = CONFIDENCE_THRESHOLD, cost_per_trade: float = 0.0):
    """
    Simulates the strategy that predict.py's generate_signal() actually
    produces: BUY (long), SELL (short), or HOLD (flat) depending on the
    model's confidence. Previously this backtest ignored confidence
    entirely and was always long or short, which meant a "good backtest"
    didn't reflect what predict.py would actually do live.

    cost_per_trade: fractional cost applied whenever the position changes
    (e.g. 0.001 = 10 bps per side). Defaults to 0 so behavior matches the
    original zero-cost version unless you opt in.

    IMPORTANT: pass a `df` the model was NOT trained on. Backtesting over
    the same rows used in model.fit() is in-sample testing and will look
    much better than live performance, because the model has partially
    memorized that data. Use features.chronological_split() to get the
    same held-out slice train.py evaluated on, e.g.:

        full_df = add_features(raw_df)
        _, test_df = chronological_split(full_df)
        backtest(model, test_df[["Open","High","Low","Close","Volume"]])
    """

    df = add_features(df).copy()

    probs = model.predict_proba(df[FEATURE_COLUMNS])
    predictions = model.predict(df[FEATURE_COLUMNS])
    confidences = probs.max(axis=1)

    df["Signal"] = predictions
    df["Confidence"] = confidences

    # ---------------------------
    # Map signals -> position, respecting the confidence threshold
    # ---------------------------
    raw_position = np.where(df["Signal"] == 1, 1, -1)
    df["Position"] = np.where(df["Confidence"] >= confidence_threshold, raw_position, 0)

    # ---------------------------
    # Market returns
    # ---------------------------
    df["MarketReturn"] = df["Close"].pct_change()

    # ---------------------------
    # Strategy returns (position lagged by 1 day so today's signal is
    # acted on starting tomorrow - avoids lookahead bias)
    # ---------------------------
    lagged_position = df["Position"].shift(1).fillna(0)
    df["StrategyReturn"] = lagged_position * df["MarketReturn"]

    if cost_per_trade > 0:
        position_changed = lagged_position.diff().abs().fillna(0)
        df["TransactionCost"] = position_changed * cost_per_trade
        df["StrategyReturn"] = df["StrategyReturn"] - df["TransactionCost"]

    df["CumulativeReturn"] = (1 + df["StrategyReturn"].fillna(0)).cumprod()
    df["BuyHoldReturn"] = (1 + df["MarketReturn"].fillna(0)).cumprod()

    n_days = len(df)
    n_trades = int((lagged_position.diff().fillna(0) != 0).sum())

    return {
        "final_return": float(df["CumulativeReturn"].iloc[-1]),
        "buy_hold_return": float(df["BuyHoldReturn"].iloc[-1]),
        "num_trades": n_trades,
        "num_days": n_days,
        "data": df
    }
