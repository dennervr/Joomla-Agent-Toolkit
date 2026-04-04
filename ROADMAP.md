# Joomla Agent Toolkit - Development Roadmap

This document outlines the planned features to expand the `joomla-rag` CLI from a documentation search tool into a complete toolkit for AI agents to autonomously manage and develop Joomla websites.

## 1. Environment Introspection (`joomla-rag inspect`)
**Goal:** Allow the AI agent to quickly understand the local Joomla project without manually exploring folders.
- Parse `configuration.php` to extract Joomla version, database prefix, and critical paths.
- Scan `/components`, `/modules`, and `/plugins` directories.
- Return a clean JSON summary of installed extensions and environment variables.

## 2. Content and Configuration Management (`joomla-rag db` / `joomla-rag api`)
**Goal:** Empower the AI to read and modify Joomla data (Articles, Categories, Menus, Modules, etc.) directly, including managing Categories and Menu Items essential for routing content and components.

- **Approach A (Direct Database):** Parse credentials from `configuration.php` to securely query the database (e.g., `#__content`, `#__modules`). 
  - *Commands:* `joomla-rag db list-articles`, `joomla-rag db get-module <id>`
- **Approach B (REST API):** Use Joomla 4/5 Web Services for standardized interactions with full CRUD operations and filters.
  - *Commands:* `joomla-rag api articles list`, `joomla-rag api categories list`, `joomla-rag api menus list`

## 3. Intelligent Scaffolding (`joomla-rag scaffold`)

**Goal:** Save AI tokens and execution time by generating boilerplate code instantly.

- Generate complete folder structures and mandatory files (XML manifests, entrypoints, language files).

- Support standard extension types: Components, Modules, and Plugins.

  - *Commands:* `joomla-rag scaffold module mod_example`, `joomla-rag scaffold component com_example`, `joomla-rag scaffold plugin plg_example`

## 4. Extension Validation (`joomla-rag validate`)
**Goal:** Ensure generated extensions are installable and follow Joomla standards before the AI finishes its task.
- Parse the `.xml` manifest file to check for required tags.
- Verify that all files and folders referenced in the manifest actually exist in the file system.
- *Command:* `joomla-rag validate <path-to-extension>`

## 5. Smart Search Integration (`joomla-rag db smart-search`)
**Goal:** Enable the AI to quickly find content using Joomla's Smart Search index (`com_finder`), since Joomla 4/5 does not expose a native REST API endpoint for it.
- **Approach:** Parse credentials from `configuration.php` and directly query the `#__finder_links` and `#__finder_terms` tables to perform fast, token-efficient searches.
- *Command:* `joomla-rag db smart-search "search term"`


