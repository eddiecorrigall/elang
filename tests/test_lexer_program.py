from core.tokens import Identifier, Keyword, Literal, Operator, Symbol, Terminal
from lexer import Lexer, LexerOutput
from tests.lexer_test_base import LexerTestBase


lex = Lexer()


class TestProgram(LexerTestBase):
    def test_whitespace_and_singleline_comments(self):
        self.givenProgramLines([
            r'if ( p ) { // meaning n is prime',
            r'   // print number with space',
            r'   print ( n , " " ) ;',
            r'   count = count + 1 ; // number of primes found so far',
            r'}',
        ])
        self.whenLex()
        self.thenReturnLexerOutput([
            # line 1
            LexerOutput(1, 1, Keyword.IF.label, None),
            LexerOutput(1, 4, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(1, 6, Identifier.IDENTIFIER.label, 'p'),
            LexerOutput(1, 8, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(1, 10, Symbol.LEFT_BRACE.label, None),
            # line 2 - comment
            # line 3
            LexerOutput(3, 4, Keyword.PRINT_STRING.label, None),
            LexerOutput(3, 10, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(3, 12, Identifier.IDENTIFIER.label, 'n'),
            LexerOutput(3, 14, Symbol.COMMA.label, None),
            LexerOutput(3, 16, Literal.STR.label, '" "'),
            LexerOutput(3, 20, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(3, 22, Symbol.SEMICOLON.label, None),
            # line 4
            LexerOutput(4, 4, Identifier.IDENTIFIER.label, 'count'),
            LexerOutput(4, 10, Operator.ASSIGN.label, None),
            LexerOutput(4, 12, Identifier.IDENTIFIER.label, 'count'),
            LexerOutput(4, 18, Operator.ADD.label, None),
            LexerOutput(4, 20, Literal.INT.label, '1'),
            LexerOutput(4, 22, Symbol.SEMICOLON.label, None),
            # line 5
            LexerOutput(5, 1, Symbol.RIGHT_BRACE.label, None),
            # line 6
            LexerOutput(6, 1, Terminal.TERMINAL.label, None),
        ])

    def test_without_whitespace(self):
        self.givenProgramLine(r'if(p){print(n," ");count=count+1;}')
        self.whenLex()
        self.thenReturnLexerOutput([
            LexerOutput(1, 1, Keyword.IF.label, None),
            LexerOutput(1, 3, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(1, 4, Identifier.IDENTIFIER.label, 'p'),
            LexerOutput(1, 5, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(1, 6, Symbol.LEFT_BRACE.label, None),
            LexerOutput(1, 7, Keyword.PRINT_STRING.label, None),
            LexerOutput(1, 12, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(1, 13, Identifier.IDENTIFIER.label, 'n'),
            LexerOutput(1, 14, Symbol.COMMA.label, None),
            LexerOutput(1, 15, Literal.STR.label, '" "'),
            LexerOutput(1, 18, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(1, 19, Symbol.SEMICOLON.label, None),
            LexerOutput(1, 20, Identifier.IDENTIFIER.label, 'count'),
            LexerOutput(1, 25, Operator.ASSIGN.label, None),
            LexerOutput(1, 26, Identifier.IDENTIFIER.label, 'count'),
            LexerOutput(1, 31, Operator.ADD.label, None),
            LexerOutput(1, 32, Literal.INT.label, '1'),
            LexerOutput(1, 33, Symbol.SEMICOLON.label, None),
            LexerOutput(1, 34, Symbol.RIGHT_BRACE.label, None),

            LexerOutput(2, 1, Terminal.TERMINAL.label, None),
        ])

    def test_case_1_without_multiline_comment(self):
        self.givenProgramLines([
            r'print("Hello, World!\n");',
        ])
        self.whenLex()
        self.thenReturnLexerOutput([
            LexerOutput(1, 1, Keyword.PRINT_STRING.label, None),
            LexerOutput(1, 6, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(1, 7, Literal.STR.label, '"Hello, World!\\n"'),
            LexerOutput(1, 24, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(1, 25, Symbol.SEMICOLON.label, None),

            LexerOutput(2, 1, Terminal.TERMINAL.label, None),
        ])

    def test_case_phoenix_number_without_multiline_comment(self):
        # Test Case 2
        self.givenProgramLines([
            r'phoenix_number = 142857;',
            r'print(phoenix_number, "\n");',
        ])
        self.whenLex()
        self.thenReturnLexerOutput([
            LexerOutput(1, 1, Identifier.IDENTIFIER.label, 'phoenix_number'),
            LexerOutput(1, 16, Operator.ASSIGN.label, None),
            LexerOutput(1, 18, Literal.INT.label, '142857'),
            LexerOutput(1, 24, Symbol.SEMICOLON.label, None),

            LexerOutput(2, 1, Keyword.PRINT_STRING.label, None),
            LexerOutput(2, 6, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(2, 7, Identifier.IDENTIFIER.label, 'phoenix_number'),
            LexerOutput(2, 21, Symbol.COMMA.label, None),
            LexerOutput(2, 23, Literal.STR.label, '"\\n"'),
            LexerOutput(2, 27, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(2, 28, Symbol.SEMICOLON.label, None),

            LexerOutput(3, 1, Terminal.TERMINAL.label, None),
        ])

    def test_case_4_without_multiline_comment(self):
        # Test case 4
        self.givenProgramLines([
            r'print(42);',
            r'print("\nHello World\nGood Bye\nok\n");',
            r'print("Print a slash n - \\n.\n");',
        ])
        self.whenLex()
        self.thenReturnLexerOutput([
            # line 1
            LexerOutput(1, 1, Keyword.PRINT_STRING.label, None),
            LexerOutput(1, 6, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(1, 7, Literal.INT.label, '42'),
            LexerOutput(1, 9, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(1, 10, Symbol.SEMICOLON.label, None),
            # line 2
            LexerOutput(2, 1, Keyword.PRINT_STRING.label, None),
            LexerOutput(2, 6, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(2, 7, Literal.STR.label, r'"\nHello World\nGood Bye\nok\n"'),
            LexerOutput(2, 38, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(2, 39, Symbol.SEMICOLON.label, None),
            # line 3
            LexerOutput(3, 1, Keyword.PRINT_STRING.label, None),
            LexerOutput(3, 6, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(3, 7, Literal.STR.label, r'"Print a slash n - \\n.\n"'),
            LexerOutput(3, 33, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(3, 34, Symbol.SEMICOLON.label, None),
            # line 4
            LexerOutput(4, 1, Terminal.TERMINAL.label, None),
        ])

    def test_case_count(self):
        # Test case 5
        self.givenProgramLines([
            r'count = 1;',
            r'while (count < 10) {',
            r'    print("count is: ", count, "\n");',
            r'    count = count + 1;',
            r'}',
        ])
        self.whenLex()
        self.thenReturnLexerOutput([
            # line 1
            LexerOutput(1, 1, Identifier.IDENTIFIER.label, r'count'),
            LexerOutput(1, 7, Operator.ASSIGN.label, None),
            LexerOutput(1, 9, Literal.INT.label, r'1'),
            LexerOutput(1, 10, Symbol.SEMICOLON.label, None),
            # line 2
            LexerOutput(2, 1, Keyword.WHILE.label, None),
            LexerOutput(2, 7, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(2, 8, Identifier.IDENTIFIER.label, r'count'),
            LexerOutput(2, 14, Operator.LESS.label, None),
            LexerOutput(2, 16, Literal.INT.label, r'10'),
            LexerOutput(2, 18, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(2, 20, Symbol.LEFT_BRACE.label, None),
            # line 3
            LexerOutput(3, 5, Keyword.PRINT_STRING.label, None),
            LexerOutput(3, 10, Symbol.LEFT_PARENTHESIS.label, None),
            LexerOutput(3, 11, Literal.STR.label, r'"count is: "'),
            LexerOutput(3, 23, Symbol.COMMA.label, None),
            LexerOutput(3, 25, Identifier.IDENTIFIER.label, r'count'),
            LexerOutput(3, 30, Symbol.COMMA.label, None),
            LexerOutput(3, 32, Literal.STR.label, r'"\n"'),
            LexerOutput(3, 36, Symbol.RIGHT_PARENTHESIS.label, None),
            LexerOutput(3, 37, Symbol.SEMICOLON.label, None),
            # line 4
            LexerOutput(4, 5, Identifier.IDENTIFIER.label, r'count'),
            LexerOutput(4, 11, Operator.ASSIGN.label, None),
            LexerOutput(4, 13, Identifier.IDENTIFIER.label, r'count'),
            LexerOutput(4, 19, Operator.ADD.label, None),
            LexerOutput(4, 21, Literal.INT.label, r'1'),
            LexerOutput(4, 22, Symbol.SEMICOLON.label, None),
            # line 5
            LexerOutput(5, 1, Symbol.RIGHT_BRACE.label, None),
            # line 6
            LexerOutput(6, 1, Terminal.TERMINAL.label, None),
        ])
