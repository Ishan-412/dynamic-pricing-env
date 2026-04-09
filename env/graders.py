from configs.settings import MAX_INVENTORY


def grade_easy(state):
    """
    Focus: maximize units sold
    """
    sold = MAX_INVENTORY - state["inventory"]

    score = sold / MAX_INVENTORY

    score = max(0.01, min(score, 0.99))
    return round(score, 4)


def grade_medium(state):
    """
    Balance revenue and volume
    """
    sold = MAX_INVENTORY - state["inventory"]
    revenue = state["total_revenue"]

    
    sales_score = sold / MAX_INVENTORY
    revenue_score = min(revenue / 1000, 1.0)

    score = 0.5 * sales_score + 0.5 * revenue_score

    score = max(0.01, min(score, 0.99))
    return round(score, 4)


def grade_hard(state):
    """
    Focus: maximize revenue with smart pricing
    """
    revenue = state["total_revenue"]

    score = min(revenue / 1500, 1.0)
    score = max(0.01, min(score, 0.99))
    return round(score, 4)


def grade_task(task_name, state):
    if task_name == "easy":
        return grade_easy(state)

    elif task_name == "medium":
        return grade_medium(state)

    elif task_name == "hard":
        return grade_hard(state)

    else:
        raise ValueError("Unknown task")