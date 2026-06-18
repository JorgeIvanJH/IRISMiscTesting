# Using Dynamic SQL

This topic discusses Dynamic SQL, queries and other SQL statements that are prepared and executed at runtime from InterSystems IRIS data platform.

This topic describes Dynamic SQL programming using the %SQL.Statement class, which is the preferred implementation of Dynamic SQL. All statements about Dynamic SQL here, and throughout our documentation, refer specifically to the %SQL.Statement implementation.

## Introduction to Dynamic SQL

Dynamic SQL refers to SQL statements that are prepared and executed at runtime. In Dynamic SQL preparing and executing an SQL command are separate operations. Dynamic SQL lets you program within InterSystems IRIS in a manner similar to an ODBC or JDBC application (except that you are executing the SQL statement within the same process context as the database engine). Dynamic SQL is invoked from an ObjectScript program.

Dynamic SQL queries are prepared at program execution time, not compilation time. This means that the compiler cannot check for errors at compilation time and preprocessor macros cannot be used within Dynamic SQL. It also means that executing programs can create specialized Dynamic SQL queries in response to user or other input.

Dynamic SQL can be used to perform an SQL query. It can also be used to issue other SQL statements. The examples here perform a `SELECT` query. For Dynamic SQL program examples, see CREATE TABLE, INSERT, UPDATE, DELETE, and CALL.

Dynamic SQL is used in the execution of the InterSystems IRIS SQL Shell, the InterSystems IRIS Management Portal Execute Query interface, the SQL Code Import methods, and the Data Import and Export Utilities.

No row can exceed the string length limit.

### Dynamic SQL versus Embedded SQL

Dynamic SQL differs from Embedded SQL in the following ways:

*   Initial execution of a Dynamic SQL query is slightly less efficient than Embedded SQL, because it does not generate in-line code for queries. However, re-execution of both Dynamic SQL and Embedded SQL is substantially faster than the first execution of the query because both support cached queries.
    
*   Dynamic SQL can accept a literal value input to a query in two ways: input parameters specified using the “?” character, and input host variables (for example, :var). Embedded SQL uses input and output host variables (for example, :var).
    
*   Dynamic SQL output values are retrieved using the API of the result set object (that is, the `Data` property). Embedded SQL uses host variables (for example, :var) with the `INTO` clause of a `SELECT` statement to output values.
    
*   Dynamic SQL sets the `%SQLCODE`, `%Message`, `%ROWCOUNT`, and `%ROWID` object properties. Embedded SQL sets the corresponding SQLCODE, %msg, %ROWCOUNT, and %ROWID local variables. Dynamic SQL does not set `%ROWID` for a `SELECT` query; Embedded SQL sets %ROWID for a cursor-based `SELECT` query.
    
*   Dynamic SQL provides an easy way to find query metadata (such as quantity and names of columns).
    
*   Dynamic SQL performs SQL privilege checking by default; you must have the appropriate privileges to access or modify a table, field, etc. Embedded SQL does not perform SQL privilege checking. Refer to the SQL %CHECKPRIV statement for further details.
    
*   Dynamic SQL cannot access a private class method. To access an existing class method, the method must be made public. This is a general SQL limitation. However, Embedded SQL gets around this limitation because the Embedded SQL operation itself is a method of the same class.
    

Dynamic SQL and Embedded SQL use the same data representation (logical mode by default, but this can be changed) and NULL handling.

## The %SQL.Statement Class

The preferred interface for Dynamic SQL is the %SQL.Statement class. To prepare and execute Dynamic SQL statements, use an instance of %SQL.Statement. The result of executing a Dynamic SQL statement is an SQL statement result object that is an instance of the %SQL.StatementResult class. An SQL statement result object is either a unitary value, a result set, or a context object. In all cases, the result object supports a standard interface. Each result object initializes the `%SQLCODE`, `%Message` and other result object properties. The values these properties are set to depends on the SQL statement issued. For a successfully executed `SELECT` statement, the object is a result set (specifically, an instance of %SQL.StatementResult) and supports the expected result set functionality.

The following ObjectScript code prepares and executes a Dynamic SQL query:

```objectscript
  /* Simple %SQL.Statement example */
  set myquery = "SELECT TOP 5 Name,DOB FROM Sample.Person"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(myquery)
   if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  set rset = tStatement.%Execute()
  do rset.%Display()
  write !,"End of data"
```

The examples on this page use methods associated with the %SQL.Statement and %SQL.StatementResult classes.

## Creating an Object Instance

You can create an instance of the %SQL.Statement class using the %New() class method:

```objectscript
  set tStatement = ##class(%SQL.Statement).%New()
```

At this point the result set object is ready to prepare an SQL statement. Once you have created an instance of the %SQL.Statement class, you can use that instance to issue multiple Dynamic SQL queries and/or `INSERT`, `UPDATE`, or `DELETE` operations.

`%New()` accepts three optional comma-separated parameters in the following order:

1.  %SelectMode, which specifies the mode used for data input and data display.
    
2.  %SchemaPath, which specifies the search path used to supply the schema name for an unqualified table name.
    
3.  %Dialect, which specifies the Transact-SQL (TSQL) Sybase or MSSQL dialect. The default is IRIS (InterSystems SQL).
    

There is also an %ObjectSelectMode property, which cannot be set as a `%New()` parameter. `%ObjectSelectMode` specifies the data type binding of fields to their related object properties.

In the following ObjectScript example, the %SelectMode is 2 (Display mode), and the %SchemaPath specifies “Sample” as the default schema:

```objectscript
  set tStatement = ##class(%SQL.Statement).%New(2,"Sample")
```

In the following ObjectScript example, a %SelectMode is not specified (note the placeholder comma), and the %SchemaPath specifies a schema search path containing three schema names:

```objectscript
  set tStatement = ##class(%SQL.Statement).%New(,"MyTests,Sample,Cinema")
```

### %SelectMode Property

The %SelectMode property specifies one of the following modes: 0=Logical (the default), 1=ODBC, 2=Display. These modes specify how a data value is input and displayed. A mode is most commonly used for date and time values and for displaying %List data (a string containing an encoded list). Data is stored in Logical mode.

A `SELECT` query uses the `%SelectMode` value to determine the format used to display data.

An `INSERT` or `UPDATE` operation uses the `%SelectMode` value to determine the permitted format(s) for data input.

`%SelectMode` is used for data display. SQL statements run internally in Logical mode. For example, an `ORDER BY` clause orders records based on their Logical values, regardless of the `%SelectMode` setting. SQL functions use Logical values, regardless of the `%SelectMode` setting. Methods projected as SQLPROC also run in Logical mode. SQL routines called as functions in an SQL statement need to return the function value in Logical format.

*   For a `SELECT` query, `%SelectMode` specifies the format used for displaying the data. Setting `%SelectMode` to ODBC or Display also affects the data format used for specifying comparison predicate values. Some predicate values must be specified in the `%SelectMode` format, other predicate values must be specified in Logical format, regardless of the `%SelectMode`. For details, refer to Overview of SQL Predicates.
    
    *   Time data type data in `%SelectMode=1` (ODBC) can display fractional seconds, which is not the same as actual ODBC time. The InterSystems IRIS Time data type supports fractional seconds. The corresponding ODBC TIME data type (TIME_STRUCT standard header definition) does not support fractional seconds. The ODBC TIME data type truncates a supplied time value to whole seconds. ADO DotNet and JDBC do not have this restriction.
        
    *   %List data type data in `%SelectMode=0` (Logical) does not display the internal storage value, because %List data is encoded using non-printing characters. Instead, Dynamic SQL displays a %List data value as a $LISTBUILD statement, such as the following: `$lb("White","Green")`. See %Print() Method for an example. %List data type data in `%SelectMode=1` (ODBC) displays list elements separated by commas. %List data type data in `%SelectMode=2` (Display) displays list elements separated by `$CHAR(10,13)` (Line Feed, Carriage Return).
        
*   For an `INSERT` or `UPDATE` operation, `%SelectMode` specifies the format for input data that will be converted to Logical storage format. For this data conversion to occur, the SQL code must have been compiled with a select mode of RUNTIME (the default) so that a Display or ODBC `%SelectMode` is used when the `INSERT` or `UPDATE` is executed. For permitted input values for dates and times, refer to the date and time data types. For further details, see INSERT or UPDATE.
    

You can specify `%SelectMode` either as the first parameter of the `%New()` class method, or set it directly, as shown in the following two examples:

```objectscript
  set tStatement = ##class(%SQL.Statement).%New(2)
```

```objectscript
  set tStatement = ##class(%SQL.Statement).%New()
  set tStatement.%SelectMode=2
```

The following example returns the current value of %SelectMode:

```objectscript
  set tStatement = ##class(%SQL.Statement).%New()
  write !,"default select mode=",tStatement.%SelectMode
  set tStatement.%SelectMode=2
  write !,"set select mode=",tStatement.%SelectMode
```

You can determine the SelectMode default setting for the current process using the $SYSTEM.SQL.Util.GetOption("SelectMode") method. You can change the SelectMode default setting for the current process using the using the $SYSTEM.SQL.Util.SetOption("SelectMode",n) method, when `n` can be 0=Logical, 1=ODBC, or 2=Display. Setting %SelectMode overrides this default for the current object instance; it does not change the SelectMode process default.

For further details on SelectMode options, see Data Display Options.

### %SchemaPath Property

The %SchemaPath property specifies the search path used to supply the schema name for an unqualified table name, view name, or stored procedure name. A schema search path is used for data management operations such as `SELECT`, `CALL`, `INSERT`, and `TRUNCATE TABLE`; it is ignored by data definition operations such as `DROP TABLE`.

The search path is specified as a quoted string containing a schema name or a comma-separated series of schema names. InterSystems IRIS searches the listed schemas in left-to-right order. InterSystems IRIS searches each specified schema until it locates the first matching table, view, or stored procedure name. Because schemas are searched in the specified order, there is no detection of ambiguous table names. Only schema names in the current namespace are searched.

The schema search path can contain both literal schema names and the CURRENT_PATH, CURRENT_SCHEMA, and DEFAULT_SCHEMA keywords.

*   CURRENT_PATH specifies the current schema search path, as defined in a prior `%SchemaPath` property. This is commonly used to add schemas to the beginning or end of an existing schema search path.
    
*   CURRENT_SCHEMA specifies the current schema container class name if the %SQL.Statement call is made from within a class method. If a #sqlcompile path macro directive is defined in a class method, the CURRENT_SCHEMA is the schema mapped to the current class package. Otherwise, CURRENT_SCHEMA is the same as DEFAULT_SCHEMA.
    
*   DEFAULT_SCHEMA specifies the system-wide default schema. This keyword enables you to search the system-wide default schema as a item within the schema search path, before searching other listed schemas. The system-wide default schema is always searched after searching the schema search path if all the schemas specified in the path have been searched without a match.
    

The `%SchemaPath` is the first place InterSystems IRIS searches schemas for a matching table name. If `%SchemaPath` is not specified, or does not list a schema that contains a matching table name, InterSystems IRIS uses the system-wide default schema.

You can specify a schema search path either by specifying the %SchemaPath property, or by specifying the second parameter of the `%New()` class method, as shown in the following two examples:

```objectscript
  set path="MyTests,Sample,Cinema"
  set tStatement = ##class(%SQL.Statement).%New(,path)
```

```objectscript
  set tStatement = ##class(%SQL.Statement).%New()
  set tStatement.%SchemaPath="MyTests,Sample,Cinema"
```

You can set `%SchemaPath` at any point prior to the `%Prepare()` method which uses it.

The following example returns the current value of `%SchemaPath`:

