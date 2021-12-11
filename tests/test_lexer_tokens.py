from lexer import Token, IntegerLiteral, Operator, Symbol, Keyword, Whitespace
from lexer.tokens import Identifier, TokenWithValue
from tests import LexerTestBase


class TestToken(Token):
    LABEL = 'TEST_TOKEN'


class OtherTestToken(Token):
    LABEL = 'OTHER_TEST_TOKEN'
    

class TestTokenWithValue(TokenWithValue):
    LABEL = 'TEST_TOKEN_WITH_VALUE'


class OtherTestTokenWithValue(TokenWithValue):
    LABEL = 'OTHER_TEST_TOKEN_WITH_VALUE'


class TestTokens(LexerTestBase):
    
    def test_token_equality(self):
        self.assertIsNot(TestToken(), TestToken())
        self.assertIsNot(TestToken(), OtherTestToken())
        self.assertEqual(TestToken(), TestToken())
        self.assertNotEqual(TestToken(), OtherTestToken())

    def test_token_equality(self):
        value = '123'
        otherValue = 'abc'

        self.assertIsNot(TestTokenWithValue(value), TestTokenWithValue(value))
        self.assertIsNot(TestTokenWithValue(value), OtherTestTokenWithValue(value))

        self.assertIsNot(TestTokenWithValue(value), TestTokenWithValue(otherValue))
        self.assertIsNot(TestTokenWithValue(value), OtherTestTokenWithValue(otherValue))

        self.assertEqual(TestTokenWithValue(value), TestTokenWithValue(value))
        self.assertNotEqual(TestTokenWithValue(value), OtherTestTokenWithValue(value))

        self.assertNotEqual(TestTokenWithValue(value), TestTokenWithValue(otherValue))
        self.assertNotEqual(TestTokenWithValue(value), OtherTestTokenWithValue(otherValue))

    def test_integer_literal_equality(self):
        value = '123'
        self.assertIsNot(IntegerLiteral(value), IntegerLiteral(value))
        self.assertEqual(IntegerLiteral(value), IntegerLiteral(value))
    
    def test_identifier_equality(self):
        value = 'print'
        self.assertIsNot(Identifier(value), Identifier(value))
        self.assertEqual(Identifier(value), Identifier(value))

    def test_operator_equality(self):
        self.assertIs(Operator.ADD, Operator.ADD)
        self.assertEqual(Operator.ADD, Operator.ADD)

    def test_operators(self):
        for operator in Operator:
            if operator == Operator.NEGATE:
                # Lexer should output Operator.SUBTRACT instead
                continue
            with self.subTest('test operator {}'.format(operator.name)):
                self.given_input(operator.sequence)
                self.when_lex()
                self.then_return_token(operator)
    
    def test_operator_negate(self):
        self.given_input(Operator.NEGATE.sequence)
        self.when_lex()
        self.then_return_token(Operator.SUBTRACT)

    def test_symbol_equality(self):
        self.assertIs(Symbol.LEFT_PARENTHESIS, Symbol.LEFT_PARENTHESIS)
        self.assertEqual(Symbol.LEFT_PARENTHESIS, Symbol.LEFT_PARENTHESIS)

    def test_symbols(self):
        for symbol in Symbol:
            with self.subTest('test symbol {}'.format(symbol.name)):
                self.given_input(symbol.sequence)
                self.when_lex()
                self.then_return_token(symbol)

    def test_keyword_equality(self):
        self.assertIs(Keyword.IF, Keyword.IF)
        self.assertEqual(Keyword.IF, Keyword.IF)

    def test_keywords(self):
        for keyword in Keyword:
            with self.subTest('test keyword {}'.format(keyword.name)):
                self.given_input(keyword.sequence)
                self.when_lex()
                self.then_return_token(keyword)

    def test_keyword_equality(self):
        self.assertIs(Whitespace.NEWLINE, Whitespace.NEWLINE)
        self.assertEqual(Whitespace.NEWLINE, Whitespace.NEWLINE)

    def test_whitespace(self):
        for whitespace in Whitespace:
            with self.subTest('test whitespace {}'.format(whitespace.name)):
                self.given_input(whitespace.sequence)
                self.when_lex()
                self.then_return_empty()
