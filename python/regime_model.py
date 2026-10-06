"""Macro regime engine used as a transparent educational framework."""

from __future__ import annotations
import pandas as pd
import numpy as np

REGIME_WEIGHTS = {
    "Risk-on":     {"S&P 500 TR": .35, "US Small Cap TR": .10, "US 10Y T Bond TR": .10, "Baa Corp Bond TR": .10, "US Real Estate TR": .10, "Gold TR": .10, "3M T-Bill TR": .15},
    "Growth":      {"S&P 500 TR": .30, "US Small Cap TR": .10, "US 10Y T Bond TR": .15, "Baa Corp Bond TR": .10, "US Real Estate TR": .10, "Gold TR": .10, "3M T-Bill TR": .15},
    "Balanced":    {"S&P 500 TR": .20, "US Small Cap TR": .05, "US 10Y T Bond TR": .20, "Baa Corp Bond TR": .15, "US Real Estate TR": .15, "Gold TR": .15, "3M T-Bill TR": .10},
    "Defensive":   {"S&P 500 TR": .10, "US Small Cap TR": .00, "US 10Y T Bond TR": .25, "Baa Corp Bond TR": .20, "US Real Estate TR": .20, "Gold TR": .20, "3M T-Bill TR": .05},
}

def z_direction(current: float, previous: float) -> int:
    return 1 if current > previous else -1 if current < previous else 0

def build_signals(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["Rate Sig"] = np.sign(out["Fed Funds Avg"] - out["Fed Funds Avg"].shift(1)).fillna(0).astype(int)
    out["Energy Sig"] = -np.sign(out["Brent Avg ($/bbl)"] - out["Brent Avg ($/bbl)"].shift(1)).fillna(0).astype(int)
    out["Momentum Sig"] = np.sign(out["S&P 500 TR"]).fillna(0).astype(int)
    out["Credit Relative"] = out["Baa Corp Bond TR"] - out["US 10Y T Bond TR"]
    out["Credit Sig"] = np.where(out["Credit Relative"] > 0, 1, np.where(out["Credit Relative"] < 0, -1, 0))
    return out

def classify(score: int) -> str:
    if score >= 2:
        return "Risk-on"
    if score == 1:
        return "Growth"
    if score >= -1:
        return "Balanced"
    return "Defensive"

def apply_regime(df: pd.DataFrame) -> pd.DataFrame:
    x = build_signals(df)
    x["Score"] = x[["Rate Sig","Energy Sig","Momentum Sig","Credit Sig"]].sum(axis=1)
    x["Regime"] = x["Score"].apply(classify)
    return x

if __name__ == "__main__":
    data = pd.read_csv("data/historical_returns.csv")
    signals = apply_regime(data)
    print(signals[["Year","Score","Regime"]].tail())
