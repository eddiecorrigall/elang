import tempfile
import unittest
from core.lexer import Lexer
from core.parser import Parser
from core.walker import Walker


lex = Lexer()
parse = Parser()
walk = Walker()

class WalkerTestBase(unittest.TestCase):
    def givenProgramLines(self, lines: list[str]):
        self.input_lines = lines

    def whenRunProgramLines(self):
        tokens = lex.from_program_lines([
            self.input_lines
        ])
        ast = parse(tokens)
        with tempfile.TemporaryFile() as stdout:
            walk(ast, stdout=stdout)
            stdout.seek(0)
            self.output_text = stdout.read().decode('utf-8')

    def thenStandardOutputEquals(self, text: str):
        self.assertEquals(text, self.output_text)
