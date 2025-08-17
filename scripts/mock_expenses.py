import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

CATEGORIES = {
    "Travel": ["Uber", "Ola", "Flight", "Train"],
    "Shopping": ["Amazon", "Flipkart", "Myntra", "Mall"],
    "Bills": ["Electricity", "Water", "Internet", "Phone"],
    "Food": ["Swiggy", "Zomato", "Dominos", "Cafe"],
    "Health": ["Pharmacy", "Doctor", "Hospital"],
}

OUTPUT_FILE = Path(".cache/mock_expenses.csv")


def generate_mock_data(n: int = 50):
    rows = []
    today = datetime.today()

    for _ in range(n):
        category = random.choice(list(CATEGORIES.keys()))
        merchant = random.choice(CATEGORIES[category])
        amount = round(random.uniform(100, 5000), 2)
        days_ago = random.randint(1, 90)
        date = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")

        rows.append([date, amount, merchant])

    return rows


def save_to_csv(rows, filename: Path):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "amount", "description"])
        writer.writerows(rows)


def main():
    rows = generate_mock_data(50)
    save_to_csv(rows, OUTPUT_FILE)
    print(f"✅ Mock data generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
