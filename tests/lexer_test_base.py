from collections.abc import Iterable
from typing import List
import unittest

from lexer.lexer import Lexer
from lexer.tokens import Literal, Token


# Use global - should not accumulate state
lex = Lexer()


class LexerTestBase(unittest.TestCase):
    input = None
    output = None
    
    def given_input(self, input: str):
        self.input = input
    
    def when_lex(self):
        self.output = lex(self.input)
        if isinstance(self.output, Iterable):
            # Convert generator to list
            self.output = list(self.output)
    
    def then_return_iterable(self):
        self.assertTrue(isinstance(self.output, Iterable))
    
    def then_return_literal(self, expected_literal: Literal, expected_value: str):
        self.then_return_iterable()
        self.assertEqual(1, len(self.output))
        self.assertEqual(expected_literal, self.output[0].token)
        self.assertEqual(expected_value, self.output[0].value)

    def then_return_tokens(self, expected_tokens: List[Token]):
        self.then_return_iterable()
        self.assertEqual(
            expected_tokens,
            [lexer_output.token for lexer_output in self.output])

    def then_return_values(self, expected_values: List[str]):
        self.then_return_iterable()
        self.assertEqual(
            expected_values,
            [lexer_output.value for lexer_output in self.output])

    def then_return_token(self, expected_token: Token):
        self.then_return_tokens([expected_token])

    def then_return_no_value(self):
        self.then_return_iterable()
        self.assertEqual(1, len(self.output))
        self.assertIsNone(self.output[0].value)
    
    def then_return_empty(self):
        self.then_return_iterable()
        self.assertEqual(0, len(self.output))
