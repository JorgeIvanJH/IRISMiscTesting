---
name: mermaid-validate
description: >-
  Validate Mermaid diagrams by rendering them with mermaid-cli inside a running
  Docker container, returning PASS on successful render or exact CLI errors for
  iterative fixes.
compatibility: >-
  Requires Docker access (docker daemon permission) and a running mermaid-cli
  container. Supports explicit container names via `--container`
  (default: `mermaid-cli-local`). Container lifecycle is managed externally.
---

# Validate Mermaid diagrams with mermaid-cli

Use this skill when the user asks to create, check, or fix Mermaid diagrams.

This skill uses `mmdc` from a running container via `docker exec`, so the
feedback loop matches real render behavior.

## Primary tool

```bash
python3 scripts/mermaid-validate.py path/to/diagram.mmd
```

Use script paths relative to this skill directory (for example,
`scripts/mermaid-validate.py`) so the skill works when the repo is cloned
anywhere.

## Optional flags

```bash
python3 scripts/mermaid-validate.py path/to/diagram.mmd --container mermaid-cli-local
python3 scripts/mermaid-validate.py path/to/diagram.mmd --output path/to/output.svg
python3 scripts/mermaid-validate.py path/to/diagram.mmd --format svg
python3 scripts/mermaid-validate.py path/to/diagram.mmd --theme dark --background transparent
python3 scripts/mermaid-validate.py path/to/diagram.mmd --config path/to/config.json
python3 scripts/mermaid-validate.py path/to/diagram.mmd --css path/to/custom.css
python3 scripts/mermaid-validate.py path/to/diagram.mmd --check-only
python3 scripts/mermaid-validate.py path/to/diagram.mmd --verbose
```

## Exit codes

- `0` — render succeeded (diagram is valid for selected options)
- `1` — Mermaid/mmdc validation or render failure
- `2` — environment/setup failure (Docker, container state, mount/path mapping)

## Workflow

1. Confirm the target `.mmd` file path.
2. Ensure the target mermaid container is running (`--container`, default `mermaid-cli-local`).
3. Run validator script on the file.
4. If validation fails (exit code 1):
   - report exact `mmdc` output
   - apply minimal edits
   - re-run
5. If environment issues occur (exit code 2):
   - explain Docker/container/path fix
   - retry once environment is healthy

## Rules for agents

- Prefer this validator over hand-checking Mermaid syntax.
- Report exact `mmdc` error output when explaining failures.
- Keep fixes minimal and preserve user node IDs/text where possible.
- Do not claim success unless command exit code is 0.
