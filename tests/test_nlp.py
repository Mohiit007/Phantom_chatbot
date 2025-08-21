import pytest
from backend.services.nlp import parse_goal_text


def test_parse_amount_with_currency_and_year():
    event, amount, year = parse_goal_text("Plan Goa trip Dec 2025 for ₹50000")
    assert "goa" in event.lower()
    assert amount == 50000.0
    assert year >= 2025


def test_parse_amount_in_lakhs():
    event, amount, year = parse_goal_text("Wedding in December 2026 for 8 lakhs")
    assert "wedding" in event.lower()
    assert amount == 800000.0
    assert year >= 2026 