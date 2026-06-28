from train import FEATURE_COLUMNS


def backtest(model, df):

    df = df.copy()

    signals = model.predict(df[FEATURE_COLUMNS])

    df["Signal"] = signals

    df["StrategyReturn"] = (
        df["Signal"].shift(1) * df["Return"]
    )

    cumulative = (
        1 + df["StrategyReturn"]
    ).cumprod()

    return cumulative.iloc[-1]
