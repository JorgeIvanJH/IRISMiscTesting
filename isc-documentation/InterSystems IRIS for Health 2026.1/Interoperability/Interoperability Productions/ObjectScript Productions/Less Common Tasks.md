# Less Common Tasks

This page discusses less common development tasks.

## Defining Custom Utility Functions

InterSystems IRIS data platform provides a set of utility functions that can be invoked from business rules and from DTL; these are described in Utility Functions for Use in Productions. You can add your own functions, and the business rules engine and Business Rule Editor accommodate your extensions automatically.

To add a new utility function:

1.  Create a new class that is a subclass of Ens.Rule.FunctionSet. The class can inherit from other classes as well, but only class methods defined in this class become utility functions.
    
2.  For each function you wish to define, add a class method to your new function set class. There is no support for polymorphism, so to be precise, you must mark these class methods as final. You can view this in the existing Ens.Util.FunctionSet methods (Ens.Util.FunctionSet is a superclass of Ens.Rule.FunctionSet).
    
3.  Compile the new class. The new functions are now available for use in rule expressions. To invoke these functions, use the `ClassMethod` name from your subclass. Unlike functions defined in Ens.Rule.FunctionSet, user-defined method names must be fully qualified with the class that they belong to. This happens automatically if you add them by selecting names from the wizards in the Management Portal.
    

As an example, the following function set class provides date and time functions for use in business rules. Its class methods `DayOfWeek()` and `TimeInSeconds()` invoke the ObjectScript functions $ZDATE and $PIECE to extract the desired date and time values from the ObjectScript special variable $HOROLOG:

```objectscript
/// Time functions to use in rule definitions.
Class Demo.MsgRouter.Functions Extends Ens.Rule.FunctionSet
{

/// Returns the ordinal position of the day in the week,
/// where 0 is Sunday, 1 is Monday, and so on.
ClassMethod DayOfWeek() As %Integer [ CodeMode = expression, Final ]
{
$zd($H,10)
}

/// Returns the time as a number of seconds since midnight.
ClassMethod TimeInSeconds() As %Integer [ CodeMode = expression, Final ]
{
$p($H,",",2)
}

}
```

For a full list of functions and special variables available in ObjectScript, see ObjectScript Reference.

Once you have added a new function as described in this topic, the syntax for referring to it is slightly different than for built-in functions. Suppose you define this function in a class that inherits from Ens.Rule.FunctionSet.

```objectscript
ClassMethod normalizaSexo(value as %String) as %String {}
```

After you compile the class, when you use one of the InterSystems IRIS Interoperability visual tools such as the Routing Rule Editor or Data Transformation Builder, you see your function name `normalizaSexo` included in the function selection box along with built-in functions like Strip, In, Contains, and so on.

Suppose you choose a built-in function from the function selection box and look at the generated code. You see that InterSystems IRIS has generated the function call using double-dot method call syntax (in DTL) or has simply referenced the function by name (in a business rule). (These syntax rules are explained in Utility Functions for Use in Productions.)

The following example is an <assign> statement from DTL that references the built-in Strip function with double-dot syntax:

```xml
<assign property='target.cod'
        value='..Strip(source.{PatientIDExternalID.ID},"<>CW")'
        action='set'/>
```

However, if you create your own, user-defined functions, the syntax for DTL is different. It is not enough simply to identify the function; you must also identify the full class name for the class that contains the class method for your function. Suppose your function `normalizaSexo` was defined in a class named `HP.Util.funciones`. In that case, after you chose a function from the function selection box and looked at the generated code, you would see something like the following example:

```xml
<assign property='target.sexo'
        value='##class(HP.Util.funciones).normalizaSexo(source.{Sex})'
        action='set'/>
```

You need to be aware of this syntax variation if you wish to type statements like this directly into your DTL code, rather than using the Data Transformation Builder to generate the code.

## Rendering Connections When the Targets Are Dynamic

The Management Portal automatically displays the connections to and from a given business host, when a user selects that business host. For example:

[Image: Production Configuration page displaying connections between business hosts]

To do this, InterSystems IRIS reads the configuration settings for the business host and uses them.

If, however, the business service host determines its targets dynamically, at runtime, InterSystems IRIS cannot automatically display such connections. In this case, to display such connections, implement the `OnGetConnections()` callback method. InterSystems IRIS automatically calls this method (which does nothing by default) when it renders the configuration diagram.

