"""

"""
from bisect import bisect_left, bisect_right

from key_entry import KeyEntry
from entry_result import EntryResult


class Node:
    def __init__(self,
                 order: int, parent = None, prev = None, next = None,
                 is_root: bool = False, is_leaf: bool = True,
                 key: list[KeyEntry] = None, children: list = None):
        self._order: int = order

        self.is_root: bool = is_root
        self.is_leaf: bool = is_leaf
        self.parent: Node = parent

        self.prev: Node = prev
        self.next: Node = next

        self._keys: list[KeyEntry] = key or []
        self._children: list = children or []

    def __len__(self):
        return len(self.keys)
    
    def __repr__(self):
        return f'({self.keys}{self.determine_sign()})'

    def determine_sign(self):
        sign = str()
        if self.is_root:
            sign += '🫚 '

        if self.is_leaf:
            sign += '🌿'

        if not self.is_root and not self.is_leaf:
            sign = '📦'

        return sign

    def search(self, key: int, exact: bool = False):
        if exact:
            index = bisect_left(self.keys, key, key = lambda entry: entry.key)

            if index < len(self) \
            and self.keys[index].key != key:
                return EntryResult()

            if index >= len(self): return EntryResult()
        else:
            index = bisect_right(self.keys, key, key = lambda entry: entry.key)

        return EntryResult(True, self, index)

    def is_overflow(self):
        return len(self) >= self.order
    
    def is_underflow(self):
        if self.is_root: return False
        return len(self) < self.order // 2

    @property
    def order(self):
        return self._order

    @property
    def keys(self):
        return self._keys
    
    @property
    def children(self):
        return self._children

    @property
    def is_internal(self):
        return not self.is_root and not self.is_leaf
