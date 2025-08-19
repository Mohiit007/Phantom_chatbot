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
