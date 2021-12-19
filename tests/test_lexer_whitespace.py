from lexer.errors import LexerSyntaxError
from lexer.tokens import Identifier, Keyword, Operator, Symbol
from tests.lexer_test_base import LexerTestBase


class TestWhitespace(LexerTestBase):
    def test_keyword_with_whitespace(self):
        self.givenProgramLine('if print')
        self.whenLexParseLine()
        self.thenReturnTokens([
            Keyword.IF,
            Keyword.PRINT_STRING,
        ])

    def test_keyword_without_whitespace(self):
        self.givenProgramLine('ifprint')
        self.whenLexParseLine()
        self.thenReturnTokens([Identifier.IDENTIFIER])
        self.thenReturnValues(['ifprint'])

    def test_operator_with_invalid_whitespace(self):
        self.givenProgramLine('& &')
        with self.assertRaises(LexerSyntaxError):
            self.whenLexParseLine()

    def test_operator_with_valid_whitespace(self):
        self.givenProgramLine(' &&')
        self.whenLexParseLine()
        self.thenReturnTokens([Operator.AND])

    def test_symbol_with_valid_whitespace(self):
        self.givenProgramLine('\t(')
        self.whenLexParseLine()
        self.thenReturnTokens([Symbol.LEFT_PARENTHESIS])
