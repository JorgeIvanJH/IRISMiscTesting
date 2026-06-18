# [Working With Power BI](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi)

This chapter describes how to use Microsoft Power BI with HealthShare Health Insight.

## [Introduction to Power BI in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_intro)

You can use the InterSystems Health Insight Connector for Power BI to [connect Microsoft Power BI to the Health Insight source tables](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=APOWER). Once you have done so, you can publish visual reports and dashboards using data directly from Health Insight.

With the connector pointed to the Analytics namespace, you can select from any of the Health Insight source tables; Power BI will automatically infer the relationships between these tables. Power BI also works well against custom views that are defined in the Analytics namespace. Within the same reports, you can also query data from other data sources, joining that data with the Health Insight data for richer reporting. The InterSystems Health Insight Connector supports both the Import and DirectQuery modes in Power BI for Data Connectivity. Given the large amount of data in most Health Insight deployments, you may find that DirectQuery mode is often the most appropriate access mode.

This documentation only includes basic report creation examples in Power BI Desktop’s Report View. For more information on advanced Power BI use cases, see the Microsoft Power BI documentation.

## [Creating Health Insight Views for Power BI](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_views)

You can solve certain issues with Power BI and the InterSystems Health Insight Connector via the creation of custom views. Instead of connecting Power BI to the source tables, you connect Power BI to the views you create. You can either [create your own views](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_views) or use the `CreateViewEntry` utility to create a view for any Health Insight table.

The following issues can be partially or completely addressed via view creation:

*   [Booleans Cause Errors in DirectQuery Mode](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_boolean)
    
*   [Long Strings Cause Errors in DirectQuery Mode](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_longstring)
    
*   [Cube Detail Listings Are Not Supported](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_detaillist)
    
*   [Row Limitations for Large Amounts of Data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_rows)
    

You can create a view for any Health Insight table with the above issues.

### [Using the View Creation Utility](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_views_utility)

You need the following privileges before you can use the `CreateViewEntry` utility:

*   Access to Terminal in the Analytics namespace
    
*   SELECT privileges on the Health Insight tables that you are creating views for
    
*   View creation privileges
    

To create a view for a Health Insight source table via the view creation utility:

1.  Open the Terminal and navigate to the Analytics namespace.
    
2.  Enter the following command:
    
    ```
    do ##class(HSAA.Utils).CreateViewEntry(tablename)
    ```
    
    ...where `tablename` is the name of the Health Insight table.
    
3.  The utility will display execution details and other information in the Terminal. After it has finished, you can navigate to the [Management Portal SQL Interface](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_smp) page to confirm that the view was created.
    

## [Parameterizing Connection Components with Power BI in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_param)

You can parameterize connection components when using the InterSystems Health Insight Connector for Power BI with Health Insight. Doing so provides a central place to manage and update connection settings and enables you to more easily change data sources. If you choose not to parameterize your connection components and want to switch instances or data sources, manual edits will be required in the Advanced Query Editor for each table used in your reports.

To replace hardcoded connection details with parameterized versions:

