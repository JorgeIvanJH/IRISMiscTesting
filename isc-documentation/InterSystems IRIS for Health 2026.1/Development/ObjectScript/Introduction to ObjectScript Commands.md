# Introduction to ObjectScript Commands

This topic introduces some of the most commonly used ObjectScript commands; also see the ObjectScript Reference.

## Command to Assign Values

Use the `SET` command to assign a value to a variable. The basic syntax of `SET` is:

```objectscript
 SET MyVar=expression
```

where `MyVar` is a variable and expression is any ObjectScript expression that is suitable in the given context. See ObjectScript Variables.

## Commands to Invoke Code

This section describes the commands used for invoking code:

*   DO
    
*   JOB
    
*   XECUTE
    
*   QUIT and RETURN
    

Also see the page Invoking Code and Passing Arguments.

### DO

To invoke a routine, procedure, or method in ObjectScript, use the `DO` command. The basic syntax of `DO` is:

```objectscript
 DO ^CodeToInvoke
```

where `CodeToInvoke` can be an InterSystems IRIS system routine or a user-defined routine. The caret character ^ must appear immediately before the name of the routine.

You can run procedures within a routine by referring to the label of the line (also called a tag) where the procedure begins within the routine. The label appears immediately before the caret. For example,

```objectscript
 SET %X = 484
 DO INT^%SQROOT
 WRITE %Y
```

This code sets the value of the `%X` system variable to 484; it then uses DO to invoke the INT procedure of the InterSystems IRIS system routine `%SQROOT`, which calculates the square root of the value in `%X` and stores it in `%Y`. The code then displays the value of `%Y` using the `WRITE` command.

When invoking methods, `DO` takes as a single argument the entire expression that specifies the method. The form of the argument depends on whether the method is an instance or a class method. To invoke a class method, use the following construction:

```objectscript
 DO ##class(PackageName.ClassName).ClassMethodName()
```

where `ClassMethodName()` is the name of the class method that you wish to invoke, `ClassName` is the name of the class containing the method, and `PackageName` is the name of the package containing the class. The `##class()` construction is a required literal part of the code.

To invoke an instance method, you need only have a handle to the locally instantiated object:

```objectscript
 DO InstanceName.InstanceMethodName()
```

where `InstanceMethodName()` is the name of the instance method that you wish to invoke, and `InstanceName` is the name of the instance containing the method.

For further details, see DO.

### JOB

While `DO` runs code in the foreground, `JOB` runs it in the background. This occurs independently of the current process, usually without user interaction. A jobbed process inherits all system defaults, except those explicitly specified.

For further details, see JOB.

### XECUTE

The `XECUTE` command runs one or more ObjectScript commands; it does this by evaluating the expression that it receives as an argument (and its argument must evaluate to a string containing one or more ObjectScript commands). In effect, each `XECUTE` argument is like a one-line subroutine called by a `DO` command and terminated when the end of the argument is reached or a `QUIT` command is encountered. After InterSystems IRIS executes the argument, it returns control to the point immediately after the `XECUTE` argument.

For further details, see XECUTE.

### QUIT and RETURN

The `QUIT` and `RETURN` commands both terminate execution of a code block, including a method. Without an argument, they simply exit the code from which they were invoked. With an argument, they use the argument as a return value. `QUIT` exits the current context, exiting to the enclosing context. `RETURN` exits the current program to the place where the program was invoked.

The following table shows how to choose whether to use `QUIT RETURN`:

