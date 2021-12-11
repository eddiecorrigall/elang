from __future__ import annotations
from typing import Any, Dict, Optional


class Node:
    def __init__(self, value = None) -> None:
        self.next: Dict[str, Node] = dict()
        self.value: Optional[Any] = value

    def __repr__(self) -> str:
        return '<{name}: [{value}]>'.format(
            name=self.__class__.__name__,
            value=self.value)

    @property
    def is_terminal(self):
        return self.value is not None
    
    def has_next(self, char: str) -> bool:
        return char in self.next
    
    def get_next(self, char: str) -> Node:
        return self.next[char]
    
    def set_next(self, char: str, node: Node) -> None:
        self.next[char] = node
