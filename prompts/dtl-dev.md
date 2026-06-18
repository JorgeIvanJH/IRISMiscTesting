---
description: Build and validate an HL7v2 DTL in Dev.cls from input/expected fixtures
argument-hint: "[extra constraints]"
---
You are working in the current project.

Goal:
Create a working HL7v2 DTL transformation in `DTL Transformations/Dev.cls` so that:
- input: `Sample Messages/input.txt`
- transforms exactly to: `Sample Messages/expected.txt`

Requirements:
- Keep `DTL Transformations/Template.cls` unchanged.
- First copy `DTL Transformations/Template.cls` to `DTL Transformations/Dev.cls` (overwrite Dev if it already exists).
- Modify only `DTL Transformations/Dev.cls` for transformation logic.
- Keep the class as `Extends Ens.DataTransformDTL` and use valid XData DTL syntax.
- Do not modify `Sample Messages/input.txt` or `Sample Messages/expected.txt`.

Documentation requirements (read before and during edits):
- `Documentation/InterSystems IRIS for Health 2026.1/Interoperability/Interoperability Productions/`
- `Documentation/InterSystems IRIS for Health 2026.1/Interoperability/Interoperability Productions/Business Logic/DTL Transformations/`
- `Documentation/InterSystems IRIS for Health 2026.1/Interoperability/Interoperability Productions/Business Logic/DTL Transformations/DTL Reference/`
- `Documentation/InterSystems IRIS for Health 2026.1/Development/ObjectScript/`
- Follow relevant markdown cross-references when needed.

Validation loop (required after each significant change):
```bash
python3 ~/.pi/agent/skills/dtl-validate/scripts/dtl-validate.py \
  --dtl "DTL Transformations/Dev.cls" \
  --input "Sample Messages/input.txt" \
  --expected "Sample Messages/expected.txt"
```
- Iterate until validator exit code is `0`.
- Do not claim success unless exit code is `0`.

Authoring guidance:
- Prefer deterministic mappings from source fields.
- If fixture-specific literals are required (constants or fixed timestamps), add explicit DTL `<comment><annotation>...</annotation></comment>` near those `<assign>` actions explaining why.
- Avoid non-deterministic values (current time/random).

When done, provide:
1) final validator output proving PASS with exit code `0`
2) concise summary of key mappings, especially any literal assumptions.
3) confirmation that `DTL Transformations/Dev.cls` contains the final transform.

Extra user constraints: $@
