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

            for child in left_node.children: child.parent = left_node
            for child in right_node.children: child.parent = right_node

            parent, index = new_root.search(mid_key.key)

            parent._keys.insert(index, mid_key)
            parent._children.insert(index, right_node)
            parent._children.insert(index, left_node)

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
            
            for child in left_node.children: child.parent = left_node
            for child in right_node.children: child.parent = right_node
            
            parent, index = target.parent.search(mid_key.key)
            parent._children.pop(index)

            parent._keys.insert(index, mid_key)
            parent._children.insert(index, right_node)
            parent._children.insert(index, left_node)

            if parent.is_overflow():
                self.split(parent)
    
    @property
    def order(self):
        return self._order

if __name__ == '__main__':
    tree = BTree(3)

    for nmbr in range(1, 26):
        tree.insert(KeyEntry(nmbr, nmbr * 10))

    print(tree)

    print(tree.search(16, exact = True))
