# [Health Insight Production Details](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_production#HSAAREF_production)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

This page provides details on the business hosts that make up the HealthShare Health Insight production. You should not modify any settings of the production or of any business hosts beyond the ones mentioned in this appendix.

## [Business Services](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_production#HSAAREF_production_services)

The Health Insight production contains the following business services:

*   [EnsLib.JavaGateway.Service](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&CLASSNAME=EnsLib.JavaGateway.Service)
    
    This business service is used to communicate with JDBC-compatible databases. You may need to modify certain settings in order to work with JDBC-compatible databases. For more information, see [Using Java Messaging Service (JMS) in Interoperability Productions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=EJMS_overview) and [Setting Up the JDBC Connection to Store Persistent Requests in a Database](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_jdbc).
    
*   [HSAA.Common.Services](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Common.Services)
    
    This business service is used internally by the Health Insight production to communicate with other HealthShare components, like the Registry and any Edge Gateways.
    
*   [HSAA.TransferSDA3.Service.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.FilePR)
    
    This business service reads in streamlets from files in the local file system for persistent requests. [HSAA.TransferSDA3.Service.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.FilePR) reads in XML files containing request messages and sends messages to [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer) for further processing.
    
    <table><tr><th>Setting</th><th>Description</th></tr><tr><td><code>BaseFilePath</code></td><td>The absolute path to the files that you want to read in.</td></tr></table>
    
*   [HSAA.TransferSDA3.Service.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.SQLPR)
    
    This business service reads in streamlets from SQL tables for persistent requests. A request message can be broken down into fields and stored into SQL tables by [HSAA.TransferSDA3.Operation.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.SQLPR). This business service reconstructs the request messages and sends them to [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer) for further processing.
    
    <table><tr><th>Setting</th><th>Description</th></tr><tr><td><code>Call Interval</code></td><td>How often <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.TransferSDA3.Service.SQLPR">HSAA.TransferSDA3.Service.SQLPR</a> reads data from the SQL table.</td></tr><tr><td><code>DSN</code></td><td>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_readconfig_table">Configuring Health Insight to Read in Persistent Requests Stored in a Table</a>.</td></tr><tr><td><code>Credentials</code></td><td>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_readconfig_table">Configuring Health Insight to Read in Persistent Requests Stored in a Table</a>.</td></tr><tr><td><code>JDBCDriver</code></td><td>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_readconfig_table">Configuring Health Insight to Read in Persistent Requests Stored in a Table</a>.</td></tr><tr><td><code>JDBC Class Path</code></td><td>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_readconfig_table">Configuring Health Insight to Read in Persistent Requests Stored in a Table</a>.</td></tr><tr><td><code>JGService</code></td><td>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_readconfig_table">Configuring Health Insight to Read in Persistent Requests Stored in a Table</a>.</td></tr><tr><td><code>Data Settings &gt; Query</code></td><td>The query that is run each time <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.TransferSDA3.Service.SQLPR">HSAA.TransferSDA3.Service.SQLPR</a> reads data from the specified database. You may need to modify the name of the table in the default query’s <code>SELECT</code> statement to match the name of your table. Depending on the structure of your table, you may also need to modify the default query.</td></tr></table>
    
*   `HSAA.TransferSDA3.Service.WebServices`
    
    This business service receives `AnalyticsUpdateRequest` messages from the Feeder Gateway during data ingestion.
    