> **Note:**
> 
> If the business host uses Ens.DataType.ConfigName or one of its subclasses for connections, the connections will be rendered automatically and `OnGetConnections()` is not necessary.

`OnGetConnections()` has the following signature:

```objectscript
ClassMethod OnGetConnections(Output pArray As %String, item As Ens.Config.Item) [ CodeMode = generator ]
{}
```

Where the arguments are as follows:

*   `pArray`—A multidimensional array, whose subscripts are the configured names of items to which this business service sends messages. For example, to send messages to the business hosts named ABC and DEF, your code could set `pArray` as follows:
    
    ```objectscript
     set pArray("ABC")=""
     set pArray("DEF")=""
    ```
    
*   `item`—The Ens.Config.Item object that represents this business service.
    

For examples of overridden `OnGetConnections()` methods, use an IDE to examine the built-in business services provided for use with electronic data interchange protocols such as X12. These are described in detail in Routing X12 Documents in Productions and other specific documentation.

## Using Ens.Director to Start and Stop a Production

During development, you typically use the Management Portal to start and stop a production. For live, deployed production, InterSystems recommends that you use the auto-start option as described in Configuring Productions.

Another option is to start or stop a production programmatically in the namespace where it is defined. To do so, invoke the following methods in the Ens.Director class:

### StopProduction()

Stop the currently running production:

```objectscript
  Do ##class(Ens.Director).StopProduction()
```

### StartProduction()

Start the specified production, as long as no other production is running:

```objectscript
  Do ##class(Ens.Director).StartProduction("myProduction")
```

This method starts a job that runs under the OS username used when the method was called; that user may or may not have appropriate permissions needed by the production. (In contrast, in the more common case, when the production calls this method, the job runs under the effective username of the instance, typically irisusr.)

### RecoverProduction()

Clean up a Troubled instance of a running production so that you can run a new instance in the same namespace:

```objectscript
  Do ##class(Ens.Director).RecoverProduction()
```

It is not necessary to call `GetProductionStatus()` to see if the production terminated abnormally prior to calling `RecoverProduction()`. If the production is not Troubled, the method simply returns.

### GetProductionStatus()

This method returns the production status via two output parameters, both of which are passed by reference. The first parameter returns the production name, but only when the status is Running, Suspended, or Troubled. The second parameter returns the production state, which is a numeric value equivalent to one of the following constants:

*   `$$$eProductionStateRunning`
    
*   `$$$eProductionStateStopped`
    
*   `$$$eProductionStateSuspended`
    
*   `$$$eProductionStateTroubled`
    

For example:

```objectscript
 Set tSC=##class(Ens.Director).GetProductionStatus(.tProductionName,.tState)
 Quit:$$$ISERR(tSC)
 If tState'=$$$eProductionStateRunning {
   $$$LOGINFO($$$Text("No Production is running.")) Quit
   }
```

You can use the production state macros such as `$$$eProductionStateRunning` in code outside of the InterSystems IRIS production classes, for example in a general class or routine. To do this, you must add the following statement to the class:

`#include Ensemble`

It is not necessary to do this inside production classes, such as in business hosts.

Ens.Director provides many class methods, including many intended for use only by the InterSystems IRIS internal framework. InterSystems recommends that you use only the Ens.Director methods documented here, and only as documented.

> **Note:**
> 
> InterSystems recommends you do not use the `^%ZSTART` routine to control production startup. The InterSystems IRIS startup mechanisms are much easier to use and are more closely tied to the production itself.

## Using Ens.Director to Access Settings

The following Ens.Director class methods allow retrieval of production settings even when the production is not running:

### GetAdapterSettings()

Returns an array containing the values of all adapter settings for the identified configuration item: a business service or business operation. The array is subscripted by setting name. You can use the InterSystems IRIS $ORDER function to access the elements of the array. The first parameter for this method is a string that contains the production name and configuration item name separated by two vertical bars (`||`). The return value is a status value. If the status value is not $$$OK, the specified combination of production name (`myProd`) and configuration item name (`myOp`) could not be found.

```objectscript
 Set tSC=##class(Ens.Director).GetAdapterSettings("myProd||myOp",.tSettings)
```

### GetAdapterSettingValue()

Returns the value of a named adapter setting for the identified configuration item: a business service or business operation. The first parameter is a string that contains the production name and configuration item name separated by two vertical bars (`||`). The second parameter is the name of a configuration setting. The third output parameter returns a status value from the call. For example:

```objectscript
 Set val=##class(Ens.Director).GetAdapterSettingValue("myProd||myOp","QSize",.tSC)
```

