# Using Embedded SQL

You can embed SQL statements within ObjectScript code used by InterSystems IRIS data platform. These Embedded SQL statements are converted to optimized, executable code at runtime.

There are two kinds of Embedded SQL:

*   A simple Embedded SQL query can only return values from a single row. Simple Embedded SQL can also be used for single-row insert, update, and delete, and for other SQL operations.
    
*   A cursor-based Embedded SQL query can iterate through a query result set, returning values from multiple rows. Cursor-based Embedded SQL can also be used for multiple row update and delete SQL operations.
    

> **Note:**
> 
> Embedded SQL cannot be input to the Terminal command line, or specified in an XECUTE statement. To execute SQL from the command line, either use the $SYSTEM.SQL.Execute() method or the SQL Shell interface.

## Compiling Embedded SQL

Embedded SQL is not compiled when the routine that contains it is compiled. Instead, compilation of Embedded SQL occurs upon the first execution of the SQL code (runtime). First execution defines an executable cached query. This parallels the compilation of Dynamic SQL, where the SQL code is not compiled until the SQL Prepare operation is executed.

Embedded SQL code is not validated against SQL tables and other entities until the first execution of the routine. Therefore, you can compile a routine or a method of a persistent class containing Embedded SQL that references tables or other SQL entities that do not exist at routine compilation time. For this reason, most SQL errors are returned upon runtime execution, not compilation.

At routine compilation time SQL syntax checking is performed on Embedded SQL. The ObjectScript compiler fails and generates compile errors for invalid SQL syntax in Embedded SQL.

You can use the Management Portal SQL interface to test for the existence of SQL entities specified in Embedded SQL without executing the SQL code. This is described in Validating Embedded SQL Code, which both validates the SQL syntax and checks for the existence of SQL entities. You can choose to validate Embedded SQL code prior to runtime execution by compiling a routine containing Embedded SQL code using the `/compileembedded=1` qualifier, as described in Validating Embedded SQL Code.

A successfully executed Embedded SQL statement generates a cached query. Subsequent execution of that Embedded SQL uses the cached query, rather than recompiling the Embedded SQL source. This provides the performance benefits of cached queries to Embedded SQL. These cached queries are listed in the Management Portal for each table in the `Catalog Details` Cached Queries listing.

Runtime execution of a cursor-based Embedded SQL statement occurs when the cursor is first opened using an `OPEN` command. At this point in execution an optimized cached query plan is generated, as shown in the SQL Statements listing in the Management Portal. The `SQL Statements` listed `Location` is the name of the routine containing the Embedded SQL code. Entries in the `Cached Query` listings with hashed class names, such as `%sqlcq.HSODS.xE6YUuGgukeA8rvZJUTKCaWPmVyd`, indicate Embedded SQL queries; however, entries with non-hashed class names, such as `%sqlcq.USER.cls1` are created by Dynamic SQL queries.

> **Note:**
> 
> The #sqlcompile mode preprocessor statement used in earlier versions of InterSystems IRIS has been deprecated. It is parsed, but no longer performs any operation for most Embedded SQL commands. Most Embedded SQL commands are compiled at runtime regardless of the #sqlcompile mode setting. However, setting #sqlcompile mode=deferred is still meaningful for a small number of Embedded SQL commands because it forces runtime compilation of all types of Embedded SQL commands.

### Embedded SQL and the Macro Preprocessor

You can use Embedded SQL within methods and within triggers (provided that they are defined to use ObjectScript) or within ObjectScript MAC routines. A MAC routine is processed by the Macro Preprocessor and converted to INT (intermediate) code which is subsequently compiled to executable OBJ code. These operations are performed at compile time on the routine containing the Embedded SQL, but not on the Embedded SQL code itself, which is not compiled until runtime. For further details, see Using Macros and Include Files.

