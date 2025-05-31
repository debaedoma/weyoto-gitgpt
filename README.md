## 🧠 AI Integration Notes

Weyoto GitGPT is designed to be AI-aware and AI-co-pilot compatible. Any GPT (including yourself, ChatGPT, custom GPTs, or plugin tools) should:

1. **Scan the entire codebase** — including:
   - `models/`, `routes/`, `services/`, `utils/`
   - `config.py`, `app.py`, and all Blueprint registrations
   - `requirements.txt`, `.env`, `.env.defaults`

2. **Check metadata files**:
   - `gpt-awareness.md` (system rules, setup steps)
   - `system_config.yaml` (auth scopes, env keys, schema paths)

3. **Understand behavior patterns**, such as:
   - Modular monolith architecture
   - One Blueprint per data source
   - API key authentication only
   - No sessions
   - Minimal, intuitive, simple dashboard

4. **Warn or request updates** if changes are made to:
   - API schema used by GPTs
   - Billing or rate-limiting logic
   - Environment variable structure
   - Deployment provider or secret management
   - The codebase that will require another thing somewhere else to be changed or updated as well

5. **Ensure GPT schema consistency**:
   - All data sources (e.g., GitHub, Server, Figma, Drive) are exposed as distinct **paths** within a single GPT action schema.  
   - Each tool is registered under a separate `/{source}/query` path inside a unified OpenAPI YAML file (e.g., `gpt/schema/combined.yaml`). 
   - The Custom GPT defines only **one action**, with multiple sub-actions handled via `operationId` and path-based routing.
   
   This structure solves GPT Builder's limitation of “duplicate domain” errors, and enables multi-source querying from a single GPT endpoint.

   All tools share:
      - A single base URL (e.g., `https://gitgpt-api.weyoto.com`)
      - One API key per user
      - Modular backend endpoints like:
        - `/github/query`
        - `/server/query`
        - `/figma/query` (future)

## ✅ Supported GPT Actions

Currently supported GitHub actions via `/github/query`:

| Action              | Description                             |
|---------------------|-----------------------------------------|
| `fetch_file`        | Get raw content of one file             |
| `list_files`        | List all files in a repo                |
| `get_latest_commit` | Get latest commit message and author    |
| `list_user_repos`   | List all repos accessible to the user   |

> Note: Actual route is `/github/query` (not `/query/github`).

## 🌱 Required Environment Variables

Ensure the following env vars are set **at the system level**:

- `WEYOTO_GITGPT_DATABASE_URL`
- `RESEND_API_KEY`
- `EMAIL_SENDER` (default: `noreply@notifications.weyoto.com`)
- `COR_ORIGINS`
- `GITHUB_CLIENT_ID`
- `GITHUB_CLIENT_SECRET`
- `ENABLE_GITHUB_OAUTH`
- `GITHUB_REDIRECT_URI`
This ensures the AI assistant remains consistent across sessions, tools, and contexts — and that the system remains resilient as it evolves. 

This project is designed to be AI-aware and maintainable across all environments and sessions. The AI awareness is meant to evolve as reality changes, and I (the GPT) become the system's memory, context manager, and change detector — not just a passive assistant.

## 📌 AI Instruction Rule

Any AI tool, GPT assistant, or plugin interacting with this repo must:

- Read the full codebase and the files listed below
- Keep `requirements.txt`, `gpt-awareness.md`, `system_config.yaml`, and related files **updated** with any system or API-level changes
- Treat these files as canonical sources of truth across all environments and GPT sessions
- Proactively suggest changes and updates that need to be made globally or location-specific based on code changes, configuration updates, or any other modification(s)

Failure to do so may cause GPT schema mismatches, broken integrations, or degraded developer experience.

## ⚠️ This File Must Be Updated When:

- A new integration is added (e.g., Sheets, Drive, Notion)
- Auth mechanisms change (e.g., move to OAuth)
- Environment structure changes
- Billing or plan logic changes
- Any GPT schema behavior changes