If the returned status value is not $$$OK, the specified combination of production name (`myProd`) and configuration item name (`myOp`) could not be found, or a setting of the specified name (`QSize`) was not found in the configuration for that specified production and configuration item.

### GetCurrProductionSettings()

Returns an array containing the values of all production settings from the currently running production or the production most recently run. The array is subscripted by setting name. The return value for this method is a status value. If the status value is not $$$OK, no current production could be identified.

```objectscript
 Set tSC=##class(Ens.Director).GetCurrProductionSettings(.tSettings)
```

### GetCurrProductionSettingValue()

Returns the string value of a named production setting from the currently running production or the production most recently run. The second output parameter returns a status value from the call. If this status value is not $$$OK, either a setting of the specified name was not found in the configuration for the current production, or no current production could be identified.

```objectscript
 Set myValue=##class(Ens.Director).GetCurrProductionSettingValue("mySet",.tSC)
```

### GetHostSettings()

Returns an array containing the values of all settings for the identified configuration item: a business service, business process, or business operation. The array is subscripted by setting name. The first parameter for this method is a string that contains the production name and configuration item name separated by two vertical bars (`||`). The return value is a status value. If the status value is not $$$OK, the specified combination of production name (`myProd`) and configuration item name (`myOp`) could not be found.

```objectscript
 Set tSC=##class(Ens.Director).GetHostSettings("myProd||myOp",.tSettings)
```

### GetHostSettingValue()

Returns the value of a named setting for the identified configuration item: a business service, business process, or business operation. The first parameter is a string that contains the production name and configuration item name separated by two vertical bars (`||`). The second parameter is the name of a configuration setting. The third output parameter returns a status value from the call. For example:

```objectscript
 Set val=##class(Ens.Director).GetHostSettingValue("myProd||myOp","QSize",.tSC)
```

If the returned status value is not $$$OK, the specified combination of production name (`myProd`) and configuration item name (`myOp`) could not be found, or a setting of the specified name (`QSize`) was not found in the configuration for that specified production and configuration item.

### GetProductionSettings()

Returns an array containing the values of all production settings from the named production. The array is subscripted by setting name. The return value for this method is a status value. If the status value is not $$$OK, the specified production could not be found.

```objectscript
 Set tSC=##class(Ens.Director).GetProductionSettings("myProd",.tSettings)
```

### GetProductionSettingValue()

Returns the value of a named production setting from the named production. The third output parameter returns a status value from the call. If this status value is not $$$OK, the specified production could not be found, or a setting of the specified name was not found in the configuration for the specified production.

```objectscript
 Set val=##class(Ens.Director).GetProductionSettingValue("prod","set",.tSC)
```

Ens.Director provides many class methods, including many intended for use only by the InterSystems IRIS internal framework. InterSystems recommends that you use only the Ens.Director methods documented here, and only as documented.

## Invoking a Business Service Directly

There are times when you want to invoke a business service directly, from a job that has been created by some other mechanism, such as a language binding, CSP pages, SOAP, or a routine invoked from the operating system level. You can do so only if the value of the `ADAPTER` class parameter is null; this type of business service is called an adapterless business service.

For a business service to work, you must create an instance of the business service class. You cannot create this instance by calling the `%New()` method. Instead, you must use the method `CreateBusinessService()` of Ens.Director. For example:

```objectscript
  Set tSC = ##class(Ens.Director).CreateBusinessService("MyService",.tService)
```

A production does not allocate a job for this business service at production startup; it assumes a `Pool Size` setting of 0.

The `CreateBusinessService()` method does the following:

1.  It makes sure that a production is running and that the production defines the given business service.
    
2.  It makes sure that the given business service is currently enabled.
    
3.  It resolves the configuration name of the business service and instantiates the correct business service object using the correct configuration values (a production may define many business services using the same business service class but with different names and settings).
    

If the `CreateBusinessService()` method succeeds, it returns, by reference, an instance of the business service class. You can then directly invoke its `ProcessInput()` method. This method is internal and cannot be seen in the class reference. Its signature is as follows:

```
Method ProcessInput(pInput As %RegisteredObject, Output pOutput As %RegisteredObject, ByRef pHint As %String) As %Status {
}
```

For example:

```objectscript
 If ($IsObject(tService)) {
    Set input = ##class(MyObject).%New()
    Set input.Value = 22
    Set tSC = tService.ProcessInput(input,.output)
 }
```

