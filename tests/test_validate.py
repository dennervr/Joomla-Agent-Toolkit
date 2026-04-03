import pytest
from pathlib import Path
import tempfile
from joomla_rag.validate import validate_extension

def create_valid_extension(tmp_path):
    """Create a minimal valid Joomla extension structure."""
    ext_dir = tmp_path / "com_test"
    ext_dir.mkdir()

    # Create XML manifest
    xml_content = """<?xml version="1.0" encoding="utf-8"?>
<extension type="component" version="4.0" method="upgrade">
    <name>Test</name>
    <version>1.0.0</version>
    <creationDate>2023-01-01</creationDate>
    <author>Test Author</author>
    <administration>
        <files folder="administrator/components/com_test">
            <filename>com_test.php</filename>
            <filename>com_test.xml</filename>
            <folder>services</folder>
        </files>
    </administration>
    <site>
        <files folder="components/com_test">
            <filename>com_test.php</filename>
            <folder>src</folder>
        </files>
    </site>
</extension>"""
    (ext_dir / "com_test.xml").write_text(xml_content)

    # Create referenced files
    (ext_dir / "com_test.php").write_text("<?php echo 'test'; ?>")
    (ext_dir / "services").mkdir()
    (ext_dir / "services" / "provider.php").write_text("<?php // provider ?>")
    (ext_dir / "src").mkdir()
    (ext_dir / "src" / "Controller.php").write_text("<?php // controller ?>")

    return ext_dir

def create_invalid_extension(tmp_path):
    """Create an invalid extension missing required tags."""
    ext_dir = tmp_path / "com_invalid"
    ext_dir.mkdir()

    # XML without required tags
    xml_content = """<?xml version="1.0" encoding="utf-8"?>
<extension type="component" version="4.0" method="upgrade">
    <name>Test</name>
    <!-- Missing version, creationDate, author -->
</extension>"""
    (ext_dir / "com_invalid.xml").write_text(xml_content)

    return ext_dir

def test_validate_valid_extension(tmp_path):
    """Test validation of a valid extension."""
    ext_dir = create_valid_extension(tmp_path)
    result = validate_extension(str(ext_dir))
    assert result is True

def test_validate_invalid_extension(tmp_path):
    """Test validation of an invalid extension."""
    ext_dir = create_invalid_extension(tmp_path)
    result = validate_extension(str(ext_dir))
    assert result is False