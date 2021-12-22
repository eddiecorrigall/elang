from core.tokens import Comment, Identifier, Keyword, Literal, Mismatch, Operator, Symbol, Terminal, Token, TokenType, Whitespace
from core.errors import LexerSyntaxError

import re

from typing import Iterator, List


class Lexer:
    def get_regex_pair(self, token_type: TokenType) -> str:
        return '(?P<{label}>{pattern})'.format(
            label=token_type.label,
            pattern=token_type.pattern)

    def __init__(self):
        # Note: order matters for enum class and enum
        token_types: List[TokenType] = []
        token_types.extend(Comment)
        token_types.extend(Whitespace)
        token_types.extend(Operator)
        token_types.extend(Symbol)
        token_types.extend(Identifier)
        token_types.extend(Literal)
        token_types.extend(Mismatch)

        # Remove NEGATE
        # Turning some SUBTRACT into NEGATE is handled by syntax analyzer
        token_types.remove(Operator.NEGATE)

        self.tokens = token_types
        self.regex = '|'.join([self.get_regex_pair(token) for token in token_types])
        
        self.keyword_lookup = dict([
            (keyword.sequence, keyword)
            for keyword in Keyword])

    def parse_line(self, line: str, line_number: int) -> Iterator[Token]:
        character_offset = None
        for mo in re.finditer(self.regex, line):
            token_label = mo.lastgroup
            token_value = mo.group()
            character_offset = 1 + mo.start()
            if token_label.startswith('Whitespace') or token_label.startswith('Comment'):
                continue
            elif token_label == Literal.CHAR.label:
                if token_value == "'\\n'":
                    token_value = '10'
                elif token_value == "'\\\\'":
                    token_value = '92'
                elif len(token_value) == 3 and token_value not in ["'\n'", "'\\'"]:
                    token_value = str(ord(token_value[1]))
                else:
                    raise LexerSyntaxError(
                        'invalid character literal on line {} at character {} - <<<{}>>>'.format(
                            line_number, character_offset, line))
            elif token_label == Identifier.IDENTIFIER.label:
                if token_value in self.keyword_lookup:
                    # Identifier matches an existing keyword
                    token_label = self.keyword_lookup[token_value].label
                    token_value = None
            elif token_label.startswith('Operator') or token_label.startswith('Symbol'):
                token_value = None
            elif token_label.startswith('Mismatch'):
                raise LexerSyntaxError(
                    'syntax error on line {} at character {} - <<<{}>>>'.format(
                        line_number, character_offset, line))
            yield Token(line_number, character_offset, token_label, token_value)

    def __call__(self, program: str) -> Iterator[Token]:
        line_number = 1
        for line in program.split('\n'):
            for token in self.parse_line(line=line, line_number=line_number):
                yield token
            line_number += 1
        yield Token(line=line_number, offset=1, label=Terminal.TERMINAL.label, value=None)
