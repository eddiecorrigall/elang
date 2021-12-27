from core.ast import Node, NodeType
from core.tokens import Identifier, Keyword, Literal, Operator, Symbol, Terminal, Token, TokenType

from typing import List, Optional


class Parser:
    @property
    def row(self) -> int:
        return self.token and self.token.row
    
    @property
    def column(self) -> int:
        return self.token and self.token.column

    @property
    def token_value(self) -> str:
        return self.token and self.token.value
    
    @property
    def token_label(self) -> str:
        return self.token and self.token.label
    
    def __init__(self):
        self.tokens = None
        self.token = None

    def __call__(self, tokens: List[Token]):
        self.tokens = (token for token in tokens)
        self.token = None
        return self.make_sequence()

    def fail(self, message: str):
        raise Exception(' - ' .join([
            message,
            'label {}'.format(self.token_label),
            'value {}'.format(self.token_value),
            'line {}'.format(self.row),
            'character {}'.format(self.column),
        ]))

    def next_token(self) -> None:
        self.token = next(self.tokens)

    def accept(self, token: TokenType):
        return self.token_label == token.label

    def expect(self, token: TokenType) -> str:
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
        # Leaf
        name = self.expect(Identifier.IDENTIFIER)
        return self.make_leaf(NodeType.IDENTIFIER, name)

    def make_integer(self):
        # Leaf
        value = self.expect(Literal.INT)
        integer = self.make_leaf(NodeType.INT, value)
        return integer

    def make_expression(self):
        # Simplified
        if self.accept(Identifier.IDENTIFIER):
            return self.make_identifier()
        if self.accept(Literal.INT):
            return self.make_integer()
        if self.accept(Symbol.OPEN_PARENTHESIS):
            return self.make_expression_parenthesis()
        self.fail('invalid expression')
    
    def make_expression_parenthesis(self):
        '''
        "(" expression ")"
        '''
        self.expect(Symbol.OPEN_PARENTHESIS)
        expression = self.make_expression()
        self.expect(Symbol.CLOSE_PARENTHESIS)
        return expression

    def make_assignment(self):
        '''
        identifier "=" expression ";"
        '''
        identifier = self.make_identifier()
        self.expect(Operator.ASSIGN)
        expression = self.make_expression()
        assignment = self.make_node(NodeType.ASSIGN, identifier, expression)
        self.expect(Symbol.SEMICOLON)
        return assignment
    
    def make_print_character(self):
        '''
        "putc" expression_parenthesis ";"
        '''
        self.expect(Keyword.PRINT_CHARACTER)
        expression_parenthesis = self.make_expression_parenthesis()
        print_character = self.make_node(NodeType.PRINT_CHARACTER, expression_parenthesis)
        self.expect(Symbol.SEMICOLON)
        return print_character

    def make_statement(self):
        '''
        statement = ";"
                  | assignment
                  | print_character
        '''
        if self.accept(Symbol.SEMICOLON):
            return self.make_sequence()
        if self.accept(Identifier.IDENTIFIER):
            return self.make_assignment()
        if self.accept(Keyword.PRINT_CHARACTER):
            return self.make_print_character()
        self.fail('invalid statement')

    def make_sequence(self):
        '''
        sequence = { statement }
        '''
        sequence = None
        self.next_token()
        while not self.accept(Terminal.TERMINAL):
            sequence = self.make_node(NodeType.SEQUENCE, self.make_statement(), sequence)
        return sequence
