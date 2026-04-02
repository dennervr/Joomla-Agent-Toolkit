import json
import os
import re
from pathlib import Path

def inspect_env(target_path: str = "."):
    target = Path(target_path).resolve()
    config_file = target / "configuration.php"
    
    if not config_file.exists():
        print("[ERROR] configuration.php not found. Not a Joomla root.")
        return {"error": "not found"}
    
    # Parse configuration.php
    config_data = {}
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract variables using regex
        variables = ['dbtype', 'host', 'user', 'db', 'dbprefix', 'log_path', 'tmp_path']
        for var in variables:
            match = re.search(rf'public \${var}\s*=\s*[\'"]([^\'"]*)[\'"];', content)
            if match:
                config_data[var] = match.group(1)
    except Exception as e:
        print(f"[ERROR] Failed to parse configuration.php: {str(e)}")
        return {"error": "parse error"}
    
    # Detect Joomla version
    version_file = target / "administrator" / "manifests" / "files" / "joomla.xml"
    version = None
    if version_file.exists():
        try:
            with open(version_file, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            match = re.search(r'<version>([^<]+)</version>', xml_content)
            if match:
                version = match.group(1)
        except Exception as e:
            pass  # Ignore errors, version remains None
    
    # Scan extensions
    extensions = {
        "components": [],
        "modules": [],
        "plugins": []
    }
    
    for ext_type in extensions:
        ext_dir = target / ext_type
        if ext_dir.exists() and ext_dir.is_dir():
            try:
                if ext_type == "plugins":
                    # Plugins are grouped by type (e.g., plugins/system/plg_name)
                    for group_dir in ext_dir.iterdir():
                        if group_dir.is_dir() and not group_dir.name.startswith('.'):
                            for item in group_dir.iterdir():
                                if item.is_dir() and not item.name.startswith('.'):
                                    extensions[ext_type].append(f"{group_dir.name}/{item.name}")
                else:
                    for item in ext_dir.iterdir():
                        if item.is_dir() and not item.name.startswith('.'):
                            extensions[ext_type].append(item.name)
            except Exception as e:
                pass  # Ignore errors
    
    # Format token-efficient output
    output = []
    output.append(f"[JOOMLA ENV] Version: {version or 'Unknown'}")
    
    if config_data:
        c = config_data
        output.append(f"[DB] {c.get('dbtype')} | Host: {c.get('host')} | User: {c.get('user')} | DB: {c.get('db')} | Prefix: {c.get('dbprefix')}")
        output.append(f"[PATHS] Log: {c.get('log_path')} | Tmp: {c.get('tmp_path')}")
        
    output.append("[EXTENSIONS]")
    for ext_type, items in extensions.items():
        if items:
            output.append(f"{ext_type.capitalize()}: {', '.join(items)}")
        else:
            output.append(f"{ext_type.capitalize()}: (None)")
            
    final_output = "\n".join(output)
    print(final_output)
    return { "config": config_data, "version": version, "extensions": extensions }