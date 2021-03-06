"""A persistent list"""

import bisect
import io
import struct
from typing import (
    Any,
    BinaryIO,
    Callable,
    Generic,
    Iterable,
    Iterator,
    List,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload
)

from jetblack_colstore.struct_stream import StructStream

T = TypeVar('T')


class StructList(MutableSequence[T]):

    def __init__(
            self,
            fmt: str,
            stream: BinaryIO
    ) -> None:
        super().__init__()
        self._stream: StructStream[T] = StructStream(
            fmt,
            stream,
            self.encode,
            self.decode
        )

    def _unpack_slice(self, index: slice) -> Tuple[int, int, int]:
        if index.step == 0:
            raise ValueError('slice step cannot be zero')
        n = len(self)
        start = index.start or 0
        stop = index.stop or n
        if start < 0:
            start += n
        if stop < 0:
            stop += n
        step = index.step or 1
        return start, stop, step

    def _get_value(self, index: int) -> T:
        if index < 0:
            index += len(self)
        if index >= len(self):
            raise IndexError('list index out of range')
        return self._stream.read(index)

    def _get_slice(self, index: slice) -> List[T]:
        start, stop, step = self._unpack_slice(index)
        return self._stream.read_many(start, stop, step)

    def _del_value(self, index: int) -> None:
        if index >= len(self):
            raise IndexError('list assignment index out of range')
        n = len(self)
        if index < 0:
            index += n
        if index < n - 1:
            start = index + 1
            count = n - start
            self._stream.copy(start, count, index)
        self._stream.truncate(n - 1)

    def _del_slice(self, index: slice) -> None:
        start, stop, step = self._unpack_slice(index)
        if step == 1:
            n = len(self)
            count = stop - start
            self._stream.copy(stop, count, start)
            self._stream.truncate(n - count)
        elif step > 0:
            for i in reversed(range(start, stop, step)):
                self._del_value(i)
        else:
            for i in range(stop - 1, start - 1, step):
                self._del_value(i)

    def _set_value(self, index: int, value: T) -> None:
        if index < 0:
            index += len(self)
        if index >= len(self):
            raise IndexError('list assignment index out of range')
        self._stream.write(index, value)

    def _set_slice(self, index: slice, values: Iterable[T]) -> None:
        start, stop, step = self._unpack_slice(index)
        if step == 1:
            self._stream.write_many(start, values)
        else:
            items = iter(values)
            for i in range(start, stop, step):
                self._set_value(i, next(items))

    def __len__(self) -> int:
        return self._stream.count()

    def __getitem__(self, index: Union[int, slice]) -> Union[T, MutableSequence[T]]:
        """Get a list item"""
        if isinstance(index, int):
            return self._get_value(index)
        elif isinstance(index, slice):
            return self._get_slice(index)
        else:
            raise ValueError('unhandled index type')

    def __delitem__(self, index: Union[int, slice]) -> None:
        if isinstance(index, int):
            self._del_value(index)
        elif isinstance(index, slice):
            self._del_slice(index)
        else:
            raise ValueError('unhandled index type')

    def __setitem__(self, index: Union[int, slice], value: Union[T, List[T]]) -> None:
        if isinstance(index, int):
            self._set_value(index, cast(T, value))
        elif isinstance(index, slice):
            self._set_slice(index, cast(Iterable[T], value))
        else:
            raise ValueError('unhandled index type')

    def insert(self, index: int, value: T) -> None:
        n = len(self)

        if index >= n:
            # Follow the behaviour of the builtin list.
            self.append(value)
            return

        if index < 0:
            index += n

        self._stream.copy(index, n - index, index + 1)
        self._stream.seek(index, io.SEEK_SET)
        self._stream.write(index, value)

    def __iadd__(self, values: Iterable[T]) -> MutableSequence[T]:
        self._stream.write_many(len(self), values)
        return self

    def append(self, value: T) -> None:
        self._stream.write(len(self), value)

    def add(
            self,
            value: T,
            lo: Optional[int] = None,
            hi: Optional[int] = None
    ) -> Tuple[int, int]:
        lo = 0 if lo is None else lo
        hi = len(self) if hi is None else hi
        left = bisect.bisect_left(self, value, lo, hi)
        right = bisect.bisect_right(self, value, left, hi)
        self.insert(right, value)
        return left, right

    def encode(self, *args: Any) -> T:
        return args[0]

    def decode(self, value: T) -> tuple:
        return (value,)

    def __iter__(self) -> Iterator[T]:
        def _iter():
            index = 0
            while index < len(self):
                yield self[index]
                index += 1
        return _iter()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, list):
            if len(self) != len(other):
                return False
            for i in range(len(other)):
                if self[i] != other[i]:
                    return False
            return True

        raise ValueError('unhandled type')

    def __repr__(self):
        return "<{0} {1}>".format(
            self.__class__.__name__,
            [item for item in self]
        )

    def __str__(self):
        return str([item for item in self])


if __name__ == '__main__':
    foo: StructList[int] = StructList(io.BytesIO(bytearray()), "<i")
    foo.append(1)
    foo.append(2)
    foo.append(3)
    foo.insert(0, 0)
    print(foo[0])
    print(foo[1])
    print(foo[2])
    print(foo)  # <MyList [1, 2, 3, 4, 5, 6]>
