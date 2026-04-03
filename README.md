# Joomla Agent Toolkit (ragJoomla)

The Joomla Agent Toolkit is a suite of tools designed to empower AI agents (such as OpenCode and Claude) to develop complete Joomla websites autonomously.

Our goal is to provide the necessary "skills" for the AI to act as a Full-Stack Joomla Developer, capable of:
- Creating and managing Articles, Categories, and Menus.
- Developing Modules, Components, and Plugins from scratch.
- Understanding and applying the Joomla MVC architecture (versions 3, 4, and 5).
- Integrating extensions and managing the CMS ecosystem.

Currently, the project features a robust initial **RAG (Retrieval-Augmented Generation)** module. This tool allows AI agents to query the official Joomla documentation in real-time and autonomously, ensuring the generated code follows best practices and the latest platform standards.

## Features

- **Smart Querying (RAG):** Embedded vector database with official Joomla documentation. The AI dynamically fetches the necessary context to solve complex problems.
- **Global Integration:** Can be installed globally on the system and used in any local project or directory.

## How to Install

```bash
# Install the CLI globally on your system using pipx
pipx install git+https://github.com/your-username/joomla-rag.git

# Ensure the pipx folder is in your PATH
pipx ensurepath

# Inject the Skill into your environment (e.g., OpenCode)
joomla-rag setup
```

## Available Commands (CLI)

- `joomla-rag setup`: Installs the instruction files (Skills) globally in the agent's environment (e.g., `~/.config/opencode/skills/`).
- `joomla-rag search "query"`: Command used autonomously by the AI to search for specific knowledge in the Joomla documentation.
- `joomla-rag inspect [path]`: Command used by the AI to introspect a local Joomla installation, returning database configs, version, and installed extensions concisely.
- `joomla-rag api articles`: Manage articles via Joomla REST API. Supports `list`, `get`, `create`, `delete` with optimizations like sparse fieldsets, category/state filters, and limit controls.
- `joomla-rag scaffold component [name]`: Instantly generate Joomla 4/5 MVC boilerplate code (provider.php, XML manifests, entrypoints).
- `joomla-rag validate [path]`: Validates a Joomla extension by parsing the XML manifest to check for required tags and verifying that all referenced files/folders actually exist.
- `joomla-rag ingest [path]`: (Optional) Administrative command to reprocess the documentation and update the internal vector database.