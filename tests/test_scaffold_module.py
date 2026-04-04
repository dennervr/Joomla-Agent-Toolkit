import pytest
from pathlib import Path
from joomla_rag.scaffold import scaffold_module

def test_scaffold_module(tmp_path):
    """Test that scaffold_module creates the correct directory structure and files."""
    module_name = "mod_test_agent"
    scaffold_module(module_name, str(tmp_path))

    # Check directories
    module_dir = tmp_path / 'modules' / module_name

    assert module_dir.exists()

    # Check module files
    assert (module_dir / f'{module_name}.php').exists()
    assert (module_dir / f'{module_name}.xml').exists()
    assert (module_dir / 'tmpl' / 'default.php').exists()
    assert (module_dir / 'services' / 'provider.php').exists()