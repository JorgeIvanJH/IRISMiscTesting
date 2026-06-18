# [Working With the Consistency Check Tool](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq).

This chapter describes the Consistency Check Tool in HealthShare Health Insight.

## [Overview of the Consistency Check Tool](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_overview)

The Consistency Check Tool ensures that data in HealthShare Unified Care Record is correctly transmitted to Health Insight by comparing counts of encounters and patients in Unified Care Record and Health Insight. Counts of patients and encounters may be compared for each facility over different time periods. The Consistency Check tool determines the count of encounters by totaling the number of encounters at each facility during a time period. The patient count is determined by the number of distinct patients that have an encounter at each facility during a time period.

Note that patients using more than one MRN in the same facility in the same month will appear in Unified Care Record as multiple, distinct patients.

## [Using the Consistency Check Tool](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_using)

### [Generating a Consistency Check Report](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_using_generate)

Prior to generating a Consistency Check report, do the following in your Health Insight instance:

1.  Switch to your Health Insight namespace, usually `HSANALYTICS`.
    
2.  Navigate to the `Production List` page (`Interoperability` > `List` > `Productions`), select your Health Insight production, and click `Open`.
    
3.  Confirm that the Health Insight production is running.
    
4.  Confirm that the [HSAA.Common.Services](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Common.Services) business service and the [HS.Gateway.HSWS.RemoteOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.HSWS.RemoteOperations) business operation are enabled.
    

Next, do the following on the Edge instances that feed your Health Insight instance:

1.  Switch to your Edge namespace (for example, `HSEDGE1`).
    
2.  Navigate to the `Production List` page (`Interoperability` > `List` > `Productions`), select your Edge production, and click `Open`.
    
3.  Confirm that the Edge production is running.
    
4.  Confirm that the [HS.Gateway.HSWS.WebServices](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.HSWS.WebServices) business service is enabled.
    

Then, do the following on your Registry instance:

1.  Switch to your Registry namespace (for example, `HSREGISTRY`).
    
2.  Navigate to the `Production List` page (`Interoperability` > `List` > `Productions`), select your Registry production, and click `Open`.
    
3.  Confirm that the Registry production is running.
    
4.  Confirm that the [HS.Hub.HSWS.WebServices](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Hub.HSWS.WebServices) business service is enabled.
    

You can use the `GenReportAsync()` method of the [HSAA.ConsistencyCheck.Report](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ConsistencyCheck.Report) class to generate a Consistency Check Report as a background job. Note that only a user with the %HSAA_Operator role can run this method.

The `GenReportAsync()` method has four arguments:

<table><tr><td><code>Days</code></td><td>Optional. A numeric argument. If a positive number of days is specified, this method generates the Consistency Check report for the last <code>Days</code> number of days. For example, if the current date was January 20th, a <code>Days</code> value of 10 would result in a Consistency Check report from January 11th to January 20th, with both the 11th and 20th included. If <code>Days</code> is not specified or if a value of <code>-1</code> is given, the Consistency Check report is generated over all time. Note that if a value of <code>All</code> or <code>Patient</code> is entered for the <code>typeFilter</code> argument, the <code>GenReport()</code> method will generate an extra row of data for each facility in the resulting Consistency Check Report table. Each of these rows represents data for patients over all time.</td></tr><tr><td><code>typeFilter</code></td><td>Optional. A String argument with three possible values: <code>All</code>, <code>Encounter</code>, or <code>Patient</code>. <code>All</code> indicates no filter on clinical data type, while specifying <code>Encounter</code> or <code>Patient</code> will generate a Consistency Check with only encounters or patients, respectively.</td></tr><tr><td><code>facilityFilter</code></td><td>Optional. A String argument that filters upon facilities. The default value is <code>All</code>, which indicates no filter on facilities. In this case, a Consistency Check report is generated for all facilities. Filtering on a list of comma-seperated facility tags, such as <code>MGH,CGH,CHMC</code> will generate a Consistency Check report for only the facilities whose facility tags are included in <code>facilityFilter</code>. Note that facility tags should not contain commas.</td></tr><tr><td><code>ReportID</code></td><td>A numeric output argument. You can use <code>ReportID</code> to get the status of the current Consistency Check Report job. To do so, use the <code>CheckReportStatus()</code> method in the <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.ConsistencyCheck.Report">HSAA.ConsistencyCheck.Report</a> class.</td></tr></table>

