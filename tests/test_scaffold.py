import pytest
from pathlib import Path
from joomla_rag.scaffold import scaffold_component


def test_scaffold_component(tmp_path):
    """Test that scaffold_component creates the correct directory structure and files."""
    component_name = "com_test"
    scaffold_component(component_name, str(tmp_path))

    # Check directories
    site_dir = tmp_path / "components" / component_name
    admin_dir = tmp_path / "administrator" / "components" / component_name

    assert site_dir.exists()
    assert admin_dir.exists()

    # Check site files
    assert (site_dir / f"{component_name}.php").exists()
    assert (site_dir / "src" / "Controller" / "DisplayController.php").exists()
    assert (site_dir / "src" / "View" / "Example" / "HtmlView.php").exists()
    assert (site_dir / "tmpl" / "example" / "default.php").exists()

    # Check admin files
    assert (admin_dir / f"{component_name}.php").exists()
    assert (admin_dir / "services" / "provider.php").exists()
    assert (admin_dir / "sql" / "install.mysql.utf8.sql").exists()
    assert (admin_dir / f"{component_name}.xml").exists()
