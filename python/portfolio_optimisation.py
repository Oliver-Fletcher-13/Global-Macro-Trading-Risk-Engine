"""Small, transparent portfolio optimisation examples.

This file intentionally keeps the math readable; the full Excel workbook contains
the larger optimisation grid and efficient-frontier sample.
"""

from __future__ import annotations
import numpy as np

def portfolio_return(weights, mean_returns):
    return float(np.dot(weights, mean_returns))

def portfolio_vol(weights, cov):
    return float(np.sqrt(weights @ cov @ weights))

def risk_parity_weights(vols):
    inv = 1 / np.asarray(vols, dtype=float)
    return inv / inv.sum()
