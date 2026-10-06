"""Illustrative Black-Scholes option calculator."""

from __future__ import annotations
from math import exp, log, sqrt, erf

def norm_cdf(x: float) -> float:
    return 0.5 * (1 + erf(x / sqrt(2)))

def price_and_delta(spot: float, strike: float, t: float, rf: float, q: float, vol: float):
    d1 = (log(spot / strike) + (rf - q + 0.5 * vol**2) * t) / (vol * sqrt(t))
    d2 = d1 - vol * sqrt(t)
    call = spot * exp(-q*t) * norm_cdf(d1) - strike * exp(-rf*t) * norm_cdf(d2)
    put = strike * exp(-rf*t) * norm_cdf(-d2) - spot * exp(-q*t) * norm_cdf(-d1)
    call_delta = exp(-q*t) * norm_cdf(d1)
    put_delta = call_delta - exp(-q*t)
    return {"call": call, "put": put, "call_delta": call_delta, "put_delta": put_delta, "d1": d1, "d2": d2}

if __name__ == "__main__":
    print(price_and_delta(7591.7, 7591.7, 1, 0.0363, 0.012, 0.18))
