def compute_demand(price: float, competitor_price: float) -> float:
    """
    Demand increases when price is competitive.
    Deterministic and bounded [0, 1].
    """
    if price <= 0:
        return 0.0

    demand = competitor_price / price

    return max(0.0, min(demand, 1.0))