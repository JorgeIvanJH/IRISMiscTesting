# MLpipeline REST service

This folder contains a specification-first InterSystems IRIS REST service for the `MLpipeline` SQL schema.

## Files

- `MLpipelineREST/spec.cls` — `%REST.Spec` class containing the OpenAPI 2.0 contract.
- `MLpipelineREST/impl.cls` — `%REST.Impl` business logic class. This is the class to edit for endpoint behavior.
- `MLpipelineREST/disp.cls` — generated `%CSP.REST` dispatch class exported from IRIS after compiling `MLpipelineREST.spec`. Do not hand-edit this file; regenerate it with `./REST/setup_rest.sh`.
- `setup_rest.sh` — repeatable setup script that imports/compiles the service, creates or updates the IRIS web application, and exports the generated dispatch class.

## Setup

Run from the repository root while the `iris-experimentation` container is running:

```bash
REST/setup_rest.sh
```

Defaults:

- Container: `iris-experimentation` (`IRIS_CONTAINER_NAME` overrides this)
- Namespace: `USER` (`IRIS_NAMESPACE` overrides this)
- Web application: `/api/mlpipeline` (`MLPIPELINE_REST_WEB_APP` overrides this)
- Dispatch class: `MLpipelineREST.disp`

The web application is configured as a REST application with password authentication enabled. Use an IRIS account with access to the `USER` namespace, for example the local development `SuperUser` account configured by `.env`.

## Endpoints

Base URL: `http://localhost:52773/api/mlpipeline`

### Health

- `GET /health`
- Response: `{"status":"ok","service":"MLpipelineREST","schema":"MLpipeline"}`

### Point samples (`MLpipeline.PointSamples`)

- `GET /points` — returns up to 50 rows ordered by `ID`:
  - Shape: `{"table":"PointSamples","count":number,"items":[{"id", "datetime", "x", "y", "label"}]}`
- `GET /points/{id}` — returns one point sample by integer `ID`.
- `POST /points` — creates one point sample. Required JSON fields are numeric `x` and `y`; optional fields are `label` and `datetime`.
  - Example body: `{"x":123.45,"y":67.89,"label":"t","datetime":"2026-06-19 14:48:00"}`
  - Success status: `201 Created`, returning the created row.
- `DELETE /points/{id}` — deletes one point sample by integer `ID`.
  - Success response: `{"deleted":true,"table":"PointSamples","id":id}`

### Predictions (`MLpipeline.Predictions`)

- `GET /predictions` — returns up to 50 rows ordered by `ID`:
  - Shape: `{"table":"Predictions","count":number,"items":[{"id", "datetime", "pointsId", "labelPred", "modelRunId", "inferenceTime"}]}`
- `GET /predictions/{id}` — returns one prediction by integer `ID`.
- `POST /predictions` — creates one prediction. Required JSON field is integer `pointsId`; optional fields are `labelPred`, `modelRunId`, `inferenceTime`, and `datetime`.
  - Example body: `{"pointsId":1,"labelPred":"a","modelRunId":"manual-test","inferenceTime":0.01}`
  - Success status: `201 Created`, returning the created row.
- `DELETE /predictions/{id}` — deletes one prediction by integer `ID`.

Delete behavior is always by path `id`; request bodies are not used for delete operations.

## Quick validation commands

```bash
BASE=http://localhost:52773/api/mlpipeline
AUTH='SuperUser:SYS'

curl -u "$AUTH" "$BASE/health"
curl -u "$AUTH" "$BASE/points"
created=$(curl -sS -u "$AUTH" -H 'Content-Type: application/json' \
  -X POST "$BASE/points" \
  -d '{"x":123.45,"y":67.89,"label":"t","datetime":"2026-06-19 14:48:00"}')
id=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])' <<<"$created")
curl -u "$AUTH" "$BASE/points/$id"
curl -u "$AUTH" -X DELETE "$BASE/points/$id"
curl -i -u "$AUTH" "$BASE/points/$id"
```

The final GET should return `404 Not Found`, confirming the delete.
