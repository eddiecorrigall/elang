
from collections import namedtuple
from typing import List
from lexer.errors import LexerNotImplemented, LexerSyntaxError
from lexer.tokens import Identifier, Keyword, Literal, Operator, Symbol, Whitespace, ZeroWidth
from trie import find, insert
from trie.node import Node


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
            integer_node = insert(self.root, integer_str, Literal.INT)
            for next_integer in range(0, 10):
                integer_node.set_next(str(next_integer), integer_node)
        # Character Literals
        insert(self.root, "'\\n'", Literal.CHAR)
        insert(self.root, "'\\\\'", Literal.CHAR)

    def __call__(self, line: str, line_number: int = 1) -> List[LexerOutput]:
        character_offset = 0
        while line:
            node, sequence = find(self.root, line)
            # Jump passed the consumed sequence
            sequence_length = len(sequence)
            line = line[sequence_length:]
            if node is None:
                raise LexerSyntaxError('syntax error in "{}"'.format(line))
            token = node.value
            if isinstance(token, Whitespace):
                pass
            elif token == Literal.CHAR:
                value_char = sequence[1:-1]  # Remove single quotes
                if value_char == '\\n':
                    yield LexerOutput(line_number, character_offset, token, '10')
                elif value_char == '\\\\':
                    yield LexerOutput(line_number, character_offset, token, '92')
                else:
                    if len(value_char) != 1:
                        raise LexerSyntaxError('invalid char {}'.format(sequence))
                    value_int = ord(value_char)
                    yield LexerOutput(line_number, 0, token, str(value_int))
            elif isinstance(token, (Literal, Identifier)):
                yield LexerOutput(line_number, character_offset, token, sequence)
            elif isinstance(token, (Operator, Symbol, Keyword, ZeroWidth)):
               yield LexerOutput(line_number, character_offset, token, None)
            else:
                raise LexerNotImplemented('sequence: {}, token: {}'.format(sequence, token))
            character_offset += sequence_length