<table><tr><th>Location</th><th>QUIT</th><th>RETURN</th></tr><tr><td>Routine code (not block structured)</td><td>Exits routine, returns to the calling routine (if any).</td><td>Exits routine, returns to the calling routine (if any).</td></tr><tr><td>TRY or CATCH block</td><td>Exits TRY / CATCH block structure pair to next code in routine. If issued from a nested TRY or CATCH block, exits one level to the enclosing TRY or CATCH block.</td><td>Exits routine, returns to the calling routine (if any).</td></tr><tr><td>DO or XECUTE</td><td>Exits routine, returns to the calling routine (if any).</td><td>Exits routine, returns to the calling routine (if any).</td></tr><tr><td>IF</td><td>Exits routine, returns to the calling routine (if any). However, if nested in a FOR, WHILE, or DO WHILE loop, exits that block structure and continues with the next line after the code block.</td><td>Exits routine, returns to the calling routine (if any).</td></tr><tr><td>FOR, WHILE, DO WHILE</td><td>Exits the block structure and continues with the next line after the code block. If issued from a nested block, exits one level to the enclosing block.</td><td>Exits routine, returns to the calling routine (if any).</td></tr></table>

For further details, see QUIT and RETURN.

## Commands to Control Flow

In order to establish the logic of any code, there must be flow control; conditional executing or bypassing blocks of code, or repeatedly executing a block of code. To that end, ObjectScript supports the following commands:

*   Conditional Execution
    
*   FOR
    
*   WHILE and DO WHILE
    

### Conditional Execution

To conditionally execute a block of code, based on boolean (true/false) test, you can use the `IF` command. (You can perform conditional execution of individual ObjectScript commands by using a postconditional expression.)

`IF` takes an expression as an argument and evaluates that expression as true or false. If true, then the block of code that follows the expression is executed; if false, the block of code is not executed. Most commonly these are represented by 1 and 0, which are the recommended values. However, InterSystems IRIS performs conditional execution on any value, evaluating it as False if it evaluates to 0 (zero), and True if it evaluates to a nonzero value. For further details, see Operators.

You can specify multiple `IF` boolean test expressions as a comma-separated list. These tests are evaluated in left-to-right order as a series of logical AND tests. Therefore, an `IF` evaluates as true when all of its test expressions evaluate as true. An `IF` evaluates as false when the one of its test expressions evaluates as false; the remaining test expressions are not evaluated.

The code usually appears in a code block containing multiple commands. Code blocks are simply one or more lines of code contained in curly braces; there can be line breaks before and within the code blocks. Consider the following:

#### IF, ELSEIF, and ELSE

The `IF` construct allows you to evaluate multiple conditions, and to specify what code is run based on the conditions. A construct, as opposed to a simple command, consists of a combination of one or more command keywords, their conditional expressions and code blocks. The `IF` construct consists of:

*   One `IF` clause with one or more conditional expressions.
    
*   Any number of `ELSEIF` clauses, each with one or more conditional expressions. The `ELSEIF` clause optional; there can be more than one `ELSEIF` clause.
    
*   At most one `ELSE` clause, with no conditional expression. The `ELSE` clause is optional.
    

The following is an example of the `IF` construct:

```objectscript
 READ "Enter the number of equal-length sides in the polygon: ",x
   IF x=1 {WRITE !,"It's so far away that it looks like a point"}
   ELSEIF x=2 {WRITE !,"I think that's a line, not a polygon"}
   ELSEIF x=3 {WRITE !,"It's an equalateral triangle"}
   ELSEIF x=4 {WRITE !,"It's a square"}
   ELSE {WRITE !,"It's a polygon with ",x," number of sides" }
 WRITE !,"Finished the IF test"
```

For further details, refer to the reference for IF.

### FOR

You use the `FOR` construct to repeat sections of code. You can create a `FOR` loop based on numeric or string values.

Typically, `FOR` executes a code block zero or more times based on the value of a numeric control variable that is incremented or decremented at the beginning of each loop through the code. When the control variable reaches its end value, control exits the `FOR` loop; if there is no end value, the loop executes until it encounters a `QUIT` command. When control exits the loop, the control variable maintains its value from the last loop executed.

The form of a numeric `FOR` loop is:

```objectscript
 FOR ControlVariable = StartValue:IncrementAmount:EndValue {
         // code block content
 }
```

All values can be positive or negative; spaces are permitted but not required around the equals sign and the colons. The code block following the `FOR` will repeat for each value assigned to the variable.

