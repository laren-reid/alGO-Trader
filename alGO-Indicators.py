import yfinance as yf
import pandas as pd
import numpy as np

def add_sma(df: pd.DataFrame, window: int) -> pd.DataFrame:
    df[f"sma_{window}"] = df["Close"].rolling(window).mean()
    return df


def add_ema(df: pd.DataFrame, window: int) -> pd.DataFrame:
    df[f"ema_{window}"] = df["Close"].ewm(span=window, adjust=False).mean()
    return df

def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    df["rsi"] = 100 - (100 / (1 + rs))
    return df

def add_macd(df: pd.DataFrame) -> pd.DataFrame:
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]
    return df

def add_bollinger(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    sma = df["Close"].rolling(window).mean()
    std = df["Close"].rolling(window).std()
    upper = sma + 2 * std
    lower = sma - 2 * std
    df["bb_position"] = (df["Close"] - lower) / (upper - lower + 1e-9)
    return df
