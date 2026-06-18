---
name: iris-dtl-validate
description: >-
  Validate an InterSystems IRIS for Health DTL transformation by running it
  against an HL7 v2 input/expected pair inside a real IRIS for Health
  Community Edition container, and reporting either a clean PASS or a diff
  that the agent can use to refine the DTL.
compatibility: >-
  Requires Docker access (docker daemon permission) and a running IRIS for
  Health container. Supports explicit container names via `--container`
  (default: `iris-dtl-validate`). Container lifecycle is managed externally.
---

# Validate a DTL against an HL7 input/expected pair

Use this skill when the user gives you (a) an HL7 v2 sample message, (b) an HL7 v2 expected message, and (c) a single `.cls` file containing a DTL that should transform (a) into (b). The skill is the feedback loop: write a candidate DTL, run the validator, read the diff, refine, repeat.

Reference the DTL documentation under `Documentation/InterSystems IRIS for Health 2026.1/Interoperability/Interoperability Productions/Business Logic/DTL Transformations/` for syntax and action semantics; that is the authoring contract this validator measures against.

## Scope (v1)

- **HL7 v2 only:** parsed `<transform sourceClass='...'>` must be `EnsLib.HL7.Message`, otherwise the validator fails with `v1 supports HL7v2 only`.
- **Exactly one `.cls` file** is loaded per run. That file must contain a class extending `Ens.DataTransformDTL`. No helper class loading in v1.
- The validator auto-detects `sourceDocType` from the DTL `<transform ...>` attributes and passes it into the runner (which sets `source.DocType` only if the imported message does not already have one).

## Primary tool

```bash
python3 scripts/iris-dtl-validate.py \
    --dtl path/to/MyDTL.cls \
    --input path/to/input.txt \
    --expected path/to/expected.txt
```

Use script paths relative to this skill directory (for example, `scripts/iris-dtl-validate.py`) so the skill works when the repo is cloned anywhere.

Optional flags:

```bash
  --container NAME    Running container name to use (default: iris-dtl-validate)
  --keep-output PATH  Write the produced HL7 message to PATH on the host
  --verbose           Print every docker / iris session command being run
```

Container behavior:

- Pass `--container <name>` to target a specific running IRIS container.
- If omitted, the default container name `iris-dtl-validate` is used.
- The script requires the container to already exist and be running.

## Exit codes

- `0` — DTL compiled, ran, and produced byte-identical output (modulo `\r`↔`\n` and trailing-newline normalisation).
- `1` — DTL compiled and ran, but output differs from expected. The unified diff is printed.
- `2` — DTL did not compile, or the runner threw at runtime. The IRIS error is printed.
- `3` — Environment problem (Docker missing/permission denied, container missing or not running, etc.).

## Workflow for an agent

1. Write a candidate DTL into a single `.cls` file (start from a template like `Test.cls` if one is provided).
2. Ensure the target IRIS container is running (`--container`, default `iris-dtl-validate`).
3. Run the validator. Read its output.
4. If exit code 2: fix the compilation/runtime error reported by IRIS and try again.
5. If exit code 1: read the unified diff. Each `-`/`+` pair tells you which segment+field of the produced message disagrees with the expected message. Adjust the DTL (`<assign>`, `<if>`, function call, literal) and re-run.
6. If exit code 0: stop.

## Determinism

The validator imposes **no** test hooks. If your DTL produces non-deterministic output (e.g. you used a wall-clock function), the diff will fail every run. The fix is to look at the input/expected pair and use a deterministic source for that field — a literal, a property of the source message, or a deterministic function — whatever the pair implies.

## Rules for agents

- Prefer this validator over reasoning about DTL output by hand.
- Always read the documentation under `DTL Transformations/` before authoring; it is the authoritative reference for action syntax (`<assign>`, `<if>`, `<foreach>`, virtual property paths like `{PID:PatientName(1)}`, etc.).
- Report the validator's exact diff or error text when explaining failures to the user.
- Do not claim the DTL is correct unless the validator exits 0.
- Do not edit the input or expected fixture to make the test pass.
