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

- Custom GPTs interact via the `/query` endpoint
- A YAML schema will be generated at: `gpt/schema.yaml`
- All schema updates must be versioned in `gpt-schema-changelog.md`

---

## Rate Limits & Plans

- Free users: 1,000 requests/month
- Pro users: unlimited
- Upgrade prompts are shown via GPT error messages returned from backend

---
