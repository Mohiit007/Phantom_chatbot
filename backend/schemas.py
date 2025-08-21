# backend/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
try:
    from pydantic import field_validator  # Pydantic v2
except Exception:
    field_validator = None  # type: ignore


# -------------------------
# Goal-related schemas
# -------------------------
class GoalBase(BaseModel):
    event_name: str
    today_cost: float
    target_year: int

    if field_validator:
        @field_validator("today_cost")
        @classmethod
        def _validate_cost(cls, v: float):
            if v <= 0:
                raise ValueError("today_cost must be > 0")
            return v

        @field_validator("target_year")
        @classmethod
        def _validate_year(cls, v: int):
            if v < datetime.now().year:
                raise ValueError("target_year cannot be in the past")
            return v


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    event_name: Optional[str] = Field(None, example="Wedding")
    today_cost: Optional[float] = Field(None, gt=0, example=800000)
    target_year: Optional[int] = Field(None, gt=1900, example=2027)


class CalculationOut(BaseModel):
    id: Optional[int] = None
    future_cost: float
    monthly_saving: float

    class Config:
        from_attributes = True


class GoalOut(GoalBase):
    id: int
    calculation: Optional[CalculationOut] = None

    class Config:
        from_attributes = True


# -------------------------
# NLP-related schemas
# -------------------------
class ParseTextRequest(BaseModel):
    text: str = Field(..., example="Plan Goa trip Dec 2025 for ₹50000")


class ParseTextResponse(BaseModel):
    event_name: str
    today_cost: float
    target_year: int


# -------------------------
# Planner-related schemas
# -------------------------
class PlanRequest(BaseModel):
    event_name: str = Field(..., example="Car Purchase")
    today_cost: float = Field(..., gt=0, example=500000)
    target_year: int = Field(..., gt=2025, example=2030)
    inflation_override_pct: Optional[float] = Field(None, ge=0, le=50)

    if field_validator:
        @field_validator("today_cost")
        @classmethod
        def _validate_plan_cost(cls, v: float):
            if v <= 0:
                raise ValueError("today_cost must be > 0")
            return v

        @field_validator("target_year")
        @classmethod
        def _validate_plan_year(cls, v: int):
            if v < datetime.now().year:
                raise ValueError("target_year cannot be in the past")
            return v


class TextPlanRequest(BaseModel):
    text: str = Field(..., example="Plan wedding in Dec 2026 for ₹800000")
    inflation_override_pct: Optional[float] = Field(None, ge=0, le=50)


class PlanResponse(BaseModel):
    event_name: str
    target_year: int
    today_cost: float
    inflation_percent_used: float
    years_to_goal: int
    future_cost: float
    monthly_saving_needed: float
    recommendation: Optional[str] = None


# -------------------------
# Agent/Chat schemas
# -------------------------
class ChatMessageRequest(BaseModel):
    message: str = Field(..., example="I want to plan a Goa trip in Dec 2026 for 50k. Also how's the market today?")


class ChatMessageResponse(BaseModel):
    reply: str
    plan: Optional[PlanResponse] = None
    market_summary: Optional[dict] = None


# -------------------------
# Expense / Income schemas
# -------------------------
class ExpenseIn(BaseModel):
    date: Optional[str] = None
    amount: float
    category: str
    note: Optional[str] = None

    if field_validator:
        @field_validator("amount")
        @classmethod
        def _validate_amount(cls, v: float):
            if v <= 0:
                raise ValueError("Amount must be > 0")
            return v


class Expense(ExpenseIn):
    id: int


class IncomeIn(BaseModel):
    date: Optional[str] = None
    amount: float
    source: str
    note: Optional[str] = None

    if field_validator:
        @field_validator("amount")
        @classmethod
        def _validate_amount(cls, v: float):
            if v <= 0:
                raise ValueError("Amount must be > 0")
            return v


class Income(IncomeIn):
    id: int


# -------------------------
# Advice schema
# -------------------------
class AdviceResponse(BaseModel):
    monthly_income_total: float
    monthly_expense_total: float
    monthly_savings: float
    savings_rate_percent: float
    tax_bracket: str
    estimated_annual_tax: float
    suggested_allocation: dict
