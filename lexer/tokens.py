from enum import Enum
from typing import Any


class Token(Enum):
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


class Literal(Token):
    INT = ('Literal_integer', r'([0-9]+)')
    CHAR = ('Literal_character', r"'([^'\n]|\\n|\\\\)'")
    STR = ('Literal_string', r'"([^"\n]*)"')


class Identifier(Token):
    IDENTIFIER = ('Identifier', r'([_a-zA-Z][_a-zA-Z0-9]*)')


class Operator(Token):
    MULTIPLY = ('Op_multiply', r'\*', '*')
    DIVIDE = ('Op_divide', r'/', '/')
    MOD = ('Op_mod', r'%', '%')
    ADD = ('Op_add', r'\+', '+')
    SUBTRACT = ('Op_subtract', r'\-', '-')
    NEGATE = ('Op_negate', r'\-', '-')
    LESS_OR_EQUAL = ('Op_lessequal', r'<=', '<=')
    LESS = ('Op_less', r'<', '<')
    GREATER_OR_EQUAL = ('Op_greaterequal', r'>=', '>=')
    GREATER = ('Op_greater', r'>', '>')
    EQUAL = ('Op_equal', r'==', '==')
    NOT_EQUAL = ('Op_notequal', r'!=', '!=')
    NOT = ('Op_not', r'!', '!')
    ASSIGN = ('Op_assign', r'=', '=')
    AND = ('Op_and', r'&&', '&&')
    OR = ('Op_or', r'\|\|', '||')


class Symbol(Token):
    LEFT_PARENTHESIS = ('LeftParen', r'\(', '(')
    RIGHT_PARENTHESIS = ('RightParen', r'\)', ')')
    LEFT_BRACE = ('LeftBrace', r'{', '{')
    RIGHT_BRACE = ('RightBrace', r'}', '}')
    SEMICOLON = ('Semicolon', r';', ';')
    COMMA = ('Comma', r',', ',')


class Keyword(Token):
    IF = ('Keyword_if', r'if', 'if')
    ELSE = ('Keyword_else', r'else', 'else')
    WHILE = ('Keyword_while', r'while', 'while')
    PRINT_CHARACTER = ('Keyword_putc', r'putc', 'putc')
    PRINT_STRING = ('Keyword_print', r'print', 'print')


class Whitespace(Token):
    NEWLINE = ('Whitespace_newline', r'\n', '\n')
    SPACE = ('Whitespace_space', r' ', ' ')
    TAB = ('Whitespace_tab', r'\t', '\t')


class Comment(Token):
    LINE = ('Comment_line', r'//(.*)')
    MULTILINE = ('Comment_multiline', r'/\*(.*)\*/')


class Mismatch(Token):
    MISMATCH = ('Mismatch',  r'.')
