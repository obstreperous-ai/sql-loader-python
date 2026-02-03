# GitHub Copilot Instructions for sql-loader-python

## Project Overview

This is a **lean CLI utility** written in Python that uses Click and SQLAlchemy to run SQL scripts in minimal environments (e.g., Python containers in Kubernetes). The project focuses on doing **one job well** with a **test-first** approach and **high quality** standards.

## Technology Stack

- **Python 3.8+** - Core language
- **Click** - Command-line interface framework
- **SQLAlchemy** - Database abstraction and ORM
- **SQLite** - Used for embedded tests (via SQLAlchemy)
- **pytest** - Testing framework (test-first approach)

## Core Principles

1. **Minimal and Lean**: Keep the codebase small, focused, and efficient
2. **Test-First Development**: Always write tests before implementing features
3. **Single Responsibility**: The tool does one job - running SQL scripts efficiently
4. **Quality Over Features**: Prioritize code quality, reliability, and maintainability
5. **Container-Friendly**: Designed to run in minimal environments (K8s, Docker, etc.)

## Build, Test, and Validation

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov

# Run specific test file
pytest tests/test_<module>.py
```

### Code Quality
```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Lint with ruff (or flake8)
ruff check .

# Type checking with mypy
mypy src/
```

### Building and Installation
```bash
# Install in development mode
pip install -e .

# Build distribution
python -m build
```

## Coding Standards

### Python Style
- Follow **PEP 8** style guidelines
- Use **type hints** for all function signatures
- Maximum line length: **88 characters** (Black default)
- Use **f-strings** for string formatting
- Prefer **pathlib** over os.path for file operations

### Click CLI Best Practices
- Use Click's decorators for clean command definitions
- Provide clear help text for all commands and options
- Use Click's built-in types (Path, Choice, etc.) for validation
- Group related commands using Click groups when applicable

### SQLAlchemy Best Practices
- Use SQLAlchemy Core for SQL script execution (not ORM for this use case)
- Always use connection pooling appropriately for the minimal environment
- Properly handle database connections and transactions
- Use parameterized queries to prevent SQL injection
- Keep database connection configuration flexible (connection strings via CLI or env vars)

### Testing Requirements
- **Test-First**: Write tests before implementation
- Use **pytest** for all tests
- Use **SQLite in-memory** database for unit tests
- Aim for **>90% code coverage**
- Test both success and error cases
- Mock external dependencies when appropriate
- Test CLI commands using Click's testing utilities (`CliRunner`)

### Code Organization
```
sql-loader-python/
├── src/
│   └── sql_loader/        # Main package
│       ├── __init__.py
│       ├── cli.py         # Click CLI commands
│       ├── executor.py    # SQL execution logic
│       └── utils.py       # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_executor.py
│   └── fixtures/          # Test SQL scripts
├── pyproject.toml         # Project metadata and dependencies
└── README.md
```

## What to ALWAYS Do

1. **Write tests first** before implementing any feature
2. **Run tests** after any code change to ensure nothing breaks
3. **Use type hints** for all function parameters and return values
4. **Handle errors gracefully** with informative error messages
5. **Keep dependencies minimal** - only add libraries when absolutely necessary
6. **Document public APIs** with clear docstrings
7. **Validate inputs** at the CLI boundary using Click's built-in validators
8. **Use context managers** for database connections and file operations
9. **Log important operations** but keep logging lean
10. **Make it container-friendly** - support environment variables, graceful shutdowns

## What to NEVER Do

1. **Never add unnecessary dependencies** - keep the tool lean
2. **Never commit secrets or credentials** to version control
3. **Never use `SELECT *`** in production code - be explicit
4. **Never ignore error handling** - every failure case should be handled
5. **Never skip tests** - test coverage must remain high
6. **Never use `os.system()` or shell=True** - security risk
7. **Never hardcode database credentials** - use environment variables or CLI args
8. **Never modify `.gitignore` to include generated files** - keep it clean
9. **Never add features without tests** - test-first approach is mandatory
10. **Never optimize prematurely** - clarity and correctness first

## Error Handling

- Use Click's `ClickException` for CLI-related errors
- Use SQLAlchemy exceptions for database errors
- Provide helpful error messages with context
- Return appropriate exit codes (0 for success, non-zero for errors)
- Log errors with sufficient detail for debugging

## Security Considerations

- **Never log sensitive data** (passwords, credentials, PII)
- **Always use parameterized queries** to prevent SQL injection
- **Validate all inputs** from CLI and environment variables
- **Use secure defaults** for database connections
- **Follow principle of least privilege** for database users

## Documentation Standards

- Keep README.md up-to-date with installation and usage instructions
- Use clear, concise docstrings for all public functions and classes
- Include examples in docstrings where helpful
- Document environment variables and CLI arguments
- Maintain a CHANGELOG.md for version history

## Performance Considerations

- Keep startup time fast (minimal imports, lazy loading)
- Use connection pooling wisely for the target environment
- Stream large result sets instead of loading into memory
- Profile before optimizing - measure, don't guess

## Commit Message Format

Use conventional commits format:
- `feat:` - New feature
- `fix:` - Bug fix
- `test:` - Test changes
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks
