# [Setting Up and Using Persistent Requests](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

This chapter describes how to set up and use the persistent request feature, which enables you to reload data during development (without retransmitting it), to set up a testing environment that uses real data, and to support reporting. It discusses the following topics:

*   [Overview of persistent requests](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_overview)
    
*   [How to configure a Health Insight instance to store persistent requests](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_store)
    
*   [How to configure a Health Insight instance to read in persistent requests](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_readconfig)
    
*   [How to retransmit persisted data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_read)
    
*   [Notes on managing the cache of persisted data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_mng)
    

> **Important:**
> 
> The persistent requests feature is supported in a mirrored environment only if the persistent requests are stored in a database. In both the primary and backup servers, the HealthShare Health Insight production must be configured in the same way.

## [Overview of Persistent Requests](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_overview)

Persistent requests allows you to maintain a record of all data transferred from HealthShare Unified Care Record to Health Insight. This record is saved as messages from the Feeder Gateway that sent them. The saved messages are known as the persistent cache of messages. You can later use the persistent requests for either or both of the following purposes:

*   To reload previously received data without retransmitting it from Unified Care Record — While developing or testing your system, it is sometimes necessary to clear out the data from Health Insight. Normally, reloading data into Health Insight requires you to resend the complete record of all patients from Unified Care Record; this can be a resource-intensive operation. With persistent requests, you can instead reload stored data from the persistent cache of messages.
    
*   To support additional Health Insight instances for testing, reporting, or other purposes — Within Unified Care Record, the Feeder Gateway can send data to only one Health Insight instance, called the primary instance. Via the persistent request mechanism, the primary instance can update another Health Insight instance, a secondary instance. In fact, you can set up multiple secondary instances. For simplicity, this chapter focuses on scenarios with a single secondary instance.
    
    The primary instance can support operational needs (such as dynamic cohorts or advanced clinical notifications) — use this instance for any activity that requires the most current data. You can use the secondary instance (or instances) for a variety of purposes:
    
    *   As a testing area. For example, you can test new dashboards, or test the effects of a setting change or of an upgrade before roll-out.
        
    *   For reporting or ad hoc queries.
        
    *   To enable you to analyze a subset of the data or to present the data in a different way than in the primary instance. For example, within a secondary instance, you could perform a detailed analysis just of medications; for this, it would not be necessary to populate all cubes.
        
    
    Furthermore, if you are using Health Insight for operational needs and for purposes that do not require the most current data, then the recommended architecture is to use the primary Health Insight instance as your operational instance and the secondary instance for all other purposes; this reduces the load on the primary instance.
    
    Always remember that the data in any secondary instance is less closely coupled to the real-time systems because of the latency. Any use of the secondary instances must take that factor into account.
    

The following figure shows the overall flow of data:

[Image: Messages go from Feeder to persistent request table in Health Insight instance. Secondary instance reads messages/stores data]

The persistent cache of messages can be stored either in files or in an SQL table in a JDBC-compliant database. In the previous figure, the cache is stored in a table within the secondary Health Insight instance.

It is less complex to configure Health Insight to store the cache as files, but with this configuration, it is necessary for you to separately manage the disk space used to store the files. The database storage method is slightly more complex to set up, but the database manages the storage.

Note that only JDBC is supported for persistent requests stored in tables; that is, ODBC connections are not supported.

## [Configuring Health Insight to Store Persistent Requests](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_store)

You must configure the primary analytics instance to store persistent request messages as either files or in a SQL table. The primary instance is the instance that receives live updates from the Feeder Gateway.

*   [How to store persistent request messages as files](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_store_file)
    
*   [How to store persistent request messages in an SQL table](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_store_table)
    

> **Important:**
> 
> The file method is useful during development and testing; it enables you to replay the entire record for a patient simply by copying a directory to the correct location. However, for a live system, InterSystems recommends that you use the database storage method, for several reasons:
> 
> *   The file method can create a huge number of files that can overwhelm the operating system unless they are properly managed.
>     
> *   The database storage method greatly simplifies backup because there are no external files to consider.
>     
> *   The database storage method gives flexibility in terms of storing in another database.
>     
> *   With the database storage method, there is no extra work to manage the disk space that is used by the persistent requests.
>     
> *   The persistent requests feature is supported in a mirrored environment only if the persistent requests are stored in a database.
>     

