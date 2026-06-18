# [Health Insight Consistency Check REST API](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_checkrest#HSAAREF_checkrest)

This reference section provides information on the REST services associated with the Health Insight [Consistency Check Tool](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency). In the following example calls, replace the host name and port, such as `localhost:57773`, with values appropriate to your system.

Only users with the %HSAA_Operator role can call endpoints in the Consistency Check REST API.

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

*   [POST /GenReportAsync/:days?TypeFilter=:TypeFilter&FacilityFilter=:FacilityFilter](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_checkrest_genreport) – Creates a background job to generate a Consistency Check report.
*   [GET /GetReport/:reportID](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_checkrest_getreport) – Gets the status or result of the Consistency Check report with the given report ID.
*   [POST /WriteLatestToFile?path=:path](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_checkrest_write) – Writes the latest Consistency Check report to a file.
*   [GET /SearchReport/:type/:facility/:time/:latestreport](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_checkrest_search) – Searches Consistency Check reports based on input parameters and returns the results.
*   [GET /LowerMatch/:latestreport](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_checkrest_lowermatch) – Returns rows of the HSAA.ConsistencyCheck.Report table with a MRN Cnt Ratio (HI/Edge) value of less than 90% (for patients) or a ENC Cnt Ratio (HI/Edge) value of less than 90% (for encounters).
*   [DELETE /DeleteReport/:day](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_checkrest_delete) – Deletes Consistency Check reports.
