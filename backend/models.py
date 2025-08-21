from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, index=True)
    today_cost = Column(Float)
    target_year = Column(Integer)

    # NEW: one-to-one with Calculation (delete calc if goal is deleted)
    calculation = relationship(
        "Calculation",
        back_populates="goal",
        uselist=False,
        cascade="all, delete-orphan",
    )

class Calculation(Base):
    __tablename__ = "calculations"
    id = Column(Integer, primary_key=True, index=True)
    future_cost = Column(Float)
    monthly_saving = Column(Float)
    goal_id = Column(Integer, ForeignKey("goals.id"))

    # NEW: backref to Goal
    goal = relationship("Goal", back_populates="calculation")
