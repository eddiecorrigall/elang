from typing import Any, Optional

from core.ast import Node, NodeType


BINARY_OPERATORS = dict([
    (NodeType.ADD, lambda a, b: a + b),
    (NodeType.SUBTRACT, lambda a, b: a - b),
    (NodeType.MULTIPLY, lambda a, b: a * b),
    (NodeType.DIVIDE, lambda a, b: a // b),
    (NodeType.MOD, lambda a, b: a % b),
    (NodeType.EQUAL, lambda a, b: a == b),
    (NodeType.NOT_EQUAL, lambda a, b: a != b),
    (NodeType.LESS_THAN, lambda a, b: a < b),
    (NodeType.LESS_THAN_OR_EQUAL, lambda a, b: a <= b),
    (NodeType.GREATER_THAN, lambda a, b: a > b),
    (NodeType.GREATER_THAN_OR_EQUAL, lambda a, b: a >= b),
    (NodeType.AND, lambda a, b: a and b),
    (NodeType.OR, lambda a, b: a or b),
    (NodeType.IDENTIFIER_INDEX, lambda array, index: array[index])
])


UNARY_OPERATORS = dict([
    (NodeType.NOT, lambda x: 0 if x else 1)
])


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
                'name {}'.format(node.type.name),
                'value {}'.format(node.value),
            ]))

    def print_str(self, value: str) -> None:
        print(value, end=str())

    def print(self, value: Any) -> None:
        if type(value) is int:
            self.print_str(str(value))
        elif type(value) is str:
            self.print_str(value)
        elif type(value) is list:
            for item in value:
                self.print(item)
        else:
            self.fail('cannot print unknown value type')

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
        elif node.type is NodeType.ARY:
            array = []
            right_value = self.walk(node.right)
            if right_value is not None:
                array.extend(right_value)
            left_value = self.walk(node.left)
            array.append(left_value)
            return array
        elif node.type is NodeType.IDENTIFIER:
            name = node.value
            if name in self.data:
                return self.data[name]
            else:
                self.fail('variable referenced before assignment', node)
        elif node.type is NodeType.ASSIGN:
            value = self.walk(node.right)  # expression
            if node.left.type is NodeType.IDENTIFIER_INDEX:
                name = node.left.left.value  # identifier
                index = self.walk(node.left.right)  # expression
                self.data[name][index] = value
            else:
                name = node.left.value  # identifier
                self.data[name] = value
            return value
        elif node.type in BINARY_OPERATORS:
            operation = BINARY_OPERATORS[node.type]
            return operation(
                self.walk(node.left),
                self.walk(node.right))
        elif node.type in UNARY_OPERATORS:
            operation = UNARY_OPERATORS[node.type]
            return operation(self.walk(node.left))
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
        elif node.type is NodeType.PRINT_STRING:
            # TODO: handle escaped characters
            value = self.walk(node.left)
            self.print(value)
        else:
            self.fail('unknown node type', node)
