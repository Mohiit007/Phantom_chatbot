

# backend/routers/planner.py
from fastapi import APIRouter, HTTPException
from backend.services.planner import plan_event
from backend.schemas import PlanRequest, PlanResponse, TextPlanRequest
from backend.services.nlp import parse_goal_text

router = APIRouter(
    prefix="/planner",
    tags=["Planner"],
)

@router.post("/", response_model=PlanResponse)
def create_plan(request: PlanRequest):
    """
    Create a financial plan for an event.
    """
    return plan_event(request.event_name, request.today_cost, request.target_year, request.inflation_override_pct)

@router.post("/parse-and-plan", response_model=PlanResponse)
def parse_and_plan(request: TextPlanRequest):
    try:
        event_name, today_cost, target_year = parse_goal_text(request.text)
        return plan_event(event_name, today_cost, target_year, request.inflation_override_pct)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