Ens.Director provides many class methods, including many intended for use only by the InterSystems IRIS internal framework. InterSystems recommends that you use only the Ens.Director methods documented here, and only as documented.

## Creating or Subclassing Inbound Adapters

This section describes how to create or subclass an inbound adapter.

### Introduction to Inbound Adapters

An inbound adapter is responsible for receiving and validating requests from external systems.

Inbound adapter classes work in conjunction with a business service classes. In general, the inbound adapter contains general-purpose, reusable code while the business service contains production-specific code (such as special validation logic). Typically you implement inbound adapter classes using one of the InterSystems IRIS built-in adapter classes. The following figure shows how a production accepts incoming requests:

[Image: Diagram demonstrating a message flowing from outside a production into an inbound adapter and onto a business service]

In general, when an external application makes a request for a certain action to be performed, the request comes into InterSystems IRIS via an inbound adapter, as shown in the previous figure. The requesting application is called a client application, because it has asked the production to do something. This application is a client of the production. The featured element at this step is the inbound adapter. This is a piece of code that adapts the client’s native request format to a one that is understandable to the production. Each application that makes requests of a production must have its own inbound adapter. No change to the client application code is needed, because the adapter handles calls that are already native to the client application.

### Defining an Inbound Adapter

To create an inbound adapter class, create a class as follows:

*   The class must extend Ens.InboundAdapter (or a subclass).
    
*   The class must implement the `OnTask()` method, as described in Implementing the OnTask() Method.
    
*   The class can define settings. See Adding and Removing Settings.
    
*   The class can implement any or all of the startup and teardown methods. See Overriding Start and Stop Behavior.
    
*   The class can include production credentials. See Including Credentials in an Adapter Class.
    
*   The class can contain methods to accomplish work internal to itself.
    

The following shows an example:

```objectscript
Class MyProduction.InboundAdapter Extends Ens.InboundAdapter
{

Parameter SETTINGS = "IPAddress,TimeOut";

Property IPAddress As %String(MAXLEN=100);

Property TimeOut As %Integer(MINVAL=0, MAXVAL=10);

Property Counter As %Integer;

Method OnTask() As %Status
{
  #; First, receive a message (note, timeout is in ms)
  Set msg = ..ReceiveMessage(..CallInterval*1000,.tSC)

  If ($IsObject(msg)) {
    Set tSC=..BusinessHost.ProcessInput(msg)
  }

  Quit tSC
}

}
```

### Implementing the OnTask() Method

The `OnTask()` method is where the actual work of the inbound adapter takes place. This method is intended to do the following things:

1.  Check for an incoming event. The inbound adapter can do this in many different ways: For example, it could wait for an incoming I/O event (such as reading from a TCP socket), or it could periodically poll for the existence of external data (such as a file).
    
    Most prebuilt inbound adapters have a setting called `CallInterval` that controls the time interval between calls to `OnTask()`. You could use this approach as well.
    
2.  Package the information from this event into an object of the type expected by the business service class.
    
3.  Call the `ProcessInput()` method of the business service object. This method is internal and cannot be seen in the class reference. Its signature is as follows:
    
    ```
    Method ProcessInput(pInput As %RegisteredObject, Output pOutput As %RegisteredObject, ByRef pHint As %String) As %Status {
    }
    ```
    
4.  If necessary, send an acknowledgment back to external system that the event was received.
    
5.  If there is more input data, `OnTask()` can do either of the following:
    
    *   Call `ProcessInput()` repeatedly until all the data is retrieved.
        
    *   Call `ProcessInput()` only once per `CallInterval`, even if multiple input events exist.
        

When designing an inbound adapter, it is important to keep in mind that the `OnTask()` method must periodically return control to the business service; that is, the `OnTask()` method must not wait indefinitely for an incoming event. It should, instead, wait for some period of time (say 10 seconds) and return control to the business service. The reason for this is that the business service object must periodically check for events from within InterSystems IRIS, such as notification that the production is being shut down.

Conversely, it is also important that the `OnTask()` method waits for events efficiently—sitting in a tight loop polling for events wastes CPU cycles and slows down an entire production. When an `OnTask()` method needs to wait, it should wait in such a way as to let its process go to sleep (such as waiting on an I/O event, or using the `Hang` command).

If your class is a subclass of a production adapter, then it probably implements the `OnTask()` method; therefore, your subclass might need to override a different method as specified by the inbound adapter class.

## Creating or Subclassing Outbound Adapters

