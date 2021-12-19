import re

from typing import Iterator, List, NamedTuple
from core.tokens import Comment, Identifier, Keyword, Literal, Mismatch, Operator, Symbol, Token, Whitespace
from lexer.errors import LexerSyntaxError


class LexerOutput(NamedTuple):
    line: int
    offset: int
    label: str
    value: str


class Lexer:
    def get_regex_pair(self, token: Token) -> str:
        return '(?P<{label}>{pattern})'.format(
            label=token.label,
            pattern=token.pattern)

    def __init__(self):
        # Note: order matters for enum class and enum
        tokens: List[Token] = []
        tokens.extend(Comment)
        tokens.extend(Whitespace)
        tokens.extend(Operator)
        tokens.extend(Symbol)
        tokens.extend(Identifier)
        tokens.extend(Literal)
        tokens.extend(Mismatch)

        # Remove NEGATE
        # Turning some SUBTRACT into NEGATE is handled by syntax analyzer
        tokens.remove(Operator.NEGATE)

        self.tokens = tokens
        self.regex = '|'.join([self.get_regex_pair(token) for token in tokens])
        
        self.keyword_lookup = dict([
            (keyword.sequence, keyword)
            for keyword in Keyword])

    def parse_line(self, line: str, line_number: int) -> Iterator[LexerOutput]:
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
            yield LexerOutput(line_number, character_offset, token_label, token_value)

    def __call__(self, program: str) -> Iterator[Token]:
        line_number = 1
        for line in program.split('\n'):
            for token in self.parse_line(line=line, line_number=line_number):
                yield token
            line_number += 1
        yield LexerOutput(line_number, 1, 'End_of_input', None)
