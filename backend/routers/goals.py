
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from backend.database import SessionLocal
from backend import models, schemas
from backend.services.planner import plan_event

router = APIRouter(prefix="/goals", tags=["Goals"])

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

@router.get("/{goal_id}", response_model=schemas.GoalOut)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(models.Goal).options(joinedload(models.Goal.calculation)).get(goal_id)
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

@router.patch("/{goal_id}", response_model=schemas.GoalOut)
def update_goal(goal_id: int, goal_update: schemas.GoalUpdate, db: Session = Depends(get_db)):
    goal = db.query(models.Goal).options(joinedload(models.Goal.calculation)).get(goal_id)
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")

    # Apply updates if provided
    if goal_update.event_name is not None:
        goal.event_name = goal_update.event_name
    if goal_update.today_cost is not None:
        goal.today_cost = goal_update.today_cost
    if goal_update.target_year is not None:
        goal.target_year = goal_update.target_year

    # Recalculate calculation
    plan = plan_event(goal.event_name, goal.today_cost, goal.target_year)

    if goal.calculation is None:
        goal.calculation = models.Calculation(
            future_cost=plan["future_cost"],
            monthly_saving=plan["monthly_saving_needed"],
        )
    else:
        goal.calculation.future_cost = plan["future_cost"]
        goal.calculation.monthly_saving = plan["monthly_saving_needed"]

    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

@router.delete("/{goal_id}", status_code=204)
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(models.Goal).get(goal_id)
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")

    db.delete(goal)
    db.commit()
    return None
