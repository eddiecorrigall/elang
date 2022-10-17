from tests.walker_test_base import WalkerTestBase


class TestWalker(WalkerTestBase):
    def test_empty(self):
        # ERROR
        self.givenProgramLines(["putc('')"])
        self.whenRunProgramLines()

    def test_single_character(self):
        self.givenProgramLines(["putc('x');"])
        self.whenRunProgramLines()
        self.thenStandardOutputEquals('x')
    
    def test_integer(self):
        self.givenProgramLines(["putc(120);"])
        self.whenRunProgramLines()
        self.thenStandardOutputEquals('x')
