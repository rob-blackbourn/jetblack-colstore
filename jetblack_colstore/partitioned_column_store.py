"""A partitioned column store"""

from typing import Any, BinaryIO, Callable, Dict, Tuple

from .column_store import ColumnStore

ColumnStoreFactory = Callable[[Tuple[BinaryIO, ...]], ColumnStore]
PartitionFactory = Callable[[tuple], Tuple[BinaryIO, ...]]


class PartitionedColumnStore:

    def __init__(
            self,
            column_store_factory: ColumnStoreFactory,
            make_partition_key: Callable[[tuple], tuple],
            partition_factory: PartitionFactory
    ) -> None:
        self._column_store_factory = column_store_factory
        self._make_partition_key = make_partition_key
        self._partition_factory = partition_factory
        self._column_stores: Dict[tuple, ColumnStore] = {}

    def append(self, *values: Any) -> None:
        column_store = self._get_column_store(*values)
        column_store.append(*values)

    def _get_column_store(self, *values: Any) -> ColumnStore:
        key = self._make_partition_key(*values)
        if key not in self._column_stores:
            streams = self._partition_factory(key)
            self._column_stores[key] = self._column_store_factory(streams)
        return self._column_stores[key]
