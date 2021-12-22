from core.ast import Node, NodeType
from core.tokens import Identifier, Literal, Operator, Symbol, Terminal, Token
from lexer.lexer import LexerOutput

from typing import List, Optional


class Parser:
    @property
    def line(self) -> int:
        return self.token and self.token.line
    
    @property
    def offset(self) -> int:
        return self.token and self.token.offset

    @property
    def token_value(self) -> str:
        return self.token and self.token.value
    
    @property
    def token_label(self) -> str:
        return self.token and self.token.label
    
    def __init__(self):
        self.tokens = None
        self.token = None

    def __call__(self, tokens: List[LexerOutput]):
        self.tokens = (token for token in tokens)
        self.token = None
        return self.make_sequence()

    def fail(self, message: str):
        raise Exception(' - ' .join([
            message,
            'label {}'.format(self.token_label),
            'value {}'.format(self.token_value),
            'line {}'.format(self.line),
            'offset {}'.format(self.offset),
        ]))

    def next_token(self) -> None:
        self.token = next(self.tokens)

    def accept(self, token: Token):
        return self.token_label == token.label

    def expect(self, token: Token) -> str:
        if self.accept(token):
            value = self.token_value
            self.next_token()
            return value
        else:
            self.fail('expected token {}'.format(token.label))

    def make_leaf(self, type: NodeType, value: str):
        return Node(type=type, value=value)

    def make_node(self, type: NodeType, left: Node, right: Optional[Node] = None):
        return Node(type=type, left=left, right=right)

    def make_identifier(self):
        name = self.expect(Identifier.IDENTIFIER)
        return self.make_leaf(NodeType.IDENTIFIER, name)

    def make_integer(self):
        value = self.expect(Literal.INT)
        integer = self.make_leaf(NodeType.INT, value)
        return integer

    def make_expression(self):
        if self.accept(Identifier.IDENTIFIER):
            return self.make_identifier()
        if self.accept(Literal.INT):
            return self.make_integer()
        self.fail('invalid expression')

    def make_assignment(self):
        identifier = self.make_identifier()
        self.expect(Operator.ASSIGN)
        expression = self.make_expression()
        assignment = self.make_node(NodeType.ASSIGN, identifier, expression)
        self.expect(Symbol.SEMICOLON)
        return assignment

    def make_statement(self):
        if self.accept(Identifier.IDENTIFIER):
            return self.make_assignment()
        self.fail('invalid statement')

    def make_sequence(self):
        # statement list
        sequence = None
        self.next_token()
        while not self.accept(Terminal.TERMINAL):
            sequence = self.make_node(NodeType.SEQUENCE, self.make_statement(), sequence)
        return sequence
