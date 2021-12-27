from core.ast import Node
from core.parser import Parser
from core.tokens import Token

import unittest

from typing import Iterable, Iterator


parser = Parser()


class ParserTestBase(unittest.TestCase):
    def givenTokens(self, tokens: Iterator[Token]):
        self.tokens = tokens

    def givenNode(self, ast: Node):
        self.ast = ast

    def whenParse(self):
        self.ast = parser(self.tokens)

    def whenNodeAsLines(self):
        self.lines = self.ast.as_lines()
        if isinstance(self.lines, Iterator):
            self.lines = list(self.lines)

    def thenReturnNode(self, expected_ast: Node):
        self.assertEqual(expected_ast.as_dict(), self.ast.as_dict())

    def thenReturnLines(self, expected_lines: Iterable[str]):
        self.assertEqual(expected_lines, self.lines)
