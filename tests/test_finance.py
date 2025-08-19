import re
from datetime import datetime

from backend.utils.finance import years_until, future_value, monthly_saving_needed


def test_years_until_non_negative():
    current_year = datetime.now().year
    assert years_until(current_year) == 0
    assert years_until(current_year + 3) == 3


def test_future_value_compounding():
    assert future_value(100_000, 10, 0) == 100000.0
    assert future_value(100_000, 10, 1) == 110000.0


def test_monthly_saving_needed_basic():
    assert monthly_saving_needed(120_000, 12) == 10000.0
    assert monthly_saving_needed(60_000, 0) == 60000.0 