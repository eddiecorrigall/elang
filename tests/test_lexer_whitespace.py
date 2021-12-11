from lexer import Identifier, LexerSyntaxError
from lexer import Keyword
from lexer.tokens import Operator
from tests.lexer_test_base import LexerTestBase


class TestWhitespace(LexerTestBase):
    def test_keyword_with_whitespace(self):
        self.given_input('if print')
        self.when_lex()
        self.then_return_tokens([
            Keyword.IF,
            Keyword.PRINT_STRING,
        ])

    def test_keyword_without_whitespace(self):
        self.given_input('ifprint')
        self.when_lex()
        self.then_return_tokens([
            Identifier('ifprint'),
        ])

    def test_operator_with_invalid_whitespace(self):
        self.given_input('& &')
        with self.assertRaises(LexerSyntaxError):
            self.when_lex()

    def test_operator_with_valid_whitespace(self):
        self.given_input(' &&')
        self.when_lex()
        self.then_return_token(Operator.AND)
