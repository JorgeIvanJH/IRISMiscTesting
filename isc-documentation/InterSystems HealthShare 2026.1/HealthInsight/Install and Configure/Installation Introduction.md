# [Introduction to Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

HealthShare Health Insight is a HealthShare add-on product, developed to provide near real-time, analytical access to comprehensive clinical data available to your organization from HealthShare Unified Care Record. Using Unified Care Record to collect and normalize data, Health Insight maintains a clinically accurate, patient-centric view of the data, combined with high performing InterSystems IRIS Business Intelligence technology for data analysis.

> **Important:**
> 
> This book assumes that you have an existing Unified Care Record implementation.

## [Health Insight Purpose and Features](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_purpose)

Health Insight is a platform for developing analytics solutions. This platform uses data that is already being collected and normalized via Unified Care Record and provides an environment, tools, and solutions that you can use to explore this data and to develop analytics solutions for your customers. Health Insight provides the following features:

*   Example dashboards. These are browser-based displays of data, especially aggregated data (sums, averages, and so on). For example, in Health Insight, dashboards typically display data that is aggregated across sets of patients or aggregated across patient encounters, and so on.
    
*   An extensive, customizable analytics model (a set of optional InterSystems IRIS Business Intelligence cubes and the underlying relational tables).
    
*   An analysis environment.
    
*   A patient-centered SQL model of clinical data, based on the data stored in Unified Care Record.
    
    Health Insight uses these tables as the basis for its cubes. You can directly query the tables for your own purposes.
    
*   Data transfer services that update data in near real-time.
    
*   The ability to define analytics query definitions, which are reusable definitions that query data in the analytics instance. These query definitions can be used in two ways:
    
    *   In the delivery of clinical messages. Unified Care Record provides the ability to deliver clinical messages, in a variety of formats and delivery methods. The message delivery system is based upon subscriptions and uses filters of various kinds. One kind of filter is an analytics filter, which uses an analytics query definition.
        
    *   In assigning patients to cohorts (dynamic cohorts). Unified Care Record provides the ability to assign patients to cohorts. Such an assignment can be based on an analytics query definition.
        
*   Pre-built solutions like the Consistency Check Tool.
    

For a high-level summary of the available data, see “[Data Available in Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_intro_available_data)” in the Health Insight User Guide.

### [Additional Information on Analytics Query Definitions and Dynamic Cohorts](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_query)

For more information on creating analytics query definitions, see “[Managing Analytics Query Definitions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs)” in the [Health Insight User Guide](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA).

For background information on clinical messages, see the [Unified Care Record Clinical Message Delivery Guide](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEPUSH).

For information on creating query instances, which are used to determine membership in dynamic cohorts, see “[Managing Query Instances](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEADM_ch_query_instance_registry)” in Unified Care Record Registries.

## [Ways to Use Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_usemodes)

There are several ways to use Health Insight:

*   Use the platform, with other tools and components, to build applications. This book assumes that this is the primary use case.
    
*   Use the platform directly for your own data analysis. Customize the data and cubes for your needs.
    
*   Use the data collected by Health Insight to feed other databases.
    
*   Use Health Insight solutions, such as the Consistency Check Tool.
    

## [About Analytics Models](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_deepsee)

Health Insight uses InterSystems IRIS Business Intelligence, an embedded technology that transforms raw data into insights that can improve the operation of a business or other organization. InterSystems IRIS Business Intelligence is intended to support a measurement-based approach to making strategic and tactical decisions. The technology makes it far easier to query your data and to create interactive dashboards that your users can use for their own exploration.

To write queries in SQL, it is necessary to have detailed knowledge of the tables and to be familiar with SQL syntax. The tables might have fields with misleading names, fields that are no longer populated, missing or inconsistent data, and other such issues. And the practice of writing complex SQL queries is considered an expert skill. A programmer is generally required if there is a need to make the query respond to user selections.

In contrast, InterSystems IRIS Business Intelligence provides a useful division of labor, ability, and knowledge, as follows:

*   Developers who are familiar with the SQL tables create an analytics model, which is a set of cubes. A cube provides the elements for use in analytics queries. These elements generally have user-friendly names and documentation. Moreover, the process of creating the cubes provides an opportunity to address data issues, present the data in a more user-friendly manner, and provide higher-level aggregations.
    
