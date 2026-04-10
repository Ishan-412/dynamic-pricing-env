from configs.settings import MAX_INVENTORY


def _normalize(x):
    """
    Normalize any value assumed in [0,1] into STRICT (0,1)
    using affine scaling.
    """
    x = max(0.0, min(x, 1.0))
    return 0.01 + 0.98 * x   # ensures strictly between (0,1)


def grade_easy(state):
    sold = MAX_INVENTORY - state["inventory"]
    raw = sold / MAX_INVENTORY
    return _normalize(raw)


def grade_medium(state):
    sold = MAX_INVENTORY - state["inventory"]
    revenue = state["total_revenue"]

    sales_score = sold / MAX_INVENTORY
    revenue_score = min(revenue / 1000.0, 1.0)

    combined = 0.5 * sales_score + 0.5 * revenue_score
    return _normalize(combined)


def grade_hard(state):
    revenue = state["total_revenue"]

    raw = min(revenue / 1500.0, 1.0)
    return _normalize(raw)


def grade_task(task_name, state):
    if task_name == "easy":
        score = grade_easy(state)
    elif task_name == "medium":
        score = grade_medium(state)
    elif task_name == "hard":
        score = grade_hard(state)
    else:
        raise ValueError("Unknown task")

    return float(score)