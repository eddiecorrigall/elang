from core.tokens import Literal, Operator
from lexer.errors import LexerSyntaxError
from tests.lexer_test_base import LexerTestBase


class TestIntegerLiteral(LexerTestBase):
    def test_invalid_integer(self):
        self.givenProgramLine('123abc')
        with self.assertRaises(LexerSyntaxError):
            self.whenLexParseLine()

    def test_zero_prefix(self):
        for input in ['00', '01']:
            with self.subTest('test zero prefix {}'.format(input)):
                self.givenProgramLine(input)
                self.whenLexParseLine()
                self.thenReturnTokens([Literal.INT])
                self.thenReturnValues([input])
    
    def test_negate_zero(self):
        # Not handled by lexer
        self.givenProgramLine('-0')
        self.whenLexParseLine()
        self.thenReturnTokens([Operator.SUBTRACT, Literal.INT])
        self.thenReturnValues([None, '0'])

    def test_zero(self):
        self.givenProgramLine('0')
        self.whenLexParseLine()
        self.thenReturnTokens([Literal.INT])
        self.thenReturnValues(['0'])

    def test_positive_integers(self):
        for input, expected in [('5', '5'), ('25', '25'), ('123', '123')]:
            with self.subTest('test positive integer {}'.format(input)):
                self.givenProgramLine(input)
                self.whenLexParseLine()
                self.thenReturnTokens([Literal.INT])
                self.thenReturnValues([expected])

    def test_negative_integers(self):
        for input, expected in [('-2', '2'), ('-32', '32'), ('-100', '100')]:
            with self.subTest('test negative integer {}'.format(input)):
                self.givenProgramLine(input)
                self.whenLexParseLine()
                self.thenReturnTokens([Operator.SUBTRACT, Literal.INT])
                self.thenReturnValues([None, expected])
