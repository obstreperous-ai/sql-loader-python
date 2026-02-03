"""SQL execution logic using SQLAlchemy."""

from pathlib import Path
from typing import List

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


class SQLExecutor:
    """Executes SQL scripts using SQLAlchemy."""

    def __init__(self, connection_string: str) -> None:
        """Initialize SQLExecutor with a database connection string.

        Args:
            connection_string: SQLAlchemy database URL
        """
        self.engine: Engine = create_engine(connection_string)

    def execute_file(self, filepath: Path) -> int:
        """Execute a SQL file.

        Args:
            filepath: Path to the SQL file to execute

        Returns:
            Number of statements executed

        Raises:
            FileNotFoundError: If the SQL file doesn't exist
            Exception: For any database errors
        """
        if not filepath.exists():
            raise FileNotFoundError(f"SQL file not found: {filepath}")

        sql_content = filepath.read_text()
        return self.execute_sql(sql_content)

    def execute_sql(self, sql: str) -> int:
        """Execute SQL statements.

        Args:
            sql: SQL content to execute

        Returns:
            Number of statements executed

        Raises:
            Exception: For any database errors
        """
        statements = self._split_statements(sql)
        statements_executed = 0

        with self.engine.connect() as conn:
            with conn.begin():
                for statement in statements:
                    if statement.strip():
                        conn.execute(text(statement))
                        statements_executed += 1

        return statements_executed

    def execute_files(self, filepaths: List[Path]) -> int:
        """Execute multiple SQL files in order.

        Args:
            filepaths: List of paths to SQL files

        Returns:
            Total number of statements executed across all files
        """
        total_statements = 0
        for filepath in filepaths:
            total_statements += self.execute_file(filepath)
        return total_statements

    def _split_statements(self, sql: str) -> List[str]:
        """Split SQL content into individual statements.

        Args:
            sql: SQL content

        Returns:
            List of SQL statements
        """
        # Simple split by semicolon for now
        # This could be enhanced for more complex cases
        statements = [s.strip() for s in sql.split(";")]
        return [s for s in statements if s]

    def close(self) -> None:
        """Close the database connection."""
        self.engine.dispose()
