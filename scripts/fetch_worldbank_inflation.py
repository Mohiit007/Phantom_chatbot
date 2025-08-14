import json
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()

WORLD_BANK_URL = (
	"https://api.worldbank.org/v2/country/IND/indicator/FP.CPI.TOTL.ZG?format=json"
)
CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "worldbank_inflation.json"
FALLBACK_INFLATION = float(os.getenv("FALLBACK_INFLATION", "6.5"))


def fetch_latest_inflation() -> dict:
	try:
		resp = requests.get(WORLD_BANK_URL, timeout=20)
		resp.raise_for_status()
		data = resp.json()
		# World Bank returns [metadata, [records...]]
		records = data[1]
		latest = next((r for r in records if r.get("value") is not None), None)
		if latest is None:
			raise ValueError("No recent inflation value found")
		return {
			"source": "worldbank",
			"inflation_percent": float(latest["value"]),
			"year": int(latest["date"]),
			"fetched_at": datetime.utcnow().isoformat() + "Z",
		}
	except Exception as exc:
		print(f"Warning: World Bank fetch failed, using fallback. Reason: {exc}")
		return {
			"source": "fallback",
			"inflation_percent": FALLBACK_INFLATION,
			"year": datetime.utcnow().year,
			"fetched_at": datetime.utcnow().isoformat() + "Z",
		}


def save_cache(payload: dict) -> None:
	with open(CACHE_FILE, "w", encoding="utf-8") as f:
		json.dump(payload, f, ensure_ascii=False, indent=2)


def main() -> None:
	result = fetch_latest_inflation()
	save_cache(result)
	print(json.dumps(result, indent=2))


if __name__ == "__main__":
	main()


