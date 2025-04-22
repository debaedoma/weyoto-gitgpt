# GPT Awareness Notes for Weyoto GitGPT (MVP)

This file documents the system behaviors and external logic that GPT tools and AI assistants must be aware of, beyond what is visible in code.

---

## Deployment (MVP)

- Project is currently running on dev/staging via **Render**
- No production deployment yet
- Environment variables will be managed via **system-level environment variables** (not .env file)
- Local development is on Windows 11 and **Cloudflare Tunnel** exposes local APIs to the web

---

## GitHub Integration (MVP)

- Users are required to paste their **Fine-grained GitHub Personal Access Token (PAT)**
- Minimum required scopes:
  - `repo`
  - `read:org`
- Repository permissions:
  - `Read-only access to contents (repository contents, commits, branches, downloads, releases, and mergers)`
  - `Read-only access to "Commit status"`
  - `Read-only access to Metadata (default and mandatory)`
- Scopes should be listed in onboarding UI and enforced in documentation
- Data is pulled live using the token (nothing stored)

---

## Environment Variables (Declared in system, not .env file)

- `WEYOTO_GITGPT_DATABASE_URL`
- `WEYOTO_API_KEY_SECRET`
- `WEYOTO_ALLOWED_ORIGINS`
- `RESEND_API_KEY`
- `EMAIL_SENDER`

---

## API Schema

- Each data source has its own query endpoint:
  - GitHub → `/github/query`
  - Figma → `/figma/query`
  - Drive → `/query/drive`
- Each data source is exposed as a separate **action** inside one Custom GPT, using its own YAML schema and endpoint (e.g., `/github/query`, `/figma/query`, etc.). All actions share the same permanent API key.
- This enables better modularity, rate-limiting, error handling, and simplicity for GPT creators
- Schema definitions live in: `gpt/schema/github.yaml`, `gpt/schema/figma.yaml`, etc.
- All schema updates must be versioned in `gpt-schema-changelog.md`

---

## Rate Limits & Plans

- Free users: 30 requests requests/per day
- Pro users: unlimited at $1/month
- Upgrade prompts are shown via GPT error messages returned from backend

---

## Currently Supported GPT Actions

### GitHub (query_github)
- Unified route: `/query/github`
- Uses the same API key and user token from DB
- `action` field determines behavior

#### Available actions:
| Name | Description |
|------|-------------|
| `fetch_file` | Get raw content of one file |
| `list_files` | List all files in a repo |
| `get_latest_commit` | Get latest commit message and author |

---

## Environment Variables (Declared in system)

- `WEYOTO_GITGPT_DATABASE_URL`
- `WEYOTO_API_KEY_SECRET`
- `WEYOTO_ALLOWED_ORIGINS`
- `RESEND_API_KEY`
- `EMAIL_SENDER`

---

## User Registration Method

Weyoto GitGPT uses **passwordless email authentication**.

### Flow:
1. User submits their email to `/auth/request-code`
2. A short verification code (6 digits) is emailed to them
3. User submits the code to `/auth/verify-code`
4. If successful, they are returned their API key and can start using the system

This method is universal and lightweight. It works across GPT tools, frontend apps, and CLI.

No GitHub login or password is required. OAuth may be added later for GitHub token management.
