from typing import Any, List, Tuple
from trie.node import *


def find(node: Node, key: str) -> Tuple[Any, str]:
    depth = 0
    prefix: List[str] = []
    for char in key:
        if node.has_next(char, depth):
            # Continue
            prefix.append(char)
            node = node.get_next(char)
        elif node.is_terminal:
            # Match and terminal
            return (node, ''.join(prefix))
        else:
            # No match
            return (None, ''.join(prefix))
        depth += 1
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


def insert_loop(node: Node, key: str, max_depth: int, exit_key: str, exit_node: Node) -> None:
    # Can this interface be improved?
    # Need to consume more than 1 key char and exit_key char
    loop_node = LoopNode(max_depth)
    node.set_next(key, loop_node)
    loop_node.set_next(exit_key, exit_node)
    return exit_node


if __name__ == '__main__':
    root = Node()
    insert(root, 'println', 'FUNCTION')
    insert(root, '(', 'SYMBOL')

    # Can we have a function to determine the loop?
    # Can we use a defaultdict for string and character sequences,
    # Where the default is to loop, oterhwsie if the character is a quote then it exists.

    insert_loop(root, '"', 1 + 2, '"', Node('CHAR LITERAL'))
    insert_loop(root, '"', 256 + 2, '"', Node('STRING LITERAL'))

    insert(root, ')', 'SYMBOL')
    insert(root, ';', 'COLON')
    insert(root, '', 'TERMINAL')

    find(root, 'println("abc123");')
