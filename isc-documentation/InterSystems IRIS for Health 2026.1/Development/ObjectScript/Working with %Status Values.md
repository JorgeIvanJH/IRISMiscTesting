# Working with %Status Values

When working with an API that returns %Status values (a status), it is best practice to check the status before proceeding, and continue with normal processing only in the case of success. In your own code, you can also return status values (and check them elsewhere as appropriate).

This page discusses status values and how to work with them.

> **Note:**
> 
> Status checking is not error checking per se. Your code should also use TRY-CATCH processing to trap unexpected, unforeseen errors.

## Basics of Working with Status Values

Methods in many InterSystems IRIS data platform classes return a %Status (%Library.Status) value to indicate success or error. If the status represents an error or errors, the status also includes information about the errors. For example, the `%Save()` method in %Library.Persistent returns a status. For any such method, be sure to obtain the returned status. Then check the status and then proceed appropriately. There are two possible scenarios:

*   In the case of success, the status equals 1.
    
*   In the case of failure, the status is an encoded string containing the error status and one or more error codes and text messages. Status text messages are localized for the language of your locale. InterSystems IRIS provides methods and macros for processing the value so that you can understand the nature of the failure.
    

The basic tools are as follows:

*   To check whether the status represents success or error, use any of the following:
    
    *   The `$$$ISOK` and `$$$ISERR` macros, which are defined in the include file `%occStatus.inc`. This include file is automatically available in all object classes.
        
    *   The `$SYSTEM.Status.IsOK()` and `$SYSTEM.Status.IsError()` methods.
        
*   To display the error details, use `$SYSTEM.Status.DisplayError()`, which writes output to the current device.
    
*   To obtain a string that contains the error details, use `$SYSTEM.Status.GetErrorText()`.
    

The special variable `$SYSTEM` is bound to the `%SYSTEM` package. This means that the methods in the previous list are in the %SYSTEM.Status and %SYSTEM.OBJ classes; see the class reference for details.

## Examples

For example:

```objectscript
 Set object=##class(Sample.Person).%New()
 Set object.Name="Smith,Janie"
 Set tSC=object.%Save()
 If $$$ISERR(tSC) {
   Do $SYSTEM.Status.DisplayError(tSC)
   Quit
 }
```

Here is a partial example that shows use of `$SYSTEM.Status.GetErrorText()`:

```
 If $$$ISERR(tSC) {
   // if error, log error message so users can see them
   Do ..LogMsg($System.Status.GetErrorText(tSC))
 }
```

> **Note:**
> 
> Some ObjectScript programmers use the letter `t` as a prefix to indicate a temporary variable, so you might see `tSC` used as a variable name in code samples, meaning “temporary status code.” You are free to use this convention, but there is nothing special about this variable name.

## Variation (%objlasterror)

Some methods, such as `%New()`, do not return a %Status but instead update the `%objlasterror` variable to contain the status. `%New()` either returns an OREF to an instance of the class upon success, or the null string upon failure. You can retrieve the status value for methods of this type by accessing the `%objlasterror` variable, as shown in the following example.

```objectscript
  Set session = ##class(%CSP.Session).%New()
  If session="" {
      Write "session OREF not created",!
      Write "%New error is ",!,$System.Status.GetErrorText(%objlasterror),!
  } Else {
      Write "session OREF is ",session,!
  }
```

For more information, refer to the %SYSTEM.Status class.

## Multiple Errors Reported in a Status Value

If a status value represents multiple errors, the previous techniques give you information about only the latest. %SYSTEM.Status provides methods you can use to retrieve individual errors: GetOneErrorText() and GetOneStatusText(). For example:

```objectscript
CreateCustomErrors
  SET st1 = $System.Status.Error(83,"my unique error")
  SET st2 = $System.Status.Error(5001,"my unique error")
  SET allstatus = $System.Status.AppendStatus(st1,st2)
DisplayErrors
  WRITE "All together:",!
  WRITE $System.Status.GetErrorText(allstatus),!!
  WRITE "One by one",!
  WRITE "First error format:",!
  WRITE $System.Status.GetOneStatusText(allstatus,1),!
  WRITE "Second error format:",!
  WRITE $System.Status.GetOneStatusText(allstatus,2),!
```

Another option is `$SYSTEM.Status.DecomposeStatus()`, which returns an array of the error details (by reference, as the second argument). For example:

```
 Do $SYSTEM.Status.DecomposeStatus(tSC,.errorlist)
 //then examine the errorlist variable
```

The variable `errorlist` is a multidimensional array that contains the error information. The following shows a partial example with some artificial line breaks for readability:

```
ZWRITE errorlist
errorlist=2
errorlist(1)="ERROR #5659: Property 'Sample.Person::SSN(1@Sample.Person,ID=)' required"
errorlist(1,"caller")="%ValidateObject+9^Sample.Person.1"
errorlist(1,"code")=5659
errorlist(1,"dcode")=5659
errorlist(1,"domain")="%ObjectErrors"
errorlist(1,"namespace")="SAMPLES"
errorlist(1,"param")=1
errorlist(1,"param",1)="Sample.Person::SSN(1@Sample.Person,ID=)"
...
errorlist(2)="ERROR #7209: Datatype value '' does not match
PATTERN '3N1""-""2N1""-""4N'"_$c(13,10)_"  >
ERROR #5802: Datatype validation failed on property 'Sample.Person:SSN',
with value equal to """""
errorlist(2,"caller")="zSSNIsValid+1^Sample.Person.1"
errorlist(2,"code")=7209
...
```

If you wanted to log each error message, you could adapt the previous logging example as follows:

```
 If $$$ISERR(tSC) {
   // if error, log error message so users can see them
   Do $SYSTEM.Status.DecomposeStatus(tSC,.errorlist)
   For i=1:1:errorlist {
       Do ..LogMsg(errorlist(i))
   }
 }
```

> **Note:**
> 
> If you call `DecomposeStatus()` again and pass in the same error array, any new errors are appended to the array.

## Returning a %Status

You can return your own custom status values. To create a %Status, use the following construction:

```
 $$$ERROR($$$GeneralError,"your error text here","parm","anotherparm")
```

Or equivalently:

```
 $SYSTEM.Status.Error($$$GeneralError,"your error text here","parm","anotherparm")
```

Where `"parm"` and `"anotherparm"` represent optional additional error arguments, such as filenames or identifiers for records where the processing did not succeed.

For example:

```
 quit $$$ERROR($$$GeneralError,"Not enough information for request")
```

To include information about additional errors, use `$SYSTEM.Status.AppendStatus()` to modify the status value. For example:

```
 set tSC=$SYSTEM.Status.AppendStatus(tSCfirst,tSCsecond)
 quit tSC
```

## %SYSTEM.Error

The %SYSTEM.Error class is a generic error object. It can be created from a %Status error, from an exception object, a `$ZERROR` error, or an SQLCODE error.

You can use %SYSTEM.Error class methods to convert a %Status to an exception, or to convert an exception to a %Status.

## See Also

For more information, see the class reference for the %SYSTEM.Status class and the %Status (%Library.Status) class.
