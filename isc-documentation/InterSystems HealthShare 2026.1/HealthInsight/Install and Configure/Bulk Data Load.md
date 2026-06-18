# [Performing a Bulk Load of Data to Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkload)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

This chapter describes how to perform a bulk load of data into HealthShare Health Insight.

For background information, see “[Overview of the Data Feed Mechanism](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed)” in the first chapter.

> **Important:**
> 
> For information on monitoring and troubleshooting the process of loading data, see the [Health Insight Administration Guide](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM).

## [Health Insight Bulk Load Overview](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkload_config_recommendations)

There are several times when it is necessary to load a large amount of data into Health Insight:

*   When you install and configure Health Insight, a large amount of data is typically already available and must be loaded into the system.
    
*   During the implementation process, if you change how you load data, you must [reset](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkload_resetting) the Health Insight database and cubes, as described at the end of this chapter, and then reload the data.
    
*   When a new Edge Gateway becomes available, that Edge Gateway might provide another large amount of data that must be loaded into the system.
    

In all these cases, InterSystems recommends performing a bulk load in three steps, as described in this chapter. In the first step, you temporarily modify some configuration settings, to disable some processing that is normally done incrementally. Then you load the data. Finally, you change the configuration settings back and perform (in bulk) the processing that was disabled in the first phase. This processing includes [building](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent) the Health Insight cubes so that they are up to date and can be queried.

The [next section](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkload_howto) contains the details.

> **Warning:**
> 
> It is critical to first test this entire process in a non-production environment to gauge resource consumption before performing these steps in a live system.

> **Note:**
> 
> This procedure assume that you are using cubes. If you are not, ignore any cube-related instructions.

## [Performing a Bulk Load to Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkload_howto)

This section describes how to perform a bulk load of data from one or more Edge Gateways.

### [Step 1: Before Loading Data](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkloadphase1)

Before performing a bulk load of data, do the following:

