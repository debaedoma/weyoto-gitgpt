# GPT Schema Changelog – Weyoto GitGPT

This file tracks versioned changes to the GPT schemas (gpt/schema/*.yaml) to keep AI tools, frontends, and backend integrations in sync.

---

## v1.0.0 – Initial Schema (GitHub MVP)

- Endpoint: `/query`
- Method: POST
- Required fields:
  - `repo_name`: GitHub repository (string)
  - `query`: Free-form question about repo content (string)
- Authentication via permanent API key (`x-api-key`)

✅ Status: Deprecated in v2.0.0.

---

## v2.0.0 – Multi-Source Schema Migration

- GitHub → `/query/github`, defined in `gpt/schema/github.yaml`
- Figma → `/query/figma`, defined in `gpt/schema/figma.yaml`
- Drive → `/query/drive`, defined in `gpt/schema/drive.yaml`
- Architecture updated:
  - One Custom GPT with multiple external actions.
  - All actions share the same permanent API key (`x-api-key`).

---

## v2.1.0 – Path Standardization and Actions Expansion

- GitHub → `/github/query`
- Figma → `/figma/query`
- Drive → `/drive/query`
- Unified multi-source schema under `/source/query` format (no "query" prefix anymore).
- GitHub available actions:
  - `fetch_file`
  - `list_files`
  - `get_latest_commit`
  - `list_user_repos`
- Permanent API key (`x-api-key`) required for all requests.

✅ Status: Active and stable.

---

## v2.2.0 – External API Enforcement + Secure Onboarding Update (April 2025)

### Schema Behavior Changes:

- All Custom GPTs must prioritize making **real-time external API calls** before attempting any memory-based reasoning.
- Action `summary` and `action` descriptions updated:
  - Must assume live external access by default.
  - Must read through specified repo or resource unless explicitly told otherwise.

### Impacts:

- Reduces hallucination by forcing real external database checks.
- Improves onboarding security by delaying API key visibility until full GitHub PAT setup is complete.
- Prepares system for scalable multi-source (Drive, Notion, Figma) authentication flows.

✅ Status: Active.
✅ No migration needed for existing users.

---

📝 Notes:
- Always keep schema changes synced across:
  - gpt/schema/*.yaml
  - gpt-schema-changelog.md
  - gpt-awareness.md (if structure impacts GPT usage patterns)

