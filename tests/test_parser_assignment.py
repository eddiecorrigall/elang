from core.ast import NodeType
from core.tokens import Identifier, Literal, Operator, Symbol, Terminal
from core.lexer import LexerOutput
from tests.parser_test_base import ParserTestBase


class TestParserAssignment(ParserTestBase):
    def test_assign_literal_integer(self):
        self.givenTokens([
            LexerOutput(line=1, offset=1, label=Identifier.IDENTIFIER.label, value='abc'),
            LexerOutput(line=1, offset=5, label=Operator.ASSIGN.label, value=None),
            LexerOutput(line=1, offset=7, label=Literal.INT.label, value='123'),
            LexerOutput(line=1, offset=10, label=Symbol.SEMICOLON.label, value=None),
            LexerOutput(line=2, offset=1, label=Terminal.TERMINAL.label, value=None),
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
            LexerOutput(line=1, offset=1, label=Identifier.IDENTIFIER.label, value='abc'),
            LexerOutput(line=1, offset=5, label=Operator.ASSIGN.label, value=None),
            LexerOutput(line=1, offset=7, label=Identifier.IDENTIFIER.label, value='xyz'),
            LexerOutput(line=1, offset=10, label=Symbol.SEMICOLON.label, value=None),
            LexerOutput(line=2, offset=1, label=Terminal.TERMINAL.label, value=None),
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
