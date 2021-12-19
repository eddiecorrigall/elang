from collections.abc import Iterable
from typing import List
import unittest

from core.tokens import Token
from lexer.lexer import Lexer, LexerOutput


# Use global - should not accumulate state
lex = Lexer()


class LexerTestBase(unittest.TestCase):
    def givenProgramLines(self, program_lines: List[str]):
        self.program = '\n'.join(program_lines)

    def givenProgramLine(self, program):
        self.program = program

    def whenLex(self):
        self.output = lex(self.program)
        self.assertIsInstance(self.output, Iterable)
        # Convert generator to list
        self.output = list(self.output)
    
    def whenLexParseLine(self):
        self.output = lex.parse_line(line=self.program, line_number=1)
        self.assertIsInstance(self.output, Iterable)
        # Convert generator to list
        self.output = list(self.output)

    def thenReturnLexerOutput(self, output: List[LexerOutput]):
        self.assertEqual(self.output, output)
    
    def thenReturnIterableLexerOutput(self):
        self.assertTrue(isinstance(self.output, Iterable))

    def thenReturnTokens(self, expected_tokens: List[Token]):
        self.thenReturnIterableLexerOutput()
        self.assertEqual(
            [expected_token.label for expected_token in expected_tokens],
            [lexer_output.label for lexer_output in self.output])

    def thenReturnValues(self, expected_values: List[str]):
        self.thenReturnIterableLexerOutput()
        self.assertEqual(
            expected_values,
            [lexer_output.value for lexer_output in self.output])
    
    def thenReturnEmptyLexerOutput(self):
        self.thenReturnIterableLexerOutput()
        self.assertEqual(0, len(self.output))