*   Analysts use the cubes to create pivot tables. A pivot table is simply a table that displays aggregated data, as in the following example:
    
    [Image: Pivot table showing data for different types of patients in two hospitals in different years]
    
    To create such pivot tables, analysts use the Analyzer, where they can drag and drop cube elements into different areas of a pivot table definition. The Analyzer provides many additional user-friendly options to control the presentation of the data.
    
    Internally, when a user creates a pivot table, InterSystems IRIS Business Intelligence generates an MDX (MultiDimensional eXpressions) query. MDX is a query language used in many BI (business intelligence) applications. It can be helpful to know MDX, but it is possible to create queries of considerable complexity and sophistication without such knowledge.
    
*   Analysts can use the Dashboard Designer to create dashboards for less technical users. A dashboard can easily be configured to include interactive elements such as filters and drill-down options, without the need for a programmer.
    

The [Health Insight User Guide](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA) provides more information.

## [Architecture of Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_arch)

The following figure shows a high-level picture of Health Insight and its users, in relationship to Unified Care Record:

[Image: UCR data ingested into Health Insight SQL tables, built into cubes. SQL Query Tools, dashboards, Analyzer query HI data]

Health Insight runs on an instance of HealthShare (the analytics instance) installed on a server separate from Unified Care Record, and it communicates with Unified Care Record via SOAP messages.

The analytics instance provides two models that your end users can query, as noted earlier. The SQL model is a set of SQL tables that contain a patient-centered representation of the data that is stored in Unified Care Record (stored in Edge Gateways that feed data to the analytics instance through a Feeder Gateway). A later section describes how these tables are populated. You can query these tables via SQL tools, including InterSystems SQL.

The analytics model is a set of cubes. You can query the cubes via the Analyzer and via dashboards that contain pivot tables that were previously created in the Analyzer.

Some additional analytics concepts are fundamental to the architecture of Health Insight:

*   The term cube can refer to either a cube definition (which is a class) or to the data structures that are generated from the definition.
    
*   For a given cube definition, the “data structures” are actually a fact table and a set of dimension tables. (You could query these tables via SQL, but their primary purpose is to enable you to create analytics queries.) For simplicity, these structures are usually referred to as a cube.
    
*   Each cube definition is based on a specific source table. The Health Insight cubes are based on the SQL tables previously mentioned.
    
*   It is necessary to build the cubes, that is, to generate and populate the fact table and dimension tables so that they contain the data needed by the analytics query engine. Also, when cubes are related to each other, they must be built in a specific order. InterSystems IRIS Business Intelligence provides general tools to build the cubes in a cube group in the correct order.
    
*   InterSystems IRIS Business Intelligence also provides general mechanisms to synchronize cubes in a cube group — update them incrementally — in the correct order when new or changed data is available.
    
    If cubes are in use, they are typically built once after the initial data feed. After that, you can configure them to synchronize automatically after subsequent data feeds as part of the batch process.
    

## [Overview of the Health Insight Data Feed Mechanism](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed)

A large, important part of any Health Insight implementation is the process of setting up the data feed mechanism that it uses. This data feed mechanism is similar to the usual Unified Care Record data flow. The following figure shows the process, with the key Unified Care Record components that play roles in this process:

[Image: Edge data goes to the Registry then the Feeder, which sends one aggregated message per patient to Health Insight]

There are three phases to the data feed process. The following subsections provide more details.

> **Note:**
> 
> Feeder Gateway is short for Health Insight Feeder Access Gateway. In previous releases, this gateway was known as the dedicated Access Gateway.

### [Phase 1: New Data Arrives in HealthShare Unified Care Record](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_phase1)

In the first phase of the data feed process, the participants are Edge Gateways and the Registry. Specific kinds of Edge Gateways can feed data to Health Insight, and other kinds cannot; see the [subsection](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_limitations). For the Gateways that can feed data to Health Insight, you can specify a production setting (`Feed Analytics`) that determines whether that Gateway does feed data.

In this phase of the data flow, data arrives at an Edge Gateway from an HL7 feed or other source, and the Gateway notifies the Registry that new or changed data is available. The Registry updates the data feed queue; specifically, this queue lists the patients that have new or changed data, with information on the Edge Gateways where this data can be found.

#### [Edge Gateways That Can Feed Analytics](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_limitations)

