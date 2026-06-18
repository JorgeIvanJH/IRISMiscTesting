---
name: structurizr-dsl-validate
description: >-
  Validate Structurizr DSL using the official Structurizr Docker parser via a
  running container.
compatibility: >-
  Requires Docker access (docker daemon permission) and a running Structurizr
  container. Supports explicit container names via `--container`
  (default: `structurizr-local`). Container lifecycle is managed externally.
---

# Validate Structurizr DSL (Official Parser)

Use this skill when the user asks to check or validate Structurizr DSL with official tooling.

This skill uses the official Structurizr parser from the `structurizr/structurizr` container, executed via `docker exec` against a running container name you choose (or `structurizr-local` by default).

## Why this skill

This uses official Structurizr parsing/validation behavior, matching local/server rendering more closely than third-party parsers.

## Practical caveat

Use this skill to get to a passable initial diagram quickly (model-first and simple views), then add richer layout/styling iteratively.

## Primary tool

```bash
python3 scripts/structurizr-validate.py <file.dsl>
```

Use script paths relative to this skill directory (for example, `scripts/structurizr-validate.py`) so the skill works when the repo is cloned anywhere.

## Optional flags

```bash
python3 scripts/structurizr-validate.py <file.dsl> --container structurizr-local
python3 scripts/structurizr-validate.py <file.dsl> --container my-structurizr-container
python3 scripts/structurizr-validate.py <file.dsl> --container-path /usr/local/structurizr/workspace.dsl
python3 scripts/structurizr-validate.py <file.dsl> --docker-bin docker
python3 scripts/structurizr-validate.py <file.dsl> --verbose
```

## Workflow

1. Confirm the target `.dsl` file path.
2. Ensure the target Structurizr container is running (`--container`, default `structurizr-local`).
3. Run validator script on the file.
4. If validation fails:
   - report exact official parser output
   - suggest minimal edits
5. If Docker permission/container issues occur:
   - explain how to fix Docker access
   - ask the user to start the target container, or pass `--container <name>` for their environment

## Rules for agents

- Prefer this official validator over third-party parsers when available.
- Report exact command output on failures.
- Keep fixes minimal and preserve identifiers/view keys.
- Do not claim success unless command exit code is 0.
