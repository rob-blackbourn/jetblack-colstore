"""Example"""

from copy import copy
import io
from random import Random

from jetblack_colstore.column_store import ColumnStore
from jetblack_colstore.list_types import IntList


def main():
    store = ColumnStore(
        [
            IntList(io.BytesIO()),
            IntList(io.BytesIO()),
            IntList(io.BytesIO()),
        ]
    )

    rows = [
        (1, 1, 1),
        (1, 1, 2),
        (1, 1, 3),
        (1, 2, 1),
        (1, 2, 2),
        (1, 2, 3),
        (1, 3, 1),
        (1, 3, 2),
        (1, 3, 3),
        (2, 1, 1),
        (2, 1, 2),
        (2, 1, 3),
        (2, 2, 1),
        (2, 2, 2),
        (2, 2, 3),
        (2, 3, 1),
        (2, 3, 2),
        (2, 3, 3),
        (3, 1, 1),
        (3, 1, 2),
        (3, 1, 3),
        (3, 2, 1),
        (3, 2, 2),
        (3, 2, 3),
        (3, 3, 1),
        (3, 3, 2),
        (3, 3, 3),
    ]
    for row in rows:
        store.add(*row)

    values = store[:4]
    print(values)


if __name__ == '__main__':
    main()