*   [HSAA.TransferSDA3.Service.Interrupt](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.Interrupt)
    
    This business service is responsible for periodically interrupting the data ingestion process so that the analytics batch can start. For details on the analytics batch, see [Key Processing Steps in the Health Insight Production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_details#HSAAREF_details_insightprod).
    
    <table><tr><th>Setting</th><th>Description</th></tr><tr><td><code>Call Interval</code></td><td>This setting determines how often <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.TransferSDA3.Service.Interrupt">HSAA.TransferSDA3.Service.Interrupt</a> interrupts the data ingestion process, in seconds. The minimum value is 300.</td></tr></table>
    
*   [HSAA.WS.WebServices](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.WS.WebServices)
    
    This business service receives analytics query definitions from other HealthShare components. Sometimes, other HealthShare components, like the Edge Gateways and the Registry, will send queries to Health Insight. After [HSAA.WS.WebServices](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.WS.WebServices) receives these queries, they are saved to the `HS_Message_Analytics.QueryRequest` table.
    
*   [HSAA.TransferSDA3.Service.ExecuteQueries](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.ExecuteQueries)
    
    This business service is responsible for starting [HSAA.TransferSDA3.Process.ExecuteQueries](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.ExecuteQueries) when analytics query execution [runs outside of the batch](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch).
    

Note that only one of [HSAA.TransferSDA3.Service.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.FilePR), [HSAA.TransferSDA3.Service.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.SQLPR), or `HSAA.TransferSDA3.Service.WebServices` can be active at once. The Health Insight production should only read in requests from one source at a time.

## [Business Processes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_production#HSAAREF_production_processes)

The Health Insight production contains the following business processes:

*   [HSAA.Query.Process](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Query.Process)
    
    This business process executes analytics query definitions. When query execution has completed, [HSAA.Query.Process](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Query.Process) sends a message to [HSAA.WS.RemoteOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.WS.RemoteOperations) with the results of the query. These results are forwarded to other HealthShare components.
    
    <table><tr><th>Setting</th><th>Description</th></tr><tr><td><code>Pool Size</code></td><td><p>This setting determines how many queries can be run at once. For example, setting <code>Pool Size</code> to <code>1</code> will cause queries to be run one at a time, while setting it to <code>2</code> will allow two queries to be run simultaneously.</p><p>The recommended pool size can vary based on your specific hardware. If you are uncertain regarding appropriate <code>Pool Size</code> values, please contact the <a href="https://www.intersystems.com/support-learning/support/">InterSystems Worldwide Response Center (WRC)</a>.</p></td></tr></table>
    
*   [HSAA.TransferSDA3.Process.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Batch)
    
    This business process is responsible for stopping and starting [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer) when an analytics batch occurs or ends, and also sends messages to [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch) so that [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch) can begin the work of the batch.
    
    <table><tr><th>Setting</th><th>Description</th></tr><tr><td><code>EnableDeferredACNQueries</code></td><td>This setting determines if ACN queries are run at the end of an analytics batch. If unchecked, ACN queries are saved but are not run at the end of a batch. Saved ACN queries will be run the next time an analytics batch is run with this setting checked.</td></tr><tr><td><code>MaxNumQuery</code></td><td>Determines how many analytics query definitions are run during each analytics batch. A value of <code>-1</code> will cause all queries to be run.</td></tr></table>
    
*   [HSAA.TransferSDA3.Process.ExecuteQueries](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.ExecuteQueries)
    
    This business process sends the top `MaxNumQuery` analytics queries from `HS_Message_Analytics.QueryRequest` to [HSAA.Query.Process](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Query.Process) for processing if analytics query execution is configured to [run outside of the batch](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch).
    
*   [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer)
    
    This business process receives `AnalyticsUpdateRequest` messages from the [HSAA.TransferSDA3.WebServices](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.WebServices) and can send these messages to one of the following three business operations:
    
    *   [HSAA.TransferSDA3.Operation.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.FilePR)
        
    *   [HSAA.TransferSDA3.Operation.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.SQLPR)
        
    *   [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer)
        
    
    <table><tr><th>Setting</th><th>Description</th></tr><tr><td><code>ToTransfer</code></td><td>This setting determines if <code>AnalyticsUpdateRequest</code> messages are sent to the <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.TransferSDA3.Operation.Transfer">HSAA.TransferSDA3.Operation.Transfer</a> for processing into the Health Insight clinical tables.</td></tr><tr><td><code>ToFile</code></td><td>This setting determines if <code>AnalyticsUpdateRequest</code> messages are sent to the <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.TransferSDA3.Operation.FilePR">HSAA.TransferSDA3.Operation.FilePR</a> to be saved into files for persistent requests. For more information, see <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist">Setting Up and Using Persistent Requests</a>.</td></tr><tr><td><code>ToSQL</code></td><td>This setting determines if <code>AnalyticsUpdateRequest</code> messages are sent to the <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.TransferSDA3.Operation.SQLPR">HSAA.TransferSDA3.Operation.SQLPR</a> to be saved into tables for persistent requests. For more information, see <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist">Setting Up and Using Persistent Requests</a>.</td></tr></table>
    

> **Note:**
> 
> Note that you should not adjust configuration settings or take other measures to free messages that are queued between [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer) (the Transfer Process) and [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer) (the Transfer Operation), as these queued messages are a normal part of data ingestion into Health Insight. You should also not modify or kill the `^IRIS.HSAA.TransferAnalyticsID` global, which ensures chronological processing of patient updates by the Transfer Process and Transfer Operation, without first consulting the [InterSystems Worldwide Response Center (WRC)](https://www.intersystems.com/support-learning/support/).
> 
> More specifically, the Transfer Process is a first-in first-out (FIFO) business process that handles a production queue of AnalyticsUpdateRequest messages. During normal data ingestion into Health Insight, each patient message that is queued on the Transfer Process is sent on a FIFO basis to a queue on the Transfer Operation for processing. When it sends a message to the Transfer Operation for processing, the Transfer Process sets a global node in `^IRIS.HSAA.TransferAnalyticsID` that contains the patient identifier and message ID to indicate active processing of the message. Health Insight uses this global to track which patient messages are undergoing active processing on the Transfer Operation, and prevents subsequent messages for those patients from being processed until the previous messages have finished processing.

## [Business Operations](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_production#HSAAREF_production_operations)

The Health Insight production contains the following business operations:

*   `AccessGatewayFeeder`
    
    This business operation is responsible for communicating with the Feeder Gateway.
    
    <table><tr><th>Setting</th><th>Description</th></tr><tr><td><code>SOAP Credentials</code></td><td>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ECONFIG_reusable#ECONFIG_reusable_credentials">Defining Credentials</a>.</td></tr><tr><td><code>ServiceName</code></td><td><p>This setting specifies the name of the service listed in the service registry that is the Web service where SOAP requests from this Web client should be directed.</p><p>On systems that are not federated, this setting should either be of the form <code>networkhostname</code>:<code>servicename</code> (for example, <code>USE4140jsmith:HSANALYTICS</code>) or just <code>servicename</code> (for example, <code>HSANALYTICS</code>), where <code>servicename</code> is the corresponding Service Name of the service from the Service Registry, and <code>networkhostname</code> is the Network Host Name of the instance that hosts the service, if one is included in the Service Registry entry for that service. On a federated system, this must take the form <code>networkhostname</code>:<code>servicename</code>. In both the federated and non-federated cases, <code>networkhostname</code> should exactly match the Network Host Name entered in the <code>Configure Network Host Name</code> dialog of the HealthShare Installer Wizard. If your system is mirrored, then <code>networkhostname</code> must match the VIP alias of the mirrored system as it appears in the Service Registry.</p></td></tr></table>
    
*   `AccessGatewayViewer`
    
    This business operation is responsible for communicating with the Viewer Access Gateway.
    
    <table><tr><th>Setting</th><th>Description</th></tr><tr><td><code>SOAP Credentials</code></td><td>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ECONFIG_reusable#ECONFIG_reusable_credentials">Defining Credentials</a>.</td></tr><tr><td><code>ServiceName</code></td><td><p>This setting specifies the name of the service listed in the service registry that is the Web service where SOAP requests from this Web client should be directed.</p><p>See the previous description for the <code>ServiceName</code> setting of <code>AccessGatewayFeeder</code> for details.</p></td></tr></table>
    
*   [HS.Gateway.HSWS.RemoteOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.HSWS.RemoteOperations)
    
    This business operation is responsible for sending notifications to other HealthShare components, like the Edge Gateways and the Registry.
    
*   [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch)
    
    This business operation performs the work of analytics batches. For details, see [Key Processing Steps in the Health Insight Production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_details#HSAAREF_details_insightprod).
    
*   [HSAA.TransferSDA3.Operation.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.FilePR)
    
    This business operation is one of three possible targets for `AnalyticsUpdateRequest` messages coming from [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer). [HSAA.TransferSDA3.Operation.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.FilePR) saves the requests to a file specified by the `BaseFilePath` setting. For more information, see [Setting Up and Using Persistent Requests](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist).
    
    <table><tr><th>Setting</th><th>Description</th></tr><tr><td><code>Additional Settings</code> &gt; <code>Failure Timeout</code></td><td>The number of seconds to continue message delivery attempts. By default, this setting has a value of <code>-1</code> so that no messages are skipped.</td></tr><tr><td><code>BaseFilePath</code></td><td>The absolute path to which you want the files saved.</td></tr></table>
    
*   [HSAA.TransferSDA3.Operation.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.SQLPR)
    
    This business operation is one of three possible targets for `AnalyticsUpdateRequest` messages coming from [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer). [HSAA.TransferSDA3.Operation.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.SQLPR) saves the requests to a SQL table.
    
    <table><tr><th>Settings</th><th>Description</th></tr><tr><td><code>DSN</code></td><td>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_jdbc">Setting Up the JDBC Connection to Store Persistent Requests in a Database</a>.</td></tr><tr><td><code>Credentials</code></td><td>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_jdbc">Setting Up the JDBC Connection to Store Persistent Requests in a Database</a>.</td></tr><tr><td><code>JDBCDriver</code></td><td>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_jdbc">Setting Up the JDBC Connection to Store Persistent Requests in a Database</a>.</td></tr><tr><td><code>JDBC Class Path</code></td><td>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_jdbc">Setting Up the JDBC Connection to Store Persistent Requests in a Database</a>.</td></tr><tr><td><code>JGService</code></td><td>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_jdbc">Setting Up the JDBC Connection to Store Persistent Requests in a Database</a>.</td></tr><tr><td><code>Additional Settings</code> &gt; SQLString</td><td><p>The query that is run each time <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.TransferSDA3.Operation.SQLPR">HSAA.TransferSDA3.Operation.SQLPR</a> inserts data into the specified database. You may need to modify the name of the table in the default query’s <code>INSERT</code> statement to match the name of your table. Depending on the structure of your table, you may also need to modify the default query.</p><p>Note that you may not change the order of the fields supplied in the <code>INSERT</code> statement. Additional fields may be added to the end of the <code>INSERT</code> statement.</p></td></tr><tr><td><code>Additional Settings</code> &gt; <code>Failure Timeout</code></td><td>The number of seconds to continue message delivery attempts. By default, this setting has a value of <code>-1</code> so that no messages are skipped.</td></tr></table>
    
*   [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer)
    
    This business operation is one of three possible targets for `AnalyticsUpdateRequest` messages coming from [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer). [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer) saves the requests to the Health Insight clinical tables.
    
    <table><tr><th>Setting</th><th>Description</th></tr><tr><td><code>Pool Size</code></td><td><p>This setting determines how many requests can be processed at once.</p><p>The recommended pool size can vary based on your specific hardware. If you are uncertain regarding appropriate <code>Pool Size</code> values, please contact the <a href="https://www.intersystems.com/support-learning/support/">InterSystems Worldwide Response Center (WRC)</a>.</p></td></tr></table>
    
*   [HSAA.WS.RemoteOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.WS.RemoteOperations)
    
    This business operation is responsible for sending messages to other HealthShare components.
