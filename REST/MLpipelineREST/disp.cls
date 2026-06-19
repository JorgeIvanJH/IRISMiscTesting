/// REST API for the MLpipeline.PointSamples and MLpipeline.Predictions tables.
/// Dispatch class defined by RESTSpec in MLpipelineREST.spec
Class MLpipelineREST.disp Extends %CSP.REST [ GeneratedBy = MLpipelineREST.spec.cls, ProcedureBlock ]
{

Parameter CONTENTTYPE = "application/json";

/// The class containing the RESTSpec which generated this class
Parameter SpecificationClass = "MLpipelineREST.spec";

/// Ignore any writes done directly by the REST method.
Parameter IgnoreWrites = 1;

/// By default convert the input stream to Unicode
Parameter CONVERTINPUTSTREAM = 1;

XData UrlMap [ XMLNamespace = "http://www.intersystems.com/urlmap" ]
{
<Routes>
  <!-- List point samples -->
  <Route Url="/points" Method="get" Call="listPoints" />
  <!-- Create a point sample -->
  <Route Url="/points" Method="post" Call="createPoint" />
  <!-- Get a point sample by ID -->
  <Route Url="/points/:id" Method="get" Call="getPoint" />
  <!-- Delete a point sample by ID -->
  <Route Url="/points/:id" Method="delete" Call="deletePoint" />
  <!-- List predictions -->
  <Route Url="/predictions" Method="get" Call="listPredictions" />
  <!-- Create a prediction -->
  <Route Url="/predictions" Method="post" Call="createPrediction" />
  <!-- Get a prediction by ID -->
  <Route Url="/predictions/:id" Method="get" Call="getPrediction" />
  <!-- Delete a prediction by ID -->
  <Route Url="/predictions/:id" Method="delete" Call="deletePrediction" />
  <!-- Service health check -->
  <Route Url="/health" Method="get" Call="health" />
</Routes>
}

/// List point samples
ClassMethod listPoints() As %Status
{
    Try {
        Do ##class(%REST.Impl).%SetContentType("application/json")
        If '##class(%REST.Impl).%CheckAccepts("application/json") {
            Try {
                Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            } Catch {
                Do ##class(%REST.Impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            }
            Quit
        }
        Set response=##class(MLpipelineREST.impl).listPoints()
        Do ##class(MLpipelineREST.impl).%WriteResponse(response)
    } Catch (ex) {
        Try {
            Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        } Catch {
            Do ##class(%REST.Impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        }
    }
    Quit $$$OK
}

/// Create a point sample
ClassMethod createPoint() As %Status
{
    Try {
        Do ##class(%REST.Impl).%SetContentType("application/json")
        If '##class(%REST.Impl).%CheckAccepts("application/json") {
            Try {
                Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            } Catch {
                Do ##class(%REST.Impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            }
            Quit
        }
        Set response=##class(MLpipelineREST.impl).createPoint()
        Do ##class(MLpipelineREST.impl).%WriteResponse(response)
    } Catch (ex) {
        Try {
            Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        } Catch {
            Do ##class(%REST.Impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        }
    }
    Quit $$$OK
}

/// Get a point sample by ID
ClassMethod getPoint(pid As %String) As %Status
{
    Try {
        Do ##class(%REST.Impl).%SetContentType("application/json")
        If '##class(%REST.Impl).%CheckAccepts("application/json") {
            Try {
                Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            } Catch {
                Do ##class(%REST.Impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            }
            Quit
        }
        If ($number(pid,"I",-9223372036854775808,9223372036854775807)="") Do ##class(%REST.Impl).%ReportRESTError(..#HTTP400BADREQUEST,$$$ERROR($$$RESTInvalid,"id",pid)) Quit
        Set response=##class(MLpipelineREST.impl).getPoint(pid)
        Do ##class(MLpipelineREST.impl).%WriteResponse(response)
    } Catch (ex) {
        Try {
            Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        } Catch {
            Do ##class(%REST.Impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        }
    }
    Quit $$$OK
}

/// Delete a point sample by ID
ClassMethod deletePoint(pid As %String) As %Status
{
    Try {
        Do ##class(%REST.Impl).%SetContentType("application/json")
        If '##class(%REST.Impl).%CheckAccepts("application/json") {
            Try {
                Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            } Catch {
                Do ##class(%REST.Impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            }
            Quit
        }
        If ($number(pid,"I",-9223372036854775808,9223372036854775807)="") Do ##class(%REST.Impl).%ReportRESTError(..#HTTP400BADREQUEST,$$$ERROR($$$RESTInvalid,"id",pid)) Quit
        Set response=##class(MLpipelineREST.impl).deletePoint(pid)
        Do ##class(MLpipelineREST.impl).%WriteResponse(response)
    } Catch (ex) {
        Try {
            Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        } Catch {
            Do ##class(%REST.Impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        }
    }
    Quit $$$OK
}

/// List predictions
ClassMethod listPredictions() As %Status
{
    Try {
        Do ##class(%REST.Impl).%SetContentType("application/json")
        If '##class(%REST.Impl).%CheckAccepts("application/json") {
            Try {
                Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            } Catch {
                Do ##class(%REST.Impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            }
            Quit
        }
        Set response=##class(MLpipelineREST.impl).listPredictions()
        Do ##class(MLpipelineREST.impl).%WriteResponse(response)
    } Catch (ex) {
        Try {
            Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        } Catch {
            Do ##class(%REST.Impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        }
    }
    Quit $$$OK
}

/// Create a prediction
ClassMethod createPrediction() As %Status
{
    Try {
        Do ##class(%REST.Impl).%SetContentType("application/json")
        If '##class(%REST.Impl).%CheckAccepts("application/json") {
            Try {
                Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            } Catch {
                Do ##class(%REST.Impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            }
            Quit
        }
        Set response=##class(MLpipelineREST.impl).createPrediction()
        Do ##class(MLpipelineREST.impl).%WriteResponse(response)
    } Catch (ex) {
        Try {
            Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        } Catch {
            Do ##class(%REST.Impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        }
    }
    Quit $$$OK
}

/// Get a prediction by ID
ClassMethod getPrediction(pid As %String) As %Status
{
    Try {
        Do ##class(%REST.Impl).%SetContentType("application/json")
        If '##class(%REST.Impl).%CheckAccepts("application/json") {
            Try {
                Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            } Catch {
                Do ##class(%REST.Impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            }
            Quit
        }
        If ($number(pid,"I",-9223372036854775808,9223372036854775807)="") Do ##class(%REST.Impl).%ReportRESTError(..#HTTP400BADREQUEST,$$$ERROR($$$RESTInvalid,"id",pid)) Quit
        Set response=##class(MLpipelineREST.impl).getPrediction(pid)
        Do ##class(MLpipelineREST.impl).%WriteResponse(response)
    } Catch (ex) {
        Try {
            Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        } Catch {
            Do ##class(%REST.Impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        }
    }
    Quit $$$OK
}

/// Delete a prediction by ID
ClassMethod deletePrediction(pid As %String) As %Status
{
    Try {
        Do ##class(%REST.Impl).%SetContentType("application/json")
        If '##class(%REST.Impl).%CheckAccepts("application/json") {
            Try {
                Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            } Catch {
                Do ##class(%REST.Impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            }
            Quit
        }
        If ($number(pid,"I",-9223372036854775808,9223372036854775807)="") Do ##class(%REST.Impl).%ReportRESTError(..#HTTP400BADREQUEST,$$$ERROR($$$RESTInvalid,"id",pid)) Quit
        Set response=##class(MLpipelineREST.impl).deletePrediction(pid)
        Do ##class(MLpipelineREST.impl).%WriteResponse(response)
    } Catch (ex) {
        Try {
            Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        } Catch {
            Do ##class(%REST.Impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        }
    }
    Quit $$$OK
}

/// Service health check
ClassMethod health() As %Status
{
    Try {
        Do ##class(%REST.Impl).%SetContentType("application/json")
        If '##class(%REST.Impl).%CheckAccepts("application/json") {
            Try {
                Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            } Catch {
                Do ##class(%REST.Impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts))
            }
            Quit
        }
        Set response=##class(MLpipelineREST.impl).health()
        Do ##class(MLpipelineREST.impl).%WriteResponse(response)
    } Catch (ex) {
        Try {
            Do ##class(MLpipelineREST.impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        } Catch {
            Do ##class(%REST.Impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus(),$parameter("MLpipelineREST.impl","ExposeServerExceptions"))
        }
    }
    Quit $$$OK
}

}