### [Storing Persistent Request Messages As Files](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_store_file)

To store persistent request messages as files, on the production configuration page in the analytics production on your primary analytics instance, make the following changes:

1.  In the [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer) business process, select the `ToFile` check box under `Additional Settings`.
    
2.  In the [HSAA.TransferSDA3.Operation.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.FilePR) business operation:
    
    *   Check the `Enabled` box under `Basic Settings`.
        
    *   In the `BaseFilePath` field under `Additional Settings`, enter the absolute path to which you want the files saved. The files are saved in subdirectories of this directory, organized by analytics ID. For details, see “[Organization of Persisted Files](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_fileorg),” below.
        

### [Storing Persistent Request Messages in an SQL Table](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_store_table)

To configure Health Insight to store persistent request message in an SQL database, perform the following steps:

*   [Create the SQL table](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_sql_table_setup)
    
*   [Set up the JDBC connection](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_jdbc)
    
*   [Configure the transfer process](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_sql_router)
    

If you are storing persistent request messages in an SQL database, you should in most cases set the `Failure Timeout` setting of the [HSAA.TransferSDA3.Operation.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.SQLPR) business operation to a value of `-1`.

#### [Creating the SQL Table for Persistent Requests](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_sql_table_setup)

You can store persistent request messages in an SQL table on any JDBC-compliant database. For example:

*   In a dedicated namespace in the secondary Health Insight instance. This is the recommended approach.
    
*   In a different HealthShare or InterSystems IRIS data platform instance (on the same or a different server)
    
*   In a non-InterSystems IRIS database that supports JDBC
    

Create the SQL table using the details given in the table below. If you use an InterSystems IRIS database, create a persistent class with the property definitions described in the column “Corresponding InterSystems IRIS Property Definition.”

<table><tr><th>Field Name</th><th>SQL Data Type</th><th>Corresponding InterSystems IRIS Property Definition</th></tr><tr><td>ID</td><td>Integer AUTO INCREMENT</td><td>**Not needed in InterSystems IRIS class</td></tr><tr><td>AnalyticsID</td><td>VARCHAR(50)</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25Library.String">%String</a></td></tr><tr><td>Resend</td><td>BIT</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25Library.Boolean">%Boolean</a></td></tr><tr><td>ContentStream</td><td>CLOB</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25Stream.GlobalCharacter">%Stream.GlobalCharacter</a></td></tr><tr><td>Action</td><td>VARCHAR(50)</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25Library.String">%String</a></td></tr><tr><td>HSCoreVersion</td><td>VARCHAR(50)</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25Library.String">%String</a></td></tr><tr><td>HSMinVersion</td><td>VARCHAR(50)</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25Library.String">%String</a></td></tr><tr><td>MRNs</td><td>VARCHAR</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25Library.String">%String</a> (also specify <code>MAXLEN=""</code>) in the property definition</td></tr></table>

If you wish to include a timestamp column in your table, include the following fields in your table:

<table><tr><th>Field Name</th><th>SQL Data Type</th><th>Corresponding InterSystems IRIS Property Definition</th></tr><tr><td>Priority</td><td>INTEGER</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25Library.Integer">%Integer</a></td></tr><tr><td>UpdateTime</td><td>TIMESTAMP</td><td><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25Library.TimeStamp">%TimeStamp</a></td></tr></table>

#### [Setting Up the JDBC Connection to Store Persistent Requests in a Database](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_jdbc)

To configure your primary Health Insight instance to connect to your SQL database via JDBC for write access, perform the following configuration steps on your primary Health Insight instance:

