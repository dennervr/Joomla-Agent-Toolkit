# 🤖 Agentic Coding Guidelines (AGENTS.md)

Welcome, fellow agent. This document serves as the primary instruction manual for any AI or autonomous agent operating within this repository (`joomla-rag`). It dictates how you should read, modify, and test this codebase.

## 🎯 1. Project Overview

This repository houses `joomla-rag`, a Python-based CLI and Agent Toolkit for querying Joomla documentation via RAG (Retrieval-Augmented Generation) and scaffolding/inspecting Joomla environments. It leverages LangChain, ChromaDB, and sentence-transformers. 
As an agent working here, your goal is to extend and maintain this toolkit, ensuring it stays robust and aligned with the "Agent Skills" architecture for OpenCode/Anthropic.

## 🛠️ 2. Build, Lint, and Test Commands

When working on this codebase, you must ensure that your changes do not break existing functionality. Use the following commands to validate your work.

### Local Environment Setup
Before running tests, ensure the environment is activated:
```bash
python -m venv venv
source venv/bin/activate
pip install -e .
pip install pytest flake8 black mypy
```

### 🧪 Running Tests
We use `pytest` as our testing framework. Tests are located in the `/tests` directory.

**Run all tests:**
```bash
pytest tests/
```

**Run a single test file:**
```bash
pytest tests/test_filename.py
```

**Run a specific single test case (CRITICAL FOR AGENTS):**
When iterating on a specific feature or bug fix, run only the relevant test to save time and context:
```bash
pytest tests/test_filename.py::test_function_name
```

**Run tests with output capturing disabled (useful for debugging):**
```bash
pytest -s tests/test_filename.py::test_function_name
```

### 🧹 Linting and Formatting
Ensure your code matches the existing style before committing.

**Check formatting:**
```bash
black --check src/ tests/
```

**Apply formatting:**
```bash
black src/ tests/
```

**Run linter:**
```bash
flake8 src/ tests/
```

**Type checking:**
```bash
mypy src/
```

## 📝 3. Code Style Guidelines

To maintain a healthy and consistent codebase, adhere strictly to the following conventions:

### Imports
- **Order:** 
  1. Standard library imports
  2. Third-party imports (e.g., `langchain`, `chromadb`)
  3. Local application/library specific imports (`from joomla_rag import ...`)
- **Style:** Use absolute imports for external packages and relative imports for internal modules within the same package.
- **Grouping:** Separate each group with a single blank line.

### Formatting & Syntax
- **Formatter:** Code must conform to `black` default styling (88 character line length). Do not introduce manual formatting tweaks.
- **Docstrings:** Use standard PEP 257 docstrings. Public modules, classes, and functions MUST have docstrings explaining their purpose, parameters, and return types.
- **Indentation:** 4 spaces per indentation level. No tabs.

### Type Hinting
- **Strict Typing:** All new functions and methods **must** include type hints for both parameters and return values. 
- **Collections:** Use standard library type hints (`list[str]`, `dict[str, Any]`, etc.).
- **Optional Types:** Explicitly define `Optional[Type]` or `Type | None` when a parameter defaults to `None`.

### Naming Conventions
- **Variables & Functions:** `snake_case` (e.g., `generate_embedding`, `document_chunk`).
- **Classes:** `PascalCase` (e.g., `JoomlaRetriever`, `AgentSkill`).
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_TOKEN_LIMIT`, `DEFAULT_DB_PATH`).
- **Private Members:** Prefix with a single underscore `_` for internal methods or variables (e.g., `_load_vector_store()`).

### Error Handling
- **Specific Exceptions:** Catch specific exceptions rather than a generic `Exception` whenever possible (e.g., `except FileNotFoundError:` instead of `except Exception:`).
- **Custom Exceptions:** Create custom exception classes for domain-specific errors (e.g., `VectorStoreLoadError`).
- **Logging vs Printing:** Use the standard Python `logging` module for warnings and errors. Only use `print()` for CLI output that the user explicitly requested.
- **Fail Fast:** Validate inputs at the boundary. Raise `ValueError` or `TypeError` early if arguments are invalid.

### File Structure & Modules
- `src/joomla_rag/`: Main package code.
- `tests/`: All unit and integration tests. Must mirror the structure of `src/`.
- `data/`: Contains markdown docs and vector DB artifacts.

## 🧠 4. Agent-Specific Operational Rules

When operating autonomously within this repository, adhere to these tenets:
1. **Read before you write:** Always use your `Read` or `Glob` tools to understand the surrounding code context before using the `Edit`/`Write` tools. Do not blindly overwrite.
2. **Atomic Commits:** If the user asks you to commit, break unrelated changes into logical, focused commits.
3. **No Silly Edits:** Do not arbitrarily change formatting on code you are not actively modifying unless it violates the project's `black` constraints and the user asked for a cleanup.
4. **Preserve the Toolkit Vision:** This project acts as an "Agent Skill" providing tools for Joomla developers. Do not alter the core design philosophy (lightweight dynamic skills over heavy persistent MCP servers).
5. **Self-Correction:** If a test fails, read the traceback carefully, fix the code, and re-run the specific test using the single-test command provided above. Do not guess; read the error.
6. **No interactive shells:** Never run tools that prompt for interactive input (`pytest --pdb`, `git add -p`).

## 🤖 5. Integration with OpenCode / Anthropic

This project utilizes the "Agent Skills" model:
- Skills are injected via `.opencode/skills/` (or `~/.config/opencode/skills/`) with YAML frontmatter.
- Ensure any new CLI tools or endpoints correctly define their expected arguments, parameters, and descriptions, as other agents rely on these definitions to execute Joomla tasks.

---
