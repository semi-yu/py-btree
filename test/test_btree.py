"""

"""
import pytest
from random import choice, shuffle

from src.data_structure.btree import BTree
from src.data_structure.key_entry import KeyEntry


def get_value():
    meta_synt = [
        'spam',
        'ham',
        'eggs',
    ]

    return choice(meta_synt)

@pytest.mark.parametrize("order", [3, 4, 5, 6, 7, 10, 20])
def test_insert_and_delete(order):
    bt = BTree(order)

    # 삽입: 순차적
    seq_keys = list(range(1, 100))
    insert_entries(bt, seq_keys)

    validate_tree(bt.root, order)

    # 삭제 테스트
    delete_entries(bt, seq_keys)

    validate_tree(bt.root, order)

    # 삽입: 무작위
    bt = BTree(order)
    random_keys = list(range(1, 100))
    shuffle(random_keys)
    insert_entries(bt, random_keys)

    # 트리 제약조건 및 참조 무결성 확인
    validate_tree(bt.root, order)

@pytest.mark.parametrize("order", [3, 4, 5, 6, 7, 10, 20])
def test_node_linkage(order):
    bt = BTree(order)

    for key in range(1, 101):
        bt.insert(KeyEntry(key, get_value()))

    # traverse minimum
    most_left = bt.root

    while most_left:
        current = most_left

        while current:
            if current.prev: assert current.prev.next is current
            if current.next: assert current.next.prev is current

            current = current.next

        if most_left.is_internal:
            most_left = most_left.children[0]
        else:
            break

def insert_entries(bt, keys):
    for key in keys:
        bt.insert(KeyEntry(key, get_value()))

        validate_tree(bt.root, bt.order)

def delete_entries(bt, keys):
    for key in keys:
        bt.delete(key)

        validate_tree(bt.root, bt.order)

def validate_tree(node, order, parent=None):
    assert node is not None, 'Node is null'
    assert node.is_root or parent is not None, 'All nodes must have a parent node except root node'

    assert len(node.keys) <= order + 1, 'All nodes must the less keys than order + 1'
    if not node.is_root: assert len(node.keys) >= 1, 'All nodes must at least have one key'

    for idx in range(len(node.keys[:-1])):
        assert node.keys[idx].key < node.keys[idx+1].key, 'All keys must kept in ascending order'

    if node.is_root and not node.is_leaf:
        assert len(node.keys) >= 1, 'Root node must have at least one key'

    if parent:
        assert node.parent == parent, 'Parent node must be same'

    if node.is_leaf:
        assert len(node.children) == 0, 'Leaf node does not have children node references'
    elif node.is_internal:
        assert len(node.children) == len(node.keys) + 1, 'Internal nodes must have k keys and k+1 children references'

        for i, child in enumerate(node.children):
            validate_tree(child, order, node)

    if node.prev and node.prev.next:
        assert node.prev.next == node, 'Next node must be same'
    if node.next and node.next.prev:
        assert node.next.prev == node, 'Previous node must be same'
