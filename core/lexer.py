from core import readlines
from core.tokens import (
    KEYWORDS_BY_SEQUENCE, LITERAL_TOKEN_TYPES, OPERATOR_TOKEN_TYPES,
    SYMBOL_TOKEN_TYPES, WHITESPACE_TOKEN_TYPES, WHITESPACES_BY_NAME,
    Token, TokenType)
from core.errors import LexerSyntaxError

import re

from typing import Iterable, Iterator


class Lexer:
    def get_regex_pair(self, token_type: TokenType) -> str:
        return '(?P<{label}>{pattern})'.format(
            label=token_type.label,
            pattern=token_type.pattern)

    def __init__(self) -> None:
        # Note: order matters for enum class and enum
        match_token_types = []
        # Highest match priority
        match_token_types.append(TokenType.COMMENT_LINE)
        match_token_types.extend(WHITESPACE_TOKEN_TYPES)
        match_token_types.extend(OPERATOR_TOKEN_TYPES)
        match_token_types.extend(SYMBOL_TOKEN_TYPES)
        match_token_types.extend(LITERAL_TOKEN_TYPES)
        match_token_types.append(TokenType.IDENTIFIER)
        match_token_types.append(TokenType.MISMATCH)
        # Lowest match priority

        self.regex = '|'.join([
            self.get_regex_pair(token_type)
            for token_type in match_token_types
        ])

    def __call__(self, line: str) -> Iterator[Token]:
        return self.from_program_line(line, row=1)

    @classmethod
    def as_lines(cls, tokens: Iterable[Token]) -> Iterable[str]:
        for token in tokens:
            parts = [str(token.row), str(token.column), token.label]
            if token.value is not None:
                if token.label == TokenType.LITERAL_STR.label:
                    parts.append('"{}"'.format(token.value))
                else:
                    parts.append(token.value)
            yield '\t'.join(parts)

    @classmethod
    def from_token_file(cls, file: str) -> Iterable[Token]:
        # TODO: Handle string double quotes
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
        yield Token(row=row, column=1, label=TokenType.TERMINAL.label, value=None)

    def from_program_file(self, file) -> Iterable[Token]:
        return self.from_program_lines(readlines(file))

    def from_program_line(self, line: str, row: int) -> Iterator[Token]:
        for mo in re.finditer(self.regex, line):
            token_label = mo.lastgroup

            # Generically extract token value
            pair_groups = mo.groups()
            matched_groups = list(filter(None, pair_groups))
            if len(matched_groups) == 2:
                # Assuming 1 capture group per pair
                token_value = matched_groups[1]
            else:
                token_value = None

            column = 1 + mo.start()

            if token_label == TokenType.COMMENT_LINE.name:
                continue
            elif token_label in WHITESPACES_BY_NAME:
                continue
            elif token_label == TokenType.LITERAL_CHAR.name:
                if token_value == '\\n':
                    token_value = '10'
                elif token_value == '\\\\':
                    token_value = '92'
                elif len(token_value) == 1 and token_value not in ['\n', '\\']:
                    token_value = str(ord(token_value[0]))
                else:
                    raise LexerSyntaxError(
                        'invalid character literal on line {} at character {} - <<<{}>>>'.format(
                            row, column, line))
                token_label = TokenType.LITERAL_INT.name
            elif token_label == TokenType.IDENTIFIER.name:
                if token_value in KEYWORDS_BY_SEQUENCE:
                    # Identifier matches an existing keyword
                    token_label = KEYWORDS_BY_SEQUENCE[token_value].name
                    token_value = None
            elif token_label == TokenType.MISMATCH.name:
                raise LexerSyntaxError(
                    'syntax error on line {} at character {} - <<<{}>>>'.format(
                        row, column, line))
            yield Token(row=row, column=column, label=token_label, value=token_value)
