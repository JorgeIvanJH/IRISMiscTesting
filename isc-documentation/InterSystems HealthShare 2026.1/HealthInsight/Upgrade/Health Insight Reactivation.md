# [Health Insight Post-Upgrade Reactivation Procedure](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

> **Note:**
> 
> Before beginning the post-upgrade reactivation procedure, review the following notices if you are upgrading from a version prior to 2025.2, and perform any applicable steps.
> 
> ## [ChangedObjects Downstream Process Updates](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_changedobjects)
> 
> If you have any downstream processes that relied on the old behavior for [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects), update them now to ensure they are compatible with the updated behavior prior to beginning with the post-upgrade reactivation steps. More specifically, if your systems:
> 
> *   Relied on batch-driven purge behavior
>     
> *   Assumed the ChangedObjects table would be empty post-batch
>     
> *   Relied on the old logic where rows were overwritten
>     
> 
> ...you must update those systems to reflect the new model where rows are appended and purging occurs via a scheduled task.
> 
> You may also want to adjust the frequency of the Purge ChangedObjects task to suit your retention requirements. Retention duration is determined by how often this task runs. Ensure that purging runs less frequently than the slowest consumer of [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) data.
> 
> ## [Readmission Custom Method Updates](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_readmission)
> 
> Starting in version 2025.2, the implementation for the default method to calculate readmissions has changed. Previously, both the default and any custom methods directly updated [HSAA.Encounter](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Encounter) relationships using a SQL query. Now, the default method computes readmissions for all encounters of a selected patient. Any custom methods must also follow this pattern. If you previously implemented a custom readmission method and want to continue using it after the upgrade, you must update it to match the new structure. See the Additional Settings documentation for guidance on modifying your custom method.

When you have completed running the installer for the software upgrade, perform the following steps that are outlined below and detailed in the sections that follow:

1.  [Clear the browser cache](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_cache).
    
2.  [Confirm that system-wide parallel query processing is enabled](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_parallel).
    
3.  [Reactivate Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_reactivate).
    
4.  [Review the Health Insight activation logs](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_logs).
    
5.  [Check referential integrity](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_integrity).
    
6.  [Rebuild indexes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_index).
    
7.  [Rebuild cubes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_cubes).
    
8.  [Inspect custom code](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_code).
    
9.  [Reapply settings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_reapply).
    
10.  [Turn off AutoTune](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_tune).
     
11.  [Reset the expired queries task](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_expired).
     
12.  [Reapply any custom listings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_listing).
     
13.  [Restart Your Analytics Production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_restart).
     

## [Step 1: Clear Browser Cache](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_cache)

Clear your browser cache immediately after the upgrade completes.

## [Step 2: Confirm that System-Wide Parallel Query Processing is Enabled](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_parallel)

A performance feature that was added in the transition from Caché to IRIS may be disabled if you upgraded from HealthShare 2019.1 at some time in the past. System-wide parallel query processing ([auto parallelization](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSOC_parallel)) can significantly speed up query processing on systems with multiple processors.

Navigate to `Home` > `System Administration` > `Configuration` > `SQL and Object Settings` > `SQL` on your Health insight instance confirm that the `Execute queries in a single process` checkbox is deselected. If you performed this step during a previous upgrade, there is no need to repeat it.

> **Note:**
> 
> In a mirrored environment, confirm that this is enabled on both mirror members.

## [Step 3: Reactivate Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_reactivate)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary mirror member:
> 
> *   You will perform this step initially on instance B when it is the primary.
>     
> *   In a later mirrored upgrade step, you will reactivate again on instance A, after failover, when A is the primary.
>     

Using the Terminal, reactivate the Analytics namespace.

To reactivate the Analytics namespace:

In the Terminal in the Health Insight instance, change to the `HSLIB` namespace and enter the following command:

```objectscript
 set status=##class(HS.Util.Installer.HSAALIB).Install("<varname>namespace</varname>")
 write status
```

Where `namespace` is the Analytics namespace, usually `HSANALYTICS`.

If `status` equals 1, the command was successful. If not, enter the following command to learn more:

```objectscript
 do $system.OBJ.DisplayError()
```

Note the following:

*   Namespace activation will not start if the analytics namespace has any previous [HS.Message.AnalyticsUpdateRequest](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Message.AnalyticsUpdateRequest) messages. You will receive an error if previous [HS.Message.AnalyticsUpdateRequest](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Message.AnalyticsUpdateRequest) messages exist. To clear these messages, purge production messages as described in the [Pre-Upgrade Steps](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_purge). Reactivation involves recompilation, which may take some time to complete.
    
    > **Important:**
    > 
    > Do not use the Installer Wizard to reactivate this namespace; the Wizard web page can time out, so that will be unable to see the status of the reactivation process.
    

## [Step 4: Review the Health Insight Activation Logs](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_logs)

