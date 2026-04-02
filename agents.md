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

### Current Implementation: The RAG Module for the Agent

The first implemented "Skill" is the intelligent documentation search (RAG):

1. **The Agent Receives the Prompt:** The user asks, for example, "How to create an MVC component in Joomla 5?".
2. **Skill Activation:** The AI detects the "Joomla" context and loads the `joomla-docs` skill.
3. **Autonomous Execution:** The skill file instructs the agent to execute the packaged CLI tool:
   ```bash
   joomla-rag search "How to create an MVC component in Joomla 5"
   ```
4. **Silent and Offline Extraction:** The local vector database (ChromaDB) is queried and instantly returns the most relevant snippets from the official Joomla documentation, without requiring external API calls and without polluting the terminal with unnecessary logs.
5. **Deep Dive (Optional):** The search response includes the absolute paths of the Markdown files. If the agent needs more context, it can use reading tools to consult the full document before generating the final code.