from lexer.errors import LexerSyntaxError
from lexer.tokens import Identifier, Keyword, Operator, Symbol
from tests.lexer_test_base import LexerTestBase


class TestWhitespace(LexerTestBase):
    def test_keyword_with_whitespace(self):
        self.givenProgramLine('if print')
        self.when_lex()
        self.then_return_tokens([
            Keyword.IF,
            Keyword.PRINT_STRING,
        ])

    def test_keyword_without_whitespace(self):
        self.givenProgramLine('ifprint')
        self.when_lex()
        self.then_return_tokens([Identifier.IDENTIFIER])
        self.then_return_values(['ifprint'])

    def test_operator_with_invalid_whitespace(self):
        self.givenProgramLine('& &')
        with self.assertRaises(LexerSyntaxError):
            self.when_lex()

    def test_operator_with_valid_whitespace(self):
        self.givenProgramLine(' &&')
        self.when_lex()
        self.then_return_token(Operator.AND)

    def test_symbol_with_valid_whitespace(self):
        self.givenProgramLine('\t(')
        self.when_lex()
        self.then_return_token(Symbol.LEFT_PARENTHESIS)
