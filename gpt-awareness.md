# GPT Awareness Notes for Weyoto GitGPT (MVP)

This file documents the system behaviors and external logic that GPT tools and AI assistants must be aware of, beyond what is visible in code.

---

## Deployment (MVP)

- Project is currently running locally via **Cloudflare Tunnel**
- No production deployment yet
- Environment variables will be managed via **system-level environment variables** (not .env file)

---

## GitHub Integration (MVP)

- Users are required to paste their **GitHub Personal Access Token (PAT)**
- Minimum required scopes:
  - `repo`
  - `read:org`
- Scopes should be listed in onboarding UI and enforced in documentation
- Data is pulled live using the token (nothing stored)

---

## Environment Variables (Declared in system, not .env file)

- `WEYOTO_GITGPT_DATABASE_URL`
- `WEYOTO_API_KEY_SECRET`
- `WEYOTO_ALLOWED_ORIGINS`

---

## API Schema

- Each data source has its own query endpoint:
  - GitHub → `/query/github`
  - Figma → `/query/figma`
  - Drive → `/query/drive`
- Each data source is exposed as a separate **action** inside one Custom GPT, using its own YAML schema and endpoint (e.g., `/query/github`, `/query/figma`, etc.). All actions share the same permanent API key.
- This enables better modularity, rate-limiting, error handling, and simplicity for GPT creators
- Schema definitions live in: `gpt/schema/github.yaml`, `gpt/schema/figma.yaml`, etc.
- All schema updates must be versioned in `gpt-schema-changelog.md`

---

## Rate Limits & Plans

- Free users: 1,000 requests/month
- Pro users: unlimited
- Upgrade prompts are shown via GPT error messages returned from backend

---

## ✅ Currently Supported GPT Actions

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

