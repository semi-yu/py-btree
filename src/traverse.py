"""

"""
from .node import Node

def traverse(node: Node, level: int = 0):
    ret = '\t' * level + f'{str(node)}' + '\n'
    
    for child in node.children:
        ret += traverse(child, level + 1)

    return ret