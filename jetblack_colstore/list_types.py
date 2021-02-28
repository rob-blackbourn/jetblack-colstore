"""List Types"""

from datetime import datetime
from typing import Any, BinaryIO

from .struct_list import StructList


class IntList(StructList[int]):

    def __init__(self, stream: BinaryIO) -> None:
        super().__init__("<i", stream)


class DatetimeList(StructList[datetime]):

    def __init__(self, stream: BinaryIO) -> None:
        super().__init__(
            "<q",
            stream
        )

    def encode(self, *args: Any) -> datetime:
        return datetime.fromtimestamp(args[0] / 1000000)

    def decode(self, value: datetime) -> tuple:
        return (int(value.timestamp() * 1000000),)


class StringList(StructList[str]):

    def __init__(
            self,
            stream: BinaryIO,
            length: int,
            encoding: str = "utf-8"
    ) -> None:
        super().__init__(
            f"<{length}s",
            stream
        )
        self.encoding = encoding

    def encode(self, *args: Any) -> str:
        return args[0].rstrip(b'\0x').decode(self.encoding)

    def decode(self, value: str) -> tuple:
        return (value.encode(self.encoding),)
