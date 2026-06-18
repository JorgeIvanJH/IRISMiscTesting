# Using TRY-CATCH

Managing the behavior of code when an error (particularly an unexpected error) occurs is called error handling or error processing. Error handling includes the following operations:

*   Correcting the condition that caused the error
    
*   Performing some action that allows execution to resume despite the error
    
*   Diverting the flow of execution
    
*   Logging information about the error
    

InterSystems IRIS data platform supports a `TRY`-`CATCH` mechanism for handling errors. Note that in code migrated from older applications, you might see traditional error processing, which is still fully supported, but is not intended for use in new applications.

Also see %Status Processing, which is not error handling in a strict sense. Typically status processing is fully contained within a `TRY` block.

## Introduction

With `TRY`-`CATCH`, you can establish delimited blocks of code, each called a `TRY` block; if an error occurs during a `TRY` block, control passes to the `TRY` block’s associated `CATCH` block, which contains code for handling the exception. A `TRY` block can also include `THROW` commands; each of these commands explicitly issues an exception from within a `TRY` block and transfers execution to a `CATCH` block.

To use this mechanism in its most basic form, include a `TRY` block within ObjectScript code. If an exception occurs within this block, the code within the associated `CATCH` block is then executed. The form of a `TRY`-`CATCH` block is:

```
 TRY {
      protected statements
 } CATCH [ErrorHandle] {
      error statements
 }
 further statements
```

where:

*   The `TRY` command identifies a block of ObjectScript code statements enclosed in curly braces. `TRY` takes no arguments. This block of code is protected code for structured exception handling. If an exception occurs within a `TRY` block, InterSystems IRIS sets the exception properties (oref.Name, oref.Code, oref.Data, and oref.Location), `$ZERROR`, and `$ECODE`, then transfers execution to an exception handler, identified by the `CATCH` command. This is known as throwing an exception.
    
*   The `protected statements` are ObjectScript statements that are part of normal execution. (These can include calls to the `THROW` command. This scenario is described in the following section.)
    
*   The `CATCH` command defines an exception handler, which is a block of code to execute when an exception occurs in a `TRY` block.
    
*   The `ErrorHandle` variable is a handle to an exception object. This can be either an exception object that InterSystems IRIS has generated in response to a runtime error or an exception object explicitly issued by invoking the `THROW` command (described in the next section).
    
*   The `error statements` are ObjectScript statements that are invoked if there is an exception.
    
*   The `further statements` are ObjectScript statements that either follow execution of the `protected statements` if there is no exception or follow execution of the error statements if there is an exception and control passes out of the `CATCH` block.
    

Depending on events during execution of the protected statements, one of the following events occurs:

*   If an error does not occur, execution continues with the `further statements` that appear outside the `CATCH` block.
    
*   If an error does occur, control passes into the `CATCH` block and `error statements` are executed. Execution then depends on contents of the `CATCH` block:
    
    *   If the `CATCH` block contains a `THROW` or `GOTO` command, control goes directly to the specified location.
        
    *   If the `CATCH` block does not contain a `THROW` or `GOTO` command, control passes out of the `CATCH` block and execution continues with the `further statements`.
        

## Using THROW with TRY-CATCH

InterSystems IRIS issues an implicit exception when a runtime error occurs. To issue an explicit exception, the `THROW` command is available. The `THROW` command transfers execution from the `TRY` block to the `CATCH` exception handler. The `THROW` command has a syntax of:

```
THROW expression
```

where `expression` is an instance of a class that inherits from the %Exception.AbstractException class, which InterSystems IRIS provides for exception handling. For more information on %Exception.AbstractException, see the following section.

The form of the `TRY`/`CATCH` block with a `THROW` is:

```
 TRY {
      protected statements
      THROW expression
      protected statements
 }
 CATCH exception {
      error statements
 }
 further statements
```

where the `THROW` command explicitly issues an exception. The other elements of the `TRY`-`CATCH` block are as described in the previous section.

The effects of `THROW` depends on where the throw occurs and the argument of `THROW`:

*   A `THROW` within a `TRY` block passes control to the `CATCH` block.
    
*   A `THROW` within a `CATCH` block passes control up the execution stack to the next error handler. If the exception is a %Exception.SystemException object, the next error handler can be any type (`CATCH` or traditional); otherwise there must be a `CATCH` to handle the exception or a <NOCATCH> error will be thrown.
    