```objectscript
  set tStatement = ##class(%SQL.Statement).%New()
  write !,"default path=",tStatement.%SchemaPath
  set tStatement.%SchemaPath="MyTests,Sample,Cinema"
   write !,"set path=",tStatement.%SchemaPath
```

You can use the %ClassPath() method to set `%SchemaPath` to the search path defined for the specified class name:

```objectscript
  set tStatement = ##class(%SQL.Statement).%New()
  set tStatement.%SchemaPath=tStatement.%ClassPath("Sample.Person")
  write tStatement.%SchemaPath
```

### %Dialect Property

The %Dialect property specifies the SQL statement dialect. You can specify Sybase, MSSQL, or IRIS (InterSystems SQL). The Sybase or MSSQL setting causes the SQL statement to be processed using the specified Transact-SQL dialect.

The Sybase and MSSQL dialects support a limited subset of SQL statements in these dialects. They support the `SELECT`, `INSERT`, `UPDATE`, `DELETE`, and `EXECUTE` statements. They support the `CREATE TABLE` statement for permanent tables, but not for temporary tables. `CREATE VIEW` is supported. `CREATE TRIGGER` and `DROP TRIGGER` are supported. However, this implementation does not support transaction rollback should the `CREATE TRIGGER` statement partially succeed but then fail on class compile. `CREATE PROCEDURE` and `CREATE FUNCTION` are supported.

The Sybase and MSSQL dialects support the `IF` flow-of-control statement. This command is not supported in the IRIS (InterSystems SQL) dialect.

The default is InterSystems SQL, represented by an empty string (`""`), or specified as `"IRIS"`

You can specify `%Dialect` either as the third parameter of the `%New()` class method, or set it directly as a property, or set it using a method, as shown in the following three examples:

Setting `%Dialect` in `%New()` class method:

```objectscript
  set tStatement = ##class(%SQL.Statement).%New(,,"Sybase")
  write "language mode set to=",tStatement.%Dialect
```

Setting the `%Dialect` property directly:

```objectscript
  set tStatement = ##class(%SQL.Statement).%New()
  set defaultdialect=tStatement.%Dialect
  write "default language mode=",defaultdialect,!
  set tStatement.%Dialect="Sybase"
  write "language mode set to=",tStatement.%Dialect,!
  set tStatement.%Dialect="IRIS"
   write "language mode reset to default=",tStatement.%Dialect,!
```

Setting the `%Dialect` property using the %DialectSet() instance method, which returns an error status:

```objectscript
  set tStatement = ##class(%SQL.Statement).%New()
  set tStatus = tStatement.%DialectSet("Sybase")
    if tStatus'=1 {write "%DialectSet failed:" do $System.Status.DisplayError(tStatus) quit}
  write "language mode set to=",tStatement.%Dialect
```

The `%DialectSet()` method returns a %Status value: Success returns a status of 1. Failure returns an object expression that begins with 0, followed by encoded error information. For this reason, you cannot perform a `tStatus=0` test for failure; you can perform a `$$$ISOK(tStatus)=0` macro test for failure.

### %ObjectSelectMode Property

The %ObjectSelectMode property is a boolean value. If `%ObjectSelectMode`=0 (the default) all columns in the SELECT list are bound to properties with literal types in the result set. If `%ObjectSelectMode`=1 then columns in the SELECT list are bound to properties with the type defined in the associated property definition.

`%ObjectSelectMode` allows you to specify how columns whose type class is a swizzleable class will be defined in the result set class generated from a SELECT statement. If `%ObjectSelectMode`=0 the property corresponding to the swizzleable column will be defined in result sets as a simple literal type corresponding to the SQL table's RowID type. If `%ObjectSelectMode`=1 the property will be defined with the column’s declared type. That means that accessing the result set property will trigger swizzling.

`%ObjectSelectMode` cannot be set as a parameter of `%New()`.

The following example returns the `%ObjectSelectMode` default value, sets `%ObjectSelectMode`, then returns the new `%ObjectSelectMode` value:

```objectscript
  set myquery = "SELECT TOP 5 %ID AS MyID,Name,Age FROM Sample.Person"
  set tStatement = ##class(%SQL.Statement).%New()
  write !,"default ObjectSelectMode=",tStatement.%ObjectSelectMode
  set tStatement.%ObjectSelectMode=1
  write !,"set ObjectSelectMode=",tStatement.%ObjectSelectMode
```

`%ObjectSelectMode`=1 is principally used when returning values from a result set using the field name property. This is further described with examples in Fieldname Property.

`%ObjectSelectMode`=1 can be used when a field in the SELECT list is linked to a collection property. `%ObjectSelectMode` will swizzle the collection. If %SelectMode = 1 or 2, the system converts the collection serial value into Logical mode form before swizzling. The resulting OREF supports the full collection interface.

## Preparing an SQL Statement

Preparing an SQL statement validates the statement, prepares it for subsequent execution, and generates metadata about the SQL statement.

There are three ways to prepare an SQL statement using the %SQL.Statement class:

*   %Prepare(), which prepares an SQL statement (a query, for example) for a subsequent `%Execute()`.
    
*   %PrepareClassQuery(), which prepares a call statement to an existing query. Once prepared, this query can be executed using a subsequent `%Execute()`.
    
*   %ExecDirect(), which both prepares and executes an SQL statement. `%ExecDirect()` is described in “Executing an SQL Statement”.
    
*   %ExecDirectNoPriv(), which prepares and executes an SQL statement and does not perform privilege checking. `%ExecDirectNoPriv()` is described in “Executing an SQL Statement”.
    

You can also prepare an SQL statement without creating an object instance by using the $SYSTEM.SQL.Prepare() method. The `Prepare()` method is shown in the following Terminal example:

```objectscript
USER>set topnum=5
USER>set prep=$SYSTEM.SQL.Prepare("SELECT TOP :topnum Name,Age FROM Sample.Person WHERE Age=?")

USER>do prep.%Display()
```

Preparing an SQL statement creates a cached query. Using a cached query allows the same SQL query to be executed multiple times without the need to re-prepare the SQL statement. A cached query can be executed one or more times by any process; it can be executed with different input parameter values.

Each time you prepare an SQL statement, InterSystems IRIS searches the query cache to determine if the same SQL statement has already been prepared and cached. (Two SQL statements are considered “the same” if they differ only in the values of literals and input parameters.) If the prepared statement does not already exist in the query cache, InterSystems IRIS creates a cached query. If the prepared statement already exists in the query cache, no new cached query is created. For this reason, it is important not to code a prepare statement within a loop structure.

### %Prepare()

You can prepare an SQL statement using the %Prepare() instance method of the %SQL.Statement class. The `%Prepare()` method takes, as its first argument, the SQL statement. This can be specified as a quoted string or a variable that resolves to a quoted string, as shown in the following example:

```objectscript
  set qStatus = tStatement.%Prepare("SELECT Name,Age FROM Sample.Person")
```

More complex queries can be specified using a subscripted array passed by reference, as shown in the following example:

```objectscript
  set myquery = 3
  set myquery(1) = "SELECT %ID AS id, Name, DOB, Home_State"
  set myquery(2) = "FROM Person WHERE Age > 80"
  set myquery(3) = "ORDER BY 2"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(.myquery)
```

A query can contain duplicate field names and field name aliases.

A query supplied to `%Prepare()` can contain input host variables, as shown in the following example:

```objectscript
  set minage = 80
  set myquery = 3
  set myquery(1) = "SELECT %ID AS id, Name, DOB, Home_State"
  set myquery(2) = "FROM Person WHERE Age > :minage"
  set myquery(3) = "ORDER BY 2"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(.myquery)
```

InterSystems IRIS substitutes the defined literal value for each input host variable when the SQL statement is executed. Note however, that if this code is called as a method, the `minage` variable must be made Public. By default, methods are ProcedureBlocks; this means that a method (such as `%Prepare()`) cannot see variables defined by its caller. You can either override this default by specifying the class as [[ Not ProcedureBlock ]](https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=ROBJ_class_procedureblock), specifying the method as [[ ProcedureBlock = 0]](https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=ROBJ_method_procedureblock), or by specifying [[ PublicList = minage ]](https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=ROBJ_method_publiclist).

> **Note:**
> 
> It is good program practice to always confirm that an input variable contains an appropriate value before inserting it into SQL code.

You can also supply literal values to a query using ? input parameters. InterSystems IRIS substitutes a literal value for each ? input parameter using the corresponding parameter value you supply to the `%Execute()` method. Following a `%Prepare()`, you can use the %GetImplementationDetails() method to list the input host variables and the ? input parameters in the query.

The `%Prepare()` method returns a %Status value: Success returns a status of 1 (the query string is valid; referenced tables exist in the current namespace). Failure returns an object expression that begins with 0, followed by encoded error information. For this reason, you cannot perform a `status=0` test for failure; you can perform a `$$$ISOK(status)=0` macro test for failure.

The `%Prepare()` method uses the `%SchemaPath` property defined earlier to resolve unqualified names.

> **Note:**
> 
> Dynamic SQL performance can be significantly improved by using fully qualified names whenever possible.

You can specify input parameters in the SQL statement by using the “? ” character:

```objectscript
  set myquery="SELECT TOP ? Name,Age FROM Sample.Person WHERE Age > ?"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(myquery)
```

You specify the value for each ? input parameter in the `%Execute()` instance method when you execute the query. An input parameter must take a literal value or an expression that resolves to a literal value. An input parameter cannot take a field name value or a field name alias. An input parameter must be declared PUBLIC for a `SELECT` statement to reference it directly.

A query can contain field aliases. In this case, the `Data` property accesses the data using the alias, not the field name.

You are not limited to `SELECT` statements within Dynamic SQL: you can use the `%Prepare()` instance method to prepare other SQL statements, including the `CALL`, `INSERT`, `UPDATE`, and `DELETE` statements.

You can display information about the currently prepared statement using the %Display() instance method, as shown in the following example:

```objectscript
  set tStatement = ##class(%SQL.Statement).%New(,"Sample")
  set myquery = 3
  set myquery(1) = "SELECT TOP ? Name,DOB,Home_State"
  set myquery(2) = "FROM Person"
  set myquery(3) = "WHERE Age > 60 AND Age < 65"
  set qStatus = tStatement.%Prepare(.myquery)
   if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  do tStatement.%Display()
  write !,"End of %Prepare display"
```

This information consists of the Implementation Class, the Arguments (a comma-separated list of the actual arguments, either literal values or ? input parameters), and the Statement Text.

`%Prepare()` takes an optional second argument, `checkPriv`, which is a logical value that determines whether InterSystems IRIS checks privileges on the statement. If `checkPriv` is 0, no privileges are checked. Disabling privilege checking gives applications more control over the execution of dynamic queries but increases security risk. The default value is 1 (privileges are checked). For example:

```objectscript
  set statement = ##class(%SQL.Statement).%New()
  set status =statement.%Prepare("DELETE FROM T",0) // No privileges checked

  set statement2 = ##class(%SQL.Statement).%New()
  set status =statement2.%Prepare("DELETE FROM T") // Privilege is checked
```

### %PrepareClassQuery()

You can prepare an existing SQL query using the %PrepareClassQuery() instance method of the %SQL.Statement class. The `%PrepareClassQuery()` method takes three parameters: the class name of the existing query, the query name, and an optional third argument that determines if privileges should be checked (if omitted, privileges are checked). The class name and the query name are specified as a quoted string or a variable that resolves to a quoted string, and the privilege checking option is specified as 0 or 1, as shown in the following example:

```objectscript
  set qStatus = tStatement.%PrepareClassQuery("User.queryDocTest","DocTest", 0) // No privileges checked
  set qStatus2 = tStatement.%PrepareClassQuery("User.queryDocTest","DocTest", 1) // Privilege is checked
  set qStatus3 = tStatement.%PrepareClassQuery("User.queryDocTest","DocTest") // Privilege is checked
```

