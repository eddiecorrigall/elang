from enum import Enum
from typing import Dict, Tuple, Union


VariableType = Enum('VariableType', [
    'UNDEFINED',
    'INT',
    'STR',
    'ARRAY',
    'MAP',
])


class Variable:
    def __init__(
        self,
        name: str,
        type: VariableType,
        value: Union[int, str, list, dict],
    ) -> None:
        self.name = name
        self.type = type
        self.value = value
    
    @property
    def is_undefined(self):
        return self.type is VariableType.UNDEFINED

    def __repr__(self):
        return '<{class_name}[{type}] {name}={value}>'.format(
            class_name=self.__class__.__name__,
            type=self.type.name,
            name=self.name,
            value=self.value)

    def __eq__(self, other):
        return self.is_undefined or self.name == other.name


class Table:
    def __init__(self) -> None:
        self.scope_stack = list()
        self.scope_enter()  # Global scope
        self.variable_by_identifier: Dict[str, Variable] = dict()
    
    @property
    def scope(self):
        return len(self.scope_stack) - 1
    
    @property
    def scope_global(self):
        return 0

    def scope_exit(self):
        self.scope_stack.pop()
    
    def scope_enter(self):
        self.scope_stack.append(dict())

    def get(self, name: str) -> Tuple[Variable, int]:
        current_scope = self.scope
        while current_scope >= 0:
            scope_dict = self.scope_stack[current_scope]
            if name in scope_dict:
                variable = scope_dict[name]
                return variable, current_scope
            current_scope -= 1
        variable_undefined = Variable(
            name='undefined',
            type=VariableType.UNDEFINED,
            value=None)
        return variable_undefined, -1

    def set(self, variable: Variable) -> None:
        existing_variable, _ = self.get(variable.name)
        if existing_variable.is_undefined:
            # Define as new variable
            self.scope_stack[self.scope][variable.name] = variable
        else:
            if existing_variable.type is variable.type:
                # Update existing variable
                existing_variable.value = variable.value
            else:
                raise Exception('variable type mismatch')
