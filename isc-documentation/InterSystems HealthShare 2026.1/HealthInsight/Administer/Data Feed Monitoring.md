# [Monitoring the Health Insight Data Feed](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq).

It is important to monitor the data feed that sends data from HealthShare Unified Care Record to HealthShare Health Insight and to correct any problems early, before you have purged production messages.

*   To fix errors that occur in the Health Insight production, see [Troubleshooting Data Feed Problems.](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob)
    
*   For an overview of the data feed, see [Overview of the Data Feed Mechanism](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed).
    
*   For detailed information on the data feed, see [Data Feed Details](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_details).
    

> **Note:**
> 
> Feeder Gateway is short for Health Insight Feeder Access Gateway. In previous releases, this gateway was known as the dedicated Access Gateway.

## [Monitoring the Event Logs in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor_evtlog)

You should monitor the Feeder Gateway and the Health Insight productions in the same way that you monitor other productions that are part of Unified Care Record.

> **Important:**
> 
> In particular, it is important to check the event log regularly and correct any problems as soon as you can. If you notice a problem and correct it early, you can use the portal option to resend the relevant messages. If you do not notice the problem until after you have purged the production messages, you will need to resend the messages from the source systems, which is more difficult.

To see the event log, do either of the following in the Management Portal, on the applicable instance:

*   Select `Interoperability`, select the name of the namespace in which the production is running, and then select `View` > `Event Log`. This page displays just the event log.
    
*   Select `Interoperability`, select the name of the namespace in which the production is running, and then select `Monitor` > `Production Monitor`. This page displays the event log, as well as other information on the activity of the production.
    

For general information on monitoring and managing productions, see [Managing Unified Care Record Productions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEENS).

## [Monitoring Feeder Patient Errors](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor_feeders)

You should monitor the feeder patient error global, `^HS.Feeder.PatientErrors`, in the Feeder namespace. When data retrieval from the Edge errors out for a patient, the Feeder records that patient in this global and blocks later updates for that patient until the patient is marked fixed. 

Administrators should review this global regularly, for example weekly, and whenever expected patient data is missing from Health Insight.

Entries in `^HS.Feeder.PatientErrors` persist until they are explicitly cleared. They are not removed by purging interoperability data or by resetting the production. 

