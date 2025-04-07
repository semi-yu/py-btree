"""

"""
import pytest

from src.node import Node
from src.entry_result import EntryResult

def test_init_as_default_node():
    node = Node(
        order = 4
    )

    assert node.order == 4, 'A node must not change the order arbitrary'
    assert node.parent is None, 'Without given parent, a node does not hold any parent node'
    assert node.prev is None, 'Without given prev, a node does not hold any previous node'
    assert node.next is None, 'Without given next, a node does not hold any next node'

    assert not node.is_root, 'Without given value, a node is not a root node'
    assert node.is_leaf, 'Without given value, a node is a leaf node'

    assert node.keys == [], 'Without given key, a node has an empty key list'
    assert node.children == [], 'Without given key, a node has an empty children list'

def test_init_as_root_node():
    node = Node(
        order = 4, is_root = True
    )
    assert node.is_root, 'With given value, a node is a root node'
    assert node.is_leaf, 'Without given value, a node is a leaf node'

def test_determine_sign():
    node = Node(order = 4)
    assert node.determine_sign() == '🌿', 'Without given, A node is a leaf node'

    node = Node(order = 4, is_root = True)
    assert node.determine_sign() == '🫚 🌿', 'A root and a leaf node is possible'

    node = Node(order = 4, is_leaf = False)
    assert node.determine_sign() == '📦', 'A node that is neither root nor leaf, is a internal node'

    node = Node(order = 4, is_root = True, is_leaf = False)
    assert node.determine_sign() == '🫚 ', 'A Node can be only a root node'

def test_search_on_empty_node_default():
    node = Node(order = 4)

    result: EntryResult = node.search(key = 10)
    assert result, 'Search result on empty node without exact mode must return True'
    result_node, index = result
    assert result_node is node, 'Node search must return same node that was invoked searching'
    assert index == 0, 'Searched index on empty node must return 0, the first location'

def test_search_on_empty_node_with_exact_mode():
    node = Node(order = 4)

    result: EntryResult = node.search(key = 11, exact = True)
    assert not result, 'Search result on empty node with exact mode must return False'

    result_node, index = result
    assert result_node is None, 'Exact search and its result node on empty node must return None'
    assert index is None, 'Exact search and its index on emptry node must return None'
