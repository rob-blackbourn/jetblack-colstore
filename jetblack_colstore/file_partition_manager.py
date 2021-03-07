"""A file partition manager"""

import os
import os.path
from typing import Callable, Sequence

from .column_store import ColumnStore
from .caches import LRUCache
from .helpers import open_column_store, StructListFactory


class FilePartitionManager:

    def __init__(
        self,
        folder: str,
        max_size: int,
        make_key: Callable[[tuple], tuple],
        struct_list_factories: Sequence[StructListFactory]
    ) -> None:
        self.folder = folder
        self.make_key = make_key
        self.struct_list_factories = struct_list_factories
        self.cache: LRUCache[tuple, ColumnStore] = LRUCache(max_size)

    def get_column_store(self, *values: tuple) -> ColumnStore:
        key = self.make_key(values)
        if self.cache.contains(key):
            return self.cache.get(key)

        path = self.folder
        for part in key:
            path = os.path.join(path, str(part))

        os.makedirs(path, exist_ok=True)

        filenames = [
            os.path.join(path, f'{i}.dat')
            for i in range(len(self.struct_list_factories))
        ]
        store = open_column_store(filenames, self.struct_list_factories)
        _evicted_key, evicted_store = self.cache.set(key, store)
        if evicted_store is not None:
            evicted_store.close()

        return store

    def close(self) -> None:
        for _, store in self.cache.clear():
            store.close()
