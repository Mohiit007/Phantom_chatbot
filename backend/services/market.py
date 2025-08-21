# backend/services/market.py
import requests
from backend.settings import settings

def fetch_yahoo_index(url: str) -> dict:
    """Fetch latest market index data from Yahoo Finance."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        result = data["chart"]["result"][0]
        meta = result["meta"]

        return {
            "symbol": meta["symbol"],
            "last_price": meta["regularMarketPrice"],
            "currency": meta["currency"]
        }

    except Exception as e:
        print(f"⚠️ Error fetching Yahoo Finance data: {e}")
        return {}

def fetch_index_summary() -> dict:
    """
    Returns NIFTY & SENSEX summary.
    Uses mock data if USE_MOCK_MARKET=true in .env
    """
    if settings.use_mock_market:
        return {
            "NIFTY_50": {"symbol": "^NSEI", "last_price": 22400.5, "currency": "INR"},
            "SENSEX": {"symbol": "^BSESN", "last_price": 74000.3, "currency": "INR"},
        }

    return {
        "NIFTY_50": fetch_yahoo_index(settings.yf_nifty_url),
        "SENSEX": fetch_yahoo_index(settings.yf_sensex_url),
    }
