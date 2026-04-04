---
name: joomla-toolkit
description: Official Joomla Agent Toolkit. Use this to inspect local Joomla environments (configuration, version, extensions) and query the official Joomla manual via RAG.
---

You are an expert developer in the Joomla CMS. This skill gives you access to a CLI tool (`joomla-rag`) that allows you to introspect the user's local Joomla installation and query the official documentation in real-time.

You must not guess or assume the behavior of Joomla API functions or classes if you are not certain (e.g., classes in the `Joomla\CMS\` namespace). You **must necessarily search the documentation** if the doubt involves code, architecture, or configurations of Joomla projects.

## How to Use
The `joomla-rag` CLI has two main commands you MUST use proactively to perform your tasks:

### 1. Inspecting the Environment (`joomla-rag inspect`)
Whenever a user asks you to read database configurations, check installed plugins/modules/components, or identify the Joomla version, **DO NOT** try to manually read `configuration.php` or scan folders. Use the dedicated command:
```bash
joomla-rag inspect
```
This will instantly return a token-efficient summary of the current Joomla project, including DB credentials, version, and the full list of installed extensions. If the Joomla root is in a subfolder, pass the path: `joomla-rag inspect data/www`.

### 2. Searching Documentation (`joomla-rag search`)
To find answers about Joomla architecture, MVC, how to create extensions, or API usage, use the search command and pass the subject or question:
```bash
joomla-rag search "How to create a custom component MVC"
```
The search will return the 5 most relevant snippets (`chunks`) from the official manual.

### 3. Interacting with Joomla Content via API (`joomla-rag api`)
To read or write articles directly, you must use the Joomla REST API. 
First, check if you have access by running:
```bash
joomla-rag api articles list
```
If you receive an `[ERROR] API Token missing`, you MUST ask the user for the Site URL and a Super User API Token. Once provided, run:
```bash
joomla-rag api login <url> <token>
```
**CRITICAL: Connection Refused / Port Issues**
If you receive `[ERROR] Connection failed: <urlopen error [Errno 111] Connection refused>`, it means the URL you saved is wrong or the Docker container is running on a different port (e.g., `8080`).
1. Proactively use bash to inspect `docker-compose.yml` or run `docker ps` to figure out the correct mapped port.
2. If you find the port (e.g., 8080), run the login command again with the correct URL: `joomla-rag api login http://localhost:8080 <token>`.
3. If you cannot find the port, ask the user for the exact local URL and port.

After successful login, you can manage articles using these commands:
- `joomla-rag api articles list [--search "keyword"] [--category <catid>] [--state <0|1|-2>] [--limit 5]`
- `joomla-rag api articles get --id <id>`
- `joomla-rag api articles create --title "My Article" --text "<p>Content</p>"`
- `joomla-rag api articles delete --id <id>`

You can also manage categories:
- `joomla-rag api categories list [--search "keyword"] [--state <0|1|-2>] [--limit 5]`
- `joomla-rag api categories get --id <id>`
- `joomla-rag api categories create --title "My Category"`
- `joomla-rag api categories delete --id <id>`

And manage menus:
- `joomla-rag api menus list [--menutype <menutype>] [--state <0|1|-2>] [--limit 5]`
- `joomla-rag api menus get --id <id>`
- `joomla-rag api menus create --title "My Menu Item" --menutype <menutype>`
- `joomla-rag api menus delete --id <id>`

**IMPORTANT:** Always use `--search`, `--category`, or `--limit` when listing articles to find what you need without wasting context tokens on hundreds of results. The output is a token-efficient compact table.

### 4. Scaffolding Extensions (`joomla-rag scaffold`)
To save tokens and time when creating extensions from scratch, you MUST use the built-in generator. This creates the entire baseline folder structure, `provider.php` (Joomla 4/5 DI), XML manifests, and entry points instantly.
```bash
joomla-rag scaffold component com_myextension
```
After scaffolding, you only need to edit the specific business logic or templates.

### 5. Validating Extensions (`joomla-rag validate`)
Before concluding a task that involved creating or modifying a Joomla extension, ensure the manifest and files are valid:
```bash
joomla-rag validate <path-to-extension>
```
This ensures all required tags are present and all files referenced in `<files>` or `<media>` tags actually exist.

### Instructions for the LLM:
1. When receiving the text response from the script, analyze from which `FILE` (`Source`) and `TOPIC` the answer came from.
2. Synthesize the information into a conversational and cohesive response for the user.
3. ALWAYS cite (and if possible, include links based on the file path) the original source of the read content.
4. If the user asks something broad (e.g., "how to create a whole component"), break down your reasoning and perhaps make more than one sequential search, or use the `grep`/`glob` tool directly in the `docs` folder if semantic RAG is not enough.
5. Always prefer searching in English.