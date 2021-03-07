"""A column store"""

from typing import List, Sequence, Union

from .struct_list import StructList


class ColumnStore:

    def __init__(
        self,
        *struct_lists: StructList
    ) -> None:
        self.struct_lists = struct_lists

    def append(self, *values) -> None:
        if len(values) != len(self.struct_lists):
            raise ValueError('value count mismatch')

        for struct_list, value in zip(self.struct_lists, values):
            struct_list.append(value)

    def insert(self, index: int, *values) -> None:
        if len(values) != len(self.struct_lists):
            raise ValueError('value count mismatch')

        for struct_list, value in zip(self.struct_lists, values):
            struct_list.insert(index, value)

    def add(self, *values) -> None:
        if len(values) != len(self.struct_lists):
            raise ValueError('value count mismatch')

        lo = hi = None
        for struct_list, value in zip(self.struct_lists, values):
            lo, hi = struct_list.add(value, lo, hi)

    def close(self) -> None:
        for struct_list in self.struct_lists:
            struct_list.close()

    def __getitem__(self, index: Union[int, slice]) -> Union[tuple, List[tuple]]:
        values = tuple(
            struct_list[index]
            for struct_list in self.struct_lists
        )
        return list(zip(*values)) if isinstance(index, slice) else values

    def __setitem__(
            self,
            index: Union[int, slice],
            values: Union[tuple, Sequence[tuple]]
    ) -> None:
        if isinstance(index, int):
            for struct_list, value in zip(self.struct_lists, values):
                struct_list[index] = value
        elif isinstance(index, slice):
            for i, struct_list in enumerate(self.struct_lists):
                struct_list[index] = [value[i] for value in values]

    def __delitem__(self, index: Union[int, slice]) -> None:
        for struct_list in self.struct_lists:
            del struct_list[index]

    def __len__(self) -> int:
        return len(self.struct_lists[0])
