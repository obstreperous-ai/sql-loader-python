"""Tests for sql_loader.executor module."""

from pathlib import Path

import pytest
from sqlalchemy import create_engine, text

from sql_loader.executor import SQLExecutor


@pytest.fixture
def in_memory_db() -> str:
    """Provide an in-memory SQLite database connection string."""
    return "sqlite:///:memory:"


@pytest.fixture
def executor(in_memory_db: str) -> SQLExecutor:
    """Provide a SQLExecutor instance with in-memory database."""
    return SQLExecutor(in_memory_db)


@pytest.fixture
def fixtures_dir() -> Path:
    """Provide path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


def test_executor_initialization(in_memory_db: str) -> None:
    """Test SQLExecutor initialization."""
    executor = SQLExecutor(in_memory_db)
    assert executor.engine is not None
    executor.close()


def test_execute_sql_simple(executor: SQLExecutor) -> None:
    """Test executing a simple SQL statement."""
    sql = "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    statements_executed = executor.execute_sql(sql)
    assert statements_executed == 1

    # Verify table was created
    with executor.engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='test'"
            )
        )
        assert result.fetchone() is not None


def test_execute_sql_multiple_statements(executor: SQLExecutor) -> None:
    """Test executing multiple SQL statements."""
    sql = """
    CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT);
    INSERT INTO test (id, name) VALUES (1, 'Alice');
    INSERT INTO test (id, name) VALUES (2, 'Bob');
    """
    statements_executed = executor.execute_sql(sql)
    assert statements_executed == 3

    # Verify data was inserted
    with executor.engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM test"))
        count = result.scalar()
        assert count == 2


def test_execute_file(executor: SQLExecutor, fixtures_dir: Path) -> None:
    """Test executing SQL from a file."""
    create_table_file = fixtures_dir / "create_table.sql"
    statements_executed = executor.execute_file(create_table_file)
    assert statements_executed == 1

    # Verify table was created
    with executor.engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
            )
        )
        assert result.fetchone() is not None


def test_execute_files(executor: SQLExecutor, fixtures_dir: Path) -> None:
    """Test executing multiple SQL files."""
    files = [
        fixtures_dir / "create_table.sql",
        fixtures_dir / "insert_data.sql",
    ]
    total_statements = executor.execute_files(files)
    assert total_statements == 4  # 1 CREATE + 3 INSERTs

    # Verify data was inserted
    with executor.engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        assert count == 3


def test_execute_file_not_found(executor: SQLExecutor) -> None:
    """Test executing a non-existent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        executor.execute_file(Path("/nonexistent/file.sql"))


def test_execute_sql_invalid(executor: SQLExecutor, fixtures_dir: Path) -> None:
    """Test executing invalid SQL raises an exception."""
    invalid_file = fixtures_dir / "invalid.sql"
    with pytest.raises(Exception):
        executor.execute_file(invalid_file)


def test_split_statements(executor: SQLExecutor) -> None:
    """Test statement splitting logic."""
    sql = "SELECT 1; SELECT 2; SELECT 3;"
    statements = executor._split_statements(sql)
    assert len(statements) == 3
    assert statements[0] == "SELECT 1"
    assert statements[1] == "SELECT 2"
    assert statements[2] == "SELECT 3"


def test_split_statements_with_empty(executor: SQLExecutor) -> None:
    """Test statement splitting handles empty statements."""
    sql = "SELECT 1;; SELECT 2;"
    statements = executor._split_statements(sql)
    assert len(statements) == 2
    assert statements[0] == "SELECT 1"
    assert statements[1] == "SELECT 2"
