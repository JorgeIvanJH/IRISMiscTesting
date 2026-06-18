# [API for Monitoring and Managing Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_api)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

This page describes methods that you can use to monitor and manage HealthShare Health Insight.

These methods are intended to be called programmatically from the Health Insight server or from a Terminal session in the Health Insight namespace. In this case, you directly run the class method.

The following sections provide a brief description of available API methods in Health Insight. For more information, see the class reference for `HSAA.API`.

## [HSAA.API.Cubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_api_methods_cubes)

A cube group is Health Insight-enabled when it is included in the Health Insight cube sync process. You can see which cube groups are Health Insight-enabled on the `Cube Sync Settings` page. Note that the reporting cubes are relevant only to analytics batches. If you programmatically call any of the API methods for building or syncing cubes, the dashboards and underlying data associated with cube sync performance are not updated.

### [RebuildAllClinicalCubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16383)

Rebuilds all the [deprecated](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20261#HSAARN_20261_cube_deprecate), out-of-the-box `HSAA` cubes and any custom cubes that are related to them.

Calling this method is equivalent to calling `RebuildCubeGroup("Health Insight Clinical Group")`.

### [RebuildAllCubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16387)

Rebuilds the [deprecated](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20261#HSAARN_20261_cube_deprecate), out-of-the-box `HSAA` cubes, the reporting cubes, and any custom cubes that are related to the `HSAA` cubes.

Calling this method is equivalent to calling `RebuildAllCubeGroups()`. This method will build cubes from all Health Insight-enabled cube groups.

### [RebuildAllReportCubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16391)

Rebuilds all reporting cubes.

Calling this method is equivalent to calling `RebuildCubeGroup("Health Insight Reporting Group")`.

### [RebuildCubeGroup](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16394)

Rebuilds all the cubes in the specified Health Insight-enabled cube group.

### [RebuildAllCubeGroups](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16398)

Rebuilds all registered cube groups.

This method will build all Health Insight-enabled cube groups.

### [BuildAndFixClinicalCubeGroups](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16402)

Rebuilds all the [deprecated](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20261#HSAARN_20261_cube_deprecate), out-of-the-box `HSAA` cubes and any custom cubes related to the them while ignoring all cube build errors. Attempts to fix any build errors.

This method should be used only in cases where a cube build error is forcing the group build to be run repeatedly. If errors persist, InterSystems support should be contacted.

### [SynchronizeAllClinicalCubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16406)

Synchronizes all the [deprecated](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20261#HSAARN_20261_cube_deprecate), out-of-the-box `HSAA` cubes and any custom cubes that are related to them.

Calling this method is equivalent to calling `SynchronizeCubeGroup("Health Insight Clinical Group")`.

### [SynchronizeAllCubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16410)

Synchronizes all the [deprecated](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20261#HSAARN_20261_cube_deprecate), out-of-the-box `HSAA` cubes, all reporting cubes, and any custom cubes that are related to the `HSAA` cubes.

Calling this method is equivalent to calling `SynchronizeAllCubeGroups()`. This method synchronizes cubes from all Health Insight-enabled cube groups.

### [SynchronizeAllReportCubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16414)

Synchronizes all the reporting cubes.

Calling this method is equivalent to calling `SynchronizeCubeGroup("Health Insight Reporting Group")`.

### [SynchronizeCubeGroup](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16418)

Synchronizes the named cube group.

This method will synchronize the specified Health Insight-enabled cube groups.

### [SynchronizeAllCubeGroups](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16422)

Synchronizes all registered cube groups.

This method will synchronize all Health Insight-enabled cube groups.

### [GetBuildOrder](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16425)

Lists a safe build order for building cubes.

### [ActivateNewCubeRegistry](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16428)

Activates a new cube registry.

### [CopyDefaultCubeRegistry](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16431)

Copies the default Cube Registry to a new class.

### [CopyAndActivateDefaultCubeRegistry](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16434)

Copies the Default Registry and activates it.

### [ResetCubeRegistry](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16437)

Resets the active Cube Manager registry to the default setting.

### [EnableAllCubeGroups](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16440)

Health Insight-enables all cube groups. If any groups are enabled, cubes will sync as part of analytics processing.

### [DisableAllCubeGroups](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16443)

Health Insight-disables all cube groups. This method disables all cube syncing during analytics processing.

### [EnableCubeGroup](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16446)

Health Insight-enable a cube group.

### [DisableCubeGroup](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16449)

Health Insight-disable a cube group.

### [EnableReportCubeGroup](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16452)

Health Insight-enable the report cube group.

### [DisableReportCubeGroup](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16455)

Health Insight-disable the report cube group.

### [EnableClinicalCubeGroup](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16458)

Health Insight-enable the [deprecated](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20261#HSAARN_20261_cube_deprecate) clinical cube group.

### [DisableClinicalCubeGroup](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16461)

Health Insight-disable the [deprecated](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20261#HSAARN_20261_cube_deprecate) clinical cube group.

### [IsCubeGroupEnabled](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16464)

Return a boolean indicating whether the specified cube group is enabled.

### [IsReportCubeGroupEnabled](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16467)

Return a boolean indicating whether the report cube group is enabled.

### [IsClinicalCubeGroupEnabled](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16470)

Return a boolean indicating whether the [deprecated](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20261#HSAARN_20261_cube_deprecate) clinical cube group is enabled.

### [GetCompiledCubeName](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16483)

Returns the cube name from the cube class name.

Two arguments:

*   A string holding the cube class name
    
*   An output argument with the `%Status` of the method
    

Returns:

*   A string with the cube’s logical name
    

### [ScanPivotsForLabResultCube](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16496)

Outputs a list of all pivot tables that reference either `HSAALABRESULT` or `HSAALABRESULTITEM`

One argument:

*   The verbose flag, with a default value of 0
    

Returns:

*   `%Status`
    

Note that if you encounter an error such as the following, you need to update the pivot to use the `LabResultItems` cube.

```
Upgrade20181/Patients Diagnosis Test Item Description.pivot
hit error on pivot 'Upgrade20181/Patients Diagnosis Test Item Description.pivot'
ERROR #5001: %GetDimensionInfo: Invalid Member spec: HSAALABRESULT:[Test].[H1].[TestItemDescription].Members
```

## [HSAA.API.Data](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_api_methods_data)

> **Note:**
> 
> If you need a clean start after resetting Health Insight data by using the data reset methods below, also clear the feeder patient error global in the Feeder namespace. Entries in `^HS.Feeder.PatientErrors` persist until they are explicitly cleared and are not removed by resetting Health Insight data.
> 
> To do so, run the following command in the Feeder namespace: 
> 
> ```
> kill ^HS.Feeder.PatientErrors
> ```

### [ResetClinicalData](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16505)

Deletes all data from `HSAA` source tables.

This method should be used for development purposes only.

### [ResetClinicalDataAndCubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16509)

Deletes all data from `HSAA` source tables, `HSAA` cubes, and any custom container classes that you have registered for use by Health Insight.

This method should be used for development purposes only.

### [ResetAllData](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16513)

Deletes all data from `HSAA` source tables and reporting tables.

This method should be used for development purposes only.

### [ResetAllDataAndCubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16517)

Deletes all data from `HSAA` source tables, reporting tables, `HSAA` cubes, and reporting cubes.

This method should be used for development purposes only.

### [ResetReportData](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16525)

Deletes all data from reporting tables:

1.  Purges records from the [HSAA.Report.BatchSummary](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Report.BatchSummary) table
    
2.  Related [HSAA.Report.CubeSummary](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Report.CubeSummary) and `HSAA.Report.BatchProgress` records are also purged.
    

### [ResetReportDataAndCubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16528)

Deletes all data from reporting tables and reporting cubes.

### [PurgeLogTable](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16531)

Purges all records from the [HSAA.Report.Log](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Report.Log) table.

### [ComputeAllReadmissions](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16545)

1.  Resets the `Do not compute readmissions after processing each patient` configuration setting, unless the caller indicates that this should not be done.
    
2.  Performs the readmission computation for all patients.
    
3.  This process can be time-consuming.
    

*   The `Do not compute readmissions after processing each patient` setting can be found on the `Additional Settings` page (`HealthShare` > `Customization` > `Additional Settings`).
    
*   Provide an argument to this method to indicate whether to reset the `Do not compute readmissions after processing each patient`flag. The default is to reset the flag.
    

### [ProcessMicrobiologyDetails](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16555)

1.  Empties the [HSAA.MicrobiologyDetail](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MicrobiologyDetail) table
    
2.  Repopulates it from the existing rows in [HSAA.LabResultItem](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.LabResultItem)
    
3.  Resets the `Enable processing of microbiology sensitivities` setting on the `Additional Settings` page
    

This process may be time-consuming!

### [TuneHSAASchema](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16570)

1.  Runs Tune Table on `HSAA` source tables
    
2.  Purges cached queries
    
3.  Runs the `RecompileCubeQueries()` method of [HSAA.Utils](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Utils)
    

*   This method updates the last schema tuning time.
    
*   This process can be time-consuming, but this method can be run while other activities are taking place on the system.
    

You can find the log file for `TuneHSAASchema()` in the `mgr` directory of your Health Insight instance. The log file is named `TuneHSAASchema_<YYYYMMDD>_<HHMMSS>.log`.

### [GetTuneTableInfo](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16578)

Retrieves data about the last tuning of the HSAA schema:

1.  The last time the schema was tuned
    
2.  The patient count prior to initiating the tune schema command
    

### [RecompileCubeQueries](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16582)

Recompiles all embedded SQL queries used by cubes.

Note that this method is automatically called as part of the `TuneHSAASchema` method, and should not need to be called when tuning the schema.

## [HSAA.API.Audit](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_api_methods_audit)

### [EnableAuditing](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16586)

Enables InterSystems IRIS Business Intelligence audit logging for the Health Insight namespace, usually `HSANALYTICS`.

### [LogToATNA](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16589)

Logs an audit record in the ATNA Repository.

### [DisableAuditing](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16592)

Disables Business Intelligence audit logging for the Health Insight namespace, usually `HSANALYTICS`.

## [HSAA.API.Transmit](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_api_methods_transmit)

### [SendDataToAnalytics](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16598)

Calls the web service method `SendDataToAnalytics` in the Feeder Gateway to start sending data from HealthShare Unified Care Record to Health Insight.

This web service has the same effect as running the following command in the Feeder Gateway namespace:

```objectscript
 do ##class(HS.Gateway.Analytics.TransmitService).Start()
```

### [PauseIngestionStartBatch](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16608)

Starts the interrupt business service ([HSAA.TransferSDA3.Service.Interrupt](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.Interrupt)), which pauses data ingestion into tables and initiates:

*   The running of smart queries
    
*   The synchronization of cubes
    
*   The update of reporting cubes
    

### [RequeueForAnalytics](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16630)

This method requeues patient information for resending from Unified Care Record to Health Insight by populating the `^HS.AADBQ` global with the appropriate information.

Depending on the arguments passed in, you can resend:

*   All the data for a single patient
    
*   All the data for an edge gateway
    
*   All the data from the Registry
    
*   All the data for everyone
    

Three arguments:

*   Resend type
    
*   Resend ID
    
*   Resend [priority](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_phase2_priority)
    

See the following table for a description of the first two arguments:

### [RequeueForAnalytics Arguments](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_api_methods_requeue)

<table><tr><th><code>pResendType</code></th><th><code>pResendId</code></th><th>These arguments repopulate the data feed queue to include ...</th></tr><tr><td><code>"MPIID"</code></td><td>MPI ID of a patient</td><td>All data for the given patient</td></tr><tr><td><code>"ANALYTICSID"</code></td><td>Analytics ID of a patient</td><td>All data for the given patient</td></tr><tr><td><code>"GATEWAY"</code></td><td>Name of an Edge Gateway</td><td>All data for any patients who have any data at the given Edge Gateway</td></tr><tr><td><code>"REGISTRY"</code></td><td>Name of the Registry</td><td>All cohort membership data from the Registry</td></tr><tr><td><code>"EVERYTHING"</code></td><td><code>"EVERYTHING"</code></td><td>All data for all patients</td></tr></table>

### [RequeueExistingMedOrdersForAnalytics](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16633)

If you need to backfill the data for medications and medication orders after performing an upgrade, you can use this utility method to cause the resend of only the specific streamlets (of the appropriate types) that are needed.

### [RequeueExistingMemberEnrollmentsForAnalytics](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16636)

If you need to backfill the data for member enrollments after performing an upgrade, you can use this utility method to cause the resend of only the specific streamlets (of the appropriate types) that are needed.

### [RequeueExistingSocialHistoriesForAnalytics](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16639)

If you need to backfill the data for social histories after performing an upgrade, you can use this utility method to cause the resend of only the specific streamlets (of the appropriate types) that are needed.

### [RequeueAllPatientsInErrorListAndClear](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16654)

Resends all patients in the `Patient Errors List` from the Registry to Health Insight. All patients resent with this method will have the same priority. By default, the priority for resend is set to the lowest value, 4.

The patients are sent to the Registry in batches, each of which contains a maximum of 10,000 analytics IDs.

Patients that had no error when queued for resend are then cleared from the `Patient Errors List`.

Patients that had an error are returned in an optional argument.

Two arguments:

*   An integer between 1–4 representing the priority for resend
    
*   An optional output argument to hold the list of patients that had errors when trying to requeue
    

If a patient with an error is deleted via streamlet ingestion, it may take some time for the patient to be completely removed from Health Insight. During this period, the patient with an error will still appear in the Patient Errors List. In certain rare cases, such as running this method before the patient is fully deleted, you may see error messages like the following in the Terminal:

```
2024-05-24 14:29:57.977268 INFO Requeuing Error Info:
2024-05-24 14:29:57.977295 INFO ERROR #5001: 1 patients had error when queuing for resend. The analytics Ids: AEGGAB
```

If you run into errors like these, you should wait for a while, then run the method again. Once deletion from Health Insight completes, you will no longer encounter this error.

### [RequeuePatientsInErrorListAndClear](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16667)

Resends a subset of patients in the `Patient Errors List` from the Registry to Health Insight, potentially with distinct priorities.

Patients are sent to the Registry by batches, each of which contains a maximum of 10,000 analytics IDs.

Patients that had no errors when queued for resend are then cleared from the `Patient Errors List`.

Three arguments:

*   A list of analytics IDs.
    
*   A list of priorities for resend or a single integer to use as the priority for all items in the list.
    
*   An optional output argument to hold the list of patients that had errors when trying to requeue
    

### [ClearAllPatientsInErrorList](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16674)

Clears all patients listed in the `Patient Errors List` in Health Insight. The total number of patients cleared is reported on the Terminal and returned in an output argument.

One argument:

*   An integer holding the number of patients cleared
    

### [ClearPatientsInErrorList](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16683)

Clears patients from the `Patient Errors List` based on a list of analytics IDs. Only patients that are present in the `Patient Errors List` are cleared. The total number of patients cleared is reported on the Terminal.

Two arguments:

*   A list of analytics IDs. For example: `$lb("MLPKHH","QNRMJJ")`
    
*   An integer holding the number of patients cleared
    

### [SetForceKillGlb](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16686)

Configures the system to concurrently halt all jobs of the [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer) business host that are processing messages into Health Insight. You can use this method if the batch process is taking too long to halt the ingestion process.

### [GetForceKillGlb](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16689)

Gets the current settings of the `SetForceKillGlb()` method.

## [HSAA.API.Utils](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_api_methods_utils)

### [ProcessPRFromFile](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16693)

Processes persistent requests that are stored as files.

### [ProcessPRFromTable](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16696)

Processes persistent requests stored in SQL tables.

### [GetProductionStatus](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16700)

Gets the status of the Health Insight production and returns the status of the Health Insight production as a string.

Possible values: Running, Stopped, Suspended, Trouble, Network Stopped, Unknown.

### [GetProductionBatchStatus](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16704)

Gets the status of the analytics batch and returns the current state of the Health Insight analytics batch as a string.

Possible values: Query Waiting, Initializing, Transferring, Finalizing, Synchronizing, Post synchronizing, Post batch processing, Report cube synchronizing, Idling.

### [GetPatientTransferErrors](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16707)

Gets a list of all current patients with a transfer error and optionally prints to the current device. The list will contain a list of analytics IDs.

## [Supported Web Services](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_api_webservices)

The following web services are currently supported in Health Insight. Note that to call these web services, you must use the “services” Web application. For example, the location property of the web services client should look like this: `http://localhost:57772/csp/healthshare/hsanalytics/services/HSAA.TransferSDA3.WebServices.cls`.

### [GetProductionBatchState](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16713)

Gets analytics production state as a number. Provided for backwards compatibility.

<table><tr><td>HealthShare component</td><td>Health Insight Analytics Production</td></tr><tr><td>Web Service Client</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.TransferSDA3.WebServicesClient">HSAA.TransferSDA3.WebServicesClient</a></td></tr><tr><td>Arguments</td><td>None</td></tr><tr><td>Returns</td><td>Batch state integer</td></tr></table>

### [GetProductionBatchStateString](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16717)

Gets analytics production state as a string. Provided for backwards compatibility.

<table><tr><td>HealthShare component</td><td>Health Insight Analytics Production</td></tr><tr><td>Web Service Client</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.TransferSDA3.WebServicesClient">HSAA.TransferSDA3.WebServicesClient</a></td></tr><tr><td>Arguments</td><td>None</td></tr><tr><td>Returns</td><td>Batch state string</td></tr></table>

### [GetProductionStatus](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16721)

Gets analytics production status as a number. Provided for backwards compatibility.:

<table><tr><td>HealthShare component</td><td>Health Insight Analytics Production</td></tr><tr><td>Web Service Client</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.TransferSDA3.WebServicesClient">HSAA.TransferSDA3.WebServicesClient</a></td></tr><tr><td>Arguments</td><td>None</td></tr><tr><td>Returns</td><td>Production status integer</td></tr></table>

### [GetProductionStatusString](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16725)

Gets analytics production status as a string. Provided for backwards compatibility.

<table><tr><td>HealthShare component</td><td>Health Insight Analytics Production</td></tr><tr><td>Web Service Client</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.TransferSDA3.WebServicesClient">HSAA.TransferSDA3.WebServicesClient</a></td></tr><tr><td>Arguments</td><td>None</td></tr><tr><td>Returns</td><td>Production status string</td></tr></table>

### [PauseIngestionStartBatch](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16736)

Starts the interrupt business service, which pauses ingestion of data into tables and initiates:

*   The running of “smart” queries
    
*   The synchronization of cubes
    
*   Updates to the reporting cubes
    

<table><tr><td>HealthShare component</td><td>Health Insight Analytics Production</td></tr><tr><td>Web Service Client</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.TransferSDA3.WebServicesClient">HSAA.TransferSDA3.WebServicesClient</a></td></tr><tr><td>Arguments</td><td>None</td></tr><tr><td>Returns</td><td>None</td></tr></table>

### [SendDataToAnalytics](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_C16740)

Sends data from the Health Insight Feeder Gateway to Health Insight. This is a web service that has the same effect as stopping and restarting the Transmit Service in the Feeder production.

<table><tr><td>HealthShare component</td><td>UCR Feeder Gateway Production</td></tr><tr><td>Web Service Client</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HS.Gateway.Access.WebServicesClient">HS.Gateway.Access.WebServicesClient</a></td></tr><tr><td>Arguments</td><td>None</td></tr><tr><td>Returns</td><td>None</td></tr></table>