This section describes how to create or subclass an outbound adapter.

### Introduction to Outbound Adapters

An outbound adapter is responsible for sending requests to external systems. The following figure shows how a production relays outgoing requests.

[Image: Diagram showing two messages of different types flowing from a business operation to an outbound adapter to an external syste]

The outbound adapter is a piece of code that adapts the native programming interface of an external application or external database into a form that is understandable to a production. Each external application or database that serves a production by means of a business operation must have its own outbound adapter. However, not every method in the external application or database needs to be mapped to the outbound adapter; only those operations that the production requires. As with inbound adapters, no change to the external application itself is needed to create an outbound adapter. And, the adapter itself is conceptually simple: It relays requests, responses, and data between the production and a specific application or database outside the production.

Outbound adapter classes work in conjunction with a business operation classes. In general, the outbound adapter contains general-purpose, reusable code while the business operation will contain production-specific code (such as special processing logic). Typically you will implement your outbound adapter classes using one of the InterSystems IRIS built-in adapter classes.

### Defining an Outbound Adapter

To create an outbound adapter class, create a class as follows:

*   The class must extend Ens.OutboundAdapter (or a subclass).
    
*   The class must define one or more methods for the corresponding business operation to invoke. Every outbound adapter is free to define its own API (set of methods) for use by the associated business operation classes.
    
*   The class can define settings. See Adding and Removing Settings.
    
*   The class can implement any or all of the startup and teardown methods. See Overriding Start and Stop Behavior.
    
*   The class can include production credentials. See Including Credentials in an Adapter Class.
    
*   The class can contain methods to accomplish work internal to itself.
    

## Including Credentials in an Adapter Class

To include production credentials in an adapter class, do the following in the class definition:

*   Include a setting named `Credentials`.
    
*   Define a method called `CredentialsSet()` that uses the value of the `Credentials` setting as a key to look up the username and password in the Credentials table. It then instantiates a credentials object that contains the username and password.
    

## Overriding Production Credentials

While the production credentials system centralizes management and keeps login data out of source code, sometimes you need to write code that gets credentials from another source. For example, your code might retrieve a username and password from a web form or cookie, and then use them with the HTTP outbound adapter to connect to some other site.

The way to handle this is in your business service or business operation code, do both of the following, before calling any adapter methods:

*   Provide code that instantiates a credentials object and assigns username and password values to it
    
*   Do not subsequently set the adapter `Credentials` property or call the adapter `CredentialsSet()` method, or the values may be reset.
    

For example:

```objectscript
  If ..Adapter.Credentials="" {
     Set ..Adapter.%CredentialsObj=##class(Ens.Config.Credentials).%New()
  }
  Set ..Adapter.%CredentialsObj.Username = tUsername
  Set ..Adapter.%CredentialsObj.Password = tPassword
```

Code such as this provides a credentials object that the EnsLib.HTTP.OutboundAdapter can use, but the values inside the object do not come from the Credentials table.

## Overriding Start and Stop Behavior

InterSystems IRIS provides a set of callback methods that you can override in order to add custom processing at start and stop times during the life cycle of the production, its business hosts, or its adapters. By default, these methods do nothing.

### Callbacks in the Production Class

If you have code that must execute before a production starts up, but that requires the InterSystems IRIS production framework to be running before it can execute, you must override the `OnStart()` method in the production class. Place these code statements in `OnStart()` so that they execute in the proper sequence: that is, after InterSystems IRIS has started, but before the production begins accepting requests. The `OnStop()` method is also available to perform a set of tasks before the production finishes shutting down.

### Callbacks in Business Host Classes

Each business host —business service, business process, or business operation—is a subclass of Ens.Host. In any of these classes you may override the `OnProductionStart()` method to provide code statements that you want InterSystems IRIS to execute on behalf of this host at production startup time. You can also implement the `OnProductionStop()` method.

For example, if your production requires different initial settings for property values, set the value in the `OnInit()` method of the business operation. For example, to change the initial setting of the `LineTerminator` property to depend on the operating system:

```objectscript
 Method OnInit() As %Status
  {
      Set ..Adapter.LineTerminator="$Select($$$isUNIX:$C(10),1:$C(13,10))"
      Quit $$$OK
  }
```

### Callbacks in Adapter Classes

An adapter class may override the `OnInit()` method. This method is called after the adapter object has been created and its configurable property values have been set. The `OnInit()` method provides a way for an adapter to perform any special setup actions.

