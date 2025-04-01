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
