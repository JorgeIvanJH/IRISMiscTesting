# Procedure Syntax

This topic describes the syntax for procedures, which are defined within ObjectScript routines.

## Introduction

The syntax for a procedure is as follows:

```
 label(argumentlist) accessmode
  {
   implementation
  }
```

Or:

```
 label(argumentlist) [pubvarlist] accessmode
  {
   implementation
  }
```

Where:

### label

The procedure name, a standard label. It must start in column one. The parentheses following the label are mandatory, even if there are no arguments.

### argumentlist

A comma-separated list of arguments in the following form:

```
argument1,argument2,argument3,...
```

An argument can have a default value, as follows:

```
argument1=default1,argument2=default2,argument3=default3,...
```

These expected arguments are known as the formal arguments list. Even in a case when the procedure takes no arguments, the procedure definition must include parentheses. The maximum number of formal parameters is 255.

Any default value must be a literal: either a number, or a string enclosed in quotation marks. You can specify a null string (`""`) as a default value. This differs from specifying no default value, because a null string defines the variable, whereas the variable for a parameter with no specified or default value would remain undefined. If you specify a default value that is not a literal, InterSystems IRIS issues a <PARAMETER> error./

### pubvar

Public variables. An optional comma-separated list of public variables used by the procedure and available to other routines and procedures. This is a list of variables both defined within this procedure and available to other routines and defined within another routine and available to this procedure. If specified, `pubvar` is enclosed in square brackets. If no `pubvar` is specified, the square brackets may be omitted. The public variables can include arguments specified for this procedure.

> **Note:**
> 
> Most procedures do not declare a list of public variables. In newer code, a list of public variables is a less commonly used feature of ObjectScript.

### accessmode

An optional keyword that controls how this procedure can be used. This must be one of the following:

*   `PUBLIC`, which declares that this procedure can be called from any routine.
    
*   `PRIVATE`, which declares that this procedure can only be called from the routine in which it is defined. `PRIVATE` is the default.
    

For instance the following defines a public procedure:

```objectscript
MyProc(x,y) PUBLIC { }
```

In contrast, the following examples define a private procedures:

```objectscript
MyProc(x,y) PRIVATE { }

MyProc2(x,y) { }
```

### implementation

ObjectScript commands. The opening curly brace ({) must be separated from the characters preceding and following it by at least one space or a line break. The closing curly brace (}) must not be followed by any code on the same line; it can only be followed by blank space or a comment. The closing curly brace can be placed in column one. This block of code is only entered by the label.

## Procedures as Functions

If an ObjectScript procedure returns a value, it is also called a function. Such a function is also sometimes called an extrinsic function, to distinguish it from built-in ObjectScript functions (which are sometimes called intrinsic functions).

To return a value from a procedure, use the RETURN command.

## Procedure Variables

Procedures and methods both support private and public variables; all of the following statements apply equally to procedures and methods:

Variables used within procedures are automatically private to that procedure. To share some of these variables with procedures that this procedure calls, pass them as parameters to the other procedures.

### Public Variable List

Via the public variable list, you can also declare public variables. These are available to all procedures and methods; those that this procedure or method calls and those that called this procedure or method. A relatively small number of variables should be defined in this way, to act as environmental variables for an application. To define public variables, list them in square brackets following the procedure name and its parameters.

The following example defines a sample procedure `proc1` with declared public variables `a` and `b`, as well as the private variables `c` and `d`:

```objectscript
proc1() [a, b]
    {
    WRITE !, "setting a"  SET a = 1
    WRITE !, "setting b"  SET b = 2
    WRITE !, "setting c"  SET c = 3
    SET d = a + b + c
    WRITE !, "The sum is: ", d
    }
```

After you execute this procedure, the variables `a` and `b` are available, and they hold the values last assigned by this procedure. In contrast, the private variables `c` and `d` exist only when `proc1` is running.

### Making Formal List Parameters Public

If a procedure has a formal list parameter, (such as x or y in `MyProc(x,y)` ) that is needed by other procedures it calls, then the parameter should be listed in the public list.

Thus,

```objectscript
MyProc(x,y)[x] {
 DO abc^rou
 }
```

makes the value of `x`, but not `y`, available to the routine abc^rou.

### Private Variables versus Variables Created with NEW

Note that private variables are not the same as variables newly created with `NEW`. If a procedure wants to make a variable directly available to other procedures or subroutines that it calls, then it must be a public variable and it must be listed in the public list. If it is a public variable being introduced by this procedure, then it makes sense to perform a `NEW` on it. That way it will be automatically destroyed when the procedure exits, and also it protects any previous value that public variable may have had. For example, the code:

```objectscript
MyProc(x,y)[name]{
 NEW name
 SET name="John"
 DO xyz^abc
}
```

enables procedure `xyz` in routine `abc` to see the value John for `name`, because it is public. Invoking the `NEW` command for `name` protects any public variable named name that may already have existed when the procedure `MyProc` was called.

