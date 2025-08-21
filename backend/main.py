from fastapi import FastAPI
from typing import List
from datetime import datetime
from backend.logging_config import logger
from backend import models
from backend.database import engine
from backend.routers import goals, planner, market, nlp, agent
from backend.schemas import ExpenseIn, Expense, IncomeIn, Income, AdviceResponse
from fastapi.middleware.cors import CORSMiddleware

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Agent")

# CORS (allow all for now; tighten with frontend origin when available)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(goals.router)
app.include_router(planner.router)
app.include_router(market.router)
app.include_router(nlp.router)
app.include_router(agent.router)

@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": "Welcome to Phantom Finance Agent 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------
# In-memory stores (DEV only)
# -------------------------
_expenses: List[Expense] = []
_income: List[Income] = []
_exp_id = 1
_inc_id = 1

def _today_iso() -> str:
    return datetime.now().date().isoformat()

@app.get("/expenses", response_model=List[Expense])
def list_expenses() -> List[Expense]:
    return _expenses

@app.post("/expenses", response_model=Expense)
def add_expense(item: ExpenseIn) -> Expense:
    global _exp_id
    e = Expense(
        id=_exp_id,
        date=item.date or _today_iso(),
        amount=item.amount,
        category=item.category,
        note=item.note,
    )
    _exp_id += 1
    _expenses.append(e)
    return e

@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    idx = next((i for i, x in enumerate(_expenses) if x.id == expense_id), -1)
    if idx >= 0:
        _expenses.pop(idx)
    return None

@app.get("/income", response_model=List[Income])
def list_income() -> List[Income]:
    return _income

@app.post("/income", response_model=Income)
def add_income(item: IncomeIn) -> Income:
    global _inc_id
    inc = Income(
        id=_inc_id,
        date=item.date or _today_iso(),
        amount=item.amount,
        source=item.source,
        note=item.note,
    )
    _inc_id += 1
    _income.append(inc)
    return inc

@app.delete("/income/{income_id}", status_code=204)
def delete_income(income_id: int):
    idx = next((i for i, x in enumerate(_income) if x.id == income_id), -1)
    if idx >= 0:
        _income.pop(idx)
    return None

@app.get("/advice", response_model=AdviceResponse)
def get_advice() -> AdviceResponse:
    # Use current month totals
    month_prefix = datetime.now().strftime("%Y-%m")
    month_exp = sum(e.amount for e in _expenses if (e.date or "").startswith(month_prefix))
    month_inc = sum(i.amount for i in _income if (i.date or "").startswith(month_prefix))
    savings = round(month_inc - month_exp, 2)
    rate = round((savings / month_inc * 100.0), 2) if month_inc > 0 else 0.0

    # Simple tax estimate (illustrative only; old-regime-like tiers INR)
    annual_inc = month_inc * 12.0
    if annual_inc <= 300000:
        bracket = "0%"
        annual_tax = 0.0
    elif annual_inc <= 600000:
        bracket = "5%"
        annual_tax = 0.05 * (annual_inc - 300000)
    elif annual_inc <= 1200000:
        bracket = "10%"
        annual_tax = (0.05 * 300000) + 0.10 * (annual_inc - 600000)
    else:
        bracket = "20%"
        annual_tax = (0.05 * 300000) + (0.10 * 600000) + 0.20 * (annual_inc - 1200000)

    # Suggested allocation based on savings level
    if rate >= 30:
        alloc = {"equity": 0.6, "debt": 0.3, "cash": 0.1}
    elif rate >= 15:
        alloc = {"equity": 0.5, "debt": 0.35, "cash": 0.15}
    else:
        alloc = {"equity": 0.4, "debt": 0.4, "cash": 0.2}

    return AdviceResponse(
        monthly_income_total=round(month_inc, 2),
        monthly_expense_total=round(month_exp, 2),
        monthly_savings=savings,
        savings_rate_percent=rate,
        tax_bracket=bracket,
        estimated_annual_tax=round(annual_tax, 2),
        suggested_allocation=alloc,
)
