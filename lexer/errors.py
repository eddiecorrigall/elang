class LexerError(Exception):
    pass


class LexerSyntaxError(LexerError):
    pass


class LexerNotImplemented(LexerError):
    pass
