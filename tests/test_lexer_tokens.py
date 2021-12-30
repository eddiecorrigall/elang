import unittest

from core.tokens import TokenType
from tests.lexer_test_base import LexerTestBase


class TestTokenEquality(unittest.TestCase):
    def test_identity_equality(self):
        self.assertIs(TokenType.LITERAL_CHAR, TokenType.LITERAL_CHAR)
        self.assertEqual(TokenType.LITERAL_CHAR, TokenType.LITERAL_CHAR)

        self.assertIsNot(TokenType.LITERAL_CHAR, TokenType.LITERAL_INT)
        self.assertNotEqual(TokenType.LITERAL_CHAR, TokenType.LITERAL_INT)

    def test_operator_equality(self):
        self.assertIs(TokenType.OPERATOR_ADD, TokenType.OPERATOR_ADD)
        self.assertEqual(TokenType.OPERATOR_ADD, TokenType.OPERATOR_ADD)

        self.assertIsNot(TokenType.OPERATOR_ADD, TokenType.OPERATOR_SUBTRACT)
        self.assertNotEqual(TokenType.OPERATOR_ADD, TokenType.OPERATOR_SUBTRACT)

    def test_symbol_equality(self):
        self.assertIs(TokenType.SYMBOL_OPEN_PARENTHESIS, TokenType.SYMBOL_OPEN_PARENTHESIS)
        self.assertEqual(TokenType.SYMBOL_OPEN_PARENTHESIS, TokenType.SYMBOL_OPEN_PARENTHESIS)

        self.assertIsNot(TokenType.SYMBOL_OPEN_PARENTHESIS, TokenType.SYMBOL_CLOSE_PARENTHESIS)
        self.assertNotEqual(TokenType.SYMBOL_OPEN_PARENTHESIS, TokenType.SYMBOL_CLOSE_PARENTHESIS)

    def test_keyword_equality(self):
        self.assertIs(TokenType.KEYWORD_IF, TokenType.KEYWORD_IF)
        self.assertEqual(TokenType.KEYWORD_IF, TokenType.KEYWORD_IF)

        self.assertIsNot(TokenType.KEYWORD_IF, TokenType.KEYWORD_ELSE)
        self.assertNotEqual(TokenType.KEYWORD_IF, TokenType.KEYWORD_ELSE)

    def test_keyword_equality(self):
        self.assertIs(TokenType.WHITESPACE_NEWLINE, TokenType.WHITESPACE_NEWLINE)
        self.assertEqual(TokenType.WHITESPACE_NEWLINE, TokenType.WHITESPACE_NEWLINE)

        self.assertIsNot(TokenType.WHITESPACE_NEWLINE, TokenType.WHITESPACE_TAB)
        self.assertNotEqual(TokenType.WHITESPACE_NEWLINE, TokenType.WHITESPACE_TAB)


class TestTokens(LexerTestBase):
    def test_operators(self):
        for token_type in TokenType:
            if not token_type.name.startswith('OPERATOR_'):
                continue
            operator = token_type
            with self.subTest('test operator {}'.format(operator.name)):
                self.givenProgramLine(operator.sequence)
                self.whenLexParseLine()
                self.thenReturnTokenTypes([operator])
    
    def test_symbols(self):
        for token_type in TokenType:
            if not token_type.name.startswith('SYMBOL_'):
                continue
            symbol = token_type
            with self.subTest('test symbol {}'.format(symbol.name)):
                self.givenProgramLine(symbol.sequence)
                self.whenLexParseLine()
                self.thenReturnTokenTypes([symbol])

    def test_keywords(self):
        for token_type in TokenType:
            if not token_type.name.startswith('KEYWORD_'):
                continue
            keyword = token_type
            with self.subTest('test keyword {}'.format(keyword.name)):
                self.givenProgramLine(keyword.sequence)
                self.whenLexParseLine()
                self.thenReturnTokenTypes([keyword])

    def test_whitespace(self):
        for token_type in TokenType:
            if not token_type.name.startswith('WHITESPACE_'):
                continue
            whitespace = token_type
            with self.subTest('test whitespace {}'.format(whitespace.name)):
                self.givenProgramLine(whitespace.sequence)
                self.whenLexParseLine()
                self.thenReturnNothing()
