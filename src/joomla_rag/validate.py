import os
import xml.etree.ElementTree as ET
from pathlib import Path

def validate_extension(path: str) -> bool:
    """
    Validates a Joomla extension by checking the XML manifest and file references.
    Returns True if valid, False otherwise.
    """
    path = Path(path)
    if not path.exists() or not path.is_dir():
        print(f"Error: Path {path} does not exist or is not a directory.")
        return False

    # Find XML manifest files
    xml_files = list(path.glob("*.xml"))
    if not xml_files:
        print("Error: No XML manifest file found in the extension directory.")
        return False

    # Assume the first XML file is the manifest (typically there's only one)
    manifest_file = xml_files[0]
    print(f"Found manifest: {manifest_file.name}")

    try:
        tree = ET.parse(manifest_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return False

    # Check for <extension> tag
    if root.tag != "extension":
        print("Error: Root tag is not 'extension'.")
        return False

    # Required tags
    required_tags = ["name", "version", "creationDate", "author"]
    missing_tags = []
    for tag in required_tags:
        if root.find(tag) is None:
            missing_tags.append(tag)

    if missing_tags:
        print(f"Missing required tags: {', '.join(missing_tags)}")
    else:
        print("All required tags present.")

    # Check files and folders
    missing_files = []
    for files_elem in root.findall(".//files") + root.findall(".//media"):
        for filename_elem in files_elem.findall("filename"):
            file_path = path / filename_elem.text
            if not file_path.exists():
                missing_files.append(filename_elem.text)
        for folder_elem in files_elem.findall("folder"):
            folder_path = path / folder_elem.text
            if not folder_path.exists() or not folder_path.is_dir():
                missing_files.append(folder_elem.text)

    if missing_files:
        print(f"Missing files/folders: {', '.join(missing_files)}")
    else:
        print("All referenced files and folders exist.")

    # Summary
    if not missing_tags and not missing_files:
        print("Validation successful: Extension is ready for installation.")
        return True
    else:
        print("Validation failed: Fix the issues above before installing.")
        return False