The `%PrepareClassQuery()` method returns a %Status value: Success returns a status of 1. Failure returns an object expression that begins with 0, followed by encoded error information. For this reason, you cannot perform a `qStatus=0` test for failure; you can perform a `$$$ISOK(qStatus)=0` macro test for failure.

The `%PrepareClassQuery()` method uses the `%SchemaPath` property defined earlier to resolve unqualified names.

`%PrepareClassQuery()` executes using a CALL statement. Because of this, the executed class query must have an SqlProc parameter.

The following example shows `%PrepareClassQuery()` invoking the ByName query defined in the Sample.Person class, passing a string to limit the names returned to those that start with that string value:

```objectscript
  set statemt=##class(%SQL.Statement).%New()
  set cqStatus=statemt.%PrepareClassQuery("Sample.Person","ByName")
    if cqStatus'=1 {write "%PrepareClassQuery failed:" do $System.Status.DisplayError(cqStatus) quit}
  set rset=statemt.%Execute("L")
  do rset.%Display()
```

The following example shows `%PrepareClassQuery()` invoking an existing query:

```objectscript
   set tStatement=##class(%SQL.Statement).%New()
   set cqStatus=tStatement.%PrepareClassQuery("%SYS.GlobalQuery","Size")
     if cqStatus'=1 {write "%PrepareClassQuery failed:" do $System.Status.DisplayError(cqStatus) quit}
   set install=$SYSTEM.Util.DataDirectory()
   set rset=tStatement.%Execute(install_"mgr\User")
   do rset.%Display()
```

The following example shows `%Prepare()` preparing a CREATE QUERY statement, and then `%PrepareClassQuery()` invoking this class query:

```sql
  /* Creating the Query */
  set query=4
  set query(1)="CREATE QUERY DocTest() SELECTMODE RUNTIME PROCEDURE "
  set query(2)="BEGIN "
  set query(3)="SELECT TOP 5 Name,Home_State FROM Sample.Person ; "
  set query(4)="END"

  set statement = ##class(%SQL.Statement).%New()
  set qStatus = statement.%Prepare(.query)
  if qStatus '= 1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}

  set rset = statement.%Execute()
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
  write !,"Created a query",!

  /* Calling the Query */
  write !,"Calling a class query..."
  set cqStatus = statement.%PrepareClassQuery("User.queryDocTest","DocTest")
  if cqStatus '= 1 {write "%PrepareClassQuery failed:" do $SYSTEM.Status.DisplayError(cqStatus) quit}

  set rset = statement.%Execute()
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  write "Query data:",!,!
  while rset.%Next()
  {
    do rset.%Print()
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
  write !,"End of data."

  /* Deleting the Query */
  &sql(DROP QUERY DocTest)
  if SQLCODE < 0 {write !,"Error deleting query:", SQLCODE, " ", %msg quit}
  write !,"Deleted the query."
```

To display a row of data retrieved by a stored query you can use the `%Print()` method, as shown in this example. To display specific column data that was retrieved by a stored query you must use either the `%Get("fieldname")` or the `%GetData(colnum)` method. See Iterating through a Result Set.

If the query is defined to accept arguments, you can specify input parameters in the SQL statement by using the “? ” character. You specify the value for each ? input parameter in the `%Execute()` method when you execute the query. An input parameter must be declared PUBLIC for a `SELECT` statement to reference it directly.

You can display information about the currently prepared query using the `%Display()` method, as shown in the following example:

```sql
  /* Creating the Query */
  set myquery=4
  set myquery(1)="CREATE QUERY DocTest() SELECTMODE RUNTIME PROCEDURE "
  set myquery(2)="BEGIN "
  set myquery(3)="SELECT TOP 5 Name,Home_State FROM Sample.Person ; "
  set myquery(4)="END"

  set statement = ##class(%SQL.Statement).%New()
  set qStatus = statement.%Prepare(.myquery)
  if qStatus '= 1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}

  set rset = statement.%Execute()
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
  write !,"Created a query",!

  /* Preparing and Displying Info about the Query */
  write !,"Preparing a class query..."
  set cqStatus = statement.%PrepareClassQuery("User.queryDocTest","DocTest")
  if cqStatus '= 1 {write "%PrepareClassQuery failed:" do $SYSTEM.Status.DisplayError(cqStatus) quit}

  do statement.%Display()
  write !,"End of %Prepare display"

  /* Deleting the Query */
  &sql(DROP QUERY DocTest)
  if SQLCODE < 0 {write !,"Error Deleting query:",SQLCODE," ",%msg  quit }
  write !,"Deleted the query"
```

This information consists of the Implementation Class, the Arguments (a comma-separated list of the actual arguments, either literal values or ? input parameters), and the Statement Text.

For further details, see Defining and Using Class Queries.

### Results of a Successful Prepare

Following a successful prepare (`%Prepare()`, `%PrepareClassQuery()`, or `%ExecDirect()`) you can invoke the %SQL.Statement %Display() instance method or %GetImplementationDetails() instance method to return the details of the currently prepared statement. For example:

`%Display()`:

```objectscript
  set myquery = "SELECT TOP 5 Name,Age FROM Sample.Person WHERE Age > 21"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(myquery)
   if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  do tStatement.%Display()
  set rset = tStatement.%Execute()
```

`%GetImplementationDetails()`:

```objectscript
  set myquery = "SELECT TOP ? Name,Age FROM Sample.Person WHERE Age > 21 AND Name=:fname"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(myquery)
   if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  set bool = tStatement.%GetImplementationDetails(.pclassname,.ptext,.pargs)
   if bool=1 {write "Implementation class= ",pclassname,!
             write "Statement text= ",ptext,!
             write "Arguments= ",$listtostring(pargs),!  }  // returns "?,?,c,21,v,fname
   else {write "%GetImplementationDetails() failed",!}
  set rset = tStatement.%Execute()
```

These methods provide the following information:

*   `Implementation class`: the class name corresponding to the cached query. For example: `%sqlcq.SAMPLES.cls49`.
    
*   `Arguments`: A list of the query arguments in the order specified. If an argument is enclosed in double parentheses to suppress literal substitution the argument is not included in the argument list.
    
    `%Display()` displays a comma-separated list of the query arguments. Each argument can be a literal value, the name of an input host variables (without the colon), or a question mark (?) for an input parameter. If there are no arguments, this item displays `<<none>>`. A predicate that specifies multiple values, such as `IN` or `%INLIST` lists each value as a separate argument.
    
    `%GetImplementationDetails()` returns the query arguments as a %List structure. Each argument is represented by a pair of elements, a type and a value: Type c (constant) is followed by a literal value; Type v (variable) is followed by the name of an input host variable (without the colon); Type ? is an input parameter, and is followed by a second question mark. If there are no arguments, the arguments list is an empty string. A predicate that specifies multiple values, such as `IN` or `%INLIST` lists each value as a separate type and value pair.
    
*   `Statement Text`: the query text, exactly as specified. Letter case is preserved, host variables and input parameters are shown as written, the default schema is not shown. For `%Prepare()` for example, `SELECT TOP :n Name FROM Clients`. For `%PrepareClassQuery()` for example, `call Sample.SP_Sample_By_Name(?)`.
    

For other metadata information generated for a prepared query, refer to SQL Metadata.

### The preparse() Method

You can use the preparse() method to return a %List structure of the query arguments without having to prepare the SQL query. The query arguments are returned in the same format as `%GetImplementationDetails()`.

The `preparse()` method also returns the query text. However, unlike `%Display()` and `%GetImplementationDetails()` which return the query text exactly as specified, the `preparse()` method replaces each query argument with a ? character, removes comments, and normalizes whitespace. It does not supply a default schema name. The `preparse()` method in the following example returns a parsed version of the query text and a %List structure of the query arguments:

```objectscript
  set myq=2
  set myq(1)="SELECT TOP ? Name /* first name */, Age "
  set myq(2)="FROM Sample.MyTable WHERE Name='Fred' AND Age > :years -- end of query"
  do ##class(%SQL.Statement).preparse(.myq,.stripped,.args)
  write "preparsed query text: ",stripped,!
  write "arguments list: ",$listtostring(args)
```

## Executing an SQL Statement

There are two ways to execute an SQL statement using the %SQL.Statement class:

*   `%Execute()`, which executes an SQL statement previous prepared using `%Prepare()` or `%PrepareClassQuery()`.
    
*   `%ExecDirect()`, which both prepares and executes an SQL statement.
    
*   `%ExecDirectNoPriv()`, which prepares and executes an SQL statement and does not perform privilege checking.
    

You can also execute an SQL statement without creating an object instance by using the $SYSTEM.SQL.Execute() method. This method both prepares and executes the SQL statement. It creates a cached query. The `Execute()` method is shown in the following Terminal example:

```objectscript
USER>set topnum=5
USER>set rset=$SYSTEM.SQL.Execute("SELECT TOP :topnum Name,Age FROM Sample.Person")

USER>do rset.%Display()
```

### %Execute()

After preparing a query, you can execute it by calling the %Execute() instance method of the %SQL.Statement class. In the case of a non-`SELECT` statement, `%Execute()` invokes the desired operation (such as performing an `INSERT`). In the case of a `SELECT` query, `%Execute()` generates a result set for subsequent traversal and data retrieval. For example:

```objectscript
  set rset = tStatement.%Execute()
```

The `%Execute()` method sets the %SQL.StatementResult class properties %SQLCODE and %Message for all SQL statements. Successful execution of the statement sets %SQLCODE to 0. This does not mean that the statement successfully retrieved results. Similarly, `%Execute()` does not set %SQLCODE to 100 if the statement retrieves no results. The check for results, and subsequent setting of %SQLCODE to 0, 100, or a negative error value occurs as you fetch the results one row at a time, such as by using the `%Next()` method.

`%Execute()` sets other %SQL.StatementResult properties as follows:

*   `INSERT`, `UPDATE`, `INSERT OR UPDATE`, `DELETE`, and `TRUNCATE TABLE` statements set %ROWCOUNT to the number of rows affected by the operation. `TRUNCATE TABLE` cannot determine the actual number of rows deleted, so it sets %ROWCOUNT to -1.
    
    `INSERT`, `UPDATE`, `INSERT OR UPDATE`, and `DELETE` set %ROWID to the RowID value of the last record inserted, updated, or deleted. If the operation did not insert, update, or delete any records, %ROWID is undefined, or remains set to its prior value. `TRUNCATE TABLE` does not set %ROWID.
    
*   A `SELECT` statement sets the %ROWCOUNT property to 0 when it creates the result set. `%ROWCOUNT` is incremented when the program iterates through the contents of the result set, for example by using the `%Next()` method. `%Next()` returns 1 to indicate that it is positioned on a row or 0 to indicate that it is positioned after the last row (at the end of the result set). If the cursor is positioned after the last row, the value of `%ROWCOUNT` indicates the number of rows contained in the result set.
    
    If a `SELECT` query returns only aggregate functions, every `%Next()` sets %ROWCOUNT=1. The first `%Next()` always sets %SQLCODE=0, even when there is no data in the table; any subsequent `%Next()` sets %SQLCODE=100 and sets %ROWCOUNT=1.
    
    A `SELECT` also sets the %CurrentResult and the %ResultColumnCount. `SELECT` does not set `%ROWID`.
    

You can use `ZWRITE` to return the values for all of the %SQL.StatementResult class properties.

For further details, see SQL System Variables. If you are executing TSQL code with %Dialect set to Sybase or MSSQL, errors are reported both in the standard protocols for that SQL dialect and in the InterSystems IRIS `%SQLCODE` and `%Message` properties.

