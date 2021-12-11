from enum import Enum
from typing import Any


class Token(Enum):
    def __new__(cls, label: str, sequence: str) -> Any:
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        obj.sequence = sequence
        return obj
    
    def __repr__(self):
        if self.sequence is None:
            return '<{}>'.format(self.label)
        else:
            return '<{}: [{}]>'.format(self.label, self.sequence)


class Literal(Token):
    INT = ('Integer', None)
    CHAR = ('Integer', None)


class Identifier(Token):
    IDENTIFIER = ('Identifier', None)


class Operator(Token):
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


class Symbol(Token):
    LEFT_PARENTHESIS = ('LeftParen', '(')
    RIGHT_PARENTHESIS = ('RightParen', ')')
    LEFT_BRACE = ('LeftBrace', '{')
    RIGHT_BRACE = ('RightBrace', '}')
    SEMICOLON = ('Semicolon', ';')
    COMMA = ('Comma', ',')


class Keyword(Token):
    IF = ('Keyword_if', 'if')
    ELSE = ('Keyword_else', 'else')
    WHILE = ('Keyword_while', 'while')
    PRINT_STRING = ('Keyword_print', 'print')
    PRINT_LINE_STRING = ('Keyword_print', 'println')
    PRINT_CHARACTER = ('Keyword_putc', 'putc')


class ZeroWidth(Token):
    TERMINAL = ('End_of_input', None)


class Whitespace(Token):
    NEWLINE = ('Whitespace_newline', '\n')
    SPACE = ('Whitespace_space', ' ')
    TAB = ('Whitespace_tab', '\t')
