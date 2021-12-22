from core.ast import NodeType
from core.tokens import Identifier, Literal, Operator, Symbol, Terminal, Token
from tests.parser_test_base import ParserTestBase


class TestParserAssignment(ParserTestBase):
    def test_assign_literal_integer(self):
        self.givenTokens([
            Token(line=1, offset=1, label=Identifier.IDENTIFIER.label, value='abc'),
            Token(line=1, offset=5, label=Operator.ASSIGN.label, value=None),
            Token(line=1, offset=7, label=Literal.INT.label, value='123'),
            Token(line=1, offset=10, label=Symbol.SEMICOLON.label, value=None),
            Token(line=2, offset=1, label=Terminal.TERMINAL.label, value=None),
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
            Token(line=1, offset=1, label=Identifier.IDENTIFIER.label, value='abc'),
            Token(line=1, offset=5, label=Operator.ASSIGN.label, value=None),
            Token(line=1, offset=7, label=Identifier.IDENTIFIER.label, value='xyz'),
            Token(line=1, offset=10, label=Symbol.SEMICOLON.label, value=None),
            Token(line=2, offset=1, label=Terminal.TERMINAL.label, value=None),
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
