"""

"""


class EntryResult:
    def __init__(self, found: bool = False, node = None, index: int = None):
        self._found = found
        self._node = node
        self._index = index
    
    def __bool__(self):
        return self._found

    def __iter__(self):
        yield self._node
        yield self._index

    def __repr__(self):
        return f'({self._node}, {self._index})' if self._found else '(Not found)'