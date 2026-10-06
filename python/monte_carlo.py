"""Simple Monte Carlo simulation for portfolio wealth."""

from __future__ import annotations
import numpy as np

def simulate(start=1.0, annual_return=0.07, annual_vol=0.08, years=5, sims=20_000, seed=42):
    rng = np.random.default_rng(seed)
    steps = years * 12
    mu = (annual_return - 0.5 * annual_vol**2) / 12
    sigma = annual_vol / np.sqrt(12)
    shocks = rng.normal(mu, sigma, size=(sims, steps))
    wealth = start * np.exp(np.cumsum(shocks, axis=1))
    return wealth

if __name__ == "__main__":
    paths = simulate()
    terminal = paths[:, -1]
    print("Median terminal wealth:", np.median(terminal))
    print("5th percentile:", np.quantile(terminal, 0.05))
    print("95th percentile:", np.quantile(terminal, 0.95))
