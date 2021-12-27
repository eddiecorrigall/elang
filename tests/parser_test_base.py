from core.ast import Node
from core.parser import Parser
from core.tokens import Token

import unittest

from typing import Iterator, List


parser = Parser()


class ParserTestBase(unittest.TestCase):
    def givenTokens(self, tokens: Iterator[Token]):
        self.tokens = tokens

    def givenAbstractSyntaxTree(self, ast: Node):
        self.ast = ast

    def whenParse(self):
        self.ast = parser(self.tokens)

    def whenAsLines(self):
        self.lines = self.ast.as_lines()
        if isinstance(self.lines, Iterator):
            self.lines = list(self.lines)

    def thenReturnAbstractSyntaxTree(self, expected_ast: dict):
        self.assertEqual(expected_ast, self.ast.as_dict())

    def thenReturnLines(self, expected_lines: List[str]):
        self.assertEqual(expected_lines, self.lines)
