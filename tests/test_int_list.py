"""Tests for IntList"""

import io

from jetblack_colstore.list_types import IntList


def test_smoke():
    """Smoke test"""
    l = IntList(io.BytesIO())
    l += [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert l == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
