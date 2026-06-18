# [Troubleshooting Data Feed Problems in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq).

This chapter discusses specific data feed problems and their solutions. It discusses the following scenarios:

*   [Cubes have no data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_cubes_empty)
    
*   [Failed to configure synchronization](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_fail_to_configsync)
    
*   [Unable to open TCP/IP socket](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_tcpip_prob)
    
*   [No production is running](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_xferprod_stopped)
    
*   [Other timeout errors](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_timeouts)
    
*   [Streamlet processing errors](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_streamletprocerrr)
    
*   [Cube build/sync errors](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_cubeerr)
    
*   [Frozen query plan](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_frozenquery)
    
*   [Empty Fields in SQL Tables or No Data members in Cubes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_nodata)
    
*   [Patient Data Is Blocked at the Feeder](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_feederpatientblocked)
    

For problems not listed here, it may be necessary to examine the flow of data within HealthShare Unified Care Record, including HealthShare Health Insight. This book does not describe this task specifically (apart from [tracking patient data to its source](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_trace)), but the task involves working with the production message search and trace pages. For general information on these tools, see [Managing Unified Care Record Productions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEENS).

> **Note:**
> 
> Feeder Gateway is short for Health Insight Feeder Access Gateway. In previous releases, this gateway was known as the dedicated Access Gateway.

## [Cubes Have No Data](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_cubes_empty)

### [Symptom](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_cubes_empty_sym)

The Health Insight cubes contain no data.

### [Diagnosis](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_cubes_empty_diag)

The Health Insight cubes have not yet been built. The Health Insight production has a setting that controls whether it synchronizes the cubes with data as it arrives, but this setting has no effect if the cubes have not yet been built.

### [Solution](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_cubes_empty_sol)

Build the Health Insight cubes. See “[API for Monitoring and Managing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api)”.

## [Failed to Configure Synchronization](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_fail_to_configsync)

### [Symptom](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_fail_to_configsync_sym)

When you try to start the Health Insight production, you receive the following error:

```
15:08:16.695:Ens.Director: Production 'HSANALYTICSPKG.HSAAProduction' starting...
Failed to configure synchronization

15:08:16.725:...KG.HSAAProduction: Startup Error 0 T6248Server Application Error)0
...
15:08:16.995:Ens.Director: Production 'HSANALYTICSPKG.HSAAProduction' started.
Done.
```

### [Diagnosis](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_fail_to_configsync_diag)

This error occurs if the Registry instance is not running or if the Registry production is not running.

### [Solution](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_fail_to_configsync_sol)

Make sure the Registry instance is running, start the Registry production, and then restart the Health Insight production.

## [Unable to Open TCP/IP Socket](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_tcpip_prob)

### [Symptom](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_tcpip_prob_sym)

In the Feeder Gateway instance, the event log includes an entry like the following:

```
ERROR #6059: Unable to open TCP/IP socket to server <servername>:<port>
```

### [Diagnosis](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_tcpip_prob_diag)

This message occurs if the Health Insight instance is not running or if the Health Insight production is not running. The message can also occur if there is a configuration problem and the Feeder Gateway does not have the correct location for the Health Insight production.

### [Solution](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_tcpip_prob_sol)

Make sure the Health Insight instance is running and start the Health Insight production.

If the error remains, go to the Service Registry on the Hub, and correct the definition of the service that points to the Health Insight production (for example, HSANALYTICS:WebServices — the name of the service depends upon the namespace in which the Health Insight production resides). In this case, also consult with the implementation staff.

## [No Production Is Running](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_xferprod_stopped)

### [Symptom](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_xferprod_stopped_sym)

In the Feeder Gateway instance, the event log includes an entry like the following

```
ERROR #6248: SOAP response is a SOAP fault:
faultcode=Server
faultstring=Server Application Error
faultactor=HSAA.TransferSDA3.WebServices
detail <error xmlns="http://www.intersystems.com/hsaa">
<text>ERROR &lt;Ens&gt;ErrProductionNotRunning:
No production is running</text>
</error>
```

### [Diagnosis](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_xferprod_stopped_diag)

This message indicates that the Health Insight production is not running.

Notice that `faultactor` specifies the Health Insight production, or more specifically, the web service in that production.

### [Solution](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_xferprod_stopped_sol)

If the Health Insight production stops running during the data feed process (or at any other time), simply start it again.

No further action is necessary.

## [Other Timeout Errors](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_timeouts)

