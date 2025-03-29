"""

"""
from bisect import bisect_left, bisect_right

from key_entry import KeyEntry
from entry_result import EntryResult

n_node = 0


class Node:
    def __init__(self,
                 order: int,
                 is_root: bool = False, is_leaf: bool = True,
                 key: list[KeyEntry] = list(), children: list = list()):
        global n_node

        self._order: int = order

        self.is_root: bool = is_root
        self.is_leaf: bool = is_leaf

        self._keys: list[KeyEntry] = key
        self._children: list = children

        self.n_node = n_node
        n_node += 1

    def __len__(self):
        return len(self.keys)
    
    def __repr__(self):
        return f'#{self.n_node:03} ({self.keys}{'🫚 ' if self.is_root else ''}{'🌿' if self.is_leaf else ''})'

    def search(self, key: int, exact: bool = False):
        if exact:
            index = bisect_left(self.keys, key, key = lambda entry: entry.key)

            if index < len(self) \
            and self.keys[index].key != key:
                return EntryResult()
        else:
            index = bisect_right(self.keys, key, key = lambda entry: entry.key)

        return EntryResult(True, self, index)

    def is_overflow(self):
        return len(self) >= self.order
    
    @property
    def order(self):
        return self._order

    @property
    def keys(self):
        return self._keys
    
    @property
    def children(self):
        return self._children
