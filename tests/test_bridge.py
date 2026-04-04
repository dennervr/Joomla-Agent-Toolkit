import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock, call
import subprocess
import sys
from joomla_rag.bridge import AgentBridge


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_joomla_path(temp_dir):
    joomla_path = temp_dir / "joomla"
    joomla_path.mkdir()
    cli_path = joomla_path / "cli"
    cli_path.mkdir()
    return joomla_path


@patch("shutil.which")
def test_deploy_php_script_verbose(mock_which, mock_joomla_path, capsys):
    mock_which.return_value = "/usr/bin/php"
    bridge = AgentBridge(mock_joomla_path, verbose=True)
    bridge.deploy_php_script()

    captured = capsys.readouterr()
    assert f"deploy_php_script() writes to {bridge.php_script_path}" in captured.err


@patch("shutil.which")
def test_agent_bridge_no_php_with_compose(mock_which, mock_joomla_path):
    mock_which.return_value = None
    (mock_joomla_path / "docker-compose.yml").touch()
    with pytest.raises(
        RuntimeError,
        match="PHP is not installed locally and a Docker Compose file was detected",
    ):
        AgentBridge(mock_joomla_path)


@patch("shutil.which")
def test_agent_bridge_no_php_no_compose(mock_which, mock_joomla_path):
    mock_which.return_value = None
    with pytest.raises(
        RuntimeError,
        match="PHP is not installed locally. If you are using a containerized environment",
    ):
        AgentBridge(mock_joomla_path)


@patch("subprocess.run")
@patch("shutil.which")
def test_run_command_success(mock_which, mock_subprocess_run, mock_joomla_path):
    mock_which.return_value = "/usr/bin/php"
    bridge = AgentBridge(mock_joomla_path)
    bridge.deploy_php_script()

    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = '{"result": "success"}'
    mock_process.stderr = ""
    mock_subprocess_run.return_value = mock_process

    result = bridge.run_command("run", {"code": "echo 'test';"})
    assert result == {"result": "success"}
    mock_subprocess_run.assert_called_once()
    args, kwargs = mock_subprocess_run.call_args
    assert args[0][0] == "php"
    assert "agent_cli.php" in args[0][1]
    assert "agent:run" in args[0][2]
    assert kwargs["cwd"] == mock_joomla_path


@patch("subprocess.run")
def test_run_command_with_exec_prefix(mock_subprocess_run, mock_joomla_path):
    bridge = AgentBridge(
        mock_joomla_path, exec_prefix="docker exec -i joomla-container"
    )
    bridge.deploy_php_script()

    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = '{"result": "success"}'
    mock_process.stderr = ""
    mock_subprocess_run.return_value = mock_process

    result = bridge.run_command("run", {"code": "echo 'test';"})
    assert result == {"result": "success"}
    mock_subprocess_run.assert_called_once()
    args, kwargs = mock_subprocess_run.call_args
    expected_cmd = [
        "docker",
        "exec",
        "-i",
        "joomla-container",
        "php",
        "cli/agent_cli.php",
        "agent:run",
    ]
    assert args[0] == expected_cmd
    assert kwargs["cwd"] is None


@patch("subprocess.run")
@patch("shutil.which")
def test_run_command_failure(mock_which, mock_subprocess_run, mock_joomla_path):
    mock_which.return_value = "/usr/bin/php"
    bridge = AgentBridge(mock_joomla_path)
    bridge.deploy_php_script()

    mock_process = MagicMock()
    mock_process.returncode = 1
    mock_process.stdout = "some output"
    mock_process.stderr = "Error: Invalid command"
    mock_subprocess_run.return_value = mock_process

    with pytest.raises(RuntimeError) as exc_info:
        bridge.run_command("invalid", {})

    error_msg = str(exc_info.value)
    assert "PHP script failed with returncode 1" in error_msg
    assert "stderr: Error: Invalid command" in error_msg
    assert "stdout: some output" in error_msg
    assert "Command executed:" in error_msg


@patch("subprocess.run")
@patch("shutil.which")
def test_run_php_code(mock_which, mock_subprocess_run, mock_joomla_path):
    mock_which.return_value = "/usr/bin/php"
    bridge = AgentBridge(mock_joomla_path)
    bridge.deploy_php_script()

    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = '{"output": "Hello World"}'
    mock_process.stderr = ""
    mock_subprocess_run.return_value = mock_process

    result = bridge.run_php_code("echo 'Hello World';")
    assert result == {"output": "Hello World"}


@patch("subprocess.run")
@patch("shutil.which")
def test_trace_route(mock_which, mock_subprocess_run, mock_joomla_path):
    mock_which.return_value = "/usr/bin/php"
    bridge = AgentBridge(mock_joomla_path)
    bridge.deploy_php_script()

    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = '{"itemid": 123, "params": {"access": 1}}'
    mock_process.stderr = ""
    mock_subprocess_run.return_value = mock_process

    result = bridge.trace_route("com_users&view=login")
    assert result == {"itemid": 123, "params": {"access": 1}}


@patch("subprocess.run")
@patch("shutil.which")
def test_run_command_verbose(mock_which, mock_subprocess_run, mock_joomla_path, capsys):
    mock_which.return_value = "/usr/bin/php"
    bridge = AgentBridge(mock_joomla_path, verbose=True)
    bridge.deploy_php_script()

    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = '{"result": "success"}'
    mock_process.stderr = ""
    mock_subprocess_run.return_value = mock_process

    result = bridge.run_command("run", {"code": "echo 'test';"})
    assert result == {"result": "success"}

    captured = capsys.readouterr()
    assert f"Resolved joomla_path: {mock_joomla_path}" in captured.err
    assert "exec_prefix used: False" in captured.err
    assert "Command to execute:" in captured.err
    assert (
        "php" in captured.err
        and "agent_cli.php" in captured.err
        and "agent:run" in captured.err
    )
