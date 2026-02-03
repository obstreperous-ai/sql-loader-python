"""Tests for sql_loader.cli module."""

from pathlib import Path

from click.testing import CliRunner

from sql_loader.cli import cli


def test_cli_version() -> None:
    """Test CLI version command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_cli_help() -> None:
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "sql-loader" in result.output


def test_run_command_no_files() -> None:
    """Test run command with no files specified."""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["run", "-c", "sqlite:///:memory:"]
    )
    assert result.exit_code == 1
    assert "No SQL files specified" in result.output


def test_run_command_with_files() -> None:
    """Test run command with SQL files."""
    runner = CliRunner()
    fixtures_dir = Path(__file__).parent / "fixtures"

    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "run",
                "-c",
                "sqlite:///test.db",
                str(fixtures_dir / "create_table.sql"),
                str(fixtures_dir / "insert_data.sql"),
            ],
        )
        assert result.exit_code == 0
        assert "Successfully executed" in result.output
        assert "4 statement(s)" in result.output
        assert "2 file(s)" in result.output


def test_run_command_verbose() -> None:
    """Test run command with verbose output."""
    runner = CliRunner()
    fixtures_dir = Path(__file__).parent / "fixtures"

    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "run",
                "-c",
                "sqlite:///test.db",
                "-v",
                str(fixtures_dir / "create_table.sql"),
            ],
        )
        assert result.exit_code == 0
        assert "Connection:" in result.output
        assert "Files to execute:" in result.output
        assert "Executing:" in result.output


def test_run_command_with_env_var() -> None:
    """Test run command using environment variable for connection."""
    runner = CliRunner()
    fixtures_dir = Path(__file__).parent / "fixtures"

    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            ["run", str(fixtures_dir / "create_table.sql")],
            env={"SQL_LOADER_CONNECTION": "sqlite:///test.db"},
        )
        assert result.exit_code == 0
        assert "Successfully executed" in result.output


def test_run_command_invalid_sql() -> None:
    """Test run command with invalid SQL."""
    runner = CliRunner()
    fixtures_dir = Path(__file__).parent / "fixtures"

    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "run",
                "-c",
                "sqlite:///test.db",
                str(fixtures_dir / "invalid.sql"),
            ],
        )
        assert result.exit_code == 1
        assert "Database error:" in result.output


def test_test_connection_success() -> None:
    """Test test-connection command with valid connection."""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["test-connection", "-c", "sqlite:///:memory:"]
    )
    assert result.exit_code == 0
    assert "Connection successful" in result.output


def test_test_connection_failure() -> None:
    """Test test-connection command with invalid connection."""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["test-connection", "-c", "invalid://connection"]
    )
    assert result.exit_code == 1
    assert "Connection failed" in result.output


def test_test_connection_with_env_var() -> None:
    """Test test-connection command using environment variable."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["test-connection"],
        env={"SQL_LOADER_CONNECTION": "sqlite:///:memory:"},
    )
    assert result.exit_code == 0
    assert "Connection successful" in result.output
