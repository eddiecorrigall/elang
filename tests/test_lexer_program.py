from core.tokens import Identifier, Keyword, Literal, Operator, Symbol, Terminal, Token
from core.lexer import Lexer
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
        self.thenReturnTokens([
            # line 1
            Token(1, 1, Keyword.IF.label, None),
            Token(1, 4, Symbol.OPEN_PARENTHESIS.label, None),
            Token(1, 6, Identifier.IDENTIFIER.label, 'p'),
            Token(1, 8, Symbol.CLOSE_PARENTHESIS.label, None),
            Token(1, 10, Symbol.OPEN_BRACE.label, None),
            # line 2 - comment
            # line 3
            Token(3, 4, Keyword.PRINT_STRING.label, None),
            Token(3, 10, Symbol.OPEN_PARENTHESIS.label, None),
            Token(3, 12, Identifier.IDENTIFIER.label, 'n'),
            Token(3, 14, Symbol.COMMA.label, None),
            Token(3, 16, Literal.STR.label, '" "'),
            Token(3, 20, Symbol.CLOSE_PARENTHESIS.label, None),
            Token(3, 22, Symbol.SEMICOLON.label, None),
            # line 4
            Token(4, 4, Identifier.IDENTIFIER.label, 'count'),
            Token(4, 10, Operator.ASSIGN.label, None),
            Token(4, 12, Identifier.IDENTIFIER.label, 'count'),
            Token(4, 18, Operator.ADD.label, None),
            Token(4, 20, Literal.INT.label, '1'),
            Token(4, 22, Symbol.SEMICOLON.label, None),
            # line 5
            Token(5, 1, Symbol.CLOSE_BRACE.label, None),
            # line 6
            Token(6, 1, Terminal.TERMINAL.label, None),
        ])

    def test_without_whitespace(self):
        self.givenProgramLine(r'if(p){print(n," ");count=count+1;}')
        self.whenLex()
        self.thenReturnTokens([
            Token(1, 1, Keyword.IF.label, None),
            Token(1, 3, Symbol.OPEN_PARENTHESIS.label, None),
            Token(1, 4, Identifier.IDENTIFIER.label, 'p'),
            Token(1, 5, Symbol.CLOSE_PARENTHESIS.label, None),
            Token(1, 6, Symbol.OPEN_BRACE.label, None),
            Token(1, 7, Keyword.PRINT_STRING.label, None),
            Token(1, 12, Symbol.OPEN_PARENTHESIS.label, None),
            Token(1, 13, Identifier.IDENTIFIER.label, 'n'),
            Token(1, 14, Symbol.COMMA.label, None),
            Token(1, 15, Literal.STR.label, '" "'),
            Token(1, 18, Symbol.CLOSE_PARENTHESIS.label, None),
            Token(1, 19, Symbol.SEMICOLON.label, None),
            Token(1, 20, Identifier.IDENTIFIER.label, 'count'),
            Token(1, 25, Operator.ASSIGN.label, None),
            Token(1, 26, Identifier.IDENTIFIER.label, 'count'),
            Token(1, 31, Operator.ADD.label, None),
            Token(1, 32, Literal.INT.label, '1'),
            Token(1, 33, Symbol.SEMICOLON.label, None),
            Token(1, 34, Symbol.CLOSE_BRACE.label, None),

            Token(2, 1, Terminal.TERMINAL.label, None),
        ])

    def test_case_1_without_multiline_comment(self):
        self.givenProgramLines([
            r'print("Hello, World!\n");',
        ])
        self.whenLex()
        self.thenReturnTokens([
            Token(1, 1, Keyword.PRINT_STRING.label, None),
            Token(1, 6, Symbol.OPEN_PARENTHESIS.label, None),
            Token(1, 7, Literal.STR.label, '"Hello, World!\\n"'),
            Token(1, 24, Symbol.CLOSE_PARENTHESIS.label, None),
            Token(1, 25, Symbol.SEMICOLON.label, None),

            Token(2, 1, Terminal.TERMINAL.label, None),
        ])

    def test_case_phoenix_number_without_multiline_comment(self):
        # Test Case 2
        self.givenProgramLines([
            r'phoenix_number = 142857;',
            r'print(phoenix_number, "\n");',
        ])
        self.whenLex()
        self.thenReturnTokens([
            Token(1, 1, Identifier.IDENTIFIER.label, 'phoenix_number'),
            Token(1, 16, Operator.ASSIGN.label, None),
            Token(1, 18, Literal.INT.label, '142857'),
            Token(1, 24, Symbol.SEMICOLON.label, None),

            Token(2, 1, Keyword.PRINT_STRING.label, None),
            Token(2, 6, Symbol.OPEN_PARENTHESIS.label, None),
            Token(2, 7, Identifier.IDENTIFIER.label, 'phoenix_number'),
            Token(2, 21, Symbol.COMMA.label, None),
            Token(2, 23, Literal.STR.label, '"\\n"'),
            Token(2, 27, Symbol.CLOSE_PARENTHESIS.label, None),
            Token(2, 28, Symbol.SEMICOLON.label, None),

            Token(3, 1, Terminal.TERMINAL.label, None),
        ])

    def test_case_4_without_multiline_comment(self):
        # Test case 4
        self.givenProgramLines([
            r'print(42);',
            r'print("\nHello World\nGood Bye\nok\n");',
            r'print("Print a slash n - \\n.\n");',
        ])
        self.whenLex()
        self.thenReturnTokens([
            # line 1
            Token(1, 1, Keyword.PRINT_STRING.label, None),
            Token(1, 6, Symbol.OPEN_PARENTHESIS.label, None),
            Token(1, 7, Literal.INT.label, '42'),
            Token(1, 9, Symbol.CLOSE_PARENTHESIS.label, None),
            Token(1, 10, Symbol.SEMICOLON.label, None),
            # line 2
            Token(2, 1, Keyword.PRINT_STRING.label, None),
            Token(2, 6, Symbol.OPEN_PARENTHESIS.label, None),
            Token(2, 7, Literal.STR.label, r'"\nHello World\nGood Bye\nok\n"'),
            Token(2, 38, Symbol.CLOSE_PARENTHESIS.label, None),
            Token(2, 39, Symbol.SEMICOLON.label, None),
            # line 3
            Token(3, 1, Keyword.PRINT_STRING.label, None),
            Token(3, 6, Symbol.OPEN_PARENTHESIS.label, None),
            Token(3, 7, Literal.STR.label, r'"Print a slash n - \\n.\n"'),
            Token(3, 33, Symbol.CLOSE_PARENTHESIS.label, None),
            Token(3, 34, Symbol.SEMICOLON.label, None),
            # line 4
            Token(4, 1, Terminal.TERMINAL.label, None),
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
        self.thenReturnTokens([
            # line 1
            Token(1, 1, Identifier.IDENTIFIER.label, r'count'),
            Token(1, 7, Operator.ASSIGN.label, None),
            Token(1, 9, Literal.INT.label, r'1'),
            Token(1, 10, Symbol.SEMICOLON.label, None),
            # line 2
            Token(2, 1, Keyword.WHILE.label, None),
            Token(2, 7, Symbol.OPEN_PARENTHESIS.label, None),
            Token(2, 8, Identifier.IDENTIFIER.label, r'count'),
            Token(2, 14, Operator.LESS.label, None),
            Token(2, 16, Literal.INT.label, r'10'),
            Token(2, 18, Symbol.CLOSE_PARENTHESIS.label, None),
            Token(2, 20, Symbol.OPEN_BRACE.label, None),
            # line 3
            Token(3, 5, Keyword.PRINT_STRING.label, None),
            Token(3, 10, Symbol.OPEN_PARENTHESIS.label, None),
            Token(3, 11, Literal.STR.label, r'"count is: "'),
            Token(3, 23, Symbol.COMMA.label, None),
            Token(3, 25, Identifier.IDENTIFIER.label, r'count'),
            Token(3, 30, Symbol.COMMA.label, None),
            Token(3, 32, Literal.STR.label, r'"\n"'),
            Token(3, 36, Symbol.CLOSE_PARENTHESIS.label, None),
            Token(3, 37, Symbol.SEMICOLON.label, None),
            # line 4
            Token(4, 5, Identifier.IDENTIFIER.label, r'count'),
            Token(4, 11, Operator.ASSIGN.label, None),
            Token(4, 13, Identifier.IDENTIFIER.label, r'count'),
            Token(4, 19, Operator.ADD.label, None),
            Token(4, 21, Literal.INT.label, r'1'),
            Token(4, 22, Symbol.SEMICOLON.label, None),
            # line 5
            Token(5, 1, Symbol.CLOSE_BRACE.label, None),
            # line 6
            Token(6, 1, Terminal.TERMINAL.label, None),
        ])
