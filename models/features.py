def add_features(df):

    df["Return"] = df["Close"].pct_change()

    df["SMA10"] = df["Close"].rolling(10).mean()
    df["SMA20"] = df["Close"].rolling(20).mean()

    df["Volatility"] = df["Return"].rolling(10).std()

    df["Momentum"] = df["Close"] - df["Close"].shift(5)

    df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

    return df.dropna()
