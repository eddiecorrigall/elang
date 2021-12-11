
from collections import namedtuple
from typing import List
from lexer.errors import LexerNotImplemented, LexerSyntaxError
from lexer.tokens import CharacterLiteral, Identifier, IntegerLiteral, Keyword, Operator, Symbol, Token, TokenWithValue, Whitespace, ZeroWidth
from trie import Node, find, insert, insert_loop


LexerOutput = namedtuple('LexerOutput', ['line', 'offset', 'token', 'value'])


class Lexer:
    def __init__(self):
        self.root = Node()
        for operator in Operator:
            if operator == Operator.NEGATE:
                # Do not insert NEGATE
                # Turning some SUBTRACT into NEGATE is handled by syntax analyzer
                continue
            insert(self.root, operator.sequence, operator)
        for symbol in Symbol:
            insert(self.root, symbol.sequence, symbol)
        for keyword in Keyword:
            insert(self.root, keyword.sequence, keyword)
        for whitespace in Whitespace:
            insert(self.root, whitespace.sequence, whitespace)
        # Integer Literals
        for integer in range(0, 10):
            integer_str = str(integer)
            insert(self.root, integer_str, IntegerLiteral(integer_str))
        # Character Literals
        insert(self.root, "'\\n'", CharacterLiteral('10'))
        insert(self.root, "'\\\\'", CharacterLiteral('92'))

    def __call__(self, input: str) -> List[LexerOutput]:
        while input:
            node, sequence = find(self.root, input)
            # Jump passed the consumed sequence
            input = input[len(sequence):]
            if node is None:
                raise LexerSyntaxError('syntax error in "{}"'.format(input))
            token = node.value
            if isinstance(token, Whitespace):
                continue
            elif isinstance(token, (CharacterLiteral, IntegerLiteral, Identifier)):
                yield LexerOutput(0, 0, token, token.value)
            elif isinstance(token, (Operator, Symbol, Keyword, ZeroWidth)):
               yield LexerOutput(0, 0, token, None)
            else:
                raise LexerNotImplemented('sequence: {}, token: {}'.format(sequence, token))
