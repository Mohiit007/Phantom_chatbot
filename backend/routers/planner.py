# backend/routers/planner.py
from fastapi import APIRouter
from backend.services.planner import plan_event

router = APIRouter(
    prefix="/planner",
    tags=["Planner"],
)

@router.post("/")
def create_plan(event_name: str, today_cost: float, target_year: int):
    """
    Create a financial plan for an event.
    """
    return plan_event(event_name, today_cost, target_year)
