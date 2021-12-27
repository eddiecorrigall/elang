from typing import Iterable


def readlines(file, EOF: str = None) -> Iterable[str]:
    EOF = str() if EOF is None else EOF
    while True:
        line = file.readline()
        if line == EOF:
            break
        else:
            # exclude the newline
            yield line[:-1]
