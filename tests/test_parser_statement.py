from core.ast import NodeType
from core.tokens import Identifier, Keyword, Literal, Operator, Symbol, Terminal, Token
from tests.parser_test_base import ParserTestBase


class TestParserStatementSemicolon(ParserTestBase):
    def test_semicolon(self):
        self.givenTokens([
            Token(1, 1, Symbol.SEMICOLON.label, None),
            Token(2, 1, Terminal.TERMINAL.label, None),
        ])
        self.whenParse()
        self.thenReturnAbstractSyntaxTree(dict(
            type=NodeType.SEQUENCE.label,
        ))
    
    def test_semicolon_as_lines(self):
        self.givenTokens([
            Token(1, 1, Symbol.SEMICOLON.label, None),
            Token(2, 1, Terminal.TERMINAL.label, None),
        ])
        self.whenParse()
        self.whenAsLines()
        self.thenReturnLines([
            NodeType.SEQUENCE.label,
            ';',
            ';',
        ])


class TestParserStatementAssignment(ParserTestBase):
    def test_assign_literal_integer(self):
        self.givenTokens([
            Token(1, 1, Identifier.IDENTIFIER.label, 'abc'),
            Token(1, 5, Operator.ASSIGN.label, None),
            Token(1, 7, Literal.INT.label, '123'),
            Token(1, 10, Symbol.SEMICOLON.label, None),
            Token(2, 1, Terminal.TERMINAL.label, None),
        ])
        self.whenParse()
        self.thenReturnAbstractSyntaxTree(dict(
            type=NodeType.SEQUENCE.label,
            left=dict(
                type=NodeType.ASSIGN.label,
                left=dict(
                    type=NodeType.IDENTIFIER.label,
                    value='abc',
                ),
                right=dict(
                    type=NodeType.INT.label,
                    value='123',
                ),
            ),
        ))

    def test_assign_identifier(self):
        self.givenTokens([
            Token(1, 1, Identifier.IDENTIFIER.label, 'abc'),
            Token(1, 5, Operator.ASSIGN.label, None),
            Token(1, 7, Identifier.IDENTIFIER.label, 'xyz'),
            Token(1, 10, Symbol.SEMICOLON.label, None),
            Token(2, 1, Terminal.TERMINAL.label, None),
        ])
        self.whenParse()
        self.thenReturnAbstractSyntaxTree(dict(
            type=NodeType.SEQUENCE.label,
            left=dict(
                type=NodeType.ASSIGN.label,
                left=dict(
                    type=NodeType.IDENTIFIER.label,
                    value='abc',
                ),
                right=dict(
                    type=NodeType.IDENTIFIER.label,
                    value='xyz',
                ),
            ),
        ))


class TestParserStatementPrintCharacter(ParserTestBase):
    def test_print_character_integer(self):
        self.givenTokens([
            Token(1, 1, Keyword.PRINT_CHARACTER.label, None),
            Token(1, 5, Symbol.OPEN_PARENTHESIS.label, None),
            Token(1, 6, Literal.INT.label, '123'),
            Token(1, 9, Symbol.CLOSE_PARENTHESIS.label, None),
            Token(1, 10, Symbol.SEMICOLON.label, None),
            Token(2, 1, Terminal.TERMINAL.label, None),
        ])
        self.whenParse()
        self.thenReturnAbstractSyntaxTree(dict(
            type=NodeType.SEQUENCE.label,
            left=dict(
                type=NodeType.PRINT_CHARACTER.label,
                left=dict(
                    type=NodeType.INT.label,
                    value='123',
                ),
            ),
        ))

    def test_print_character_integer_as_lines(self):
        self.givenTokens([
            Token(1, 1, Keyword.PRINT_CHARACTER.label, None),
            Token(1, 5, Symbol.OPEN_PARENTHESIS.label, None),
            Token(1, 6, Literal.INT.label, '123'),
            Token(1, 9, Symbol.CLOSE_PARENTHESIS.label, None),
            Token(1, 10, Symbol.SEMICOLON.label, None),
            Token(2, 1, Terminal.TERMINAL.label, None),
        ])
        self.whenParse()
        self.whenAsLines()
        self.thenReturnLines([
            NodeType.SEQUENCE.label,
            NodeType.PRINT_CHARACTER.label,
            NodeType.INT.label + '\t' + '123',
            ';',
            ';',
        ])
