"""Portfolio risk diagnostics used by the research project."""

from __future__ import annotations
import numpy as np

def max_drawdown(returns):
    wealth = np.cumprod(1 + np.asarray(returns))
    peaks = np.maximum.accumulate(wealth)
    return np.min(wealth / peaks - 1)

def var_historical(returns, confidence=0.95):
    return -np.quantile(np.asarray(returns), 1-confidence)

def expected_shortfall(returns, confidence=0.95):
    r = np.asarray(returns)
    threshold = np.quantile(r, 1-confidence)
    tail = r[r <= threshold]
    return -tail.mean()

def sharpe(returns, rf=0.0):
    r = np.asarray(returns)
    excess = r - rf
    return excess.mean() / excess.std(ddof=1) * np.sqrt(len(r))
