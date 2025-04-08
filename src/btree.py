"""

"""
from bisect import bisect_left

from .traverse import traverse

from .key_entry import KeyEntry
from .entry_result import EntryResult
from .node import Node


class BTree:
    def __init__(self,
                 order: int):
        self._order = order

        self.root = Node(
            order = order,
            is_root = True, is_leaf = True)
        
    def __repr__(self):
        return traverse(self.root)

    def search(self, key: int, start: Node = None, exact: bool = False):
        current = start or self.root

        while not current.is_leaf:
            index = bisect_left(current.keys, key, key = lambda entry: entry.key)

            if index < len(current) and current.keys[index].key == key:
                return EntryResult(True, current, index)
            current = current.children[index]

        return current.search(key, exact)

    def insert(self, entry: KeyEntry):
        target, index = self.search(entry.key)
        target._keys.insert(index, entry)

        if target.is_overflow():
            self.split(target)

    def split(self, target: Node):
        mid_point = len(target) // 2
        mid_key = target.keys[mid_point]

        # generate new root
        if target.is_root:
            parent = Node(order = self.order, parent = None,
                            is_root = True, is_leaf = False)
        # inherit original parent
        else:
            parent = target.parent

        left_node, right_node = target.split(parent)
        _, index = parent.search(mid_key.key)

        if target.is_root:
            self.root = parent
        else:
            parent._children.pop(index)

        parent._keys.insert(index, mid_key)
        parent._children.insert(index, left_node)
        parent._children.insert(index+1, right_node)

        if parent.is_overflow():
            self.split(parent)

    def delete(self, key: int):
        target, index = self.search(key, exact = True)

        if target is None: return

        # remove and rebalance
        if target.is_leaf:
            target._keys.pop(index)
            node = target
        else:
            node = self.trawl(target, index)

        if node.is_underflow():
            return self.balance(node)

    def balance(self, target: Node):
        sibling = self.get_sibling(target)

        if self.is_rotatable(target):
            self.rotate(target, sibling)
            return
        else:
            parent = self.merge(target, sibling)

            if parent.is_underflow():
                return self.balance(parent)

    def is_rotatable(self, target: Node) -> bool:
        if target.prev and target.prev.parent is target.parent:
            if len(target.prev) - 1 > self.order // 2: return True

        if target.next and target.next.parent is target.parent:
            if len(target.next) - 1 > self.order // 2: return True

        return False

    def get_sibling(self, target: Node) -> Node:
        if target.prev and target.prev.parent is target.parent:
            return target.prev
        else: # target.next and target.next.parent is target.parent
            return target.next

    def parent_index_and_key(self, destination: Node, source: Node) -> tuple[Node, int, KeyEntry]:
        if destination.next is source:
            parent, index = destination.parent.search(source._keys[0].key)
            index -= 1
        else: # destination.prev is source
            parent, index = destination.parent.search(source._keys[-1].key)

        key = parent._keys[index]

        return parent, index, key

    def rotate(self, destination: Node, source: Node):
        parent, parent_index, parent_key = self.parent_index_and_key(destination, source)

        if destination.next is source: # counter-clockwise rotation
            destination._keys.insert(len(destination._keys), parent_key)
            parent._keys[parent_index] = source._keys.pop(0)
        elif destination.prev is source:
            destination._keys.insert(0, parent_key)
            parent._keys[parent_index] = source._keys.pop(-1)

    def merge(self, destination: Node, source: Node) -> Node:
        parent, parent_index, parent_key = self.parent_index_and_key(destination, source)

        if destination.next is source:
            merged = destination.merge(source, parent_key)
        elif destination.prev is source:
            merged = source.merge(destination, parent_key)

        parent._keys.pop(parent_index)
        parent._children.pop(parent_index)
        parent._children.pop(parent_index)
        parent._children.insert(parent_index, merged)

        if parent is self.root and len(self.root) == 0:
            self.root = merged
            merged.is_root = True

        return merged.parent

    def trawl(self, target: Node, index: int) -> Node:
        # get smallest from right
        node = target._children[index + 1]
        while not node.is_leaf:
            node = node._children[0]

        # change key
        target._keys[index] = node._keys.pop(0)

        return node

    @property
    def order(self) -> int:
        return self._order
