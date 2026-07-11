"""
Demo script for the algo-trader ML module.

Runs the full pipeline end to end:
1. Get historical price data (real data via yfinance if available/online, otherwise a synthetic random-walk fallback so the demo still runs offline)
2. Train the model, printing held-out evaluation metrics
3. Generate a live prediction/signal from the most recent data
4. Backtest strictly on held-out (out-of-sample) data, with a buy-and-hold comparison and an optional transaction-cost scenario

Usage:
    python demo.py                # uses default ticker (AAPL)
    python demo.py TSLA           # or pass any ticker
    python demo.py TSLA --synthetic   # force synthetic data (skip yfinance)
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "models"))

import numpy as np
import pandas as pd


def make_synthetic_data(n: int = 750, seed: int = 42) -> pd.DataFrame:
    """Random-walk OHLCV data. Used when yfinance/network isn't available,
    just so the pipeline can still be demoed offline. This has no real
    predictive structure, so don't read anything into the resulting
    accuracy/returns beyond 'the code runs'."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2023-01-01", periods=n, freq="B")
    returns = rng.normal(0.0003, 0.015, n)
    close = 100 * np.cumprod(1 + returns)

    df = pd.DataFrame({
        "Open": close * (1 + rng.normal(0, 0.002, n)),
        "High": close * (1 + np.abs(rng.normal(0, 0.005, n))),
        "Low": close * (1 - np.abs(rng.normal(0, 0.005, n))),
        "Close": close,
        "Volume": rng.integers(1_000_000, 5_000_000, n),
    }, index=dates)
    return df


def get_data(ticker: str, force_synthetic: bool) -> tuple[pd.DataFrame, bool]:
    """Returns (df, used_synthetic)."""
    if not force_synthetic:
        try:
            from data_fetcher import get_historical_data
            df = get_historical_data(ticker, "2022-01-01", "2026-07-11")
            if not df.empty and len(df) > 100:
                return df, False
            print(f"[Demo] yfinance returned insufficient data for {ticker}, falling back to synthetic data.")
        except Exception as e:
            print(f"[Demo] Couldn't fetch live data ({e}); falling back to synthetic data.")

    return make_synthetic_data(), True


def main():
    parser = argparse.ArgumentParser(description="Demo the algo-trader ML pipeline end to end.")
    parser.add_argument("ticker", nargs="?", default="AAPL", help="Stock ticker to use (default: AAPL)")
    parser.add_argument("--synthetic", action="store_true", help="Skip yfinance and use synthetic data")
    parser.add_argument("--cost", type=float, default=0.001, help="Per-trade transaction cost for the backtest scenario (default: 0.001 = 10bps)")
    args = parser.parse_args()

    from features import add_features, chronological_split
    from train import train
    from predict import predict
    from backtest import backtest

    print("=" * 60)
    print(f"ALGO-TRADER DEMO — ticker: {args.ticker}")
    print("=" * 60)

    df, used_synthetic = get_data(args.ticker, args.synthetic)
    source = "SYNTHETIC (random walk — for demo purposes only, no real signal)" if used_synthetic else "yfinance (real data)"
    print(f"\n[1/4] Data source: {source}")
    print(f"      Rows: {len(df)}  |  Date range: {df.index[0].date()} to {df.index[-1].date()}")

    print("\n[2/4] Training model (chronological 80/20 split, held-out evaluation)...")
    model, metrics = train(df, verbose=True)

    print("\n[3/4] Generating live prediction from most recent data...")
    result = predict(df)
    print(f"      Prediction: {'UP' if result['prediction'] == 1 else 'DOWN'}")
    print(f"      Confidence: {result['confidence']*100:.1f}%")
    print(f"      Signal:     {result['signal']}")

    print("\n[4/4] Backtesting on held-out data only (out-of-sample — not the rows used to train)...")
    full_features = add_features(df)
    _, test_features = chronological_split(full_features)
    test_raw = df.loc[test_features.index]

    bt = backtest(model, test_raw)
    print(f"      Zero-cost strategy return: {bt['final_return']:.3f}x  ({(bt['final_return']-1)*100:+.1f}%)")
    print(f"      Buy-and-hold return:       {bt['buy_hold_return']:.3f}x  ({(bt['buy_hold_return']-1)*100:+.1f}%)")
    print(f"      Number of trades:          {bt['num_trades']}")

    bt_cost = backtest(model, test_raw, cost_per_trade=args.cost)
    print(f"\n      With {args.cost*100:.2f}% cost per trade: {bt_cost['final_return']:.3f}x  ({(bt_cost['final_return']-1)*100:+.1f}%)")

    print("\n" + "=" * 60)
    if used_synthetic:
        print("NOTE: results above are on synthetic random-walk data and are")
        print("not meaningful as trading performance — re-run with a real")
        print("ticker (requires yfinance + network) for anything real.")
    print("Done. Trained model saved via train.py to models/stock_model.pkl")
    print("=" * 60)


if __name__ == "__main__":
    main()
