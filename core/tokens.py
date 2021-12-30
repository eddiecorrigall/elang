from enum import Enum
from typing import Any, Dict, Iterable, NamedTuple


class Token(NamedTuple):
    row: int
    column: int
    label: str
    value: str


class TokenType(Enum):
    def __new__(cls, pattern: str, sequence: str=None) -> Any:
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        obj.pattern = pattern
        obj.sequence = sequence
        return obj

    def __repr__(self):
        if self.pattern is None:
            return '<{}>'.format(self.label)
        else:
            return '<{}: [{}]>'.format(self.label, self.pattern)
    
    @property
    def label(self):
        return self.name

    LITERAL_INT = r'([0-9]+)(?![a-zA-Z])'
    LITERAL_CHAR = r"'([^'\n]|\\n|\\\\)'"
    LITERAL_STR = r'"([^"\n]*)"'

    IDENTIFIER = r'([_a-zA-Z][_a-zA-Z0-9]*)'
    
    OPERATOR_MULTIPLY = (r'\*', '*')
    OPERATOR_DIVIDE = (r'/', '/')
    OPERATOR_MOD = (r'%', '%')
    OPERATOR_ADD = (r'\+', '+')
    OPERATOR_SUBTRACT = (r'\-', '-')
    OPERATOR_LESS_OR_EQUAL = (r'<=', '<=')
    OPERATOR_LESS = (r'<', '<')
    OPERATOR_GREATER_OR_EQUAL = (r'>=', '>=')
    OPERATOR_GREATER = (r'>', '>')
    OPERATOR_EQUAL = (r'==', '==')
    OPERATOR_NOT_EQUAL = (r'!=', '!=')
    OPERATOR_NOT = (r'!', '!')
    OPERATOR_ASSIGN = (r'=', '=')
    OPERATOR_AND = (r'&&', '&&')
    OPERATOR_OR = (r'\|\|', '||')
    
    SYMBOL_OPEN_PARENTHESIS = (r'\(', '(')
    SYMBOL_CLOSE_PARENTHESIS = (r'\)', ')')
    SYMBOL_OPEN_BRACE = (r'{', '{')
    SYMBOL_CLOSE_BRACE = (r'}', '}')
    SYMBOL_SEMICOLON = (r';', ';')
    SYMBOL_COMMA = (r',', ',')

    KEYWORD_IF = (r'if', 'if')
    KEYWORD_ELSE = (r'else', 'else')
    KEYWORD_WHILE = (r'while', 'while')
    KEYWORD_PRINT_CHARACTER = (r'putc', 'putc')
    KEYWORD_PRINT_STRING = (r'print', 'print')

    WHITESPACE_NEWLINE = (r'\n', '\n')
    WHITESPACE_SPACE = (r' ', ' ')
    WHITESPACE_TAB = (r'\t', '\t')

    COMMENT_LINE = r'//(.*)'
    
    MISMATCH = r'.'
    
    TERMINAL = None


def get_token_type_by_prefix(prefix: str) -> Iterable[TokenType]:
    # Note: Preserve order
    return list([
        token_type
        for token_type in TokenType
        if token_type.name.startswith(prefix)
    ])

LITERAL_TOKEN_TYPES = get_token_type_by_prefix('LITERAL_')
OPERATOR_TOKEN_TYPES = get_token_type_by_prefix('OPERATOR_')
SYMBOL_TOKEN_TYPES = get_token_type_by_prefix('SYMBOL_')
KEYWORD_TOKEN_TYPES = get_token_type_by_prefix('KEYWORD_')
WHITESPACE_TOKEN_TYPES = get_token_type_by_prefix('WHITESPACE_')

def get_token_type_by_name(token_types: Iterable[TokenType]) -> Dict[str, TokenType]:
    return dict([
        (token_type.name, token_type)
        for token_type in token_types
    ])

WHITESPACES_BY_NAME = get_token_type_by_name(WHITESPACE_TOKEN_TYPES)

def get_token_type_by_sequence(token_types: Iterable[TokenType]) -> Dict[str, TokenType]:
    return dict([
        (token_type.sequence, token_type)
        for token_type in token_types
        if token_type.sequence
    ])

KEYWORDS_BY_SEQUENCE = get_token_type_by_sequence(KEYWORD_TOKEN_TYPES)