The `NEW` command does not affect private variables; it only works on public variables. Within a procedure, it is illegal to specify `NEW x` or `NEW (x)` if `x` is not listed in the public list and `x` is not a % variable.

## Procedure Code

The body of code between the braces is the procedure code. Note the following points:

*   A procedure can only be entered at the procedure label. Access to the procedure through `label+offset` syntax is not allowed.
    
*   Any labels in the procedure are private to the procedure and can only be accessed from within the procedure. The PRIVATE keyword can be used on labels within a procedure, although it is not required. The PUBLIC keyword cannot be used on labels within a procedure — it yields a syntax error. Even the system function `$TEXT` cannot access a private label by name, although `$TEXT` does support `label+offset` using the procedure label name.
    
*   Duplicate labels are not permitted within a procedure but, under certain circumstances, are permitted within a routine. Specifically, duplicate labels are permitted within different procedures. Also, the same label can appear within a procedure and elsewhere within the routine in which the procedure is defined. For instance, the following three occurrences of `Label1` are permitted:
    
    ```objectscript
    Rou1 // Rou1 routine
    Proc1(x,y) {
    Label1 // Label1 within the proc1 procedure within the Rou1 routine
    }
    
    Proc2(a,b,c) {
    Label1 // Label1 within the Proc2 procedure (local, as with previous Label1)
    }
    
    Label1 // Label1 that is part of Rou1 and neither procedure
    ```
    
*   If the procedure contains a `DO` command or user-defined function without a routine name, it refers to a label within the procedure, if one exists. Otherwise, it refers to a label in the routine but outside of the procedure.
    
*   If the procedure contains a `DO` or user-defined function with a routine name, it always identifies a line outside of the procedure. This is true even if that name identifies the routine that contains the procedure. For example:
    
    ```objectscript
    ROU1 ;
    PROC1(x,y) {
     DO Label1^ROU1
    Label1 ;
     }
    Label1 ; The DO calls this label
    ```
    
*   If a procedure contains a `GOTO`, it must be to a private label within the procedure. You cannot exit a procedure with a `GOTO`.
    
*   `label+offset` syntax is not supported within a procedure, with a few exceptions:
    
    *   `$TEXT` supports `label+offset` from the procedure label.
        
    *   `GOTO label+offset` is supported in direct mode lines from the procedure label as a means of returning to the procedure following a `Break` or error.
        
    *   The `ZBREAK` command supports a specification of `label+offset` from the procedure label.
        
*   When the procedure ends, the system restores the `$TEST` state that had been in effect when the procedure was called.
    
*   The `}` that denotes the end of the procedure can be in any character position on the line, including the first character position. Code can precede the `}` on the line, but cannot follow it on the line.
    
*   An implicit `QUIT` is present just before the closing brace.
    
*   Indirection and `XECUTE` commands behave as if they are outside of a procedure.
    

## Indirection, XECUTE Commands, and JOB Commands within Procedures

Name indirection, argument indirection, and `XECUTE` commands that appear within a procedure are not executed within the scope of the procedure. Thus, `XECUTE` acts like an implied `DO` of a subroutine that is outside of the procedure.

Indirection and `XECUTE` only access public variables. As a result, if indirection or an `XECUTE` references a variable `x`, then it references the public variable `x` regardless of whether or not there is also a private `x` in the procedure. For example:

```objectscript
 SET x="set a=3" XECUTE x ; sets the public variable a to 3
 SET x="label1" DO @x ; accesses the public subroutine label1
```

Similarly, a reference to a label within indirection or an `XECUTE` is to a label outside of the procedure. Hence `GOTO @A` is not supported within a procedure, since a `GOTO` from within a procedure must be to a label within the procedure.

Other parts of the documentation contain more detail on indirection and the XECUTE command.

Similarly, when you issue a JOB command within a procedure, it starts a child process that is outside the method. This means that for code such as the following:

```objectscript
    KILL ^MyVar
    JOB MyLabel
    QUIT $$$OK
MyLabel
    SET ^MyVar=1
    QUIT
```

In order for the child process to be able to see the label, the method or the class cannot be contained in a procedure block.

## Error Traps within Procedures

If an error trap gets set from within a procedure, it needs to be directly to a private label in the procedure. (This is unlike in legacy code, where it can contain `+offset` or a routine name. This rule is consistent with the idea that executing an error trap essentially means unwinding the stack back to the error trap and then executing a `GOTO`.)

If an error occurs inside a procedure, $ZERROR gets set to the procedure `label+offset`, not to a private `label+offset`.

To set an error trap, the normal `$ZTRAP` is used, but the value must be a literal. For instance:

```objectscript
 SET $ZTRAP = "abc"
 // sets the error trap to the private label "abc" within this block
```

For more information on error traps, see Using Try-Catch.