#### %Execute() with Input Parameters

The `%Execute()` method can take one or more parameters that correspond to the input parameters (indicated by “?”) within the prepared SQL statement. The `%Execute()` parameters correspond to the sequence in which the “?” characters appear within the SQL statement: the first parameter is used for the first “?”, the second parameter for the second “?”, and so on. Multiple `%Execute()` parameters are separated by commas. You can omit a parameter value by specifying the placeholder comma. The number of `%Execute()` parameters must correspond to the “?” input parameters. If there are fewer or more `%Execute()` parameters than corresponding “?” input parameters, execution fails with the `%SQLCODE` property set to an SQLCODE -400 error.

You can use an input parameter to supply a literal value or an expression to the SELECT list and to the other query clauses, including the TOP clause and the WHERE clause. You cannot use an input parameter to supply a column name or a column name alias to the SELECT list or to the other query clauses.

When an input parameter is used in a greater than or less than comparison, such as in a WHERE clause, the parameter is normalized only if it is a valid number. If the input parameter is not a valid number, the comparison condition is checked using either the sorts after operator (]]) or the no sorts after operator (']]), depending on the comparison. Note that this operator orders all numbers before any nonnumeric values (such as strings).

The maximum number of input parameters when specified as explicit `%Execute()` parameters is 255. The maximum number of input parameters when specified using a variable length array `%Execute(vals...)` is 380.

Following a Prepare, you can use Prepare arguments metadata to return the count and required data types for ? input parameters. You can use the %GetImplementationDetails() method to return a list of ? input parameters in a prepared query and the query text with the ? input parameters shown in context.

The following ObjectScript example executes a query with two input parameters. It specifies the input parameter values (21 and 26) in the `%Execute()` method.

```objectscript
  SET tStatement = ##class(%SQL.Statement).%New(1)
  SET tStatement.%SchemaPath = "MyTests,Sample,Cinema"
  SET myquery=2
  SET myquery(1)="SELECT Name,DOB,Age FROM Person"
  SET myquery(2)="WHERE Age > ? AND Age < ? ORDER BY Age"
  SET qStatus = tStatement.%Prepare(.myquery)
    IF qStatus'=1 {WRITE "%Prepare failed:" DO $System.Status.DisplayError(qStatus) QUIT}
  SET rset = tStatement.%Execute(21,26)
  WRITE !,"Execute OK: SQLCODE=",rset.%SQLCODE,!!
  DO rset.%Display()
  WRITE !,"End of data: SQLCODE=",rset.%SQLCODE
```

The following ObjectScript example executes the same query. The `%Execute()` method formal parameter list uses a variable length array (dynd...) to specify an indefinite number of input parameter values; in this case, the subscripts of the `dynd` array. The `dynd` variable is set to 2 to indicate two subscript values.

```objectscript
  set tStatement = ##class(%SQL.Statement).%New(1)
  set tStatement.%SchemaPath = "MyTests,Sample,Cinema"
  set myquery=2
  set myquery(1)="SELECT Name,DOB,Age FROM Person"
  set myquery(2)="WHERE Age > ? AND Age < ? ORDER BY Age"
  set dynd=2,dynd(1)=21,dynd(2)=26
  set qStatus = tStatement.%Prepare(.myquery)
    if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  set rset = tStatement.%Execute(dynd...)
  write !,"Execute OK: SQLCODE=",rset.%SQLCODE,!!
  do rset.%Display()
  write !,"End of data: SQLCODE=",rset.%SQLCODE
```

You can issue multiple `%Execute()` operations on a prepared result set. This enables you to run a query multiple times, supplying different input parameter values. It is not necessary to close the result set between `%Execute()` operations, as shown in the following example:

```objectscript
  set myquery="SELECT Name,SSN,Age FROM Sample.Person WHERE Name %STARTSWITH ?"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(myquery)
    if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  set rset = tStatement.%Execute("A")
  do rset.%Display()
  write !,"End of A data",!!
  set rset = tStatement.%Execute("B")
  do rset.%Display()
  write !,"End of B data"
```

#### Handling %Execute Errors Using Try/Catch

You can execute Dynamic SQL within a TRY block structure, passing runtime errors to the associated CATCH block exception handler. For `%Execute()` errors, you can use the %Exception.SQL class to create an exception instance, which you can then THROW to the `CATCH` exception handler.

The following example creates an SQL exception instance when an `%Execute()` error occurs. In this case, the error is a cardinality mismatch between the number of ? input parameters (1) and the number of `%Execute()` parameters (3). It throws the `%SQLCODE` and `%Message` property values (as Code and Data) to the `CATCH` exception handler. The exception handler uses the `%IsA()` instance method to test the exception type, then displays the `%Execute()` error:

```objectscript
  try {
  set myquery = "SELECT TOP ? Name,DOB FROM Sample.Person"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(myquery)
     if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  set rset = tStatement.%Execute(7,9,4)
     if rset.%SQLCODE=0 { write !,"Executed query",! }
     else { set badSQL=##class(%Exception.SQL).%New(,rset.%SQLCODE,,rset.%Message)
            throw badSQL }
  do rset.%Display()
  write !,"End of data"
  return
  }
  catch exp { write "In the catch block",!
              if 1=exp.%IsA("%Exception.SQL") {
                write "SQLCODE: ",exp.Code,!
                write "Message: ",exp.Data,! }
              else { write "Not an SQL exception",! }
              return
  }
```

### %ExecDirect()

The %SQL.Statement class provides the %ExecDirect() class method, that both prepares and executes a query in a single operation. It can prepare either a specified query (like %Prepare()) or an existing class query (like %PrepareClassQuery()).

`%ExecDirect()` prepares and executes a specified query:

```objectscript
  set myquery=2
  set myquery(1)="SELECT Name,Age FROM Sample.Person"
  set myquery(2)="WHERE Age > 21 AND Age < 30 ORDER BY Age"
  set rset = ##class(%SQL.Statement).%ExecDirect(,.myquery)
    if rset.%SQLCODE=0 { write !,"ExecDirect OK",!! }
    else { write !,"ExecDirect SQLCODE=",rset.%SQLCODE,!,rset.%Message  quit}
  do rset.%Display()
  write !,"End of data: SQLCODE=",rset.%SQLCODE
```

`%ExecDirect()` prepares and executes an existing class query:

```objectscript
  set mycallq = "?=CALL Sample.PersonSets('A','NH')"
  set rset = ##class(%SQL.Statement).%ExecDirect(,mycallq)
    if rset.%SQLCODE=0 { write !,"ExecDirect OK",!! }
    else { write !,"ExecDirect SQLCODE=",rset.%SQLCODE,!,rset.%Message  quit}
  do rset.%Display()
  write !,"End of data: SQLCODE=",rset.%SQLCODE
```

You can specify input parameter values as the third and subsequent parameters of the `%ExecDirect()` class method, as shown in the following example:

```objectscript
  set myquery=2
  set myquery(1)="SELECT Name,Age FROM Sample.Person"
  set myquery(2)="WHERE Age > ? AND Age < ? ORDER BY Age"
  set rset = ##class(%SQL.Statement).%ExecDirect(,.myquery,12,20)
    if rset.%SQLCODE'=0 {write !,"1st ExecDirect SQLCODE=",rset.%SQLCODE,!,rset.%Message  quit}
  do rset.%Display()
  write !,"End of teen data",!!
  set rset2 = ##class(%SQL.Statement).%ExecDirect(,.myquery,19,30)
    if rset2.%SQLCODE'=0 {write !,"2nd ExecDirect SQLCODE=",rset2.%SQLCODE,!,rset2.%Message  quit}
  do rset2.%Display()
  write !,"End of twenties data"
```

The `%ExecDirect()` input parameters correspond to the sequence in which the “?” characters appear within the SQL statement: the third parameter is used for the first “?”, the fourth parameter for the second “?”, and so on. You can omit a parameter value by specifying a placeholder comma. If there are fewer `%ExecDirect()` input parameters than corresponding “?” input parameters, the default value (if one exists) is used.

In the following example, the first `%ExecDirect()` specifies all three “?” input parameters, the second `%ExecDirect()` specifies only the second ? input parameter, and omits the first and third. It takes the `Sample.PersonSets()` default ('MA') for the third input parameter:

```objectscript
  set mycall = "?=CALL Sample.PersonSets(?,?)"
  set rset = ##class(%SQL.Statement).%ExecDirect(,mycall,"","A","NH")
    if rset.%SQLCODE'=0 {write !,"1st ExecDirect SQLCODE=",rset.%SQLCODE,!,rset.%Message  quit}
  do rset.%Display()
  write !,"End of A people data",!!
  set rset2 = ##class(%SQL.Statement).%ExecDirect(,mycall,,"B")
    if rset2.%SQLCODE'=0 {write !,"2nd ExecDirect SQLCODE=",rset2.%SQLCODE,!,rset2.%Message  quit}
  do rset2.%Display()
  write !,"End of B people data"
```

`%ExecDirect()` can invoke the %SQL.Statement %Display() instance method or %GetImplementationDetails() instance method to return the details of the currently prepared statement. Because `%ExecDirect()` can prepare and execute either a specified query or an existing class query, you can use the `%GetImplementationDetails() pStatementType` parameter to determine which kind of query was prepared:

```objectscript
  set mycall = "?=CALL Sample.PersonSets('A',?)"
  set rset = ##class(%SQL.Statement).%ExecDirect(tStatement,mycall,,"NH")
    if rset.%SQLCODE'=0 {write !,"ExecDirect SQLCODE=",rset.%SQLCODE,!,rset.%Message  quit}
  set bool = tStatement.%GetImplementationDetails(.pclassname,.ptext,.pargs,.pStatementType)
  if bool=1 {if pStatementType=1 {write "Type= specified query",!}
             elseif pStatementType=45 {write "Type= existing class query",!}
             write "Implementation class= ",pclassname,!
             write "Statement text= ",ptext,!
             write "Arguments= ",$listtostring(pargs),!!  }
  else {write "%GetImplementationDetails() failed"}
  do rset.%Display()
  write !,"End of data"
```

For further details, see Results of a Successful Prepare.

### %ExecDirectNoPriv()

The %SQL.Statement class provides the `%ExecDirectNoPriv()` class method, which, like %ExecDirect, prepares and executes a query in a single operation. `%ExecDirectNoPriv()` also disables privilege checking on the statement during query preparation. Disabling privilege checking gives applications more control over the execution of dynamic queries but increases security risk.

While `%ExecDirectNoPriv()` disables privilege checked during query preparation, it does not disable privilege checking at execution time. This behavior particularly applies when attempting to grant users new privileges. For example, if a user attempts to grant another user the `SELECT` privilege on a certain table, but does not have that privilege, the SQL Statement fails during execution because the operation is not allowed.

## Returning the Full Result Set

Executing a statement with either `%Execute()` or `%ExecDirect()` returns an object that implements the %SQL.StatementResult interface. This object can be a unitary value, a result set, or a context object that is returned from a `CALL` statement.

### %Display() Method

You can display the entire result set (the contents of the result object) by calling the %Display() instance method of the %SQL.StatementResult class, as shown in the following example:

```objectscript
  do rset.%Display()
```

Note that the `%Display()` method does not return a %Status value.

When displaying a query result set, `%Display()` concludes by displaying the row count: “5 Rows(s) Affected”. (This is the `%ROWCOUNT` value after `%Display()` has iterated through the result set.) Note that `%Display()` does not issue a line return following this row count statement.

`%Display()` has two optional arguments:

*   Delimiter: a string inserted between data columns and data headers. It appears between resultset columns, immediately before the header or data value. The default is no delimiter. If omitted, specify a placeholder comma before the Column Alignment flag.
    
*   Column Alignment: an integer flag that specifies how whitespace is calculated between data columns and data headers. The available options are:
    
    *   0: Resultset header/data columns will be aligned based on the standard delimiter (tab). This is the default.
        
    *   1: Resultset header/data columns will be aligned based on the length of the column header and the standard delimiter (tab).
        
    *   2: Resultset header/data columns will be aligned based on the precision/length of the column data property and the standard delimiter (tab).
        

### %DisplayFormatted() Method

You can reformat and redirect the result set contents to a generated file by calling the %DisplayFormatted() instance method of the %SQL.StatementResult class, rather than calling `%Display()`.

You can specify the result set format either by specifying the string option `%DisplayFormatted("HTML")` or the corresponding integer code `%DisplayFormatted(1)`. InterSystems IRIS generates a file of the specified type, appending the appropriate file name extension. This table shows the options you can specify and the files you can generate.

<table><tr><th>String Option</th><th>Integer Code</th><th>Extension of Generated File</th></tr><tr><td><code>"XML"</code></td><td><code>0</code></td><td><code>.xml</code></td></tr><tr><td><code>"HTML"</code></td><td><code>1</code></td><td><code>.html</code></td></tr><tr><td><code>"PDF"</code></td><td><code>2</code></td><td><code>.pdf</code></td></tr><tr><td><code>"TXT"</code></td><td><code>99</code></td><td><code>.txt</code></td></tr><tr><td><code>"CSV"</code></td><td><code>100</code></td><td><code>.csv</code></td></tr></table>

Note that the values in the generated CSV file are separated by tabs, not commas.

If you specify any other number or string, then `%DisplayFormatted()` generates a text (.txt) file. Text files conclude with the row count (for example “5 Rows(s) Affected”). The other formats do not include a row count.

You can specify or omit a result set file name:

*   If you specify a destination file (for example, `%DisplayFormatted(99,"myresults")`) a file with that name and the appropriate suffix (file name extension) is generated in the mgr directory in the subdirectory for the current namespace. For example, C:\InterSystems\IRIS\mgr\user\myresults.txt. If the specified file with that suffix already exists, InterSystems IRIS overwrites it with new data.
    
*   If you do not specify a destination file (for example, `%DisplayFormatted(99)`) a file with a randomly-generated name and the appropriate suffix (file name extension) is generated in the mgr directory in the Temp subdirectory. For example, C:\InterSystems\IRIS\mgr\Temp\w4FR2gM7tX2Fjs.txt. Each time a query is run a new destination file is generated.
    

These examples show Windows filenames; InterSystems IRIS supports equivalent locations on other operating systems.

If the specified file cannot be opened, this operation times out after 30 seconds with an error message; this commonly occurs when the user does not have write privileges to the specified directory (file folder).

If data cannot be rendered in the specified format, the destination file is created but no result set data is written to it. Instead, an appropriate message is written to the destination file. For example, a stream field OID contains characters that conflict with XML and HTML special formatting characters. This XML and HTML stream field issue can be resolved by using the XMLELEMENT function on stream fields; for example, `SELECT Name,XMLELEMENT("Para",Notes)`.

You can optionally supply the name of a translate table that `%DisplayFormatted()` will use when performing the specified format conversion.

In the case of multiple result sets in a result set sequence, the content of each result set is written to its own file.

The optional third `%DisplayFormatted()` argument specifies that messages are stored in a separate result set. Upon successful completion a message like the following is returned:

```
Message
21 row(s) affected.
```

The following Windows example creates two PDF (integer code 2) result set files in C:\InterSystems\IRIS\mgr\user\. It creates the `mess` result set for messages, then uses `%Display()` to display messages to the Terminal:

```objectscript
  set $NAMESPACE="USER"
  set myquery=2
  set myquery(1)="SELECT Name,Age FROM Sample.Person"
  set myquery(2)="WHERE Age > ? AND Age < ? ORDER BY Age"
  set rset = ##class(%SQL.Statement).%ExecDirect(,.myquery,12,20)
    if rset.%SQLCODE'=0 {write !,"1st ExecDirect SQLCODE=",rset.%SQLCODE,!,rset.%Message  quit}
  do rset.%DisplayFormatted(2,"Teenagers",.mess)
  do mess.%Display()
  write !,"End of teen data",!!
  set rset2 = ##class(%SQL.Statement).%ExecDirect(,.myquery,19,30)
    if rset2.%SQLCODE'=0 {write !,"2nd ExecDirect SQLCODE=",rset2.%SQLCODE,!,rset2.%Message  quit}
  do rset2.%DisplayFormatted(2,"Twenties",.mess)
  do mess.%Display()
  write !,"End of twenties data"
```

### Paginating a Result Set

You can use a view ID (%VID) to paginate a result set. The following example returns pages from the result set, each page containing 5 rows:

```objectscript
  set q1="SELECT %VID AS RSRow,* FROM "
  set q2="(SELECT Name,Home_State FROM Sample.Person WHERE Home_State %STARTSWITH 'M') "
  set q3="WHERE %VID BETWEEN ? AND ?"
  set myquery = q1_q2_q3
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus=tStatement.%Prepare(myquery)
      if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  for i=1:5:25 {
      write !!,"Next Page",!
      set rset=tStatement.%Execute(i,i+4)
      do rset.%Display()
      }
```

Refer to %GetRows() for another way to return groups of rows (records) from a result set.

## Returning Specific Values from the Result Set

To return specific values from a query result set, you must iterate through the result set one row at a time. To iterate through a result set, use the %Next() instance method. You can then either display the results of the whole current row using the %Print() method, or retrieve the value of a specified column in the current row.

The `%Next()` method fetches the data for the next row within the query results and places this data in the `Data` property of the result set object. `%Next()` returns one of these values:

*   `%Next()` = `1` — Cursor is positioned on a row in the query result.
    
*   `%Next()` = `0` — Cursor is positioned after the last row, indicating that there are no more rows to return or that the query returned 0 rows.
    

Each call to `%Next()` that returns 1 increments the `%ROWCOUNT` property of the result set by 1. If the cursor is positioned after the last row (`%Next()` returns 0), `%ROWCOUNT` indicates the number of rows in the result set.

Each call to `%Next()` also updates the `%SQLCODE` property of the result set. The updated `%SQLCODE` value depends on the fetched results:

*   `%SQLCODE` = `0` — `%Next()` successfully fetched a row of results.
    
*   `%SQLCODE` = `100` — `%Next()` fetched no results. Either the query returned no results or the cursor is positioned after the last row and there are no more results to fetch.
    
*   `%SQLCODE` < `0` — `%Next()` failed to perform the fetch. `%Next()` sets `%SQLCODE` to the SQLCODE of the error that caused the fetch to fail. It also sets the `%Message` property of the result set to the error message text. When calling `%Next()` iteratively in a loop, to avoid silent errors, check for negative `%SQLCODE` values and display the `%SQLCODE` error and its `%Message` text. For example:
    
    ```objectscript
      while rset.%Next()
      {
        write "%Next succeeded."
      }
      if (rset.%SQLCODE < 0)
      {
        write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message
        quit
      }
    ```
    

If a `SELECT` query returns only aggregate functions, every `%Next()` sets `%ROWCOUNT`=1. The first `%Next()` returns 1 and sets `%SQLCODE`=0 and `%ROWCOUNT`=1, even when there is no data in the table. Any subsequent `%Next()` returns 0 and sets `%SQLCODE`=100 and `%ROWCOUNT`=1.

After fetching a row from the result set, you can display data from that row using these methods:

*   rset.%Print() to return all of the data values for the current row from the query result set.
    
*   rest.%GetRow() and rset.%GetRows() to return the data values for a row as elements in an encoded List structure from the query result set.
    
*   rset.name to return a data value by property name, field name, alias property name, or alias field name from a query result set.
    
*   rset.%Get("fieldname") to return a data value by field name or alias field name from either a query result set or a stored query.
    
*   rset.%GetData(n) to return a data value by column number from either a query result set or a stored query.
    

### %Print() Method

The %Print() instance method retrieves the current record from the result set. By default, `%Print()` inserts a blank space delimiter between data field values. `%Print()` does not insert a blank space before the first field value or after the last field value in a record; it issues a line return at the end of the record. If a data field value already contains a blank space, that field value is enclosed in quotation marks to differentiate it from the delimiter. For example, if `%Print()` is returning city names, it would return them as follows: `Chicago "New York" Boston Atlanta "Los Angeles" "Salt Lake City" Washington`. `%Print()` quotes field values that contain the delimiter as part of the data value even when the `%Print()` delimiter is never used; for example if there is only one field in the result set.

You can optionally specify a `%Print()` parameter that provides a different delimiter to be placed between the field values. Specifying a different delimiter overrides the quoting of data strings that contain blank spaces. This `%Print()` delimiter can be one or more characters. It is specified as a quoted string. It is generally preferable that the `%Print()` delimiter be a character or string not found in the result set data. However, if a field value in the result set contains the `%Print()` delimiter character (or string), that field value is returned enclosed in quotation marks to differentiate it from the delimiter.

If a field value in the result set contains a line feed character, that field value is returned delimited by quotation marks.

The following ObjectScript example iterates through the query result set using `%Print()` to display each result set record, separating values with a "^|^" delimiter. Note how `%Print()` displays data from the FavoriteColors field which is an encoded list of elements:

```objectscript
  set q1="SELECT TOP 5 Name,DOB,Home_State,FavoriteColors "
  set q2="FROM Sample.Person WHERE FavoriteColors IS NOT NULL"
  set query = q1_q2
  set statement = ##class(%SQL.Statement).%New()

  set status = statement.%Prepare(query)
  if $$$ISERR(status) {write "%Prepare failed:" do $SYSTEM.Status.DisplayError(status) quit}

  set rset = statement.%Execute()
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  while rset.%Next()
  {
    write "Row count ",rset.%ROWCOUNT,!
    do rset.%Print("^|^")
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
  write !,"End of data"
  write !,"Total row count=",rset.%ROWCOUNT
```

The following example shows how field values that contain the delimiter are returned enclosed in quotation marks. In this example, the capital letter A is used as the field delimiter; therefore, any field value (name, street address, or state abbreviation) that contains a capital A literal is returned delimited by quotation marks.

```objectscript
  set query = "SELECT TOP 25 Name,Home_Street,Home_State,Age FROM Sample.Person"
  set statement = ##class(%SQL.Statement).%New()

  set status = statement.%Prepare(query)
  if $$$ISERR(status) {write "%Prepare failed:" do $SYSTEM.Status.DisplayError(status) quit}

  set rset = statement.%Execute()
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  while rset.%Next()
  {
     do rset.%Print("A")
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
  write !,"End of data"
  write !,"Total row count=",rset.%ROWCOUNT
```

### %GetRow() and %GetRows() Methods

The %GetRow() instance method retrieves the current row (record) from the result set as an encoded list of field value elements:

```objectscript
  set myquery = "SELECT TOP 17 %ID,Name,Age FROM Sample.Person"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(myquery)
    if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  set rset = tStatement.%Execute()
  for {set x=rset.%GetRow(.row,.status)
        if x=1 {write $listtostring(row," | "),! }
        else {write !,"End of data"
              write !,"Total row count=",rset.%ROWCOUNT
              return }
      }
```

The %GetRows() instance method retrieves a group of rows (records) of a specified size from the result set. Each row is returned as an encoded list of field value elements.

The following example returns the 1st, 6th, and 11th row in the result set. In this example, the `%GetRows()` first parameter (5) specifies that `%GetRows()` should retrieve successive groups of five rows. `%GetRows()` returns 1 if it successfully retrieves a group of five rows. The `.rows` parameter passes by reference a subscripted array of these five rows, so `rows(1)` returns the first row from each set of five: rows 1, 6, and 11. Specifying `rows(2)` would return rows 2, 7, and 12.

```objectscript
  set myquery = "SELECT TOP 17 %ID,Name,Age FROM Sample.Person"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(myquery)
    if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  set rset = tStatement.%Execute()
  for {set x=rset.%GetRows(5,.rows,.status)
        if x=1 {write $listtostring(rows(1)," | "),! }
        else {write !,"End of data"
              write !,"Total row count=",rset.%ROWCOUNT
              return }
       }
```

Rather than retrieving individual rows by subscript, you can use the `ZWRITE rows` command to return all of the subscripts in the retrieved array. Note that above example `ZWRITE rows` does not return the 16th and 17th row in the result set, because these rows are remainders after the last group of five rows was retrieved.

### rset.name Property

When InterSystems IRIS generates a result set, it creates a result set class that contains a unique property corresponding to each field name and field name alias in the result set.

You can use the `rset.name` property to return a data value by property name, field name, property name alias, or field name alias.

*   Property Name: If no field alias is defined, specify the field property name as `rset.PropName`. The result set field property name is taken from the corresponding property name in the table definition class.
    
*   Field Name: If no field alias is defined, specify the field name (or the property name) as `rset."fieldname"`. This is the SqlFieldName specified in the table definition. InterSystems IRIS uses this field name to locate the corresponding property name. In many cases, the property name and the field name (SqlFieldName) are identical.
    
*   Alias Property Name: If a field alias is defined, specify the alias property name as `rset.AliasProp`. An alias property name is generated from the column name alias in the `SELECT` statement. You cannot specify a field property name for a field with a defined alias.
    
*   Alias Name: If a field alias is defined, specify this alias name (or the alias property name) as `rset."alias"`. This is the column name alias in the `SELECT` statement. You cannot specify a field name for a field with a defined alias.
    
*   Aggregate, Expression, or Subquery: InterSystems IRIS assigns these `select-items` a field name of Aggregate_n, Expression_n, or Subquery_n (where the integer `n` corresponds to the sequence of the `select-item` list specified in the query). You can retrieve these `select-item` values using the field name (`rset."SubQuery_7"` not case-sensitive), the corresponding property name (`rset.Subquery7` case-sensitive), or by a user-defined field name alias. You can also just specify the `select-item` sequence number using rset.%GetData(n).
    

When specifying a property name, you must use correct letter case; when specifying a field name, correct letter case is not required.

This invocation of `rset.name` using the property name has the following consequences:

*   Letter Case: Property names are case-sensitive. Field names are not case-sensitive. Dynamic SQL can automatically resolve differences in letter case between a specified field or alias name and the corresponding property name. However, letter case resolution takes time. To maximize performance, you should specify the exact letter case of the property name or the alias.
    
*   Non-alphanumeric Characters: A property name can only contain alphanumeric characters (except for an initial % character). If the corresponding SQL field name or field name alias contains non-alphanumeric characters (for example, `Last_Name`) you can do either of the following:
    
    *   Specify the field name delimited with quotation marks. For example, `rset."Last_Name"`). This use of delimiters does not require that delimited identifiers be enabled. Letter case resolution is performed.
        
    *   Specify the corresponding property name, eliminating the non-alphanumeric characters. For example, `rset.LastName` (or `rset."LastName"`). You must specify the correct letter case for the property name.
        
