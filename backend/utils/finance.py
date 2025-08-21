from datetime import datetime

def years_until(target_year: int) -> int:
    """How many whole years from now until the target_year (min 0)."""
    now = datetime.now().year
    return max(0, target_year - now)

def future_value(today_cost: float, annual_inflation_pct: float, years: int) -> float:
    """Compound today_cost by inflation for 'years'."""
    r = annual_inflation_pct / 100.0
    return round(today_cost * ((1 + r) ** years), 2)

def monthly_saving_needed(future_cost: float, months: int) -> float:
    """Evenly spread future_cost across remaining months."""
    if months <= 0:
        return round(future_cost, 2)
    return round(future_cost / months, 2)
