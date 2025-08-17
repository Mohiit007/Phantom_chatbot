import csv
from pathlib import Path
from collections import defaultdict
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

CACHE_DIR = Path(".cache")
UPLOAD_FILE = CACHE_DIR / "expenses_upload.csv"
MOCK_FILE = CACHE_DIR / "mock_expenses.csv"
OUTPUT_FILE = CACHE_DIR / "expenses_report.pdf"

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


def generate_pdf(expenses, summary):
    doc = SimpleDocTemplate(str(OUTPUT_FILE), pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("📊 Expense Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Summary table
    data = [["Category", "Total (₹)"]] + [
        [cat, f"{total:.2f}"] for cat, total in summary.items()
    ]
    table = Table(data, colWidths=[200, 150])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    elements.append(table)
    elements.append(Spacer(1, 24))

    # Detailed transactions
    elements.append(Paragraph("📜 Detailed Transactions", styles["Heading2"]))
    data = [["Date", "Description", "Amount (₹)", "Category"]] + [
        [e["date"], e["description"], e["amount"], e["category"]] for e in expenses[:20]
    ]
    table = Table(data, colWidths=[100, 200, 100, 100])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("ALIGN", (2, 1), (2, -1), "RIGHT"),
            ]
        )
    )
    elements.append(table)

    doc.build(elements)
    print(f"✅ PDF report generated: {OUTPUT_FILE}")


def main():
    # Auto-detect file
    if UPLOAD_FILE.exists():
        file_to_use = UPLOAD_FILE
        print(f"📂 Using uploaded file: {UPLOAD_FILE}")
    elif MOCK_FILE.exists():
        file_to_use = MOCK_FILE
        print(f"📂 Using mock file: {MOCK_FILE}")
    else:
        print("❌ No expense file found. Run mock_expenses or upload_expenses first.")
        return

    expenses_raw = load_expenses(file_to_use)

    expenses = []
    summary = defaultdict(float)

    for row in expenses_raw:
        category = categorize(row["description"])
        amount = float(row["amount"])
        expenses.append(
            {
                "date": row["date"],
                "amount": f"{amount:.2f}",
                "description": row["description"],
                "category": category,
            }
        )
        summary[category] += amount

    generate_pdf(expenses, summary)


if __name__ == "__main__":
    main()
