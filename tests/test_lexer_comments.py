from tests.lexer_test_base import LexerTestBase


class TestComments(LexerTestBase):
    def test_line_comment(self):
        self.givenProgramLine('//print("Hello world")')
        self.whenLexParseLine()
        self.thenReturnNothing()

    '''
    def test_multiline_comment(self):
        self.givenProgramLine('/* while(1) { print("Forever"); } */')
        self.whenLexParseLine()
        self.thenReturnEmptyLexerOutput()
    '''
