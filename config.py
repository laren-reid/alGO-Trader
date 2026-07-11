"""
Shared configuration for the ML trading module.
Keeping these constants in one place avoids the old problem of
predict.py importing from train.py just to get FEATURE_COLUMNS.
"""

import os

# Directory this file lives in - used to build absolute paths so the
# code works no matter what directory it's launched from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "stock_model.pkl")

FEATURE_COLUMNS = [
    "Return",
    "Momentum",
    "Volatility",

    "sma_10",
    "sma_20",
    "ema_10",

    "rsi",
    "macd",
    "macd_signal",
    "macd_hist",

    "bb_position"
]

# Single source of truth for the confidence cutoff used both when
# generating a live signal (predict.py) and when simulating the
# strategy (backtest.py).
CONFIDENCE_THRESHOLD = 0.60
