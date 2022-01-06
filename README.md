elang
=====

Toy programming language written by yours truely.
- Purely Python with standard library
- Parser: recursive descent
- Expressions in polish notation
- Abstract Syntax Tree Walker
- Literals: integer, character, string, array, map

![Mandlebrot Demo](./demo.gif)

## Use CLI

```bash
# Create virtual environment
python3 -m venv venv

# Activate virual environment
source venv/bin/activate

# Install depedencies
pip3 install -r requirements.txt

# Add parent working directory to PATH
export PATH="$(pwd):$PATH"

# List help contents for elang
elang --help

# Run test suit
elang test

# Deactivate virtual environment
deactivate
```

### Example

Produce Abstract Syntax Tree as standard output in JSON format.

```bash
$ echo 'print("Hello world");' | elang lex | elang parse --format json
{
  "type": "SEQUENCE",
  "left": {
    "type": "PRINT_STRING",
    "left": {
      "type": "STR",
      "value": "\"Hello world\""
    }
  }
}
```

Run program.

```bash
$ echo 'print("Hello world");' | elang run
Hello world
```

## Python API

```python
lex = Lexer()
tokens = Lexer.from_token_file(file)
tokens = lex.from_program_file(file)
tokens = lex.from_program_lines(lines)
tokens = lex(program_line)
line_generator = Lexer.as_lines(tokens)
```

```python
parse = Parser()
ast = parse(tokens)
ast_dict = ast.as_dict()
json_str = ast.as_json()
line_generator = ast.as_lines()
```

```python
walk = Walker()
walk(ast)
```

## Run Tests

```bash
export PYTHONPATH="$(pwd)"

# Run all tests
python3 -m unittest discover --verbose --start-directory tests/

# Run specific test suite
python3 -m unittest --verbose tests/test_lexer_tokens.py

# Run specific test
python3 -m unittest --verbose tests.test_lexer_integer_literal.TestIntegerLiteral.test_positive_integers
```

## References
- https://rosettacode.org/wiki/Compiler/lexical_analyzer
- https://en.wikibooks.org/wiki/Compiler_Construction/Syntax_Analysis
- https://docs.python.org/3/library/re.html#writing-a-tokenizer
- https://en.wikipedia.org/wiki/Operator-precedence_parser

## TODO

- [ ] boolean
- [ ] implement static array
  - [x] assign single value
  - [x] assign row
  - [ ] binary operation (eg multiply) row
  - [x] print
  - [x] access single value
  - [x] access row
- [ ] implement hash table
  - [x] default value
  - [x] assign single value
  - [x] access single value
  - [x] print
  - [ ] access keys
  - [ ] access values
- [ ] loop
  - [x] while with condition and statement
  - [ ] halt loop
  - [ ] continue loop
- [ ] variables
  - [x] int
  - [x] char
  - [x] string
  - [x] array
  - [ ] constants / immutable value
  - [ ] typing / immutable type
- [x] print statement with multiple arguments
- [x] handle print string escape characters
- [x] assert statement throws error and causes walker to exist with non-zero status code

- test `putc('');` => error
- test `putc('x');` => 'x'
- test `putc(120);` => 'x'
- test `print("");` => ''
- test `print("x");` => 'x'
- test `print('x');` => '120'
- test `print(120);` => '120'
- test `print(["Hello", " ", "world", ]);` => 'Hello world'
- test `print([["Hello", " ", "wolrd",]]);` => 'Hello world'
