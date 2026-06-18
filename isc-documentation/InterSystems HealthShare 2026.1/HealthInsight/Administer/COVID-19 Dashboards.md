# [Working With the Health Insight COVID-19 Dashboards](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq).

> **Note:**
> 
> The COVID-19 dashboards are [deprecated](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20251#HSAARN_20251_deprecated).

Sample COVID-19 InterSystems IRIS Business Intelligence demonstration dashboards are included with HealthShare Health Insight.

*   [Overview](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_over)
    
*   [Working with the Counts Over Time Dashboard](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_counts)
    
*   [Working with the Risk Model Dashboard](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_risk)
    
*   [Working with the Syndromic Surveillance Dashboard](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_surveillance)
    
*   [Customizing the Value Set](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_valueset)
    
*   [Customizing a COVID-19 Dashboard](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_customize)
    

## [COVID-19 Dashboard Overview](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_over)

The sample COVID-19 dashboards illustrate how customers can use Health Insight to analyze, explore, and report on COVID-19–related data. Health Insight includes several of these Business Intelligence dashboard examples, which use test data (the `HSAA_COVID19.ValueSets` table in the Analytics namespace) and queries related to COVID-19. These dashboards, as well as the corresponding value sets, cubes, cube dimensions, and pivots, can be copied and adapted to suit your organization’s needs. For more information on Business Intelligence, see the [Business Intelligence documentation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2GS_ch_intro).

The `HSAA_COVID19.ValueSets` data included with Health Insight provides examples of codes and coding standards directly related to COVID-19, as well as other clinical data. The examples use the Patient Current Conditions cube to identify comorbidities that may raise the risk of patients for developing severe complications with COVID-19. A number of cubes, such as the Lab Result Item cube, have dimensions that are used by the COVID-19 dashboards. Pre-constructed pivot tables built from such cubes (like the COVID19 Tests by Age pivot) are used as data sources on the COVID-19 dashboard widgets.

As a more specific example, the Lab Result Items cube has a Covid-19 Lab Test dimension, which has a HadCOVID19LabTest level based on a source expression. This level’s source expression calls a class method in the [HSAA.COVID19.CubeQueries](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.COVID19.CubeQueries) class, which executes a cube query to check if a patient has any lab test items with codes matching the COVID-19 Lab Test Value Set. If a lab test item has a matching code, then the patient has had a COVD-19 lab test performed. In general, the COVID-19 dashboards rely on the [HSAA.COVID19.CubeQueries](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.COVID19.CubeQueries) class, which contains methods that both query Health Insight data and compare that data with codes from the `HSAA_COVID19.ValueSet` table.

Prior to using the COVID-19 dashboards for the first time after a new install or upgrade, you must run the `RunSetupCOVID19Dashboards()` method. This method performs required setup steps for the COVID-19 dashboards. The last step of the `RunSetupCOVID19Dashboards()` method involves building all cubes that either support the dashboard or are related to cubes that support the dashboard. Building these cubes might take a long time if you have large amounts of Health Insight data, so this last step runs as a background job once all other parts of the method have completed.

To run the `RunSetupCOVID19Dashboards()` method, execute the following command in your Analytics namespace:

```objectscript
 set tsc=##class(HSAA.COVID19.Installer).RunSetupCOVID19Dashboards()
```

You can check the status of the background cube build job with the following command:

```objectscript
 set sc=##class(HSAA.COVID19.Installer).CheckSetupCOVID19Dashboards()
```

Once the `RunSetupCOVID19Dashboards()` method has completed execution, you can view the COVID-19 dashboards by navigating to the User Portal from the Management Portal Home Page (`HealthShare` > `User Portal`). Note that the widgets on each dashboard exclude patients who do not have any age data.

You can also use the `BuildCubesAsBGJob()` method to build all cubes that either support the dashboard or are related to cubes that support the dashboards. This command will build the cubes in the background. You might want to build the cubes due to updated data or updated valusets.

To run the `BuildCubesAsBGJob()` method, execute the following command in your analytics namespace:

```objectscript
 set sc=##class(HSAA.COVID19.Installer).BuildCubesAsBGJob()
```

To check the status of the cube build, run the following command:

```objectscript
 set sc=##class(HSAA.COVID19.Installer).BuildCubesAsBGJobStatus()
```

## [Working with the Counts Over Time Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_counts)

The `COVID-19 Tests Counts Over Time` demonstration dashboard displays information related to COVID-19 lab test counts. The dashboard displays the following four widgets:

### [COVID-19 Test Counts](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_C12575)

Pie chart displaying counts of COVID-19 test results.

<table><tr><th>Actions</th><th>&nbsp;</th></tr><tr><td>Toggle between chart and table view</td><td>Click either the chart or table icon in the upper left of the widget.</td></tr><tr><td>Create a PDF from this pivot</td><td>Click the <code>Print</code> button in the upper left of the widget.</td></tr><tr><td>Reload dashboard</td><td>Click the house icon in the upper left of the widget.</td></tr></table>

<table><tr><th>Filters</th><th>&nbsp;</th></tr><tr><td>Filtering on test results</td><td>Clicking on slices of the pie chart filters data in all of the other three widgets in this dashboard. For example, clicking on the positive test results slice will filter out any non-positive data from the other three widgets</td></tr><tr><td>Filtering on lab test result date range</td><td><p>Clicking on the magnifying glass icon at the top of the widget displays a calendar so that users can specify dates. This filter also applies to all widgets on the dashboard.</p><p>To select a range of dates, hold down the Ctrl key and click each date that you want to include or exclude. You should avoid using the Shift key, which can cause an error.</p></td></tr></table>

### [COVID-19 Test Counts Over Time](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_C12580)

COVID-19 test results displayed over time in a bar chart.

<table><tr><th>Actions</th><th>&nbsp;</th></tr><tr><td>Toggle between chart and table view</td><td>Click either the chart or table icon in the upper left of the widget.</td></tr><tr><td>Create a PDF from this pivot</td><td>Click the <code>Print</code> button in the upper left of the widget.</td></tr></table>

<table><tr><th>Filters</th><th>&nbsp;</th></tr><tr><td><code>All Time By Year</code></td><td>Filters this widget to display test counts for each year where COVID-19 lab tests have been performed.</td></tr><tr><td><code>Since 2019 By Month</code></td><td>Filters this widget to display test counts for each month since January 1st, 2019 in which COVID-19 lab tests have been performed.</td></tr><tr><td><code>Select then Show Last N Days</code></td><td>Dropdown menu that contains a list of selectable days for use with the <code>Show Last N Days</code> button.</td></tr><tr><td><code>Show Last N Days</code></td><td>Filters this widget to display test counts for the last N days, where N is the number of days chosen in the <code>Select then Show Last N Days</code> dropdown.</td></tr></table>

### [COVID-19 Tests by Age and Gender](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_C12585)

Counts of COVID-19 tests displayed by the age and/or gender of the patients that had the tests in a bar chart. Excludes patients that do not have any age data.

<table><tr><th>Actions</th><th>&nbsp;</th></tr><tr><td>Toggle between chart and table view</td><td>Click either the chart or table icon in the upper left of the widget.</td></tr><tr><td>Create a PDF from this pivot</td><td>Click the <code>Print</code> button in the upper left of the widget.</td></tr></table>

<table><tr><th>Filters</th><th>&nbsp;</th></tr><tr><td><code>By Age Group &amp; Gender</code></td><td>Filters this widget to display COVID-19 test counts by age group and gender. Excludes patients with no gender data.</td></tr><tr><td><code>By Age Group</code></td><td>Filters this widget to display COVID-19 test counts by age group.</td></tr><tr><td><code>By Gender</code></td><td>Filters this widget to display COVID-19 test counts by gender. Excludes patients with no gender data.</td></tr></table>

### [COVID-19 Lab Test Details (Top 100)](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_C12589)

Table displaying the first 100 COVID-19 lab test details ordered by patient HSAAID.

<table><tr><th>Actions</th><th>&nbsp;</th></tr><tr><td>Create a PDF from this pivot</td><td>Click the <code>Print</code> button in the upper left of the widget.</td></tr><tr><td>Export table to Excel</td><td>Click the Export button in the upper left of the widget to export the <code>Patient Lab Test Order Details</code> table. All records, not just the first 100, are included.</td></tr></table>

Selecting individual bars in the `COVID-19 Test Counts Over Time` widget filters the `COVID-19 Test Counts by Age and Gender` and `Patient Lab Test Order Details` widgets to display data only for the selected time frame. Additionally, the `Patient Lab Test Order Details` widget is further filtered to display only COVID-19 lab tests for patients who have had COVID-19 tests performed, as opposed to all lab tests for those patients.

## [Working with the Risk Model Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_risk)

The `COVID-19 Risk Model` demonstration dashboard displays information related to patient risk scores that are not validated and are for illustrative purposes only. These risk scores show how Health Insight data can be used to calculate a patient’s risk for developing severe complications after contracting COVID-19. The dashboard displays the following four widgets:

### [Patient Count with COVID-19 Risk Scores](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_C12596)

Donut chart displaying counts of patients in different risk score categories.

<table><tr><th>Actions</th><th>&nbsp;</th></tr><tr><td>Toggle between chart and table view</td><td>Click either the chart or table icon in the upper left of the widget.</td></tr><tr><td>Create a PDF from this pivot</td><td>Click the <code>Print</code> button in the upper left of the widget.</td></tr><tr><td>Export table to Excel</td><td>Click the <code>Export</code> button in the upper left of the widget.</td></tr><tr><td>Reload dashboard</td><td>Click the house icon in the upper left of the widget.</td></tr></table>

<table><tr><th>Filters</th><th>&nbsp;</th></tr><tr><td><code>Patient Demographics</code></td><td>You can filter the counts or patients shown in the <code>Patient Demographics</code> widget of this dashboard by clicking on specific segments of the donut chart or pivot table.</td></tr></table>

### [COVID-19 Risk Scores by Location](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_C12601)

Sortable bar chart displaying the percentages of patients with certain risk scores in states and cities.

<table><tr><th>Actions</th><th>&nbsp;</th></tr><tr><td>Toggle between chart and table view</td><td>Click either the chart or table icon in the upper left of the widget.</td></tr><tr><td>Create a PDF from this pivot</td><td>Click the <code>Print</code> button in the upper left of the widget.</td></tr><tr><td>Export table to Excel</td><td>Click the <code>Export</code> button in the upper left of the widget.</td></tr></table>

<table><tr><th>Filters</th><th>&nbsp;</th></tr><tr><td><code>Sort Location By Risk Score</code> dropdown</td><td>You can choose to sort this widget by state or city and by risk score. For example, choosing <code>Sort State by Risk Score 2</code> will display data for states, with the displayed states sorted in descending order for percentages of patients with risk scores of 2. In this case, the state with the highest percentage of patients with risk score 2 would be listed first, followed by the state with the second highest percentage of patients with risk score 2, and so on.</td></tr><tr><td><code>Top Location Count</code> dropdown</td><td>You can use this dropdown to choose the number of locations to display.</td></tr></table>

### [COVID-19 Risk Scores by Age Group or Gender](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_C12606)

COVID-19 risk score counts by age group or gender.

<table><tr><th>Actions</th><th>&nbsp;</th></tr><tr><td>Toggle between chart and table view</td><td>Click either the chart or table icon in the upper left of the widget.</td></tr><tr><td>Create a PDF from this pivot</td><td>Click the <code>Print</code> button in the upper left of the widget.</td></tr><tr><td>Export table to Excel</td><td>Click the <code>Export</code> button in the upper left of the widget.</td></tr></table>

<table><tr><th>Filters</th><th>&nbsp;</th></tr><tr><td><code>By Age Group</code></td><td>Filters this widget to display COVID-19 risk score counts by age group.</td></tr><tr><td><code>By Gender</code></td><td>Filters this widget to display COVID-19 risk score counts by gender. When this filter is applied, this widget excludes patients that do not have any gender data.</td></tr></table>

### [Patient Demographics](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_C12611)

Demographic details of the patients with risk score calculated.

<table><tr><th>Actions</th><th>&nbsp;</th></tr><tr><td>Create a PDF from this pivot</td><td>Click the <code>Print</code> button in the upper left of the widget.</td></tr><tr><td>Export table to Excel</td><td>Click the <code>Export</code> button in the upper left of the widget.</td></tr></table>

<table><tr><th>Filters</th><th>&nbsp;</th></tr><tr><td><code>Has an Appointment in 30 Days</code></td><td>Filters this widget to display patients who either do or do not have an appointment scheduled in the next 30 days.</td></tr><tr><td><code>Toggle Count/Listing</code></td><td>Control that toggles the widget to display either a count of patients with COVID-19 risk scores or a detail listing for those patients.</td></tr><tr><td><code>Add Patient to Cohort</code></td><td>Action that adds any selected patient or patients to a cohort that is defined and registered in the Cohort Registry.</td></tr><tr><td><code>Assign to Care Manager</code></td><td>Action that adds any selected patient or patients to a care manager defined in the system.</td></tr><tr><td><code>View Patient Record</code></td><td>Action that displays the detailed record for a selected patient using the Clinical Viewer.</td></tr></table>

### [Risk Model Details](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_risk_model)

This section describes the example COVID-19 risk model used in the `COVID-19 Risk Model` dashboard. In this specific model, a patient’s risk score for developing severe COVID-19 symptoms is calculated by summing risk scores for four different factors that can increase a patient’s risk for developing more severe symptoms. The four factors considered in this model are a patient’s admission reasons, comorbidities, age, and observations. For each of these factors, patients will have risk scores of either 0 or 1, so a patient’s overall risk score can range from 0 to 4.

For example, a patient with a high-risk admission reason in their Encounter data in the past 14 days would have a score of 1 for their admission reasons risk score. The system determines which admission reasons are high-risk by comparing the patient’s admission reasons with a set of predefined high-risk admission reasons listed in the `HSAA_COVID19.ValueSets` table.

The following table describes each risk factor and the categories in the `HSAA_COVID19.ValueSets` table that they are associated with:

#### [Risk Model Details](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_risk_details_table)

<table><tr><th>Risk Factor</th><th>How the Risk Score is Calculated</th><th>Associated <code>HSAA_COVID19.ValueSets</code> Categories</th></tr><tr><td>Admission reasons</td><td><p>Determine if a patient has any of the following high-risk admission reasons for encounters within the past 14 days:</p><ul><li><p>Cough and/or fever</p></li><li><p>Shortness of breath</p></li><li><p>Dyspnea, abnormality of breathing, or difficulty breathing</p></li></ul><p>The system does this by comparing the patient’s admission reason codes with the ones listed in the associated <code>HSAA_COVID19.ValueSets</code> category. If no match is found, the system also searches the admission reason’s description for the following keywords:</p><ul><li><p>Fever</p></li><li><p>Cough</p></li><li><p>Dyspnea</p></li></ul><p>If the patient’s admission reason codes and coding standards match ones listed in the associated value set category, or if their admission reason description contains the above keywords (case insensitive), their risk score for this risk factor is 1.</p></td><td><code>COVID-19-Like Illness Value Set</code></td></tr><tr><td>Comorbidities</td><td><p>Determine if a patient has any of the following high-risk comorbidities:</p><ul><li><p>Angina Pectoris</p></li><li><p>Asthma</p></li><li><p>COPD</p></li><li><p>Myocardial Infarction</p></li><li><p>Pulmonary disease</p></li></ul><p>The system does this by comparing the patient’s comorbidities with the ones listed in the associated <code>HSAA_COVID19.ValueSets</code> category.</p><p>If a patient has any of the above comorbidities, their risk score for this risk factor is 1.</p></td><td><code>COVID-19 High Risk Comorbidity Value Set</code></td></tr><tr><td>Age</td><td>Determine if a patient is older than 60. If they are, their risk score for this risk factor is 1.</td><td>N/A</td></tr><tr><td>Observations</td><td><p>Determine if a patient has had any of the following high-risk observations for encounters within the past 14 days:</p><ul><li><p>Body temperature &gt; 100.4 ºF</p></li><li><p>O2 saturation &lt; 93%</p></li><li><p>Respiration rate &gt; 22 per minute</p></li></ul><p>The system does this by comparing the patient’s observations with the ones listed in the associated <code>HSAA_COVID19.ValueSets</code> categories.</p><p>If a patient has any of the above observations, their risk score for this risk factor is 1.</p></td><td><ul><li><p><code>Vital Signs - Body Temperature - Value Set</code></p></li><li><p><code>Vital Signs - O2 Saturation - Value Set</code></p></li><li><p><code>Vital Signs - Respiration Rate - Value Set</code></p></li></ul></td></tr></table>

## [Working with the Syndromic Surveillance Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_surveillance)

The `COVID-19 Syndromic Surveillance` demonstration dashboard compares hospitalization and ED visit data across different years to help track trends for COVID-19–related syndromes in patient population data.

The dashboard displays the following four widgets:

### [Syndromic Surveillance: Total ED Visits](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_C12621)

Column chart comparing total ED visits among selected years.

<table><tr><th>Actions</th><th>&nbsp;</th></tr><tr><td>Toggle between chart and table view</td><td>Click either the chart or table icon in the upper left of the widget.</td></tr><tr><td>Create a PDF from this pivot</td><td>Click the <code>Print</code> button in the upper left of the widget.</td></tr><tr><td>Export table to Excel</td><td>Click the <code>Export</code> button in the upper left of the widget.</td></tr></table>

<table><tr><th>Filters</th><th>&nbsp;</th></tr><tr><td><code>Surveillance Year (Apply to all widgets)</code></td><td>Filter that specifies a range of years to display data for. The chosen range applies to all widgets on the dashboard.</td></tr><tr><td><code>By Age Group</code></td><td>Filters this widget to display ED visits by age group.</td></tr><tr><td><code>By Facility (Top 10)</code></td><td>Filters this widget to display ED visits by the 10 facilities with the most ED visits.</td></tr></table>

### [Syndromic Surveillance: Total Hospitalization](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_C12626)

Column chart comparing total hospitalizations among selected years.

<table><tr><th>Actions</th><th>&nbsp;</th></tr><tr><td>Toggle between chart and table view</td><td>Click either the chart or table icon in the upper left of the widget.</td></tr><tr><td>Create a PDF from this pivot</td><td>Click the <code>Print</code> button in the upper left of the widget.</td></tr><tr><td>Export table to Excel</td><td>Click the <code>Export</code> button in the upper left of the widget.</td></tr></table>

<table><tr><th>Filters</th><th>&nbsp;</th></tr><tr><td><code>By Age Group</code></td><td>Filters this widget to display hospitalizations by age group.</td></tr><tr><td><code>By Facility (Top 10)</code></td><td>Filters this widget to display hospitalizations by the 10 facilities with the most hospitalizations.</td></tr></table>

### [Syndromic Surveillance: % ED Visits](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_C12631)

Line chart displaying the percentage of ED visits that are due to COVID-like illnesses or pneumonia among selected years.

<table><tr><th>Actions</th><th>&nbsp;</th></tr><tr><td>Toggle between chart and table view</td><td>Click either the chart or table icon in the upper left of the widget.</td></tr><tr><td>Create a PDF from this pivot</td><td>Click the <code>Print</code> button in the upper left of the widget.</td></tr><tr><td>Export table to Excel</td><td>Click the <code>Export</code> button in the upper left of the widget.</td></tr></table>

<table><tr><th>Filters</th><th>&nbsp;</th></tr><tr><td><code>COVID-Like Illness</code></td><td>Filters this widget to display the percentage of ED visits that are due to COVID-like illness.</td></tr><tr><td><code>Pneumonia</code></td><td>Filters this widget to display the percentage of ED visits that are due to pneumonia.</td></tr></table>

### [Syndromic Surveillance: % Hospitalization](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_C12636)

Line chart displaying the percentage of hospitalizations that are due to COVID-like illnesses or pneumonia among selected years.

<table><tr><th>Actions</th><th>&nbsp;</th></tr><tr><td>Toggle between chart and table view</td><td>Click either the chart or table icon in the upper left of the widget.</td></tr><tr><td>Create a PDF from this pivot</td><td>Click the <code>Print</code> button in the upper left of the widget.</td></tr><tr><td>Export table to Excel</td><td>Click the <code>Export</code> button in the upper left of the widget.</td></tr></table>

<table><tr><th>Filters</th><th>&nbsp;</th></tr><tr><td><code>COVID-Like Illness</code></td><td>Filters this widget to display the percentage of hospitalizations that are due to COVID-like illness.</td></tr><tr><td><code>Pneumonia</code></td><td>Filters this widget to display the percentage of hospitalizations that are due to pneumonia.</td></tr></table>

The `COVID-19 Syndromic Surveillance` dashboard displays ED and hospital visits with COVID-Like Illness (CLI) or with pneumonia. Patient visits with Encounter Admit Reason codes that correspond to fever, shortness of breath, or dyspnea are counted in the CLI display. Visits with an Encounter Admit Diagnosis of pneumonia are counted in the pneumonia display. Tracking the occurrence over time of patient visits involving CLI symptoms or pneumonia can provide evidence for potential or ongoing COVID-19 outbreaks.

The system categorizes ED visits and hospitalizations under the CLI syndrome or the Pneumonia syndrome by examining data in the Health Insight relational tables for Encounter, Diagnosis, and Problem. If an Encounter Admit Reason’s code and coding standard matches one of the entries under the `COVID-19-Like Illness Value Set` Category in the `HSAA.COVID19.ValueSet` table, the corresponding ED visit or hospitalization is categorized as being due to a COVID-like illness. The system also performs a case-insensitive search in the Encounter Admit Reason’s description for the keywords `fever`, `cough`, and `dyspnea` — if one of these keywords is present in the description, then the corresponding ED visit or hospitalization is categorized as being due to a COVID-like illness.

Similarly, if a Diagnosis code and coding standard matches one of the pneumonia codes under the `Pneumonia Value Set` category in the `HSAA.COVID19.ValueSet` table, the corresponding ED visit or hospitalization is categorized as being due to pneumonia. If no match is found, the system also searches the descriptions of Encounters, Diagnoses, and Problems. If the keyword `pneumonia` shows up in these descriptions, then the corresponding ED visit or hospitalization is categorized as being due to pneumonia. Note that text matching as a filter has certain known limitations. These dashboards are for illustrative purposes only.

The following Encounter Admit Reasons have corresponding codes in the `COVID-19-Like Illness Value Set` Category and are therefore part of the COVID-Like Illness syndrome:

*   Fever and/or cough
    
*   Shortness of breath
    
*   Dyspnea, abnormality of breathing, or difficulty breathing
    

For example, if a patient were hospitalized with an Encounter Admit Reason of fever and/or cough, that hospitalization would register as being due to a COVID-like illness on the `COVID-19 Syndromic Surveillance` dashboard.

If you want to add more symptoms and codes to the CLI and Pneumonia syndromes, you can add entries to the `COVID-19-Like Illness Value Set` and `Pneumonia Value Set` categories in the `HSAA.COVID19.ValueSet` table, as described in [the following section](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_valueset).

## [Customizing the COVID-19 Value Set](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_valueset)

The initial `HSAA_COVID19.ValueSets` demonstration data provided with Health Insight contains codes, coding standards, and other information that support COVID-19–related cube queries. InterSystems strongly recommends that you review and update the value sets data with different values to suit your organization’s needs. For example, you may want to add more conditions that place COVID-19 patients at higher risk of developing severe complications. There are two options for updating the `HSAA_COVID19.ValueSets` data, as described below.

InterSystems recommends that you do not modify the Category field for any existing rows of the COVID-19 Value Set table, as the COVID-19 dashboards rely on the presence of the Category fields to function correctly. If you wish to modify the COVID-19 Value Set and the existing cube queries to meet the needs of your specific COVID-19 Dashboards, you should instead add more entries under the preexisting Categories with different CodingStandard or Code fields. For example, you might add a new row in the table with the preexisting Category of `COVID-19 Lab Test Value Set`, with new CodingStandard and Code fields. The initial value set data contains a sample row with placeholder values:

```
COVID-19 Lab Test Value Set,CustomerCodingStandard,CustomerCode,Customer COVID-19 lab test code
```

Deletions to the COVID-19 Value Sets table are not supported at this time. If you delete preexisting entries in the COVID-19 Value Set, those entries will be restored upon upgrade. However, any updates to rows or additions to rows in the Value Sets table will persist through upgrades.

### [Individual Updates Through SQL](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_valueset_sql)

You can update the COVID–19 Value Sets via `INSERT` or `UPDATE` statements made in the SQL Explorer. To do so, do the following:

1.  Navigate to your Analytics namespace.
    
2.  Navigate to the SQL Explorer via the Management Portal (`System Explorer` > `SQL`).
    
3.  Click on the `Execute Query` tab and enter an `INSERT` or `UPDATE` like the following:
    
    ```sql
    INSERT INTO HSAA_COVID19.ValueSets VALUES ('NewCategory', 'NewCodingStandard', 'NewCode', 'NewDescription')
    ```
    
    You should replace the values, such as `'NewCode'` above with the categories, coding standards, codes, and descriptions that you want to insert into the COVID-19 Value Sets table.
    

### [Batch Updates via CSV File](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_valueset_batch)

You can update the COVID-19 Value Sets by editing the `covid-19–valuesets.csv` file, which is typically located at `install-dir/csp/hsaalib/covid19`, where `install-dir` is the installation directory of your Health Insight instance. After making your edits:

1.  [Make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write).
    
2.  Run a command like the following in the `HSAALIB` namespace:
    
    ```
    do ##class(HSAA.COVID19.ValueSets).ImportOrUpdateValueSets(
                                                  "covid-19-valuesets.csv-file-full-path",
                                                  "analytics-namespace-name")
    ```
    
    ...where `covid-19-valuesets.csv-file-full-path` is the file path where the `covid-19–valuesets.csv` is located, and `analytics-namespace-name` is your Analytics namespace.
    
3.  Return HSAALIB to read-only by following the procedure to [make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write), but select the `Mount Read-Only` option instead of clearing it.
    

## [Modifying an Example COVID-19 Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_dashboard#HSAAADM_dashboard_customize)

The COVID-19 examples included in Health Insight are intended to show how Health Insight is used to explore, analyze, and report on COVID-19–related data. These dashboards can be copied, edited, or extended to fit the needs of your organization. As an example, you might make the following change in order to modify the `COVID-19 Test Counts` widget on the `COVID-19 Tests Counts Over Time` dashboard from a pie chart to a bar chart:

1.  Navigate to the `COVID-19 Tests Counts Over Time` dashboard (`HealthShare` > `User Portal` > `COVID-19 Test Counts Over Time`).
    
2.  Expand the `Dashboard Editor` by clicking the arrow on the left side of the screen.
    
3.  Click `Widgets`, then click `COVID-19 Test Counts`.
    
4.  Click `Type & Data Source`.
    
5.  For `Widget Type`, select `Bar Chart`.
    

This procedure modifies the `COVID-19 Test Counts` widget to display a bar chart instead of a pie chart. You might choose to make more significant changes, such as by adding new dimensions to certain cubes, by defining new class methods for supporting these new dimensions, or by creating new pivot tables and widgets.

For more information on dashboard customization options, see the [Business Intelligence documentation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2GS_ch_intro).
