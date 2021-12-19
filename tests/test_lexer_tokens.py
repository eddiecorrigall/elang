import unittest

from lexer.tokens import Literal, Operator, Symbol, Keyword, Whitespace
from tests.lexer_test_base import LexerTestBase


class TestTokenEquality(unittest.TestCase):
    def test_identity_equality(self):
        self.assertIs(Literal.CHAR, Literal.CHAR)
        self.assertEqual(Literal.CHAR, Literal.CHAR)

        self.assertIsNot(Literal.CHAR, Literal.INT)
        self.assertNotEqual(Literal.CHAR, Literal.INT)

    def test_operator_equality(self):
        self.assertIs(Operator.ADD, Operator.ADD)
        self.assertEqual(Operator.ADD, Operator.ADD)

        self.assertIsNot(Operator.ADD, Operator.SUBTRACT)
        self.assertNotEqual(Operator.ADD, Operator.SUBTRACT)

    def test_symbol_equality(self):
        self.assertIs(Symbol.LEFT_PARENTHESIS, Symbol.LEFT_PARENTHESIS)
        self.assertEqual(Symbol.LEFT_PARENTHESIS, Symbol.LEFT_PARENTHESIS)

        self.assertIsNot(Symbol.LEFT_PARENTHESIS, Symbol.RIGHT_PARENTHESIS)
        self.assertNotEqual(Symbol.LEFT_PARENTHESIS, Symbol.RIGHT_PARENTHESIS)

    def test_keyword_equality(self):
        self.assertIs(Keyword.IF, Keyword.IF)
        self.assertEqual(Keyword.IF, Keyword.IF)

        self.assertIsNot(Keyword.IF, Keyword.ELSE)
        self.assertNotEqual(Keyword.IF, Keyword.ELSE)

    def test_keyword_equality(self):
        self.assertIs(Whitespace.NEWLINE, Whitespace.NEWLINE)
        self.assertEqual(Whitespace.NEWLINE, Whitespace.NEWLINE)

        self.assertIsNot(Whitespace.NEWLINE, Whitespace.TAB)
        self.assertNotEqual(Whitespace.NEWLINE, Whitespace.TAB)


class TestTokens(LexerTestBase):
    def test_operators(self):
        for operator in Operator:
            if operator == Operator.NEGATE:
                # Lexer should output Operator.SUBTRACT instead
                continue
            with self.subTest('test operator {}'.format(operator.name)):
                self.givenProgramLine(operator.sequence)
                self.whenLexParseLine()
                self.then_return_token(operator)
    
    def test_operator_negate(self):
        self.givenProgramLine(Operator.NEGATE.sequence)
        self.whenLexParseLine()
        self.then_return_token(Operator.SUBTRACT)

    def test_symbols(self):
        for symbol in Symbol:
            with self.subTest('test symbol {}'.format(symbol.name)):
                self.givenProgramLine(symbol.sequence)
                self.whenLexParseLine()
                self.then_return_token(symbol)

    def test_keywords(self):
        for keyword in Keyword:
            with self.subTest('test keyword {}'.format(keyword.name)):
                self.givenProgramLine(keyword.sequence)
                self.whenLexParseLine()
                self.then_return_token(keyword)

    def test_whitespace(self):
        for whitespace in Whitespace:
            with self.subTest('test whitespace {}'.format(whitespace.name)):
                self.givenProgramLine(whitespace.sequence)
                self.whenLexParseLine()
                self.thenReturnEmptyLexerOutput()
