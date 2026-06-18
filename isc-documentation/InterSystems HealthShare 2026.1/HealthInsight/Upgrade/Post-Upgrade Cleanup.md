# [Health Insight Post-Upgrade Cleanup Steps](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_finalsteps#HSAAUP_finalsteps)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

Perform the final cleanup steps to complete your Health Insight upgrade:

1.  [Unfreeze frozen query plans](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_finalsteps#HSAAUP_frozen).
    
2.  [Tune the HSAA schema](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_finalsteps#HSAAUP_tune).
    
3.  [Choose how to run analytics queries](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_finalsteps#HSAAUP_queries).
    
4.  [Perform extra steps if upgrading from a very old version](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_finalsteps#HSAAUP_finalsteps_old).
    

## [Step 1: Unfreeze Frozen Query Plans](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_finalsteps#HSAAUP_frozen)

To unfreeze frozen query plans:

On your Health Insight instance, run the following commands in the Analytics namespace in the Terminal:

```objectscript
 set status = ##class(%SYSTEM.SQL.Statement).UnfreezeAll(1)
 w:status'=1 $system.OBJ.DisplayError(status)
```

For more information on frozen query plans, see [Troubleshooting Data Feed Problems](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob).

## [Step 2: Tune the HSAA Schema](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_finalsteps#HSAAUP_tune)

Tune the HSAA schema to avoid slow query performance:

1.  On your Health Insight instance, run the following commands in the Analytics namespace in the Terminal:
    
    ```objectscript
     set status=##class(HSAA.Util.Installer.Upgrade.PostActivationCommon).TuneHSAASchema()
     write $system.OBJ.DisplayError(status)
    ```
    
    The `TuneHSAASchema()` method will tune the HSAA schema as a background job.
    
2.  Use the `TuneHSAASchemaStatus()` method to check the status of the `TuneHSAASchema()` method's execution:
    
    ```objectscript
     do ##class(HSAA.Util.Installer.Upgrade.PostActivationCommon).TuneHSAASchemaStatus()
    ```
    
3.  Inspect the log file for this step in the `mgr` directory of your Health Insight instance. The log file is named `TuneHSAASchema_<YYYYMMDD>_<HHMMSS>.log`.
    
    > **Note:**
    > 
    > If you encounter error messages similar to the following example message:
    > 
    > ```
    > {}ERROR <HSAAErr> TuneHSAASchema: Error during tuning HSAA schema: There are 0 errors in routine %sqlcq.HSANALYTICS.19
    > ERROR: [aborting compile of %sqlcq.HSANALYTICS.19: <MAXSTRING>FILE+16^%qarmac] There are 0 errors in routine %sqlcq.HSANALYTICS.18
    > ```
    > 
    > then certain tables were not successfully tuned, which may result in slow queries. This is a known issue.
    

## [Choose How to Run Analytics Queries](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_finalsteps#HSAAUP_queries)

Starting in version 2024.2 of Health Insight, users can decide whether to run [analytics queries](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs) as part of the analytics batch. If you use analytics queries, decide whether to run them as part of the analytics batch or [via a separate scheduled task](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch).

## [Step 3: Extra Steps for Very Old Versions](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_finalsteps#HSAAUP_finalsteps_old)

> **Important:**
> 
> Proceed with these sub-steps only if you meet the following conditions:
> 
> *   You started using Health Insight on a version older than 2019.1.
>     
> *   You did not already run these step during a previous upgrade.
>     
> 
> If you do not meet those conditions, then your upgrade is now complete.

### [Step 1A: Adding Observation Groups to Existing Data](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_finalsteps#HSAAUP_observation)

If you wish to use ObservationGroups, you should follow the instructions listed in [Adding Observation Groups to Existing Data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEFLW_ch_observation_group#HEFLW_observation_group_historic_data). Both the Registry and the Edge Gateway where the group loader utility is run must be running in order for you to perform these steps. Once you have completed these steps, ObservationGroup streamlets will be sent to Health Insight as part of regular ingestion. For more information, see [Grouping Observations](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEFLW_ch_observation_group) in Implementing HealthShare Unified Care Record.

### [Step 1B: Run the PopulateClinicians() Method](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_finalsteps#HSAAUP_populateclinicians)

You can optionally use the `PopulateClinicians()` utility to populate the Encounter table with AttendingClinicians and ConsultingClinicians data. Use the following call:

```objectscript
 set sc = ##class(HSAA.Util.Installer.Upgrade.V20191).PopulateClinicians()
```

This utility may take some time to execute. Note that you should only use the `PopulateClinicians()` utility immediately after upgrading, before resuming data ingestion.
