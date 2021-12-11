from typing import Any, List, Tuple
from trie.node import Node


def find(node: Node, key: str) -> Tuple[Any, str]:
    prefix: List[str] = []
    for char in key:
        if node.has_next(char):
            # Continue
            prefix.append(char)
            node = node.get_next(char)
        elif node.is_terminal:
            # Match and terminal
            return (node, ''.join(prefix))
        else:
            # No match
            return (None, ''.join(prefix))
    if node.is_terminal:
        # Match and terminal
        return (node, ''.join(prefix))
    else:
        # No match
        return (None, ''.join(prefix))


def insert(node: Node, key: str, value: Any) -> Node:
    for char in key:
        if not node.has_next(char):
            node.set_next(char, Node())
        node = node.get_next(char)
    node.value = value
    return node
