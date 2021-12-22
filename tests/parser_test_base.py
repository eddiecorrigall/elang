from core.parser import Parser
from core.tokens import Token

import unittest

from typing import Iterator


parser = Parser()


class ParserTestBase(unittest.TestCase):
    def givenTokens(self, tokens: Iterator[Token]):
        self.tokens = tokens

    def whenParse(self):
        self.ast = parser(self.tokens)

    def thenReturnAbstractSyntaxTree(self, expected_ast: dict):
        self.assertEqual(expected_ast, self.ast.as_dict())
