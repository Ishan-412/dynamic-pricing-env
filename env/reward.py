from configs.settings import (
    REVENUE_WEIGHT,
    EFFICIENCY_WEIGHT,
    COMPETITIVENESS_WEIGHT,
    MAX_REVENUE_NORMALIZER
)


def compute_reward(revenue, units_sold, price, competitor_price):
    
    normalized_revenue = min(revenue / MAX_REVENUE_NORMALIZER, 1.0)

    
    efficiency = units_sold / 10

    
    price_diff = abs(price - competitor_price)
    if competitor_price == 0:
        competitiveness = 0
    else:
        competitiveness = max(0.0, 1 - price_diff / competitor_price)

    reward = (
        REVENUE_WEIGHT * normalized_revenue +
        EFFICIENCY_WEIGHT * efficiency +
        COMPETITIVENESS_WEIGHT * competitiveness
    )

    return round(min(reward, 1.0), 4)