For example, the following `OnInit()` method establishes a connection to a device when the adapter is started—assuming that this adapter also implements a `ConnectToDevice()` method:

```objectscript
Method OnInit() As %Status
{
  // Establish a connection to the input device
  Set tSC = ..ConnectToDevice()
  Quit tSC
}
```

An adapter class can also override the `OnTearDown()` method. This method is called during shutdown before the adapter object is destroyed. The `OnTearDown()` method provides a way for an adapter to perform any special cleanup actions.

For example, the following `OnTearDown()` method closes a connection to a device when the adapter is stopped, assuming that this adapter also implements a method named `CloseDevice()`:

```objectscript
Method OnTearDown() As %Status
{
  // close the input device
  Set tSC = ..CloseDevice()
  Quit tSC
}
```

## Programmatically Working with Lookup Tables

InterSystems IRIS provides the utility function called Lookup() so that you can easily perform a table lookup from a business rule or DTL data transformation. This function works only after you have created at least one lookup table and have populated it with appropriate data.

For information on defining lookup tables, see Defining Data Lookup Tables.

If you need more direct manipulation of lookup tables than the Management Portal provides, use the Ens.Util.LookupTable class. This class exposes lookup tables to access via objects or SQL. Additionally, it provides class methods to clear tables, export data as XML, and import data from XML.

Ens.Util.LookupTable provides the following string properties:

### TableName

Name of the lookup table, up to 255 characters. You can view the lookup tables defined in a namespace by selecting `Interoperability`, `Configure`, and `Data Lookup Tables` in the InterSystems IRIS portal and then selecting `Open`.

### KeyName

Key for the entry within the lookup table, up to 255 characters. This is the value from the `Key` field on the `Interoperability` > `Configure` > `Data Lookup Tables` page.

### DataValue

Value associated with this key in the lookup table, up to 32000 characters. This is the value from the `Value` field on the `Interoperability` > `Configure` > `Data Lookup Tables` page.

A sample SQL query might be:

```sql
SELECT KeyName,DataValue FROM Ens_Util.LookupTable WHERE TableName = 'myTab'
```

Ens.Util.LookupTable also provides the following class methods:

### %ClearTable()

Deletes the contents of the specified lookup table.

```objectscript
  do ##class(Ens.Util.LookupTable).%ClearTable("myTab")
```

### %Import()

Imports lookup table data from the specified XML file. For the import to be successful, the file must use the same XML format as that provided by the `%Export()` method of this class.

```objectscript
  do ##class(Ens.Util.LookupTable).%Import("myFile.xml")
```

### %Export()

Exports lookup table data to the specified XML file. If the file exists, InterSystems IRIS overwrites it with new data. If the file does not already exist, InterSystems IRIS creates it. The following example exports only the contents of the specified lookup table, `myTab`:

```objectscript
  do ##class(Ens.Util.LookupTable).%Export("myFile.xml","myTab")
```

The following example exports the contents of all lookup tables in the namespace:

```objectscript
  do ##class(Ens.Util.LookupTable).%Export("myFile.xml")
```

The resulting XML file looks like the following example. Note that all entries, in all tables, appear as sibling <entry> elements inside a single <lookupTable> element.

```xml
<?xml version="1.0"?>
<lookupTable>
  <entry table="myOtherTab" key="myKeyA">aaaaaa</entry>
  <entry table="myOtherTab" key="myKeyB">bbbbbbbbb</entry>
  <entry table="myTab" key="myKey1">1111</entry>
  <entry table="myTab" key="myKey2">22222</entry>
  <entry table="myTab" key="myKey3">333333</entry>
</lookupTable>
```

For each <entry>, the `table` attribute identifies the table that contains the entry. The `key` attribute gives the name of the key. The text contents of the <entry> element provide the entry’s value.

In addition to the XML format described above, you can use the SQL Import Wizard to import comma-separated value (CSV) files that list tables and keys.

## Defining a Custom Archive Manager

For InterSystems IRIS, the Management Portal provides a tool called the Archive Manager; this is described in Using the Archive Manager. You can define and use a custom Archive Manager. To do so, create a class as follows:

*   It can use Ens.Archive.Manager as a superclass.
    
*   It must define the `DoArchive()` method, which has the following signature:
    
    ```
    ClassMethod DoArchive() As %Status
    ```
    

An alternative option is to use the Enterprise Message Bank, which enables you to archive messages from multiple productions. For an overview, see Defining the Enterprise Message Bank.
