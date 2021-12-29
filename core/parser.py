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
    
    def __init__(self) -> None:
        self.tokens = None
        self.token = None

    def __call__(self, tokens: List[Token]) -> Node:
        self.tokens = (token for token in tokens)
        self.next_token()   # Consume first token
        return self.parse_sequence()

    def fail(self, message: str) -> None:
        raise Exception(' - ' .join([
            message,
            'label {}'.format(self.token_label),
            'value {}'.format(self.token_value),
            'line {}'.format(self.row),
            'character {}'.format(self.column),
        ]))

    def next_token(self) -> None:
        self.token = next(self.tokens)

    def accept(self, token: TokenType) -> bool:
        return self.token_label == token.label

    def expect(self, token: TokenType) -> str:
        if self.accept(token):
            value = self.token_value
            self.next_token()
            return value
        else:
            self.fail('expected token {}'.format(token.label))

    def make_leaf(self, type: NodeType, value: str) -> Node:
        return Node(type=type, value=value)

    def make_node(self, type: NodeType, left: Node, right: Optional[Node] = None) -> Node:
        return Node(type=type, left=left, right=right)

    def parse_identifier(self) -> Node:
        # Leaf
        name = self.expect(Identifier.IDENTIFIER)
        return self.make_leaf(NodeType.IDENTIFIER, name)

    def parse_integer(self) -> Node:
        # Leaf
        value = self.expect(Literal.INT)
        integer = self.make_leaf(NodeType.INT, value)
        return integer
    
    def parse_string(self) -> Node:
        # Leaf
        value = self.expect(Literal.STR)
        string = self.make_leaf(NodeType.STR, value)
        return string

    def parse_expression_binary(self):
        '''
        expression_binary = | ( "+" "-" "*" "/" "%" "<" | "<=" | ">" | ">=" )
                              expression
                              expression
                              ;
        '''
        if self.accept(Operator.ADD):
            type = NodeType.ADD
        elif self.accept(Operator.SUBTRACT):
            type = NodeType.SUBTRACT
        elif self.accept(Operator.MULTIPLY):
            type = NodeType.MULTIPLY
        elif self.accept(Operator.DIVIDE):
            type = NodeType.DIVIDE
        elif self.accept(Operator.MOD):
            type = NodeType.MOD
        elif self.accept(Operator.LESS):
            type = NodeType.LESS_THAN
        elif self.accept(Operator.EQUAL):
            type = NodeType.EQUAL
        elif self.accept(Operator.NOT_EQUAL):
            type = NodeType.NOT_EQUAL
        elif self.accept(Operator.LESS_OR_EQUAL):
            type = NodeType.LESS_THAN_OR_EQUAL
        elif self.accept(Operator.GREATER):
            type = NodeType.GREATER_THAN
        elif self.accept(Operator.GREATER_OR_EQUAL):
            type = NodeType.GREATER_THAN_OR_EQUAL
        else:
            # Unknown / unregistered
            self.fail('expected binary operator')
        self.next_token()  # Consume operator
        left_expression = self.parse_expression()
        right_expression = self.parse_expression()
        return self.make_node(type, left_expression, right_expression)

    def parse_expression_not(self) -> Node:
        '''
        expression_not = "!" expression ;
        '''
        self.expect(Operator.NOT)
        expression = self.parse_expression()
        return self.make_node(NodeType.NOT, expression)

    def parse_expression(self) -> Node:
        '''
        expression = expression_parenthesis
                   | integer
                   | string
                   | identifier
                   | expression_not
                   | expression_binary
                   ;
        '''
        if self.accept(Symbol.OPEN_PARENTHESIS):
            return self.parse_expression_parenthesis()
        elif self.accept(Literal.INT):
            return self.parse_integer()
        elif self.accept(Literal.STR):
            return self.parse_string()
        elif self.accept(Identifier.IDENTIFIER):
            return self.parse_identifier()
        elif self.accept(Operator.NOT):
            return self.parse_expression_not()
        else:
            return self.parse_expression_binary()
    
    def parse_expression_parenthesis(self) -> Node:
        '''
        expression_parenthesis = "(" expression ")" ;
        '''
        self.expect(Symbol.OPEN_PARENTHESIS)
        expression = self.parse_expression()
        self.expect(Symbol.CLOSE_PARENTHESIS)
        return expression

    def parse_assignment(self) -> Node:
        '''
        identifier "=" expression ";" ;
        '''
        identifier = self.parse_identifier()
        self.expect(Operator.ASSIGN)
        expression = self.parse_expression()
        assignment = self.make_node(NodeType.ASSIGN, identifier, expression)
        self.expect(Symbol.SEMICOLON)
        return assignment

    def parse_while(self) -> Node:
        '''
        while = "while" expression_parenthesis statement ;
        '''
        self.expect(Keyword.WHILE)
        expression_parenthesis = self.parse_expression_parenthesis()
        statement = self.parse_statement()
        return self.make_node(NodeType.WHILE, expression_parenthesis, statement)

    def parse_if(self) -> Node:
        '''
        if = "if" expression_parenthesis statement [ "else" statement ] ;
        '''
        self.expect(Keyword.IF)
        expression_parenthesis = self.parse_expression_parenthesis()
        if_statement = self.parse_statement()
        else_statement = None
        if self.accept(Keyword.ELSE):
            self.expect(Keyword.ELSE)
            else_statement = self.parse_statement()
        return self.make_node(
            NodeType.IF,
            expression_parenthesis,
            self.make_node(NodeType.IF, if_statement, else_statement))

    def parse_print_character(self) -> Node:
        '''
        print_character = "putc" expression_parenthesis ";" ;
        '''
        self.expect(Keyword.PRINT_CHARACTER)
        expression_parenthesis = self.parse_expression_parenthesis()
        print_character = self.make_node(NodeType.PRINT_CHARACTER, expression_parenthesis)
        self.expect(Symbol.SEMICOLON)
        return print_character
    
    def parse_print_string(self) -> Node:
        '''
        print_string = "print" expression_parenthesis ";" ;
        '''
        self.expect(Keyword.PRINT_STRING)
        expression_parenthesis = self.parse_expression_parenthesis()
        print_string = self.make_node(NodeType.PRINT_STRING, expression_parenthesis)
        self.expect(Symbol.SEMICOLON)
        return print_string

    def parse_block(self) -> None:
        '''
        block = "{" { statement } "}" ;
        '''
        self.expect(Symbol.OPEN_BRACE)
        sequence = None
        while not self.accept(Terminal.TERMINAL):
            if self.accept(Symbol.CLOSE_BRACE):
                break
            sequence = self.make_node(NodeType.SEQUENCE, self.parse_statement(), sequence)
        self.expect(Symbol.CLOSE_BRACE)
        return sequence

    def parse_statement(self) -> Node:
        '''
        statement = block
                  | assignment
                  | while
                  | if
                  | print_character
                  ;
        '''
        if self.accept(Symbol.OPEN_BRACE):
            return self.parse_block()
        elif self.accept(Identifier.IDENTIFIER):
            return self.parse_assignment()
        elif self.accept(Keyword.WHILE):
            return self.parse_while()
        elif self.accept(Keyword.IF):
            return self.parse_if()
        elif self.accept(Keyword.PRINT_CHARACTER):
            return self.parse_print_character()
        elif self.accept(Keyword.PRINT_STRING):
            return self.parse_print_string()
        else:
            self.fail('invalid statement')

    def parse_sequence(self) -> Node:
        '''
        sequence = ";" | { statement } ;
        '''
        sequence = None
        while not self.accept(Terminal.TERMINAL):
            if self.accept(Symbol.SEMICOLON):
                self.next_token()
                continue
            sequence = self.make_node(NodeType.SEQUENCE, self.parse_statement(), sequence)
        if sequence is None:
            sequence = self.make_node(NodeType.SEQUENCE, None)
        return sequence
