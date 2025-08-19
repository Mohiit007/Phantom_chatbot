from pydantic import BaseModel
from typing import Optional

class GoalBase(BaseModel):
    event_name: str
    today_cost: float
    target_year: int

class GoalCreate(GoalBase):
    pass

class CalculationOut(BaseModel):
    id: Optional[int] = None
    future_cost: float
    monthly_saving: float

    class Config:
        orm_mode = True

class GoalOut(GoalBase):
    id: int
    calculation: Optional[CalculationOut] = None

    class Config:
        orm_mode = True
