import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests

from backend.settings import settings
from backend.logging_config import logger

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)

YAHOO_ENDPOINTS = {
    "NIFTY50": settings.yf_nifty_url,
    "SENSEX": settings.yf_sensex_url,
}

CACHE_TTL = settings.cache_ttl_market_seconds


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


def fetch_index(name: str, url: str, retries: int = 3, delay: int = 2) -> dict:
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            return {
                "index": name,
                "meta": data.get("chart", {}).get("result", [{}])[0].get("meta", {}),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as exc:
            logger.warning(f"{name} fetch failed (attempt {attempt}/{retries}): {exc}")
            if attempt < retries:
                time.sleep(delay)
            else:
                logger.error(f"{name} fetch failed after {retries} attempts")
                return {
                    "index": name,
                    "error": str(exc),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }


def save_cache(payload: dict, file_path: Path) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main() -> None:
    outputs = {}
    for name, url in YAHOO_ENDPOINTS.items():
        cache_file = CACHE_DIR / f"yahoo_{name.lower()}.json"

        if is_cache_valid(cache_file, CACHE_TTL):
            logger.info(f"Using cached data for {name}")
            payload = load_cache(cache_file)
        else:
            logger.info(f"Fetching fresh data for {name}")
            payload = fetch_index(name, url)
            save_cache(payload, cache_file)

        outputs[name] = payload

    print(json.dumps(outputs, indent=2))


if __name__ == "__main__":
    main()