*   % Property Names: Generally, property names beginning with a % character are reserved for system use. If a field property name or alias begins with a % character and that name conflicts with a system-defined property, the system-defined property is returned. For example, for `SELECT Notes AS %Message`, invoking `rset.%Message` will not return the Notes field values; it returns the %Message property defined for the statement result class. You can use rset.%Get("%Message") to return the field value.
    
*   Column Alias: If an alias is specified, Dynamic SQL always matches the alias rather than matching the field name or field property name. For example, for `SELECT Name AS Last_Name`, the data can only be retrieved using `rset.LastName` or `rset."Last_Name"`, not by using `rset.Name`.
    
*   Duplicate Names: Names are duplicate if they resolve to the same property name. Duplicate names can be multiple references to the same field in a table, alias references to different fields in a table, or references to fields in different tables. For example `SELECT p.DOB,e.DOB` specifies two duplicate names, even though those names refer to fields in different tables.
    
    If the `SELECT` statement contains multiple instances of the same field name or field name alias, `rset.PropName` or `rset."fieldname"` always return the first one specified in the `SELECT` statement. For example, for `SELECT c.Name,p.Name FROM Sample.Person AS p,Sample.Company AS c` using `rset.Name` retrieves the company name field data; `SELECT c.Name,p.Name AS Name FROM Sample.Person AS p,Sample.Company AS c` using `rset."name"` also retrieves the company name field data. If there are duplicate `Name` fields in the query the last character of the field name (`Name`) is replaced by a character (or characters) to create a unique property name. Thus a duplicate `Name` field name in a query has a corresponding unique property name, beginning with `Nam0` (for the first duplicate) through `Nam9` and continuing with capital letters `NamA` through `NamZ`.
    

