"""Illustrative duration / DV01 / convexity calculations."""

def price_change(price: float, modified_duration: float, convexity: float, yield_change: float) -> float:
    """Second-order price approximation: -D*dy + 0.5*C*dy^2."""
    return price * (-modified_duration * yield_change + 0.5 * convexity * yield_change**2)

def dv01(price: float, modified_duration: float, notional: float) -> float:
    """Approximate dollar P&L for a 1bp yield rise."""
    return notional * (-modified_duration * 0.0001)

if __name__ == "__main__":
    print("25bp shock on 100 price:", price_change(100, 8, 70, 0.0025))
    print("DV01 on $10m:", dv01(100, 8, 10_000_000))
