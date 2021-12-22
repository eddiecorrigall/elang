import sys

from lexer import Lexer
from core.parser import Parser

'''
Example:

ipython -i run.py 'abc = 123;'
'''

if __name__ == '__main__':
    name, program = sys.argv

    lex = Lexer()
    tokens = list(lex(program))
    print('TOKENS %s' % tokens)

    parser = Parser()
    ast = parser(tokens)
    print('AST %s' % ast.as_json())