For example, the following `FOR` loop will execute five times:

```objectscript
 WRITE "The first five multiples of 3 are:",!
 FOR multiple = 3:3:15 {
    WRITE multiple,!
 }
```

You can also use a variable to determine the end value. In the example below, a variable specifies how many iterations of the loop occur:

```objectscript
 SET howmany = 4
 WRITE "The first ",howmany," multiples of 3 are "
 FOR multiple = 1:1:howmany {
     WRITE (multiple*3),", "
     IF multiple = (howmany - 1) {
         WRITE "and "
     }
     IF multiple = howmany {
         WRITE "and that's it!"
     }
 }
 QUIT
```

Because this example uses `multiple`, the control variable, to determine the multiples of 3, it displays the expression `multiple*3`. It also uses the `IF` command to insert and before the last multiple.

> **Note:**
> 
> The `IF` command in this example provides an excellent example of the implications of order of precedence in ObjectScript (order of precedence is always left to right with no hierarchy among operators). If the `IF` expression were simply multiple = howmany - 1, without any parentheses or parenthesized as a whole, then the first part of the expression, multiple = howmany, would be evaluated to its value of False (0); the expression as a whole would then be equal to 0 - 1, which is -1, which means that the expression will evaluate as true (and insert and for every case except the final iteration through the loop).

The argument of `FOR` can also be a variable set to a list of values; in this case, the code block will repeat for each item in the list assigned to the variable.

```objectscript
 FOR item = "A", "B", "C", "D" {
    WRITE !, "Now examining item: "_item
 }
```

You can specify the numeric form of `FOR` without an ending value by placing a `QUIT` within the code block that triggers under particular circumstances and thereby terminates the `FOR`. This approach provides a counter of how many iterations have occurred and allows you to control the `FOR` using a condition that is not based on the counter’s value. For example, the following loop uses its counter to inform the user how many guesses were made:

```objectscript
    FOR i = 1:1 {
    READ !, "Capital of MA? ", a
    IF a = "Boston" {
        WRITE "...did it in ", i, " tries"
        QUIT
        }
    }
```

If you have no need for a counter, you can use the argumentless `FOR`:

```objectscript
    FOR  {
        READ !, "Know what? ", wh
        QUIT:(wh = "No!")
        WRITE "   That's what!"
    }
```

For further details, see FOR.

### WHILE and DO WHILE

Two related flow control commands are `WHILE` and `DO WHILE` commands, each of which loops over a code block and terminates based on a condition. The two commands differ in when they evaluate the condition: `WHILE` evaluates the condition before the entire code block and `DO WHILE` evaluates the condition after the block. As with `FOR`, a `QUIT` within the code block terminates the loop.

The syntax for the two commands is:

```
 DO {code} WHILE condition
 WHILE condition {code}
```

The following example displays values in the Fibonacci sequence up to a user-specified value twice — first using `DO WHILE` and then using `WHILE`:

```objectscript
fibonacci() PUBLIC { // generate Fibonacci sequences
    READ !, "Generate Fibonacci sequence up to where? ", upto
    SET t1 = 1, t2 = 1, fib = 1
    WRITE !
    DO {
        WRITE fib,"  "  set fib = t1 + t2, t1 = t2, t2 = fib
    }
    WHILE ( fib '> upto )

    SET t1 = 1, t2 = 1, fib = 1
    WRITE !
    WHILE ( fib '> upto ) {
        WRITE fib,"  "
        SET fib = t1 + t2, t1 = t2, t2 = fib
    }
 }
```

The distinction between `WHILE`, `DO WHILE`, and `FOR` is that `WHILE` necessarily tests the control expression’s value before executing the loop, `DO WHILE` necessarily tests the value after executing the loop, and `FOR` can test it anywhere within the loop. This means that if you have two parts to a code block, where execution of the second depends on evaluating the expression, the `FOR` construct is best suited; otherwise, the choice depends on whether expression evaluation should precede or follow the code block.

