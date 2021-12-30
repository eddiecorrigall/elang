from core.errors import LexerSyntaxError
from core.tokens import TokenType
from tests.lexer_test_base import LexerTestBase


class TestWhitespace(LexerTestBase):
    def test_keyword_with_whitespace(self):
        self.givenProgramLine(
            TokenType.KEYWORD_IF.sequence +
            ' ' +
            TokenType.KEYWORD_PRINT_STRING.sequence)
        self.whenLexParseLine()
        self.thenReturnTokenTypes([
            TokenType.KEYWORD_IF,
            TokenType.KEYWORD_PRINT_STRING,
        ])

    def test_keyword_without_whitespace(self):
        self.givenProgramLine(
            TokenType.KEYWORD_IF.sequence +
            TokenType.KEYWORD_PRINT_STRING.sequence)
        self.whenLexParseLine()
        self.thenReturnTokenTypes([TokenType.IDENTIFIER])
        self.thenReturnValues([
            TokenType.KEYWORD_IF.sequence +
            TokenType.KEYWORD_PRINT_STRING.sequence])

    def test_two_operators_with_valid_whitespace(self):
        self.givenProgramLine(
            TokenType.OPERATOR_LESS.sequence +
            ' ' +
            TokenType.OPERATOR_EQUAL.sequence)
        self.whenLexParseLine()
        

    def test_once_operator_with_valid_whitespace(self):
        self.givenProgramLine(
            ' ' + TokenType.OPERATOR_LESS_OR_EQUAL.sequence)
        self.whenLexParseLine()
        self.thenReturnTokenTypes([TokenType.OPERATOR_LESS_OR_EQUAL])

    def test_symbol_with_valid_whitespace(self):
        self.givenProgramLine(
            '\t' + TokenType.SYMBOL_OPEN_PARENTHESIS.sequence)
        self.whenLexParseLine()
        self.thenReturnTokenTypes([TokenType.SYMBOL_OPEN_PARENTHESIS])