After the `GenReportAsync()` method is called, the [HSAA.ConsistencyCheck.Report](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ConsistencyCheck.Report) table is populated with data. Each Consistency Check report consists of rows in the [HSAA.ConsistencyCheck.Report](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ConsistencyCheck.Report) table. Rows that are from the same Consistency Check report will have the same Report Time and Report ID.

You can view the [HSAA.ConsistencyCheck.Report](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ConsistencyCheck.Report) table in the SQL Explorer. This table has the following fields:

<table><tr><td>Report Time</td><td>When the report is generated</td></tr><tr><td>Report ID</td><td>The ID of the report</td></tr><tr><td>Info Type</td><td>The type of clinical data</td></tr><tr><td>Facility</td><td>The facility in which the clinical data originated</td></tr><tr><td>Month</td><td>Time associated with a clinical data event in YYYY-MM format. Equivalent to the Unified Care Record <code>UpdatedOn</code> property from the <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HS.SDA3.Streamlet.Abstract">HS.SDA3.Streamlet.Abstract</a> class.</td></tr><tr><td>Edge Count</td><td>Count of patients or encounters on the Edge Gateway. If the Info Type of the row is <code>Patient</code>, Edge Count represents the number of distinct MRNs in the specified facility for the specified month. If the Month of a row is <code>Null</code>, Edge Count represents the total distinct MRNs in the specified facility over all time for that facility.</td></tr><tr><td>Health Insight Count</td><td>Count of patients or encounters in Health Insight. For patients, Health Insight Count totals the number of HSAAIDs. If the Month of a row is <code>Null</code>, Health Insight Count represents the count of distinct HSAAIDs in the specified facility over all time.</td></tr><tr><td>HI MPI Count</td><td>The count of distinct MPIs for patients who have one or more encounters at a facility during a given month in Health Insight. If the Month of a row is <code>Null</code>, this field is the count of the distinct MPIs for patients who have had encounters at the specified facility over all time. Only meaningful when Info Type is <code>Patient</code>. For other Info Types, this field should be <code>-1</code>.</td></tr><tr><td>HI MRN Count</td><td>The count of distinct MRNs for patients who have one or more encounters at a facility during a given month in Health Insight. If the month of a row is <code>Null</code>, this field is the count of distinct MPIs for patients who have had encounters at the specified facility over all time. Only meaningful when Info Type is <code>Patient</code>. For other Info Types, this field should be <code>-1</code>.</td></tr><tr><td>Hub MPI Count</td><td>The count of distinct MPIs for patients who have been to the specified facility over all time on the Hub. This field is only meaningful when Info Type is <code>Patient</code> and Month is <code>Null</code> because Hub MPI and MRN counts can be grouped by facility, but not by month. In any other case, this field should have a value of <code>-1</code>.</td></tr><tr><td>Hub MRN Count</td><td>The count of distinct MRNs for patients who have been to the specified facility over all time on the Hub. This field is only meaningful when Info Type is <code>Patient</code> and Month is <code>Null</code> because Hub MPI and MRN counts can be grouped by facility, but not by month. In any other case, this field should have a value of <code>-1</code>.</td></tr><tr><td>MRN Cnt Delta (Edge-Hub)</td><td>Edge Count — Hub MRN Count. Only meaningful when Info Type is <code>Patient</code> and Month is <code>Null</code> because Hub MPI and MRN counts can be grouped by facility, but not by month. In any other case, this field should have a value of <code>-1</code>.</td></tr><tr><td>MRN Cnt Ratio (Hub/Edge)</td><td>Hub MRN Count/Edge Count. Only meaningful when Info Type is <code>Patient</code> and Month is <code>Null</code> because Hub MPI and MRN counts can be grouped by facility, but not by month. In any other case, this field should have a value of <code>-1</code>.</td></tr><tr><td>MRN Cnt Delta (Hub-HI)</td><td>Hub MRN Count — HI MRN Count. Only meaningful when Info Type is <code>Patient</code> and Month is <code>Null</code> because Hub MPI and MRN counts can be grouped by facility, but not by month. In any other case, this field should have a value of <code>-1</code>.</td></tr><tr><td>MRN Cnt Ratio (HI/Hub)</td><td>HI MRN Count/Hub MRN Count. Only meaningful when Info Type is <code>Patient</code> and Month is <code>Null</code> because Hub MPI and MRN counts can be grouped by facility, but not by month. In any other case, this field should have a value of <code>-1</code>.</td></tr><tr><td>MPI Cnt Delta (Hub-HI)</td><td>Hub MPI Count — HI MPI Count. Only meaningful when Info Type is <code>Patient</code> and Month is <code>Null</code> because Hub MPI and MRN counts can be grouped by facility, but not by month. In any other case, this field should have a value of <code>-1</code>.</td></tr><tr><td>MPI Cnt Ratio (HI/Hub)</td><td>HI MPI Count/Hub MPI Count. Only meaningful when Info Type is <code>Patient</code> and Month is <code>Null</code> because Hub MPI and MRN counts can be grouped by facility, but not by month. In any other case, this field should have a value of <code>-1</code>.</td></tr><tr><td>MRN Cnt Delta (Edge-HI)</td><td>Edge MRN Count — HI MRN Count. Only meaningful when Info Type is <code>Patient</code>. In any other case, this field should have a value of <code>-1</code>.</td></tr><tr><td>MRN Cnt Ratio (HI/Edge)</td><td>HI MRN Count/Edge MRN Count. Only meaningful when Info Type is <code>Patient</code>. In any other case, this field should have a value of <code>-1</code>.</td></tr><tr><td>ENC Cnt Delta (Edge-HI)</td><td>Edge Count — Health Insight Count. Only meaningful when Info Type is <code>Encounter</code>. In any other case, this field should have a value of <code>-1</code>.</td></tr><tr><td>ENC Cnt Ratio (HI/Edge)</td><td>Health Insight Count/Edge Count. Only meaningful when Info Type is <code>Encounter</code>. In any other case, this field should have a value of <code>-1</code>.</td></tr></table>

