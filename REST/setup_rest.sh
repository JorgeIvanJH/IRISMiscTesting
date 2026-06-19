#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${IRIS_CONTAINER_NAME:-iris-experimentation}"
NAMESPACE="${IRIS_NAMESPACE:-USER}"
WEB_APP="${MLPIPELINE_REST_WEB_APP:-/api/mlpipeline}"
DISPATCH_CLASS="MLpipelineREST.disp"
REST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKG_DIR="${REST_DIR}/MLpipelineREST"
CONTAINER_DIR="/tmp/MLpipelineREST"

if ! docker ps --format '{{.Names}}' | grep -qx "${CONTAINER_NAME}"; then
  echo "IRIS container '${CONTAINER_NAME}' is not running" >&2
  exit 1
fi

if [[ ! -f "${PKG_DIR}/spec.cls" || ! -f "${PKG_DIR}/impl.cls" ]]; then
  echo "Expected ${PKG_DIR}/spec.cls and ${PKG_DIR}/impl.cls" >&2
  exit 1
fi

echo "Copying REST classes to ${CONTAINER_NAME}:${CONTAINER_DIR}"
docker exec -u root "${CONTAINER_NAME}" rm -rf "${CONTAINER_DIR}"
docker cp "${PKG_DIR}" "${CONTAINER_NAME}:${CONTAINER_DIR}"
docker exec -u root "${CONTAINER_NAME}" chmod -R a+rwX "${CONTAINER_DIR}"

echo "Importing and compiling MLpipelineREST classes in namespace ${NAMESPACE}"
docker exec -i "${CONTAINER_NAME}" bash <<BASH
set -euo pipefail
iris session IRIS -U "${NAMESPACE}" <<'EOF'
Set specFile="/tmp/MLpipelineREST/spec.cls"
Set implFile="/tmp/MLpipelineREST/impl.cls"
Write "Importing ",specFile,!
Set sc=\$System.OBJ.Import(specFile,"ck")
If \$System.Status.IsError(sc) { Write \$System.Status.GetErrorText(sc),! ZHALT 1 }
Write "Importing ",implFile,!
Set sc=\$System.OBJ.Import(implFile,"ck")
If \$System.Status.IsError(sc) { Write \$System.Status.GetErrorText(sc),! ZHALT 1 }
Write "Compiling MLpipelineREST.spec to regenerate dispatch class",!
Set sc=\$System.OBJ.Compile("MLpipelineREST.spec","ck")
If \$System.Status.IsError(sc) { Write \$System.Status.GetErrorText(sc),! ZHALT 1 }
Write "Compile completed",!
Halt
EOF
BASH

echo "Creating/updating REST web application ${WEB_APP}"
docker exec -i "${CONTAINER_NAME}" bash <<BASH
set -euo pipefail
iris session IRIS -U %SYS <<'EOF'
Set name="${WEB_APP}"
Set app=##class(Security.Applications).%OpenId(name)
If '\$IsObject(app) Set app=##class(Security.Applications).%New(),app.Name=name
Set app.NameSpace="${NAMESPACE}"
Set app.Enabled=1
Set app.Type=2
Set app.DispatchClass="${DISPATCH_CLASS}"
Set app.AutheEnabled=32
Set app.Recurse=1
Set app.ServeFiles=1
Set app.Description="REST API for MLpipeline.PointSamples and MLpipeline.Predictions"
Set sc=app.%Save()
If \$System.Status.IsError(sc) { Write \$System.Status.GetErrorText(sc),! ZHALT 1 }
Write "Web application ",name," maps to ",app.DispatchClass," in namespace ",app.NameSpace,!
Halt
EOF
BASH

echo "Exporting generated dispatch class to ${PKG_DIR}/disp.cls"
docker exec -i "${CONTAINER_NAME}" bash <<BASH
set -euo pipefail
iris session IRIS -U "${NAMESPACE}" <<'EOF'
Set sc=\$System.OBJ.ExportUDL("MLpipelineREST.disp.cls","/tmp/MLpipelineREST/disp.cls")
If \$System.Status.IsError(sc) { Write \$System.Status.GetErrorText(sc),! ZHALT 1 }
Write "Exported MLpipelineREST.disp",!
Halt
EOF
BASH
docker cp "${CONTAINER_NAME}:${CONTAINER_DIR}/disp.cls" "${PKG_DIR}/disp.cls"

echo "REST setup completed. Base URL: http://localhost:52773${WEB_APP}"
