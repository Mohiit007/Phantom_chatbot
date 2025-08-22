# backend/services/market.py
import requests
from backend.settings import settings

def fetch_yahoo_index(url: str) -> dict:
    """Fetch latest market index data from Yahoo Finance."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("chart", {}).get("result"):
            print(f"⚠️ Unexpected API response format: {data}")
            return {}

        result = data["chart"]["result"][0]
        meta = result.get("meta", {})

        if not all(key in meta for key in ["symbol", "regularMarketPrice", "currency"]):
            print(f"⚠️ Missing required fields in API response: {meta}")
            return {}

        return {
            "symbol": meta["symbol"],
            "last_price": meta["regularMarketPrice"],
            "currency": meta["currency"]
        }

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Request error fetching Yahoo Finance data: {e}")
    except (ValueError, KeyError, IndexError) as e:
        print(f"⚠️ Error parsing Yahoo Finance response: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error in fetch_yahoo_index: {e}")
    
    return {"symbol": "N/A", "last_price": 0, "currency": "INR"}

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
