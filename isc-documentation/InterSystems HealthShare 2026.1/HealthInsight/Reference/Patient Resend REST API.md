# [Health Insight Patient Resend REST API](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_resendpat#HSAAREF_resendpat)

This reference section provides information on the REST services associated with the `Resend Patient To Health Insight` page. In the following example calls, replace the host name and port, such as `localhost:57773`, with values appropriate to your system.

Only users with the %HSAA_Operator role can call this REST API.

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

*   [POST /Resend/:UseMPIID/:IDLIST](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_resendpat_resend) – Resends a comma-separated list of patients, identified by MPIID or HSAAID, with high priority.