If control passes into a `CATCH` block because of a `THROW` with an argument, the `ErrorHandle` contains the value from the argument. If control passes into a `CATCH` block because of a system error, the `ErrorHandle` is a %Exception.SystemException object. If no `ErrorHandle` is specified, there is no indication of why control has passed into the `CATCH` block.

For example, suppose there is code to divide two numbers:

```
div(num,div) public {
 TRY {
  SET ans=num/div
 } CATCH errobj {
  IF errobj.Name="<DIVIDE>" { SET ans=0 }
  ELSE { THROW errobj }
 }
 QUIT ans
}
```

If a divide-by-zero error happens, the code is specifically designed to return zero as the result. For any other error, the `THROW` sends the error on up the stack to the next error handler.

## Using $$$ThrowOnError and $$$ThrowStatus Macros

InterSystems IRIS provides macros for use with exception handling. When invoked, these macros throw an exception object to the `CATCH` block.

The following example invokes the `$$$ThrowOnError()` macro when an error status is returned by the `%Prepare()` method:

```objectscript
  #include %occStatus
  TRY {
    SET myquery = "SELECT TOP 5 Name,Hipness,DOB FROM Sample.Person"
    SET tStatement = ##class(%SQL.Statement).%New()
    SET status = tStatement.%Prepare(myquery)
    $$$ThrowOnError(status)
    WRITE "%Prepare succeeded",!
    RETURN
  }
  CATCH sc {
    WRITE "In Catch block",!
    WRITE "error code: ",sc.Code,!
    WRITE "error location: ",sc.Location,!
    WRITE "error data:",$LISTGET(sc.Data,2),!
  RETURN
  }
```

The following example invokes `$$$ThrowStatus` after testing the value of the error status returned by the `%Prepare()` method:

```objectscript
  #include %occStatus
  TRY {
    SET myquery = "SELECT TOP 5 Name,Hipness,DOB FROM Sample.Person"
    SET tStatement = ##class(%SQL.Statement).%New()
    SET status = tStatement.%Prepare(myquery)
    IF ($System.Status.IsError(status)) {
      WRITE "%Prepare failed",!
      $$$ThrowStatus(status) }
    ELSE {WRITE "%Prepare succeeded",!
      RETURN }
  }
  CATCH sc {
    WRITE "In Catch block",!
    WRITE "error code: ",sc.Code,!
    WRITE "error location: ",sc.Location,!
    WRITE "error data:",$LISTGET(sc.Data,2),!
  RETURN
  }
```

See System Macros for more information.

## Using the %Exception.SystemException and %Exception.AbstractException Classes

InterSystems IRIS provides the %Exception.SystemException and %Exception.AbstractException classes for use with exception handling. %Exception.SystemException inherits from the %Exception.AbstractException class and is used for system errors. For custom errors, create a class that inherits from %Exception.AbstractException. %Exception.AbstractException contains properties such as the name of the error and the location at which it occurred.

When a system error is caught within a `TRY` block, the system creates a new instance of the %Exception.SystemException class and places error information in that instance. When throwing a custom exception, the application programmer is responsible for populating the object with error information.

An exception object has the following properties:

*   Name — The error name, such as <UNDEFINED>
    
*   Code — The error number
    
*   Location — The label+offset^routine location of the error
    
*   Data — Any extra data reported by the error, such as the name of the item causing the error
    

## Other Considerations with TRY-CATCH

The following describe conditions that may arise when using a `TRY`-`CATCH` block.

### QUIT within a TRY-CATCH Block

A `QUIT` command within a `TRY` or `CATCH` block passes control out of the block to the next statement after the `TRY`-`CATCH` as a whole.

### TRY-CATCH and the Execution Stack

The `TRY` block does not introduce a new level in the execution stack. This means that it is not a scope boundary for `NEW` commands. The error statements execute at the same level as that of the error. This can result in unexpected results if there are `DO` commands within the protected statements and the `DO` target is also within the protected statements. In such cases, the `$ESTACK` special variable can provide information about the relative execution levels.

### Using TRY-CATCH with Traditional Error Processing

`TRY`-`CATCH` error processing is compatible with `$ZTRAP` error traps used at different levels in the execution stack. The exception is that `$ZTRAP` may not be used within the protected statements of a `TRY` clause. User-defined errors with a `THROW` are limited to `TRY`-`CATCH` only. User-defined errors with the `ZTRAP` command may be used with any type of error processing.