For further details, see WHILE and DO WHILE.

## Commands to Processes Error

Use the `TRY` / `CATCH` block structure for error processing: It is recommended that you use the `TRY` and `CATCH` commands to create block structures for error processing.

See The TRY-CATCH Mechanism, and see TRY, THROW, and CATCH.

## Commands to Process Transactions

Use the `TSTART`, `TCOMMIT`, and `TROLLBACK` commands for transaction processing. See Transaction Processing, and see TSTART, TCOMMIT, and TROLLBACK.

## Command for Locking and Concurrency Control

Use the `LOCK` command for locking and unlocking resources. See Locking and Concurrency Control and see LOCK.

Locking is also relevant in transaction processing; see Transaction Processing.

## Write Commands

ObjectScript supports four commands to display (write) literals and variable values to the current output device:

*   WRITE command
    
*   ZWRITE command
    
*   ZZDUMP command
    
*   ZZWRITE command
    

### Argumentless Display Commands

*   Argumentless `WRITE` displays the name and value of each defined local variable, one variable per line. It lists both public and private variables. It does not list global variables, process-private globals, or special variables. It lists variables in collation sequence order. It lists subscripted variables in subscript tree order.
    
    It displays all data values as quoted strings delimited by double quote characters, except for canonical numbers and object references. It displays a variable assigned an object reference (OREF) value as `variable=<OBJECT REFERENCE>[oref]`. It displays a %List format value or a bitstring value in their encoded form as a quoted string. Because these encoded forms may contain non-printing characters, a %List or bitstring may appear to be an empty string.
    
    `WRITE` does not display certain non-printing characters; no placeholder or space is displayed to represent these non-printing characters. `WRITE` executes control characters (such as line feed or backspace).
    
*   Argumentless `ZWRITE` is functionally identical to argumentless `WRITE`.
    
*   Argumentless `ZZDUMP` is an invalid command that generates a <SYNTAX> error.
    
*   Argumentless `ZZWRITE` is a no-op that returns the empty string.
    

### Display Commands with Arguments

The following tables list the features of the argumented forms of the four commands. All four commands can take a single argument or a comma-separated list of arguments. All four commands can take as an argument a local, global, or process-private variable, a literal, an expression, or a special variable:

The following tables also list the %Library.Utility.FormatString() method default return values. The `FormatString()` method is most similar to `ZZWRITE`, except that it does not list `%val=` as part of the return value, and it returns only the object reference (OREF) identifier. `FormatString()` allows you to set a variable to a return value in `ZWRITE` / `ZZWRITE` format.

#### Display Formatting

<table><tr><th>&nbsp;</th><th>WRITE</th><th>ZWRITE</th><th>ZZDUMP</th><th>ZZWRITE</th><th>FormatString()</th></tr><tr><td>Each value on a separate line?</td><td>NO</td><td>YES</td><td>YES (16 characters per line)</td><td>YES</td><td>One input value only</td></tr><tr><td>Variable names identified?</td><td>NO</td><td>YES</td><td>NO</td><td>Represented by <code>%val=</code></td><td>NO</td></tr><tr><td>Undefined variable results in &lt;UNDEFINED&gt; error?</td><td>YES</td><td>NO (skipped, variable name not returned)</td><td>YES</td><td>YES</td><td>YES</td></tr></table>

All four commands evaluate expressions and return numbers in canonical form.

#### How Values are Displayed

