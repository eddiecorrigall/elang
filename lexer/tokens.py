from enum import Enum
from typing import Any

from lexer.errors import LexerNotImplemented


class Token:
    @property
    def label(self):
        return self.LABEL

    def __eq__(self, other):
        return self.label == other.label


class TokenWithValue(Token):
    @property
    def value(self) -> str:
        return self._value
    
    def __init__(self, value: str) -> None:
        super().__init__()
        self._value = value

    def __eq__(self, other):
        return (
            super().__eq__(other)
            and self.value == other.value)
   
    def __repr__(self) -> str:
        return '<{class_name}: {value}>'.format(
            class_name=self.__class__.__name__,
            value=self.value)


class IntegerLiteral(TokenWithValue):
    LABEL = 'Integer'


class CharacterLiteral(TokenWithValue):
    LABEL = 'Integer'


class Identifier(TokenWithValue):
    LABEL = 'Identifier'


class StaticToken(Token, Enum):
    def __new__(cls, label: str, sequence: str) -> Any:
        obj = object.__new__(cls)
        obj._value_ = dict(
            label=label,
            sequence=sequence,
        )
        return obj
    
    @property
    def label(self) -> str:
        return self.value['label']
    
    @property
    def sequence(self) -> str:
        return self.value['sequence']
    
    def __repr__(self) -> str:
        return '<{name}>'.format(name=self.name)


class Operator(StaticToken):
    MULTIPLY = ('Op_multiply', '*')
    DIVIDE = ('Op_divide', '/')
    MOD = ('Op_mod', '%')
    ADD = ('Op_add', '+')
    SUBTRACT = ('Op_subtract','-')
    NEGATE = ('Op_negate', '-')
    LESS = ('Op_less', '<')
    LESS_OR_EQUAL = ('Op_lessequal', '<=')
    GREATER = ('Op_greater', '>')
    GREATER_OR_EQUAL = ('Op_greaterequal', '>=')
    EQUAL = ('Op_equal', '==')
    NOT_EQUAL = ('Op_notequal', '!=')
    NOT = ('Op_not', '!')
    ASSIGN = ('Op_assign', '=')
    AND = ('Op_and', '&&')
    OR = ('Op_or', '¦¦')


class Symbol(StaticToken):
    LEFT_PARENTHESIS = ('LeftParen', '(')
    RIGHT_PARENTHESIS = ('RightParen', ')')
    LEFT_BRACE = ('LeftBrace', '{')
    RIGHT_BRACE = ('RightBrace', '}')
    SEMICOLON = ('Semicolon', ';')
    COMMA = ('Comma', ',')


class Keyword(StaticToken):
    IF = ('Keyword_if', 'if')
    ELSE = ('Keyword_else', 'else')
    WHILE = ('Keyword_while', 'while')
    PRINT_STRING = ('Keyword_print', 'print')
    PRINT_LINE_STRING = ('Keyword_print', 'println')
    PRINT_CHARACTER = ('Keyword_putc', 'putc')


class ZeroWidth(StaticToken):
    TERMINAL = ('End_of_input', None)


class Whitespace(StaticToken):
    NEWLINE = ('Whitespace_newline', '\n')
    SPACE = ('Whitespace_space', ' ')
    TAB = ('Whitespace_tab', '\t')