#### [Example GenReportAsync() Calls](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_using_generateasync_ex)

*   To create a background Consistency Check report job that checks all data, do the following:
    
    ```
     set sc = ##class(HSAA.ConsistencyCheck.Report).GenReportAsync(-1,,,.ReportID)
     set sc = ##class(HSAA.ConsistencyCheck.Report).CheckReportStatus (ReportID,.Status,.Error)
     w Status
     w Error
    ```
    
    To create a background Consistency Check report job that checks data for events in the last 30 days, do the following:
    
    ```
     set sc = ##class(HSAA.ConsistencyCheck.Report).GenReportAsync(30,”All”,”All”,.ReportID)
     set sc = ##class(HSAA.ConsistencyCheck.Report).CheckReportStatus (ReportID,.Status,.Error)
     w Status
     w Error
    ```
    
    To create a background Consistency Check report job that checks data for Encounters in the `CGH` and `MGH` facilities in the last 30 days, do the following:
    
    ```
     set sc = ##class(HSAA.ConsistencyCheck.Report).GenReportAsync(30,”Encounter”,”CGH,MGH”,.ReportID)
     set sc = ##class(HSAA.ConsistencyCheck.Report).CheckReportStatus (ReportID,.Status,.Error)
     w Status
     w Error
    ```
    

### [Writing a Generated Report to a File](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_using_write)

To write the results of the latest Consistency Check report to a file, use the `WriteToFile()` method of the [HSAA.ConsistencyCheck.Report](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ConsistencyCheck.Report) class. The `WriteToFile()` method has one argument:

<table><tr><td><code>FilePath</code></td><td>Required. A String argument. This argument is the target file path, for the resulting Consistency Check report file. <code>FilePath</code> should include the desired name for the Consistency Check report file. If only a filename, such as <code>ConsistencyCheck.csv</code>, is specified, the file will be generated in the user’s <code>instancePath</code>\mgr\<code>namespace</code> directory, where <code>instancePath</code> is the path of the Health Insight instance, and <code>namespace</code> is the name of the Health Insight namespace.</td></tr></table>

### [Searching the Report](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_using_search)

To perform searches on Consistency Check reports, use the `SearchReport()` method of the [HSAA.ConsistencyCheck.Report](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ConsistencyCheck.Report) class. This method will search the rows of the [HSAA.ConsistencyCheck.Report](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ConsistencyCheck.Report) table. The `SearchReport()` method has four arguments:

