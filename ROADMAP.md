# Joomla Agent Toolkit - Development Roadmap

This document outlines the planned features to expand the `joomla-rag` CLI from a documentation search tool into a complete toolkit for AI agents to autonomously manage and develop Joomla websites.

## 1. Environment Introspection (`joomla-rag inspect`)
**Goal:** Allow the AI agent to quickly understand the local Joomla project without manually exploring folders.
- Parse `configuration.php` to extract Joomla version, database prefix, and critical paths.
- Scan `/components`, `/modules`, and `/plugins` directories.
- Return a clean JSON summary of installed extensions and environment variables.

## 2. Native Execution Bridge (Joomla API Runner) 🚀 *[NEW]*
**Goal:** Execute isolated PHP scripts or complex logic safely inside the Joomla context without "Failed to start application" errors.
- **Approach:** Inject a Joomla Console Plugin (CLI Application) that properly bootstraps the DI container.
- **Execution:** Expose an `agent:run` command to receive PHP logic via `stdin` (JSON payload) and return structured output.
- **Audit & Logging (Crucial):** Every code execution or database alteration made through this bridge MUST be logged automatically (e.g., to an `agent_audit.log` or database table) for analysis, security review, and future replication.
- **Container Support:** When Joomla runs in a container without host volume mounts, deploy the bridge script inside the container using `joomla-rag bridge --exec ... --cwd ... --deploy-via-exec`.

## 3. Entity Inspector and Editor (REST API)
**Goal:** Empower the AI to read and modify Joomla data (Articles, Categories, Menus, Modules, Plugins) without breaking JSON structures (`params`) or UTF-8 encoding.
- **Approach:** Deprecate raw SQL queries for complex entities. Instead, use the Joomla 4/5 Core Web Services (REST API).
- **Implementation:** The CLI Runner will provide an `agent:auth` command to securely fetch a Super User API token and enable the Web Services plugin. The Python toolkit will then make clean HTTP requests.
- *Commands:* `joomla-rag api modules get --id <id> [--client site|admin]`, `joomla-rag api menus list`, etc.

## 4. Route and Redirect Mapper 🗺️ *[NEW]*
**Goal:** Demystify Joomla's `Itemid` routing system to understand which menu item controls a specific view, its access level (ACL), and redirection rules.
- **Approach:** Add an `agent:trace` command to the CLI Bridge that instantiates `SiteRouter` and `MenuRules`.
- **Functionality:** Input a raw internal route (e.g., `com_users&view=login`) and output the exact `Itemid` taking control, along with its `params` (JSON) and `access` rules.

## 5. Intelligent Scaffolding (`joomla-rag scaffold`)
**Goal:** Save AI tokens and execution time by generating boilerplate code instantly.
- Generate complete folder structures and mandatory files (XML manifests, entrypoints, language files).
- Support standard extension types: Components, Modules, and Plugins.

## 6. Extension Validation (`joomla-rag validate`)
**Goal:** Ensure generated extensions are installable and follow Joomla standards before the AI finishes its task.
- Parse the `.xml` manifest file to check for required tags.
- Verify that all files and folders referenced in the manifest actually exist in the file system.

## 7. Smart Search Integration (`joomla-rag db smart-search`)
**Goal:** Enable the AI to quickly find content using Joomla's Smart Search index (`com_finder`).
- **Approach:** Parse credentials from `configuration.php` and directly query the `#__finder_links` and `#__finder_terms` tables to perform fast, token-efficient searches (since Joomla 4/5 does not expose a native REST API endpoint for it).
