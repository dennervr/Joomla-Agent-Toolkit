# Joomla Agent Toolkit

The Joomla Agent Toolkit is a suite of CLI tools designed to empower AI agents (such as OpenCode and Claude) to autonomously develop, manage, and maintain complete Joomla 4 and 5 websites.

Our goal is to provide the necessary "skills" for the AI to act as a Full-Stack Joomla Developer, capable of:
- **Introspecting Environments:** Instantly understanding local Joomla setups, database credentials, and installed extensions.
- **Content Management:** Creating, reading, and managing Articles, Categories, Menus, and Modules via the official Joomla REST API.
- **Native Execution Bridge:** Safely executing PHP scripts and tracing routes within the Joomla environment.
- **Intelligent Scaffolding:** Instantly generating boilerplate code for Components following the modern Joomla MVC architecture (Namespaces, Dependency Injection).
- **Extension Validation:** Ensuring generated extensions have valid XML manifests and correct file structures before installation.
- **Smart Querying (RAG):** Querying an embedded vector database with official Joomla documentation in real-time to ensure code follows best practices and the latest platform standards.

## How to Install

```bash
# Install the CLI globally on your system using pipx
pipx install git+https://github.com/dennervr/Joomla-Agent-Toolkit.git

# Ensure the pipx folder is in your PATH
pipx ensurepath

# Inject the Skill into your environment (e.g., OpenCode)
joomla-rag setup
```

## Available Commands (CLI)

- `joomla-rag setup`: Installs the instruction files (Skills) globally in the agent's environment (e.g., `~/.config/opencode/skills/`).
- `joomla-rag inspect [path]`: Introspects a local Joomla installation, returning database configs, version, and installed extensions concisely.
- `joomla-rag api`: Manage Joomla content via REST API using `requests`. Subcommands: `articles list/get/create/delete`, `categories list`, `menus list`, `modules get`.
- `joomla-rag bridge`: Native execution bridge for running PHP code and tracing routes within Joomla context. Subcommands: `run` (execute PHP code), `trace` (resolve routes), `auth` (retrieve API token).
  - For containerized Joomla where the Joomla filesystem is not mounted on the host, use: `--exec ... --cwd ... --deploy-via-exec`.
  - For debugging silent failures, use: `--verbose`.
- `joomla-rag scaffold component [name]`: Instantly generates Joomla 4/5 MVC boilerplate code for components and modules (`provider.php`, XML manifests, entrypoints).
- `joomla-rag validate [path]`: Validates a Joomla extension by parsing the XML manifest to check for required tags and verifying that all referenced files/folders actually exist.
- `joomla-rag search "query"`: Command used autonomously by the AI to search for specific knowledge in the Joomla documentation.
- `joomla-rag ingest [path]`: (Optional) Administrative command to reprocess the documentation and update the internal vector database.
