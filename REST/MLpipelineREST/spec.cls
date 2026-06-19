Class MLpipelineREST.spec Extends %REST.Spec [ ProcedureBlock ]
{

Parameter CONTENTTYPE = "application/json";

XData OpenAPI [ MimeType = application/json ]
{
{
  "swagger": "2.0",
  "info": {
    "title": "MLpipeline REST API",
    "version": "1.0.0",
    "description": "REST API for the MLpipeline.PointSamples and MLpipeline.Predictions tables."
  },
  "basePath": "/api/mlpipeline",
  "consumes": ["application/json"],
  "produces": ["application/json"],
  "paths": {
    "/points": {
      "get": {
        "operationId": "listPoints",
        "summary": "List point samples",
        "responses": {"200": {"description": "Point sample list"}}
      },
      "post": {
        "operationId": "createPoint",
        "summary": "Create a point sample",
        "responses": {"201": {"description": "Created point sample"}, "400": {"description": "Invalid request"}}
      }
    },
    "/points/{id}": {
      "parameters": [
        {"name": "id", "in": "path", "required": true, "type": "integer", "format": "int64"}
      ],
      "get": {
        "operationId": "getPoint",
        "summary": "Get a point sample by ID",
        "responses": {"200": {"description": "Point sample"}, "404": {"description": "Not found"}}
      },
      "delete": {
        "operationId": "deletePoint",
        "summary": "Delete a point sample by ID",
        "responses": {"200": {"description": "Delete result"}, "404": {"description": "Not found"}}
      }
    },
    "/predictions": {
      "get": {
        "operationId": "listPredictions",
        "summary": "List predictions",
        "responses": {"200": {"description": "Prediction list"}}
      },
      "post": {
        "operationId": "createPrediction",
        "summary": "Create a prediction",
        "responses": {"201": {"description": "Created prediction"}, "400": {"description": "Invalid request"}}
      }
    },
    "/predictions/{id}": {
      "parameters": [
        {"name": "id", "in": "path", "required": true, "type": "integer", "format": "int64"}
      ],
      "get": {
        "operationId": "getPrediction",
        "summary": "Get a prediction by ID",
        "responses": {"200": {"description": "Prediction"}, "404": {"description": "Not found"}}
      },
      "delete": {
        "operationId": "deletePrediction",
        "summary": "Delete a prediction by ID",
        "responses": {"200": {"description": "Delete result"}, "404": {"description": "Not found"}}
      }
    },
    "/health": {
      "get": {
        "operationId": "health",
        "summary": "Service health check",
        "responses": {"200": {"description": "Health response"}}
      }
    }
  }
}
}

}
