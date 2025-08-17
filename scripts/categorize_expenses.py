import csv
from pathlib import Path
from collections import defaultdict

CACHE_DIR = Path(".cache")
UPLOAD_FILE = CACHE_DIR / "expenses_upload.csv"
MOCK_FILE = CACHE_DIR / "mock_expenses.csv"

CATEGORY_KEYWORDS = {
    "Food": ["restaurant", "dominos", "zomato", "swiggy", "groceries", "food"],
    "Travel": ["uber", "ola", "flight", "train", "bus", "travel"],
    "Shopping": ["amazon", "flipkart", "shopping", "clothes", "shoes"],
    "Bills": ["electricity", "internet", "mobile", "rent", "bill"],
    "Health": ["hospital", "pharmacy", "doctor", "medicine", "health"],
}

def categorize(description: str) -> str:
    desc = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in desc for word in keywords):
            return category
    return "Other"


def load_expenses(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def main():
    # Auto-detect file to use
    if UPLOAD_FILE.exists():
        file_to_use = UPLOAD_FILE
        print(f"📂 Using uploaded file: {UPLOAD_FILE}")
    elif MOCK_FILE.exists():
        file_to_use = MOCK_FILE
        print(f"📂 Using mock file: {MOCK_FILE}")
    else:
        print("❌ No expense file found. Run mock_expenses or upload_expenses first.")
        return

    expenses = load_expenses(file_to_use)

    summary = defaultdict(float)
    detailed = []

    for row in expenses:
        category = categorize(row["description"])
        amount = float(row["amount"])
        summary[category] += amount
        detailed.append({
            "date": row["date"],
            "amount": row["amount"],
            "description": row["description"],
            "category": category,
        })

    print("\n📊 Expense Summary:")
    for category, total in summary.items():
        print(f"  {category}: ₹{total:.2f}")

    print("\n📜 Sample Detailed Expenses:")
    for d in detailed[:5]:
        print(d)


if __name__ == "__main__":
    main()
