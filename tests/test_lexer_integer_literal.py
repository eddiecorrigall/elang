from lexer.errors import LexerSyntaxError
from lexer.tokens import Literal, Operator
from tests.lexer_test_base import LexerTestBase


class TestIntegerLiteral(LexerTestBase):
    def test_invalid_integer(self):
        self.givenProgramLine('123abc')
        with self.assertRaises(LexerSyntaxError):
            self.when_lex()

    def test_zero_prefix(self):
        for input in ['00', '01']:
            with self.subTest('test zero prefix {}'.format(input)):
                self.givenProgramLine(input)
                self.when_lex()
                self.then_return_literal(Literal.INT, input)
    
    def test_negate_zero(self):
        # Not handled by lexer
        self.givenProgramLine('-0')
        self.when_lex()
        self.then_return_tokens([Operator.SUBTRACT, Literal.INT])
        self.then_return_values([None, '0'])
            
    def test_zero(self):
        self.givenProgramLine('0')
        self.when_lex()
        self.then_return_literal(Literal.INT, '0')

    def test_positive_integers(self):
        for input, expected in [('5', '5'), ('25', '25'), ('123', '123')]:
            with self.subTest('test positive integer {}'.format(input)):
                self.givenProgramLine(input)
                self.when_lex()
                self.then_return_literal(Literal.INT, expected)

    def test_negative_integers(self):
        for input, expected in [('-2', '2'), ('-32', '32'), ('-100', '100')]:
            with self.subTest('test negative integer {}'.format(input)):
                self.givenProgramLine(input)
                self.when_lex()
                self.then_return_tokens([Operator.SUBTRACT, Literal.INT])
                self.then_return_values([None, expected])
