"""Column store helpers"""

from typing import BinaryIO, Callable, Sequence

from .column_store import ColumnStore
from .struct_list import StructList

StructListFactory = Callable[[BinaryIO], StructList]


def open_column_store(
    filenames: Sequence[str],
    struct_lists: Sequence[StructListFactory]
) -> ColumnStore:
    stores = [
        struct_list(open(filename, "a+b"))
        for filename, struct_list in zip(filenames, struct_lists)
    ]
    return ColumnStore(*stores)
