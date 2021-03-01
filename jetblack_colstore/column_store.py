"""A column store"""

from typing import List, Union

from .struct_list import StructList


class ColumnStore:

    def __init__(
        self,
        struct_lists: List[StructList]
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

    def __getitem__(self, index: Union[int, slice]) -> Union[tuple, List[tuple]]:
        return tuple(
            struct_list[index]
            for struct_list in self.struct_lists
        )
