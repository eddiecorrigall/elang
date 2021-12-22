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

# Deactivate virtual environment
deactivate
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
