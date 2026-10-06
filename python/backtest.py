"""Simple annual back-test for the regime allocation framework."""

from __future__ import annotations
import pandas as pd
from regime_model import apply_regime, REGIME_WEIGHTS

ASSETS = list(REGIME_WEIGHTS["Balanced"].keys())

def backtest(df: pd.DataFrame) -> pd.DataFrame:
    x = apply_regime(df).copy()
    # Use the prior year's observable signals to set weights for the next year.
    x["Signal Year"] = x["Year"] - 1
    returns = x.set_index("Year")[ASSETS]
    rows = []
    for _, row in x.iterrows():
        year = int(row["Year"])
        if year < 2000:
            continue
        regime = row["Regime"]
        weights = REGIME_WEIGHTS[regime]
        r = sum(weights[a] * row[a] for a in ASSETS)
        rows.append({"Year": year, "Regime": regime, "Strategy Return": r, "S&P 500": row["S&P 500 TR"]})
    result = pd.DataFrame(rows)
    result["Strategy Wealth"] = (1 + result["Strategy Return"]).cumprod()
    result["S&P Wealth"] = (1 + result["S&P 500"]).cumprod()
    result["Strategy Peak"] = result["Strategy Wealth"].cummax()
    result["Drawdown"] = result["Strategy Wealth"] / result["Strategy Peak"] - 1
    return result

if __name__ == "__main__":
    df = pd.read_csv("data/historical_returns.csv")
    bt = backtest(df)
    print(bt.tail())
