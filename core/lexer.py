from core import readlines
from core.tokens import Comment, Identifier, Keyword, Literal, Mismatch, Operator, Symbol, Terminal, Token, TokenType, Whitespace
from core.errors import LexerSyntaxError

import re

from typing import Iterable, Iterator, List


class Lexer:
    def get_regex_pair(self, token_type: TokenType) -> str:
        return '(?P<{label}>{pattern})'.format(
            label=token_type.label,
            pattern=token_type.pattern)

    def __init__(self) -> None:
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

    def __call__(self, line: str) -> Iterator[Token]:
        return self.from_program_line(line, row=1)

    @classmethod
    def as_lines(cls, tokens: Iterable[Token]) -> Iterable[str]:
        for token in tokens:
            parts = [str(token.row), str(token.column), token.label]
            if token.value is not None:
                parts.append(token.value)
            yield '\t'.join(parts)

    @classmethod
    def from_token_file(cls, file: str) -> Iterable[Token]:
        for line in readlines(file):
            line_parts = line.split('\t')
            value = None
            if len(line_parts) == 3:
                row, column, label = line_parts
            elif len(line_parts) == 4:
                row, column, label, value = line_parts
            else:
                raise Exception('unexpected file format')
            yield Token(
                row=int(row), column=int(column), label=label, value=value)

    def from_program_lines(self, lines: Iterable[str]) -> Iterable[Token]:
        row = 1
        for line in lines:
            for token in self.from_program_line(line=line, row=row):
                yield token
            row += 1
        yield Token(row=row, column=1, label=Terminal.TERMINAL.label, value=None)

    def from_program_file(self, file) -> Iterable[Token]:
        return self.from_program_lines(readlines(file))

    def from_program_line(self, line: str, row: int) -> Iterator[Token]:
        column = None
        for mo in re.finditer(self.regex, line):
            token_label = mo.lastgroup
            token_value = mo.group()
            column = 1 + mo.start()
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
                            row, column, line))
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
                        row, column, line))
            yield Token(row=row, column=column, label=token_label, value=token_value)
