from core.tokens import Token, TokenType
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
            Token(1, 1, TokenType.KEYWORD_IF.name, None),
            Token(1, 4, TokenType.SYMBOL_OPEN_PARENTHESIS.name, None),
            Token(1, 6, TokenType.IDENTIFIER.name, 'p'),
            Token(1, 8, TokenType.SYMBOL_CLOSE_PARENTHESIS.name, None),
            Token(1, 10, TokenType.SYMBOL_OPEN_BRACE.name, None),
            # line 2 - comment
            # line 3
            Token(3, 4, TokenType.KEYWORD_PRINT_STRING.name, None),
            Token(3, 10, TokenType.SYMBOL_OPEN_PARENTHESIS.name, None),
            Token(3, 12, TokenType.IDENTIFIER.name, 'n'),
            Token(3, 14, TokenType.SYMBOL_COMMA.name, None),
            Token(3, 16, TokenType.LITERAL_STR.name, ' '),
            Token(3, 20, TokenType.SYMBOL_CLOSE_PARENTHESIS.name, None),
            Token(3, 22, TokenType.SYMBOL_SEMICOLON.name, None),
            # line 4
            Token(4, 4, TokenType.IDENTIFIER.name, 'count'),
            Token(4, 10, TokenType.OPERATOR_ASSIGN.name, None),
            Token(4, 12, TokenType.IDENTIFIER.name, 'count'),
            Token(4, 18, TokenType.OPERATOR_ADD.name, None),
            Token(4, 20, TokenType.LITERAL_INT.name, '1'),
            Token(4, 22, TokenType.SYMBOL_SEMICOLON.name, None),
            # line 5
            Token(5, 1, TokenType.SYMBOL_CLOSE_BRACE.name, None),
            # line 6
            Token(6, 1, TokenType.TERMINAL.name, None),
        ])

    def test_without_whitespace(self):
        self.givenProgramLine(r'if(p){print(n," ");count=count+1;}')
        self.whenLex()
        self.thenReturnTokens([
            Token(1, 1, TokenType.KEYWORD_IF.name, None),
            Token(1, 3, TokenType.SYMBOL_OPEN_PARENTHESIS.name, None),
            Token(1, 4, TokenType.IDENTIFIER.name, 'p'),
            Token(1, 5, TokenType.SYMBOL_CLOSE_PARENTHESIS.name, None),
            Token(1, 6, TokenType.SYMBOL_OPEN_BRACE.name, None),
            Token(1, 7, TokenType.KEYWORD_PRINT_STRING.name, None),
            Token(1, 12, TokenType.SYMBOL_OPEN_PARENTHESIS.name, None),
            Token(1, 13, TokenType.IDENTIFIER.name, 'n'),
            Token(1, 14, TokenType.SYMBOL_COMMA.name, None),
            Token(1, 15, TokenType.LITERAL_STR.name, ' '),
            Token(1, 18, TokenType.SYMBOL_CLOSE_PARENTHESIS.name, None),
            Token(1, 19, TokenType.SYMBOL_SEMICOLON.name, None),
            Token(1, 20, TokenType.IDENTIFIER.name, 'count'),
            Token(1, 25, TokenType.OPERATOR_ASSIGN.name, None),
            Token(1, 26, TokenType.IDENTIFIER.name, 'count'),
            Token(1, 31, TokenType.OPERATOR_ADD.name, None),
            Token(1, 32, TokenType.LITERAL_INT.name, '1'),
            Token(1, 33, TokenType.SYMBOL_SEMICOLON.name, None),
            Token(1, 34, TokenType.SYMBOL_CLOSE_BRACE.name, None),

            Token(2, 1, TokenType.TERMINAL.name, None),
        ])

    def test_case_1_without_multiline_comment(self):
        self.givenProgramLines([
            r'print("Hello, World!\n");',
        ])
        self.whenLex()
        self.thenReturnTokens([
            Token(1, 1, TokenType.KEYWORD_PRINT_STRING.name, None),
            Token(1, 6, TokenType.SYMBOL_OPEN_PARENTHESIS.name, None),
            Token(1, 7, TokenType.LITERAL_STR.name, 'Hello, World!\\n'),
            Token(1, 24, TokenType.SYMBOL_CLOSE_PARENTHESIS.name, None),
            Token(1, 25, TokenType.SYMBOL_SEMICOLON.name, None),

            Token(2, 1, TokenType.TERMINAL.name, None),
        ])

    def test_case_phoenix_number_without_multiline_comment(self):
        # Test Case 2
        self.givenProgramLines([
            r'phoenix_number = 142857;',
            r'print(phoenix_number, "\n");',
        ])
        self.whenLex()
        self.thenReturnTokens([
            Token(1, 1, TokenType.IDENTIFIER.name, 'phoenix_number'),
            Token(1, 16, TokenType.OPERATOR_ASSIGN.name, None),
            Token(1, 18, TokenType.LITERAL_INT.name, '142857'),
            Token(1, 24, TokenType.SYMBOL_SEMICOLON.name, None),

            Token(2, 1, TokenType.KEYWORD_PRINT_STRING.name, None),
            Token(2, 6, TokenType.SYMBOL_OPEN_PARENTHESIS.name, None),
            Token(2, 7, TokenType.IDENTIFIER.name, 'phoenix_number'),
            Token(2, 21, TokenType.SYMBOL_COMMA.name, None),
            Token(2, 23, TokenType.LITERAL_STR.name, '\\n'),
            Token(2, 27, TokenType.SYMBOL_CLOSE_PARENTHESIS.name, None),
            Token(2, 28, TokenType.SYMBOL_SEMICOLON.name, None),

            Token(3, 1, TokenType.TERMINAL.name, None),
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
            Token(1, 1, TokenType.KEYWORD_PRINT_STRING.name, None),
            Token(1, 6, TokenType.SYMBOL_OPEN_PARENTHESIS.name, None),
            Token(1, 7, TokenType.LITERAL_INT.name, '42'),
            Token(1, 9, TokenType.SYMBOL_CLOSE_PARENTHESIS.name, None),
            Token(1, 10, TokenType.SYMBOL_SEMICOLON.name, None),
            # line 2
            Token(2, 1, TokenType.KEYWORD_PRINT_STRING.name, None),
            Token(2, 6, TokenType.SYMBOL_OPEN_PARENTHESIS.name, None),
            Token(2, 7, TokenType.LITERAL_STR.name, r'\nHello World\nGood Bye\nok\n'),
            Token(2, 38, TokenType.SYMBOL_CLOSE_PARENTHESIS.name, None),
            Token(2, 39, TokenType.SYMBOL_SEMICOLON.name, None),
            # line 3
            Token(3, 1, TokenType.KEYWORD_PRINT_STRING.name, None),
            Token(3, 6, TokenType.SYMBOL_OPEN_PARENTHESIS.name, None),
            Token(3, 7, TokenType.LITERAL_STR.name, r'Print a slash n - \\n.\n'),
            Token(3, 33, TokenType.SYMBOL_CLOSE_PARENTHESIS.name, None),
            Token(3, 34, TokenType.SYMBOL_SEMICOLON.name, None),
            # line 4
            Token(4, 1, TokenType.TERMINAL.name, None),
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
            Token(1, 1, TokenType.IDENTIFIER.name, r'count'),
            Token(1, 7, TokenType.OPERATOR_ASSIGN.name, None),
            Token(1, 9, TokenType.LITERAL_INT.name, r'1'),
            Token(1, 10, TokenType.SYMBOL_SEMICOLON.name, None),
            # line 2
            Token(2, 1, TokenType.KEYWORD_WHILE.name, None),
            Token(2, 7, TokenType.SYMBOL_OPEN_PARENTHESIS.name, None),
            Token(2, 8, TokenType.IDENTIFIER.name, r'count'),
            Token(2, 14, TokenType.OPERATOR_LESS.name, None),
            Token(2, 16, TokenType.LITERAL_INT.name, r'10'),
            Token(2, 18, TokenType.SYMBOL_CLOSE_PARENTHESIS.name, None),
            Token(2, 20, TokenType.SYMBOL_OPEN_BRACE.name, None),
            # line 3
            Token(3, 5, TokenType.KEYWORD_PRINT_STRING.name, None),
            Token(3, 10, TokenType.SYMBOL_OPEN_PARENTHESIS.name, None),
            Token(3, 11, TokenType.LITERAL_STR.name, r'count is: '),
            Token(3, 23, TokenType.SYMBOL_COMMA.name, None),
            Token(3, 25, TokenType.IDENTIFIER.name, r'count'),
            Token(3, 30, TokenType.SYMBOL_COMMA.name, None),
            Token(3, 32, TokenType.LITERAL_STR.name, r'\n'),
            Token(3, 36, TokenType.SYMBOL_CLOSE_PARENTHESIS.name, None),
            Token(3, 37, TokenType.SYMBOL_SEMICOLON.name, None),
            # line 4
            Token(4, 5, TokenType.IDENTIFIER.name, r'count'),
            Token(4, 11, TokenType.OPERATOR_ASSIGN.name, None),
            Token(4, 13, TokenType.IDENTIFIER.name, r'count'),
            Token(4, 19, TokenType.OPERATOR_ADD.name, None),
            Token(4, 21, TokenType.LITERAL_INT.name, r'1'),
            Token(4, 22, TokenType.SYMBOL_SEMICOLON.name, None),
            # line 5
            Token(5, 1, TokenType.SYMBOL_CLOSE_BRACE.name, None),
            # line 6
            Token(6, 1, TokenType.TERMINAL.name, None),
        ])