If an Embedded SQL statement itself contains Macro Preprocessor statements (# commands, ## functions, or $$$macro references) these statements are compiled when the routine is compiled and are made available to the SQL code at runtime. This may affect `CREATE PROCEDURE`, `CREATE FUNCTION`, `CREATE METHOD`, `CREATE QUERY`, or `CREATE TRIGGER` statements that contain an ObjectScript code body.

#### Include Files in Embedded SQL

Embedded SQL statements require any macro Include files that they reference to be loaded on the system at runtime.

Because the compilation of Embedded SQL is deferred until it is first referenced, the context in which an Embedded SQL class is compiled will be the runtime environment rather than the compile-time environment of the containing class or routine. If the runtime current namespace is different than the containing routine’s compile-time namespace, the Include files in the compile-time namespace may not be visible in the runtime namespace. In this situation the following occurs:

1.  If an Include file is not visible in the runtime namespace, Embedded SQL compilation removes all Include files. Because Include files are rarely needed for SQL compilation, the runtime Embedded SQL compile will often succeed without them.
    
2.  If after removing the Include files the compile fails, the InterSystems IRIS error reports the routine compile-time namespace, the Embedded SQL runtime namespace, and the list of Include files not visible from the runtime namespace.
    

#### The #SQLCompile Macro Directives

The Macro Preprocessor provides three preprocessor directives for use with Embedded SQL:

*   #sqlcompile select specifies the format for data display when returned from a `SELECT` statement, or the required format for data input when specified to an `INSERT` or `UPDATE` statement, or a `SELECT` input host variable. It supports the following six options: `Logical` (the default), `Display`, `ODBC`, `Runtime`, `Text` (synonym for `Display`), and `FDBMS` (see below). If `#sqlcompile select=Runtime`, you can use the $SYSTEM.SQL.Util.SetOption("SelectMode",n) method to change how the data is displayed. The `n` value can be 0=Logical, 1=ODBC, or 2=Display.
    
    Regardless of the `#sqlcompile select` option specified, an `INSERT` or `UPDATE` automatically converts the specified data value to its corresponding Logical format for storage.
    
    Regardless of the `#sqlcompile select` option specified, a `SELECT` automatically converts an input host variable value to its corresponding Logical format for predicate matching.
    
    Using`#sqlcompile select` for query display is shown in the following examples. These examples display the DOB (date of birth) value, then change the SelectMode to ODBC format, then display the DOB again. In the first example, changing the SelectMode has no effect on the display; in the second example, because `#sqlcompile select=Runtime`, changing the SelectMode changes the display:
    
    ```sql
       #sqlcompile select=Display
       &sql(SELECT DOB INTO :a FROM Sample.Person)
          IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
          ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
       WRITE "1st date of birth is ",a,!
       DO $SYSTEM.SQL.Util.SetOption("SelectMode",1)
       WRITE "changed select mode to: ",$SYSTEM.SQL.Util.GetOption("SelectMode"),!
       &sql(SELECT DOB INTO :b FROM Sample.Person)
       WRITE "2nd date of birth is ",b
    ```
    
    ```sql
       #sqlcompile select=Runtime
       &sql(SELECT DOB INTO :a FROM Sample.Person)
          IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
          ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
       WRITE "1st date of birth is ",a,!
       DO $SYSTEM.SQL.Util.SetOption("SelectMode",1)
       WRITE "changed select mode to: ",$SYSTEM.SQL.Util.GetOption("SelectMode"),!
       &sql(SELECT DOB INTO :b FROM Sample.Person)
       WRITE "2nd date of birth is ",b
    ```
    
    For further details on SelectMode options, refer to Data Display Options.
    
    *   `#sqlcompile select=FDBMS` is provided to enable Embedded SQL to format data in the same way as FDBMS. If a query has a constant value in the WHERE clause, FDBMS mode assumes it to be a Display value and converts it using DisplayToLogical conversion. If a query has a variable in the WHERE clause, FDBMS mode converts it using FDBMSToLogical conversion. The FDBMSToLogical conversion method should be designed to handle the three FDBMS variable formats: Internal, Internal_$c(1)_External, and $c(1)_External. If a query selects into a variable, it invokes the LogicalToFDBMS conversion method. This method returns Internal_$c(1)_External.
        
*   #sqlcompile path (or #import) specifies the schema search path used to resolves unqualified table, view, and stored procedure names in data management commands such as `SELECT`, `CALL`, `INSERT`, `UPDATE`, `DELETE`, and `TRUNCATE TABLE`. If no schema search path is specified, or if the table is not found in the specified schemas, InterSystems IRIS uses the default schema. `#sqlcompile path` and `#import` are ignored by data definition statements such as `ALTER TABLE`, `DROP VIEW`, `CREATE INDEX`, or `CREATE TRIGGER`. Data definition statements use the default schema to resolve unqualified names.
    
*   #sqlcompile audit is a boolean switch specifying whether or not the execution of Embedded SQL statements should be recorded in the system events audit log. For further details, refer to Auditing Embedded SQL.
    

For further details on these preprocessor directives, refer to Preprocessor Directives Reference.

## Embedded SQL Syntax

The syntax of the Embedded SQL directive is described below.

### The &sql Directive

Embedded SQL statements are set off from the rest of the code by the &sql() directive, as shown in the following example:

```sql
   NEW SQLCODE,a
   WRITE "Invoking Embedded SQL",!
   &sql(SELECT Name INTO :a FROM Sample.Person)
      IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
      ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
   WRITE "The name is ",a
```

Results are returned using the INTO clause specifying one or more host variables. In this case, the host variable is named `:a`. For further details, see Host Variables, which includes information on interactions between SQLCODE and host variables.

The &sql directive is not case-sensitive; you can use &sql, &SQL, &Sql, and so on. The &sql directive must be followed by an open parenthesis, with no intervening spaces, line breaks, or comments. The &sql directive can be used on the same line as a label, as shown in the following example:

```sql
Mylabel  &sql(
       SELECT Name INTO :a
       FROM Sample.Person
       )
```

The body of an &sql directive should contain a valid Embedded SQL statement, enclosed in parentheses. You can format your SQL statements in any way you like: white space and new lines are ignored by SQL.

When the Macro Preprocessor encounters an &sql directive, it hands the enclosed SQL statement to the SQL Query Processor. The Query Processor returns the code needed (in ObjectScript INT format) to execute the query. The Macro Preprocessor then replaces the &sql directive with this code (or a call to a label containing the code).

If an &sql directive contains an invalid Embedded SQL statement, the Macro Preprocessor generates a compilation error. An invalid SQL statement may have syntax errors, or refer to tables or columns that do not exist at compile time. Refer to Validating Embedded SQL Code.

An &sql directive can contain SQL-style comments anywhere within its parentheses, can contain no SQL code, or contain only comment text. If an &sql directive contains no SQL code or only commented text, the directive is parsed as a no-op and the SQLCODE variable is not defined.

```objectscript
  NEW SQLCODE
  WRITE !,"Entering Embedded SQL"
  &sql()
  WRITE !,"Leaving Embedded SQL"
```

```sql
  NEW SQLCODE
  WRITE !,"Entering Embedded SQL"
  &sql(/* SELECT Name INTO :a FROM Sample.Person */)
  WRITE !,"Leaving Embedded SQL"
```

### &sql Alternative Syntax

Because complex Embedded SQL programs may contain multiple &sql directives — including nested &sql directives — the following alternative syntax formats are provided:

*   `##sql(...)`: this directive is functionally equivalent to &sql. It provides an alternative syntax for clarity of code. However, it cannot include marker syntax.
    
*   `&sql<marker>(...)<reversemarker>`: this directive allows you to specify multiple &sql directives, identifying each with a user-selected marker character or string. This marker syntax is described in the following section.
    

### &sql Marker Syntax

You can identify a specific &sql directive using user-defined marker syntax. This syntax consists of a character or string specified between “&sql” and the open parenthesis character. The reverse of this marker must appear immediately after the closing parenthesis at the end of the Embedded SQL. The syntax is as follows:

```
  &sql<marker>( SQL statement )<reverse-marker>
```

Note that no white space (space, tab, or line return) is permitted between &sql, `marker`, and the open parenthesis, and no white space is permitted between the closing parenthesis and `reverse-marker`.

A `marker` can be a single character or a series of characters. A `marker` cannot contain the following punctuation characters:

```
( + - / \ | * )
```

A `marker` cannot contain a whitespace character (space, tab, or line return). It may contain all other printable characters and combinations of characters, including Unicode characters. The `marker` and `reverse-marker` are case-sensitive.

The corresponding `reverse-marker` must contain the same characters as `marker` in the reverse order. For example: `&sqlABC( ... )CBA`. If `marker` contains a [ or { character, `reverse-marker` must contain the corresponding ] or } character. The following are examples of valid &sql `marker` and `reverse-marker` pairs:

```
  &sql@@( ... )@@   &sql[( ... )]   &sqltest( ... )tset   &sql[Aa{( ... )}aA]
```

When selecting a marker character or string, note the following important SQL restriction: the SQL code cannot contain the character sequence “`)<reversemarker>`” anywhere in the code, including in literal strings and comments. For example, if the marker is “ABC”, the character string “)CBA” cannot appear anywhere in the Embedded SQL code. If this occurs, the combination of a valid marker and valid SQL code will fail compilation. Thus it is important to use care in selecting a `marker` character or string to prevent this collision.

### Embedded SQL and Line Offsets

The presence of Embedded SQL affects ObjectScript line offsets, as follows:

*   Embedded SQL adds (at least) 2 to the total number of INT code lines at that point in the routine. Therefore, a single line of Embedded SQL counts as 3 lines, two lines of Embedded SQL count as 4 lines, and so forth. Embedded SQL that invokes other code can add many more lines to the INT code.
    
    A dummy Embedded SQL statement, containing only a comment counts as 2 INT code lines, as in the following example: `&sql( /* for future use */)`.
    
*   All lines within Embedded SQL count as line offsets, including comments and blank lines.
    

You can display INT code lines using the ^ROUTINE global.

## Embedded SQL Code

Considerations for writing SQL code in Embedded SQL include the following:

*   Simple (non-cursor) Embedded SQL statements
    
*   Schema name resolution
    
*   Literal data values
    
*   Data formatting for %List and date/time data values
    
*   Privilege Checking
    

Host variables, which are used to export data values from Embedded SQL are described later on this page.

### Simple SQL Statements

You can use a simple SQL statement (a single Embedded SQL statement) for a variety of operations including:

*   INSERT, UPDATE, INSERT OR UPDATE, and DELETE statements.
    
*   DDL statements.
    
*   GRANT and REVOKE statements.
    
*   SELECT statements that return only a single row (or if you are only interested in the first returned row).
    

Simple SQL statements are also referred to as non-cursor–based SQL statements. Also see Cursor-based Embedded SQL.

For example, the following statement finds the name of the (one and only) `Patient` with ID of 43:

```sql
 &sql(SELECT Name INTO :name
    FROM Patient
    WHERE %ID = 43)
```

If you use a simple statement for a query that can return multiple rows, then only the first row is returned:

```sql
 &sql(SELECT Name INTO :name
    FROM Patient
    WHERE Age = 43)
```

Depending on the query, there is no guarantee which row will actually be returned first.

The INTO clause output host variables are set to the null string when Embedded SQL is compiled. For this reason, an simple Embedded SQL statement should test for SQLCODE=100 (query returns no data), or SQLCODE=0 (successful execution) before accessing output host variables.

### Schema Name Resolution

A table name, view name, or stored procedure name is either qualified (specifies a schema name) or unqualified (does not specify a schema name). If the name does not specify a schema name, InterSystems IRIS resolves the schema name as follows:

*   Data Definition: InterSystems IRIS uses the system-wide default schema to resolve an unqualified name. If the default schema does not exist, InterSystems IRIS creates the schema and the corresponding class package. All data definition statements use the system-wide default schema; data definition statements ignore the `#import` and `#sqlcompile path` macro preprocessor directives.
    
