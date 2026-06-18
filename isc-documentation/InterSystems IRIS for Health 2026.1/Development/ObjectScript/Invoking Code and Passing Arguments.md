# Invoking Code and Passing Arguments

This page describes how to invoke units of code and pass arguments to that code.

For an introduction to the commands shown here, see Commands to Invoke Code.

## Calling Units of Code

The syntax to call a unit of code depends on the type of code you are calling, as well as whether you are obtaining any value returned by that code:

### ObjectScript function

To call an ObjectScript function, write an expression of the following form, including that expression wherever the resulting value is needed:

```
 $functionName(args)
```

For example:

```
 set myvariable=$length("this is a sample string")
```

### routines

To call a routine, use the DO command or one of the other commands to invoke code, with syntax that refers to the routine name:

```
 DO ^routinename
```

```
 JOB ^routinename
```

### procedure

To call a procedure, use either the DO command or one of the other commands to invoke code, with syntax that refers to the procedure name:

```
 DO procedure^routinename
```

```
 JOB procedure^routinename
```

You can omit the `^routinename` part if this command is within the same routine.

If the procedure accepts arguments, you can include the argument list at the end, for example:

```
 DO procedure^routinename(argument1,argument2)
```

Depending on the procedure implementation, it can return a value. If so, and if you want to obtain the value, write an expression of the following form:

```
$$procedure^routinename
```

For example:

```
 set myvariable=$$procedure^routinename
```

You can omit the `^routinename` part if this command is within the same routine.

As before, if the procedure accepts arguments, you can include the argument list at the end, for example:

```
$$procedure^routinename(argument1,argument2)
```

If you attempt to access a private procedure from outside the routine that defines it, a <NOLINE> error occurs.

### methods

To invoke a class method, use an expression of the following form:

```
##class(Package.Class).MethodName(args)
```

For example:

```
do ##class(Package.Class).MethodName(args)
```

Or:

```
set myvariable=##class(Package.Class).MethodName(args)
```

Unlike with procedures, you must include the trailing parentheses even if the method takes no arguments.

To invoke an instance method, you first need an OREF that contains a reference to the relevant object. For example:

```
 set oref=##class(Sample.Class).%OpenId(10000)
 do oref.WriteAddress()
```

Or:

```
 set oref=##class(Sample.Class).%OpenId(10000)
 set myvariable=oref.WriteAddress()
```

For details and variations, see Working with Registered Objects.

## Formal Argument Lists and Examples

Each ObjectScript function, each procedure (or other form of subroutine), and each method has (or can have) a formal argument list, which is a comma-separated list of arguments. This section presents basic examples.

### ObjectScript functions

For an ObjectScript function, the corresponding reference page shows the formal argument list. For example, the reference page for the `$LENGTH` function shows the formal argument list as follows:

```
$LENGTH(expression,delimiter)
```

### Methods

For methods, the class documentation shows the formal argument list and any generated comments, and you can also view the code directly in your IDE. In contrast to the ObjectScript function documentation, the formal argument list includes information about the expected values of the arguments and default values.

For example, %Library.File shows the formal argument list for the `NormalizeFilename()` method as follows:

```
classmethod NormalizeFilename(filename As %String, directory As %String = "") as %String
```

### procedures and other forms of subroutines

For any type of subroutine explained in the documentation, the documentation generally shows the formal argument list in context—for example as part of the command you would use. For example, the reference page for the `^PERFMON` routine shows the syntax for calling the `Collect()` function within this routine, as follows:

```
 set status = $$Collect^PERFMON(time,format,output)
```

For any new routines, InterSystems suggests you create procedures, but you may encounter legacy forms of subroutines.

## Passing Arguments (Basics)

When you invoke a unit of code, you pass arguments, usually using syntax of the following general form:

```
 codeunitidentifier(arg1,arg2,arg3)
```

Note the following general points:

*   This syntax passes arguments by value. An alternative, less common-form passes arguments by reference.
    
*   Some units of code do not accept any arguments.
    
    If the unit of code is a method or an ObjectScript function, you must include the parentheses after its name. If the unit of code is a subroutine (of any form), you do not need to include the parentheses after its name.
    
*   InterSystems IRIS maps the given arguments, by position, to the corresponding arguments in the formal argument list. Thus, the value of the first arguments in the actual list is placed in the first variable in the formal list; the second value is placed in the second variable; and so on.
    
    The matching of these arguments is done by position, not name.
    
