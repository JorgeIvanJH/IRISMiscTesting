Class MLpipelineREST.impl Extends %REST.Impl [ ProcedureBlock ]
{

Parameter ExposeServerExceptions = 1;

ClassMethod health() As %DynamicObject
{
    Set response = {"status":"ok","service":"MLpipelineREST","schema":"MLpipeline"}
    Quit response
}

ClassMethod listPoints() As %DynamicObject
{
    Quit ..ListRows("PointSamples", "ID,x,y,label,datetime")
}

ClassMethod getPoint(id As %Integer) As %DynamicObject
{
    Quit ..GetRow("PointSamples", id)
}

ClassMethod createPoint() As %DynamicObject
{
    Set body = ..ReadBody()
    If '$IsObject(body) Quit ..Error(400, "Request body must be a JSON object")

    If '..HasNumber(body, "x") Quit ..Error(400, "Field 'x' is required and must be numeric")
    If '..HasNumber(body, "y") Quit ..Error(400, "Field 'y' is required and must be numeric")

    Set label = body.%Get("label")
    Set datetime = body.%Get("datetime")

    If datetime = "" {
        Set sql = "INSERT INTO MLpipeline.PointSamples (x,y,label) VALUES (?,?,?)"
        Set rs = ..Execute(sql, body.%Get("x"), body.%Get("y"), label)
    } Else {
        Set sql = "INSERT INTO MLpipeline.PointSamples (x,y,label,datetime) VALUES (?,?,?,?)"
        Set rs = ..Execute(sql, body.%Get("x"), body.%Get("y"), label, datetime)
    }

    If (rs.%SQLCODE < 0) Quit ..SQLError(400, rs)
    Set id = rs.%ROWID
    Do ..%SetStatusCode(201)
    Quit ..GetRow("PointSamples", id)
}

ClassMethod deletePoint(id As %Integer) As %DynamicObject
{
    Quit ..DeleteRow("PointSamples", id)
}

ClassMethod listPredictions() As %DynamicObject
{
    Quit ..ListRows("Predictions", "ID,PointsIDForeignKey,LabelPred,Modelrunid,InferenceTime,datetime")
}

ClassMethod getPrediction(id As %Integer) As %DynamicObject
{
    Quit ..GetRow("Predictions", id)
}

ClassMethod createPrediction() As %DynamicObject
{
    Set body = ..ReadBody()
    If '$IsObject(body) Quit ..Error(400, "Request body must be a JSON object")

    If '..HasInteger(body, "pointsId") Quit ..Error(400, "Field 'pointsId' is required and must be an integer")

    Set labelPred = body.%Get("labelPred")
    Set modelRunId = body.%Get("modelRunId")
    Set inferenceTime = body.%Get("inferenceTime")
    Set datetime = body.%Get("datetime")

    If inferenceTime = "" Set inferenceTime = 0

    If datetime = "" {
        Set sql = "INSERT INTO MLpipeline.Predictions (PointsIDForeignKey,LabelPred,Modelrunid,InferenceTime) VALUES (?,?,?,?)"
        Set rs = ..Execute(sql, body.%Get("pointsId"), labelPred, modelRunId, inferenceTime)
    } Else {
        Set sql = "INSERT INTO MLpipeline.Predictions (PointsIDForeignKey,LabelPred,Modelrunid,InferenceTime,datetime) VALUES (?,?,?,?,?)"
        Set rs = ..Execute(sql, body.%Get("pointsId"), labelPred, modelRunId, inferenceTime, datetime)
    }

    If (rs.%SQLCODE < 0) Quit ..SQLError(400, rs)
    Set id = rs.%ROWID
    Do ..%SetStatusCode(201)
    Quit ..GetRow("Predictions", id)
}

ClassMethod deletePrediction(id As %Integer) As %DynamicObject
{
    Quit ..DeleteRow("Predictions", id)
}

ClassMethod ListRows(table As %String, columns As %String) As %DynamicObject [ Private ]
{
    Set sql = "SELECT TOP 50 "_columns_" FROM MLpipeline."_table_" ORDER BY ID"
    Set rs = ##class(%SQL.Statement).%ExecDirect(, sql)
    If (rs.%SQLCODE < 0) Quit ..SQLError(500, rs)

    Set items = []
    While rs.%Next() {
        Do items.%Push(..RowObject(table, rs))
    }

    Set response = {}
    Do response.%Set("table", table)
    Do response.%Set("count", items.%Size())
    Do response.%Set("items", items)
    Quit response
}

ClassMethod GetRow(table As %String, id As %Integer) As %DynamicObject [ Private ]
{
    If id = "" Quit ..Error(400, "ID is required")

    If table = "PointSamples" {
        Set sql = "SELECT ID,x,y,label,datetime FROM MLpipeline.PointSamples WHERE ID=?"
    } Else {
        Set sql = "SELECT ID,PointsIDForeignKey,LabelPred,Modelrunid,InferenceTime,datetime FROM MLpipeline.Predictions WHERE ID=?"
    }

    Set rs = ..Execute(sql, id)
    If (rs.%SQLCODE < 0) Quit ..SQLError(500, rs)
    If 'rs.%Next() Quit ..Error(404, table_" row not found for id "_id)

    Quit ..RowObject(table, rs)
}

ClassMethod DeleteRow(table As %String, id As %Integer) As %DynamicObject [ Private ]
{
    If id = "" Quit ..Error(400, "ID is required")

    If table = "PointSamples" {
        Set existsSql = "SELECT ID FROM MLpipeline.PointSamples WHERE ID=?"
        Set deleteSql = "DELETE FROM MLpipeline.PointSamples WHERE ID=?"
    } Else {
        Set existsSql = "SELECT ID FROM MLpipeline.Predictions WHERE ID=?"
        Set deleteSql = "DELETE FROM MLpipeline.Predictions WHERE ID=?"
    }

    Set check = ..Execute(existsSql, id)
    If (check.%SQLCODE < 0) Quit ..SQLError(500, check)
    If 'check.%Next() Quit ..Error(404, table_" row not found for id "_id)

    Set rs = ..Execute(deleteSql, id)
    If (rs.%SQLCODE < 0) Quit ..SQLError(409, rs)

    Set response = {"deleted":true}
    Do response.%Set("table", table)
    Do response.%Set("id", id)
    Quit response
}

ClassMethod RowObject(table As %String, rs As %SQL.StatementResult) As %DynamicObject [ Private ]
{
    Set obj = {}
    Do obj.%Set("id", rs.%Get("ID"))
    Do obj.%Set("datetime", rs.%Get("datetime"))

    If table = "PointSamples" {
        Do obj.%Set("x", rs.%Get("x"))
        Do obj.%Set("y", rs.%Get("y"))
        Do obj.%Set("label", rs.%Get("label"))
    } Else {
        Do obj.%Set("pointsId", rs.%Get("PointsIDForeignKey"))
        Do obj.%Set("labelPred", rs.%Get("LabelPred"))
        Do obj.%Set("modelRunId", rs.%Get("Modelrunid"))
        Do obj.%Set("inferenceTime", rs.%Get("InferenceTime"))
    }

    Quit obj
}

ClassMethod ReadBody() As %DynamicObject [ Private ]
{
    Try {
        Set body = ##class(%DynamicObject).%FromJSON(%request.Content)
    } Catch ex {
        Set body = ""
    }
    Quit body
}

ClassMethod HasNumber(body As %DynamicObject, name As %String) As %Boolean [ Private ]
{
    If 'body.%IsDefined(name) Quit 0
    If body.%Get(name) = "" Quit 0
    Quit $IsValidNum(body.%Get(name))
}

ClassMethod HasInteger(body As %DynamicObject, name As %String) As %Boolean [ Private ]
{
    If '..HasNumber(body, name) Quit 0
    Quit (body.%Get(name) = +body.%Get(name))
}

ClassMethod Execute(sql As %String, p1 = "", p2 = "", p3 = "", p4 = "", p5 = "") As %SQL.StatementResult [ Private ]
{
    Set stmt = ##class(%SQL.Statement).%New()
    Set sc = stmt.%Prepare(sql)
    If $$$ISERR(sc) {
        Set rs = ##class(%SQL.StatementResult).%New()
        Set rs.%SQLCODE = -400
        Set rs.%Message = $System.Status.GetErrorText(sc)
        Quit rs
    }

    Set argCount = $Length(sql, "?") - 1
    If argCount = 0 Quit stmt.%Execute()
    If argCount = 1 Quit stmt.%Execute(p1)
    If argCount = 2 Quit stmt.%Execute(p1, p2)
    If argCount = 3 Quit stmt.%Execute(p1, p2, p3)
    If argCount = 4 Quit stmt.%Execute(p1, p2, p3, p4)
    Quit stmt.%Execute(p1, p2, p3, p4, p5)
}

ClassMethod Error(statusCode As %Integer, message As %String) As %DynamicObject [ Private ]
{
    Do ..%SetStatusCode(statusCode)
    Set response = {"error":true}
    Do response.%Set("message", message)
    Quit response
}

ClassMethod SQLError(statusCode As %Integer, rs As %SQL.StatementResult) As %DynamicObject [ Private ]
{
    Do ..%SetStatusCode(statusCode)
    Set response = {"error":true}
    Do response.%Set("sqlcode", rs.%SQLCODE)
    Do response.%Set("message", rs.%Message)
    Quit response
}

}
