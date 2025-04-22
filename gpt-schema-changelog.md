# GPT Schema Changelog – Weyoto GitGPT

This file tracks versioned changes to the GPT schema (gpt/schema.yaml) to keep AI tools in sync with backend API behavior.

---

## v1.0.0 – Initial Schema (GitHub MVP)

- Endpoint: `/query`
- Method: POST
- Required fields:
  - `repo_name`: GitHub repository (string)
  - `query`: Free-form question about repo content (string)
- Authentication via permanent API key (`x-api-key`)


## v2.0.0 – Multi-source Schema Migration

- GitHub → `/query/github`, defined in `gpt/schema/github.yaml`
- Figma → `/query/figma`, defined in `gpt/schema/figma.yaml`
- Drive → `/query/drive`, defined in `gpt/schema/drive.yaml`
- Architecture updated to use one Custom GPT with multiple actions
- All actions share the same permanent API key (`x-api-key`)

## v2.1.0 – Multi-source Schema Migration

- GitHub → `/query/github`, changed to `/github/query`
- Figma → `/query/figma`, changed to `/figma/query`
- Drive → `/query/drive`, changed to `drive/query`
- Unified with one Custom GPT and multiple actions
- All actions share the same permanent API key (`x-api-key`)
### GitHub Actions:
- `fetch_file`
- `list_files`
- `get_latest_commit`
- `list_user_repos`


📝 Deprecated:
- `v1.0.0` schema with `repo_name` and `query` is no longer used.