Review the activation logs.

HealthShare creates namespace-specific log files for activations in the `<install-dir>\mgr` directory. When your activation completes, check the highest incremented log file for the Analytics namespace to confirm that everything worked correctly or to detect any errors. This file will be named `HS.Util.Installer.<namespace>-<#>.log`. When inspecting the log files, pay particular attention to entries with `[WARNING]` or `[ERROR:`

*   `[WARNING]` indicates that an action should be taken.
    
*   `[ERROR]` indicates that an error occurred during activation.
    

See “[Post-Upgrade Procedures for Unified Care Record](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEUPGRADE_pre_reactivate#HEUPGRADE_reactivate_reactivate)” for more information.

> **Note:**
> 
> In a mirrored upgrade:
> 
> *   If you have just performed the activation of the Analytics namespace for the first time (on instance B), go on to the [next step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_integrity).
>     
> *   If you have just performed the second activation of the Analytics namespace (on instance A), return to the [referring step in the mirrored upgrade procedure](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_reactivateHI).
>     

## [Step 5: Check Referential Integrity](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_integrity)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary mirror member.

Use the `ListReferentialIntegrityErrors()` method of the [HSAA.Util.Installer.Upgrade.PostActivation20181](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Util.Installer.Upgrade.PostActivation20181) class to check for any referential integrity errors. If you find errors, you should correct them. One option for correcting these errors is to remove the corresponding row(s). Once you have done so, you can clear the error list by calling the `ClearReferentialIntegrityErrors()` method of the [HSAA.Util.Installer.Upgrade.PostActivation20181](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Util.Installer.Upgrade.PostActivation20181) class. If the activation process is rerun, any old referential integrity errors will be cleared from the error list.

## [Step 6: Rebuild Indexes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_index)

> **Important:**
> 
> In a mirrored upgrade, skip this step.
> 
> You will perform it at a later stage of the mirrored upgrade procedure, [when instructed](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_rundefer).
> 
> Instead, go on to the [next step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_cubes).

Run the RebuildIndices utility. This utility backfills indices on certain tables and builds indices that were added in previous versions of Health Insight but were not built. More information about the original issue is available in the [Health Insight 2022.2 release notes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20222).

> **Note:**
> 
> As specified in the [2023.1 release notes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20231#HSAARN_20231_known_rebuildindices), the RebuildIndices utility can cause queries and data ingestion to slow down significantly while it is running. Execution times for the utility can vary and range from several minutes to a few hours. In certain cases, execution time may be even longer. You can use the `^IRIS.HSAA.Internal("NumberWorkersOverride")` global to adjust the number of logical CPUs used to run the API. For more information, see [Specifying CPU Count for the RebuildIndices Utility](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_rebuildindices).

To rebuild the indexes:

1.  Switch to the analytics namespace (usually HSANALYTICS) in the Terminal on your Health Insight instance and run the following command:
    
    ```objectscript
     do ##class(HSAA.Util.Installer.Upgrade.PostActivationCommon).RebuildIndices()
    ```
    
2.  The utility may take several hours to complete, especially for environments with a large amount of Health Insight data. The utility runs as a background job.
    
    Use the `RebuildIndicesStatus()` method to check the status of the method’s execution. To do so, run the following command:
    
    ```objectscript
     set status = ##class(HSAA.Util.Installer.Upgrade.PostActivationCommon).RebuildIndicesStatus()
     write status
    ```
    
3.  Check the `PostActivation<version>_RebuildIndices.log` file in the `<install-dir>\mgr` directory for more information about the rebuild process, where `<version>` is the version that you are upgrading to.
    
4.  If the `RebuildIndicesStatus()` method reports any rebuild errors, use the `RebuildIndicesReset()` method to reset the error status of any tables where the index rebuild process encountered errors, so that you can run the utility again after fixing the errors. Tables with completed or running index rebuilds are unaffected.
    
    ```objectscript
     do ##class(HSAA.Util.Installer.Upgrade.PostActivationCommon).RebuildIndicesReset()
    ```
    
5.  If you experience an interruption during the execution of the `RebuildIndices()` method, use the `Hard Reset` mode of the `RebuildIndicesReset()` method to reset the status of the index rebuild for any tables that are stuck in a running state or to reset the status of any tables with errors. Examples of interruptions to execution include production shutdowns and Terminal crashes. Use the following call:
    
    ```objectscript
     do ##class(HSAA.Util.Installer.Upgrade.PostActivationCommon).RebuildIndicesReset(1)
    ```
    
    Run the `RebuildIndices()` method again after using the `RebuildIndicesReset()` method in either mode, so that the step can finish.
    

## [Step 7: (Optional) Rebuild Cubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_cubes)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary mirror member.
> 
> You will perform this step at two different points in the mirrored upgrade procedure, first on instance B, when you run the entire post-upgrade procedure, and then later [on instance A after you rebuild the index.](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_rundefer)

If you are using cubes, recompile and rebuild all of your cubes, including any custom cubes.

> **Note:**
> 
> Rebuilding cubes can take a long time, especially in environments with large datasets.

For details on how to do so, see the [API for Monitoring and Managing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_api_methods_cubes).

## [Step 8: Inspect Custom Code](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_code)

Check your custom code for any old methods or old versions of APIs. Update your code to use the new versions. For more details, see [API for Monitoring and Managing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api).

> **Note:**
> 
> In a mirrored upgrade, if all of your custom code is in `HSCUSTOM`, then perform this step only on the primary mirror member. For any code that is not in `HSCUSTOM`, you must make the code databases on the backup match those on the primary.

## [Step 9: Reapply Settings](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_reapply)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary mirror member.

In the [Pre-Upgrade Tasks](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_settings), you noted several production and other settings. In this step you will reapply these settings.

Perform the following procedures from the Management Portal on your Health Insight instance:

### [Production Logging Settings](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_reapply_logging)

1.  Navigate to `Home` > `HealthShare` > `analyticsNamespace`.
    
2.  Click the `Productions` link in the banner.
    
3.  Click `Configure` > `Production`. (If needed, select your analytics production and click `Open`.)
    
4.  In the `Production Settings` pane, under `Additional Settings`, enter the values that you [noted earlier](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_settings) for the following production settings:
    
    *   `LogTarget`
        
    *   `TargetPath`
        
    *   `LogLevel`
        
5.  Click `Apply`.
    

## [Step 10: Turn off AutoTune](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_tune)

> **Note:**
> 
> In a mirrored upgrade, perform this step on both mirror members.

Turn off the AutoTune feature by running the following command in the Terminal:

```
set ^%SYS("sql","sys","autotune")=0
```

## [Step 11: Reset Expired Queries Task](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_expired)

> **Note:**
> 
> In a mirrored upgrade, perform this step on both mirror members.

Set the frequency of execution for the `Run expired queries` task from “on demand” back to its original setting that you noted in the [Pre-Upgrade Steps](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_expired):

1.  On the Unified Care Record Registry instance, log in to the Management Portal as user with administrative privileges.
    
2.  Navigate to the `Task Schedule` page: `Home` > `System Operation` > `Task Manager` > `Task Schedule`
    
3.  Select the `Run Expired Queries` task from the list of scheduled tasks.
    
4.  Click `Edit`.
    
5.  Click `Next`.
    
6.  Change the value of the setting `How often do you want the Task Manager to execute this task?`
    
    In the [Pre-Upgrade Steps](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_expired) you set this value to “on demand”. Now set it back to its original value.
    
7.  Click `Finish`.
    
8.  In a mirrored upgrade, repeat this procedure on the backup mirror member.
    

## [Step 12: Reapply Custom Listings](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_listing)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary mirror member.

On the Health Insight instance, if you created any custom listings or made any other changes on the Health Insight Custom Listing page, return to that page and select `Reapply Custom Listings for All Cubes`. See [Defining Custom Listings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_listings) for more information.

This step is needed whenever you recompile classes in the `HSAA` package, and reactivating the Health Insight production in [Step 3](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_reactivate) recompiled the classes in the `HSAA` package.

## [Step 13: Restart Your Analytics Production](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_restart)

Restart your Analytics production:

1.  You can perform the restart either from the Management Portal or Terminal:
    
    ### [Restart from the Management Portal](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_C20763)
    
    1.  On your Health Insight instance, log in to the Management Portal as a user with administrative credentials.
        
    2.  Navigate to `Home` > `HealthShare` > `analyticsNamespace`.
        
    3.  Click the `Productions` link in the banner.
        
    4.  Click `Configure` > `Production`. (If needed, select your Analytics production and click `Open`.)
        
    5.  Click `Start`.
        
    
    ### [Restart from the Terminal](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_C20772)
    
    1.  Switch to the `HSLIB` namespace in the Terminal on your Health Insight instance.
        
    2.  Run the following command:
        
        ```
         do ##class(HS.Director).Start(namespace)
        ```
        
        Where `namespace` is the Analytics namespace, usually `HSANALYTICS`.
        
    
2.  Check the Event Log; you may see either or both of the following errors:
    
    `ERROR #5002: error: <SUBSCRIPT>zGetLatestUnresolved+8 ^%SYNC.SyncSet.1 *aa("")`
    
    `ERROR #5824: Object referenced by 'Report' does not exist`
    
    These errors are associated with the initial synchronization with the Registry. The synchronization service should succeed on its next try. To confirm that it did, go to the production Message Viewer at the Registry and confirm that after the errors, the sync service completed without error. If it did not, you may stop and restart the production again.
    
    [Image: generated description: error]