*   In some cases, some arguments are optional. If an argument is optional, and you need to specify an argument in a later position, simply use commas to skip the arguments that you do not want to pass. For example:
    
    ```
     set myval=##class(Sample.MyClass).MyMethod(arg1,,,arg4)
    ```
    
*   If you pass more arguments than are present in the formal argument list, a <PARAMETER> error occurs. (This does not include code units that accept a variable number of arguments; these never produce a <PARAMETER> error.)
    

Variations are discussed in the following sections.

## Passing ByRef or Output Arguments

Some argument lists include the keyword `ByRef` or the keyword `Output` before one or more arguments. For example:

*   %Library.Persistent shows the formal argument list for the `%OpenID()` method as follows, with line breaks for readability:
    
    ```
    classmethod %OpenID(id As %String="",
                        concurrency As %Integer = -1,
                        ByRef sc As %Status = $$$OK) as %ObjectHandle
    ```
    
*   %Library.File shows the formal argument list for the `Exists()` method as follows:
    
    ```
    classmethod Exists(filename As %String, Output return As %Integer) as %Boolean
    ```
    

In these cases, when calling such units of code, place a period immediately before any `ByRef` or `Output` argument. This means that the argument must be a variable, rather than a literal or other kind of expression.

In these cases, you are passing the given argument by reference. In general, this means that this argument is set by or updated by the code unit that you are calling. Similarly, this means that the argument then contains a value intended for your use, such as in deciding how to proceed.

For example, when calling the `Exists()` method of the %Library.File class, use a period before the second argument:

```
 set status=##class(%Library.File).Exists("c:\temp\check.txt",.returncode)
```

As indicated in the class reference, the second argument contains the value obtained from the operating system when this check is performed.

Similarly, when calling the `%OpenID()` method of %Library.Persistent, inherited by all persistent classes, use a period before the third argument:

```
 set myvar=##class(MyPackage.MyClass).%OpenId(10034,,.statuscode)
```

As indicated in the class reference, the third argument contains the status code that indicates success or failure ( and the reason, in case of failure).

Except for ObjectScript functions, any unit of code can be written to accept arguments passed by reference.

For information on defining a method this way, see Indicating How Arguments Are to Be Passed.

## Comparison: Arguments by Value and Arguments by Reference

This section describes the differences between the two ways of passing arguments. This section first discusses passing local variables with no subscripts (the most common scenario).

As with other programming languages, InterSystems IRIS has a memory location that contains the value of each local variable. The name of the variable acts as the address to the memory location.

When you pass a local variable with no subscripts to a method, you pass the variable by value. This means that the system makes a copy of the value, so that the original value is not affected. To pass the memory address instead, place a period immediately before the name of the variable in the argument list.

To demonstrate this, consider the following method in a class called `Test.Parameters`:

```objectscript
ClassMethod Square(input As %Integer) As %Integer
{
    set answer=input*input
    set input=input + 10
    return answer
}
```

Suppose that you define a variable and pass it by value to this method:

```objectscript
TESTNAMESPACE>set myVariable = 5

TESTNAMESPACE>write ##class(Test.Parameters).Square(myVariable)
25
TESTNAMESPACE>write myVariable
5
```

In contrast, suppose that you pass the variable by reference:

```objectscript
TESTNAMESPACE>set myVariable = 5

TESTNAMESPACE>write ##class(Test.Parameters).Square(.myVariable)
25
TESTNAMESPACE>write myVariable
15
```

Consider the following method, which writes the contents of the argument it receives:

```
ClassMethod WriteContents(input As %String)
{
    zwrite input
}
```

Now, suppose you have an array with three nodes:

```objectscript
TESTNAMESPACE>zwrite myArray
myArray="Hello"
myArray(1)="My"
myArray(2)="Friend"
```

If you pass the array to the method by value, you are only passing the top-level node:

```objectscript
TESTNAMESPACE>do ##class(Test.Parameters).WriteContents(myArray)
input="Hello"
```

If you pass the array to the method by reference, you are passing the entire array:

```objectscript
TESTNAMESPACE>do ##class(Test.Parameters).WriteContents(.myArray)
input="Hello"
input(1)="My"
input(2)="Friend"
```

You can pass the value of a single node of a global to a method:

```objectscript
TESTNAMESPACE>zwrite ^myGlobal
^myGlobal="Start"
^myGlobal(1)="Your"
^myGlobal(2)="Engines"
TESTNAMESPACE>do ##class(Test.Parameters).WriteContents(^myGlobal)
input="Start"
```

Trying to pass a global to a method by reference results in a syntax error:

```objectscript
TESTNAMESPACE>do ##class(Test.Parameters).WriteContents(.^myGlobal)
^
<SYNTAX>
```

The following table summarizes all the possibilities:

<table><tr><th>Kind of Variable</th><th>Passing by Value</th><th>Passing by Reference</th></tr><tr><td>Local variable with no subscripts</td><td>The standard way in which these variables are passed</td><td>Allowed</td></tr><tr><td>Local with subscripts (array)</td><td>Passes the value of a single node</td><td>The standard way in which these variables are passed</td></tr><tr><td>Global variable with or without subscripts</td><td>Passes the value of a single node</td><td>Cannot be passed this way (data for a global is not in memory)</td></tr><tr><td>Object Reference (OREF)</td><td>The standard way in which these variables are passed</td><td>Allowed</td></tr></table>

* If you have a variable representing an object, you refer to the object by means of an object reference (OREF). When you pass an OREF as an argument, you typically pass it by value. However, since an OREF is a pointer to the object, you are effectively passing the object by reference. Changing the value of a property of the object inside the method changes the actual object, not a copy of the object. Passing an OREF by reference is allowed and can be used if you want to change the OREF to point to a different object. This is not a common usage. See Objects for more information on objects and object references.

## Passing a Variable Number of Arguments

Some units of code can accept a variable number of arguments. For example:

*   The reference page for the `$CLASSMETHOD` function shows the formal argument list as follows:
    
    ```
    $CLASSMETHOD(classname, methodname, arg1, arg2, arg3, ... )
    ```
    
    In this case, `arg1`, `arg2`, and `arg3` are placeholders, and the three trailing periods indicate that this function can accept a variable number of arguments.
    
*   %SQL.Statement shows the formal argument list for the `%Execute()` method as follows:
    
    ```
    method %Execute(%parm...) as %SQL.StatementResult
    ```
    
    Notice the three periods after the argument. This syntax indicates that the method accepts a variable number of arguments.
    

With a variable number of arguments like this, you can pass a set of arguments—of varying number—to another unit of code, which has a argument list that may not be known in advance. In all cases when a variable number of arguments are accepted, you should list these arguments in the order expected by the applicable downstream unit of code. Separate these arguments with commas as usual. (Or create and pass a multidimensional array, as described in the subsection.)

For example, the `$CLASSMETHOD` function enables you to invoke a class method, passing to it any arguments of that method. Suppose that `MyPkg.MyClass` has a method with the following signature:

```objectscript
ClassMethod SampleMethod(arg1 as %Integer,arg2 as %String,arg3 as %String) as %String {
}
```

You could invoke this method as follows:

```objectscript
 set a=10
 set b="abc"
 set c=$username
 set myvar=$CLASSMETHOD("MyPkg.MyClass","SampleMethod",a,b,c)
```

Similarly, as seen above, the `%Execute()` method accepts a variable number of arguments, which are all passed, in order, to the query being executed by the %SQL.Statement instance.

For information on defining a method this way, see Specifying a Variable Number of Arguments.

### Variation: Using a Multidimensional Array

When a method accepts a variable number of arguments, you can create and pass a multidimensional array that contains the arguments. This is best explained via an example, using the previous example method:

```objectscript
 set myargs=3
 set myargs(1)=10
 set myargs(2)="abc"
 set myargs(3)=$username
 set myvar=$CLASSMETHOD("MyPkg.MyClass","SampleMethod",myargs...)
```

Notice that the top node of the multidimensional array indicates the number of array elements and the subscripts are integers starting with 1. Also notice the three periods after the name of the multidimensional array.

This technique provides a useful way to pass a variable number of arguments when using %SQL.Statement. For example:

```
   Set sql="SELECT * FROM Test.Test WHERE A=?"
   Set params($INCREMENT(params))="value 0"
   If condition1 {
      Set sql=sql_" AND B=?"
      Set params($INCREMENT(params))="value 1"
    }
    If condition2 {
        Set sql=sql_" AND C=?"
        Set params($INCREMENT(params))="value 2"
    }
    Set statementResult=##class(%SQL.Statement).%ExecDirect(,sql,params...)
```
