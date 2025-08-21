import re
from datetime import datetime
from typing import Optional, Tuple

from dateparser.search import search_dates


LAKH_KEYWORDS = {"lakh", "lakhs", "lac", "lacs", "l"}
CRORE_KEYWORDS = {"crore", "crores", "cr"}


def _to_amount(number_str: str, unit: Optional[str]) -> Optional[float]:
    try:
        number = float(number_str.replace(",", ""))
    except Exception:
        return None
    unit_norm = (unit or "").lower()
    if unit_norm in LAKH_KEYWORDS:
        return number * 100_000
    if unit_norm in CRORE_KEYWORDS:
        return number * 10_000_000
    return number


def _extract_amount(text: str) -> Optional[float]:
    t = text.strip()
    t = t.replace("Rs.", "Rs").replace("rs.", "rs")

    # 1) Look for contextual phrases like 'for/budget/cost/amount'
    ctx_pattern = r"(?:for|budget|cost|amount)\s*(?:of|is|=|:)?\s*(₹|rs|inr)?\s*([0-9][0-9,]*\.?[0-9]*)\s*(lakh|lakhs|lac|lacs|l|crore|crores|cr)?"
    m = re.search(ctx_pattern, t, flags=re.IGNORECASE)
    if m:
        amt = _to_amount(m.group(2), m.group(3))
        if amt is not None:
            return amt

    # 2) Explicit currency symbol first (₹ or Rs/INR)
    currency_patterns = [
        r"₹\s*([0-9][0-9,]*\.?[0-9]*)\s*(lakh|lakhs|lac|lacs|l|crore|crores|cr)?",
        r"(?:rs|inr)\s*([0-9][0-9,]*\.?[0-9]*)\s*(lakh|lakhs|lac|lacs|l|crore|crores|cr)?",
    ]
    for pat in currency_patterns:
        m = re.search(pat, t, flags=re.IGNORECASE)
        if m:
            amt = _to_amount(m.group(1), m.group(2) if len(m.groups()) >= 2 else None)
            if amt is not None:
                return amt

    # 3) Numbers with explicit units (lakhs/crore)
    unit_pattern = r"([0-9][0-9,]*\.?[0-9]*)\s*(lakh|lakhs|lac|lacs|l|crore|crores|cr)\b"
    m = re.search(unit_pattern, t, flags=re.IGNORECASE)
    if m:
        amt = _to_amount(m.group(1), m.group(2))
        if amt is not None:
            return amt

    # 4) As a last resort, avoid bare numbers to prevent picking years
    return None


def _extract_year(text: str) -> Optional[int]:
    now_year = datetime.now().year

    # Prefer natural date parsing
    try:
        results = search_dates(text, settings={"PREFER_DATES_FROM": "future"})
        if results:
            for _, dt in results:
                year = dt.year
                if year >= now_year:
                    return year
            return results[-1][1].year
    except Exception:
        pass

    # Fallback: explicit year like 2025, 2026
    candidates = re.findall(r"(?<![0-9])20[2-9][0-9](?![0-9])", text)
    for c in candidates:
        year = int(c)
        if year >= now_year:
            return year
    return None


def _extract_event_name(text: str) -> str:
    t = text.strip()
    t = re.sub(r"\s+", " ", t)

    parts = re.split(r"\sfor\s", t, flags=re.IGNORECASE)
    candidate = parts[0]

    candidate = re.sub(r"^(plan(ning)?\s+|please\s+|my\s+|a\s+)", "", candidate, flags=re.IGNORECASE)

    candidate = re.sub(r"\b(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(t)?(ember)?|oct(ober)?|nov(ember)?|dec(ember)?)\b\s*20[0-9]{2}", "", candidate, flags=re.IGNORECASE)

    candidate = re.sub(r"(₹|inr|rs\.?)[^ ]+", "", candidate, flags=re.IGNORECASE)

    candidate = candidate.strip(" -:,")
    return candidate or "Goal"


def parse_goal_text(text: str) -> Tuple[str, float, int]:
    """Parse free text and return (event_name, today_cost, target_year)."""
    event_name = _extract_event_name(text)
    amount = _extract_amount(text)
    year = _extract_year(text)

    if amount is None:
        raise ValueError("Could not detect amount from text")
    if year is None:
        raise ValueError("Could not detect target year from text")

    return event_name, float(amount), int(year) 