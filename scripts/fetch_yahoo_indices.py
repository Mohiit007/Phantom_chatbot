import json
from datetime import datetime
from pathlib import Path

import requests


YAHOO_ENDPOINTS = {
	"NIFTY50": "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI?range=1d&interval=1m",
	"SENSEX": "https://query1.finance.yahoo.com/v8/finance/chart/%5EBSESN?range=1d&interval=1m",
}

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)


def fetch_index(name: str, url: str) -> dict:
	try:
		resp = requests.get(url, timeout=20)
		resp.raise_for_status()
		data = resp.json()
		result = {
			"index": name,
			"meta": data.get("chart", {}).get("result", [{}])[0].get("meta", {}),
			"timestamp": datetime.utcnow().isoformat() + "Z",
		}
		return result
	except Exception as exc:
		return {
			"index": name,
			"error": str(exc),
			"timestamp": datetime.utcnow().isoformat() + "Z",
		}


def main() -> None:
	outputs = {}
	for name, url in YAHOO_ENDPOINTS.items():
		payload = fetch_index(name, url)
		outputs[name] = payload
		cache_file = CACHE_DIR / f"yahoo_{name.lower()}.json"
		with open(cache_file, "w", encoding="utf-8") as f:
			json.dump(payload, f, ensure_ascii=False, indent=2)
	print(json.dumps(outputs, indent=2))


if __name__ == "__main__":
	main()


