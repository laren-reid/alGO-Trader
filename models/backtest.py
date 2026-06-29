import joblib
from train import FEATURE_COLUMNS


def backtest(df):

    df = df.copy()

    model = joblib.load("stock_model.pkl")

    X = df[FEATURE_COLUMNS]

    signals = model.predict(X)

    df["Signal"] = signals

    df["StrategyReturn"] = df["Signal"].shift(1) * df["Return"]

    cumulative = (1 + df["StrategyReturn"]).cumprod()

    return cumulative.iloc[-1]
