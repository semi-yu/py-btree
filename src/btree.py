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
        parent = None
        current = self.root

        while not current.is_leaf:
            index = bisect_left(current.keys, key, key = lambda entry: entry.key)

            if index < len(current) and current.keys[index].key == key:
                return EntryResult(True, current, index)

            parent = current
            current = current.children[index]

        return parent, current.search(key, exact)
    
    def insert(self, entry: KeyEntry):
        parent, result = self.search(entry.key)

        target, index = result

        target._keys.insert(index, entry)

        if target.is_overflow():
            self.split(parent, target)

    def split(self, parent: Node, target: Node):
        mid_point = len(target) // 2
        mid_key = target.keys[mid_point]
            
        if target.is_root:
            left_node = Node(order = self.order,
                        is_root = False, is_leaf = target.is_leaf,
                        key = target._keys[:mid_point], children = target._children[:mid_point+1])
            right_node = Node(order = self.order, is_leaf = target.is_leaf,
                         key = target._keys[mid_point+1:], children = target._children[mid_point+1:])

            new_root = Node(order = self.order,
                            is_root = True, is_leaf = False,
                            key = [mid_key], children = [left_node, right_node])

            self.root = new_root
    
    @property
    def order(self):
        return self._order

if __name__ == '__main__':
    tree = BTree(5)

    tree.root._keys = [KeyEntry(2, 10), KeyEntry(3, 30), KeyEntry(17, 30), KeyEntry(22, 30), KeyEntry(31, 30),]

    tree.insert(KeyEntry(7, 70))
    
    print(tree)
    
    print(tree.search(22, exact = True))


