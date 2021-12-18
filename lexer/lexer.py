import re

from typing import List, NamedTuple
from lexer.errors import LexerSyntaxError
from lexer.tokens import Comment, Identifier, Keyword, Literal, Mismatch, Operator, Symbol, Token, Whitespace


class LexerOutput(NamedTuple):
    line: int
    offset: int
    label: str
    value: str


class Lexer:
    def getRegexPair(self, token: Token) -> str:
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
        self.regex = '|'.join([self.getRegexPair(token) for token in tokens])
        
        self.keyword_lookup = dict([
            (keyword.sequence, keyword)
            for keyword in Keyword])

    def __call__(self, line: str, line_number: int = 1) -> List[LexerOutput]:
        character_offset = 0
        for mo in re.finditer(self.regex, line):
            token_label = mo.lastgroup
            token_value = mo.group()
            character_offset = mo.start() - character_offset
            if token_label.startswith('Whitespace') or token_label.startswith('Comment'):
                continue
            elif token_label == Literal.CHAR.label:
                if token_value == "'\\n'":
                    token_value = '10'
                elif token_value == "'\\\\'":
                    token_value = '92'
                elif len(token_value) == 3:
                    if token_value in ["'\n'", "'\\'"]:
                        raise LexerSyntaxError(
                            'invalid character literal on line {} at character {} - <<<{}>>>'.format(
                                line_number, character_offset, line))
                    else:
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
            elif token_label.startswith('Op'):
                token_value = None
            elif token_label.startswith('Mismatch'):
                raise LexerSyntaxError(
                    'syntax error on line {} at character {} - <<<{}>>>'.format(
                        line_number, character_offset, line))
            yield LexerOutput(line_number, character_offset, token_label, token_value)
