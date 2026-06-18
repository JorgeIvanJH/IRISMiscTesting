# [Orientation to the Health Insight Dashboards and Pivot Tables](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_dborient#HSAA_dborient)

HealthShare Health Insight provides a set of dashboards and pivot tables that you can provide to your customers or instead copy and modify. This chapter explains how to access these samples and how to see their implementation details.

## [Accessing the Health Insight Dashboards](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_dborient#HSAA_dborient_db_accessing)

To access the Health Insight dashboards:

1.  Display the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_home_page).
    
2.  Click `User Portal`.
    
    The system then displays the User Portal, which lists the dashboards visible to you in this namespace.
    
    By default, the User Portal displays items in Covers view, which displays a rectangular book cover for each item. To display the items as a traditional list instead, click the `List` option.
    
3.  To open a dashboard, click its name.
    

The following shows an example dashboard (cropped, for reasons of space):

[Image: Example Dashboard showing several counts and bar charts related to patient data.]

### [Providing Dashboards to Your Users](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_dborient#HSAA_db_deploying)

You can enable your users to access the dashboards in any of the following ways:

*   Give the users access to the User Portal.
    
    Note that users can access the User Portal from the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_home_page).
    
*   Provide direct links to the dashboards.
    
    For details, see the chapter “[Accessing Dashboards from Your Application](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2IMP_ch_dashboards)” in [Implementing InterSystems IRIS Business Intelligence](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2IMP).
    
    Note that the form of the URL is slightly different for Health Insight. Specifically, instead of `/csp/namespace`, you must use `/csp/healthshare/namespace`
    
*   Embed the dashboards in inline frames (`<iframe>`) in Zen pages or other web pages.
    
    For details, see the chapter “[Accessing Dashboards from Your Application](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2IMP_ch_dashboards)” in [Implementing InterSystems IRIS Business Intelligence](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2IMP).
    

## [Viewing the Definition of a Health Insight Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_dborient#HSAA_dborient_db_definition)

To see how a dashboard is defined:

1.  Display the dashboard.
    
2.  Click the > button to its left. The system then displays the Dashboard Editor, which contains all configuration details for the dashboard.
    
3.  Click the `Widgets` menu, which holds most of the configuration details. Then the system displays a list of the widgets on the dashboard.
    
4.  To see the details for a widget, click its name in this list.
    
5.  To see the data source for the widget, click `Type & Data Source`.
    
    On the submenu, `Widget Type` specifies the appearance of the widget, and `Data Source` specifies the data source that it should use.
    

Other submenus contain other parts of the dashboard definition. For details, see [Creating Dashboards](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2DASH). You can also see the dashboard definition in XML form in [your IDE](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides), as described in the chapter “[Introduction to Dashboards](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2DASH_ch_intro)” in that book.

## [Accessing the Health Insight Pivot Tables](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_dborient#HSAA_dborient_pivot_accessing)

To access the Health Insight pivot tables:

1.  In the Management Portal, click `Analytics`, click `Analyzer`, and then click `Go`.
    
2.  Click `Open`.
    
3.  Select the pivot table and click `OK`.
    

> **Tip:**
> 
> You can also open the Analyzer via the `Menu` in the User Portal. Also, if a pivot table is public and is visible to you, it is listed in the User Portal, from which you can open it directly.

## [Viewing the Definition of a Health Insight Pivot Table](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_dborient#HSAA_dborient_pivot_definition)

To see how a pivot table is defined, display the pivot table in the Analyzer.

The top area of the right side contains all the options that define the pivot table:

[Image: Top area of Analyzer with Rows, Colummns, Measures, and Filters boxes, as well as various buttons.]

Use these options to find parts of the definition as follows:

<table><tr><th>Option</th><th>Notes</th></tr><tr><td>or</td><td>Query Text button. Use this to see the underlying MDX query, which is generally the most important part of the pivot table. If this button looks like , the query was manually edited; in this case, disregard the <code>Rows</code>, <code>Columns</code>, <code>Measures</code>, and <code>Filters</code> boxes (and the filter bar below them).</td></tr><tr><td></td><td>Pivot Options button. Use this to see overall options such as the use of a summary line, use of titles, and so on. Note that a dashboard can define such items as well, overriding options specified here.</td></tr><tr><td></td><td>Print Options button. Use this to see how the print options are defined.</td></tr><tr><td></td><td>Conditional Formatting button. Use this to see how any conditional formatting was defined.</td></tr><tr><td>Items listed in the <code>Rows</code> box</td><td><p>The <code>Rows</code> box controls the rows in the pivot table. Note that the names shown in this box are not necessarily informative. For details on any item shown here, click the Options button ( or ). The Analyzer then displays details for that item, including its full name, as in the following example:</p><p>[Image: Partial image of the Level Options dialogue box, which allows you to configure options for the selected pivot table level]</p><p>The Analyzer displays the button if the options have been customized.</p></td></tr><tr><td>Items listed in the <code>Columns</code> and <code>Measures</code> boxes</td><td>The <code>Columns</code> and <code>Measures</code> boxes controls the columns of the pivot table. For details on any item shown here, click the Options button ( or ).</td></tr><tr><td>Items listed in the <code>Filters</code> boxes</td><td>The <code>Filters</code> box (and the filter bar) controls the overall filtering of the pivot table. For details on any item shown here, click the Options button ( or ), if available, or see the corresponding item in the filter bar.</td></tr><tr><td>Filter bar directly below the <code>Rows</code>, <code>Columns</code>, <code>Measures</code>, and <code>Filters</code> boxes</td><td>Items in this bar control how the pivot table is filtered.</td></tr></table>

You can also see the pivot definition in XML form in [your IDE](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides), as described in the chapter “[Introduction to the Analyzer](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2ANLY_ch_intro)” in [Using the Analyzer](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2ANLY).

### [Viewing Details for Items Defined in the Analyzer](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_dborient#HSAA_dborient_pivot_definition_custom_definitions)

In some cases, a pivot table might use a calculated member, calculated measure, or a named filter that was defined in the Analyzer. In such cases, when you open the pivot table in the Analyzer, the left area of the Analyzer lists this item along with the usual contents of the applicable cube. To identify any such items and see their definitions:

*   Look in the `Measures` folder for any items shown with the Calculated Item icon. These are calculated measures. To see the definition of a calculated measure, click its name and then click the Define Calculated Item button .
    
*   Also look in the `Dimensions` folder for any items shown with the Calculated Item icon. These are calculated members. To see the definition of a calculated member, click its name and then click the Define Calculated Item button .
    
*   Look for the `Named Filters` folder, which contains any named filters. To see the definition of a named filter, click its name and then click the Named Filter button .
    

In all cases, the Analyzer then displays a dialog box that shows the definition of the item. For details, see [Using the Analyzer](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2ANLY).
