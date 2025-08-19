
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from backend.database import SessionLocal
from backend import models, schemas
from backend.services.planner import plan_event

router = APIRouter()

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.GoalOut)
def create_goal(goal_in: schemas.GoalCreate, db: Session = Depends(get_db)):
    """
    1) Save Goal
    2) Compute plan (future cost + monthly saving)
    3) Save Calculation linked to Goal
    4) Return Goal with Calculation
    """
    goal = models.Goal(
        event_name=goal_in.event_name,
        today_cost=goal_in.today_cost,
        target_year=goal_in.target_year,
    )
    db.add(goal)
    db.flush()  # allocate goal.id without full commit

    plan = plan_event(goal.event_name, goal.today_cost, goal.target_year)

    calc = models.Calculation(
        future_cost=plan["future_cost"],
        monthly_saving=plan["monthly_saving_needed"],
        goal_id=goal.id,
    )
    db.add(calc)
    db.commit()
    db.refresh(goal)
    db.refresh(calc)

    # Let Pydantic serialize the ORM objects (orm_mode=True)
    return goal

@router.get("/", response_model=List[schemas.GoalOut])
def get_all_goals(db: Session = Depends(get_db)):
    """Return all goals with their calculations eager-loaded."""
    goals = db.query(models.Goal).options(
        joinedload(models.Goal.calculation)
    ).all()
    return goals
