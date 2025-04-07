"""

"""
import pytest

from random import choice

from src.btree import BTree
from src.key_entry import KeyEntry


def get_value():
    meta = ['spam', 'ham', 'eggs']
    return choice(meta)

@pytest.fixture
def empty_tree():
    tree = BTree(3)
    return tree

@pytest.fixture
def single_level():
    tree = BTree(3)

    for n in range(1, 4):
        tree.insert(KeyEntry(n, get_value()))

    return tree

@pytest.fixture
def double_level():
    tree = BTree(3)
    
    for n in range(1, 11):
        tree.insert(KeyEntry(n, get_value()))

    return tree

@pytest.fixture
def triple_level():
    tree = BTree(3)

    for n in range(1, 21):
        tree.insert(KeyEntry(n, get_value()))

    return tree

def test_default_search_on_empty_tree(empty_tree):
    result = empty_tree.search(42)
    assert result, 'Default search on empty b-tree always yields true'

    res_node, index = result
    assert res_node is empty_tree.root, 'Default search on empty b-tree ends at a root node'
    assert index == 0, 'Default search on empty b-tree ends at the first location, 0'

def test_default_search_on_single_level(single_level):
    result = single_level.search(1)
    assert result, 'Default search'

    for k in range(1, 4):
        node, index = single_level.search(key = k)
        assert node.keys[index-1].key <= k, 'Default search yields the next index'

    node, index = single_level.search(42)
    assert node.keys[index - 1].key < 42, 'Default search on non-existing element yields the next index'

def test_default_search_on_double_level(double_level):
    result = double_level.search(1)
    assert result, 'Default search'

    node, index = double_level.search(42)
    assert node.keys[index - 1].key < 42, 'Default search on non-existing element yields the next index'

def test_exact_search_on_empty_tree(empty_tree):
    result = empty_tree.search(42, exact = True)
    assert not result, 'Exact search on empty b-tree always yields false'

    res_node, index = result
    assert res_node is None, 'Exact search on emptry b-tree yields None'
    assert index == None, 'Exact search on emptry b-tree yields None'

def test_exact_search_on_single_level(single_level):
    for k in range(1, 4):
        result = single_level.search(key = k, exact = True)
        assert result, 'Exact search on existing element yields true'

        node, index = result
        assert node.keys[index].key == k, 'Exact search yields the exact index'
    
    result = single_level.search(42, exact = True)
    assert not result, 'Exact search on non-existing element yields None'

def test_exact_search_on_double_level(double_level):
    for k in range(1, 11):
        result = double_level.search(key = k, exact = True)
        assert result, 'Exact search on existing element yields true'

        node, index = result
        assert node.keys[index].key == k, 'Default search yields the exact index'

    result = double_level.search(42, exact = True)
    assert not result, 'Exact search on non-existing element yields None'

def test_exact_search_on_triple_level(triple_level):
    for k in range(1, 21):
        result = triple_level.search(key = k, exact = True)
        assert result, 'Exact search on existing element yields true'

        node, index = result
        assert node.keys[index].key == k, 'Exact search yields the exact index'

    result = triple_level.search(42, exact = True)
    assert not result, 'Exact search on non-existing element yields None'