<table><tr><th>&nbsp;</th><th>WRITE</th><th>ZWRITE</th><th>ZZDUMP</th><th>ZZWRITE</th><th>FormatString()</th></tr><tr><td>Hexadecimal representation?</td><td>NO</td><td>NO</td><td>YES</td><td>NO</td><td>NO</td></tr><tr><td>Strings quoted to distinguish from numerics?</td><td>NO</td><td>YES</td><td>NO</td><td>YES (a string literal is returned as <code>%val="value"</code>)</td><td>YES</td></tr><tr><td>Subscript nodes displayed?</td><td>NO</td><td>YES</td><td>NO</td><td>NO</td><td>NO</td></tr><tr><td>Global variables in another namespace (extended global reference) displayed?</td><td>YES</td><td>YES (extended global reference syntax shown)</td><td>YES</td><td>YES</td><td>YES</td></tr><tr><td>Non-printing characters displayed?</td><td>NO, not displayed; control characters executed</td><td>YES, displayed as <code>$c(n)</code></td><td>YES, displayed as hexadecimal</td><td>YES, displayed as <code>$c(n)</code></td><td>YES, displayed as <code>$c(n)</code></td></tr><tr><td>List value format</td><td>encoded string</td><td><code>$lb(val)</code> format</td><td>encoded string</td><td><code>$lb(val)</code> format</td><td><code>$lb(val)</code> format</td></tr><tr><td>%Status format</td><td>string containing encoded Lists</td><td>string containing <code>$lb(val)</code> format Lists, with appended /*... */ comment specifying error and message.</td><td>string containing encoded Lists</td><td>string containing <code>$lb(val)</code> format Lists, with appended /*... */ comment specifying error and message.</td><td>string containing <code>$lb(val)</code> format Lists, with (by default) appended /*... */ comment specifying error and message.</td></tr><tr><td>Bitstring format</td><td>encoded string</td><td>$zwc format with appended /* $bit() */ comment listing 1 bits. For example: <code>%val=$zwc(407,2,1,2,3,5)/*$bit(2..4,6)*/</code></td><td>encoded string</td><td>$zwc format with appended /* $bit() */ comment listing 1 bits. For example: <code>%val=$zwc(407,2,1,2,3,5)/*$bit(2..4,6)*/</code></td><td>$zwc format with (by default) appended /* $bit() */ comment listing 1 bits. For example: <code>%val=$zwc(407,2,1,2,3,5)/*$bit(2..4,6)*/</code></td></tr><tr><td>Object Reference (OREF) format</td><td>OREF only</td><td>OREF in <code>&lt;OBJECT REFERENCE&gt;[oref]</code> format. General information, attribute values, etc. details listed. All subnodes listed</td><td>OREF only</td><td>OREF in <code>&lt;OBJECT REFERENCE&gt;[oref]</code> format. General information, attribute values, etc. details listed.</td><td>OREF only, as quoted string</td></tr></table>

JSON dynamic arrays and JSON dynamic objects are returned as OREF values by all of these commands. To return the JSON contents, you must use `%ToJSON()`, as shown in the following example:

```
  SET jobj={"name":"Fred","city":"Bedrock"}
  WRITE "JSON object reference:",!
  ZWRITE jobj
  WRITE !!,"JSON object value:",!
  ZWRITE jobj.%ToJSON()
```

For further details, see WRITE, ZWRITE, ZZDUMP, and ZZWRITE.

## READ Command

The `READ` command allows you to accept and store input entered by the end user via the current input device. The `READ` command can have any of the following arguments:

```objectscript
  READ format, string, variable
```

Where `format` controls where the user input area will appear on the screen, `string` will appear on the screen before the input prompt, and `variable` will store the input data.

The following format codes are used to control the user input area:

<table><tr><th>Format Code</th><th>Effect</th></tr><tr><td>!</td><td>Starts a new line.</td></tr><tr><td>#</td><td>Starts a new page. On a terminal it clears the current screen and starts at the top of a new screen.</td></tr><tr><td>?n</td><td>Positions at the nth column position where <code>n</code> is a positive integer.</td></tr></table>

For further details, see READ.

## Files and Devices

To work with files and directories, InterSystems IRIS provides the %File API.

In addition, InterSystems IRIS provides low-level commands you can use to work with devices. This process as a whole is described in the I/O Device Guide. For further details, see OPEN, USE, and CLOSE.

## See Also

*   ObjectScript Command Reference
