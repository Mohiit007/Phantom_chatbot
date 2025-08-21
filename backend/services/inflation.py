import json
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path
from backend.settings import settings

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "worldbank_inflation.json"


def _is_cache_valid(file_path: Path, ttl_seconds: int) -> bool:
    if not file_path.exists():
        return False
    modified_time = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
    return (datetime.now(timezone.utc) - modified_time) < timedelta(seconds=ttl_seconds)


def fetch_worldbank_inflation() -> dict:
    """Fetch latest inflation data for India from World Bank API with simple cache."""
    if _is_cache_valid(CACHE_FILE, settings.cache_ttl_inflation_seconds):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cached = json.load(f)
                if "inflation_percent" in cached:
                    return {"inflation_percent": float(cached["inflation_percent"])}
        except Exception:
            pass

    try:
        # Use full endpoint from settings (README/.env.example)
        response = requests.get(settings.world_bank_base_url, timeout=15)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 1:
            records = data[1]
            latest = next((r for r in records if r.get("value") is not None), None)
            if latest:
                payload = {
                    "source": "worldbank",
                    "inflation_percent": float(latest["value"]),
                    "year": int(latest["date"]),
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                }
                try:
                    with open(CACHE_FILE, "w", encoding="utf-8") as f:
                        json.dump(payload, f, ensure_ascii=False, indent=2)
                except Exception:
                    pass
                return {"inflation_percent": payload["inflation_percent"]}
    except Exception:
        pass

    # fallback
    return {"inflation_percent": float(settings.fallback_inflation)}