1.  Ensure that you have the most recent version of Java supported by your Health Insight instance. See “[Supported Java Technologies](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ISP_technologies#ISP_ejb)” in the [Supported Platforms](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ISP) book for information.
    
2.  [Define a set of interoperability credentials](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ECONFIG_reusable#ECONFIG_reusable_credentials) that contain the username and password needed to log in to the database.
    
3.  On the production configuration page in the analytics production, configure the [EnsLib.JavaGateway.Service](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&CLASSNAME=EnsLib.JavaGateway.Service):
    
    *   Ensure that the service is enabled.
        
    *   Set `JavaHome` equal to the full path to the directory that contains the Java executable file.
        
4.  On the production configuration page in the analytics production, configure the [HSAA.TransferSDA3.Operation.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.SQLPR) business operation so that it uses JDBC to connect to your persistent request database:
    
    1.  Make sure the business operation is enabled.
        
    2.  Set `DSN` to the connection URL of the persistent request database.
        
        For example, for an InterSystems IRIS database, the URL would have the form [<baseURL>](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GCGI_intro#GCGI_intro_howitworks_url)`/namespace` where `namespace` is the namespace where you set up your SQL table.
        
    3.  Set the `Credentials` field equal to the name of the interoperability credentials you created above.
        
    4.  Set `JDBCDriver` to the name of the JDBC driver that you will use to connect to the database.
        
        For example, if you are using an InterSystems IRIS database, set `JDBCDriver` to `com.intersystems.jdbc.IRISDriver`.
        
    5.  Set `JDBC Class Path` to the location of the applicable JDBC driver jar file.
        
        For example, for an InterSystems IRIS database, use `install directory\dev\java\lib\JDK18\intersystems-jdbc-3.1.0.jar` where `install directory` is the location where the Health Insight instance is installed.
        
    6.  Set `JGService` to `EnsLib.JavaGateway.Service.`
        
    7.  In the `SQLString` setting, replace the string `HSAA_Test.AnalyticsUpdateRequest` in the INSERT statement with your database table name. The SQL string should look like:
        
        ```sql
        INSERT INTO yourtablenamehere
        (Action, AnalyticsID, ContentStream, HSCoreVersion, HSMinVersion, Resend, MRNs)
        VALUES(?, ?, ?, ?, ?, ?, ?)
        ```
        
    8.  If you want to include a timestamp column in your persistent requests table, modify the `SQLString` setting:
        
        ```sql
        INSERT INTO yourtablenamehere
        (Action, AnalyticsID, ContentStream, HSCoreVersion, HSMinVersion, Resend, MRNs, Priority, UpdateTime)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        ```
        
        Note that you must follow the order of fields listed in this example. If you choose to include the timestamp column, you will need to modify your persistent requests table accordingly. See [Creating the SQL Table for Persistent Requests](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_sql_table_setup).
        

#### [Configuring the Transfer Process for SQL Storage of Persistent Requests](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_sql_router)

To configure your primary Health Insight instance to store persistent request messages in a SQL table, on the production configuration page in the analytics production, configure the [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer) as follows:

1.  Ensure that the business process is enabled.
    
2.  Select the `ToSQL` check box under `Additional Settings`.
    
3.  Set `SQLTarget` to [HSAA.TransferSDA3.Operation.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.SQLPR).
    

#### [Storing Persistent Request Messages to Multiple SQL Tables](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_multiple)

To configure your primary Health Insight instance to store persistent request messages to multiple SQL tables, make the following changes:

1.  In the [HSAA.TransferSDA3.Operation.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.SQLPR) business operation, click the `Actions` tab in the `Production Settings` area.
    
2.  Click `Copy` and enter a name for the copy. Click `OK`.
    
3.  In the [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer) business process, click the dropdown arrow next to the `SQLTarget` setting. The dropdown will display a list of business hosts.
    
4.  Select your new business operation as a target while keeping the existing `HSAA.TransferSDA3.Operation.SQLPR` selection.
    
5.  Modify the `SQLString` setting of your new business operation to point to a database table name of your choice.
    
6.  Upon inbound Health Insight traffic, persistent request messages will be generated and sent to each of the business operations specified by `SQLTarget`. You may repeat these steps to create additional endpoints.
    

## [Configuring Health Insight to Read In Persistent Requests](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_readconfig)

This section describes how to configure either a secondary Health Insight instance or the primary Health Insight instance to read in persistent requests.

> **Warning:**
> 
> Except in early stages of development, when you may want to start over by retransmitting data from Unified Care Record, you should not configure the primary Health Insight instance to read in persistent requests. Doing so risks mixing persistent requests with live updates, which can lead to data corruption, because Health Insight expects to receive messages in FIFO order.

The steps are different depending on whether the persistent request messages are stored as files or in a table. Note that the [HSAA.TransferSDA3.Service.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.SQLPR) will run as soon as it is enabled. Depending on the number of persistent requests, there may be a large queue for [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer).

*   [How to read in persistent request messages stored as files](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_readconfig_file)
    
*   [How to read in persistent request messages stored in an SQL table](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_readconfig_table)
    

### [Configuring Health Insight to Read In Persistent Requests Stored as Files](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_readconfig_file)

To configure a Health Insight instance to read persistent requests that are stored as files, on the production configuration page in the analytics production, configure the [HSAA.TransferSDA3.Service.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.FilePR) business service as follows:

1.  Check the `Enabled` box under `Basic Settings`.
    
2.  Set `BaseFilePath` under `Additional Settings` to the absolute path from which the files will be consumed.
    

> **Warning:**
> 
> Persistent request files are destroyed upon consumption. Therefore, be sure that the `BaseFilePath` property in the [HSAA.TransferSDA3.Service.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.FilePR) business service is different from the `BaseFilePath` property in the [HSAA.TransferSDA3.Operation.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.FilePR) business operation. This allows you to consume each persistent request more than once. If `BaseFilePath` is empty or invalid for either component, the system uses the default, which is `installation-directory\mgr\tmp`.

### [Configuring Health Insight to Read In Persistent Requests Stored in a Table](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_readconfig_table)

To configure a Health Insight instance to connect to your SQL database via JDBC for read access, perform the following configuration steps on the appropriate Health Insight instance:

1.  Ensure that you have the most recent version of Java supported by your Health Insight instance. See “[Supported Java Technologies](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ISP_technologies#ISP_ejb)” in the [Supported Platforms](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ISP) book for information.
    
2.  [Define a set of interoperability credentials](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ECONFIG_reusable#ECONFIG_reusable_credentials) that contain the username and password needed to log in to the database.
    
3.  In the analytics production, configure the [EnsLib.JavaGateway.Service](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&CLASSNAME=EnsLib.JavaGateway.Service):
    
    *   Ensure that the service is enabled.
        
    *   Set `JavaHome` equal to the full path to the directory that contains the Java executable file.
        
4.  On the production configuration page in the analytics production, configure the [HSAA.TransferSDA3.Service.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.SQLPR) business service so that it uses JDBC to connect to your persistent request database:
    
    1.  Set `DSN` to the connection URL of the persistent request database.
        
        For example, for an InterSystems IRIS database, the URL would have the form [<baseURL>](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GCGI_intro#GCGI_intro_howitworks_url)`/namespace`, where `namespace` is the namespace where you set up your SQL table.
        
    2.  Set the `Credentials` field equal to the name of the interoperability credentials you created above.
        
    3.  Set `JDBCDriver` to the name of the JDBC driver that you will use to connect to the database.
        
        For example, if you are using an InterSystems IRIS database, set `JDBCDriver` to `com.intersystems.jdbc.IRISDriver`.
        
    4.  Set `JDBC Class Path` to the location of the applicable JDBC driver jar file.
        
        For example, for an InterSystems IRIS database, use `install directory\dev\java\lib\JDK18\intersystems-jdbc-3.1.0.jar` where `install directory` is the location where the Health Insight instance is installed.
        
    5.  Set `JGService` to `EnsLib.JavaGateway.Service.`
        
    6.  In the `Query` property, replace the string `HSAA_Test.AnalyticsUpdateRequest` in the FROM clause of the SELECT statement with your database table name. The query should look like:
        
        ```sql
        SELECT %ID AS ID, Action AS Action, AnalyticsID AS AnalyticsID, ContentStream AS ContentStream,
        HSCoreVersion AS HSCoreVersion, HSMinVersion AS HSMinVersion, Resend AS Resend,
        MRNs As MRNs
        FROM yourtablenamehere ORDER BY %ID
        ```
        

## [Using Persistent Requests to Retransmit Data](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_read)

This section describes how to cause an analytics instance to read in persistent request messages from the persistent cache and load the data contained in them. The steps are different depending on whether the persistent requests are stored as files or in a table.

*   [How to read in persistent requests stored as files](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_read_file)
    
*   [How to read in persistent requests stored in an SQL table](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_read_table)
    

### [Reading in Persistent Requests Stored as Files](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_read_file)

Persistent request files are destroyed once they are consumed, so you should have followed the recommendation to set the `BaseFilePath` setting (in [HSAA.TransferSDA3.Operation.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.FilePR)) to a different location than the `BaseFilePath` property in the [HSAA.TransferSDA3.Service.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.FilePR) business service that will read in the persistent requests, as described in the sections above. Note that if `BaseFilePath` is empty or invalid for either component, Health Insight uses the default location, which is `installation-directory\mgr\tmp`.

Before reading in the persistent request messages, copy the messages you wish to read in from the first location to the second location. This allows you to consume each persistent request more than once, for example if you need to start over again, or set up a secondary analytics system with a full set of messages. The structure of the directories that store persistent request messages is described in the next section.

#### [Organization of Persisted Files](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_fileorg)

When you store the messages as files, the files are grouped into directories, with one directory per patient. The file names have the form `BaseFilePath\AnalyticsID\AnalyticsRequest_sequenceNumber.xml`. where:

*   `BaseFilePath` is the directory specified in the `BaseFilePath` setting of the [HSAA.TransferSDA3.Operation.FilePR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.FilePR) business operation of the analytics production.
    
*   `AnalyticsID` is the unique anonymized patient identifier provided by Unified Care Record. See “[Overview of the Data Feed Mechanism](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed).”
    
*   `sequenceNumber` begins at 000 and is incremented for each record.
    

#### [Initiating Persistent Request Consumption](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_consume_files)

To initiate the consumption of persistent request messages stored as files, complete the following steps:

1.  Navigate to the task scheduler on the appropriate instance. To do so, select `System Operation` > `Task Manager` > `Task Schedule`.
    
2.  Select the `Consume Persistent Requests` task.
    
3.  Select `Edit`, and ensure that the `Source` is set to `File`.
    
4.  Select `Finish`.
    
5.  Select the `Run` button on the `Consume Persistent Requests` row in the task scheduler.
    

Alternatively, you can start the process programmatically. To do so, run the following terminal commands in the `HSANALYTICS` namespace:

```objectscript
 set status=##class(HSAA.API.Utils).ProcessPRFromFile()
 write status
```

If `status` equals 1, the command was successful. If not, enter the following command to learn more:

```objectscript
 do $system.OBJ.DisplayError()
```

### [Reading in Persistent Requests Stored in an SQL Table](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_read_table)

To read in data from the persistent requests table, complete the following steps:

1.  Navigate to the task scheduler. To do so, select `System Operation` > `Task Manager` > `Task Schedule`.
    
2.  Select the `Consume Persistent Requests` task.
    
3.  Select `Edit` and change `Type` to `SQL`.
    
4.  Select `Finish`.
    
5.  Select the `Run` button on the `Consume Persistent Requests` row in the task scheduler.
    

Alternatively, you can start the process programmatically. To do so, run the following terminal commands in the `HSANALYTICS` namespace:

```objectscript
 set status=##class(HSAA.API.Utils).ProcessPRFromTable()
 write status
```

If `status` equals 1, the command was successful. If not, enter the following command to learn more:

```objectscript
 do $system.OBJ.DisplayError()
```

You can also start the process by enabling [HSAA.TransferSDA3.Service.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.SQLPR). This business service starts automatically when the `Enabled` setting is selected.

To consume only a portion of the persistent requests, modify the WHERE clause in the `Query` property of the [HSAA.TransferSDA3.Service.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.SQLPR) business service to select only the appropriate records, or construct a new table that contains only the appropriate records, and read in from that table by modifying the FROM clause of the SELECT statement in the `Query` property of the [HSAA.TransferSDA3.Service.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.SQLPR) business service.

## [Notes on Managing the Persistent Request Cache](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_mng)

Whether you store the cache of persistent requests in a table or as files, it will be necessary to manage this cache, because it grows over time:

*   If the cache is stored in a table, the database manages the disk space, and the cache is backed up as part of the database. It is still necessary, however, to plan appropriately for the needed space. For example, if you want a cache of all messages ever sent into Health Insight, this table will continue to grow. If, on the other hand, if you need only a subset of messages for testing, you can trim the table.
    
*   If the cache is stored as files, in addition to planning for the overall space needs, it is also necessary to separately manage the disk space used by the files.
    
*   You can use the `Delete Query` setting of [HSAA.TransferSDA3.Service.SQLPR](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.SQLPR) to purge persistent requests stored in a table. Use a query such as the following:
    
    ```
    DELETE FROM yourtablenamehere WHERE ID=?
    ```
    
    Where `yourtablenamehere` is the name of your persistent request table. For more information on the `Delete Query` setting, see [Using the SQL Inbound Adapter](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ESQL_inbound).
