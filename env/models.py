from pydantic import BaseModel, Field
from typing import Optional


class Observation(BaseModel):
    current_price: float
    demand_level: float
    competitor_price: float
    inventory: int
    time_step: int
    last_reward: Optional[float] = None


class Action(BaseModel):
    new_price: float = Field(gt=0)


class Reward(BaseModel):
    score: float
    revenue: float
    units_sold: int
    reason: str