"""

"""
from key_entry import KeyEntry

class Node:
    def __init__(self,
                 order: int,
                 is_root: bool = False, is_leaf: bool = True,
                 key: list[KeyEntry] = list(), children: list = list()):
        self._order: int = order

        self._is_root: bool = is_root
        self._is_leaf: bool = is_leaf
        
        self._key: list[KeyEntry] = key
        self._children: list = children

    