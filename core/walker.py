import sys
from typing import Any, List, Optional, Tuple, Union

from core.ast import Node, NodeType
from core.variables import Table, Variable, VariableType


def as_int(value: Union[int, bool]) -> int:
    return 1 if value else 0


BINARY_OPERATORS = dict([
    # Returns integer
    (NodeType.ADD, lambda a, b: a + b),
    (NodeType.SUBTRACT, lambda a, b: a - b),
    (NodeType.MULTIPLY, lambda a, b: a * b),
    (NodeType.DIVIDE, lambda a, b: a // b),
    (NodeType.MOD, lambda a, b: a % b),

    # Returns 1 or 0
    (NodeType.EQUAL, lambda a, b: as_int(a == b)),
    (NodeType.NOT_EQUAL, lambda a, b: as_int(a != b)),
    (NodeType.LESS_THAN, lambda a, b: as_int(a < b)),
    (NodeType.LESS_THAN_OR_EQUAL, lambda a, b: as_int(a <= b)),
    (NodeType.GREATER_THAN, lambda a, b: as_int(a > b)),
    (NodeType.GREATER_THAN_OR_EQUAL, lambda a, b: as_int(a >= b)),

    # Binary, but does not necessarily return int
    (NodeType.AND, lambda a, b: a and b),
    (NodeType.OR, lambda a, b: a or b),
])


UNARY_OPERATORS = dict([
    (NodeType.NOT, lambda x: 0 if x else 1)
])


def expect_variable(
    table: Table,
    name: str,
    type: Optional[VariableType] = None,
) -> Variable:
    variable, _ = table.get(name)
    if variable.is_undefined:
        raise Exception(
            'variable reference before assignment - {} is undefined'.format(name))
    if type and type is not variable.type:
        raise Exception(
            'variable type mismatch - {} is not of type {}'.format(name, type))
    return variable


class IdentifierOperator:
    def __repr__(self) -> str:
        return '<{class_name} {identifier}>'.format(
            class_name=self.__class__.__name__,
            identifier=self.identifier)


class IdentifierArray(IdentifierOperator):
    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        self.indices = []
    
    def get(self, table: Table) -> Any:
        variable = expect_variable(table, self.identifier, VariableType.ARRAY)
        item = variable.value
        for index in self.indices:
            item = item[index]
        return item

    def set(self, table: Table, value: Any) -> None:
        variable = expect_variable(table, self.identifier, VariableType.ARRAY)
        item = variable.value
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

    def get(self, table: Table) -> Union[int, str, list]:
        # Default variable must be defined, and (TODO) match type of key-value pair
        default_variable = expect_variable(table, self.identifier)
        map_variable = expect_variable(table, self.name, VariableType.MAP)
        if self.key in map_variable.value:
            value = map_variable.value[self.key]
            return value
        return default_variable.value

    def set(self, table: Table, value: Union[int, str, list]) -> None:
        default_variable = expect_variable(table, self.identifier)
        if default_variable.is_undefined:
            # Infer default value from type
            if type(value) is int:
                table.set(Variable(self.identifier, VariableType.INT, 0))
            elif type(value) is str:
                table.set(Variable(self.identifier, VariableType.STR, str()))
            elif type(value) is list:
                table.set(Variable(self.identifier, VariableType.ARRAY, list()))
            else:
                raise Exception('unknown type of identifier key')
        map_variable, _ = table.get(self.name)
        if map_variable.is_undefined:
            map_variable = Variable(self.name, VariableType.MAP, dict())
            table.set(map_variable)
        map_variable.value[self.key] = value


class Walker:
    def __init__(self):
        self.table = Table()

    def __call__(self, node: Node, stdout=None) -> Any:
        self.stdout = stdout or sys.stdout
        return self.walk(node)

    def fail(self, message: str, node: Optional[Node] = None, constructor = None) -> None:
        if constructor is None:
            constructor = lambda message: Exception(message)
        self.debug(message, node)
        raise constructor(message)

    def debug_info(self, message: str, node: Node) -> str:
        info = [
            message,
            'node {}'.format(node.type.name),
        ]
        if node.value is not None:
            info.append('value {}'.format(node.value))
        '''
        if node.left is not None:
            left_value = self.walk(node.left)  # Probably trouble
            left_value = self.dereference(left_value)
            info.append('left value {}'.format(left_value))
        if node.right is not None:
            right_value = self.walk(node.right)  # Probably trouble
            right_value = self.dereference(right_value)
            info.append('right value {}'.format(right_value))
        '''
        return ' - ' .join(info)

    def debug(self, message: str, node: Optional[Node] = None) -> None:
        # TODO: Debugging information to assiciate node and token
        if node:
            message = self.debug_info(message, node)
        print(message, file=sys.stderr)

    def dereference(self, value: Any) -> IdentifierOperator:
        if isinstance(value, IdentifierOperator):
            return value.get(self.table)
        else:
            return value

    def assert_true(self, message: str, truthy: Any, node: Node) -> None:
        if not truthy:
            self.fail(message=message, node=node, constructor=AssertionError)

    def print_str(self, value: str) -> None:
        # Replace escaped newline in string
        value = value.replace(r'\n', '\n')
        # Replace escaped tab in string
        value = value.replace(r'\t', '\t')
        print(value, file=self.stdout, end=str())

    def print(self, value: Any) -> None:
        if type(value) is int:
            self.print_str(str(value))
        elif type(value) is str:
            self.print_str(value)
        elif type(value) is list:
            for item in value:
                self.print(item)
        elif isinstance(value, IdentifierOperator):
            value = self.dereference(value)
            self.print(value)
        else:
            self.fail('cannot print unknown value type')

    def walk(self, node: Node) -> Any:
        # TODO: Convert to non-recursive
        if node is None:
            return
        elif node.type is NodeType.SEQUENCE:
            self.walk(node.right)
            self.walk(node.left)
        elif node.type is NodeType.BLOCK:
            self.table.scope_enter()
            self.walk(node.left)
            self.table.scope_exit()
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
            variable, _ = self.table.get(name)
            if variable.is_undefined:
                self.fail('variable {} referenced before assignment'.format(name), node)
            else:
                return variable.value
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
            value = self.dereference(value)
            if node.left.type is NodeType.IDENTIFIER_ARRAY:
                identifier_array = self.walk(node.left)
                identifier_array.set(self.table, value)
            elif node.left.type is NodeType.IDENTIFIER_MAP:
                identifier_map = self.walk(node.left)
                identifier_map.set(self.table, value)
            elif node.left.type is NodeType.IDENTIFIER:
                identifier = node.left.value
                if type(value) is int:
                    self.table.set(Variable(identifier, VariableType.INT, value))
                elif type(value) is str:
                    self.table.set(Variable(identifier, VariableType.STR, value))
                elif type(value) is list:
                    self.table.set(Variable(identifier, VariableType.ARRAY, value))
                elif type(value) is dict:
                    self.table.set(Variable(identifier, VariableType.MAP, value))
                else:
                    self.fail('unknown type - {}'.format(value), node)
            else:
                self.fail('cannot assign to unknown type')
            return value
        elif node.type in BINARY_OPERATORS:
            operation = BINARY_OPERATORS[node.type]
            left = self.walk(node.left)
            left = self.dereference(left)
            right = self.walk(node.right)
            right = self.dereference(right)
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
            print(character, file=self.stdout, end=str())
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
