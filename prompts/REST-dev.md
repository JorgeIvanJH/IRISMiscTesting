---
description: Build, validate, and document a REST service for InterSystems IRIS in the current project
argument-hint: "[extra constraints]"
---
You are working in the current project.

Goal:
Create a working REST service on the local InterSystems IRIS instance that supports GET, POST, and DELETE operations for the target tables in the `MLpipeline` schema.

Primary outcome:
The service must work end to end against the running Docker IRIS instance, not just compile successfully.

Requirements:
- Read the IRIS REST documentation in `isc-documentation/InterSystems IRIS for Health 2026.1/Development/REST Services/` before editing anything.
- Prefer a simple, reproducible implementation path.
- Keep the dispatch class generated or framework-managed when possible, and do not hand-edit generated code if the platform expects it to be regenerated.
- Put the service implementation in the project structure requested by the task.
- Put all IRIS setup steps needed to create the web application into a shell script so the setup can be repeated reliably.
- If the task requires manual portal steps that cannot be reproduced in terminal or script form, explain the blocker clearly and prefer a terminal-based equivalent if the documentation supports one.
- Keep changes limited to the REST service, its setup script, and its documentation unless a dependency forces an adjacent change.
- Do not introduce unrelated refactors.

Implementation guidance:
- Use the existing IRIS REST documentation as the source of truth for how to create or update the service.
- If the service is specification-first, generate from OpenAPI and then implement the business logic in the implementation class.
- If the service is manually coded, keep the dispatch class focused on routing and keep business logic in the implementation layer.
- Make request and response shapes explicit and deterministic.
- For any delete behavior, define whether the endpoint deletes by id, by key, or by a request body, and keep that contract consistent across code and tests.
- If authentication or authorization is required, define the exact access model and test it explicitly.

Required files to produce:
- A dispatch class placed at the requested REST location.
- A shell script that creates the IRIS web application and any supporting configuration needed for repeatability.
- A short markdown explanation of the approach in the REST folder.
- Any additional service classes needed for the implementation, tests, or documentation.

Validation loop:
After each significant change, run a validation cycle and do not proceed until it passes.

Validation success criteria:
- The service classes compile without errors.
- The web application exists and is mapped to the correct dispatch class.
- At least one GET request returns the expected data shape.
- At least one POST request creates or updates a record successfully.
- At least one DELETE request removes the expected record successfully.
- A follow-up GET confirms the delete actually happened.
- If the service uses security, unauthorized access fails and authorized access succeeds.
- The final documentation matches the implemented behavior.

Validation order:
1. Compile the changed classes.
2. Confirm the web application setup script runs successfully.
3. Exercise GET, POST, and DELETE against the live IRIS instance.
4. Confirm the underlying data changed as expected.
5. Repeat the failing step after any fix until the service passes all checks.

When done, provide:
1. The final validation output showing success.
2. A concise summary of the implemented endpoints and any assumptions.
3. Confirmation that the requested files were created and the service works against the running IRIS instance.

Extra user constraints: $@
