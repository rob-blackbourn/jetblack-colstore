"""Tests for ColumnStore"""

import io

from jetblack_colstore.column_store import ColumnStore
from jetblack_colstore.list_types import IntList


def test_append():
    store = ColumnStore(
        [
            IntList(io.BytesIO()),
            IntList(io.BytesIO()),
            IntList(io.BytesIO()),
        ]
    )

    store.append(1, 10, 100)
    store.append(2, 20, 200)
    store.append(3, 30, 300)

    assert store[0] == (1, 10, 100)
    assert store[1] == (2, 20, 200)
    assert store[2] == (3, 30, 300)
