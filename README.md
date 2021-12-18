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
- https://docs.python.org/3/library/re.html#writing-a-tokenizer