This data feed mechanism is supported only for Edge Gateways where the cache type is either “Complete Transactional” or “Notify And Query”, as described in “[Edge Gateway Cache Types](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HESUP_ch_edge#HESUP_edge_config_cache_types)” in [Setting Up Unified Care Record](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HESUP).

If you have XDS.b data, that data can be transmitted to Health Insight only via a Notify and Query Edge Gateway. To convert an existing XDS.b Edge Gateway into a Notify and Query Edge Gateway, follow the steps in “[Converting an Existing Repository to Notify and Query](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSIHE_configuring_repository#HSIHE_configuring_repository_notify_and_query_converting)” in [Setting Up Unified Care Record](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HESUP).

For other types of Edge Gateways (PureQuery, ConsumeAndForward, ExpireAndQuery), the Feeder Access Gateway would not be able to coordinate the incremental changes to a patient’s record as seen by Health Insight. Thus these Edge Gateways cannot feed data to Health Insight.

> **Note:**
> 
> For older systems, it is important to examine the implementation to determine the actual cache type, rather than simply checking the `Cache Type` setting of the production. For example, this setting could equal `CompleteTransactional` even though the actual cache type is custom.

### [Phase 2: Feeder Gateway Sends a Batch of Patients](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_phase2)

In the second phase, activity is controlled by the Health Insight Feeder Access Gateway (or Feeder Gateway), which is a specialized Access Gateway running on a Unified Care Record instance. This Gateway has specialized business hosts that are not present in other Access Gateways. The Feeder Gateway is responsible for all communications between Health Insight and Unified Care Record.

> **Important:**
> 
> Because the Feeder Gateway must handle a large volume of messages, InterSystems recommends using this instance only for use in feeding data to Health Insight.

[Image: Feeder Gateway periodically checks for data and (if needed) sends a batch of messages to Health Insight]

At regular (configurable) intervals, if no batch is currently being sent to Health Insight, the Feeder Gateway sends a request message to the Registry, asking for information about the data feed queue. If the data feed queue is not empty, the Feeder Gateway creates and sends a batch of messages to Health Insight. To create this batch, the Feeder Gateway first sends a message to the Registry, asking it to sort the data feed queue. It then sends subsequent messages to request the MPIIDs of the patients on the data feed queue. By default, the Feeder Gateway requests 10000 MPIIDs per batch. The Feeder Gateway then communicates with the participating Edge Gateways to obtain data, processes the returned data, performs any terminology translation, and applies anonymization and streamlet filtering. Finally, the Feeder Gateway sends one message for each patient in the batch to the Health Insight production.

It is important to note that the data feed queue can contain multiple updates for any given patient. For any given patient in the batch, the Feeder Gateway processes the updates on a first-in, first-out basis, creating a single composite message to send to Health Insight.

A web service in the Health Insight production receives these messages and processes them immediately. There is no interruption to any activities in Health Insight.

#### [How the Registry Sorts the Data Feed Queue](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_phase2_priority)

The data feed queue contains the list of patients to send to the Health Insight Feeder Gateway. The Registry sorts the data feed queue based on priority and last updated timestamp, so that messages with higher priority are sent from the Registry to the Feeder Gateway before messages with lower priority. A priority of 1 is the highest, while a priority of 4 is the lowest. The default priority is 2. Messages with priority 1 will be processed prior to messages of any other priority, regardless of the time at which they arrive in the Registry. Within each priority, messages are processed based on timestamp, from oldest to newest. The timestamp of the message is determined by the time the update reaches the Registry.

Note that the processing of messages by time and priority only affects the order in which updates are sent to the Health Insight Feeder Gateway from the Registry. Sending a batch of high priority messages through the system will get this batch of messages to the Feeder Gateway sooner than low priority messages on the Registry. Since there is a queue of data on the Feeder Gateway as well as on Health Insight, this high priority message will still be processed after the other message from previous batches that are already queued up on the Feeder Gateway and in Health Insight.

Within a batch of messages on the Feeder Gateway, there is no guarantee that high priority messages will be processed before messages with lower priority, as messages on the Feeder Gateway message queue and the Health Insight production are processed in parallel. For example, if the Feeder Gateway requested a batch of size 10 from the Registry, and these messages had varying priorities from 1–4, these messages would be sent to the Feeder Gateway production in the same batch. Upon arriving at the Feeder Gateway message queue, a message with priority 4 could be processed by the Feeder Gateway before a message with priority 1, because these messages are being processed in parallel. The same applies to messages arriving in the Health Insight production.

Alternatively, if there were 100 messages with priority 1 on the Registry and 1000 patients with priority 2, setting the Feeder Gateway batch size to 100 would cause the 100 patients with priority 1 to be sent to the Feeder Gateway and Health Insight first. Only after the Feeder Gateway finished processing the first batch of 100 patients would it request more MPIIDs from the Registry. At that point, the Feeder Gateway would start requesting the patients with priority 2.

The following table summarizes the priorities used for data in Health Insight that comes from Unified Care Record:

<table><tr><th>Event/Action</th><th>Default Priority</th><th>Can Priority be Modified?</th></tr><tr><td>Data flows into Unified Care Record via regular activity from edge gateways (HL7, CCDs, etc)</td><td>2</td><td>No</td></tr><tr><td>The <code>Feed Analytics</code> setting on an edge gateway is changed generating a bulk load (or unload)</td><td>3</td><td>No</td></tr><tr><td><code>RequeueAllPatientsInErrorListAndClear</code> and <code>RequeuePatientsInErrorListAndClear</code> API methods</td><td>4</td><td>Yes</td></tr><tr><td><code>RequeueForAnalytics</code> API method</td><td>2</td><td>Yes</td></tr></table>

### [Phase 3: Health Insight Production Processes the Data in the Message Table](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_phase3)

In the third phase of the data feed process, the Health Insight production processes the data in the Health Insight message queue, writes it to the source tables used by the Health Insight cubes, and then synchronizes the cubes.

[Image: Health Insight production constantly processes data from message table, until interrupted by an analytics batch]

Health Insight is constantly ingesting data from the message queue and storing it in source tables. Periodically, an analytics batch will interrupt the ingestion process to perform processing steps, run queries associated with dynamic cohorts or advanced clinical notifications, and synchronize cubes.

The Health Insight analytics batch works as follows:

1.  At regular (configurable) intervals, the Health Insight interrupt business service checks to see if the previous analytics batch is still running. If the previous batch is not running, the interrupt business service will interrupt the ingestion process and start a new analytics batch.
    
2.  The batch process stops all transfer operations.
    
3.  The batch process performs post-transfer processing.
    
4.  The batch process synchronizes the Health Insight cubes (so that they show the most recent data).
    
5.  The batch process performs post-sync processing.
    
6.  The batch process performs post-batch processing.
    
7.  The batch process sends queries to the query process and waits for the completion of any queries used by Advanced Clinical Notifications (ACN). Analytics queries are only sent if you have not configured them to [run outside the batch](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch).
    
8.  The batch process updates the report cubes.
    
9.  The batch process re-enables transfer operations.
    

You can add custom processing at specific points within this flow; see the options in “[Specifying Additional Settings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional)” in the chapter “[Customizing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube).”

#### [Halting Ingestion Processes in Parallel](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_phase3_stop)

If you are experiencing long delays when the batch process tries to begin because the system is taking a long time to halt ingestion, you can use the `SetForceKillGlb()` method of the [HSAA.API.Transmit](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.API.Transmit) class to force all ingestion processes to stop in parallel. To do so, open the Terminal and navigate to your Health Insight namespace. Make a call such as the following:

```objectscript
 set sc = ##class(HSAA.API.Transmit).SetForceKillGlb(1,2)
```

In the above call, the first argument of the method determines whether or not the system should concurrently halt all [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer) jobs that are ingesting messages into Health Insight. The second argument determines how long the system will wait (in seconds) before halting these jobs. In the above example, when the batch process begins and the system attempts to halt ingestion, the system will stop all [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer) jobs that are processing messages after waiting for 2 seconds.

Running this method (with a first argument of `1`) configures the system to end ingestion after the specified time period when the batch process begins. Doing so ensures that batch tasks and queries can start in a timely fashion. If you configure your system to pause ingestion in this way, there may be incomplete data in your source tables and cubes during the batch, and also before the ingestion process has had a chance to continue. After the [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer) business host restarts and ingestion resumes, data will be ingested as normal. Any messages that were being processed by the jobs when they were stopped remain in the queue of [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer) and are ingested normally when ingestion resumes.

You can use the `GetForceKillGlb()` method of the HSAA.API.Transmit class to display the system’s settings for the `SetForceKillGlb()` method. For example, execute the following commands in the Terminal after you call `SetForceKillGlb()`:

```objectscript
  do ##class(HSAA.API.Transmit).GetForceKillGlb(.pForceKill,.pStopTimeout)
  w "ForceKill: "_pForceKill_", "_ "Stop Timeout: "_pStopTimeout
```

If you called `SetForceKillGlb()` with the arguments `1` and `2`, you would see those values printed in the Terminal.

A `pForceKill` value of 0 indicates that the system is not currently configured to forcefully stop message ingestion jobs concurrently at the beginning of the batch process. In this case, `pStopTimeout` will have a value of -1, indicating that the `pStopTimeout` value is not applicable. This means that the system will end ingestion jobs in the default way — serially, rather than in parallel. In this case, the system will wait up to `n` seconds for each job to end, where `n` is determined by the `Update Timeout` setting in the `Production Settings` of your Health Insight production.

### [Additional Notes on the Data Feed Mechanism](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_notes)

The data feed mechanism described here automatically handles incremental updates to data, so that the Health Insight database is in sync with the data that is available to Unified Care Record. When Unified Care Record receives new or changed data for a given patient, the Feeder Gateway sends appropriate messages that adjust the data accordingly in the Health Insight database. Similarly, when data is removed in Unified Care Record, the Feeder Gateway sends a message to remove the corresponding Health Insight data.

It is not necessary to know the details of the synchronization mechanism. However, it is useful to know how patients are identified in the different components. Within Unified Care Record, a patient is identified by a Master Person Index ID (MPIID), which can be connected to the identifiers for that patient in the participating facilities and thus can be connected to the actual patient. Every patient has a unique analytics identifier. Even if you elect not to send the MPIID to Health Insight, Unified Care Record has a mapping of the MPIID to the analytics identifier.

If two patients are determined to be the same person, a merge will occur in Unified Care Record. If one patient has MPIID A and the other has MPIID B, only MPIID A will remain in Health Insight after a merge. When two patients are merged in Unified Care Record, records for both MPIID A and MPIID B are marked for resend to Health Insight. When MPIID B is resent, the record is empty. When MPIID A is sent, it contains the fully merged record. Any time a full resend of a patient's record is made to Health Insight, the entire patient record is deleted, and the record contained in the message is inserted into Health Insight. In the case of a merge, MPIID B is deleted in Health Insight and there is no new data to insert. Next, MPIID A is deleted, and the fully merged record is inserted into the database. This results in a single record for the patient under MPIID A.

## [Health Insight Home Page and Other Tools](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page)

To access the home page for Health Insight:

1.  Open the Management Portal on the analytics instance.
    
2.  Select `HealthShare`.
    
3.  Select the name of the Analytics namespace, usually `HSANALYTICS`.
    

This page provides the following menu options:

<table><tr><th>Option</th><th>Intended Users</th><th>Discussion</th></tr><tr><td><code>User Portal</code></td><td rowspan="3">Analysts, Modelers</td><td rowspan="3">See the <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA">Health Insight User Guide</a>.</td></tr><tr><td><code>Model Browser</code></td></tr><tr><td><code>Health Insight Analyzer</code></td></tr><tr><td><code>SQL Explorer</code></td><td>Administrators, Analysts, Modelers</td><td><p>Use SQL to query the Health Insight source tables (and other tables).</p><p>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_smp">Using the Management Portal SQL Interface</a>.</p></td></tr><tr><td><code>Query Definition Registry</code></td><td>Analysts, Modelers</td><td><p>Create query definitions for use in Clinical Alerts.</p><p>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs">Creating Analytics Query Definitions</a>.</p></td></tr><tr><td><code>Cube Management</code></td><td>Analysts, Modelers</td><td><p>Managing the Health Insight cubes.</p><p>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube">Customizing Health Insight</a>. Also see <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent">Keeping the Cubes Current</a>.</p></td></tr><tr><td><code>Customization</code></td><td>Implementers, Modelers</td><td><p>Customize Health Insight.</p><p>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube">Customizing Health Insight</a>.</p></td></tr><tr><td><code>Internal Data Management</code></td><td>Implementers, Administrators</td><td>Options to purge data when it is no longer needed.See the <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM">Health Insight Administration Guide</a>.</td></tr><tr><td><code>Platform Information</code></td><td>Implementers, Administrators</td><td>Dashboards that provide high-level system information.See the <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM">Health Insight Administration Guide</a>.</td></tr></table>

Implementers and administrators also use Production management pages, which are accessible via a link at the top of the page. For general information, see [Managing Unified Care Record Productions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEENS).

Implementers also use Terminal and a supported IDE; see [Using the Terminal](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GTER) and [IDEs](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides).

## [For Additional Information on Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_seealso)

At [learning.intersystems.com](https://learning.intersystems.com/), you can find the following online courses for Health Insight:

*   Health Insight Overview ([https://learning.intersystems.com/course/view.php?name=Health%20Insight%20Overview](https://learning.intersystems.com/course/view.php?name=Health%20Insight%20Overview))
    
*   Health Insight Data Flow ([https://learning.intersystems.com/course/view.php?name=Health%20Insight%20Data%20Flow](https://learning.intersystems.com/course/view.php?name=Health%20Insight%20Data%20Flow))
