# [When a Health Insight Mirror Fails Over](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_onfailover#HSAAADM_onfailover)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq).

If yourHealthShare Health Insight instance is mirrored, if the primary server fails over, it is necessary to tune the `HSAA` tables as soon as possible on new primary server. To do this:

1.  Open the Terminal on the new primary server.
    
2.  Switch to the `HSANALYTICS` namespace.
    
3.  Enter the following command:
    
    ```objectscript
     do ##class(HSAA.API.Data).TuneHSAASchema()
    ```
    

While this method is running, the system can be running and can have users as usual.

> **Caution:**
> 
> Do not use the task `Tune HSAA Schema on Mirror`. This task is visible in the Task Manager page but is intended for use in a future release. If you try to run this task, an error occurs.
