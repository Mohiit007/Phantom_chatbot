import requests
from backend.settings import settings

def fetch_worldbank_inflation() -> dict:
    """Fetch latest inflation data for India from World Bank API."""
    try:
        response = requests.get(settings.world_bank_base_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # World Bank response format is nested, extract the latest value
        if isinstance(data, list) and len(data) > 1:
            records = data[1]
            for record in records:
                if record.get("value") is not None:
                    return {"inflation_percent": float(record["value"])}

    except Exception as e:
        print(f"⚠️ Error fetching World Bank inflation: {e}")

    # fallback
    return {"inflation_percent": float(settings.fallback_inflation)}
