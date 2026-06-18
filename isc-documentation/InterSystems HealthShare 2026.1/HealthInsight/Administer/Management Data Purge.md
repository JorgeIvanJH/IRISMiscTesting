# [Purging Management Data in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_purgedata#HSAAADM_purgedata)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq)

The HealthShare Health Insight instance stores some management data outside of the Health Insight production. This data consists of the following:

*   Performance data, which is used in the Platform Information dashboards
    
*   Health Insight log
    

The production management tools ignore this data. Health Insight provides a separate user interface that you can use to purge this data when it is no longer needed. To purge this data:

1.  Open the Management Portal.
    
2.  Switch to the analytics namespace, typically `ANALYTICS` or `HSANALYTICS`.
    
3.  Select `HealthShare`.
    
4.  Select `Internal Data Management` > `Table Maintenance`.
    
5.  To purge performance data, select `Purge Summary Tables`. By default, the last seven days of data are kept; to change this, type an integer into `Days to Keep`. Then select `Purge Data`.
    
6.  To purge the Health Insight log, select `Purge Logging Tables`. By default, the last seven days of data are kept; to change this, type an integer into `Days to Keep`. Then select `Purge Data`.
    

(For information on `Internal Data Management` > `Patient Error Management`, see “[Streamlet Processing Errors](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_streamletprocerrr)” earlier in this book.)

> **Important:**
> 
> If the Health Insight log (specifically the table `HSAA_Report.Log`) becomes too large, the `Table Maintenance` page can time out. Therefore, it is best practice to keep no more than 2 million rows in this table. If you receive a timeout error when viewing the `Table Maintenance` page, open the Terminal on the Analytics instance, switch to the Analytics namespace, and enter the following commands:
> 
> ```objectscript
>  W ##class(HSAA.API.Data).PurgeLogTable(pOlderThanDays)
>  W ##class(HSAA.API.Data).ResetReportData(pOlderThanDays)
> ```
> 
> Where `pOlderThanDays` is an integer that specifies the number of days of records to keep (the most recent).
