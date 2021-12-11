from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple

# force consume one char in char literal


class Node:
    def __init__(self, value=None) -> None:
        self.next: Dict[str, Node] = dict()
        self.value: Optional[Any] = value

    def __repr__(self) -> str:
        return '<{name} value="{value}">'.format(
            name=self.__class__.__name__,
            value=self.value)

    @property
    def is_terminal(self):
        return self.value is not None
    
    def has_next(self, char: str, depth=None) -> bool:
        return char in self.next
    
    def get_next(self, char: str) -> Node:
        return self.next[char]
    
    def set_next(self, char: str, node: Node) -> None:
        self.next[char] = node


class LoopNode(Node):
    def __init__(self, max_depth=None) -> None:
        super().__init__()
        self.max_depth: Optional[int] = max_depth

    def has_next(self, char: str, depth: int) -> bool:
        if self.max_depth is not None and self.max_depth == depth:
            return False
        # Loops always have next
        return True
    
    def get_next(self, char: str) -> Node:
        if super().has_next(char):
            return super().get_next(char)
        # By default, anything not defined as next loops back
        return self
