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
    IDENTIFIER = ('Identifier', True)
    ASSIGN = ('Assign', )
    INT = ('Integer', True)


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
        result = dict(type=self.type.label)
        if self.value:
            result['value'] = self.value
        if self.left:
            result['left'] = self.left.as_dict()
        if self.right:
            result['right'] = self.right.as_dict()
        return result

    def as_json(self) -> str:
        return json.dumps(self.as_dict(), indent=2)
    
    def as_lines(self) -> Iterable[str]:
        # Non-recursive traversal
        stack = [self]
        while stack:
            node = stack.pop()
            if node is None:
                continue
            elif node.is_leaf:
                yield '%s\t%s' % (node.label, node.value)
            else:
                yield node.label
                stack.insert(0, node.left)
                stack.insert(0, node.right)
        yield ';'

    def __repr__(self) -> str:
        return '<{class_name} {type}>'.format(
            class_name=self.__class__.__name__,
            type=self.type.label)
