from core.errors import LexerSyntaxError
from core.tokens import TokenType
from tests.lexer_test_base import LexerTestBase


class TestWhitespace(LexerTestBase):
    def test_keyword_with_whitespace(self):
        self.givenProgramLine('if print')
        self.whenLexParseLine()
        self.thenReturnTokenTypes([
            TokenType.KEYWORD_IF,
            TokenType.KEYWORD_PRINT_STRING,
        ])

    def test_keyword_without_whitespace(self):
        self.givenProgramLine('ifprint')
        self.whenLexParseLine()
        self.thenReturnTokenTypes([TokenType.IDENTIFIER])
        self.thenReturnValues(['ifprint'])

    def test_operator_with_invalid_whitespace(self):
        self.givenProgramLine('& &')
        with self.assertRaises(LexerSyntaxError):
            self.whenLexParseLine()

    def test_operator_with_valid_whitespace(self):
        self.givenProgramLine(' &&')
        self.whenLexParseLine()
        self.thenReturnTokenTypes([TokenType.OPERATOR_AND])

    def test_symbol_with_valid_whitespace(self):
        self.givenProgramLine('\t(')
        self.whenLexParseLine()
        self.thenReturnTokenTypes([TokenType.SYMBOL_OPEN_PARENTHESIS])
