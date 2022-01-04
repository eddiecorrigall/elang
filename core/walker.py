from typing import Any, Iterable, List, Optional, Tuple, Union

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
])


UNARY_OPERATORS = dict([
    (NodeType.NOT, lambda x: 0 if x else 1)
])


class IdentifierOperator:
    def __repr__(self) -> str:
        return '<{class_name} {identifier}>'.format(
            class_name=self.__class__.__name__,
            identifier=self.identifier)


class IdentifierArray(IdentifierOperator):
    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        self.indices = []
    
    def get(self, table: dict) -> Any:
        if self.identifier not in table:
            raise Exception('variable reference before assignment')
        item = table[self.identifier]
        for index in self.indices:
            item = item[index]
        return item

    def set(self, table: dict, value: Any) -> None:
        if self.identifier not in table:
            raise Exception('variable reference before assignment')
        item = table[self.identifier]
        for index in self.indices[:-1]:
            item = item[index]
        item[self.indices[-1]] = value


class IdentifierMap(IdentifierOperator):
    def __init__(self, identifier: str, key: Union[int, str, list]) -> None:
        self.identifier = identifier
        # Convert to hashable
        if isinstance(key, (List, Tuple)):
            if len(key) == 1:
                self.key = key[0]
            else:
                self.key = tuple(key)
        elif type(key) is int or type(key) is str:
            self.key = key
        else:
            raise Exception('unknown identifier map key type')
    
    @property
    def name(self):
        return self.identifier + '#'

    def get(self, table: dict) -> Union[int, str, list]:
        if self.identifier not in table:
            raise Exception('variable reference before assignment')
        default_value = table[self.identifier]
        if self.key in table[self.name]:
            return table[self.name][self.key]
        return default_value

    def set(self, table: dict, value: Union[int, str, list]) -> None:
        if self.name not in table:
            table[self.name] = dict()
        if self.identifier not in table:
            # Infer default value from type
            if type(value) is int:
                table[self.identifier] = 0
            elif type(value) is str:
                table[self.identifier] = str()
            else:
                raise Exception('unknown type of identifier key')
        table[self.name][self.key] = value


class Walker:
    def __init__(self):
        self.data = dict()
    
    def __call__(self, node: Node) -> Any:
        return self.walk(node)

    def fail(self, message: str, node: Optional[Node] = None, constructor = None) -> None:
        if constructor is None:
            constructor = lambda message: Exception(message)
        # TODO: Debugging information to assiciate node and token
        if node is None:
            raise constructor(message)
        else:
            info = [
                message,
                'node {}'.format(node.type.name),
            ]
            if node.value is not None:
                info.append('value {}'.format(node.value))
            if node.left is not None:
                left_value = self.walk(node.left)  # Probably trouble
                if isinstance(left_value, IdentifierOperator):
                    left_value = left_value.get(self.data)
                info.append('left value {}'.format(left_value))
            if node.right is not None:
                right_value = self.walk(node.right)  # Probably trouble
                if isinstance(right_value, IdentifierOperator):
                    right_value = right_value.get(self.data)
                info.append('right value {}'.format(right_value))
            raise constructor(' - ' .join(info))

    def assert_true(self, message: str, truthy: Any, node: Node) -> None:
        if not truthy:
            self.fail(message=message, node=node, constructor=AssertionError)

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
        elif isinstance(value, IdentifierOperator):
            self.print_str(value.get(self.data))
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
        elif node.type is NodeType.ARRAY:
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
        elif node.type is NodeType.IDENTIFIER_ARRAY:
            if node.left.type is NodeType.IDENTIFIER:
                # Leaf node: has name and index
                identifier_array = IdentifierArray(
                    identifier=node.left.value)
            else:
                # Inner node: has index only
                identifier_array = self.walk(node.left)  # identifier index
            index = self.walk(node.right)  # expression
            identifier_array.indices.append(index)
            return identifier_array
        elif node.type is NodeType.IDENTIFIER_MAP:
            if node.left.type is not NodeType.IDENTIFIER:
                self.fail('identifier map missing identifier')
            return IdentifierMap(
                identifier=node.left.value,
                key=self.walk(node.right))
        elif node.type is NodeType.ASSIGN:
            value = self.walk(node.right)  # expression
            if isinstance(value, IdentifierOperator):
                # Dereference
                value = value.get(self.data)
            if node.left.type is NodeType.IDENTIFIER_ARRAY:
                identifier_array = self.walk(node.left)
                identifier_array.set(self.data, value)
            elif node.left.type is NodeType.IDENTIFIER_MAP:
                identifier_map = self.walk(node.left)
                identifier_map.set(self.data, value)
            elif node.left.type is NodeType.IDENTIFIER:
                identifier = node.left.value
                self.data[identifier] = value
            else:
                self.fail('cannot assign to unknown type')
            return value
        elif node.type in BINARY_OPERATORS:
            operation = BINARY_OPERATORS[node.type]
            left = self.walk(node.left)
            if isinstance(left, IdentifierOperator):
                # Dereference
                left = left.get(self.data)
            right = self.walk(node.right)
            if isinstance(right, IdentifierOperator):
                # Dereference
                right = right.get(self.data)
            return operation(left, right)
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
        elif node.type is NodeType.ASSERT:
            expression_parenthesis = self.walk(node.left)
            self.assert_true(
                message='assertion failed',
                node=node.left,
                truthy=expression_parenthesis,
            )
        else:
            self.fail('unknown node type', node)