1.  Make the following temporary changes within the Health Insight instance:
    
    *   Disable cube synchronization by clicking the `Unselect All` button on the `Cube Sync Settings` page, so that no cube groups are included in the Health Insight synchronization process. Click `Save Settings` to save your settings.
        
        See “[Enabling Automatic Cube Synchronization](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent#HSAAIC_cubescurrent_sync_enable),” in the next chapter.
        
    *   Optionally, if you have enabled the processing of microbiology sensitivities, disable that processing. To do so, set any value for `Enable processing of microbiology sensitivities` on the [Additional Settings page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional). (In a later step, you perform this computation in bulk for all the patients, if needed.)
        
    *   Disable journaling for the [`HSAAFACT`](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_databases) database.
        
2.  If you are resending all data to Health Insight, purge the Health Insight patient errors and other Health Insight management data. See [Purging Management Data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_purgedata) in the Health Insight Administration Guide.
    
3.  Purge the production messages and event log in the analytics production, so that there is more disk space. To do so, navigate to `Interoperability` > `Configure` > `Purge Data Settings` in your analytics namespace. When purging, use the following configuration settings:
    
    *   `Include message bodies` — Select this option.
        
    *   `Purge only completed sessions` — Clear this option.
        
4.  Purge the production messages and event log in the Feeder Gateway, so that there is more disk space To do so, navigate to `Interoperability` > `Configure` > `Purge Data Settings` in your Feeder Gateway namespace. When purging, use the following configuration settings:
    
    *   `Include message bodies` — Select this option.
        
    *   `Purge only completed sessions` — Clear this option.
        
    
    (This step assumes that this Access Gateway is not used for any other purpose. This Access Gateway should be dedicated for use by Health Insight.)
    

### [Step 2: Load Data](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkloadphase2)

#### [Complete Transactional Edge Gateway](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkloadphase2_completetransactional)

For each Complete Transactional Edge Gateway that is responsible for providing data to Health Insight:

1.  If this Edge Gateway had previously sent data to Health Insight, complete the substeps below. Otherwise skip to the next step.
    
    1.  Disable the production setting `FeedAnalytics`.
        
    2.  Restart the production. Unlike other settings, the `FeedAnalytics` setting is checked and used only when the production restarts.
        
    3.  Wait briefly so that the change is registered at the Hub.
        
2.  Stop the production.
    
3.  Make sure that the production setting `FeedAnalytics` is enabled.
    
4.  Restart the production.
    

#### [Notify and Query Edge Gateway](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkloadphase2_notifyandquery)

For each Notify and Query Edge Gateway that is responsible for providing data to Health Insight:

1.  If this Edge Gateway had previously sent data to Health Insight, complete the substeps below. Otherwise skip to the next step.
    
    1.  Disable the production setting `FeedAnalytics`.
        
    2.  Restart the production. Unlike other settings, the `FeedAnalytics` setting is checked and used only when the production restarts.
        
    3.  Wait briefly so that the change is registered at the Hub.
        
    4.  In the Terminal, change to the namespace of this Edge Gateway and execute the following command to clear the global that tracks data to be sent to Health Insight:
        
        ```objectscript
         kill ^HS.ECRQueryQ
        ```
        
2.  Stop the production.
    
3.  Enable the production setting `FeedAnalytics`.
    
4.  Restart the production.
    
    The next steps define and run a system task that will parse documents in the repository.
    
5.  In the Management Portal for the Notify and Query instance, go to the Task Manager (click `System Operation` > `Task Manager` > `Task Schedule`).
    
6.  If the list shows a task of type `HS.Gateway.ECR.QueryTask`, then (temporarily) change the schedule of that task to be on-demand.
    
    Make a note of how the task had been scheduled so that you can later redefine the task to use its original schedule.
    
7.  Otherwise, click `New Task` and specify the following information:
    
    *   `Task Name`: Use a name such as `Consume Docs for ECR`
        
    *   `Description`: Enter a description
        
    *   `Namespace to run task in`: select the namespace of the Edge Gateway from the drop-down list.
        
    *   `Task type`: select `HS.Gateway.ECR.QueryTask` from the drop-down list.
        
    *   `Task priority`: select `Priority Normal` from the drop-down list.
        
    *   `Run task as user`: `HS_Services`
        
    *   Accept the defaults for the rest of the fields.
        
8.  Click `Next`
    
9.  On the scheduling page, initially set the task to be on-demand.
    
10.  Click `Finish`.
     
11.  On the `Task Schedule` page, click the `Run` button next to your new task to consume the documents in the repository.
     
     > **Note:**
     > 
     > This may take a long time depending on the number and complexity of documents in your repository.
     
12.  Modify the task definition again (if applicable) to use its original schedule.
     

### [Step 3: After Loading Data](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkloadphase3)

Periodically check to see when the processing is complete. For information, see the chapter “[Monitoring the Data Feed](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor)” in the Health Insight Administration Guide. Then, when the processing is complete, do the following:

1.  If you disabled the computation of microbiology sensitivities in [Before Loading Data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkloadphase1) step and you want to use the Microbiology cube, do the following on the Health Insight instance:
    
    ```objectscript
     do ##class(HSAA.API.Data).ProcessMicrobiologyDetails()
    ```
    
    This method empties the [HSAA.MicrobiologyDetail](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MicrobiologyDetail) table and then repopulates it from the existing rows in [HSAA.LabResultItem](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.LabResultItem). This method also resets the setting `Enable processing of microbiology sensitivities` on the [Additional Settings page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional). This processing can be time-consuming.
    
    If you do not want to use the Microbiology cube, skip this step.
    
2.  If there is substantially more data in the analytics instance than before, or if this data has a substantially different character (for example, many more encounters or diagnoses), recompile the class queries used by Health Insight. To do so, use the `RecompileCubeQueries()` method of [HSAA.Utils](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Utils):
    
    ```objectscript
     do ##class(HSAA.API.Data).RecompileCubeQueries()
    ```
    
    As explanation: Health Insight uses embedded SQL queries in many of its cube definitions. Embedded SQL is the fastest form of InterSystems SQL but it is necessary to recompile code that contains it when the character of the queried data changes greatly.
    
3.  Build the cubes. To do so, execute the following command in the `HSANALYTICS` namespace:
    
    ```objectscript
     set status=##class(HSAA.API.Cubes).RebuildAllCubes()
     write status
    ```
    
    If `status` equals 1, the command was successful. If not, enter the following command to learn more:
    
    ```objectscript
     do $system.OBJ.DisplayError()
    ```
    
    For more information on this method, see the [next chapter](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent).
    
4.  Re-enable journaling for the `HSAAFACT` database.
    
5.  Enable cube synchronization.
    
    See “[Enabling Automatic Cube Synchronization](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent#HSAAIC_cubescurrent_sync_enable),” in the next chapter.
    

## [Resetting the Health Insight Database and Cubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkload_resetting)

As you load data into Health Insight, it might be necessary to adjust how you handle the data that comes into HealthShare Unified Care Record. When you do so, you typically want to reset the Health Insight database and cubes so that you can reload the data.

To reset the Health Insight database and cubes, use the Terminal, go to the `HSANALYTICS` namespace, and enter the following command:

```objectscript
 set status = ##class(HSAA.API.Data).ResetAllDataAndCubes()
```

> **Caution:**
> 
> This method first deletes all data currently contained in the Health Insight clinical tables and cubes, as well as data in any [custom container classes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_customcontainer) that you have registered for use by Health Insight. This method should not be used in production without careful consideration of the consequences.
> 
> This method also deletes all data from the reporting tables and reporting cubes.

If `status` equals 1, the command was successful. If not, enter the following command to learn more:

```objectscript
 do $system.OBJ.DisplayError()
```

> **Note:**
> 
> If you need a clean start after resetting Health Insight data, also clear the feeder patient error global in the Feeder namespace. Entries in `^HS.Feeder.PatientErrors` persist until they are explicitly cleared and are not removed by resetting Health Insight data, purging interoperability data, or resetting the production.
> 
> Run the following command in the Feeder namespace: 
> 
> ```
> kill ^HS.Feeder.PatientErrors
> ```
