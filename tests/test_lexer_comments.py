from tests.lexer_test_base import LexerTestBase


class TestComments(LexerTestBase):
    def test_double_forward_slash(self):
        self.given_input('//')
        self.when_lex()
        self.then_return_empty()
