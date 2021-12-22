from core.lexer import LexerOutput
from core.parser import Parser

import unittest

from typing import List


parser = Parser()


class ParserTestBase(unittest.TestCase):
    def givenTokens(self, tokens: List[LexerOutput]):
        self.tokens = tokens

    def whenParse(self):
        self.ast = parser(self.tokens)

    def thenReturnAbstractSyntaxTree(self, expected_ast: dict):
        self.assertEqual(expected_ast, self.ast.as_dict())
