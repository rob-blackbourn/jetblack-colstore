"""Tests for ColumnStore"""

from copy import copy
import io
import random

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


def test_add2():
    store = ColumnStore(
        [
            IntList(io.BytesIO()),
            IntList(io.BytesIO()),
            IntList(io.BytesIO()),
        ]
    )

    store.add(1, 1, 1)
    store.add(1, 1, 2)
    store.add(1, 1, 3)
    store.add(1, 2, 1)
    store.add(1, 2, 2)
    store.add(1, 2, 3)
    store.add(1, 3, 1)
    store.add(1, 3, 2)
    store.add(1, 3, 3)
    store.add(2, 1, 1)
    store.add(2, 1, 2)
    store.add(2, 1, 3)
    store.add(2, 2, 1)
    store.add(2, 2, 2)
    store.add(2, 2, 3)
    store.add(2, 3, 1)
    store.add(2, 3, 2)
    store.add(2, 3, 3)
    store.add(3, 1, 1)
    store.add(3, 1, 2)
    store.add(3, 1, 3)
    store.add(3, 2, 1)
    store.add(3, 2, 2)
    store.add(3, 2, 3)
    store.add(3, 3, 1)
    store.add(3, 3, 2)
    store.add(3, 3, 3)

    assert store[0] == (1, 1, 1)
    assert store[1] == (1, 1, 2)
    assert store[2] == (1, 1, 3)
    assert store[3] == (1, 2, 1)
    assert store[4] == (1, 2, 2)
    assert store[5] == (1, 2, 3)
    assert store[6] == (1, 3, 1)
    assert store[7] == (1, 3, 2)
    assert store[8] == (1, 3, 3)

    assert store[9] == (2, 1, 1)
    assert store[10] == (2, 1, 2)
    assert store[11] == (2, 1, 3)
    assert store[12] == (2, 2, 1)
    assert store[13] == (2, 2, 2)
    assert store[14] == (2, 2, 3)
    assert store[15] == (2, 3, 1)
    assert store[16] == (2, 3, 2)
    assert store[17] == (2, 3, 3)

    assert store[18] == (3, 1, 1)
    assert store[19] == (3, 1, 2)
    assert store[20] == (3, 1, 3)
    assert store[21] == (3, 2, 1)
    assert store[22] == (3, 2, 2)
    assert store[23] == (3, 2, 3)
    assert store[24] == (3, 3, 1)
    assert store[25] == (3, 3, 2)
    assert store[26] == (3, 3, 3)


def test_add3():
    store = ColumnStore(
        [
            IntList(io.BytesIO()),
            IntList(io.BytesIO()),
            IntList(io.BytesIO()),
        ]
    )

    store.add(1, 1, 1)
    store.add(2, 1, 2)
    store.add(3, 2, 3)
    store.add(3, 2, 2)
    store.add(3, 1, 1)
    store.add(1, 1, 2)
    store.add(1, 1, 3)
    store.add(3, 2, 1)
    store.add(2, 2, 2)
    store.add(3, 3, 3)
    store.add(3, 3, 1)
    store.add(3, 1, 2)
    store.add(1, 2, 1)
    store.add(2, 3, 2)
    store.add(1, 2, 2)
    store.add(2, 2, 1)
    store.add(2, 1, 1)
    store.add(3, 3, 2)
    store.add(1, 2, 3)
    store.add(2, 2, 3)
    store.add(1, 3, 1)
    store.add(1, 3, 2)
    store.add(1, 3, 3)
    store.add(3, 1, 3)
    store.add(2, 1, 3)
    store.add(2, 3, 1)
    store.add(2, 3, 3)

    assert store[0] == (1, 1, 1)
    assert store[1] == (1, 1, 2)
    assert store[2] == (1, 1, 3)
    assert store[3] == (1, 2, 1)
    assert store[4] == (1, 2, 2)
    assert store[5] == (1, 2, 3)
    assert store[6] == (1, 3, 1)
    assert store[7] == (1, 3, 2)
    assert store[8] == (1, 3, 3)

    assert store[9] == (2, 1, 1)
    assert store[10] == (2, 1, 2)
    assert store[11] == (2, 1, 3)
    assert store[12] == (2, 2, 1)
    assert store[13] == (2, 2, 2)
    assert store[14] == (2, 2, 3)
    assert store[15] == (2, 3, 1)
    assert store[16] == (2, 3, 2)
    assert store[17] == (2, 3, 3)

    assert store[18] == (3, 1, 1)
    assert store[19] == (3, 1, 2)
    assert store[20] == (3, 1, 3)
    assert store[21] == (3, 2, 1)
    assert store[22] == (3, 2, 2)
    assert store[23] == (3, 2, 3)
    assert store[24] == (3, 3, 1)
    assert store[25] == (3, 3, 2)
    assert store[26] == (3, 3, 3)

# def test_add_complex():
#     store = ColumnStore(
#         [
#             IntList(io.BytesIO()),
#             IntList(io.BytesIO()),
#             IntList(io.BytesIO()),
#         ]
#     )

#     values = []
#     for i in range(3):
#         for j in range(3):
#             for k in range(3):
#                 values.append(tuple([i, j, k]))

#     random.seed(0)
#     candidate_values = copy(values)
#     while candidate_values:
#         index = random.randrange(len(candidate_values))
#         row = candidate_values.pop(index)
#         store.add(*row)

#     for index, row in enumerate(values):
#         if store[index] != row:
#             print(store[index], row)
#         assert store[index] == row
