import argparse
import sys
from pathlib import Path
import shutil
import os

# Suppress loading bars
os.environ["TQDM_DISABLE"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_WARNINGS"] = "1"
os.environ["huggingface_hub_VERBOSITY"] = "error"

from . import ingest
from . import search
from . import inspect

def setup(dev=False):
    """Setup the skill by copying or symlinking SKILL.md to opencode skills directory and creating data directory."""
    config_dir = Path.home() / ".config" / "opencode" / "skills" / "joomla-docs"
    data_dir = Path.home() / ".local" / "share" / "joomla-rag"
    
    # Create directories
    config_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    skill_md_dst = config_dir / "SKILL.md"
    
    if dev:
        # Development mode: Create a symlink to the local SKILL.md so changes are instant
        skill_md_src = Path.cwd() / "src" / "joomla_rag" / "data" / "SKILL.md"
        if not skill_md_src.exists():
            print(f"Error: Local SKILL.md not found at {skill_md_src}", file=sys.stderr)
            sys.exit(1)
            
        if skill_md_dst.exists() or skill_md_dst.is_symlink():
            skill_md_dst.unlink()
            
        os.symlink(skill_md_src, skill_md_dst)
        print(f"Created symlink: {skill_md_dst} -> {skill_md_src}")
        print("Development mode active! Any changes to SKILL.md will instantly reflect in OpenCode.")
    else:
        # Production mode: Copy from the installed package
        skill_md_src = Path(__file__).parent / "data" / "SKILL.md"
        if skill_md_src.exists():
            if skill_md_dst.exists() or skill_md_dst.is_symlink():
                skill_md_dst.unlink()
            shutil.copy(skill_md_src, skill_md_dst)
            print(f"Copied SKILL.md to {skill_md_dst}")
        else:
            print("SKILL.md not found in package data", file=sys.stderr)
            sys.exit(1)
    
    print(f"Created data directory at {data_dir}")
    print("Setup complete.")

def main():
    parser = argparse.ArgumentParser(description="Joomla RAG CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup the skill")
    setup_parser.add_argument("--dev", action="store_true", help="Development mode: symlink SKILL.md instead of copying")
    
    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest documentation")
    ingest_parser.add_argument("docs_path", type=str, nargs='?', default=None, help="Optional path to custom documentation directory")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search the documentation")
    search_parser.add_argument("query", type=str, help="Search query")
    search_parser.add_argument("--k", type=int, default=5, help="Number of results")
    
    # Inspect command
    inspect_parser = subparsers.add_parser("inspect", help="Inspect Joomla environment")
    inspect_parser.add_argument("path", type=str, nargs='?', default=".", help="Path to Joomla root directory")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        setup(dev=args.dev)
    elif args.command == "ingest":
        ingest.ingest_docs(args.docs_path)
    elif args.command == "search":
        search.search_docs(args.query, args.k)
    elif args.command == "inspect":
        inspect.inspect_env(args.path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()