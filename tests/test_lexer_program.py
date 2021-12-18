from typing import List
import unittest

from lexer import Lexer
from lexer.lexer import LexerOutput
from lexer.tokens import Identifier, Keyword, Literal, Operator, Symbol, Token


lex = Lexer()


class TestProgram(unittest.TestCase):
    def givenProgramLines(self, program_lines: List[str]):
        self.program = '\n'.join(program_lines)

    def givenProgram(self, program):
        self.program = program

    def whenLex(self):
        self.tokens = list(lex(self.program))

    def thenReturnTokens(self, tokens: List[Token]):
        self.assertEqual(tokens, self.tokens)

    def test_whitespace_and_comments(self):
        self.givenProgramLines([
            'if ( p /* meaning n is prime */ ) {',
            '   print ( n , " " ) ;',
            '   count = count + 1 ; /* number of primes found so far */',
            '}',
        ])
        self.whenLex()
        self.thenReturnTokens([
            # line 1
            LexerOutput(1, 0, Keyword.IF.label, None),
            LexerOutput(1, 3, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(1, 5, Identifier.IDENTIFIER.label, 'p'),
            LexerOutput(1, 32, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(1, 34, Symbol.LEFT_BRACE.label, None),
            # line 2
            LexerOutput(2, 3, Keyword.PRINT_STRING.label, None),
            LexerOutput(2, 9, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(2, 11, Identifier.IDENTIFIER.label, 'n'),
            LexerOutput(2, 13, Symbol.COMMA.label, None),
            LexerOutput(2, 15, Literal.STR.label, '" "'),
            LexerOutput(2, 19, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(2, 21, Symbol.SEMICOLON.label, None),
            # line 3
            LexerOutput(3, 3, Identifier.IDENTIFIER.label, 'count'),
            LexerOutput(3, 9, Operator.ASSIGN.label, None),
            LexerOutput(3, 11, Identifier.IDENTIFIER.label, 'count'),
            LexerOutput(3, 17, Operator.ADD.label, None),
            LexerOutput(3, 19, Literal.INT.label, '1'),
            LexerOutput(3, 21, Symbol.SEMICOLON.label, None),
            # line 4
            LexerOutput(4, 0, Symbol.RIGHT_BRACE.label, None),
        ])

    def test_without_whitespace(self):
        self.givenProgram('if(p){print(n," ");count=count+1;}')
        self.whenLex()
        self.thenReturnTokens([
            LexerOutput(1, 0, Keyword.IF.label, None),
            LexerOutput(1, 2, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(1, 3, Identifier.IDENTIFIER.label, 'p'),
            LexerOutput(1, 4, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(1, 5, Symbol.LEFT_BRACE.label, None),
            LexerOutput(1, 6, Keyword.PRINT_STRING.label, None),
            LexerOutput(1, 11, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(1, 12, Identifier.IDENTIFIER.label, 'n'),
            LexerOutput(1, 13, Symbol.COMMA.label, None),
            LexerOutput(1, 14, Literal.STR.label, '" "'),
            LexerOutput(1, 17, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(1, 18, Symbol.SEMICOLON.label, None),
            LexerOutput(1, 19, Identifier.IDENTIFIER.label, 'count'),
            LexerOutput(1, 24, Operator.ASSIGN.label, None),
            LexerOutput(1, 25, Identifier.IDENTIFIER.label, 'count'),
            LexerOutput(1, 30, Operator.ADD.label, None),
            LexerOutput(1, 31, Literal.INT.label, '1'),
            LexerOutput(1, 32, Symbol.SEMICOLON.label, None),
            LexerOutput(1, 33, Symbol.RIGHT_BRACE.label, None),
        ])
