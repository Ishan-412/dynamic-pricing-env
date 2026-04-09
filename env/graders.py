
from configs.settings import MAX_INVENTORY

def _clip01(x, eps=1e-6):
    # strictly within (0,1)
    if x <= 0.0:
        return eps
    if x >= 1.0:
        return 1.0 - eps
    return float(x)


def grade_easy(state):
    """
    Focus: maximize units sold
    """
    sold = MAX_INVENTORY - state["inventory"]

    score = sold / MAX_INVENTORY
    score = _clip01(score)
    return score


def grade_medium(state):
    """
    Balance revenue and volume
    """
    sold = MAX_INVENTORY - state["inventory"]
    revenue = state["total_revenue"]

    sales_score = _clip01(sold / MAX_INVENTORY)
    revenue_score = _clip01(revenue / 1000.0)

    score = 0.5 * sales_score + 0.5 * revenue_score
    score = _clip01(score)
    return score


def grade_hard(state):
    """
    Focus: maximize revenue with smart pricing
    """
    revenue = state["total_revenue"]

    score = _clip01(revenue / 1500.0)
    return score


def grade_task(task_name, state):
    if task_name == "easy":
        return grade_easy(state)

    elif task_name == "medium":
        return grade_medium(state)

    elif task_name == "hard":
        return grade_hard(state)

    else:
        raise ValueError("Unknown task")