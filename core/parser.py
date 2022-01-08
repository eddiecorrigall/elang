from core.ast import Node, NodeType
from core.tokens import Token, TokenType

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
        return self.token and self.token.name
    
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
        return self.token_label == token.name

    def expect(self, token: TokenType) -> str:
        if self.accept(token):
            value = self.token_value
            self.next_token()
            return value
        else:
            self.fail('expected token {}'.format(token.name))

    def make_leaf(self, type: NodeType, value: str) -> Node:
        return Node(type=type, value=value)

    def make_node(self, type: NodeType, left: Node, right: Optional[Node] = None) -> Node:
        return Node(type=type, left=left, right=right)

    def parse_identifier(self) -> Node:
        # Leaf
        name = self.expect(TokenType.IDENTIFIER)
        return self.make_leaf(NodeType.IDENTIFIER, name)

    def parse_integer(self) -> Node:
        # Leaf
        value = self.expect(TokenType.LITERAL_INT)
        integer = self.make_leaf(NodeType.INT, value)
        return integer
    
    def parse_string(self) -> Node:
        # Leaf
        value = self.expect(TokenType.LITERAL_STR)
        string = self.make_leaf(NodeType.STR, value)
        return string

    def parse_array(self) -> Node:
        '''
        array = "[" { expression "," } "]" ";" ;
        '''
        self.expect(TokenType.SYMBOL_OPEN_SQUARE_BRACKET)
        array = None
        while not self.accept(TokenType.TERMINAL):
            if self.accept(TokenType.SYMBOL_CLOSE_SQUARE_BRACKET):
                break
            expression = self.parse_expression()
            self.expect(TokenType.SYMBOL_COMMA)
            array = self.make_node(NodeType.ARRAY, expression, array)
        self.expect(TokenType.SYMBOL_CLOSE_SQUARE_BRACKET)
        return array

    def parse_expression_binary(self):
        '''
        expression_binary = | ( "+" | "-" | "*" | "/" | "%" | "<" | "<=" | ">" | ">=" | "and" | "or" )
                              expression
                              expression
                              ;
        '''
        if self.accept(TokenType.OPERATOR_ADD):
            type = NodeType.ADD
        elif self.accept(TokenType.OPERATOR_SUBTRACT):
            type = NodeType.SUBTRACT
        elif self.accept(TokenType.OPERATOR_MULTIPLY):
            type = NodeType.MULTIPLY
        elif self.accept(TokenType.OPERATOR_DIVIDE):
            type = NodeType.DIVIDE
        elif self.accept(TokenType.OPERATOR_MOD):
            type = NodeType.MOD
        elif self.accept(TokenType.OPERATOR_LESS):
            type = NodeType.LESS_THAN
        elif self.accept(TokenType.OPERATOR_EQUAL):
            type = NodeType.EQUAL
        elif self.accept(TokenType.OPERATOR_NOT_EQUAL):
            type = NodeType.NOT_EQUAL
        elif self.accept(TokenType.OPERATOR_LESS_OR_EQUAL):
            type = NodeType.LESS_THAN_OR_EQUAL
        elif self.accept(TokenType.OPERATOR_GREATER):
            type = NodeType.GREATER_THAN
        elif self.accept(TokenType.OPERATOR_GREATER_OR_EQUAL):
            type = NodeType.GREATER_THAN_OR_EQUAL
        elif self.accept(TokenType.OPERATOR_AND):
            type = NodeType.AND
        elif self.accept(TokenType.OPERATOR_OR):
            type = NodeType.OR
        else:
            # Unknown / unregistered
            self.fail('unknown operator')
        self.next_token()  # Consume operator
        left_expression = self.parse_expression()
        right_expression = self.parse_expression()
        return self.make_node(type, left_expression, right_expression)

    def parse_expression_not(self) -> Node:
        '''
        expression_not = "not" expression ;
        '''
        self.expect(TokenType.OPERATOR_NOT)
        expression = self.parse_expression()
        return self.make_node(NodeType.NOT, expression)

    def parse_identifier_operator(self) -> Node:
        '''
        identifier_operator = identifier (
            { "@" expression } |
            { "#" expression }
        ) ;
        '''
        identifier = self.parse_identifier()
        while not self.accept(TokenType.TERMINAL):
            if not self.accept(TokenType.OPERATOR_AT):
                break
            self.next_token()  # Consume operator
            index = self.parse_expression()
            identifier = self.make_node(NodeType.IDENTIFIER_ARRAY, identifier, index)
        while not self.accept(TokenType.TERMINAL):
            if not self.accept(TokenType.OPERATOR_HASH):
                break
            self.next_token()  # Consume operator
            index = self.parse_expression()
            identifier = self.make_node(NodeType.IDENTIFIER_MAP, identifier, index)
        return identifier

    def parse_expression(self) -> Node:
        '''
        expression = expression_parenthesis
                   | integer
                   | string
                   | identifier_operator
                   | array
                   | expression_not
                   | expression_binary
                   ;
        '''
        if self.accept(TokenType.SYMBOL_OPEN_PARENTHESIS):
            return self.parse_expression_parenthesis()
        elif self.accept(TokenType.LITERAL_INT):
            return self.parse_integer()
        elif self.accept(TokenType.LITERAL_STR):
            return self.parse_string()
        elif self.accept(TokenType.IDENTIFIER):
            return self.parse_identifier_operator()
        elif self.accept(TokenType.SYMBOL_OPEN_SQUARE_BRACKET):
            return self.parse_array()
        elif self.accept(TokenType.OPERATOR_NOT):
            return self.parse_expression_not()
        else:
            return self.parse_expression_binary()
    
    def parse_expression_parenthesis(self) -> Node:
        '''
        expression_parenthesis = "(" expression ")" ;
        '''
        self.expect(TokenType.SYMBOL_OPEN_PARENTHESIS)
        expression = self.parse_expression()
        self.expect(TokenType.SYMBOL_CLOSE_PARENTHESIS)
        return expression

    def parse_assignment(self) -> Node:
        '''
        assignment = identifier "=" expression ";" ;
        '''
        identifier = self.parse_identifier_operator()
        self.expect(TokenType.OPERATOR_ASSIGN)
        expression = self.parse_expression()
        assignment = self.make_node(NodeType.ASSIGN, identifier, expression)
        self.expect(TokenType.SYMBOL_SEMICOLON)
        return assignment

    def parse_while(self) -> Node:
        '''
        while = "while" expression_parenthesis keyword_block ;
        '''
        self.expect(TokenType.KEYWORD_WHILE)
        expression_parenthesis = self.parse_expression_parenthesis()
        block = self.parse_keyword_block()
        return self.make_node(NodeType.WHILE, expression_parenthesis, block)

    def parse_if(self) -> Node:
        '''
        if = "if" expression_parenthesis keyword_block [ "else" keyword_block ] ;
        '''
        self.expect(TokenType.KEYWORD_IF)
        expression_parenthesis = self.parse_expression_parenthesis()
        if_block = self.parse_keyword_block()
        else_block = None
        if self.accept(TokenType.KEYWORD_ELSE):
            self.expect(TokenType.KEYWORD_ELSE)
            else_block = self.parse_keyword_block()
        return self.make_node(
            NodeType.IF,
            expression_parenthesis,
            self.make_node(NodeType.IF, if_block, else_block))

    def parse_print_character(self) -> Node:
        '''
        print_character = "putc" expression_parenthesis ";" ;
        '''
        self.expect(TokenType.KEYWORD_PRINT_CHARACTER)
        expression_parenthesis = self.parse_expression_parenthesis()
        print_character = self.make_node(NodeType.PRINT_CHARACTER, expression_parenthesis)
        self.expect(TokenType.SYMBOL_SEMICOLON)
        return print_character

    def parse_print_string(self) -> Node:
        '''
        print_string = "print" expression_parenthesis ";" ;
        '''
        self.expect(TokenType.KEYWORD_PRINT_STRING)
        expression_parenthesis = self.parse_expression_parenthesis()
        print_string = self.make_node(NodeType.PRINT_STRING, expression_parenthesis)
        self.expect(TokenType.SYMBOL_SEMICOLON)
        return print_string

    def parse_assert(self) -> Node:
        '''
        assert = "assert" expression_parenthesis ";" ;
        '''
        self.expect(TokenType.KEYWORD_ASSERT)
        expression_parenthesis = self.parse_expression_parenthesis()
        _assert = self.make_node(NodeType.ASSERT, expression_parenthesis)
        self.expect(TokenType.SYMBOL_SEMICOLON)
        return _assert

    def parse_block(self) -> Node:
        '''
        block = "{" { statement } "}" ;
        '''
        self.expect(TokenType.SYMBOL_OPEN_BRACE)
        sequence = None
        while not self.accept(TokenType.TERMINAL):
            if self.accept(TokenType.SYMBOL_CLOSE_BRACE):
                break
            sequence = self.make_node(NodeType.SEQUENCE, self.parse_statement(), sequence)
        self.expect(TokenType.SYMBOL_CLOSE_BRACE)
        return self.make_node(NodeType.BLOCK, sequence)

    def parse_keyword_block(self) -> Node:
        '''
        keyword_block = block | statement ;
        '''
        if self.accept(TokenType.SYMBOL_OPEN_BRACE):
            return self.parse_block()
        else:
            return self.make_node(NodeType.BLOCK, self.parse_statement())

    def parse_statement(self) -> Node:
        '''
        statement = block
                  | assignment
                  | while
                  | if
                  | print_character
                  | print_string
                  | assert
                  ;
        '''
        if self.accept(TokenType.SYMBOL_OPEN_BRACE):
            return self.parse_block()
        elif self.accept(TokenType.IDENTIFIER):
            return self.parse_assignment()
        elif self.accept(TokenType.KEYWORD_WHILE):
            return self.parse_while()
        elif self.accept(TokenType.KEYWORD_IF):
            return self.parse_if()
        elif self.accept(TokenType.KEYWORD_PRINT_CHARACTER):
            return self.parse_print_character()
        elif self.accept(TokenType.KEYWORD_PRINT_STRING):
            return self.parse_print_string()
        elif self.accept(TokenType.KEYWORD_ASSERT):
            return self.parse_assert()
        else:
            self.fail('invalid statement')

    def parse_sequence(self) -> Node:
        '''
        sequence = ";" | { statement } ;
        '''
        sequence = None
        while not self.accept(TokenType.TERMINAL):
            if self.accept(TokenType.SYMBOL_SEMICOLON):
                self.next_token()
                continue
            sequence = self.make_node(NodeType.SEQUENCE, self.parse_statement(), sequence)
        if sequence is None:
            sequence = self.make_node(NodeType.SEQUENCE, None)
        return sequence
