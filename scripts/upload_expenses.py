import sys
import csv
from pathlib import Path
from datetime import datetime

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = CACHE_DIR / "expenses_upload.csv"

REQUIRED_COLUMNS = {"date", "amount", "description"}


def normalize_row(row: dict) -> dict:
    """Ensure consistent data types."""
    try:
        row["date"] = datetime.strptime(row["date"], "%Y-%m-%d").strftime("%Y-%m-%d")
    except Exception:
        raise ValueError(f"Invalid date format: {row['date']} (expected YYYY-MM-DD)")

    try:
        row["amount"] = float(row["amount"])
    except Exception:
        raise ValueError(f"Invalid amount: {row['amount']} (must be number)")

    return row


def upload_csv(input_file: Path):
    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            raise ValueError(
                f"CSV must contain columns: {', '.join(REQUIRED_COLUMNS)}"
            )

        rows = [normalize_row(row) for row in reader]

    # Save normalized version
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "amount", "description"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Uploaded and saved {len(rows)} expenses → {OUTPUT_FILE}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m scripts.upload_expenses <file.csv>")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    upload_csv(input_file)


if __name__ == "__main__":
    main()
