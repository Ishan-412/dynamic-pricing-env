from configs.settings import MAX_INVENTORY

# Numerical stability helpers
EPS = 1e-6

def _safe_ratio(num, denom):
    """
    Returns a ratio strictly in (0,1) even at boundaries.
    """
    denom = float(denom) + 2 * EPS
    num = float(num) + EPS
    r = num / denom
    # guard for any numerical drift
    if r <= 0.0:
        return EPS
    if r >= 1.0:
        return 1.0 - EPS
    return r

def _squash_01(x):
    """
    Smoothly squash any non-negative value into (0,1) using a saturating transform.
    """
    # x >= 0 expected
    # use x / (1 + x) which is in (0,1)
    r = x / (1.0 + x)
    if r <= 0.0:
        return EPS
    if r >= 1.0:
        return 1.0 - EPS
    return float(r)


def grade_easy(state):
    """
    Focus: maximize units sold
    """
    sold = MAX_INVENTORY - state["inventory"]

    score = _safe_ratio(sold, MAX_INVENTORY)
    return score


def grade_medium(state):
    """
    Balance revenue and volume
    """
    sold = MAX_INVENTORY - state["inventory"]
    revenue = state["total_revenue"]

    sales_score = _safe_ratio(sold, MAX_INVENTORY)
    # scale revenue then squash to (0,1)
    revenue_scaled = revenue / 1000.0
    revenue_score = _squash_01(revenue_scaled)

    score = 0.5 * sales_score + 0.5 * revenue_score
    # final guard to keep strictly within (0,1)
    if score <= 0.0:
        score = EPS
    elif score >= 1.0:
        score = 1.0 - EPS
    return float(score)


def grade_hard(state):
    """
    Focus: maximize revenue with smart pricing
    """
    revenue = state["total_revenue"]

    revenue_scaled = revenue / 1500.0
    score = _squash_01(revenue_scaled)
    return score


def grade_task(task_name, state):
    if task_name == "easy":
        score = grade_easy(state)
    elif task_name == "medium":
        score = grade_medium(state)
    elif task_name == "hard":
        score = grade_hard(state)
    else:
        raise ValueError("Unknown task")

    # FINAL SAFETY CLAMP (guaranteed fix)
    EPS = 1e-6
    if score <= 0.0:
        score = EPS
    elif score >= 1.0:
        score = 1.0 - EPS

    return float(score)