1.  [Create a parameter](https://learn.microsoft.com/en-us/power-query/power-query-query-parameters#creating-a-parameter) with your connection details.
    
2.  For any table that you want to parameterize the connection of, use the [Advanced Editor](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-query-overview#advanced-editor) to replace hardcoded connection parameters with the new variables that you created.
    

## [Troubleshooting and Logging Power BI with Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_trouble)

If you encounter issues when using Power BI with Health Insight, you can enable Power BI and ODBC logging on your Power BI machine to troubleshoot. Only enable these types of logging in controlled environments, as they can have large performance impact.

### [Using Power BI Logging in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_trouble_bi)

For more information on using Power BI logging, see the Microsoft Power BI [documentation](https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-diagnostics). Note that Power BI generates many log files, so you may want to use the `Clear Traces folder` button to clear previous logs before you begin using Power BI logging. This ensures that your log files were generated during your most recent logging session.

### [Using ODBC Logging for Power BI in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_trouble_odbc)

For instructions on enabling ODBC logging, see [ODBC Logging on Windows](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=BNETODBC_logging#BNETODBC_logging_logwin). If you have a locally installed kit of InterSystems IRIS or HealthShare, DSNs are created during the installation process. You can enable logging for any existing InterSystems IRIS ODBC35 data source. Once you enable ODBC logging for any InterSystems IRIS DSN, ODBC logging is enabled for all ODBC connections using an InterSystems IRIS DSN on your machine.

If you downloaded an ODBC driver manually and do not have a locally installed kit, you must first [create a DSN](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=BNETODBC_winodbc#BNETODBC_winodbc_dsn-dialog) using the InterSystems IRIS ODBC35 driver so that you can enable logging. Note that DSNs are not otherwise used by the Connector or Power BI for any purpose, including when connecting to Health Insight. Setting up a DSN when using Power BI with Health Insight is only required for enabling ODBC logging. As a result, you can enter the details for any InterSystems IRIS or HealthShare instance when setting up your DSN.

Contact the WRC if you need assistance interpreting your ODBC logs.

### [Cannot Load Model When Publishing to Power BI](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_trouble_publishing)

When publishing a Power BI report that uses DirectQuery to connect to Health Insight, you may encounter the following error: `Cannot Load Model.` This issue typically occurs when a required data gateway is not configured or associated with the published dataset.

To resolve this issue, install and configure the [on-premises data gateway](https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-install) on your Power BI machine. After installation, ensure that the gateway is added to your Power BI Service account and associated with the dataset in the workspace where the report is published.

Once the gateway is correctly configured, Power BI should be able to connect to Health Insight using DirectQuery and load the model without errors.

This issue does not occur when using Import mode instead of DirectQuery, as Import mode does not require a live connection to the data source after publishing.

### [DataSource Error for Power BI Dashboard and SQL Views](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_C11810)

In some cases, dashboard visualizations may fail to load and display the error message: `Couldn’t load the data for this visual`. A similar DataSource issue can also occur when previewing certain SQL views within Power BI.

This error is typically caused by a run-time issue with parallel query execution on the connected Health Insight instance.

To resolve the issue, restart the HealthShare or InterSystems IRIS instance to which Power BI is connected. This clears the internal state and restores query functionality for affected dashboards and views.

## [Known Issues with Power BI in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known)

This section describes known issues that can occur when you use the InterSystems Health Insight Connector to connect Microsoft Power BI to Health Insight. It also discusses complete or partial workarounds for some issues.

### [Booleans Cause Errors in DirectQuery Mode](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_boolean)

When using Power BI in DirectQuery mode, attempting to create filters, slicers, or visuals with Health Insight Booleans will result in errors. This is because the InterSystems Health Insight Connector exposes Booleans as the BIT datatype. Power BI cannot handle BIT data in DirectQuery mode and will return a folding error if you attempt to create filters, slicers, or visuals.

You can correct this issue by exposing the Boolean in a [view](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_views) via a [CAST](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_cast) statement like the following:

```
CAST((CASE WHEN <fieldname>=1 then 1 ELSE 0 END) as INTEGER) as <fieldname>
```

...where `<fieldname>` is the Boolean in question.

This CAST statement exposes the Boolean as an Integer, which Power BI can handle without error. Any NULLs are defaulted to 0.

See the [Creating Views](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_views) section for more information.

### [Long Strings Cause Errors in DirectQuery Mode](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_longstring)

When using Power BI in DirectQuery mode, attempting to create filters, slicers, or visuals with long Health Insight strings will result in errors. When data is brought into a report in DirectQuery mode, the Power BI engine tries to limit the number of queries sent to the source environment and will attempt to use data that it has cached in memory. When the engine uses cached memory data, it is unable to handle larger strings and returns a folding error.

For example, `Gender_Code` in [HSAA.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Patient) has a maximum length of 32,000 and will cause errors in DirectQuery mode. You can correct this issue by exposing the property in a [view](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_views) via a [CAST](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_cast) statement like the following:

```
CAST(<fieldname> AS VARCHAR(4000)) as <fieldname>
```

...where `<fieldname>` is the long string in question.

This CAST statement limits the schema maximum length that is sent to Power BI. Ensure that you do not eliminate important data via this CAST statement. As an example, you might confirm that your Gender_Code data never exceeds 4000 characters in length, meaning that you can shorten the maximum length that is sent to Power BI without consequence.

See the [Creating Views](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_views) section for more information.

### [Cube Detail Listings Are Not Supported](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_detaillist)

If you use Power BI with the Health Insight cubes, detail listings are not supported. Several Power BI options do not fully replicate the detail listing functionality, but are similar:

*   The [drill-down option](https://learn.microsoft.com/en-us/power-bi/consumer/end-user-drill) can be used to view data at a higher level of granularity and works best with hierarchical data.
    
*   The [drillthrough option](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-drillthrough) can be used to view data in a specific context for a targeted subset of data.
    
*   The [Data point table option](https://learn.microsoft.com/en-us/power-bi/create-reports/end-user-show-data?tabs=powerbi-desktop#use-data-point-table-in-power-bi-desktop) can be used to focus on the data behind a particular component in a visual.
    

You can also create a view to support drilling down to specific data. To do so:

1.  [Create a view](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_views) for the table and fields of interest.
    
2.  Connect to the view that you created with Power BI and [add a relationship](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-create-and-manage-relationships#create-a-relationship-manually) between the view and `Fact.Patient`. Use the view that you created as your report table.
    
3.  Create a listing report and [specify the field](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-cross-report-drill-through#set-up-a-cross-report-drillthrough-target) that you want to drill to.
    
4.  Create a report or visual with data from your view. When you right-click on the data, the field that you specified earlier should appear under `Drill through`.
    

### [Row Limitations for Large Amounts of Data](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_rows)

DirectQuery mode restricts query results [to a maximum of 1 million rows](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-directquery-about#directquery-limitations). Users may encounter this issue when working with large amounts of data. This limit impacts both tables and cubes, but is more pronounced for tables. To address this issue, consider the following workarounds:

*   Create a view [for the tables](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_views_utility) or cubes that limits row output to below one million and connect Power BI to this view. For example, if you wanted to limit your data to only include entries from 2016, you might add a WHERE clause like the following to your table view query:
    
    ```
    WHERE StartTime BETWEEN '2016-01-01 00:00:00' AND '2016-12-31 24:00:00'
    ```
    
    If you create a view for a cube, ensure that it combines the cube details you need. Combine your fact and dimension columns together in one presentation layer.
    
*   [Apply a filter](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-add-filter?tabs=powerbi-desktop) to limit the number of rows in Power BI. You can use the filter functionality to display a specific number of leading rows.
    
*   [Use a slicer](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicers?source=recommendations&tabs=powerbi-desktop) to limit the number of rows that are displayed. Ensure that the slicers that you provide work in all instances that a user might select.
    

You can also consider upgrading to Power BI Premium, which [removes the 1 million row limit](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-premium-workloads#max-intermediate-row-set-count). Consult the WRC before proceeding.

### [Top N Filters Can Fail When Filtering on Large Data Sets](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_topn)

If you use Top N filter in Power BI on a large Health Insight table or cube, you may encounter an error. Power BI will first retrieve the entirety of the data that you queried for before applying the Top N filter. If your table or cube is too large, Power BI may encounter the [1 million row restriction issue](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_rows) before the Top N filter is applied. You can apply the workarounds listed in the [Row Limitations for Large Amounts of Data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_rows) section to pre-filtered data. After you do so, you will be able to apply a Top N filter to the data in question.

This issue is described in the Microsoft Power BI [documentation](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-directquery-about#reporting-limitations), in the TopN Filters section.

### [Cube Calculations Not Exposed to Power BI](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_calc)

Health Insight supports the creation of cube calculations, like calculated measures and columns. However, these calculations are not exposed to Power BI and do not show up once you have connected Power BI to a cube. If you want to access these calculations in Power BI, you can either:

*   Recreate your calculation via an alternate method, such as in a [custom view](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_calc_view) or cube
    
*   Recreate your calculation [via Power BI](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_calc_powerbi)
    

Any [SQL](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_overview) calculations in Health Insight are exposed to Power BI.

#### [Recreating a Calculated Measure Via a View](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_calc_view)

This section provides an example of how you might recreate a measure via a view. In the standard Health Insight Patient cube, there is a measure called InpatientVisits, which counts the number of inpatient encounters for a patient. You might [create a view](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_views) via a command like the following to duplicate the measure:

```
CREATE VIEW HSAA_Views.InpatientVisits AS
SELECT patient, COUNT(ID) AS InpatientVisits
FROM HSAA.Encounter
WHERE EncounterType = 'INPATIENT'
GROUP BY patient
WITH READ ONLY;
```

#### [Recreating Calculations in Power BI](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_calc_powerbi)

Power BI supports the creation of two types of calculations: measures and columns. If calculations are specific to certain rows, use calculated columns. If a calculation is more global and aggregates values across rows, use a calculated measure. Calculations in Power BI use DAX. For more information on DAX, see the [DAX function reference](https://learn.microsoft.com/en-us/dax/).

See the Power BI documentation for more information on [calculated measures](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-tutorial-create-measures) and [calculated columns](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-tutorial-create-calculated-columns).

When you create calculations in Power BI, keep in mind the following:

*   Develop your calculation in the most optimal area, ensuring the use of as many indexes as possible.
    
*   Ensure consistent data types are returned in your functions to avoid folding issues in Power BI.
    
*   Be aware of any limitations for the options that you select. For example, certain DAX functions are not available for use if you use Direct Query.
    

### [Filters May Not Apply to Unused Fields in Power BI Visuals](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_powerbi#HSAA_powerbi_known_visualfilter)

If you filter on a field in a Power BI visual, the filter will not be applied unless the field is used in at least one visual within your currently open Power BI report.
