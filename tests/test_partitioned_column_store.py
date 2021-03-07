"""Tests for partitioned column stores"""

import io
from typing import BinaryIO, Dict, Tuple

from jetblack_colstore.partitioned_column_store import PartitionedColumnStore
from jetblack_colstore.column_store import ColumnStore
from jetblack_colstore.list_types import IntList


class PartitionConfig:

    def __init__(self) -> None:
        self.partition_cache: Dict[
            Tuple[int, int],
            Tuple[BinaryIO, BinaryIO, BinaryIO]
        ] = {}

    def column_store_factory(
            self,
            streams: Tuple[BinaryIO, BinaryIO, BinaryIO]
    ) -> ColumnStore:
        return ColumnStore(
            IntList(streams[0]),
            IntList(streams[1]),
            IntList(streams[2])
        )

    def make_partition_key(
            self,
            first: int,
            second: int,
            _third: int
    ) -> Tuple[int, int]:
        return first % 10, second % 100

    def partition_factory(
            self,
            key: Tuple[int, int]
    ) -> Tuple[BinaryIO, BinaryIO, BinaryIO]:
        streams = self.partition_cache.get(key)
        if streams is None:
            streams = (io.BytesIO(), io.BytesIO(), io.BytesIO())
            self.partition_cache[key] = streams
        return streams


def test_smoke():
    config = PartitionConfig()
    store = PartitionedColumnStore(
        config.column_store_factory,
        config.make_partition_key,
        config.partition_factory
    )
    store.append(1, 12, 100)
