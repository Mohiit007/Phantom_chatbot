from fastapi import FastAPI
from backend.logging_config import logger
from backend import models
from backend.database import engine
from backend.routers import goals, planner   # <-- Import routers

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Agent")

# Include Routers
app.include_router(goals.router)
app.include_router(planner.router)

@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": "Welcome to Phantom Finance Agent 🚀"}
