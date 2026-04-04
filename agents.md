# Agent Configuration and "Skills" (OpenCode / Anthropic)

This project is designed with an **Agent Skills** architecture, aiming to optimize the context window of AI agents and provide the necessary tools for them to operate as **Full-Stack Joomla Developers**.

## The Joomla Agent Toolkit Vision

Instead of focusing solely on documentation search (RAG), this project aims to provide a complete ecosystem of skills so the AI can:
- Create and manage Articles, Categories, and Menus directly in the database or via API.
- Scaffold and develop Modules, Components (MVC), and Plugins from scratch.
- Understand the architectural differences between Joomla 3, 4, and 5.
- Package extensions ready for installation.

## The "Agent Skills" Model

In OpenCode and Anthropic-based agents (like Claude Desktop), keeping local servers running (like the Model Context Protocol - MCP) continuously consumes a lot of resources. The "Agent Skill" approach is lighter and more efficient:
- Functions as dynamic instructions injected via `.opencode/skills/` (or `~/.config/opencode/skills/`).
- Has a YAML frontmatter defining `name` and `description`.
- The agent reads the instructions and available tools **only** when the user needs to work with Joomla.

### Current Implementation: The Joomla Agent Toolkit

The toolkit now provides multiple skills for comprehensive Joomla development:

1. **Environment Introspection (`inspect`):** Quickly understand the local Joomla project by parsing `configuration.php` and scanning directories for installed extensions.

2. **Content Management via REST API (`api articles/categories/menus`):** Manage Joomla content with full CRUD operations (list, get, create, delete) and filters using Joomla's Web Services API.

3. **Intelligent Scaffolding (`scaffold component/module`):** Generate boilerplate code and folder structures for extensions instantly, supporting Components and Modules.

4. **Extension Validation (`validate`):** Ensure generated extensions are installable and follow Joomla standards by checking manifests and file structures.

5. **Smart Querying (RAG via `search`):** Intelligent documentation search using a local vector database for offline, instant access to Joomla docs.

The agent can autonomously execute these tools, such as inspecting the environment, scaffolding a new component, validating it, and querying documentation as needed, all without manual intervention.