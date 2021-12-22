from enum import Enum
from typing import Any, NamedTuple


class Token(NamedTuple):
    line: int
    offset: int
    label: str
    value: str


class TokenType(Enum):
    def __new__(cls, label: str, pattern: str, sequence: str=None) -> Any:
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        obj.pattern = pattern
        obj.sequence = sequence
        return obj

    def __repr__(self):
        if self.pattern is None:
            return '<{}>'.format(self.label)
        else:
            return '<{}: [{}]>'.format(self.label, self.pattern)


class Literal(TokenType):
    INT = ('Literal_integer', r'([0-9]+)(?![a-zA-Z])')
    CHAR = ('Literal_character', r"'([^'\n]|\\n|\\\\)'")
    STR = ('Literal_string', r'"([^"\n]*)"')


class Identifier(TokenType):
    IDENTIFIER = ('Identifier', r'([_a-zA-Z][_a-zA-Z0-9]*)')


class Operator(TokenType):
    MULTIPLY = ('Operator_multiply', r'\*', '*')
    DIVIDE = ('Operator_divide', r'/', '/')
    MOD = ('Operator_mod', r'%', '%')
    ADD = ('Operator_add', r'\+', '+')
    SUBTRACT = ('Operator_subtract', r'\-', '-')
    NEGATE = ('Operator_negate', r'\-', '-')
    LESS_OR_EQUAL = ('Operator_lessequal', r'<=', '<=')
    LESS = ('Operator_less', r'<', '<')
    GREATER_OR_EQUAL = ('Operator_greaterequal', r'>=', '>=')
    GREATER = ('Operator_greater', r'>', '>')
    EQUAL = ('Operator_equal', r'==', '==')
    NOT_EQUAL = ('Operator_notequal', r'!=', '!=')
    NOT = ('Operator_not', r'!', '!')
    ASSIGN = ('Operator_assign', r'=', '=')
    AND = ('Operator_and', r'&&', '&&')
    OR = ('Operator_or', r'\|\|', '||')


class Symbol(TokenType):
    OPEN_PARENTHESIS = ('Symbol_openparenthesis', r'\(', '(')
    CLOSE_PARENTHESIS = ('Symbol_closeparenthesis', r'\)', ')')
    OPEN_BRACE = ('Symbol_openbrace', r'{', '{')
    CLOSE_BRACE = ('Symbol_closebrace', r'}', '}')
    SEMICOLON = ('Symbol_semicolon', r';', ';')
    COMMA = ('Symbol_comma', r',', ',')


class Keyword(TokenType):
    IF = ('Keyword_if', r'if', 'if')
    ELSE = ('Keyword_else', r'else', 'else')
    WHILE = ('Keyword_while', r'while', 'while')
    PRINT_CHARACTER = ('Keyword_putc', r'putc', 'putc')
    PRINT_STRING = ('Keyword_print', r'print', 'print')


class Whitespace(TokenType):
    NEWLINE = ('Whitespace_newline', r'\n', '\n')
    SPACE = ('Whitespace_space', r' ', ' ')
    TAB = ('Whitespace_tab', r'\t', '\t')


class Comment(TokenType):
    LINE = ('Comment_line', r'//(.*)')


class Mismatch(TokenType):
    MISMATCH = ('Mismatch',  r'.')


class Terminal(TokenType):
    TERMINAL = ('Terminal', None)
