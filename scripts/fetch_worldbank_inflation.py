import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests

from backend.settings import settings
from backend.logging_config import logger

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "worldbank_inflation.json"

WORLD_BANK_URL = (
    f"{settings.world_bank_base_url}/country/IND/indicator/FP.CPI.TOTL.ZG?format=json"
)
FALLBACK_INFLATION = settings.fallback_inflation
CACHE_TTL = settings.cache_ttl_inflation_seconds


def is_cache_valid(file_path: Path, ttl_seconds: int) -> bool:
    if not file_path.exists():
        return False
    modified_time = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
    return (datetime.now(timezone.utc) - modified_time) < timedelta(seconds=ttl_seconds)


def load_cache(file_path: Path) -> dict | None:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def fetch_latest_inflation() -> dict:
    try:
        resp = requests.get(WORLD_BANK_URL, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        records = data[1]
        latest = next((r for r in records if r.get("value") is not None), None)
        if latest is None:
            raise ValueError("No recent inflation value found")
        return {
            "source": "worldbank",
            "inflation_percent": float(latest["value"]),
            "year": int(latest["date"]),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        logger.warning(f"World Bank fetch failed, using fallback. Reason: {exc}")
        return {
            "source": "fallback",
            "inflation_percent": FALLBACK_INFLATION,
            "year": datetime.now(timezone.utc).year,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }


def save_cache(payload: dict, file_path: Path) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main() -> None:
    if is_cache_valid(CACHE_FILE, CACHE_TTL):
        logger.info("Using cached inflation data")
        result = load_cache(CACHE_FILE)
    else:
        logger.info("Fetching fresh inflation data")
        result = fetch_latest_inflation()
        save_cache(result, CACHE_FILE)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
