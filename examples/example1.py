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

    copy_of_rows = copy(rows)
    rand = Random(3)
    while copy_of_rows:
        index = rand.randrange(len(copy_of_rows))
        row = copy_of_rows.pop(index)
        print('adding', row)
        store.add(*row)
        for i in range(len(store)):
            print(store[i])
        print()

    for index, row in enumerate(rows):
        if store[index] != row:
            print(store[index], row)


if __name__ == '__main__':
    main()
