import pytest
from pathlib import Path
import tempfile
import os
from unittest.mock import patch
from joomla_rag.inspect import inspect_env


def test_inspect_env_with_valid_joomla_root(tmp_path):
    # Create fake Joomla structure
    joomla_root = tmp_path / "joomla_site"
    joomla_root.mkdir()

    # Create configuration.php
    config_content = "<?php\nclass JConfig {\n    public $dbtype = 'mysqli';\n    public $host = 'localhost';\n    public $user = 'joomla_user';\n    public $password = 'secret';\n    public $db = 'joomla_db';\n    public $dbprefix = 'jos_';\n    public $log_path = '/var/log/joomla';\n    public $tmp_path = '/tmp/joomla';\n}\n"
    (joomla_root / "configuration.php").write_text(config_content)

    # Create version file
    admin_dir = joomla_root / "administrator" / "manifests" / "files"
    admin_dir.mkdir(parents=True)
    (admin_dir / "joomla.xml").write_text("<version>4.4.0</version>")

    # Create extensions
    (joomla_root / "components" / "com_fake").mkdir(parents=True)
    (joomla_root / "modules" / "mod_fake").mkdir(parents=True)
    (joomla_root / "plugins" / "system" / "plg_fake").mkdir(parents=True)

    # Mock print to capture output
    with patch("builtins.print") as mock_print:
        result = inspect_env(str(joomla_root))

    # Assert config data
    expected_config = {
        "dbtype": "mysqli",
        "host": "localhost",
        "user": "joomla_user",
        "db": "joomla_db",
        "dbprefix": "jos_",
        "log_path": "/var/log/joomla",
        "tmp_path": "/tmp/joomla",
    }
    assert result["config"] == expected_config
    assert result["version"] == "4.4.0"
    assert "com_fake" in result["extensions"]["components"]
    assert "mod_fake" in result["extensions"]["modules"]
    assert "system/plg_fake" in result["extensions"]["plugins"]

    # Assert print was called
    assert mock_print.call_count > 0


def test_inspect_env_no_config_file(tmp_path):
    joomla_root = tmp_path / "no_config"
    joomla_root.mkdir()

    with patch("builtins.print") as mock_print:
        result = inspect_env(str(joomla_root))

    assert result == {"error": "not found"}
    mock_print.assert_called_with(
        "[ERROR] configuration.php not found. Not a Joomla root."
    )


def test_inspect_env_invalid_config(tmp_path):
    joomla_root = tmp_path / "invalid_config"
    joomla_root.mkdir()
    (joomla_root / "configuration.php").write_text("invalid php")

    with patch("builtins.print") as mock_print:
        result = inspect_env(str(joomla_root))

    assert result["config"] == {}
    assert result["version"] is None
    assert result["extensions"] == {"components": [], "modules": [], "plugins": []}
    mock_print.assert_called_once()