<table><tr><td><code>Type</code></td><td>Optional. A String argument with three possible values: <code>All</code>, <code>Encounter</code>, or <code>Patient</code>. <code>All</code> indicates search on all clinical data types, while specifying <code>Encounter</code> or <code>Patient</code> indicates a search only on rows that correspond to Encounters or Patients, respectively.</td></tr><tr><td><code>Facility</code></td><td>Optional. A String argument that indicates if facility should be searched on. The default value is <code>All</code>, which indicates a search on all facilities. A <code>Facility</code> value of <code>MGH</code> indicates a search only on rows with a Facility tag of <code>MGH</code>.</td></tr><tr><td><code>Time</code></td><td>Optional. A String argument that indicates if a specific time range should be searched on. The default value is <code>All</code>, which indicates a search across all time. Input should be in the format <code>YYYY-MM</code>.</td></tr><tr><td><code>LatestReport</code></td><td>Optional. A Boolean argument. A <code>LatestReport</code> value of <code>1</code> indicates a search on the latest generated report, which is the latest result of <code>GenReport()</code>. Note that this latest generated report may or may not have been generated by the current user, and may or may not contain records with the type, facility, or time that the user is searching for. Otherwise, this method searches on all generated reports in the <code>HSAA_ConsistencyCheck.Report</code> table.</td></tr></table>

The `SearchReport()` method has one output argument:

<table><tr><td><code>rset</code></td><td>Required. A <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25SQL.StatementResult">%SQL.StatementResult</a> output argument. This is the corresponding <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25SQL.StatementResult">%SQL.StatementResult</a> from the <code>HSAA_ConsistencyCheck.Report</code> table.</td></tr></table>

#### [Example Calls](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_using_search_ex)

*   To search over all time in the latest generated report for rows of the [HSAA.ConsistencyCheck.Report](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ConsistencyCheck.Report) table that:
    
    *   Have the Encounter type
        
    *   Are from the CGH facility
        
    
    use calls such as the following:
    
    ```objectscript
     set sc = ##class(HSAA.ConsistencyCheck.Report).SearchReport("Encounter","CGH","All",1,.rset)
     do rset.%Display()
    ```
    
*   To search in the month of May 2018 over all generated reports for rows of the [HSAA.ConsistencyCheck.Report](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ConsistencyCheck.Report) table that:
    
    *   Have the Encounter type
        
    *   Are from any facility
        
    
    use calls such as the following:
    
    ```objectscript
     set sc = ##class(HSAA.ConsistencyCheck.Report).SearchReport("Encounter","All","2018-05",0,.rset)
     do rset.%Display()
    ```
    

### [Fetching Consistency Checks with Lower Match Percentages](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_using_lower)

In order to fetch all rows of the [HSAA.ConsistencyCheck.Report](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ConsistencyCheck.Report) table with MRN Cnt Ratio (HI/Edge) < 90% or ENC Cnt Ratio < 90%, use the `GetConsistencyCheckWithLowerMatchPercent()` method in the [HSAA.ConsistencyCheck.Report](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ConsistencyCheck.Report) class. This method has one input argument:

<table><tr><td><code>LatestReport</code></td><td>Optional. A Boolean argument. The default value is 1, which indicates a search on rows of the <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.ConsistencyCheck.Report">HSAA.ConsistencyCheck.Report</a> table in the latest generated report. Otherwise, this method searches on all rows in the <code>HSAA_ConsistencyCheck.Report</code> table.</td></tr></table>

This method has one output argument:

<table><tr><td><code>rset</code></td><td>Required. A <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25SQL.StatementResult">%SQL.StatementResult</a> output argument. These are the corresponding Consistency Check records with lower match percentages from the <code>HSAA_ConsistencyCheck.Report</code> table in <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25SQL.StatementResult">%SQL.StatementResult</a> form.</td></tr></table>

### [Clearing the HSAA_ConsistencyCheck.Report Table](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_using_clean)

In order to remove records from the `HSAA_ConsistencyCheck.Report` table, use the `CleanTable()` method in the [HSAA.ConsistencyCheck.Report](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ConsistencyCheck.Report) class. This method has one input argument:

<table><tr><td><code>Days</code></td><td>Optional. A numeric argument. The default value is –1, which indicates that all data in the <code>HSAA_ConsistencyCheck.Report</code> table should be deleted. A positive value for <code>Days</code> indicates that only Consistency Check records with a report time greater than <code>Days</code> days ago should be deleted. For example, a value of 30 for <code>Days</code> indicates that all records that were generated more than 30 days ago should be deleted.</td></tr></table>