*   Data Management: InterSystems IRIS uses the schema search path specified by the #sqlcompile path and/or the #import macro preprocessor directive(s) in effect for the class or routine that contains the Embedded SQL statement. The `#import` and `#sqlcompile path` directives are mutually independent lists of possible schema names with different functionality. Either or both may be used to supply a schema name for an unqualified table, view, or stored procedure name. If no schema search path is specified, InterSystems IRIS uses the system-wide default schema name.
    

See Packages for more details on schemas.

### Literal Values

Embedded SQL queries may contain literal values (strings, numbers, or dates). Strings should be enclosed within single (') quotes. (In InterSystems SQL, double quotes specify a delimited identifier):

```sql
  &sql(SELECT 'Employee (' || Name || ')' INTO :name
       FROM Sample.Employee)
          IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
          ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
  WRITE name
```

Numeric values can be used directly. Literal numbers and timestamp values are “lightly normalized” before InterSystems IRIS compares these literal values to field values, as shown in the following example where +0050.000 is normalized to 50:

```sql
  &sql(SELECT Name,Age INTO :name,:age
       FROM Sample.Person
       WHERE Age = +0050.000)
         IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
         ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
  WRITE name," age=",age
```

Arithmetic, function, and special variable expressions can be specified:

```sql
  &sql(DECLARE C1 CURSOR FOR
       SELECT Name,Age-65,$HOROLOG INTO :name,:retire,:today
       FROM Sample.Person
       WHERE Age > 60
       ORDER BY Age,Name)
  &sql(OPEN C1)
      QUIT:(SQLCODE'=0)
  &sql(FETCH C1)
  WHILE (SQLCODE = 0) {
     WRITE $ZDATE(today)," ",name," has ",retire," eligibility years",!
    &sql(FETCH C1) }
  &sql(CLOSE C1)
```

You can also input a literal value using an input host variable. Input host numeric values are also “lightly normalized.” For further details, see Host Variables.

In Embedded SQL, a few character sequences that begin with ## are not permitted within a string literal and must be specified using ##lit. These character sequences are: `##;`, `##beginlit`, `##expression(`, `##function(`, `##quote(`, `##stripq(`, and `##unique(`. For example, the following example fails:

```sql
  WRITE "Embedded SQL test",!
  &sql(SELECT 'the sequence ##unique( is restricted' INTO :x)
  WRITE x
```

The following workaround succeeds:

```sql
  WRITE "Embedded SQL test",!
  &sql(SELECT 'the sequence ##lit(##unique() is restricted' INTO :x)
  WRITE x
```

### Data Format

Within Embedded SQL, data values are in “Logical mode”; that is, values are in the native format used by the SQL Query Processor. For string, integers, and other data types that do not define a `LogicalToOdbc` or `LogicalToDisplay` conversion, this has no effect. Data format affects %List data, and the %Date and %Time data types.

The %List data type displays in Logical mode as element values prefaced with non-printing list encoding characters. The `WRITE` command displays these values as concatenated elements. For example, the FavoriteColors field of Sample.Person stores data in %List data type, such as the following: `$LISTBUILD('Red','Black')`. In Embedded SQL this displays in Logical mode as `RedBlack`, with a length of 12 characters. In Display mode it displays as `Red Black`; in ODBC mode it displays as `Red,Black`. This is shown in the following example:

```sql
  &sql(DECLARE C1 CURSOR FOR
       SELECT TOP 10 FavoriteColors INTO :colors
       FROM Sample.Person WHERE FavoriteColors IS NOT NULL)
  &sql(OPEN C1)
      QUIT:(SQLCODE'=0)
  &sql(FETCH C1)
  WHILE (SQLCODE = 0) {
     WRITE $LENGTH(colors),": ",colors,!
    &sql(FETCH C1) }
  &sql(CLOSE C1)
```

The %Date and %Time data types provided by InterSystems IRIS use the InterSystems IRIS internal date representation ($HOROLOG format) as their Logical format. A %Date data type returns INTEGER data type values in Logical mode; VARCHAR data type values in Display mode, and DATE data type values in ODBC mode. The %TimeStamp data type uses ODBC date-time format (YYYY-MM-DD HH:MM:SS) for its Logical, Display, and ODBC format.

For example, consider the following class definition:

```objectscript
Class MyApp.Patient Extends %Persistent
{
/// Patient name
Property Name As %String(MAXLEN = 50);

/// Date of birth
Property DOB As %Date;

/// Date and time of last visit
Property LastVisit As %TimeStamp;
}
```

A simple Embedded SQL query against this table will return values in logical mode. For example, consider the following query:

```sql
 &sql(SELECT Name, DOB, LastVisit
        INTO :name, :dob, :visit
         FROM Patient
        WHERE %ID = :id)
```

This query returns logical value for the three properties into the host variables `name`, `dob`, and `visit`:

<table><tr><th>Host Variable</th><th>Value</th></tr><tr><td><code>name</code></td><td>"Weiss,Blanche"</td></tr><tr><td><code>dob</code></td><td>44051</td></tr><tr><td><code>visit</code></td><td>"2001-03-15 11:11:00"</td></tr></table>

Note that `dob` is in $HOROLOG format. You can convert this to a display format using the $ZDATETIME function:

```objectscript
 SET dob = 44051
 WRITE $ZDT(dob,3),!
```

The same consideration as true within a WHERE clause. For example, to find a Patient with a given birthday, you must use a logical value in the WHERE clause:

```sql
 &sql(SELECT Name INTO :name
        FROM Patient
        WHERE DOB = 43023)
```

or, alternatively, using a host variable:

```sql
 SET dob = $ZDH("01/02/1999",1)

 &sql(SELECT Name INTO :name
        FROM Patient
        WHERE DOB = :dob)
```

In this case, we use the $ZDATEH function to convert a display format date into its logical, $HOROLOG equivalent.

### Privilege Checking

Embedded SQL does not perform SQL privilege checking. You can access all tables, views, and columns and perform any operation, regardless of the privileges assignments. It is assumed that applications using Embedded SQL will check for privileges before using Embedded SQL statements.

You can use the InterSystems SQL %CHECKPRIV statement in Embedded SQL to determine the current privileges.

For further details, refer to SQL Users, Roles, and Privileges.

## Host Variables

A host variable is a local variable that passes a literal value into or out of Embedded SQL. Most commonly, host variables are used to either pass the value of a local variable as an input value into Embedded SQL, or to pass an SQL query result value as an output host variable from an Embedded SQL query.

A host variable cannot be used to specify an SQL identifier, such as a schema name, table name, field name, or cursor name. A host variable cannot be used to specify an SQL keyword.

*   Output host variables are only used in Embedded SQL. They are specified in an INTO clause, an SQL query clause that is only supported in Embedded SQL. Compiling Embedded SQL initializes all INTO clause variables to the null string ('').
    
*   Input host variables can be used in either Embedded SQL or Dynamic SQL. In Dynamic SQL, you can also input a literal to an SQL statement using the “?” input parameter. This “?” syntax cannot be used in Embedded SQL.
    

Within Embedded SQL, input host variables can be used in any place that a literal value can be used. Output host variables are specified using an INTO clause of a `SELECT` or `FETCH` statement.

> **Note:**
> 
> When an SQL NULL is output to ObjectScript, it is represented by an ObjectScript empty string (""), a string of length zero. See NULL and Undefined Host Variables.

To use a variable or a property reference as a host variable, precede it with a colon (:). A host variable in embedded InterSystems SQL can be one of the following:

*   One or more ObjectScript local variables, such as :myvar, specified as a comma-separated list. A local variable can be fully formed and can include subscripts. Like all local variables, it is case-sensitive and can contain Unicode letter characters.
    
*   A single ObjectScript local variable array, such as :myvars(). A local variable array can receive only field values from a single table (not joined tables or a view). For details, refer to “Host Variable Subscripted by Column Number”, below.
    
*   An object reference, such as :oref.Prop, where Prop is a property name, with or without a leading % character. This can be a simple property or a multidimensional array property, such as :oref.Prop(1). It can be an instance variable, such as :i%Prop or :i%%Data. The property name may be delimited; for example `:Person."Home City"`. Delimited property names can be used even when support for delimited identifiers is deactivated. Multidimensional properties may include :i%Prop() and :m%Prop() host variable references. An object reference host variable can include any number of dot syntax levels; for example, `:Person.Address.City`.
    
    When an oref.Prop is used as a host variable inside a procedure block method, the system automatically adds the oref variable (not the entire oref.Prop reference) to the PublicList and `NEW`s it.
    

Double quotes in a host variable specify a literal string, not a delimited identifier. For example, `:request.GetValueAt("PID:SetIDPID")` or `:request.GetValueAt("PID:PatientName(1).FamilyName")`.

Host variables should be listed in the ObjectScript procedure’s PublicList variables list and reinitialized using the NEW command. You can configure InterSystems IRIS to also list all host variables used in Embedded SQL in comment text; this is described in Comment.

Host variable values have the following behavior:

*   Input host variables are never modified by the SQL statement code. They retain their original values even after Embedded SQL has run. However, input host variable values are “lightly normalized” before being supplied to the SQL statement code: Valid numeric values are stripped of leading and trailing zeros, a single leading plus sign, and a trailing decimal point. Timestamp values are stripped of trailing spaces, trailing zeros in fractional seconds, and (if there are no fractional seconds) a trailing decimal point.
    
*   Output host variables specified in the INTO clause are defined when the query is compiled. They are set to the null string so that referencing them does not result in an <UNDEFINED> error. Host variable values only represent actual values when SQLCODE=0. In DECLARE ... SELECT ... INTO statements, do not modify the output host variables in the INTO clause between two FETCH calls, since that might cause unpredictable query results.
    

You must check the SQLCODE value before processing output host variables. Output host variable values should only be used when SQLCODE=0.

When using a comma-separated list of host variables in the INTO clause, you must specify the same number of host variables as the number of select-items (fields, aggregate functions, scalar functions, arithmetic expressions, literals). Too many or too few host variables results in an SQLCODE -76 cardinality error upon compilation.

This is often a concern when using SELECT * in Embedded SQL. For example, `SELECT * FROM Sample.Person` is only valid with a comma-separated list of 15 host variables (the exact number of non-hidden columns, which, depending on the table definition, may or may not include the system-generated RowID (ID) column). Note that this number of columns may not be a simple correspondence to the number of properties listed in the InterSystems Class Reference.

Because the number of columns can change, it is usually not a good idea to specify `SELECT *` with an `INTO` clause list of individual host variables. When using `SELECT *`, it is usually preferable to use a host variable subscripted array, such as the following:

```sql
   NEW SQLCODE
  &sql(SELECT %ID,* INTO :tflds() FROM Sample.Person )
        IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
        ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
   FOR i=0:1:25 {
       IF $DATA(tflds(i)) {
       WRITE "field ",i," = ",tflds(i),! }
     }
```

This example uses %ID to return the RowID as field number 1, whether or not the RowID is hidden. Note that in this example the field number subscripts may not be continuous sequence; some fields may be hidden and are skipped over. Fields that contain NULL are listed with an empty string value. Using a host variable array is described in “Host Variable Subscripted by Column Number”, below.

It is good programming practice to check the SQLCODE value immediately after exiting Embedded SQL. Output host variable values should only be used when SQLCODE=0.

### Host Variable Examples

In the following ObjectScript example, an Embedded SQL statement uses output host variables to return a name and home state address from an SQL query to ObjectScript:

```sql
   &sql(SELECT Name,Home_State
        INTO :CName,:CAddr
        FROM Sample.Person)
        IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
        ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
      WRITE !,"Name is: ",CName
      WRITE !,"State is: ",CAddr
```

The Embedded SQL uses an INTO clause that specifies the host variables `:CName` and `:CAddr` to return the selected customer’s name in the local variable `CName`, and home state in the local variable `CAddr`.

The following example performs the same operation, using subscripted local variables:

```sql
   &sql(SELECT Name,Home_State
        INTO :CInfo(1),:CInfo(2)
        FROM Sample.Person)
        IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
        ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
      WRITE !,"Name is: ",CInfo(1)
      WRITE !,"State is: ",CInfo(2)
```

These host variables are simple local variables with user-supplied subscripts (`:CInfo(1)`). However, if you omit the subscript (`:CInfo()`), InterSystems IRIS populates the host variable subscripted array using SqlColumnNumber, as described below.

In the following ObjectScript example, an Embedded SQL statement uses both input host variables (in the WHERE clause) and output host variables (in the INTO clause):

```sql
  SET minval = 10000
  SET maxval = 50000
  &sql(SELECT Name,Salary INTO :outname, :outsalary
       FROM MyApp.Employee
       WHERE Salary > :minval AND Salary < :maxval)
        IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
        ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
      WRITE !,"Name is: ",outname
      WRITE !,"Salary is: ",outsalary
```

The following example performs “light normalization” on an input host variable. Note that InterSystems IRIS treats the input variable value as a string and does not normalize it, but Embedded SQL normalizes this number to 65 to perform the equality comparison in the WHERE clause:

```sql
  SET x="+065.000"
  &sql(SELECT Name,Age
       INTO :a,:b
       FROM Sample.Person
       WHERE Age=:x)
        IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
        ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
  WRITE !,"Input value is: ",x
  WRITE !,"Name value is: ",a
  WRITE !,"Age value is: ",b
```

In the following ObjectScript example, an Embedded SQL statement uses object properties as host variables:

```sql
   &sql(SELECT Name, Title INTO :obj.Name, :obj.Title
        FROM MyApp.Employee
        WHERE %ID = :id )
```

In this case, `obj` must be a valid reference to an object that has mutable (that is, they can be modified) properties `Name` and `Title`. Note that if a query includes an INTO statement and no data is returned (that is, that SQLCODE is 100), then executing the query may result in the value of the host variable being modified.

### Host Variable Subscripted by Column Number

If the FROM clause contains a single table, you can specify a subscripted host variable for fields selected from that table; for example, the local array `:myvar()`. The local array is populated by InterSystems IRIS, using each field’s SqlColumnNumber as the numeric subscript. Note that SqlColumnNumber is the column number in the table definition, not the `select-list` sequence. (You cannot use a subscripted host variable for fields of a view.)

A host variable array must be a local array that has its lowest level subscript omitted. Therefore, `:myvar()`, `:myvar(5,)`, and `:myvar(5,2,)` are all valid host variable subscripted arrays.

*   A host variable subscripted array may be used for input in an `INSERT`, `UPDATE`, or `INSERT OR UPDATE` statement VALUES clause. When used in an `INSERT` or `UPDATE` statement, a host variable array allows you to define which columns are being updated at runtime, rather than at compile time.
    
*   A host variable subscripted array may be used for output in a `SELECT` or `DECLARE` statement INTO clause. Subscripted array usage in `SELECT` is shown in the examples that follow.
    

In the following example, the `SELECT` populates the Cdata array with the values of the specified fields. The elements of Cdata() correspond to the table column definition, not the `SELECT` elements. Therefore, the Name field is column 6, the Age field is column 2, and the date of birth (DOB) field is column 3 in Sample.Person:

```sql
   &sql(SELECT Name,Age,DOB
        INTO :Cdata()
        FROM Sample.Person)
          IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
          ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
      WRITE !,"Name is: ",Cdata(6)
      WRITE !,"Age is: ",Cdata(2)
      WRITE !,"DOB is: ",$ZDATE(Cdata(3),1)
```

The following example uses a subscripted array host variable to return all of the field values of a row:

```sql
   &sql(SELECT * INTO :Allfields()
        FROM Sample.Person)
          IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
          ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
      SET x=1
      WHILE x '="" {
      WRITE !,x," field is ",Allfields(x)
      SET x=$ORDER(Allfields(x))
      }
```

Note that this `WHILE` loop is incremented using `$ORDER` rather than a simple `x=x+1`. This is because in many tables (such as Sample.Person) there may be hidden columns. These cause the column number sequence to be discontinuous.

If the SELECT list contains items that are not fields from that table, such as expressions or arrow-syntax fields, the INTO clause must also contain comma-separated non-array host variables. The following example combines a subscripted array host variable to return values that correspond to defined table columns, and host variables to return values that do not correspond to defined table columns:

```sql
   &sql(SELECT Name,Home_City,{fn NOW},Age,($HOROLOG-DOB)/365.25,Home_State
        INTO :Allfields(),:timestmp('now'),:exactage
        FROM Sample.Person)
          IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
          ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
      SET x=$ORDER(Allfields(""))
      WHILE x '="" {
      WRITE !,x," field is ",Allfields(x)
      SET x=$ORDER(Allfields(x)) }
      WRITE !,"date & time now is ",timestmp("now")
      WRITE !,"exact age is ",exactage
```

Note that the non-array host variables must match the non-column `SELECT` items in number and sequence.

The use of a host variable as a subscripted array is subject to the following restrictions:

*   A subscripted list can only be used when selecting fields from a single table in the FROM clause. This is because when selecting fields from multiple tables, the SqlColumnNumber values may conflict.
    
*   A subscripted list can only be used when selecting table fields. It cannot be used for expressions or aggregate fields. This is because these `select-list` items do not have an SqlColumnNumber value.
    

For further details on using a host variable array, see INTO Clause.

### NULL and Undefined Host Variables

If you specify an input host variable that is not defined, Embedded SQL treats its value as NULL.

```sql
   NEW x
   &sql(SELECT Home_State,:x
        INTO :a,:b
        FROM Sample.Person)
          IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
          ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
     WRITE !,"The length of Home_State is: ",$LENGTH(a)
     WRITE !,"The length of x is: ",$LENGTH(b)
```

The SQL NULL is equivalent to the ObjectScript "" string (a zero-length string).

When Embedded SQL is compiled, all INTO clause output host variables are defined as the ObjectScript "" string (a zero-length string). If you output a NULL to a host variable, Embedded SQL treats its value as the ObjectScript "" string (a zero-length string). For example, some records in Sample.Person have a NULL Spouse field. After executing this query:

```sql
 &sql(SELECT Name,Spouse
    INTO :name, :spouse
    FROM Sample.Person
    WHERE Spouse IS NULL)
        IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
        ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
    WRITE !,"Name: ",name," of length ",$LENGTH(name)," defined: ",$DATA(name)
    WRITE !,"Spouse: ",spouse," of length ",$LENGTH(spouse)," defined: ",$DATA(spouse)
```

The host variable, `spouse`, will be set to "" (a zero-length string) to indicate a NULL value. Therefore, the ObjectScript `$DATA` function cannot be used to determine if an SQL field is NULL. `$DATA` returns true (variable is defined) when passed an output host variable for an SQL field with a NULL value.

In the rare case that a table field contains an SQL zero-length string (''), such as if an application explicitly set the field to an SQL '' string, the host variable will contain the special marker value, $CHAR(0) (a string of length 1, containing only a single, ASCII 0 character), which is the ObjectScript representation for the SQL zero-length string. Use of SQL zero-length strings is strongly discouraged.

The following example compares host variables output from an SQL NULL and an SQL zero-length string:

```sql
 &sql(SELECT '',Spouse
    INTO :zls, :spouse
    FROM Sample.Person
    WHERE Spouse IS NULL)
        IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
        ELSEIF SQLCODE=100 {WRITE "Query returns no results"  QUIT}
    WRITE "In ObjectScript"
    WRITE !,"ZLS is of length ",$LENGTH(zls)," defined: ",$DATA(zls)
       /* Length=1, Defined=1 */
    WRITE !,"NULL is of length ",$LENGTH(spouse)," defined: ",$DATA(spouse)
       /* Length=0, Defined=1 */
```

Note that this host variable NULL behavior is only true within server-based queries (Embedded SQL and Dynamic SQL). Within ODBC and JDBC, NULL values are explicitly specified using the ODBC or JDBC interface.

### Validity of Host Variables

*   Input host variables are never modified by Embedded SQL.
    
*   Output host variables are only reliably valid after Embedded SQL when SQLCODE = 0.
    

For example, the following use of `OutVal` is not reliably valid:

```sql
InvalidExample
   SET InVal = "1234"
   SET OutVal = "None"
   &sql(SELECT Name
        INTO :OutVal
        FROM Sample.Person
        WHERE %ID=:InVal)
   IF OutVal="None" {           ; Improper Use
   WRITE !,"No data returned"
   WRITE !,"SQLCODE=",SQLCODE }
   ELSE {
   WRITE !,"Name is: ",OutVal }
```

The value of `OutVal` set before invoking Embedded SQL should not be referenced by the `IF` command after returning from Embedded SQL.

Instead, you should code this example as follows, using the SQLCODE variable:

```sql
ValidExample
   SET InVal = "1234"
   &sql(SELECT Name
        INTO :OutVal
        FROM Sample.Person
        WHERE %ID=:InVal)
   IF SQLCODE'=0 { SET OutVal="None"
      IF OutVal="None" {
      WRITE !,"No data returned"
      WRITE !,"SQLCODE=",SQLCODE } }
   ELSE {
   WRITE !,"Name is: ",OutVal }
```

The Embedded SQL sets the SQLCODE variable to 0 to indicate the successful retrieval of an output row. An SQLCODE value of 100 indicates that no row was found that matches the `SELECT` criteria. An SQLCODE negative number value indicates a SQL error condition.

### Host Variables and Procedure Blocks

If your Embedded SQL is within a procedure block, all input and output host variables must be public. This can be done by declaring them in the PUBLIC section at the beginning of the procedure block, or by naming them with an initial % character (which automatically makes them public). Note, however, that a user-defined % host variable is automatically public, but is not automatically NEWed. It is the user’s responsibility to perform a `NEW` on such variables, as desired. Some SQL % variables, such as %ROWCOUNT, %ROWID, and %msg, are both automatically public and automatically NEWed, as described in Embedded SQL Variables. You must declare SQLCODE as public. For further details on the SQLCODE variable, see Embedded SQL Variables.

In the following procedure block example, the host variables `zip`, `city`, and `state`, as well as the SQLCODE variable are declared as PUBLIC. The SQL system variables %ROWCOUNT, %ROWID, and %msg are already public, because their names begin with a % character. The procedure code then performs a `NEW` on SQLCODE, the other SQL system variables, and the `state` local variable:

```sql
UpdateTest(zip,city)
  [SQLCODE,zip,city,state] PUBLIC {
  NEW SQLCODE,%ROWCOUNT,%ROWID,%msg,state
  SET state="MA"
  &sql(UPDATE Sample.Person
       SET Home_City = :city, Home_State = :state
       WHERE Home_Zip = :zip)
        IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
        QUIT %ROWCOUNT
  }
```

## SQL Cursors

A cursor is a pointer to data that allows an Embedded SQL program to perform an operation on the record pointed to. By using a cursor, Embedded SQL can iterate through a result set. Embedded SQL can use a cursor to execute a query that returns data from multiple records. Embedded SQL can also use a cursor to update or delete multiple records.

You must first DECLARE an SQL cursor, giving it a name. In the `DECLARE` statement you supply a `SELECT` statement that identifies which records the cursor will point to. You then supply this cursor name to the OPEN cursor statement. You then repeatedly issue the FETCH cursor statement to iterate through the `SELECT` result set. You then issue a CLOSE cursor statement; it is imperative that you close the cursor before exiting the ObjectScript method that contains Embedded SQL.

*   A cursor-based query uses DECLARE cursorname CURSOR FOR SELECT to select records and (optionally) return select column values into output host variables. The FETCH statement iterates through the result set, using these variables to return selected column values.
    
*   A cursor-based DELETE or UPDATE uses DECLARE cursorname CURSOR FOR SELECT to select records for the operation. No output host variables are specified. The FETCH statement iterates through the result set. The `DELETE` or `UPDATE` statement contains a `WHERE CURRENT OF` clause to identify the current cursor position in order to perform the operation on the selected record. For further details on cursor-based `DELETE` and `UPDATE`, see WHERE CURRENT OF.
    

Note that a cursor cannot span methods. Therefore, you must declare, open, fetch, and close a cursor within the same class method. It is important to consider this with all code that generates classes and methods, such as classes generated from a .CSP file.

The following example, uses a cursor to execute a query and display the results to the principal device:

```sql
 &sql(DECLARE C1 CURSOR FOR
    SELECT %ID,Name
    INTO :id, :name
    FROM Sample.Person
    WHERE Name %STARTSWITH 'A'
    ORDER BY Name
 )

 &sql(OPEN C1)
      QUIT:(SQLCODE'=0)
 &sql(FETCH C1)

 While (SQLCODE = 0) {
     Write id, ":  ", name,!
    &sql(FETCH C1)
 }

 &sql(CLOSE C1)
```

This example does the following:

1.  It declares a cursor, `C1`, that returns a set of `Person` rows ordered by `Name`.
    
2.  It opens the cursor.
    
3.  It calls FETCH on the cursor until it reaches the end of the data. After each call to FETCH, the SQLCODE variable will be set to 0 if there is more data to fetch. After each call to FETCH, the values returned are copied into the host variables specified by the INTO clause of the DECLARE statement.
    
4.  It closes the cursor.
    

### The DECLARE Cursor Statement

The DECLARE statement specifies both the cursor name and the SQL SELECT statement that defines the cursor. The DECLARE statement must occur within a routine before any statements that use the cursor.

A cursor name is case-sensitive.

A cursor name must be unique within a class or routine. For this reason, a routine that is called recursively cannot contain a cursor declaration. In this situation, it may be preferable to use Dynamic SQL.

The following example declares a cursor named `MyCursor`:

```sql
 &sql(DECLARE MyCursor CURSOR FOR
    SELECT Name, DOB
    FROM Sample.Person
    WHERE Home_State = :state
    ORDER BY Name
    )
```

A DECLARE statement may include an optional INTO clause that specifies the names of the local host variables that will receive data as the cursor is traversed. For example, we can add an INTO clause to the previous example:

```sql
 &sql(DECLARE MyCursor CURSOR FOR
    SELECT Name, DOB
    INTO :name, :dob
    FROM Sample.Person
    WHERE Home_State = :state
    ORDER BY Name
    )
```

The INTO clause may contain a comma-separated list of host variables, a single host variable array, or a combination of both. If specified as a comma-separated list, the number of INTO clause host variables must exactly match the number of columns within the cursor’s SELECT list or you will receive a “Cardinality Mismatch” error when the statement is compiled.

If the DECLARE statement does not include an INTO clause, then the INTO clause must appear within the FETCH statement. A small performance improvement may result from specifying the INTO clause in the DECLARE statement, rather than in the FETCH statement.

Because DECLARE is a declaration, not an executed statement, it does not set or kill the SQLCODE variable.

If a specified cursor has already been declared, compilation fails with a SQLCODE -52 error, `Cursor name already declared`.

Executing a DECLARE statement does not compile the SELECT statement. The SELECT statement is compiled the first time the OPEN statement is executed. Embedded SQL is not compiled at routine compile time, but at SQL execution time (runtime).

### The OPEN Cursor Statement

The OPEN statement prepares a cursor for subsequent execution:

```sql
 &sql(OPEN MyCursor)
```

Executing the OPEN statement compiles the Embedded SQL code found in the DECLARE statement, creates an optimized query plan, and generates a cached query. Error involving missing resources (such as an undefined table or field) are issued when the OPEN is executed (at SQL runtime).

Upon a successful call to OPEN, the SQLCODE variable will be set to 0.

You cannot FETCH data from a cursor without first calling OPEN.

### The FETCH Cursor Statement

The FETCH statement fetches the data for the next row of the cursor (as defined by the cursor query):

```sql
 &sql(FETCH MyCursor)
```

You must DECLARE and OPEN a cursor before you can call FETCH on it.

A FETCH statement may contain an INTO clause that specifies the names of the local host variables that will receive data as the cursor is traversed. For example, we can add an INTO clause to the previous example:

```sql
 &sql(FETCH MyCursor INTO :a, :b)
```

The INTO clause may contain a comma-separated list of host variables, a single host variable array, or a combination of both. If specified as a comma-separated list, the number of INTO clause host variables must exactly match the number of columns within the cursor’s SELECT list or you will receive an SQLCODE -76 “Cardinality Mismatch” error when the statement is compiled.

Commonly, the INTO clause is specified in the DECLARE statement, not the FETCH statement. If both the SELECT query in the DECLARE statement and the FETCH statement contain an INTO clause, only the host variables specified by the DECLARE statement are set. If only the FETCH statement contain an INTO clause, the host variables specified by the FETCH statement are set.

If FETCH retrieves data, the SQLCODE variable is set to 0; if there is no data (or no more data) to FETCH, SQLCODE is set to 100 (No more data). Host variable values should only be used when SQLCODE=0.

Depending on the query, the first call to FETCH may perform additional tasks (such as sorting values within a temporary data structure).

### The CLOSE Cursor Statement

The CLOSE statement terminates the execution of a cursor:

```sql
 &sql(CLOSE MyCursor)
```

The CLOSE statement cleans up any temporary storage used by the execution of a query. Programs that fail to call CLOSE will experience resource leaks (such as unneeded increase of the IRISTEMP temporary database).

Upon a successful call to CLOSE, the SQLCODE variable is set to 0. Therefore, before closing a cursor you should check whether the final FETCH set SQLCODE to 0 or 100.

## Embedded SQL Variables

The following local variables have specialized uses in Embedded SQL. These local variable names are case-sensitive. At process initiation, these variables are undefined. They are set by Embedded SQL operations. They can also be set directly using the `SET` command, or reset to undefined using the `NEW` command. Like any local variable, a value persists for the duration of the process or until set to another value or undefined using `NEW`. For example, some successful Embedded SQL operations do not set %ROWID; following these operations, %ROWID is undefined or remains set to its prior value.

*   %msg
    
*   %ROWCOUNT
    
*   %ROWID
    
*   SQLCODE
    

These local variables are not set by Dynamic SQL. (Note that the SQL Shell and the Management Portal SQL interface execute Dynamic SQL.) Instead, Dynamic SQL sets corresponding object properties.

The following ObjectScript special variables are used in Embedded SQL. These special variable names are not case-sensitive. At process initiation, these variables are initialized to a value. They are set by Embedded SQL operations. They cannot be set directly using the `SET` or `NEW` commands.

*   $TLEVEL
    
*   $USERNAME
    

As part of the defined InterSystems IRIS Embedded SQL interface, InterSystems IRIS may set any of these variables during Embedded SQL processing.

If the Embedded SQL is in a class method (with ProcedureBlock=ON), the system automatically places all of these variables in the PublicList and `NEW`s the SQLCODE, %ROWID, %ROWCOUNT, %msg, and all non-% variables used by the SQL statement. You can pass these variables by reference to/from the method; variables passed by reference will not be `NEW`ed automatically in the class method procedure block.

If the Embedded SQL is in a routine, it is the responsibility of the programmer to NEW the %msg, %ROWCOUNT, %ROWID, and SQLCODE variables before invoking Embedded SQL. NEWing these variables prevents interference with prior settings of these variables. To avoid a <FRAMESTACK> error, you should not perform this `NEW` operation within an iteration cycle.

### %msg

A variable that contains a system-supplied error message string. InterSystems SQL only sets %msg if it has set SQLCODE to a negative integer, indicating an error. If SQLCODE is set to 0 or 100, the %msg variable is unchanged from its prior value.

This behavior differs from the corresponding Dynamic SQL %Message property, which is set to the empty string when there is no current error.

In some cases, a specific SQLCODE error code may be associated with more than one %msg string, describing different conditions that generated the SQLCODE. %msg can also take a user-defined message string. This is most commonly used to issue a user-defined message from a trigger when trigger code explicitly sets %ok=0 to abort the trigger.

An error message string is generated in the NLS language in effect for the process when the SQL code is executed. The SQL code may be compiled in a different NLS language environment; the message will be generated according to the runtime NLS environment. See $SYS.NLS.Locale.Language.

### %ROWCOUNT

An integer counter that indicates the number of rows affected by a particular statement.

*   `INSERT`, `UPDATE`, `INSERT OR UPDATE`, and `DELETE` set %ROWCOUNT to the number of rows affected. An `INSERT` command with explicit values can only affect one row, and thus sets %ROWCOUNT to either 0 or 1. An `INSERT` query results, an `UPDATE`, or a `DELETE` can affect multiple rows, and can thus set %ROWCOUNT to 0 or a positive integer.
    
*   `TRUNCATE TABLE` always sets %ROWCOUNT to –1, regardless of how many rows were deleted or if any rows were deleted. Therefore, to determine the actual number of rows deleted, either perform a COUNT(*) on the table before `TRUNCATE TABLE`, or delete all the rows in the table using `DELETE`, rather than `TRUNCATE TABLE`.
    
*   `SELECT` with no declared cursor can only act upon a single row, and thus execution of a simple `SELECT` always sets %ROWCOUNT to either 1 (single row that matched the selection criteria retrieved) or 0 (no rows matched the selection criteria).
    
*   `DECLARE cursorname CURSOR FOR SELECT` does not initialize %ROWCOUNT; %ROWCOUNT is unchanged following the `SELECT`, and remains unchanged following `OPEN cursorname`. The first successful `FETCH` sets %ROWCOUNT. If no rows matched the query selection criteria, `FETCH` sets %ROWCOUNT=0; if `FETCH` retrieves a row that matched the query selection criteria, it sets %ROWCOUNT=1. Each subsequent `FETCH` that retrieves a row increments %ROWCOUNT. Upon `CLOSE` or when `FETCH` issues an SQLCODE 100 (No Data, or No More Data), %ROWCOUNT contains the total number of rows retrieved.
    

This `SELECT` behavior differs from the corresponding Dynamic SQL %ROWCOUNT property, which is set to 0 upon completion of query execution, and is only incremented when the program iterates through the result set returned by the query.

If a `SELECT` query returns only aggregate functions, every `FETCH` sets %ROWCOUNT=1. The first `FETCH` always completes with SQLCODE=0, even when there is no data in the table; any subsequent `FETCH` completes with SQLCODE=100 and sets %ROWCOUNT=1.

The following Embedded SQL example declares a cursor and uses `FETCH` to fetch each row in the table. When the end of data is reached (SQLCODE=100) %ROWCOUNT contains the number of rows retrieved:

```sql
   SET name="LastName,FirstName",state="##"
   &sql(DECLARE EmpCursor CURSOR FOR
        SELECT Name, Home_State
        INTO :name,:state FROM Sample.Person
        WHERE Home_State %STARTSWITH 'M')
   WRITE !,"BEFORE: Name=",name," State=",state
   &sql(OPEN EmpCursor)
      QUIT:(SQLCODE'=0)
   FOR { &sql(FETCH EmpCursor)
        QUIT:SQLCODE
        WRITE !,"Row fetch count: ",%ROWCOUNT
        WRITE " Name=",name," State=",state
 }
   WRITE !,"Final Fetch SQLCODE: ",SQLCODE
   &sql(CLOSE EmpCursor)
   WRITE !,"AFTER: Name=",name," State=",state
   WRITE !,"Total rows fetched: ",%ROWCOUNT
```

The following Embedded SQL example performs an `UPDATE` and sets the number of rows affected by the change:

```sql
 &sql(UPDATE MyApp.Employee
     SET Salary = (Salary * 1.1)
     WHERE Salary < 50000)
        IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}
  WRITE "Employees: ", %ROWCOUNT,!
```

Keep in mind that all Embedded SQL statements (within a given process) modify the %ROWCOUNT variable. If you need the value provided by %ROWCOUNT, be sure to get its value before executing additional Embedded SQL statements. Depending on how Embedded SQL is invoked, you may have to `NEW` the %ROWCOUNT variable before entering Embedded SQL.

Also note that explicitly rolling back a transaction will not affect the value of %ROWCOUNT. For example, the following will report that changes have been made, even though they have been rolled back:

```sql
 TSTART // start an explicit transaction
  NEW SQLCODE,%ROWCOUNT,%ROWID
 &sql(UPDATE MyApp.Employee
     SET Salary = (Salary * 1.1)
     WHERE Salary < 50000)
        IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE," ",%msg  QUIT}

 TROLLBACK // force a rollback; this will NOT modify %ROWCOUNT
 Write "Employees: ", %ROWCOUNT,!
```

Implicit transactions (such as if an `UPDATE` fails a constraint check) are reflected by %ROWCOUNT.

### %ROWID

When you initialize a process, %ROWID is undefined. When you issue a `NEW %ROWID` command, %ROWID is reset to undefined. %ROWID is set by the Embedded SQL operations described below. If the operation is not successful, or completes successfully but does not fetch or modify any rows, the %ROWID value remains unchanged from its prior value: either undefined, or set to a value by a previous Embedded SQL operation. For this reason, it is important to NEW %ROWID before each Embedded SQL operation.

%ROWID is set to the RowID of the last row affected by the following operations:

*   `INSERT`, `UPDATE`, `INSERT OR UPDATE`, or `DELETE`: After a single-row operation, the %ROWID variable contains the system-assigned value of the RowID (Object ID) assigned to the inserted, updated, or deleted record. After a multiple-row operation, the %ROWID variable contains the system-assigned value of the RowID (Object ID) of the last record inserted, updated, or deleted. If no record is inserted, updated, or deleted, the %ROWID variable value is unchanged. `TRUNCATE TABLE` does not set %ROWID.
    
*   Cursor-based `SELECT`: The `DECLARE cursorname CURSOR` and `OPEN cursorname` statements do not initialize %ROWID; the %ROWID value is unchanged from its prior value. The first successful `FETCH` sets %ROWID. Each subsequent `FETCH` that retrieves a row resets %ROWID to the current RowID value. `FETCH` sets %ROWID if it retrieves a row of an updateable cursor. An updateable cursor is one in which the top FROM clause contains exactly one element, either a single table name or an updateable view name. If the cursor is not updateable, %ROWID remains unchanged. If no rows matched the query selection criteria, `FETCH` does not change the prior the %ROWID value (if any). Upon `CLOSE` or when `FETCH` issues an SQLCODE 100 (No Data, or No More Data), %ROWID contains the RowID of the last row retrieved.
    
    Cursor-based `SELECT` with a DISTINCT keyword or a GROUP BY clause does not set %ROWID. The %ROWID value is unchanged from its previous value (if any).
    
    Cursor-based `SELECT` with an aggregate function does not set %ROWID if it returns only aggregate function values. If it returns both field values and aggregate function values, the %ROWID value for every `FETCH` is set to the RowID of the last row returned by the query.
    
*   `SELECT` with no declared cursor does not set %ROWID. The %ROWID value is unchanged upon the completion of a simple `SELECT` statement.
    

In Dynamic SQL, the corresponding %ROWID property returns the RowID value of the last record inserted, updated, or deleted. Dynamic SQL does not return a `%ROWID` property value when performing a `SELECT` query.

You can retrieve the current %ROWID from ObjectScript using the following method call:

```objectscript
  WRITE $SYSTEM.SQL.GetROWID()
```

Following an `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE TABLE`, or Cursor-based `SELECT` operation, the LAST_IDENTITY SQL function returns the value of the IDENTITY field for the most-recently modified record. If the table does not have an IDENTITY field, this function returns the RowID for the most-recently modified record.

### SQLCODE

After running an embedded SQL Query, you must check the SQLCODE before processing the output host variables. In particular, you should always check SQLCODE<0; if this condition holds true, then there was error while processing the query and your application should respond accordingly.

If SQLCODE=0 the query completed successfully and returned data. The output host variables contain field values.

If SQLCODE=100 the query completed successfully, but output host variable values may differ. Either:

*   The query returned one or more rows of data (SQLCODE=0), then reached the end of the data (SQLCODE=100), in which case output host variables are set to the field values of the last row returned. %ROWCOUNT>0.
    
*   The query returned no data, in which case the output host variables are set to the null string. %ROWCOUNT=0.
    

After any invocation of the &sql() directive, you should check SQLCODE<0. If this condition holds true, then an error arose.

If a query returns only aggregate functions, the first `FETCH` always completes with SQLCODE=0 and %ROWCOUNT=1, even when there is no data in the table. The second `FETCH` completes with SQLCODE=100 and %ROWCOUNT=1. If there is no data in the table or no data matches the query conditions, the query sets output host variables to 0 or the empty string, as appropriate.

If SQLCODE is a negative number the query failed with an error condition. For a list of these error codes and additional information, refer to SQLCODE Values and Error Messages.

Depending on how Embedded SQL is invoked, you may have to NEW the SQLCODE variable before entering Embedded SQL. Within trigger code, setting SQLCODE to a nonzero value automatically sets %ok=0, aborting and rolling back the trigger operation.

In Dynamic SQL, the corresponding %SQLCODE property returns SQL error code values.

### $TLEVEL

The transaction level counter. InterSystems SQL initializes `$TLEVEL` to 0. If there is no current transaction, `$TLEVEL` is 0.

*   An initial START TRANSACTION sets `$TLEVEL` to 1. Additional `START TRANSACTION` statements have no effect on `$TLEVEL`.
    
*   Each SAVEPOINT statement increments `$TLEVEL` by 1.
    
*   A ROLLBACK TO SAVEPOINT pointname statement decrements `$TLEVEL`. The amount of decrement depends on the savepoint specified.
    
*   A COMMIT resets `$TLEVEL` to 0.
    
*   A ROLLBACK resets `$TLEVEL` to 0.
    

You can also use the %INTRANSACTION statement to determine if a transaction is in progress.

`$TLEVEL` is also set by ObjectScript transaction commands. For further details, see $TLEVEL.

### $USERNAME

The SQL username is the same as the InterSystems IRIS username, stored in the ObjectScript $USERNAME special variable. The username can be used as the system-wide default schema or as an element in the schema search path.

## Embedded SQL in Methods of a Persistent Class

The following example shows a persistent class containing a class method and an instance method, both of which contain Embedded SQL:

```sql
Class Sample.MyClass Extends %Persistent [DdlAllowed]
 {
 ClassMethod NameInitial(Myval As %String) As %String [SqlProc]
  {
     &sql(SELECT Name INTO :n FROM Sample.Stuff WHERE Name %STARTSWITH :Myval)
        IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE  RETURN %msg}
        ELSEIF SQLCODE=100 {WRITE "Query returns no results"  RETURN}
   WRITE "Hello "  RETURN n
  }
 Method CountRows() As %Integer
  {
   &sql(SELECT COUNT(*) INTO :count FROM Sample.Stuff)
        IF SQLCODE<0 {WRITE "SQLCODE error ",SQLCODE  RETURN %msg}
        ELSEIF SQLCODE=100 {WRITE "Query returns no results"  RETURN}
   WRITE "Number of rows is "  RETURN count
  }
 }
```

The class method is invoked as follows:

```objectscript
  WRITE ##class(Sample.MyClass).NameInitial("G")
```

The instance method is invoked as follows:

```objectscript
  SET x=##class(Sample.MyClass).%New()
  WRITE x.CountRows()
```

SQL entities such as tables and fields do not have to exist for these methods to successfully compile. Because checking for the existence of SQL entities is performed at runtime, Embedded SQL methods should contain SQLCODE test logic.

You can test for the existence of SQL entities specified in Embedded SQL without executing the code. This is described in Validating Embedded SQL Code.

## Validating Embedded SQL Code

You can validate Embedded SQL code without executing the code in three ways:

*   Compiling a routine containing Embedded SQL code using the `/compileembedded=1` qualifier.
    
*   Compiling multiple Embedded SQL routines using the $SYSTEM.OBJ.GenerateEmbedded() method.
    
*   Testing the Embedded SQL code using the Management Portal SQL interface `Show Plan` option.
    

### Compile with /compileembedded Qualifier

You can validate Embedded SQL code by using the compile class methods of the `$SYSTEM.OBJ` class and specifying in the `qspec` argument the `/compileembedded=1` qualifier. The`/compileembedded` default is 0.

*   $SYSTEM.OBJ.Compile() compiles the specified class and all routines within that class.
    
*   $SYSTEM.OBJ.CompileList() compiles a list of specified classes and all routines within those classes.
    
*   $SYSTEM.OBJ.CompilePackage() compiles all classes/routines in the specified package (schema).
    
*   $SYSTEM.OBJ.CompileAll() compiles all classes/routines in the current namespace.
    
*   $SYSTEM.OBJ.CompileAllNamespaces() compiles all classes/routines in all namespaces.
    

You can specify use of the `/compileembedded=1` qualifier by default using the SetQualifiers() method from the Terminal:

```objectscript
USER>DO $SYSTEM.OBJ.SetQualifiers("/compileembedded=1")    /* sets /compileembedded for current namespace */
```

```objectscript
USER>DO $SYSTEM.OBJ.SetQualifiers("/compileembedded=1",1)  /* sets /compileembedded for all namespaces */
```

To display a list of `qspec` qualifiers, including `/compileembedded`, invoke:

```objectscript
USER>DO $SYSTEM.OBJ.ShowQualifiers()
```

The non-default qualifier settings are shown at the end of the ShowQualifiers() display.

### Test with Show Plan

You can use the Management Portal SQL interface to validate Embedded SQL code without executing the code. This operation both validates the SQL syntax and checks for the existence of the specified SQL entities.

From the Management Portal `System Explorer` option select the `SQL` option to display the Execute Query code area.

1.  Input your Embedded SQL query. For example `SELECT Name INTO :n FROM Sample.MyTest` or `DECLARE MyCursor CURSOR FOR SELECT Name,Age INTO :n,:a FROM Sample.MyTest WHERE Age > 21 FOR READ ONLY`.
    
2.  Press the `Show Plan` button to check the code. If the code is valid, `Show Plan` displays a Query Plan. If the code is invalid, `Show Plan` displays an SQLCODE error value and message.
    
    Note that `Show Plan` validation will not issue an error if the INTO clause is missing, because the INTO clause may be specified in the FETCH statement. `Show Plan` will issue appropriate errors if the INTO clause contains an error or is in the wrong location.
    

You cannot use the `Execute` button to execute Embedded SQL code.

## Auditing Embedded SQL

InterSystems IRIS supports optional auditing of Embedded SQL statements. Embedded SQL auditing is performed when the following two requirements are met:

1.  The %System/%SQL/EmbeddedStatement system audit event is enabled system-wide. By default, this system audit event is not enabled. To enable, go to Management Portal, `System Administration`, select `Security`, then `Auditing`, then `Configure System Events`.
    
2.  The routine containing the Embedded SQL statement must contain the #sqlcompile audit macro preprocessor directive. If this directive is set to ON, any Embedded SQL statement following it in the compiled routine is audited when executed.
    

Auditing records information in the Audit Database. To view the Audit Database, go to the Management Portal, `System Administration`, select `Security`, then `Auditing`, then `View Audit Database`. You can set the `Event Name` filter to EmbeddedStatement to limit the `View Audit Database` to Embedded SQL statements. The Audit Database lists Time (a local timestamp), User, PID (process ID), and the Description, which specifies the type of Embedded SQL statement. For example, `SQL SELECT Statement`.

By selecting the `Details` link for an event you can list additional information, including the `Event Data`. The Event Data includes the SQL statement executed and the values of any input arguments to the statement. For example:

```
SELECT TOP :n Name,ColorPreference INTO :name,:color FROM Sample.Stuff WHERE Name %STARTSWITH :letter
Parameter values:
n=5
letter="F"
```

InterSystems IRIS also supports auditing of Dynamic SQL statements (`Event Name`=DynamicStatement) and ODBC and JDBC statements (`Event Name`=XDBCStatement).
