from lexer.errors import LexerSyntaxError
from lexer.tokens import Literal
from tests.lexer_test_base import LexerTestBase


class TestCharLiteral(LexerTestBase):
    def test_empty_character(self):
        self.given_input("''")
        with self.assertRaises(LexerSyntaxError):
            self.when_lex()

    def test_single_character(self):
        self.given_input("'A'")
        self.when_lex()
        self.then_return_literal(Literal.CHAR, '65')
    
    def test_two_characters(self):
        self.given_input("'Ab'")
        with self.assertRaises(LexerSyntaxError):
            self.when_lex()
    
    def test_three_characters(self):
        self.given_input("'Abc'")
        with self.assertRaises(LexerSyntaxError):
            self.when_lex()
    
    def test_newline(self):
        self.given_input("'\n'")
        with self.assertRaises(LexerSyntaxError):
            self.when_lex()

    def test_escaped_newline(self):
        self.given_input("'\\n'")
        self.when_lex()
        self.then_return_literal(Literal.CHAR, '10')

    def test_single_quote(self):
        self.given_input("'''")
        with self.assertRaises(LexerSyntaxError):
            self.when_lex()
    
    def test_escaped_single_quote(self):
        self.given_input("'\\''")
        with self.assertRaises(LexerSyntaxError):
            self.when_lex()

    def test_backslash(self):
        self.given_input("'\\'")
        with self.assertRaises(LexerSyntaxError):
            self.when_lex()

    def test_escaped_backslash(self):
        self.given_input("'\\\\'")
        self.when_lex()
        self.then_return_literal(Literal.CHAR, '92')

    def test_escaped_single_quote(self):
        self.given_input("'\\''")
        with self.assertRaises(LexerSyntaxError):
            self.when_lex()

    def test_unknown_escape_character(self):
        self.given_input("'\\r'")
        with self.assertRaises(LexerSyntaxError):
            self.when_lex()
