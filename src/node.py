"""

"""
from bisect import bisect_left, bisect_right

from .key_entry import KeyEntry
from .entry_result import EntryResult


class Node:
    def __init__(self,
                 order: int, parent = None, prev = None, next = None,
                 is_root: bool = False, is_leaf: bool = True,
                 keys: list[KeyEntry] = None, children: list = None):
        self._order: int = order

        self.is_root: bool = is_root
        self.is_leaf: bool = is_leaf
        self.parent: Node = parent

        self.prev: Node = prev
        self.next: Node = next

        self._keys: list[KeyEntry] = keys or []
        self._children: list = children or []

    def __len__(self):
        return len(self.keys)
    
    def __repr__(self):
        return f'({self.keys}{self.symbol()})'

    def symbol(self):
        sign = str()
        if self.is_root: sign += '🫚 '
        if self.is_leaf: sign += '🌿'

        if not self.is_root and not self.is_leaf: sign = '📦'

        return sign

    def search(self, key: int, exact: bool = False):
        index = bisect_left(self.keys, key, key = lambda entry: entry.key)

        if exact:
            if index < len(self) \
            and self.keys[index].key != key:
                return EntryResult()

            if index >= len(self): return EntryResult()

        return EntryResult(True, self, index)

    def split(self, parent_node):
        mid_point: int = len(self) // 2

        left_node = Node(self.order, parent = parent_node,
                         is_root = False, is_leaf = self.is_leaf,
                         keys = self._keys[:mid_point], children = self._children[:mid_point+1])
        right_node = Node(self.order, parent = parent_node,
                          is_root = False, is_leaf = self.is_leaf,
                          keys = self._keys[mid_point+1:], children = self._children[mid_point+1:])

        if self.prev: self.prev.next = left_node

        left_node.prev = self.prev
        left_node.next = right_node
        right_node.prev = left_node

        if self.next: self.next.prev = right_node

        for child in left_node.children: child.parent = left_node
        for child in right_node.children: child.parent = right_node

        return left_node, right_node

    def merge(self, other, parent_key: KeyEntry):
        merged = Node(
            order = self.order, parent = self.parent,
            is_root = self.is_root, is_leaf = self.is_leaf
        )

        if self.prev: self.prev.next = merged
        merged.prev = self.prev
        merged.next = other.next
        if other.next: other.next.prev = merged

        merged._keys = self.keys + [parent_key] + other.keys
        merged._children = self.children + other.children

        for child in merged._children:
            child.parent = merged

        return merged

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
