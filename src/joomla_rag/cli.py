import argparse
import sys
import json
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
from . import api
from . import scaffold
from . import validate
from . import bridge


def setup(dev=False):
    """Setup the skill by copying or symlinking SKILL.md to opencode skills directory and creating data directory."""
    config_dir = Path.home() / ".config" / "opencode" / "skills" / "joomla-toolkit"
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
        print(
            "Development mode active! Any changes to SKILL.md will instantly reflect in OpenCode."
        )
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
    setup_parser.add_argument(
        "--dev",
        action="store_true",
        help="Development mode: symlink SKILL.md instead of copying",
    )

    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest documentation")
    ingest_parser.add_argument(
        "docs_path",
        type=str,
        nargs="?",
        default=None,
        help="Optional path to custom documentation directory",
    )

    # Search command
    search_parser = subparsers.add_parser("search", help="Search the documentation")
    search_parser.add_argument("query", type=str, help="Search query")
    search_parser.add_argument("--k", type=int, default=5, help="Number of results")

    # Inspect command
    inspect_parser = subparsers.add_parser("inspect", help="Inspect Joomla environment")
    inspect_parser.add_argument(
        "path", type=str, nargs="?", default=".", help="Path to Joomla root directory"
    )

    # API command
    api_parser = subparsers.add_parser("api", help="API commands")
    api_subparsers = api_parser.add_subparsers(dest="api_command")

    # Login subcommand
    login_parser = api_subparsers.add_parser("login", help="Login to Joomla API")
    login_parser.add_argument("url", help="Joomla site URL")
    login_parser.add_argument("token", help="Super User API Token")

    # Articles subcommand
    articles_parser = api_subparsers.add_parser("articles", help="Manage articles")
    articles_parser.add_argument(
        "action", choices=["list", "get", "create", "delete"], help="Action to perform"
    )
    articles_parser.add_argument("--id", type=int, help="Article ID for get/delete")
    articles_parser.add_argument("--title", help="Title for create")
    articles_parser.add_argument("--text", help="Text for create")
    articles_parser.add_argument(
        "--search", type=str, help="Search keyword to filter articles"
    )
    articles_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Max number of articles to return (default 5)",
    )
    articles_parser.add_argument(
        "--category", type=int, help="Category ID to filter articles"
    )
    articles_parser.add_argument("--state", type=int, help="State to filter articles")

    # Categories subcommand
    categories_parser = api_subparsers.add_parser(
        "categories", help="Manage categories"
    )
    categories_parser.add_argument("action", choices=["list"], help="Action to perform")
    categories_parser.add_argument(
        "--search", type=str, help="Search keyword to filter categories"
    )
    categories_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Max number of categories to return (default 5)",
    )
    categories_parser.add_argument(
        "--state", type=int, help="State to filter categories (published)"
    )

    # Menus subcommand
    menus_parser = api_subparsers.add_parser("menus", help="Manage menu items")
    menus_parser.add_argument("action", choices=["list"], help="Action to perform")
    menus_parser.add_argument(
        "--menutype", type=str, help="Menu type to filter menu items"
    )
    menus_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Max number of menu items to return (default 5)",
    )
    menus_parser.add_argument(
        "--state", type=int, help="State to filter menu items (published)"
    )

    # Scaffold command
    scaffold_parser = subparsers.add_parser(
        "scaffold", help="Scaffold Joomla components"
    )
    scaffold_subparsers = scaffold_parser.add_subparsers(dest="scaffold_command")

    # Component subcommand
    component_parser = scaffold_subparsers.add_parser(
        "component", help="Scaffold a component"
    )
    component_parser.add_argument("name", type=str, help="Component name")
    component_parser.add_argument(
        "--path", type=str, default=".", help="Path to Joomla root"
    )

    # Module subcommand
    module_parser = scaffold_subparsers.add_parser("module", help="Scaffold a module")
    module_parser.add_argument("name", type=str, help="Module name")
    module_parser.add_argument(
        "--path", type=str, default=".", help="Path to Joomla root"
    )

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate", help="Validate Joomla extension"
    )
    validate_parser.add_argument("path", type=str, help="Path to extension directory")

    # Bridge command
    bridge_parser = subparsers.add_parser(
        "bridge", help="Native Execution Bridge commands"
    )
    bridge_parser.add_argument(
        "--exec", type=str, help="Execution prefix, e.g., 'docker exec -i container'"
    )
    bridge_parser.add_argument(
        "--cwd", type=str, help="Working directory for execution"
    )
    bridge_subparsers = bridge_parser.add_subparsers(dest="bridge_command")

    # Run subcommand
    run_parser = bridge_subparsers.add_parser(
        "run", help="Execute PHP code in Joomla context"
    )
    run_parser.add_argument("code", type=str, help="PHP code to execute")
    run_parser.add_argument("--path", type=str, default=".", help="Path to Joomla root")

    # Trace subcommand
    trace_parser = bridge_subparsers.add_parser("trace", help="Trace Joomla route")
    trace_parser.add_argument(
        "route", type=str, help="Route to trace (e.g., com_users&view=login)"
    )
    trace_parser.add_argument(
        "--path", type=str, default=".", help="Path to Joomla root"
    )

    # Auth subcommand
    auth_parser = bridge_subparsers.add_parser("auth", help="Get API token")
    auth_parser.add_argument(
        "--path", type=str, default=".", help="Path to Joomla root"
    )

    args = parser.parse_args()

    if args.command == "setup":
        setup(dev=args.dev)
    elif args.command == "ingest":
        ingest.ingest_docs(args.docs_path)
    elif args.command == "search":
        search.search_docs(args.query, args.k)
    elif args.command == "inspect":
        inspect.inspect_env(args.path)
    elif args.command == "api":
        if args.api_command == "login":
            api.api_login(args.url, args.token)
        elif args.api_command == "articles":
            api.manage_articles(
                args.action,
                id=args.id,
                title=args.title,
                text=args.text,
                search=args.search,
                limit=args.limit,
                category=args.category,
                state=args.state,
            )
        elif args.api_command == "categories":
            api.manage_categories(
                args.action, search=args.search, limit=args.limit, state=args.state
            )
        elif args.api_command == "menus":
            api.manage_menus(
                args.action, menutype=args.menutype, limit=args.limit, state=args.state
            )
        else:
            api_parser.print_help()
    elif args.command == "scaffold":
        if args.scaffold_command == "component":
            scaffold.scaffold_component(args.name, args.path)
        elif args.scaffold_command == "module":
            scaffold.scaffold_module(args.name, args.path)
        else:
            scaffold_parser.print_help()
    elif args.command == "validate":
        validate.validate_extension(args.path)
    elif args.command == "bridge":
        joomla_path = Path(args.path)
        agent_bridge = bridge.AgentBridge(
            joomla_path,
            exec_prefix=getattr(args, "exec", None),
            cwd=getattr(args, "cwd", None),
        )
        agent_bridge.deploy_php_script()
        if args.bridge_command == "run":
            result = agent_bridge.run_php_code(args.code)
            print(json.dumps(result, indent=2))
        elif args.bridge_command == "trace":
            result = agent_bridge.trace_route(args.route)
            print(json.dumps(result, indent=2))
        elif args.bridge_command == "auth":
            result = agent_bridge.get_api_token()
            print(json.dumps(result, indent=2))
        else:
            bridge_parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
