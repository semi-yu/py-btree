"""

"""
from bisect import bisect_left

from traverse import traverse

from key_entry import KeyEntry
from entry_result import EntryResult
from node import Node


class BTree:
    def __init__(self,
                 order: int):
        self._order = order

        self.root = Node(
            order = order,
            is_root = True, is_leaf = True)
        
    def __repr__(self):
        return traverse(self.root)

    def search(self, key: int, exact: bool = False):
        current = self.root

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
            
        if target.is_root:
            new_root = Node(order = self.order, parent = None,
                            is_root = True, is_leaf = False,
                            key = [], children = [])

            left_node = Node(order = self.order, parent = new_root,
                             is_root = False, is_leaf = target.is_leaf,
                             key = target._keys[:mid_point], children = target._children[:mid_point+1])
            right_node = Node(order = self.order, parent = new_root,
                              is_root = False, is_leaf = target.is_leaf,
                              key = target._keys[mid_point+1:], children = target._children[mid_point+1:])

            if target.prev: target.prev.next = left_node

            left_node.prev = target.prev
            left_node.next = right_node

            right_node.prev = left_node

            if target.next: target.next.prev = right_node

            for child in left_node.children: child.parent = left_node
            for child in right_node.children: child.parent = right_node

            parent, index = new_root.search(mid_key.key)

            parent._keys.insert(index, mid_key)
            parent._children.insert(index, left_node)
            parent._children.insert(index + 1, right_node)

            self.root = new_root
        else:
            left_node = Node(order = self.order, parent = target.parent,
                             is_root = False, is_leaf = target.is_leaf,
                             key = target._keys[:mid_point], children = target._children[:mid_point+1])
            right_node = Node(order = self.order, parent = target.parent,
                              is_root = False, is_leaf = target.is_leaf,
                              key = target._keys[mid_point+1:], children = target._children[mid_point+1:])

            if target.prev: target.prev.next = left_node

            left_node.prev = target.prev
            left_node.next = right_node

            right_node.prev = left_node

            if target.next: target.next.prev = right_node

            for child in left_node.children: child.parent = left_node
            for child in right_node.children: child.parent = right_node
            
            parent, index = target.parent.search(mid_key.key)
            parent._children.pop(index)

            parent._keys.insert(index, mid_key)
            parent._children.insert(index, left_node)
            parent._children.insert(index+1, right_node)

            if parent.is_overflow():
                self.split(parent)

    def delete(self, entry: KeyEntry):
        target, index = self.search(entry.key, exact = True)

        if target is None: return

        # remove and rebalance
        if target.is_leaf:
            target._keys.pop(index)
            node = target
        else:
            node = self.borrow_from_child(target, index)

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

    def rotate(self, destination: Node, source: Node):
        if destination.next is source: # counter-clockwise rotation
            parent, parent_index = destination.parent.search(source._keys[0].key)
            parent_index -= 1

            destination._keys.insert(len(destination._keys), parent._keys[parent_index+0])
            parent._keys[parent_index+0] = source._keys.pop(0)
        elif destination.prev is source:
            parent, parent_index = destination.parent.search(source._keys[-1].key)

            destination._keys.insert(0, parent._keys[parent_index])
            parent._keys[parent_index] = source._keys.pop(-1)

    def merge(self, destination: Node, source: Node) -> Node:
        merged = Node(
            order = self.order, parent = destination.parent,
            is_root = destination.is_root, is_leaf = destination.is_leaf
        )

        if destination.next is source:
            parent, parent_index = destination.parent.search(source._keys[0].key)
            parent_index -= 1
            parent_key = parent._keys[parent_index]

            if destination.prev: destination.prev.next = merged
            merged.prev = destination.prev
            merged.next = source.next
            if source.next: source.next.prev = merged

            merged._keys = destination._keys + [parent_key] + source._keys
            merged._children = destination._children + source._children
        elif destination.prev is source:
            parent, parent_index = destination.parent.search(source._keys[-1].key)
            parent_key = parent._keys[parent_index]

            if source.prev: source.prev.next = merged
            merged.prev = source.prev
            merged.next = destination.next
            if destination.next: destination.next.prev = merged

            merged._keys = source._keys + [parent_key] + destination._keys
            merged._children = source._children + destination._children

        for child in merged._children:
            child.parent = merged

        parent._keys.pop(parent_index)
        parent._children.pop(parent_index)
        parent._children.pop(parent_index)
        parent._children.insert(parent_index, merged)

        if parent is self.root and len(self.root) == 0:
            self.root = merged
            merged.is_root = True

        return merged.parent

    def borrow_from_child(self, target: Node, index: int) -> Node:
        # get smallest from right
        node = target._children[index + 1]
        while not node.is_leaf:
            node = node._children[0]

        # change key
        target._keys[index] = node._keys.pop(0)

        return node

    @property
    def order(self):
        return self._order
