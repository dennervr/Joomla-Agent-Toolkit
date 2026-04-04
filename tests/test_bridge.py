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


@patch("subprocess.check_output")
@patch("shutil.which")
def test_agent_bridge_init(mock_which, mock_check_output, mock_joomla_path):
    mock_which.return_value = "/usr/bin/php"
    bridge = AgentBridge(mock_joomla_path)
    assert bridge.joomla_path == mock_joomla_path
    assert bridge.php_script_path == mock_joomla_path / "cli" / "agent_cli.php"
    assert bridge.exec_prefix is None
    assert bridge.cwd is None


@patch("subprocess.check_output")
@patch("shutil.which")
def test_agent_bridge_auto_detect_docker(
    mock_which, mock_check_output, mock_joomla_path
):
    mock_which.return_value = None
    mock_check_output.return_value = "joomla-container\nother-container"
    bridge = AgentBridge(mock_joomla_path)
    assert bridge.exec_prefix == "docker exec -i joomla-container"


@patch("subprocess.check_output")
@patch("shutil.which")
@patch("subprocess.run")
def test_run_command_success(
    mock_subprocess_run, mock_which, mock_check_output, mock_joomla_path
):
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


@patch("subprocess.check_output")
@patch("shutil.which")
@patch("subprocess.run")
def test_run_command_failure(
    mock_subprocess_run, mock_which, mock_check_output, mock_joomla_path
):
    mock_which.return_value = "/usr/bin/php"
    bridge = AgentBridge(mock_joomla_path)
    bridge.deploy_php_script()

    mock_process = MagicMock()
    mock_process.returncode = 1
    mock_process.stdout = ""
    mock_process.stderr = "Error: Invalid command"
    mock_subprocess_run.return_value = mock_process

    with pytest.raises(RuntimeError, match="PHP script failed"):
        bridge.run_command("invalid", {})


@patch("subprocess.check_output")
@patch("shutil.which")
@patch("subprocess.run")
def test_run_php_code(
    mock_subprocess_run, mock_which, mock_check_output, mock_joomla_path
):
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


@patch("subprocess.check_output")
@patch("shutil.which")
@patch("subprocess.run")
def test_trace_route(
    mock_subprocess_run, mock_which, mock_check_output, mock_joomla_path
):
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


@patch("subprocess.check_output")
@patch("shutil.which")
@patch("subprocess.run")
def test_get_api_token(
    mock_subprocess_run, mock_which, mock_check_output, mock_joomla_path
):
    mock_which.return_value = "/usr/bin/php"
    bridge = AgentBridge(mock_joomla_path)
    bridge.deploy_php_script()

    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = '{"token": "abc123"}'
    mock_process.stderr = ""
    mock_subprocess_run.return_value = mock_process

    result = bridge.get_api_token()
    assert result["token"] == "abc123"
