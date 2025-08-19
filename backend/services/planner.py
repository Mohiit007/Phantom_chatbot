# from backend.utils.finance import years_until, future_value, monthly_saving_needed
# from backend.settings import settings

# def _get_inflation_percent() -> float:
#     """
#     Try to use Mohit's script if available, else fall back to .env value.
#     Expecting the script function to return {'inflation_percent': <float>}.
#     """
#     try:
#         # Optional dependency on your scripts/ module
#         from scripts.fetch_worldbank_inflation import fetch_latest_inflation  # type: ignore
#         data = fetch_latest_inflation()
#         pct = float(data.get("inflation_percent"))  # may raise if missing; caught below
#         if pct > 0:
#             return pct
#     except Exception:
#         pass
#     return float(settings.fallback_inflation)

# def plan_event(event_name: str, today_cost: float, target_year: int) -> dict:
#     """Return a complete plan object (no DB involved)."""
#     inflation_pct = _get_inflation_percent()
#     yrs = years_until(target_year)
#     fut = future_value(today_cost, inflation_pct, yrs)
#     monthly = monthly_saving_needed(fut, yrs * 12)

#     return {
#         "event_name": event_name,
#         "target_year": target_year,
#         "today_cost": today_cost,
#         "inflation_percent_used": inflation_pct,
#         "years_to_goal": yrs,
#         "future_cost": fut,
#         "monthly_saving_needed": monthly,
#     }
from backend.utils.finance import years_until, future_value, monthly_saving_needed
from backend.settings import settings
from backend.services.inflation import fetch_worldbank_inflation  # 👈 

def _get_inflation_percent() -> float:
    """Fetch real inflation if possible, else fallback."""
    try:
        data = fetch_worldbank_inflation()
        pct = float(data.get("inflation_percent"))
        if pct > 0:
            return pct
    except Exception:
        pass
    return float(settings.fallback_inflation)

def plan_event(event_name: str, today_cost: float, target_year: int) -> dict:
    inflation_pct = _get_inflation_percent()
    yrs = years_until(target_year)
    fut = future_value(today_cost, inflation_pct, yrs)
    monthly = monthly_saving_needed(fut, yrs * 12)

    return {
        "event_name": event_name,
        "target_year": target_year,
        "today_cost": today_cost,
        "inflation_percent_used": inflation_pct,
        "years_to_goal": yrs,
        "future_cost": fut,
        "monthly_saving_needed": monthly,
    }
