"""List Types"""

from datetime import datetime
from typing import Any, BinaryIO

from .struct_list import StructList


class IntList(StructList[int]):

    def __init__(self, stream: BinaryIO) -> None:
        super().__init__("<i", stream)


def _encode_datetime(*args: Any) -> datetime:
    return datetime.fromtimestamp(args[0] / 1000000)


def _decode_datetime(value: datetime) -> tuple:
    return (int(value.timestamp() * 1000000),)


class DatetimeList(StructList[datetime]):

    def __init__(self, stream: BinaryIO) -> None:
        super().__init__(
            "<q",
            stream,
            _encode_datetime,
            _decode_datetime
        )
