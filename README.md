# sql-loader-python

[![Build, Test, and Release](https://github.com/obstreperous-ai/sql-loader-python/actions/workflows/build-test-release.yml/badge.svg)](https://github.com/obstreperous-ai/sql-loader-python/actions/workflows/build-test-release.yml)
[![codecov](https://codecov.io/gh/obstreperous-ai/sql-loader-python/branch/main/graph/badge.svg)](https://codecov.io/gh/obstreperous-ai/sql-loader-python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lean CLI utility in Python using Click and SQLAlchemy to run SQL scripts in minimal environments (e.g., Python containers in Kubernetes).

## Features

- 🚀 **Minimal and Fast**: Designed for minimal container environments
- 🔌 **Database Agnostic**: Works with any database supported by SQLAlchemy
- 🧪 **Test-First**: High test coverage with pytest
- 📦 **Multiple Distribution Formats**: PyPI wheel and standalone binaries
- 🔧 **Simple CLI**: Built with Click for intuitive command-line interface
- 🐳 **Container-Friendly**: Supports environment variables for configuration

## Installation

### From PyPI (Wheel)

```bash
pip install sql-loader
```

### From Binary Release

Download the latest binary for your platform from the [releases page](https://github.com/obstreperous-ai/sql-loader-python/releases):

- **Linux**: `sql-loader-linux`
- **macOS**: `sql-loader-macos`
- **Windows**: `sql-loader-windows.exe`

```bash
# Linux/macOS
chmod +x sql-loader-*
./sql-loader-* --help

# Windows
sql-loader-windows.exe --help
```

### From Source

```bash
git clone https://github.com/obstreperous-ai/sql-loader-python.git
cd sql-loader-python
pip install -e '.[dev]'
```

## Quick Start

### Basic Usage

```bash
# Run a SQL file
sql-loader run -c sqlite:///mydb.db schema.sql

# Run multiple SQL files in order
sql-loader run -c sqlite:///mydb.db schema.sql data.sql migrations/*.sql

# Test database connection
sql-loader test-connection -c sqlite:///mydb.db

# Enable verbose output
sql-loader run -c sqlite:///mydb.db -v schema.sql
```

### Using Environment Variables

```bash
# Set connection string via environment variable
export SQL_LOADER_CONNECTION="sqlite:///mydb.db"
sql-loader run schema.sql data.sql

# Or inline
SQL_LOADER_CONNECTION="postgresql://user:pass@localhost/db" sql-loader run migrations/*.sql
```

### Database Connection Strings

sql-loader supports any database that SQLAlchemy supports:

```bash
# SQLite (file-based)
sql-loader run -c "sqlite:///path/to/database.db" schema.sql

# SQLite (in-memory)
sql-loader run -c "sqlite:///:memory:" test.sql

# PostgreSQL
sql-loader run -c "postgresql://user:password@localhost:5432/dbname" schema.sql

# MySQL
sql-loader run -c "mysql+pymysql://user:password@localhost:3306/dbname" schema.sql

# SQL Server
sql-loader run -c "mssql+pyodbc://user:password@localhost/dbname?driver=ODBC+Driver+17+for+SQL+Server" schema.sql
```

## Use Cases

### Kubernetes Init Containers

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-db-init
spec:
  initContainers:
  - name: db-init
    image: python:3.12-slim
    command: ["/bin/sh", "-c"]
    args:
      - |
        pip install sql-loader
        sql-loader run /sql/*.sql
    env:
    - name: SQL_LOADER_CONNECTION
      value: "postgresql://user:pass@postgres:5432/appdb"
    volumeMounts:
    - name: sql-scripts
      mountPath: /sql
  containers:
  - name: app
    image: myapp:latest
  volumes:
  - name: sql-scripts
    configMap:
      name: db-migrations
```

### Docker Compose

```yaml
version: '3.8'
services:
  db-init:
    image: python:3.12-slim
    command: >
      sh -c "pip install sql-loader &&
             sql-loader run /sql/*.sql"
    environment:
      SQL_LOADER_CONNECTION: postgresql://user:pass@db:5432/appdb
    volumes:
      - ./sql:/sql
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: appdb
```

### CI/CD Pipelines

```yaml
# GitHub Actions example
- name: Apply database migrations
  run: |
    pip install sql-loader
    sql-loader run migrations/*.sql
  env:
    SQL_LOADER_CONNECTION: ${{ secrets.DB_CONNECTION_STRING }}
```

## Development

### Prerequisites

- Python 3.8+
- [Task](https://taskfile.dev/) (optional, for using Taskfile commands)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/obstreperous-ai/sql-loader-python.git
cd sql-loader-python

# Create virtual environment and install dependencies
task venv
# Or manually:
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e '.[dev]'
```

### Running Tests

```bash
# Run tests with coverage
task test
# Or manually:
pytest

# Run tests with HTML coverage report
task test-cov
# Or manually:
pytest --cov=sql_loader --cov-report=html --cov-report=term
```

### Code Quality

```bash
# Format code
task format
# Or manually:
black src tests
isort src tests

# Lint code
task lint
# Or manually:
ruff check src tests

# Type check
task typecheck
# Or manually:
mypy src
```

### Building

```bash
# Build wheel distribution
task wheel
# Or manually:
python -m build

# Build standalone binary
task package
# Or manually:
pyinstaller --onefile --name sql-loader src/sql_loader/cli.py
```

### Available Tasks

Run `task --list` to see all available tasks:

```
task: Available tasks for this project:
* clean:        Clean build artifacts
* clean-all:    Clean everything including venv
* format:       Format code with black and isort
* lint:         Lint code with ruff
* package:      Build binary with PyInstaller
* test:         Run tests with pytest
* test-cov:     Run tests with coverage report
* typecheck:    Type check with mypy
* venv:         Create virtual environment and install dependencies
* wheel:        Build wheel distribution
```

## Project Structure

```
sql-loader-python/
├── .devcontainer/          # VS Code dev container configuration
│   └── devcontainer.json
├── .github/
│   ├── dependabot.yml      # Dependabot configuration
│   └── workflows/          # GitHub Actions workflows
│       └── build-test-release.yml
├── src/
│   └── sql_loader/         # Main package
│       ├── __init__.py
│       ├── cli.py          # Click CLI commands
│       └── executor.py     # SQL execution logic
├── tests/
│   ├── fixtures/           # Test SQL scripts
│   ├── test_cli.py
│   └── test_executor.py
├── .gitignore
├── LICENSE                 # MIT License
├── pyproject.toml         # Project metadata and dependencies
├── README.md
└── Taskfile.yml           # Task automation
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the test-first approach
4. Ensure all tests pass (`task test`)
5. Format and lint your code (`task format && task lint`)
6. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## GitHub Copilot Instructions

This project includes custom GitHub Copilot instructions to help you work effectively with the codebase. See [.github/copilot-instructions.md](.github/copilot-instructions.md) for detailed guidance on:

- Project principles (minimal, test-first, quality-focused)
- Technology stack (Python, Click, SQLAlchemy, pytest)
- Coding standards and best practices
- Testing requirements
- What to always do and never do
- Security considerations

When working on this project, Copilot will automatically follow these guidelines to ensure code quality and consistency.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI
- Powered by [SQLAlchemy](https://www.sqlalchemy.org/) for database operations
- Tested with [pytest](https://pytest.org/)
