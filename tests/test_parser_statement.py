from core.ast import Node, NodeType
from core.tokens import Token, TokenType
from tests.parser_test_base import ParserTestBase


class TestParserStatementSemicolon(ParserTestBase):
    def test_semicolon(self):
        self.givenTokens([
            Token(1, 1, TokenType.SYMBOL_SEMICOLON.label, None),
            Token(2, 1, TokenType.TERMINAL.label, None),
        ])
        self.whenParse()
        self.thenReturnNode(Node(
            type=NodeType.SEQUENCE,
        ))
    
    def test_semicolon_as_lines(self):
        self.givenNode(Node(
            type=NodeType.SEQUENCE,
        ))
        self.whenNodeAsLines()
        self.thenReturnLines([
            NodeType.SEQUENCE.name,
            ';',
            ';',
        ])


class TestParserStatementAssignment(ParserTestBase):
    def test_assign_literal_integer(self):
        self.givenTokens([
            Token(1, 1, TokenType.IDENTIFIER.label, 'abc'),
            Token(1, 5, TokenType.OPERATOR_ASSIGN.label, None),
            Token(1, 7, TokenType.LITERAL_INT.label, '123'),
            Token(1, 10, TokenType.SYMBOL_SEMICOLON.label, None),
            Token(2, 1, TokenType.TERMINAL.label, None),
        ])
        self.whenParse()
        self.thenReturnNode(Node(
            type=NodeType.SEQUENCE,
            left=Node(
                type=NodeType.ASSIGN,
                left=Node(
                    type=NodeType.IDENTIFIER,
                    value='abc',
                ),
                right=Node(
                    type=NodeType.INT,
                    value='123',
                ),
            ),
        ))

    def test_assign_identifier(self):
        self.givenTokens([
            Token(1, 1, TokenType.IDENTIFIER.label, 'abc'),
            Token(1, 5, TokenType.OPERATOR_ASSIGN.label, None),
            Token(1, 7, TokenType.IDENTIFIER.label, 'xyz'),
            Token(1, 10, TokenType.SYMBOL_SEMICOLON.label, None),
            Token(2, 1, TokenType.TERMINAL.label, None),
        ])
        self.whenParse()
        self.thenReturnNode(Node(
            type=NodeType.SEQUENCE,
            left=Node(
                type=NodeType.ASSIGN,
                left=Node(
                    type=NodeType.IDENTIFIER,
                    value='abc',
                ),
                right=Node(
                    type=NodeType.IDENTIFIER,
                    value='xyz',
                ),
            ),
        ))


class TestParserStatementPrintCharacter(ParserTestBase):
    def test_print_character_integer(self):
        self.givenTokens([
            Token(1, 1, TokenType.KEYWORD_PRINT_CHARACTER.label, None),
            Token(1, 5, TokenType.SYMBOL_OPEN_PARENTHESIS.label, None),
            Token(1, 6, TokenType.LITERAL_INT.label, '123'),
            Token(1, 9, TokenType.SYMBOL_CLOSE_PARENTHESIS.label, None),
            Token(1, 10, TokenType.SYMBOL_SEMICOLON.label, None),
            Token(2, 1, TokenType.TERMINAL.label, None),
        ])
        self.whenParse()
        self.thenReturnNode(Node(
            type=NodeType.SEQUENCE,
            left=Node(
                type=NodeType.PRINT_CHARACTER,
                left=Node(
                    type=NodeType.INT,
                    value='123',
                ),
            ),
        ))

    def test_print_character_integer_as_lines(self):
        self.givenNode(Node(
            type=NodeType.SEQUENCE,
            left=Node(
                type=NodeType.PRINT_CHARACTER,
                left=Node(
                    type=NodeType.INT,
                    value='123',
                ),
            ),
        ))
        self.whenNodeAsLines()
        self.thenReturnLines([
            NodeType.SEQUENCE.name,
            NodeType.PRINT_CHARACTER.name,
            NodeType.INT.name + '\t' + '123',
            ';',
            ';',
        ])


class TestParserStatementIf(ParserTestBase):
    def test_if(self):
        self.givenTokens([
            Token(1, 1, TokenType.KEYWORD_IF.label, None),
            Token(1, 4, TokenType.SYMBOL_OPEN_PARENTHESIS.label, None),
            Token(1, 5, TokenType.IDENTIFIER.label, 'is_even'),
            Token(1, 12, TokenType.SYMBOL_CLOSE_PARENTHESIS.label, None),
            Token(2, 5, TokenType.KEYWORD_PRINT_CHARACTER.label, None),
            Token(2, 9, TokenType.SYMBOL_OPEN_PARENTHESIS.label, None),
            Token(2, 10, TokenType.LITERAL_INT.label, '0'),
            Token(2, 11, TokenType.SYMBOL_CLOSE_PARENTHESIS.label, None),
            Token(2, 12, TokenType.SYMBOL_SEMICOLON.label, None),
            Token(3, 1, TokenType.TERMINAL.label, None),
        ])
        self.whenParse()
        self.thenReturnNode(Node(
            type=NodeType.SEQUENCE,
            left=Node(
                type=NodeType.IF,
                left=Node(
                    type=NodeType.IDENTIFIER,
                    value='is_even',
                ),
                right=Node(
                    type=NodeType.IF,
                    left=Node(
                        type=NodeType.PRINT_CHARACTER,
                        left=Node(
                            type=NodeType.INT,
                            value='0',
                        ),
                    ),
                ),
            ),
        ))

    def test_if_else(self):
        self.givenTokens([
            Token(1, 1, TokenType.KEYWORD_IF.label, None),
            Token(1, 4, TokenType.SYMBOL_OPEN_PARENTHESIS.label, None),
            Token(1, 5, TokenType.IDENTIFIER.label, 'is_even'),
            Token(1, 12, TokenType.SYMBOL_CLOSE_PARENTHESIS.label, None),
            Token(2, 5, TokenType.KEYWORD_PRINT_CHARACTER.label, None),
            Token(2, 9, TokenType.SYMBOL_OPEN_PARENTHESIS.label, None),
            Token(2, 10, TokenType.LITERAL_INT.label, '0'),
            Token(2, 11, TokenType.SYMBOL_CLOSE_PARENTHESIS.label, None),
            Token(2, 12, TokenType.SYMBOL_SEMICOLON.label, None),
            Token(3, 1, TokenType.KEYWORD_ELSE.label, None),
            Token(4, 5, TokenType.KEYWORD_PRINT_CHARACTER.label, None),
            Token(4, 9, TokenType.SYMBOL_OPEN_PARENTHESIS.label, None),
            Token(4, 10, TokenType.LITERAL_INT.label, '1'),
            Token(4, 11, TokenType.SYMBOL_CLOSE_PARENTHESIS.label, None),
            Token(4, 12, TokenType.SYMBOL_SEMICOLON.label, None),
            Token(5, 1, TokenType.TERMINAL.label, None),
        ])
        self.whenParse()
        self.thenReturnNode(Node(
            type=NodeType.SEQUENCE,
            left=Node(
                type=NodeType.IF,
                left=Node(
                    type=NodeType.IDENTIFIER,
                    value='is_even',
                ),
                right=Node(
                    type=NodeType.IF,
                    left=Node(
                        type=NodeType.PRINT_CHARACTER,
                        left=Node(
                            type=NodeType.INT,
                            value='0',
                        ),
                    ),
                    right=Node(
                        type=NodeType.PRINT_CHARACTER,
                        left=Node(
                            type=NodeType.INT,
                            value='1',
                        ),
                    ),
                ),
            ),
        ))
