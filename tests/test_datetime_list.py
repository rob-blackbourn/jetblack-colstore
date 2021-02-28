"""Tests for IntList"""

from datetime import datetime
import io

from jetblack_colstore.list_types import DatetimeList


def test_smoke():
    """Smoke test"""
    l = DatetimeList(io.BytesIO())
    orig = [datetime(2020, 1, 1, 12, 23, 56), datetime(2020, 1, 1, 13, 22, 12)]
    l += orig
    assert l == orig
