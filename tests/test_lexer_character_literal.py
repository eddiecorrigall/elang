from core.errors import LexerSyntaxError
from core.tokens import Literal
from tests.lexer_test_base import LexerTestBase


class TestCharLiteral(LexerTestBase):
    def test_empty_character(self):
        self.givenProgramLine("''")
        with self.assertRaises(LexerSyntaxError):
            self.whenLexParseLine()

    def test_single_character(self):
        self.givenProgramLine("'A'")
        self.whenLexParseLine()
        self.thenReturnTokenTypes([Literal.INT])
        self.thenReturnValues(['65'])
    
    def test_two_characters(self):
        self.givenProgramLine("'Ab'")
        with self.assertRaises(LexerSyntaxError):
            self.whenLexParseLine()
    
    def test_three_characters(self):
        self.givenProgramLine("'Abc'")
        with self.assertRaises(LexerSyntaxError):
            self.whenLexParseLine()
    
    def test_newline(self):
        self.givenProgramLine("'\n'")
        with self.assertRaises(LexerSyntaxError):
            self.whenLexParseLine()

    def test_escaped_newline(self):
        self.givenProgramLine("'\\n'")
        self.whenLexParseLine()
        self.thenReturnTokenTypes([Literal.INT])
        self.thenReturnValues(['10'])

    def test_single_quote(self):
        self.givenProgramLine("'''")
        with self.assertRaises(LexerSyntaxError):
            self.whenLexParseLine()
    
    def test_escaped_single_quote(self):
        self.givenProgramLine("'\\''")
        with self.assertRaises(LexerSyntaxError):
            self.whenLexParseLine()

    def test_backslash(self):
        self.givenProgramLine("'\\'")
        with self.assertRaises(LexerSyntaxError):
            self.whenLexParseLine()

    def test_escaped_backslash(self):
        self.givenProgramLine("'\\\\'")
        self.whenLexParseLine()
        self.thenReturnTokenTypes([Literal.INT])
        self.thenReturnValues(['92'])

    def test_escaped_single_quote(self):
        self.givenProgramLine("'\\''")
        with self.assertRaises(LexerSyntaxError):
            self.whenLexParseLine()

    def test_unknown_escape_character(self):
        self.givenProgramLine("'\\r'")
        with self.assertRaises(LexerSyntaxError):
            self.whenLexParseLine()