After the underlying problem is corrected, the patient must be marked fixed before data for that patient can be sent or resent to Health Insight. For details, see the [troubleshooting topic on feeder patient errors](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob#HSAAADM_prob_feederpatientblocked).

## [Monitoring the Health Insight Log](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor_xferlog)

During the data feed process, Health Insight writes any streamlet processing errors to its log, which is the table `HSAA_Report.Log`. You can query this table with any SQL tool via xDBC. To query this table from the Management Portal on the analytics instance, do the following:

1.  Access the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_intro#HSAAADM_home_page).
    
2.  Click `SQL Explorer`.
    
    Note that you can find the same page without going to the Health Insight home page. To do so, click `System Explorer` > `SQL`.
    
3.  Optionally enter `HSAA_Report` into `Filter`.
    
    Because there are many tables in the analytics namespace, this step makes it easier to find the table.
    
4.  Expand the `Tables` folder.
    
    This displays a list of the tables in the `HSAA_Report` schema. If you select the triangle by a table name, the system displays the names of the fields in that table.
    
5.  On the right side, click the `Execute Query` tab.
    
6.  Drag and drop a table name from the left area into the large box on the `Execute Query` tab. The primary table is `HSAA_Report.Log`; see the following subsection for details.
    
    Or directly type an SQL query into the box and press `Execute`.
    
    For information on the SQL Explorer, see “[Using the Management Portal SQL Interface](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_smp)” in Using InterSystems SQL.
    
7.  If you see errors, make a note of the associated `SessionID` field. You can use this in the production message page, to find the activity that occurred near the error.
    
    For details on using the production message search page, see [Managing Unified Care Record Productions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEENS).
    

You should have configured logging when you performed [Step 7: Configure the Health Insight Production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_config) of the [Configuration Procedure for a New Health Insight Instance](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi).

For information on purging older records in this log, see “[Purging Management Data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_purgedata).”

### [Table Details](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor_xferlog_details)

The table `HSAA_Report.Log` contains the following fields:

<table><tr><th>Field</th><th>Indexed?</th><th>Notes</th></tr><tr><td>ID</td><td>Yes</td><td>Row ID</td></tr><tr><td>AnalyticsID</td><td>Yes</td><td>Health Insight analytics ID (HSAAID)</td></tr><tr><td>LogLevel</td><td>Yes</td><td>&nbsp;</td></tr><tr><td>LogTime</td><td>Yes</td><td>&nbsp;</td></tr><tr><td>Message</td><td>No</td><td>Error or informational message</td></tr><tr><td>SessionID</td><td>Yes</td><td>session ID</td></tr><tr><td>StackTrace</td><td>No</td><td>Line of code where the error occurred</td></tr></table>

## [Using the Health Insight Platform Information Dashboards](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor_dashboards)

Health Insight also provides a set of dashboards that display information about current and past performance of the data feeds, as well as other useful information. To access these dashboards:

1.  Access the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_intro#HSAAADM_home_page).
    
2.  Click `Platform Information`.
    

Then select a dashboard from the drop-down list on the left. The following subsection describes the available dashboards.

### [Current System Status](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor_dashboards_current_system_status)

Use this dashboard to find out:

*   The state of the Health Insight production. Normally, the production should be running.
    
*   The state of the analytics batch processing.
    
*   Schema tuning information.
    
*   Auditing status.
    
*   Details about the analytics production. The settings listed are relevant to the data feed process. For information on the settings, see [Step 7: Configure the Health Insight Production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_config) in the [Configuration Procedure for a New Health Insight Instance](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi).
    

This dashboard refreshes every five minutes.

### [End to End Monitor](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor_dashboards_end_to_end)

Use this dashboard to see information regarding the status of the entire Health Insight data flow. This page shows information about the processing of messages on Health Insight, and also the number and kinds of messages queued up on the Health Insight Feeder Gateway and on the Registry. This page also shows the count of messages by [priority](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_phase2_priority) and timestamp for data queued up in the Registry.

This dashboard refreshes every two minutes.

### [Transfer Performance Over Time](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor_dashboards_batch_perf)

Use this dashboard to see how much data is being processed by Health Insight. The upper chart displays (as separate series) the number of updates and resends, as well as the total count of messages and the total error count. The lower chart displays (as separate series) the size of updates and resends in bytes, as well as the total size of all messages.

Use the buttons on the charts to control the horizontal axis.

*   If you click `Last 24 Active Hours`, the horizontal axis displays timestamps and dates during the past 24 hours when the system was actively ingesting data. Hours during which the system was idling are not included.
    
*   If you click `Last 30 Days`, the horizontal axis displays dates during the past 30 days.
    
*   If you click `Last 12 Months`, the horizontal axis displays months during the past 12 months.
    

### [Batch Activity Over Time](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor_dashboards_batch_activity)

Use this dashboard for more information on what occurred during various parts of any given analytics batch. This chart displays how much time was spent on average in each step of the analytics batch.

Use the buttons on the chart to control the horizontal axis.

*   If you click `View By Date`, the horizontal axis displays the dates of the batches. In this case, the chart also shows data summarized for each day.
    
*   If you click `View By Batch Session ID`, the horizontal axis displays the session IDs of the batches. Each batch is shown separately.
    

### [Cube Sync Performance Over Time](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor_dashboards_cube_sync)

Use this dashboard to see how much time was spent synchronizing the Health Insight cubes. The first chart displays how much time was spent synchronizing each cube. The second displays how much time was spent evaluating source expressions in each cube; any value in a cube is based either on a source value or a source expression. If a large amount of time is spent evaluating source expressions, it is worth examining the code used in those expressions. The last chart displays the rate at which the cubes were updated, in facts per second (which means the number of rows in the fact table, per second).

Use the buttons in the upper chart to control the horizontal axis; see “[Batch Activity Over Time](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor_dashboards_batch_activity).”

### [Most Recent Batch Details](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor#HSAAADM_monitor_dashboards_most_recent)

Use this dashboard to see the progress of the most recent analytics batch (or for the selected batch).

The dashboard displays the following information for each batch:

*   `Batch Session ID` is the session ID of the most recent batch.
    
*   `First QueryRequest ID` and `Last QueryRequest ID` are the IDs of the first and last Advanced Clinical Notification (ACN) queries to be executed.
    
*   `Sync Error Count` is the total number of cube synchronization errors for all Health Insight-enabled cubes.
    
*   `Batch Start Time` and `Batch End Time` indicate the start and end times of the batch. For details on the steps within the analytics batch, see “[Data Feed Details](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_details)” in the Health Insight Installation and Configuration Guide.
    
*   `Post Transfer Start` and `Post Transfer End` indicate the start and end times of the post-transfer phase.
    
*   `Clinical Cube Sync Start` and `Clinical Cube Sync End` indicate the start and end times of the phase during which Health Insight synchronizes the main Health Insight cubes (as opposed to the reporting cubes, which are used on these dashboards).
    
*   `Post Sync Start` and `Post Sync End` indicate the start and end times of the post-synchronization phase.
    
*   `Post Batch Start` and `Post Batch End` indicate the start and end times of the post-batch phase.
    
*   `Query Start` and `Query End` are the time when the first ACN query begins executing and the time when the last ACN query finishes executing.
    
*   `Report Cube Update Start` and `Report Cube Update End` indicate the start and end times of the phase during which Health Insight updates the cubes used by the Platform Information dashboards.
