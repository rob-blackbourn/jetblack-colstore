"""Tests for StringList"""

import io

from jetblack_colstore.list_types import StringList


def test_smoke():
    """Smoke test"""
    l = StringList(io.BytesIO(), 10)
    l += ["tom", "dick", "harry", ""]
    assert l == ["tom", "dick", "harry", ""]
