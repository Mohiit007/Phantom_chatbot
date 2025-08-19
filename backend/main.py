from fastapi import FastAPI
from backend.logging_config import logger
from backend import models
from backend.database import engine
from backend.routers import goals, planner , market  # <-- Import routers
from backend.routers import nlp
from fastapi.middleware.cors import CORSMiddleware

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Agent")

# CORS (allow all for now; tighten with frontend origin when available)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(goals.router)
app.include_router(planner.router)
app.include_router(market.router)
app.include_router(nlp.router)

@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": "Welcome to Phantom Finance Agent 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}
