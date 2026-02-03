"""CLI interface for sql-loader using Click."""

import sys
from pathlib import Path
from typing import List

import click

from sql_loader import __version__
from sql_loader.executor import SQLExecutor


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """sql-loader: A lean CLI utility to run SQL scripts in minimal environments."""
    pass


@cli.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option(
    "-c",
    "--connection",
    envvar="SQL_LOADER_CONNECTION",
    required=True,
    help="Database connection string (or set SQL_LOADER_CONNECTION env var)",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
def run(files: tuple, connection: str, verbose: bool) -> None:
    """Execute SQL files against a database.

    FILES: One or more SQL files to execute

    Examples:
        sql-loader run -c sqlite:///test.db schema.sql data.sql
        SQL_LOADER_CONNECTION=postgresql://user:pass@localhost/db \\
            sql-loader run migrations/*.sql
    """
    if not files:
        click.echo("Error: No SQL files specified", err=True)
        sys.exit(1)

    file_list: List[Path] = list(files)

    if verbose:
        click.echo(f"Connection: {connection}")
        click.echo(f"Files to execute: {len(file_list)}")
        for f in file_list:
            click.echo(f"  - {f}")

    try:
        executor = SQLExecutor(connection)
        total_statements = 0

        for filepath in file_list:
            if verbose:
                click.echo(f"\nExecuting: {filepath}")

            statements = executor.execute_file(filepath)
            total_statements += statements

            if verbose:
                click.echo(f"  Executed {statements} statement(s)")

        executor.close()

        click.echo(
            f"\n✓ Successfully executed {total_statements} statement(s) "
            f"from {len(file_list)} file(s)",
            color=True,
        )

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Database error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "-c",
    "--connection",
    envvar="SQL_LOADER_CONNECTION",
    required=True,
    help="Database connection string (or set SQL_LOADER_CONNECTION env var)",
)
def test_connection(connection: str) -> None:
    """Test database connection.

    Examples:
        sql-loader test-connection -c sqlite:///:memory:
        sql-loader test-connection -c postgresql://user:pass@localhost/db
    """
    try:
        executor = SQLExecutor(connection)
        # Try a simple query
        executor.execute_sql("SELECT 1")
        executor.close()
        click.echo("✓ Connection successful", color=True)
    except Exception as e:
        click.echo(f"✗ Connection failed: {e}", err=True, color=True)
        sys.exit(1)


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
