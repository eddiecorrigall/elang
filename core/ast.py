from __future__ import annotations

import json

from enum import Enum
from typing import Any, Iterable, Optional


class NodeType(Enum):
    def __new__(cls, label: str, is_leaf = False) -> Any:
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        obj.is_leaf = is_leaf
        return obj
    
    def __repr__(self):
        return '<{class_name} {label}>'.format(
            class_name=self.__class__.__name__,
            label=self.label)
    
    SEQUENCE = ('Sequence', )
    EXPRESSION = ('Expression', )
    ADD = ('Add', )
    SUBTRACT = ('Subtract', )
    MULTIPLY = ('Multiply', )
    DIVIDE = ('Divide', )
    MOD = ('Mod', )
    NOT = ('Not', )
    LESS_THAN = ('LessThan', )
    LESS_OR_EQUAL_THAN = ('LessThanOrEqual', )
    GREATER_THAN = ('GreaterThan', )
    GREATER_OR_EQUAL_THAN = ('GreaterOrEqualThan', ),
    IDENTIFIER = ('Identifier', True)
    ASSIGN = ('Assign', )
    INT = ('Integer', True)
    STR = ('String', True)
    WHILE = ('While', )
    IF = ('If', )
    ELSE = ('Else', )
    PRINT_CHARACTER = ('Print_character', )


class Node:
    @property
    def is_leaf(self) -> bool:
        return self.type.is_leaf
    
    @property
    def label(self) -> str:
        return self.type.label

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
        result = dict(type=self.type.label)
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
            type=self.type.label)
