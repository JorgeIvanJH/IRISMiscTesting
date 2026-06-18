# [Data Feed Details](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_details#HSAAREF_details)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

This page provides details on the behavior of the [Feeder Gateway production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_details#HSAAREF_details_feedprod) and the [Health Insight production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_details#HSAAREF_details_insightprod).

## [Key Processing Steps in the Feeder Gateway](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_details#HSAAREF_details_feedprod)

The HealthShare Health Insight Feeder Access Gateway (formerly known as the dedicated Access Gateway) is responsible for all communications between Health Insight and HealthShare Unified Care Record. This production periodically checks and sends data to the Health Insight production, as follows. The steps here also indicate where Health Insight starts new sessions.

1.  The [HS.Gateway.Analytics.TransmitService](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.TransmitService) periodically checks to see whether it is appropriate to start acquiring data to send to Health Insight. Specifically, at regular intervals (controlled by the `Call Interval` setting), this business service checks the following conditions:
    
    1.  Is the Feeder Gateway currently sending data to Health Insight? If so, the business service does nothing (until the next call interval).
        
    2.  Are there any patients to process? If so, the business service sends a message to [HS.Gateway.Analytics.BatchProcess](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.BatchProcess). If there are no patients to process, the business service does nothing (until the next call interval).
        
    
    Note that these checks do not add entries to the message viewer or message trace.
    
2.  (In the next session) When [HS.Gateway.Analytics.BatchProcess](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.BatchProcess) receives this message, it sends a message to [HS.Hub.HSWS.RemoteOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Hub.HSWS.RemoteOperations) (the HUB business operation), which in turn communicates with the Registry. The purpose of this message is to obtain a list of MPIIDs to process.
    
    This message carries the value of the `Transmit batch size` setting from the [`Additional Settings`](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional) page, which specifies the maximum number of MPIIDs to retrieve.
    
    The response message contains the MPIIDs that should be processed.
    
3.  (In the next session) Using the first MPIID, the [HS.Gateway.Analytics.BatchProcess](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.BatchProcess) sends a message to [HS.Gateway.Access.AnalyticsProcess](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Access.AnalyticsProcess). The purpose of this message is to initiate processing for the given patient.
    
4.  The [HS.Gateway.Access.AnalyticsProcess](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Access.AnalyticsProcess) sends a message (containing the same MPIID) to [HS.Hub.HSWS.RemoteOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Hub.HSWS.RemoteOperations) (the HUB business operation), which in turn communicates with the Registry. The purpose of this message is to obtain details about the data that should be retrieved for the given patient.
    
    The response message contains the analytics ID that corresponds to the given MPIID. It also contains the part of the update queue that is relevant to the given patient; this information indicates which Edge Gateways must be contacted to retrieve the data.
    
5.  For each Edge Gateway that contains data needed for processing for this patient, the [HS.Gateway.Access.AnalyticsProcess](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Access.AnalyticsProcess) sends a message to [HS.Gateway.HSWS.RemoteOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.HSWS.RemoteOperations) (the GATEWAY business operation), which in turn communicates with the needed Edge Gateways. The request messages indicate which streamlets are needed, and the response messages contain the streamlets.
    
6.  After all the needed streamlets have been retrieved, the [HS.Gateway.Access.AnalyticsProcess](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Access.AnalyticsProcess) sends a message to [HS.Gateway.Analytics.RemoteOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.RemoteOperations), which in turn communicates with the Health Insight production.
    
    The request message is an [HS.Message.AnalyticsUpdateRequest](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Message.AnalyticsUpdateRequest) message. The message contains the analytics ID (but not the MPIID), and it contains all the information needed to update the data for this patient within the Health Insight tables.
    
7.  (In the next session) Using the next MPIID, the [HS.Gateway.Analytics.BatchProcess](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.BatchProcess) sends a message to [HS.Gateway.Access.AnalyticsProcess](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Access.AnalyticsProcess). Processing continues for this patient as described in steps 3 through 6.
    

Each additional MPIID is processed in a separate session.

The following table lists the settings that are relevant to the processing described here:

<table><tr><th>Setting</th><th>Location</th></tr><tr><td><code>Call Interval</code></td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HS.Gateway.Analytics.TransmitService">HS.Gateway.Analytics.TransmitService</a></td></tr><tr><td><code>MaxNumMPIID</code></td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HS.Gateway.Analytics.BatchProcess">HS.Gateway.Analytics.BatchProcess</a></td></tr></table>

For information, see “[Configuring the Feeder Gateway Production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_config)” in the chapter “[Setting Up a New Feeder Gateway (With or Without Mirroring)](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder).”

## [Key Processing Steps in the Health Insight Production](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_details#HSAAREF_details_insightprod)

The Health Insight production is responsible for processing data for use by Health Insight.

When the [HSAA.TransferSDA3.WebServices](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.WebServices) receives an `AnalyticsUpdateRequest` message from the Feeder Gateway, it stores the message in the `HS_Message.AnalyticsUpdateRequest` table, which serves as the message queue for the Health Insight production. This step does not add anything to the message viewer or message trace. The [HSAA.TransferSDA3.WebServices](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.WebServices) sends the `AnalyticsUpdateRequest` message to the [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer), which then sends the message to the [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer). Depending on the configuration of the `ToTransfer`, `ToFile`, and `ToSQL` settings in the [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer) business process, [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer) could send the `AnalyticsUpdateRequest` message to any combination of the following business operations:

*   [HSAA.TransferSDA3.Operation.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.FilePR)
    
*   [HSAA.TransferSDA3.Operation.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.SQLPR)
    
*   [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer)
    

[HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer) processes the `AnalyticsUpdateRequest`, breaks up the message, and uses it to update the Health Insight clinical tables, for example [HSAA.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Patient).

Periodically, Health Insight will trigger an analytics batch, which interrupts data ingestion as follows:

1.  At regular intervals (controlled by the `Call Interval` setting of this business service), the [HSAA.TransferSDA3.Service.Interrupt](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.Interrupt) checks to see if it's appropriate to start a new batch. If the previous analytics batch has finished, it sends a message to [HSAA.TransferSDA3.Process.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Batch).
    
2.  The [HSAA.TransferSDA3.Process.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Batch) stops [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer), halting the ingestion of data.
    
    Note that you can forcefully halt ingestion if the system is taking a long time to do so while the batch process is starting. For more information on this option, see [Halting Ingestion During the Batch Process](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_phase3_stop), earlier in this book.
    
3.  The [HSAA.TransferSDA3.Process.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Batch) begins sending messages to [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch), which begins the work of the batch.
    
4.  The [HSAA.TransferSDA3.Process.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Batch) sends an `HSAAPostTransferRequest` message to [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch). The [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch) executes any code specified by the option `Post-transfer processing method`.
    
5.  If cube sync is enabled, the [HSAA.TransferSDA3.Process.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Batch) sends an `HSAASynchronizeCubesRequest` message to the [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch). [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch) synchronizes the Health Insight cubes, other than those used by the Platform Information dashboards.
    
    The control for choosing which cubes are included in the Health Insight cube sync process can be found on the `Cube Sync Settings` page, under `Cube Group Settings`.
    
6.  The [HSAA.TransferSDA3.Process.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Batch) sends an `HSAAPostSynchronizeRequest` message to the [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch). [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch) executes any code specified by the option `Post-synchronization processing method`.
    
7.  The [HSAA.TransferSDA3.Process.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Batch) sends an `HSAAPostBatchRequest` message to the [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch). [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch) executes any code specified by the option `Post-batch processing method`.
    
8.  The [HSAA.TransferSDA3.Process.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Batch) sends an `HSAAUpdateReportCubesRequest` message to [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch). [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch) synchronizes the cubes used in the Platform Information dashboards.
    
    The control for choosing whether or not to synchronize these cubes can be found on the `Cube Sync Settings` page. Checking `Sync Reporting Cubes` will cause the reporting cubes to be synchronized during this step.
    
9.  The [HSAA.TransferSDA3.Process.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Batch) sends any analytics query definitions to the [HSAA.Query.Process](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Query.Process) and waits for the completion of any such queries. Analytics queries are only sent if you have not configured them to [run outside the batch](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch).
    
10.  The [HSAA.TransferSDA3.Process.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Batch) updates internal tables used by the Platform Information dashboards. This step does not add any entries to the message viewer or the message trace.
     
11.  Finally, the [HSAA.TransferSDA3.Process.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Batch) re-enables [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer), restarting the ingestion of data.
     

The following table lists the settings and options that are relevant to the processing described here:

<table><tr><th>Item</th><th>Location</th></tr><tr><td><code>Call Interval</code> setting</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.TransferSDA3.Service.Interrupt">HSAA.TransferSDA3.Service.Interrupt</a></td></tr><tr><td><code>Post-transfer processing method</code> option</td><td><code>Additional Settings</code>, accessible from the Health Insight home page</td></tr><tr><td><code>Sync Reporting Cubes</code> setting</td><td rowspan="2"><code>Cube Sync Settings</code>, accessible from the Health Insight home page</td></tr><tr><td><code>Cube Groups Settings</code></td></tr><tr><td><code>Post-synchronization processing method</code> option</td><td rowspan="2"><code>Additional Settings</code>, accessible from the Health Insight home page</td></tr><tr><td><code>Post-batch processing method</code> option</td></tr></table>

For information on the settings, see “[Configuring the Health Insight Production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_config).”

For information on the options in the `Additional Settings` group, see “[Specifying Additional Settings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional).”
