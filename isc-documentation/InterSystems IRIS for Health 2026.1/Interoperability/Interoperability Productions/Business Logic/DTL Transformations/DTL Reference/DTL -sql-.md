# DTL <sql>

Executes an embedded SQL SELECT statement within a data transformation, within a DTL transformation.

## Syntax

```
<sql>
   <![CDATA[
      SELECT SSN INTO :context.SSN
      FROM MyApp.PatientTable
      WHERE PatID = :request.PatID ]]>
 </sql>
```

## Elements

<table><tr><th>Element</th><th>Purpose</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_annotation">&lt;annotation&gt;</a></td><td>Optional. A text string that describes the &lt;sql&gt; element.</td></tr></table>

## Description

The DTL <sql> element executes an arbitrary embedded SQL SELECT statement from within a DTL <transform> element.

To use the <sql> element effectively, keep the following tips in mind:

*   Always use the fully qualified name of the table, including both the SQL schema name and table name, as in:
    
    `MyApp.PatientTable`
    
    Where `MyApp` is the SQL schema name and `PatientTable` is the table name.
    
*   The contents of the <sql> element must contain a valid embedded SQL SELECT statement.
    
    It is convenient to place the SQL query within a CDATA block so that you do not have to worry about escaping special XML characters.
    
*   Any tables listed in the SQL query’s FROM clause must either be stored within the local InterSystems IRIS database or linked to an external relational database using the SQL Gateway.
    
*   Within the INTO and WHERE clauses of the SQL query, you can refer to a property of the source or target object by placing a : (colon) in front of the variable name. For example:
    
    ```xml
    <sql><![CDATA[
      SELECT Name INTO :target.Name
      FROM MainFrame.EmployeeRecord
      WHERE SSN = :source.SSN AND City = :source.Home.City
    ]]>
    </sql>
    ```
    
*   Only the first row returned by the query will be used. Make sure that your WHERE clause correctly specifies the desired row.