If there was a timeout while an Edge Gateway was retrieving a particularly large or complex patient record, there is a different timeout message. In this case, increase the session timeout period for the web application in which that Edge Gateway is running. See “[Web Applications](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSA_manage_applications#GSA_manage_applications_typecsp).”

## [Streamlet Processing Errors](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_streamletprocerrr)

This section discusses a kind of error that you can detect only in the Health Insight production. It is important to monitor this production for such errors and then to correct the situation.

### [Symptoms](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_streamletprocerrr_id)

This kind of error can be seen in multiple places, with the same error message:

*   [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer) has an error, with a message like the following:
    
    ```
    ERROR <HSAAErr>Previous: AnalyticsID IJFMEF marked as having a previous error
    ```
    
*   The production Message Viewer and message trace display similar information.
    
*   The [Health Insight log](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor_xferlog) displays similar information. Use any [`Log Level`](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_config_loglevel) other than `None`.
    
    Note that the Health Insight log displays only errors related to processing streamlets.
    

### [Diagnosis](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_streamletprocerrr_diag)

These error messages indicate a streamlet processing error. A streamlet is a unit of data received by the Health Insight production. A data issue can cause a streamlet processing error, after which the Health Insight production cannot process data for the patient whose data was being processed. If this occurs, no new data for this patient is available in the Health Insight source tables and cubes. If the production receives any further data for that patient, the production does not process that data either (so that you are protected from the data corruption that could result from processing the data in the wrong order).

### [Solution](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_streamletprocerrr_whatnext)

If a streamlet processing error occurs, the Health Insight production does not transmit any more data for that particular patient into the Health Insight source tables. Your goal is to transmit the missing data and ensure that additional data for this patient is also transmitted.

The following steps are one suggested approach:

1.  First, within the analytics instance:
    
    1.  Log in to the Management Portal.
        
    2.  Select `HealthShare.`
        
    3.  Select the name of your analytics namespace, typically `ANALYTICS` or `HSANALYTICS`.
        
    4.  Select `Internal Data Management` > `Patient Error Management`.
        
        This page lists the patients (if any) whose data could not be processed.
        
        Note that you can also use the event log to identify the patients.
        
    5.  Make a note of the Analytics ID of these patients.
        
    6.  Clear the errors using either `ClearAllPatientsInErrorList()` or `ClearPatientsInErrorList()`, then use the Resend feature to resend the messages for the patient. See the [subsection](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_streamletprocerrr_resending). Also see [API for Monitoring and Managing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api) for more information on the API methods.
        
    7.  Alternatively, you may call `RequeueAllPatientsInErrorListAndClear()` or `RequeuePatientsInErrorListAndClear()` to resend the messages for the patients and clear the errors.
        
2.  If the previous step does not correct the error, examine the data for this patient. Typically there is a data problem of some kind. Possible causes of errors include these:
    
    *   A text field is too long to be stored
        
    *   A date field contains an invalid date or a date in an incorrect format
        
3.  If the problem is a data error:
    
    1.  Correct the data in the source system from which it came.
        
    2.  Clear the patient error using either `ClearAllPatientsInErrorList()` or `ClearPatientsInErrorList()` so that the Health Insight production will process the new data when it arrives.
        
    3.  Resend it into the Edge Gateway that originally processed this data. Details depend upon the kind of data and the kind of Edge Gateway. This book does not describe this task.
        

#### [Resending the Messages in the Health Insight Production](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_streamletprocerrr_resending)

To resend the messages for a given patient within the Health Insight production, do the following:

1.  In the Health Insight production, find the messages for this patient. To do so:
    
    1.  In the message viewer in the analytics namespace, expand the `Extended Criteria` section.
        
    2.  Select `Add Criterion`.
        
    3.  For `Criterion Type`, select `Search Table Field`.
        
    4.  For `Class`, select `HSAA.TransferSDA3.SearchTable.AnalyticsUpdateRequest`.
        
    5.  Edit `Condition` to be `IF AnalyticsID = PatientIDHere` where `PatientIDHere` is the analytics ID.
        
    6.  Select `OK`.
        
    7.  Select `Search`.
        
    
    The message viewer then displays the transfer messages for the selected patient. Do not resend them yet.
    
2.  Resend the messages. To do so, return to the Portal and do the following:
    
    1.  Select the check box at the top of column of check boxes.
        
    2.  Select `Resend`. This displays the `Resend Messages` page.
        
    3.  Select `Resend`. The messages are then resent in order, starting with the oldest message.
        
3.  After the messages have been resent, enter the following command in the Terminal window:
    
    ```objectscript
     do ##class(HSAA.API.Cubes).SynchronizeAllCubes()
    ```
    

## [Build/Sync Errors](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_cubeerr)

### [Symptoms](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_cubeerr_sym)

The Most Recent Batch Details dashboard displays a nonzero count for Sync Error Count.

> **Note:**
> 
> This kind of error should be extremely rare but is serious because it can mean a data integrity issue. However, if such an error does occur, Health Insight will continue the analytics batch.

### [Diagnosis](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_cubeerr_diag)

Cube build/sync errors can mean that the cubes are inconsistent with each other (for example, an encounter record may point to a patient that does not exist in the Patients cube). In most cases, such errors are simply the result of a timing problem. (Note that the errors shown in the following example were artificially caused.)

### [Solution](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_cubeerr_sol)

1.  Select `System Explorer` > `Globals`.
    
2.  Scroll to `^DeepSee.BuildErrors` and click the `View` link. You should see something like this:
    
    [Image: View Global Data page showing nodes of ^DeepSee.BuildErrors, with subscripts containing names of cubes with build errors]
3.  The left side of the display indicates the cubes that have build errors. The part in quotation marks is the logical name of a Health Insight cube.
    
    The right side of the display (that is, to the right of the equals sign) shows the details of the errors; you can ignore this area because there is an easier way to see the error details.
    
4.  Make a note of the cubes that had problems. In this example, three cubes had problems:
    
    *   HSAACAREPROVIDERSITE
        
    *   HSAAENCOUNTER
        
    *   HSAAEVENTCAREPROVIDERSITE
        
5.  Open the Terminal on the analytics instance and switch to the analytics namespace.
    
6.  Use the `%PrintBuildErrors()` method of [%DeepSee.Utils](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&CLASSNAME=%25DeepSee.Utils), as follows:
    
    ```objectscript
     do ##class(%DeepSee.Utils).%PrintBuildErrors(cubename)
    ```
    
    Where `cubename` is the logical name of the cube, in quotes.
    
    This method displays information about all build errors for that cube. For example (with added line breaks):
    
    ```objectscript
    ANALYTICS>d ##class(%DeepSee.Utils).%PrintBuildErrors("HSAAEVENTCAREPROVIDERSITE")
        1   Source ID: 10384
            ERROR #5001: Missing relationship reference in HSAAEventCareProviderSite:
            source ID 10384 missing reference to RxPatient 1654
    
        2   Source ID: 10385
            ERROR #5001: Missing relationship reference in HSAAEventCareProviderSite:
            source ID 10385 missing reference to RxPatient 1654
    
        3   Source ID: 10386
            ERROR #5001: Missing relationship reference in HSAAEventCareProviderSite:
            source ID 10386 missing reference to RxPatient 1654
    
    3 build error(s) for 'HSAAEVENTCAREPROVIDERSITE'
    ```
    
    `Source ID` is the ID of the source record used for the given cube.
    
7.  Consider the nature of each error and correct as appropriate.
    
    *   In the case of a “missing reference” error, first call the `%FixBuildErrors()` method (next step) and see if that fixes the problem. If so, the underlying cause was merely a timing issue. If `%FixBuildErrors()` does not fix the problem, the underlying cause is bad data of some kind. In that case, examine the data carefully and correct it (resending data as appropriate). The [next chapter](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_resend) has information on resending data to Health Insight.
        
    *   In the case of errors other than a “missing reference” error, examine the data carefully and correct it (resending data as appropriate; see the [next chapter](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_resend)).
        
8.  Still in the analytics namespace, call the `%FixBuildErrors()` method of [%DeepSee.Utils](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&CLASSNAME=%25DeepSee.Utils), passing as the argument the name of the cube that should be fixed. Note that this argument is not case-sensitive. This method returns a status code (which should be 1 in the case of success). For example:
    
    ```objectscript
     set sc=##class(%DeepSee.Utils).%FixBuildErrors("hsaaencounter")
    ```
    
    This method completes the synchronization for the given cube. For example:
    
    ```objectscript
    ANALYTICS>set sc=##class(%DeepSee.Utils).%FixBuildErrors("hsaacareprovidersite")
    Fact '1263' corrected
    Fact '1264' corrected
    Fact '1265' corrected
    
    
    3 fact(s) corrected for 'hsaacareprovidersite'
    0 error(s) remaining for 'hsaacareprovidersite'
    
    ANALYTICS>w sc
    1
    ```
    
    Repeat as needed.
    
9.  Check that zero errors remain for each cube.
    
10.  If any post-synchronization code is defined, run that code manually. Health Insight cannot run it automatically.
     
     See [Specifying Additional Settings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional) in the chapter “[Customizing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube)” in the Health Insight Installation and Configuration Guide.
     

## [Frozen Query Plan](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_frozenquery)

### [Symptoms](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_frozenquery_sym)

You receive `SQL error –76` when running a query, typically a query of the form:

```
SELECT * FROM <TableName>
```

### [Diagnosis](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_frozenquery_diag)

This may be the result of a query whose query plan was frozen, but the underlying table metadata has changed. See the chapter “[Frozen Plans](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSOC_frozenplans)” in the InterSystems SQL Optimization Guide for more information on frozen query plans.

### [Solution](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_frozenquery_sol)

You can unfreeze all query plans in the Health Insight namespace by running the following command from a terminal session:

```objectscript
 Do $System.SQL.FreezePlans(2 ,1, , .errors)
```

Confirm that the `errors` variable has a value of `0`. This should unfreeze the query plan and eliminate the error.

## [Empty Fields in SQL Tables or No Data Members in Cubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_nodata)

### [Symptoms](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_nodata_sym)

You query the Health Insight Patient SQL table and find rows with empty Age fields, or you find that certain Business Intelligence cubes have `No Data` members when queried via MDX or pivot tables.

### [Diagnosis](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_nodata_diag)

These symptoms may be the result of erroneous data coming into Health Insight. For example, if your SDA contains a patient where DeathTime is earlier than BirthTime, that patient's Age field will be empty in the [HSAA.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Patient) table, and a `No Data Age` member will exist in the Patient cube. Similar `No Data` symptoms can also occur in the Encounter and Appointment cubes. You might see `No Data` members in your Encounters cube under the `Age At Encounter` dimension if your SDA provides a StartTime for an encounter that is earlier than the patient's time of birth. Similarly, you might see a `No Data` member under the `Age At Appointment` dimension in your Appointment cube if your SDA provides a FromTime that is earlier than a patient's time of birth.

### [Solution](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_nodata_sol)

Ensure that data coming into Health Insight does not have the types of errors mentioned above.

## [Patient Data Is Blocked at the Feeder](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_feederpatientblocked)

### [Symptom](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_feederpatientblocked_sym)

Expected patient data is missing from Health Insight, or a patient's data remains stale, even after any underlying data problems have been corrected on the Edge. For example:

*   A known patient is missing from Health Insight.
    
*   A customer may expect to see a certain number of patients with a specific diagnosis during a given time period, but finds none or significantly fewer than expected in Health Insight.
    
*   A query, pivot, or report returns no patients, or significantly fewer patients than expected, for a diagnosis, procedure, or encounter type during a given time period.
    
*   New updates for a previously errored patient never appear in Health Insight.
    

### [Diagnosis](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_feederpatientblocked_diag)

When data retrieval from the Edge errors out at the Feeder for a patient, the Feeder records the patient in the `^HS.Feeder.PatientErrors` global in the Feeder namespace and blocks later updates for that patient until the patient is marked fixed.

An error and a warning are logged in the message trace for [HS.Gateway.Access.AnalyticsProcess](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Access.AnalyticsProcess). Additional warnings are logged when later updates are received for that patient, with a message similar to:

```
MPIID <someID> errored out previously and has not been fixed. Ingestion of this patient's data is blocked.
```

Possible causes of such errors include the following:

*   Data or content errors. Because the Feeder performs data aggregation and transformation, including XSLT processing, invalid or unexpected XML data can cause errors.
    
*   Queue, production, or system errors. These include operational failures in the messaging and production pipeline, such as messages not being handled by the production as expected, job failures, queue backlogs or stuck messages, and disk, memory, or cache-related problems. In these cases, the issue may not be with the patient data itself, but with the system’s ability to process and forward that data.
    

Network or connectivity errors can also interrupt processing, but they are handled differently and are not recorded in `^HS.Feeder.PatientErrors`.

### [Solution](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_feederpatientblocked_sol)

1.  Identify the affected patient MPIID via the [HS.Gateway.Access.AnalyticsProcess](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Access.AnalyticsProcess) message traces, or by viewing the `^HS.Feeder.PatientErrors` global in the Feeder namespace.
    
2.  Review the error and warning information in the message trace for [HS.Gateway.Access.AnalyticsProcess](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Access.AnalyticsProcess).
    
3.  Investigate and correct the underlying data problem on the Edge.
    
4.  In the Feeder namespace, run the following command in the Terminal:
    
    ```
    Set ^HS.Feeder.PatientErrors(<tMPIID>,"Fixed") = 1
    ```
    
    Replace `<tMPIID>` with the MPIID of the affected patient.
    
5.  Once the patient is marked fixed, the next time an update for that patient is sent to Health Insight through the Feeder, the patient is no longer blocked. Resends for that patient can also pass through the Feeder without being blocked.
    
6.  Verify that the patient's data now appears correctly in Health Insight.
