from typing import Any, Optional

from core.ast import Node, NodeType


class Walker:
    def __init__(self):
        self.data = dict()
    
    def __call__(self, node: Node) -> Any:
        return self.walk(node)

    def fail(self, message: str, node: Optional[Node] = None) -> None:
        # TODO: Debugging information to assiciate node and token
        if node is None:
            raise Exception(message)
        else:
            raise Exception(' - ' .join([
                message,
                'label {}'.format(node.label),
                'value {}'.format(node.value),
            ]))

    def walk(self, node: Node) -> Any:
        # TODO: Convert to non-recursive
        if node is None:
            return
        elif node.type is NodeType.SEQUENCE:
            self.walk(node.right)
            self.walk(node.left)
        elif node.type is NodeType.STR:
            return node.value
        elif node.type is NodeType.INT:
            return int(node.value)
        elif node.type is NodeType.IDENTIFIER:
            name = node.value
            if name in self.data:
                return self.data[name]
            else:
                self.fail('variable referenced before assignment', node)
        elif node.type is NodeType.ASSIGN:
            name = node.left.value
            value = self.walk(node.right)
            self.data[name] = value
            return value
        elif node.type is NodeType.MULTIPLY:
            return self.walk(node.left) * self.walk(node.right)
        elif node.type is NodeType.ADD:
            return self.walk(node.left) + self.walk(node.right)
        elif node.type is NodeType.LESS_THAN:
            return self.walk(node.left) < self.walk(node.right)
        elif node.type is NodeType.IF:
            if self.walk(node.left):
                self.walk(node.right.left)
            else:
                self.walk(node.right.right)
        elif node.type is NodeType.WHILE:
            while self.walk(node.left):
                self.walk(node.right)
        elif node.type is NodeType.PRINT_CHARACTER:
            # TODO: Why does `putc(144);` cause the walker stdout to stop?
            value = self.walk(node.left)
            character = chr(value)
            print(character, end=str())
        else:
            self.fail('unknown node type', node)
