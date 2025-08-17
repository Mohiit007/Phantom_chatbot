
from fastapi import FastAPI
from backend.logging_config import logger  # works only with uvicorn run

app = FastAPI()

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Finance Agent Backend is running 🚀"}