## [Consistency Check Dashboards](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_dash)

Health Insight provides several dashboards that display reports using data obtained from Consistency Check reports. To access these dashboards:

1.  Switch to your Health Insight namespace, usually `HSANALYTICS`.
    
2.  From the Management Portal, click `Analytics`, then click `User Portal`.
    
3.  Click on a dashboard of your choice under the `Consistency Check` category in the User Portal.
    

Health Insight provides several default Consistency Check dashboards. Users with the %HSAA_Operator role can access all of these dashboards. More specifically, any user with the %HSAA_OperationalDashboards resource can access these dashboards.

### [MRN and Encounter (with Monthly drill-down) Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_dash_mrnencounter)

The `MRN and Encounter (with Monthly drill-down)` compares MRN and Encounter counts between Health Insight and the Edge Gateways. This dashboard displays percentage agreement on the y axis by dividing the Health Insight count by the Edge count. Two comparisons are displayed — MRN Cnt Ratio (HI/Edge) for patients, and ENC Cnt Ratio (HI/Edge) for encounters. Reports can be scheduled to run repeatedly. The dashboard displays the time that each report was generated on the x axis.

You can drill down to the month level by selecting a bar of data on the dashboard and using the Drill Down arrow button on the toolbar. To return to the high-level report, use the up arrow button on the toolbar.

This dashboard has four available filters:

*   `Report Time` — Filters by the time a report was generated.
    
*   `Facility` — Filters by the facility tag of the clinical data.
    
*   `Clinical Data Date` — Filters by the month of the clinical data.
    
*   `Clinical Data Type` — Filters by the type of clinical data.
    

### [MPI (with Facility drill-down) Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_dash_mpi)

The `MPI (with Facility drill-down)` dashboard compares counts between Health Insight and the HealthShare Registry (Hub). This dashboard displays percentage agreement in the form of the MPI Cnt Ratio (HI/Hub) on the y axis and time that the report was generated on the x axis.

You can drill down to the facility level by selecting a bar of data on the dashboard and using the Drill Down arrow button on the toolbar. To return to the high-level report, use the up arrow button on the toolbar.

This dashboard has two available filters, Facility and Report Time, which are described in the [MRN and Encounter (with Monthly drill-down) Dashboard](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_dash_mrnencounter) section.

### [MRN (with Facility drill-down) Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_dash_mrn)

The `MRN (with Facility drill-down)` dashboard compares counts between Health Insight, the HealthShare Registry, and the Edge Gateways. The left chart displays percentage agreement on the y axis. Two types of agreement are displayed: MRN Cnt Ratio (Hub/Edge) and MRN Cnt Ratio (HI/Hub). The left chart displays report generation time on the x axis.

The right chart displays counts of MRNs between Health Insight, the Registry, and the Edge Gateways. The x axis displays the time when the report was generated, while the y-axis displays counts of MRNs.

You can drill down to the facility level by selecting a bar of data on the dashboard and using the Drill Down arrow button on the toolbar. To return to the high-level report, use the up arrow button on the toolbar.

This dashboard has two available filters, Facility and Report Time, which are described in the [MRN and Encounter (with Monthly drill-down) Dashboard](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_dash_mrnencounter) section. The Facility and Report Time filters apply to both charts when used.

### [Consistency Check Reports Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_dash_consistencycheck)

The `Consistency Check Reports Dashboard` shows detailed reports for each Clinical Data Type, Facility, and Clinical Data Date.

The four available filters are identical to the filters of the [MRN and Encounter (with Monthly drill-down) Dashboard](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_dash_mrnencounter).

### [Saving a Copy of a Dashboard with a Different Filter](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_dash_saving)

You can create a copy of a dashboard and save it with filter settings applied. To do so:

1.  Navigate to the dashboard you want to copy, as described [above](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency#HSAAADM_consistency_dash).
    
2.  Click `Menu` > `Save As`.
    
3.  Keep the same value for `Category`, but enter a different `Dashboard Title`.
    
4.  Click `Home` to navigate back to the User Portal.
    
5.  Open the new dashboard that you created.
    
6.  Choose the filters that you want to apply, then use `Menu` > `Save Settings` to save the dashboard with your filter settings.
