from __future__ import annotations

import json

from enum import Enum
from typing import Any, Optional


class NodeType(Enum):
    def __new__(cls, label: str) -> Any:
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj
    
    def __repr__(self):
        return '<{class_name} {label}>'.format(
            class_name=self.__class__.__name__,
            label=self.label)
    
    SEQUENCE = ('Sequence', )
    EXPRESSION = ('Expression', )
    IDENTIFIER = ('Identifier', )
    ASSIGN = ('Assign', )
    INT = ('Integer', )


class Node:
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

    def as_dict(self):
        result = dict(type=self.type.label)
        if self.value:
            result['value'] = self.value
        if self.left:
            result['left'] = self.left.as_dict()
        if self.right:
            result['right'] = self.right.as_dict()
        return result

    def as_json(self):
        return json.dumps(self.as_dict(), indent=2)

    def __repr__(self):
        return '<{class_name} {type}>'.format(
            class_name=self.__class__.__name__,
            type=self.type.label)
