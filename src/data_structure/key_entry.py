"""

"""
from typing import Any


class KeyEntry:
    def __init__(self, key: int, value: Any = None):
        self._key = key
        self._value = value

    def __repr__(self):
        return f'({'🔑' if self.key and not self.value else ''}{self._key}:{self._value if self._value else ''})'
    
    @property
    def key(self):
        return self._key
    
    @property
    def value(self):
        return self._value
