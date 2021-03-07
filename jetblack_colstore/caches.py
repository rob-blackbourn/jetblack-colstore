"""Caches"""

from typing import Dict, Generic, List, Optional, Tuple, TypeVar

TKey = TypeVar('TKey')
TValue = TypeVar('TValue')


class LRUCache(Generic[TKey, TValue]):

    def __init__(
            self,
            max_size: int
    ) -> None:
        self.max_size = max_size
        self._keys: List[TKey] = []
        self._data: Dict[TKey, TValue] = {}

    def contains(self, key: TKey) -> bool:
        return key in self._data

    def get(self, key: TKey) -> TValue:
        return self._data[key]

    def set(self, key: TKey, value: TValue) -> Tuple[Optional[TKey], Optional[TValue]]:
        if key in self._data:
            index = self._keys.index(key)
            if index > 0:
                del self._keys[index]
                self._keys.insert(0, key)
            return None, None

        self._keys.insert(0, key)
        self._data[key] = value
        if len(self._keys) <= self.max_size:
            return None, None

        key_to_evict = self._keys.pop()
        value_to_evict = self._data.pop(key_to_evict)
        return key_to_evict, value_to_evict

    def clear(self) -> List[Tuple[TKey, TValue]]:
        items = list(self._data.items())
        self._data.clear()
        del self._keys[:]
        return items

    def __len__(self) -> int:
        return len(self._keys)
