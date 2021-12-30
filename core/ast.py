from __future__ import annotations

import json

from enum import Enum
from typing import Iterable, Optional


NodeType = Enum('NodeType', [
    'SEQUENCE',
    'EXPRESSION',
    'ADD',
    'SUBTRACT',
    'MULTIPLY',
    'DIVIDE',
    'MOD',
    'EQUAL',
    'NOT_EQUAL',
    'LESS_THAN',
    'LESS_THAN_OR_EQUAL',
    'GREATER_THAN',
    'GREATER_THAN_OR_EQUAL',
    'AND',
    'OR',
    'NOT',
    'IDENTIFIER',
    'ASSIGN',
    'INT',
    'STR',
    'WHILE',
    'IF',
    'ELSE',
    'PRINT_CHARACTER',
    'PRINT_STRING',
])


LEAF_NODE_TYPES = frozenset([
    NodeType.IDENTIFIER,
    NodeType.INT,
    NodeType.STR,
])


class Node:
    @property
    def is_leaf(self) -> bool:
        return self.type in LEAF_NODE_TYPES
    
    @property
    def label(self) -> str:
        return self.type.name

    def __init__(
            self,
            type: NodeType,
            left: Optional[Node] = None,
            right: Optional[Node] = None,
            value: Optional[str] = None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

    def as_dict(self) -> dict:
        # Recursive traversal
        result = dict(type=self.label)
        if self.value:
            result['value'] = self.value
        if self.left:
            result['left'] = self.left.as_dict()
        if self.right:
            result['right'] = self.right.as_dict()
        return result

    def as_json(self) -> str:
        # Recursive traversal
        return json.dumps(self.as_dict(), indent=2)

    def as_lines(self) -> Iterable[str]:
        # Non-recursive traversal
        stack = [self]
        while stack:
            node = stack.pop()  # Pop (from end)
            if node is None:
                yield ';'
            elif node.is_leaf:
                yield '%s\t%s' % (node.label, node.value)
            else:
                yield node.label
                stack.append(node.right)  # Push (to end)
                stack.append(node.left)  # Push (to end)

    def as_lines_recursive(self, node: Node) -> Iterable[str]:
        if node is None:
            yield ';'
        else:
            if node.is_leaf:
                yield '%s\t%s' % (node.label, node.value)
            else:
                yield node.label
                for left_node in self.as_lines_recursive(node.left):
                    yield left_node
                for right_node in self.as_lines_recursive(node.right):
                    yield right_node

    def __repr__(self) -> str:
        return '<{class_name} {type}>'.format(
            class_name=self.__class__.__name__,
            type=self.label)
