# [Managing Analytics Query Definitions in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs)

This chapter describes how to create, modify, and delete an analytics query definition. An analytics query definition is a reusable query that can deliver clinical messages or assign patients to cohorts.

## [How Analytics Queries Are Used in Unified Care Record](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_intro)

An analytics query definition is a reusable definition that queries data in your analytics instance. While query definitions are stored in the query definition registry on the Registry instance in your federation, you define them from the analytics instance in your federation. These analytics queries can be used by HealthShare Unified Care Record in two ways:

### [Clinical Message Delivery](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_C11530)

Unified Care Record can deliver clinical messages to subscribers using a variety of formats and delivery methods. [Clinical message delivery](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEPUSH) is based on subscriptions. Whenever new data arrives for a patient, Unified Care Record examines the data to see if triggers a relevant subscription and if so, creates and sends messages to the subscribers. To examine the data, Unified Care Record uses filters of various kinds. One kind of filter is an [analytics filter](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEPUSH_ch_filters#HEPUSH_filters_analytics). An analytics filter is based on an analytics query definition.

In this use case, the analytics query should select a single patient.

For additional information, refer to the Unified Care Record [Clinical Message Delivery Guide](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEPUSH).

### [Dynamic Cohorts](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_C11535)

A cohort is a group of patients that meet a particular definition based on their demographic and clinical history. With a [dynamic cohort](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEADM_ch_query_instance_registry), Unified Care Record dynamically assigns patients to the cohort based on the results of an analytics query that is run on a regular basis.

In this case, the analytics query should select a set of patients.

For additional information, see [Managing Query Instances](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEADM_ch_query_instance_registry).

### [Implementing an Analytics Query Definition](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_impl)

There are three possible ways to implement a query definition:

*   SQL queries — For this kind of query definition, you specify an SQL SELECT statement that is executed against one or more tables in your analytics namespace. This is the most common kind of query definition.
    
*   Pivot tables — For this kind of query definition, you select an existing pivot table in your analytics namespace. Internally, a pivot table is an MDX query that is executed on one or more cubes.
    
*   Custom queries — For this kind of query, you define a class that defines a custom query, typically using ObjectScript. This class must be in your analytics namespace. Custom queries are relatively rare.
    

SQL queries and custom queries can accept parameters. Currently, pivot tables cannot accept parameters.

### [Requirements for Return Values from an Analytics Query](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_returnedvals)

The requirements for return values depend upon the use case:

#### [Dynamic Cohorts](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_C11549)

If the analytics query is used to determine membership in a dynamic cohort, the query must return fields named HSAAID, AnalyticsID, MPIID, or PatientID. This is true for any [query implementation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_impl).

#### [Clinical Message Delivery](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_C11552)

If the query is to be used for clinical message delivery, there is no specific requirement about fields that must be returned. When designing the query, however, it is important to consider any result filters with which the query might be used. See [Managing Query Instances](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEADM_ch_query_instance_registry) for more details.

In both cases, it is important to consider query performance.

## [Accessing the Query Definition Registry](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_registry)

To access the query definition registry, do the following on your analytics instance:

1.  Open the Management Portal.
    
2.  Switch to your analytics namespace, typically `ANALYTICS`.
    
3.  Select `HealthShare`.
    
4.  Select `Query Definition Registry`.
    

The page then displays a table of any existing query definitions. Here you can create new definitions, edit existing definitions, and remove existing definitions.

> **Note:**
> 
> If you instead receive an error message, make sure that the registry instance and the registry production are both running.

The `Parameters` tab displays parameters defined in the query (except for pivot tables which do not currently support parameters). You can specify additional information about the parameters; see the next section.

The `Headers` tab displays a generated list of column headers. For a pivot table, this can also display row headers. Note that for a pivot table without a detail listing, this information is determined at runtime from the data and thus can be different between executions of the pivot table. If the pivot table definition changes, it is necessary to click `Redefine` and then resave the query definition.

The following sections provide details on these tasks.

## [Creating an Analytics Query Definition](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_creating)

To create a query definition:

1.  Access the query definition registry as described [earlier](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_registry).
    
2.  Select `Add Query`.
    
3.  Specify the following details:
    
    *   `Name` — Unique name for this query definition.
        
    *   `Description` — Description of this query definition, for display in other user interfaces. This description should explain any parameters of the query, as well as any other details needed to use the query.
        
    *   `Mode` — Select the kind of query. Select `SQL Query`, `MDX Pivot`, or `Custom`, depending on the kind of query to use.
        
    *   `SQL Query` (if `Mode` is `SQL Query`) — Enter the SQL SELECT statement. See “[Details for SQL Queries](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_sql).”
        
    *   `Pivot` (if `Mode` is `MDX Pivot`) — Select a pivot table. If this query is for use with a dynamic cohort, select a pivot table that has been saved as a detail listing. This detail listing must include fields named HSAAID, AnalyticsID, MPIID, or PatientID. If this query is for use with Advanced Clinical Notifications, it can be a pivot table saved as a listing (more common) or a regular pivot table.
        
    *   `Class` (if `Mode` is `Custom`) — Select the class that defines the custom query. See “[Details for Custom Queries](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_custom).” Note that custom queries are rare.
        
4.  If you specified a query that uses parameters, specify details for these parameters as follows:
    
    1.  Select the `Headers` tab and then select the `Parameters` tab.
        
        Notice that this tab now displays one row for each parameter.
        
    2.  Select the gear icon next to the first parameter.
        
        This displays a dialog box where you can specify information about this parameter.
        
    3.  For `Label`, specify a label to use rather than the parameter name, if wanted.
        
    4.  For `Type`, select the data type of this parameter. Other user interfaces use the type to validate parameter values.
        
    5.  For `Description`, type information to display in other user interfaces (as a tooltip). Include any information needed to use this parameter appropriately.
        
    6.  Select `OK`.
        
    7.  Repeat the preceding steps as needed for each additional parameter.
        
5.  Select `Save`.
    

> **Important:**
> 
> Be sure to specify `Description` for the query and for any parameters, for display in other user interfaces.

## [Details for Analytics SQL Queries](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_sql)

For an analytics query definition, if the definition uses SQL, the definition must be an SQL SELECT statement. You can use the analytics source tables (which are in the `HSAA` schema) or you can use the generated fact and dimension tables (which are in the schemas that have names like `HSAA_AllergyCube`). The latter tables contain the actual data seen in the analytics cubes. You could also use your tables, if applicable.

> **Tip:**
> 
> The Management Portal provides web pages that you can use to test SQL statements and build SQL queries. To access these pages, go to the [analytics home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_home_page) and then click `SQL Explorer`. Note that you cannot test query parameters in these pages.

### [Using Standard Parameters in an Analytics SQL Query](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_sql_stdparm)

Unified Care Record automatically specifies values for the following parameters, which you can use in your SELECT statement:

*   `MPIID` — Contains the patient MPI ID.
    
*   `HSAAID` — Contains the patient ID used within HealthShare Health Insight.
    
*   `Context` — Contains context information with values from the inbound message. This parameter is a [$ListBuild](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=RCOS_flistbuild) structure of the context values (to be specified in the push filter). For example, these values might include insurer, medication codes, or lab result values.
    

The query definition registry does not display these parameters.

### [Defining Additional Parameters in an Analytics SQL Query](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_sql_extraparm)

To include a custom parameter in the query, include a variable name, preceded with a colon. The variable name must be a valid SQL identifier. For example, suppose that you use the following SQL statement:

```
SELECT MPIID FROM HSAA.Patient WHERE age=:ageparameter
```

In this case, the query definition registry would display one parameter for the query: a parameter named `ageparameter`.

## [Details for Custom Analytics Queries](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_custom)

For an analytics query definition based on a custom query, use [your IDE](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides) to create and compile a class definition in your analytics namespace. This class must extend the class [HSAA.Query.Handler](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Query.Handler) and must implement a specific set of instance methods, described [below](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_custom_meths). [HSAA.Query.Handler](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Query.Handler) provides a mechanism you can use to easily include parameters in your query, also described [below](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_custom_parms).

Note that this custom query mechanism is similar to the more generic custom query mechanism in ObjectScript; for background, see “[Defining Custom Class Queries](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GOBJ_queries_userqueries)” in Defining and Using Classes. To run the query, Unified Care Record does the following:

1.  Creates an instance of your custom class.
    
2.  Invokes the `Prepare()` method of that instance.
    
3.  Invokes the `Execute()` method of that instance.
    
4.  Invokes the `Fetch()` method, once per row.
    
5.  Invokes the `Close()` method.
    

The mechanism works by passing an instance of [HS.Types.Analytics.QueryDefinition](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Types.Analytics.QueryDefinition) from one step to the next. Unified Care Record initializes the instance of [HS.Types.Analytics.QueryDefinition](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Types.Analytics.QueryDefinition) and your methods can set or get values of it.

For an example, see the class [HSAA.Query.Test.ObjectScript](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Query.Test.ObjectScript).

### [Implementing the Required Methods in a Custom Analytics Query](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_custom_meths)

The custom query class must implement the following methods:

#### [Prepare()](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_C11652)

```
Method Prepare(pQuery As HS.Types.Analytics.QueryDefinition) As %Status
```

`pQuery` is an instance of [HS.Types.Analytics.QueryDefinition](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Types.Analytics.QueryDefinition); this argument holds the query definition. The `Prepare()` method must perform any one-time setup steps, such as initializing the query definition. In the following example, this method defines the column headers:

```
Method Prepare(pQuery As HS.Types.Analytics.QueryDefinition) As %Status
{
    $$$QuitOnError(pQuery.ColumnHeaders.Insert(##class(HS.Types.Grid.Axis).%New("Company")))
    $$$QuitOnError(pQuery.ColumnHeaders.Insert(##class(HS.Types.Grid.Axis).%New("Mission")))
    $$$QuitOnError(pQuery.ColumnHeaders.Insert(##class(HS.Types.Grid.Axis).%New("Mission")))
    $$$QuitOnError(pQuery.ColumnHeaders.Insert(##class(HS.Types.Grid.Axis).%New("City","%String")))
    $$$QuitOnError(pQuery.ColumnHeaders.Insert(##class(HS.Types.Grid.Axis).%New("Employees","%Integer")))
    Quit ##super(pQuery)
}
```

If the query uses any parameters, this method can define them. The easiest way to do that is to call the `Prepare()` method of the superclass as shown in the last line of the above; see “[Defining Query Parameters](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_custom_parms),” later in this section.

For more options, see the class reference for [HS.Types.Analytics.QueryDefinition](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Types.Analytics.QueryDefinition).

#### [Execute()](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_C11656)

```
Method Execute(pQuery As HS.Types.Analytics.QueryDefinition) As %Status
```

This method executes the query. This method must contain any logic that is needed before fetching rows.

#### [Fetch()](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_C11663)

```
Method Fetch(Output pRow As %List = "", Output pAtEnd As %Boolean = 0) As %Status
```

This method fetches a row and indicates whether the last row has been reached. `pRow` is a [%List](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&CLASSNAME=%25Library.List) that contains the data for a row.

[%List](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&CLASSNAME=%25Library.List) is the class that corresponds to the [$LISTBUILD](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=RCOS_flistbuild) structure. That is, to create such a list, use the $LISTBUILD function. For example, to create a row that consists of string values, you could do this:

```
 Set pRow = $LISTBUILD("value a","value b","value c")
```

The method should set the variable `pAtEnd` to 1 if the last row has been reached, or 0 if the last row has not been reached.

#### [Close()](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_C11667)

```
Method Close() As %Status
```

This method contains any logic needed to clean up after fetching all the rows.

### [Values Available in a Custom Analytics Query](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_custom_stdparm)

Unified Care Record automatically passes a set of values to a custom query. To do this, Unified Care Record specifies values for the following properties of the instance of [HS.Types.Analytics.QueryDefinition](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Types.Analytics.QueryDefinition), which you can use in your methods:

*   `MPIID` — Contains the patient MPI ID.
    
*   `HSAAID` — Contains the patient ID used within Health Insight.
    
*   `Context` — Contains context information with values from the inbound message. This value is a list of strings.
    

### [Defining Query Parameters in a Custom Analytics Query](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_custom_parms)

To define custom parameters in the query, do the following:

*   Define one class property for each desired parameter, using the name that you want the parameter to have. For example, to add a parameter named `Companies`, add a property named `Companies`.
    
    Optionally specify [InitialExpression](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ROBJ_property_initialexpression) for each property.
    
*   Within the `Prepare()` method of your class, invoke the `Prepare()` method of the superclass. This step sets initial values for the properties of the instance of [HS.Types.Analytics.QueryDefinition](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Types.Analytics.QueryDefinition).
    
*   Within the `Execute()` and `Fetch()` methods, set or get values of these properties as needed.
    
*   Specify the `PARAMETERS` parameter of the query class. For its value, specify a comma-separated list of the parameter names.
    
    This step advertises the availability of the query parameters. Specifically, the query definition registry uses the contents of the `PARAMETERS` parameter to determine what the query parameters are.
    

## [Modifying an Analytics Query Definition](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_modifying)

To modify a query definition:

1.  Access the query definition registry as described [earlier](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_registry).
    
2.  Select the query.
    
3.  Edit details as needed.
    
4.  If the query uses a pivot table, and the definition of that pivot table has changed, click `Redefine`. This step updates the information on the `Headers` tab.
    
5.  Select `Save`.
    

## [Deleting an Analytics Query Definition](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_deleting)

To delete a query definition:

1.  Access the query definition registry as described [earlier](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs#HSAA_qdefs_registry).
    
2.  Select the query.
    
3.  Select `Delete`.
    
    The query definition is deleted immediately.
