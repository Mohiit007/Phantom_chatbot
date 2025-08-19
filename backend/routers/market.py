# backend/routers/market.py
from fastapi import APIRouter
from backend.services.market import fetch_index_summary

router = APIRouter(prefix="/market", tags=["Market"])

@router.get("/summary")
def get_market_summary():
    """
    Get latest market summary (Nifty + Sensex).
    Cached for performance.
    """
    return fetch_index_summary()
