from typing import Tuple
from .models import Observation, Action, Reward
from .demand import compute_demand
from .reward import compute_reward
from configs.settings import *


class DynamicPricingEnv:
    def __init__(self, task_name="easy"):
        from .tasks import TASKS

        if task_name not in TASKS:
            valid = ", ".join(sorted(TASKS.keys()))
            raise ValueError(
                f"Unknown task_name '{task_name}'. Valid options: {valid}"
            )

        self.task_name = task_name
        self.max_steps = TASKS[task_name]["max_steps"]
        self.reset()

    def reset(self) -> Observation:
        self.state_data = {
            "current_price": 50.0,
            "competitor_price": 45.0,
            "inventory": MAX_INVENTORY,
            "time_step": 0,
            "total_revenue": 0.0,
        }
        self.done = False
        return self._get_observation(None)

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, dict]:
        if self.done:
            raise Exception("Episode finished. Call reset().")

        self.state_data["time_step"] += 1

        price = action.new_price
        competitor_price = self.state_data["competitor_price"]

        # Demand
        demand = compute_demand(price, competitor_price)

        # Sales
        units_sold = min(
            self.state_data["inventory"],
            int(demand * MAX_UNITS_PER_STEP)
        )

        revenue = units_sold * price

        # Update state
        self.state_data["inventory"] -= units_sold
        self.state_data["total_revenue"] += revenue
        self.state_data["current_price"] = price

        # Reward
        reward_score = compute_reward(
            revenue, units_sold, price, competitor_price
        )

        reward = Reward(
            score=reward_score,
            revenue=revenue,
            units_sold=units_sold,
            reason="Revenue + efficiency + competitiveness"
        )

        # Deterministic competitor change (IMPORTANT)
        self.state_data["competitor_price"] += (
            (self.state_data["time_step"] % 3) - 1
        )

        # Done
        if (
            self.state_data["inventory"] <= 0
            or self.state_data["time_step"] >= self.max_steps
        ):
            self.done = True

        obs = self._get_observation(reward.score)

        return obs, reward, self.done, {}

    def _get_observation(self, last_reward):
        demand = compute_demand(
            self.state_data["current_price"],
            self.state_data["competitor_price"]
        )

        return Observation(
            current_price=self.state_data["current_price"],
            demand_level=demand,
            competitor_price=self.state_data["competitor_price"],
            inventory=self.state_data["inventory"],
            time_step=self.state_data["time_step"],
            last_reward=last_reward
        )

    def state(self):
        return self.state_data