For a user-specified query prepared using %Prepare() you can use the property name by itself. For a stored query prepared using %PrepareClassQuery(), you must use the %Get("fieldname") method.

The following example returns the values of three fields specified by property names: two field values by property name and the third field value by alias property name. In these cases, the specified property name is identical to the field name or field alias:

```objectscript
  set query = "SELECT TOP 5 Name,DOB AS bdate,FavoriteColors FROM Sample.Person"
  set statement = ##class(%SQL.Statement).%New(1)

  set status = statement.%Prepare(query)
  if $$$ISERR(status) {write "%Prepare failed:" do $SYSTEM.Status.DisplayError(status) quit}

  set rset = statement.%Execute()
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  while rset.%Next()
  {
    write "Row count ",rset.%ROWCOUNT,!
    write rset.Name
    write " prefers ",rset.FavoriteColors
    write ", Birth date ",rset.bdate,!!
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
  write !,"End of data"
  write !,"Total row count=",rset.%ROWCOUNT
```

In the above example, one of the fields returned is the FavoriteColors field, which contains %List data. To display this data, the `%New(1)` class method sets the %SelectMode property parameter to 1 (ODBC), causing this program to display %List data as a comma-separated string and the birth date in ODBC format:

The following example returns the Home_State field. Because a property name cannot contain an underscore character, this example specifies the field name (the SqlFieldName) delimited with quotation marks ("Home_State"). You could also specify the corresponding generated property name without quotation marks (HomeState). Note that the delimited field name ("Home_State") is not case-sensitive, but the generated property name (HomeState) is case-sensitive:

```objectscript
  set query = "SELECT TOP 5 Name,Home_State FROM Sample.Person"
  set statement = ##class(%SQL.Statement).%New(2)

  set status = statement.%Prepare(query)
  if $$$ISERR(status) {write "%Prepare failed:" do $SYSTEM.Status.DisplayError(status) quit}

  set rset = statement.%Execute()
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  while rset.%Next()
  {
     write "Row count ",rset.%ROWCOUNT,!
     write rset.Name
     write " lives in ",rset."Home_State",!
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
  write !,"End of data"
  write !,"Total row count=",rset.%ROWCOUNT
```

#### Swizzling a Fieldname Property with %ObjectSelectMode=1

The following example is prepared with %ObjectSelectMode=1, which causes fields whose type class is a swizzleable type (a persistent class, a serial class, or a stream class) to automatically swizzle when returning a value using the field name property. The result of swizzling a field value is the corresponding object reference (OREF). InterSystems IRIS does not perform this swizzling operation when accessing a field using the `%Get()` or `%GetData()` methods. In this example, `rset.Home` is swizzled, while `rset.%GetData(2)`, which refers to the same field, is not swizzled:

```objectscript
  set query = "SELECT TOP 5 Name,Home FROM Sample.Person"
  set statement = ##class(%SQL.Statement).%New(0)
  set statement.%ObjectSelectMode = 1
  write !,"set ObjectSelectMode=",statement.%ObjectSelectMode,!

  set status = statement.%Prepare(query)
  if $$$ISERR(status) {write "%Prepare failed:" do $SYSTEM.Status.DisplayError(status) quit}

  set rset = statement.%Execute()
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  while rset.%Next()
  {
     write "Row count: ",rset.%ROWCOUNT,!
     write rset.Name,!
     write " ",rset.Home,!
     write rset.%GetData(1)
     write " ",$listtostring(rset.%GetData(2)),!!
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
  write !,"End of data"
  write !,"Total row count=",rset.%ROWCOUNT
```

The following example uses `%ObjectSelectMode`=1 to derive Home_State values for the selected records from the unique record ID (%ID). Note that the Home_State field is not selected in the original query:

```objectscript
  set query = "SELECT TOP 5 %ID AS MyID,Name,Age FROM Sample.Person"
  set statement = ##class(%SQL.Statement).%New()
  set statement.%ObjectSelectMode=1

  set status = statement.%Prepare(query)
  if $$$ISERR(status) {write "%Prepare failed:" do $SYSTEM.Status.DisplayError(status) quit}

  set rset = statement.%Execute()
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  while rset.%Next()
  {
     write rset.Name
     write " Home State:",rset.MyID.Home.State,!
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
  write !,"End of data"
  write !,"Total row count=",rset.%ROWCOUNT
```

If configured, the system generates a <SWIZZLE FAIL> error if the swizzled property is defined but cannot be referenced. This can occur if the referenced property has been unexpectedly deleted from disk or is locked by another process. To determine the cause of the swizzle failure look in %objlasterror immediately after the <SWIZZLE FAIL> error and decode this %Status value.

By default, <SWIZZLE FAIL> is not configured. You can set this behavior globally by setting `set ^%SYS("ThrowSwizzleError")=1`, or by using the InterSystems IRIS Management Portal. From `System Administration`, select `Configuration`, then `SQL and Object Settings`, then `Objects`. On this screen you can set the <SWIZZLE FAIL> option.

### %Get("fieldname") Method

You can use the %Get("fieldname") instance method to return a data value by field name or field name alias. Dynamic SQL resolves letter case as needed. If the specified field name or field name alias does not exist, the system generates a <PROPERTY DOES NOT EXIST> error.

The following example returns values for the Home_State field and the Last_Name alias from the query result set.

```objectscript
  set query = "SELECT TOP 5 Home_State,Name AS Last_Name FROM Sample.Person"
  set statement = ##class(%SQL.Statement).%New(2)

  set status = statement.%Prepare(query)
  if $$$ISERR(status) {write "%Prepare failed:" do $SYSTEM.Status.DisplayError(status) quit}

  set rset = statement.%Execute()
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  while rset.%Next()
  {
    write rset.%Get("Home_State")," : ",rset.%Get("Last_Name"),!
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
  write !,"End of data"
  write !,"Total row count=",rset.%ROWCOUNT
```

You must use the %Get("fieldname") instance method to retrieve individual data items by field property name from an existing query prepared using %PrepareClassQuery(). If the field property name does not exist, the system generates a <PROPERTY DOES NOT EXIST> error.

The following example returns the Nsp (namespace) field values by field property name from a built-in query. Because this query is an existing stored query, this field retrieval requires the use of the `%Get("fieldname")` method. Note that because "Nsp" is a property name, it is case-sensitive:

```objectscript
  set statement = ##class(%SQL.Statement).%New(2)
  set status = statement.%PrepareClassQuery("%SYS.Namespace","List")
  if $$$ISERR(status) {write "%Prepare failed:" do $SYSTEM.Status.DisplayError(status) quit}

  set rset = statement.%Execute()
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  while rset.%Next()
  {
     write "Namespace: ",rset.%Get("Nsp"),!
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
  write !,"End of data"
  write !,"Total row count=",rset.%ROWCOUNT
```

