from collections.abc import Iterable
from typing import List
import unittest

from core.tokens import Token, TokenType
from core.lexer import Lexer


# Use global - should not accumulate state
lex = Lexer()


class LexerTestBase(unittest.TestCase):
    def givenProgramLines(self, program_lines: Iterable[str]):
        self.program_lines = program_lines

    def givenProgramLine(self, program_line: str):
        self.program_lines = [program_line]

    def whenLex(self):
        self.output = lex.from_program_lines(self.program_lines)
        self.assertIsInstance(self.output, Iterable)
        # Convert generator to list
        self.output = list(self.output)
    
    def whenLexParseLine(self):
        self.assertEqual(1, len(self.program_lines))
        self.output = lex(self.program_lines[0])
        self.assertIsInstance(self.output, Iterable)
        # Convert generator to list
        self.output = list(self.output)

    def thenReturnTokens(self, output: List[Token]):
        self.assertEqual(self.output, output)
    
    def thenReturnIterableTokens(self):
        self.assertTrue(isinstance(self.output, Iterable))

    def thenReturnTokenTypes(self, expected_tokens: List[TokenType]):
        self.thenReturnIterableTokens()
        self.assertEqual(
            [expected_token.name for expected_token in expected_tokens],
            [lexer_output.name for lexer_output in self.output])

    def thenReturnValues(self, expected_values: List[str]):
        self.thenReturnIterableTokens()
        self.assertEqual(
            expected_values,
            [lexer_output.value for lexer_output in self.output])
    
    def thenReturnNothing(self):
        self.thenReturnIterableTokens()
        self.assertEqual(0, len(self.output))
