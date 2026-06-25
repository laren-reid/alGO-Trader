def backtest(model, df, features):

    df = df.copy()

    df["signal"] = model.predict(df[features])

    df["strategy_return"] = df["signal"].shift(1) * df["Return"]

    cumulative = (1 + df["strategy_return"]).cumprod()

    return cumulative.iloc[-1]