Duplicate Names: Names are duplicate if they resolve to the same property name. Duplicate names can be multiple references to the same field, references to different fields in a table, or references to fields in different tables. If the `SELECT` statement contains multiple instances of the same field name or field name alias, `%Get("fieldname")` always returns the last instance of a duplicate name as specified in the query. This is the opposite of `rset.PropName`, which returns the first instance of a duplicate name as specified in the query. This is shown in the following example:

```objectscript
  set query = "SELECT c.Name,p.Name FROM Sample.Person AS p,Sample.Company AS c"
  set statement = ##class(%SQL.Statement).%New()

  set status = statement.%Prepare(query)
  if $$$ISERR(status) {write "%Prepare failed:" do $SYSTEM.Status.DisplayError(status) quit}

  set rset = statement.%Execute()
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  while rset.%Next()
  {
    write "Prop=",rset.Name," Get=",rset.%Get("Name"),!
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
  write !,rset.%ROWCOUNT," End of data"
```

### %GetData(n) Method

The %GetData(n) instance method returns data for the current row indexed by the integer count column number of the result set. You can use `%GetData(n)` with either a specified query prepared using `%Prepare()` or a stored query prepared using `%PrepareClassQuery()`.

The integer `n` corresponds to the sequence of the `select-item` list specified in the query. The RowID field is not given an integer `n` value, unless explicitly specified in the `select-item` list. If `n` is higher than the number of `select-item`s in the query, or 0, or a negative number, Dynamic SQL returns no value and issues no error.

`%GetData(n)` is the only way to return a specific duplicate field name or duplicate alias; `rset.Name` returns the first duplicate, `%Get("Name")` returns the last duplicate.

```objectscript
  set query = "SELECT TOP 5 Name,SSN,Age FROM Sample.Person"
  set statement = ##class(%SQL.Statement).%New()

  set status = statement.%Prepare(query)
  if $$$ISERR(status) {write "%Prepare failed:" do $SYSTEM.Status.DisplayError(status) quit}

  set rset = statement.%Execute()
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  while rset.%Next()
  {
    write "Years:",rset.%GetData(3)," Name:",rset.%GetData(1),!
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
  write "End of data"
  write !,"Total row count=",rset.%ROWCOUNT
```

## Returning Multiple Result Sets

A CALL statement can return multiple dynamic result sets as a collection referred to as a result set sequence (RSS).

The following example uses the %NextResult() method to return multiple result sets separately:

```objectscript
  set mycall = "CALL Sample.CustomSets()"
  set rset = ##class(%SQL.Statement).%ExecDirect(,mycall)
  if rset.%SQLCODE'=0 {write !,"ExecDirect SQLCODE=",rset.%SQLCODE,!,rset.%Message  quit}

  set rset1 = rset.%NextResult()
  do rset1.%Display()
  write !,"End of 1st Result Set data",!!

  set rset2 = rset.%NextResult()
  do rset2.%Display()
  write !,"End of 2nd Result Set data"
```

## SQL Metadata

Dynamic SQL provides the following types of metadata:

*   After a Prepare, metadata describing the type of query.
    
*   After a Prepare, metadata describing the select-items in the query (`Columns` and `Extended Column Info`).
    
*   After a Prepare, metadata describing the query arguments: ? parameters, `:var` parameters, and constants. (`Statement Parameters`, `Formal Parameters`, and `Objects`)
    
*   After an Execute, metadata describing the query result set.
    

%SQL.StatementMetadata property values are available following a Prepare operation (`%Prepare()`, `%PrepareClassQuery()`, or `%ExecDirect()`).

*   You can return %SQL.StatementMetadata properties directly for the most recent `%Prepare()`.
    
*   You can return the %SQL.Statement `%Metadata` property containing the OREF for the %SQL.StatementMetadata properties. This enables you to return metadata for multiple Prepare operations.
    

A `SELECT` or `CALL` statement returns all of this metadata. An `INSERT`, `UPDATE`, or `DELETE` returns Statement Type Metadata and the `Formal Parameters`.

### Statement Type Metadata

Following a Prepare using the %SQL.Statement class, you can use the %SQL.StatementMetadata `statementType` property to determine what type of SQL statement was prepared, as shown in the following example. This example uses the %SQL.Statement `%Metadata` property to preserve and compare the metadata for two Prepare operations:

```objectscript
   set tStatement = ##class(%SQL.Statement).%New()
   set myquery1 = "SELECT TOP ? Name,Age,AVG(Age),CURRENT_DATE FROM Sample.Person"
   set myquery2 = "CALL Sample.SP_Sample_By_Name(?)"
   set qStatus = tStatement.%Prepare(myquery1)
    if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
    set meta1 = tStatement.%Metadata
     set qStatus = tStatement.%Prepare(myquery2)
    if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
    set meta2 = tStatement.%Metadata
  write "Statement type query 1: ",meta1.statementType,!
  write "Statement type query 2: ",meta2.statementType,!
  write "End of metadata"
```

The `Class Reference` entry for the statementType property lists the statement type integer codes. The most common codes are 1 (a SELECT query) and 45 (a CALL to a stored query).

You can return the same information using the %GetImplementationDetails() instance method, as described in Results of a Successful Prepare.

After executing a query, you can return the statement type name (for example, SELECT) from the result set.

### Select-item Metadata

Following a Prepare of a `SELECT` or `CALL` statement using the %SQL.Statement class, you can return metadata about each select-item column specified in the query, either by displaying all of the metadata or by specifying individual metadata items. This column metadata includes ODBC data type information, as well as client type and InterSystems Objects property origins and class type information.

The following example returns the number of columns specified in the most recently prepared query:

```objectscript
  set myquery = "SELECT %ID AS id,Name,DOB,Age,AVG(Age),CURRENT_DATE,Home_State FROM Sample.Person"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(myquery)
    if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  write "Number of columns=",tStatement.%Metadata.columnCount,!
  write "End of metadata"
```

The following example returns the column name (or column alias), ODBC data type, maximum data length (precision), and scale for each select-item field:

```objectscript
  set $NAMESPACE="SAMPLES"
  set myquery=2
  set myquery(1)="SELECT Name AS VendorName,LastPayDate,MinPayment,NetDays,"
  set myquery(2)="AVG(MinPayment),$HOROLOG,%TABLENAME FROM Sample.Vendor"
  set rset = ##class(%SQL.Statement).%New()
  set qStatus = rset.%Prepare(.myquery)
    if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  set x=rset.%Metadata.columns.Count()
  set x=1
  while rset.%Metadata.columns.GetAt(x) {
    set column=rset.%Metadata.columns.GetAt(x)
    write !,x," ",column.colName," is data type ",column.ODBCType
    write " with a size of ",column.precision," and scale = ",column.scale
    set x=x+1 }
  write !,"End of metadata"
```

The following example displays all of the column metadata using the %SQL.StatementMetadata %Display() instance method:

```objectscript
  set query = "SELECT %ID AS id,Name,DOB,Age,AVG(Age),CURRENT_DATE,Home_State FROM Sample.Person"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(query)
  if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  do tStatement.%Metadata.%Display()
  write !,"End of metadata"
```

This returns two table listings of the selected fields. The first columns metadata table lists column definition information:

<table><tr><th>Display Header</th><th><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25SQL.StatementColumn">%SQL.StatementColumn</a> Property</th><th>Description</th></tr><tr><td>Column Name</td><td>colName</td><td><p>The <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_createtable#RSQL_createtable_args_column">SQL name of the column</a>. If the column is given an alias, the <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_select#RSQL_select_args_columnalias">column alias</a>, not the field name, is listed here. Names and aliases are truncated to 12 characters.</p><p>For an expression, aggregate, literal, host variable, or subquery, the assigned “Expression_n”, “Aggregate_n”, “Literal_n”, “HostVar_n”, or “Subquery_n” label is listed (with <code>n</code> being the SELECT item sequence number). If you have assigned an alias to an expression, aggregate, literal, host variable, or subquery, the alias is listed here.</p></td></tr><tr><td>Type</td><td>ODBCType</td><td>The integer code for the ODBC data type. These codes are listed in <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_datatype#RSQL_datatype_intcodes">Integer Codes for Data Types</a>. Note that these ODBC data type codes are not the same as the CType data type codes.</td></tr><tr><td>Prec</td><td>precision</td><td>The <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_datatype#RSQL_datatype_pands">precision</a> or <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_datatype#RSQL_datatype_maxlen">maximum length</a>, in characters. Precision and scale metadata for TIME data types are described in <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_datatype#RSQL_datatype_date">Date, Time, PosixTime, and TimeStamp Data Types</a>.</td></tr><tr><td>Scale</td><td>scale</td><td>The maximum number of <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_datatype#RSQL_datatype_pands">fractional decimal digits</a>. Returns 0 for integer or non-numeric values. Precision and scale metadata for TIME data types are described in <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_datatype#RSQL_datatype_date">Date, Time, PosixTime, and TimeStamp Data Types</a>.</td></tr><tr><td>Null</td><td>isNullable</td><td>An integer value that indicates whether the column is defined as Non-NULL (0), or if NULL is permitted (1). The RowID returns 0. If the SELECT item is an aggregate or subquery that could result in NULL, or if it specifies the NULL literal, this item is set to 1. If the SELECT item is an expression or host variable, this item is set to 2 (cannot be determined).</td></tr><tr><td>Label</td><td>label</td><td>The <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_createtable#RSQL_createtable_args_column">column name</a> or <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_select#RSQL_select_args_columnalias">column alias</a> (same as Column Name).</td></tr><tr><td>Table</td><td>tableName</td><td>The <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_tables#GSQL_tables_names">SQL table name</a>. The actual table name is always listed here, even if you have given the table an alias. If the SELECT item is an expression or an aggregate no table name is listed. If the SELECT item is a subquery, the subquery table name is listed.</td></tr><tr><td>Schema</td><td>schemaName</td><td>The table’s <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_tables#GSQL_tables_schema">schema name</a>. If no schema name was specified, returns the <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_tables#GSQL_tables_schemadefault">system-wide default schema</a>. If the SELECT item is an expression or an aggregate no schema name is listed. If the SELECT item is a subquery no schema name is listed.</td></tr><tr><td>CType</td><td>clientType</td><td>The integer code for the client data type. See the <a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25SQL.StatementColumn">%SQL.StatementColumn</a> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25SQL.StatementColumn#PROPERTY_clientType">clientType</a> property for a list of values.</td></tr></table>

The second columns metadata table lists extended column information. The Extended Column Info table lists each column with twelve boolean flags (SQLRESULTCOL), specified as Y (Yes) or N (No):

