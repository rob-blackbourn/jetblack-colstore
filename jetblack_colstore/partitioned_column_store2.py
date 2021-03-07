"""A partitioned column store"""

from typing import Any, BinaryIO, Callable, Dict, Tuple

from .column_store import ColumnStore


class PartitionedColumnStore:

    def __init__(
            self,
            column_store_accessor: Callable[[tuple], ColumnStore]
    ) -> None:
        self._column_store_accessor = column_store_accessor

    def append(self, *values: Any) -> None:
        column_store = self._column_store_accessor(*values)
        column_store.append(*values)
