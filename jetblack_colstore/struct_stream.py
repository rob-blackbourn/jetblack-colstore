"""A struct stream"""

import io
import struct
from typing import (
    Any,
    BinaryIO,
    Callable,
    Generic,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar
)

T = TypeVar('T')


def _encode(*args: Any) -> T:
    return args[0]


def _decode(value: T) -> tuple:
    return (value,)


class StructStream(Generic[T]):

    def __init__(
            self,
            fmt: str,
            stream: BinaryIO,
            encode: Optional[Callable[..., T]] = None,
            decode: Optional[Callable[[T], tuple]] = None
    ) -> None:
        self.fmt = fmt
        self.stream = stream
        self.size = struct.calcsize(fmt)
        self.encode = encode or _encode
        self.decode = decode or _decode

    def seek(self, offset: int, whence: int) -> int:
        return self.stream.seek(offset * self.size, whence) // self.size

    def tell(self) -> int:
        return self.stream.tell() // self.size

    def read(self, index) -> T:
        self.seek(index, io.SEEK_SET)
        buf = self.stream.read(self.size)
        value = struct.unpack(self.fmt, buf)
        return self.encode(*value)

    def read_many(self, start: int, stop: int, step: int) -> List[T]:
        self.seek(start, io.SEEK_SET)
        count = stop - start
        buf = self.stream.read(self.size * count)
        values = [
            self.encode(*value)
            for value in struct.iter_unpack(self.fmt, buf)
        ]
        if step == 1:
            return values

        return values[::step]

    def write(self, index: int, value: T) -> None:
        buf = struct.pack(self.fmt, *self.decode(value))
        self.seek(index, io.SEEK_SET)
        self.stream.write(buf)

    def write_many(self, index: int, values: Iterable[T]) -> None:
        self.seek(index, io.SEEK_SET)
        for value in values:
            buf = struct.pack(self.fmt, *self.decode(value))
            self.stream.write(buf)

    def count(self) -> int:
        return self.seek(0, io.SEEK_END)

    def copy(self, start: int, count, index: int) -> None:
        self.seek(start, io.SEEK_SET)
        buf = self.stream.read(count * self.size)
        self.seek(index, io.SEEK_SET)
        self.stream.write(buf)

    def truncate(self, count: int) -> None:
        self.stream.truncate(self.size * count)