<table><tr><th>Boolean Flag</th><th><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25SQL.StatementColumn">%SQL.StatementColumn</a> Property</th><th>Description</th></tr><tr><td>1: AutoIncrement</td><td>isAutoIncrement</td><td>The RowID and IDENTITY fields returns Y.</td></tr><tr><td>2: CaseSensitive</td><td>isCaseSensitive</td><td><p>A string data type field with <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_createtable#RSQL_createtable_desc_collation">%EXACT collation</a> returns Y.</p><p>A property that references a <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_tables#GSQL_tables_via_classes_serialobject">%SerialObject embedded object</a> returns Y.</p></td></tr><tr><td>3: Currency</td><td>isCurrency</td><td>A field defined with a data type of <a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25Library.Currency">%Library.Currency</a>, such as the MONEY data type.</td></tr><tr><td>4: ReadOnly</td><td>isReadOnly</td><td>An Expression, Aggregate, Literal, HostVar, or Subquery returns Y. The RowID, IDENTITY, and RowVersion fields returns Y.</td></tr><tr><td>5: RowVersion</td><td>isRowVersion</td><td>The <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_createtable#RSQL_createtable_desc_counters">RowVersion</a> field returns Y.</td></tr><tr><td>6: Unique</td><td>isUnique</td><td>A field defined as having a <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_createtable#RSQL_createtable_desc_unique">unique value constraint</a>. The RowID and IDENTITY fields returns Y.</td></tr><tr><td>7: Aliased</td><td>isAliased</td><td>The system supplies an alias to a non-field select-item. Therefore, an Expression, Aggregate, Literal, HostVar, or Subquery returns Y, whether or not the user replaced the system alias by specifying a column alias. This flag is not affected by user-specified column aliases.</td></tr><tr><td>8: Expression</td><td>isExpression</td><td>An Expression returns Y.</td></tr><tr><td>9: Hidden</td><td>isHidden</td><td>If the table is defined with <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_createtable#RSQL_createtable_desc_publicrowid">%PUBLICROWID</a> or <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=ROBJ_class_sqlrowidprivate">SqlRowIdPrivate</a>=0 (the default), the RowID field returns N. Otherwise, the RowID field returns Y. A property that references a <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_tables#GSQL_tables_via_classes_serialobject">%SerialObject embedded object</a> returns Y.</td></tr><tr><td>10: Identity</td><td>isIdentity</td><td>A field defined as an <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_createtable#RSQL_createtable_idfield">IDENTITY field</a> returns Y. The RowID field if the<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_tables#GSQL_tables_idfield_hidden"> RowID is not hidden</a> returns Y.</td></tr><tr><td>11: KeyColumn</td><td>isKeyColumn</td><td>A field defined as a primary key field or the target of a <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_createtable#RSQL_createtable_desc_fkey">foreign key constraint</a>. The RowID field returns Y.</td></tr><tr><td>12: RowID</td><td>isRowId</td><td>The RowID and IDENTITY fields returns Y.</td></tr><tr><td>13: isList</td><td>isList</td><td><p>A field defined as <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_datatype#RSQL_datatype_lists">data type %Library.List</a> or %Library.ListOfBinary, or a field that is a list or array collection returns Y. CType (client data type)=6.</p><p>An expression using the <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_d_listbuild">$LISTBUILD</a> or <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RSQL_d_listfromstring">$LISTFROMSTRING</a> function to generate a list returns Y.</p></td></tr></table>

The Extended Column Info metadata table lists the `Column Name` (the SQL name or column alias), the `Linked Prop` (linked persistent class property) and `Type Class` (data type class) for each of the selected fields. Note that the `Linked Prop` lists the persistent class name (not the SQL table name) and the property name (not the column alias).

*   For an ordinary table field (`SELECT Name FROM Sample.Person`): `Linked Prop`=Sample.Person.Name, `Type Class`=%Library.String.
    
*   For the table’s RowID (`SELECT %ID FROM Sample.Person`): `Linked Prop`= [none], `Type Class`=Sample.Person.
    
*   For an Expression, Aggregate, Literal, HostVar, or Subquery (`SELECT COUNT(Name) FROM Sample.Person`): `Linked Prop`= [none], `Type Class`=%Library.BigInt.
    
*   For a referenced %SerialObject embedded object property (`SELECT Home_State FROM Sample.Person`). `Linked Prop`=Sample.Address.State, `Type Class`=%Library.String.
    
*   For a field referencing a %SerialObject embedded object (`SELECT Home FROM Sample.Person`). `Linked Prop`=Sample.Person.Home, `Type Class`=Sample.Address.
    

In this example, the Home_State field in Sample.Person references the State property of the %SerialObject class Sample.Address.

The following example returns the metadata for a called stored procedure with one formal parameter, which is also a statement parameter:

```objectscript
  set mysql = "CALL Sample.SP_Sample_By_Name(?)"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(.mysql)
    if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  do tStatement.%Metadata.%Display()
  write !,"End of metadata"
```

It returns not only column (field) information, but also values for Statement Parameters, Formal Parameters, and Objects.

The following example returns the metadata for a with three formal parameters. One of these three parameters is designated with a question mark (?) making it a statement parameter:

```objectscript
  set mycall = "CALL personsets(?,'MA')"
  set tStatement = ##class(%SQL.Statement).%New(0,"sample")
  set qStatus = tStatement.%Prepare(mycall)
    if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  do tStatement.%Metadata.%Display()
  write !,"End of metadata"
```

Note that this metadata returns no column information, but the Statement Parameters, Formal Parameters lists contain the column names and data types.

### Query Arguments Metadata

Following a Prepare using the %SQL.Statement class, you can return metadata about query arguments: input parameters (specified as a question mark (?)), input host variables (specified as `:varname`), and constants (literal values). The following metadata can be returned:

*   Count of ? parameters: parameterCount property
    
*   ODBC data types of ? parameters: %SQL.StatementMetadata %Display() instance method Statement Parameters list.
    
*   List of ?, v (`:var`), and c (constant) parameters: %GetImplementationDetails() instance method, as described in Results of a Successful Prepare.
    
*   ODBC data types of ?, v (`:var`), and c (constant) parameters: formalParameters property.
    
    %SQL.StatementMetadata %Display() instance method Formal Parameters list.
    
*   Text of query showing these arguments: %GetImplementationDetails() instance method, as described in Results of a Successful Prepare.
    

The statement metadata `%Display()` method lists the Statement Parameters and Formal parameters. For each parameter it lists the sequential parameter number, ODBC data type, precision, scale, whether it is nullable (2 means that a value is always supplied), and its corresponding property name (colName), and column type.

Note that some ODBC data types are returned as negative integers. For a table of ODBC data type integer codes, see Data Types.

The following example returns the ODBC data types of each of the query arguments (?, `:var`, and constants) in order. Note that the TOP argument is returned as data type 12 (VARCHAR) rather than 4 (INTEGER) because it is possible to specify TOP ALL:

```objectscript
  set myquery = 4
  set myquery(1) = "SELECT TOP ? Name,DOB,Age+10 "
  set myquery(2) = "FROM Sample.Person"
  set myquery(3) = "WHERE %ID BETWEEN :startid :endid AND DOB=?"
  set myquery(4) = "ORDER BY $PIECE(Name,',',?)"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(.myquery)
    if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  set prepmeta = tStatement.%Metadata
  write "Number of ? parameters=",prepmeta.parameterCount,!
  set formalobj = prepmeta.formalParameters
  set i=1
  while formalobj.GetAt(i) {
     set prop=formalobj.GetAt(i)
     write prop.colName," type= ",prop.ODBCType,!
     set i=i+1 }
  write "End of metadata"
```

Following an Execute, arguments metadata is not available from the query result set metadata. In a result set all parameters are resolved. Therefore `parameterCount` = 0, and `formalParameters` contains no data.

### Query Result Set Metadata

Following an Execute using the %SQL.Statement class, you can return result set metadata by invoking:

*   %SQL.StatementResult class properties.
    
*   %SQL.StatementResult %GetMetadata() method, accessing %SQL.StatementMetadata class properties.
    

#### %SQL.StatementResult Properties

Following an Execute query operation, %SQL.StatementResult returns:

*   The %StatementType property returns an integer code that corresponds to the SQL statement most recently executed. The following is a partial list of these integer codes: 1 = `SELECT`; 2 = `INSERT`; 3 = `UPDATE`; 4 = `DELETE` or `TRUNCATE TABLE`; 9 = `CREATE TABLE`; 15 = `CREATE INDEX`; 45 = `CALL`. For a complete list of these values, see %SQL.StatementResult.
    
*   The %StatementTypeName calculated property returns the command name of the SQL statement most recently executed, based on the `%StatementType`. This name is returned in uppercase letters. Note that a `TRUNCATE TABLE` operation is returned as DELETE. An `INSERT OR UPDATE` is returned as INSERT, even when it performed an update operation.
    
*   The %ResultColumnCount property returns the number of columns in the result set rows.
    

The following example shows these properties:

```objectscript
  set myquery = "SELECT TOP ? Name,DOB,Age FROM Sample.Person WHERE Age > ?"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(myquery)
    if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
  set rset = tStatement.%Execute(10,55)
  if rset.%SQLCODE=0 {
  write "Statement type=",rset.%StatementType,!
  write "Statement name=",rset.%StatementTypeName,!
  write "Column count=",rset.%ResultColumnCount,!
  write "End of metadata" }
  else { write !,"SQLCODE=",rset.%SQLCODE," ",rset.%Message }
```

#### %SQL.StatementResult %GetMetadata()

Following an Execute, you can use the %SQL.StatementResult %GetMetadata() method to access the %SQL.StatementMetadata class properties. These are the same properties accessed by the %SQL.Statement `%Metadata` property following a Prepare.

The following example shows the properties:

```objectscript
  set myquery=2
  set myquery(1)="SELECT Name AS VendorName,LastPayDate,MinPayment,NetDays,"
  set myquery(2)="AVG(MinPayment),$HOROLOG,%TABLENAME FROM Sample.Vendor"
  set tStatement = ##class(%SQL.Statement).%New()
  set qStatus = tStatement.%Prepare(.myquery)
    if qStatus'=1 {write "%Prepare failed:" do $System.Status.DisplayError(qStatus) quit}
    set rset = tStatement.%Execute()
  if rset.%SQLCODE=0 {
  set rsmeta=rset.%GetMetadata()
  set x=rsmeta.columns.Count()
  set x=1
  while rsmeta.columns.GetAt(x) {
    set column=rsmeta.columns.GetAt(x)
    write !,x," ",column.colName," is data type ",column.ODBCType
    write " with a size of ",column.precision," and scale = ",column.scale
    set x=x+1 }
  }
  else { write !,"SQLCODE=",rset.%SQLCODE," ",rset.%Message }
  write !,"End of metadata"
```

Note that the result set metadata does not provide arguments metadata. This is because the Execute operation resolves all parameters. Therefore, in a result set, `parameterCount` = 0, and `formalParameters` contains no data.

## Auditing Dynamic SQL

InterSystems IRIS supports optional auditing of Dynamic SQL statements. Dynamic SQL auditing is performed when the %System/%SQL/DynamicStatement system audit event is enabled. By default, this system audit event is not enabled.

If you enable %System/%SQL/DynamicStatement, the system automatically audits every %SQL.Statement dynamic statement that is executed system-wide. Auditing records information in the Audit Database.

To view the Audit Database, go to the Management Portal, `System Administration`, select `Security`, then `Auditing`, then `View Audit Database`. You can set the `Event Name` filter to DynamicStatement to limit the `View Audit Database` to Dynamic SQL statements. The Audit Database lists Time (a local timestamp), User, PID (process ID), and the Description of the event. The Description specifies the type of Dynamic SQL statement. For example, `SQL SELECT Statement (%SQL.Statement)` or `SQL CREATE VIEW Statement (%SQL.Statement)`.

By selecting the `Details` link for an event you can list additional information, including the `Event Data`. The Event Data includes the SQL statement executed and the values of any arguments to the statement. For example:

```
SELECT TOP ? Name , Age FROM Sample . MyTest WHERE Name %STARTSWITH ?
/*#OPTIONS {"DynamicSQLTypeList":",1"} */
Parameter values:
%CallArgs(1)=5
%CallArgs(2)="Fred"
```

The total length of Event Data, which includes the statement and parameters, is 3,632,952 characters. If the statement and parameters are longer than 3632952, the Event Data will be truncated.

InterSystems IRIS also supports auditing of ODBC and JDBC statements (`Event Name`=XDBCStatement), and auditing of Embedded SQL statements (`Event Name`=EmbeddedStatement).
