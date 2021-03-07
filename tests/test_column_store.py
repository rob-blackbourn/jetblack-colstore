"""Tests for ColumnStore"""

from copy import copy
import io
from random import Random

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


def test_insert():
    store = ColumnStore(
        [
            IntList(io.BytesIO()),
            IntList(io.BytesIO()),
            IntList(io.BytesIO()),
        ]
    )

    store.insert(0, 3, 30, 300)
    store.insert(0, 1, 10, 100)
    store.insert(1, 2, 20, 200)

    assert store[0] == (1, 10, 100)
    assert store[1] == (2, 20, 200)
    assert store[2] == (3, 30, 300)


def test_add():
    store = ColumnStore(
        [
            IntList(io.BytesIO()),
            IntList(io.BytesIO()),
            IntList(io.BytesIO()),
        ]
    )

    store.add(3, 30, 300)
    store.add(1, 10, 100)
    store.add(2, 20, 200)

    assert store[0] == (1, 10, 100)
    assert store[1] == (2, 20, 200)
    assert store[2] == (3, 30, 300)


def test_add_nested_sort():
    """Add sorted rows in a random order"""

    rows = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                rows.append(tuple([i, j, k]))

    for seed in range(100):
        random = Random(seed)
        store = ColumnStore(
            [
                IntList(io.BytesIO()),
                IntList(io.BytesIO()),
                IntList(io.BytesIO()),
            ]
        )

        candidate_rows = copy(rows)
        random.shuffle(candidate_rows)
        for row in candidate_rows:
            store.add(*row)

        for index, row in enumerate(rows):
            if store[index] != row:
                print(store[index], row)
            assert store[index] == row


def test_set():
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

    store[0] = (4, 40, 400)
    store[1:] = [
        (5, 50, 500),
        (6, 60, 600)
    ]

    assert store[0] == (4, 40, 400)
    assert store[1] == (5, 50, 500)
    assert store[2] == (6, 60, 600)


def test_delete():
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

    del store[0]
    assert len(store) == 2

    del store[:]
    assert len(store) == 0
