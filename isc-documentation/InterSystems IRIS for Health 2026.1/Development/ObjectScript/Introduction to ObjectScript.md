# Introduction to ObjectScript

ObjectScript is a built-in, fully general programming language in InterSystems IRIS data platform. ObjectScript source code is compiled into object code that executes within the InterSystems IRIS Virtual Machine. This object code is highly optimized for operations typically found within business applications, including string manipulations and database access. ObjectScript programs are completely portable across all platforms supported by InterSystems IRIS.

You can use ObjectScript in any of the following contexts:

*   As the implementation language for methods of InterSystems IRIS classes. (Note that class definitions are not formally part of ObjectScript. Rather, you can use ObjectScript within specific parts of class definitions).
    
*   As the implementation language for stored procedures and triggers within InterSystems SQL.
    
*   To create routines.
    
*   Interactively within the ObjectScript shell.
    

> **Important:**
> 
> Operator precedence in ObjectScript is strictly left-to-right; within an expression, operations are performed in the order in which they appear. Use explicit parentheses within an expression to force certain operations to be carried out ahead of others.

## Features

Some of the key features of ObjectScript include:

*   Native support for objects including methods, properties, and polymorphism
    
*   Support for concurrency control
    
*   A set of commands for dealing with I/O devices
    
*   Support for multidimensional, sparse arrays: both local and global (persistent)
    
*   Support for efficient, Embedded SQL
    
*   Support for indirection as well as runtime evaluation and execution of commands
    

## Sample Class with ObjectScript

Class definitions are not part of ObjectScript, but can include ObjectScript in multiple places, and classes are compiled into routines and ultimately into the same runtime code. Within a class, the most common use for ObjectScript is as the implementation of a method.

The following shows an sample class that gives us an opportunity to see some common ObjectScript commands, operators, and functions, and to see how code is organized within a method.

```objectscript
Class User.DemoClass
{

/// Generate a random number.
/// This method can be called from outside the class.
ClassMethod Random() [ Language = objectscript ]
{
    set rand=$RANDOM(10)+1        ; rand is an integer in the range 1-10
    write "Your random number: "_rand
    set name=..GetNumberName(rand)
    write !, "Name of this number: "_name
}

/// Input a number.
/// This method can be called from outside the class.
ClassMethod Input() [ Language = objectscript ]
{
    read "Enter a number from 1 to 10: ", input
    set name=..GetNumberName(input)
    write !, "Name of this number: "_name
}

/// Given an number, return the name.
/// This method can be called only from within this class.
ClassMethod GetNumberName(number As %Integer) As %Integer [ Language = objectscript, Private ]
{
    set name=$CASE(number,1:"one",2:"two",3:"three",
        4:"four",5:"five",6:"six",7:"seven",8:"eight",
        9:"nine",10:"ten",:"other")
    quit name
}

/// Write some interesting values.
/// This method can be called from outside the class.
ClassMethod Interesting() [ Language = objectscript ]
{
    write "Today's date: "_$ZDATE($HOROLOG,3)
    write !,"Your installed version: "_$ZVERSION
    write !,"Your username: "_$USERNAME
    write !,"Your security roles: "_$ROLES
}

}
```

Note the following highlights:

*   The `Random()` and `Input()` methods invoke the `GetNumberName()` method, which is private to this class and cannot be called from outside the class.
    
*   `WRITE`, `QUIT`, `SET`, and `READ` are ObjectScript commands. The language includes other commands to remove variables, commands to control program flow, commands to control I/O devices, commands to manage transactions (possibly nested), and so on.
    
    The names of commands are not case-sensitive, although they are shown in running text in all upper case by convention.
    
*   The sample includes two ObjectScript operators. The plus sign (+) performs addition, and the underscore (_) performs string concatenation.
    
    ObjectScript provides the usual operators and some special operators not seen in other languages.
    
*   `$RANDOM`, `$CASE`, and `$ZDATE` are ObjectScript functions.
    
    The language provides functions for string operations, conversions of many kinds, formatting operations, mathematical operations, and others.
    
*   `$HOROLOG`, `$ZVERSION`, `$USERNAME`, and `$ROLES` are ObjectScript system variables (called special variables in InterSystems IRIS). Most special variables contain values for aspects of the InterSystems IRIS operating environment, the current processing state, and so on.
    
*   ObjectScript supports comment lines, block comments, and comments at the end of statements.
    

We can execute the methods of this class in the ObjectScript shell, as a demonstration. In these examples, `TESTNAMESPACE>` is the prompt shown in the shell. The text after the prompt on the same line is the entered command. The lines after that show the values that the system writes to the shell in response.

```objectscript
TESTNAMESPACE>do ##class(User.DemoClass).Input()
Enter a number from 1 to 10: 7
Name of this number: seven
TESTNAMESPACE>do ##class(User.DemoClass).Interesting()
Today's date: 2021-07-15
Your installed version: IRIS for Windows (x86-64) 2019.3 (Build 310U) Mon Oct 21 2019 13:48:58 EDT
Your username: SuperUser
Your security roles: %All
TESTNAMESPACE>
```

## Sample Routine

The following shows an sample ObjectScript routine named `demoroutine`. It contains procedures that do the exact same thing as the methods shown in the sample class in the previous section.

```objectscript
 ; this is demoroutine
 write "Use one of the following entry points:"
 write !,"random"
 write !,"input"
 write !,"interesting"
 quit

 //this procedure can be called from outside the routine
random() public {
    set rand=$RANDOM(10)+1        ; rand is an integer in the range 1-10
    write "Your random number: "_rand
    set name=$$getnumbername(rand)
    write !, "Name of this number: "_name
 }

 //this procedure can be called from outside the routine
input() public {
    read "Enter a number from 1 to 10: ", input
    set name=$$getnumbername(input)
    write !, "Name of this number: "_name
 }

 //this procedure can be called only from within this routine
getnumbername(number) {
    set name=$CASE(number,1:"one",2:"two",3:"three",
        4:"four",5:"five",6:"six",7:"seven",8:"eight",
        9:"nine",10:"ten",:"other")
    quit name
}

 /* write some interesting values
 this procedure can be called from outside the routine
 */
interesting() public {
    write "Today's date: "_$ZDATE($HOROLOG,3)
    write !,"Your installed version: "_$ZVERSION
    write !,"Your username: "_$USERNAME
    write !,"Your security roles: "_$ROLES
    }
```

Note the following highlights:

*   The only identifiers that actually start with a caret (`^`) are the names of globals; these are discussed later in this page. However, in running text and in code comments, it is customary to refer to a routine as if its name started with a caret, because you use the caret when you invoke the routine (as shown later in this page). For example, the routine `demoroutine` is usually called `^demoroutine`.
    
*   The routine name does not have to be included within the routine. However, many programmers include the routine name as a comment at the start of the routine or as the first label in the routine.
    
*   The routine has multiple labels: `random`, `input`, `getnumbername`, and `interesting`.
    
    Labels are used to indicate the starting point for procedures (as in this example) and legacy forms of subroutines. You can also use them as a destination for certain commands.
    
    Labels are common in routines, but you can also use them within methods.
    
    Labels are also called entry points or tags.
    
*   The `random` and `input` subroutines invoke the `getnumbername` subroutine, which is private to the routine.
    

We can execute parts of this routine in the ObjectScript shell, as a demonstration. First, the following shows a session in which we run the routine itself.

```objectscript
TESTNAMESPACE>do ^demoroutine
Use one of the following entry points:
random
input
TESTNAMESPACE>
```

When we run the routine, we just get help information, as you can see. It is not required to write your routines in this way, but it is common. Note that the routine includes a `QUIT` before the first label, to ensure that when a user invokes the routine, processing is halted before that label. This practice is also not required, but is also common.

Next, the following shows how a couple of the subroutines behave:

```objectscript
TESTNAMESPACE>do input^demoroutine
Enter a number from 1 to 10: 7
Name of this number: seven
TESTNAMESPACE>do interesting^demoroutine
Today's date: 2018-02-06
Your installed version: IRIS for Windows (x86-64) 2018.1 (Build 513U) Fri Jan 26 2018 18:35:11 EST
Your username: _SYSTEM
Your security roles: %All
TESTNAMESPACE>
```

A method can contain the same statements, labels, and comments as routines do. That is, all the information here about the contents of a routine also applies to the contents of a method.

## Variables

In ObjectScript, there are two primary kinds of variables, as categorized by how they hold data. The name of the variable establishes which kind of variable it is.

*   Local variables, which hold data in memory.
    
    Local variables can have public or private scope.
    
    Example local variable names are `MyVar` and `%MyVar`.
    
*   Global variables, which hold data in a database. These are also called globals. All interactions with a global affect the database immediately. For example, when you set the value of a global, that change immediately affects what is stored; there is no separate step for storing values. Similarly, when you remove a global, the data is immediately removed from the database.
    
    Example global variable names are `^MyVar` and `^%MyVar`.
    

See ObjectScript Variables and Scope.

## Multidimensional Arrays

In ObjectScript, any variable can be an InterSystems IRIS multidimensional array (also called an array). An object property can also be a multidimensional array, if it is declared as such. A multidimensional array is generally intended to hold a set of values that are related in some way. ObjectScript provides commands and functions that provide convenient and fast access to the values.

You may or may not work directly with multidimensional arrays, depending on the APIs that you use and your own preferences. InterSystems IRIS provides a class-based alternative to use when you want a container for sets of related values; see Collection Classes.

### Basics

A multidimensional array consists of any number of nodes, defined by subscripts. The following example sets several nodes of an array and then prints the contents of the array:

```objectscript
 set myarray(1)="value A"
 set myarray(2)="value B"
 set myarray(3)="value C"
 zwrite myarray
```

This example shows a typical array. Notes:

*   This array has one subscript. In this case, the subscripts are the integers 1, 2, and 3.
    
*   There is no need to declare the structure of the array ahead of time.
    
*   `myarray` is the name of the array itself.
    
*   ObjectScript provides commands and functions that can act on an entire array or on specific nodes. For example:
    
    ```objectscript
     kill myarray
    ```
    
    You can also kill a specific node and its child nodes.
    
*   The following variation sets several subscripts of a global array named `^myglobal`; that is, these values are written to disk:
    
    ```objectscript
     set ^myglobal(1)="value A"
     set ^myglobal(2)="value B"
     set ^myglobal(3)="value C"
    ```
    
*   There is a limit to the possible length of a global reference. This limit affects the length of the global name and the length and number of any subscripts. If you exceed the limit, you get a <SUBSCRIPT> error. See Maximum Length of a Global Reference.
    
*   The length of a value of a node must be less than the string length limit.
    

A multidimensional array has one reserved memory location for each defined node and no more than that. For a global, all the disk space that it uses is dynamically allocated.

### Structure Variations

The preceding examples show a common form of array. Note the following possible variations:

*   You can have any number of subscripts. For example:
    
    ```objectscript
     Set myarray(1,1,1)="grandchild of value A"
    ```
    
*   A subscript can be a string. The following is valid:
    
    ```objectscript
     set myarray("notes to self","2 Dec 2010")="hello world"
    ```
    

### Use Notes

For those who are learning ObjectScript, a common mistake is to confuse globals and arrays. It is important to remember that any variable is either local or global, and may or may not have subscripts. The following table shows the possibilities:

<table><tr><th>Kind of Variable</th><th>Example and Notes</th></tr><tr><td>Local variable without subscripts</td><td><code>Set MyVar=10</code><p>Variables like this are quite common. The majority of the variables you see might be like this.</p></td></tr><tr><td>Local variable with subscripts</td><td><p><code>Set MyVar(1)="alpha"</code></p><p><code>Set MyVar(2)="beta"</code></p><p><code>Set MyVar(3)="gamma"</code></p><p>A local array like this is useful when you want to pass a set of related values.</p></td></tr><tr><td>Global variable without subscripts</td><td><code>Set ^MyVar="saved note"</code><p>In practice, globals usually have subscripts.</p></td></tr><tr><td>Global variable with subscripts</td><td><code>Set ^MyVar($USERNAME,"Preference 1")=42</code></td></tr></table>

## Operators

This section provides an overview of the operators in ObjectScript; some are familiar, and others are not.

Operator precedence in ObjectScript is strictly left-to-right; within an expression, operations are performed in the order in which they appear. You can use explicit parentheses within an expression to force certain operations to be carried out ahead of others.

Typically you use parentheses even where you do not strictly need them. It is useful to other programmers (and to yourself at a later date) to do this because it makes the intent of your code clearer.

### Familiar Operators

ObjectScript provides the following operators for common activities:

*   Mathematical operators: addition (`+`), subtraction (`-`), division (`/`), multiplication (`*`), integer division (`\`), modulus (`#`), and exponentiation (`**`)
    
*   Unary operators: positive (`+`) and negative (`-`)
    
*   String concatenation operator (`_`)
    
*   Logical comparison operators: equals (`=`), greater than (`>`), greater than or equal to (`>=`), less than (`<`), less than or equal to (`<=`)
    
*   Logical complement operator (`'`)
    
    You can use this immediately before any logical value as well as immediately before a logical comparison operator.
    
*   Operators to combine logical values: AND (`&&`), OR (`||`)
    
    Note that ObjectScript also supports an older, less efficient form of each of these: `&` is a form of the `&&` operator, and `!` is a form of the `||` operator. You might see these older forms in existing code.
    

### Unfamiliar Operators

ObjectScript also includes operators that have no equivalent in some languages. The most important ones are as follows:

*   The pattern match operator (`?`) tests whether the characters in its left operand use the pattern in its right operand. You can specify the number of times the pattern is to occur, specify alternative patterns, specify pattern nesting, and so on.
    
    For example, the following writes the value 1 (true) if a string (`testthis`) is formatted as a U.S. Social Security Number and otherwise writes 0.
    
    ```objectscript
     Set testthis="333-99-0000"
     Write testthis ?3N1"-"2N1"-"4N
    ```
    
    This is a valuable tool for ensuring the validity of input data, and you can use it within the definition of class properties.
    
*   The binary contains operator (`[`) returns 1 (true) or 0 (false) depending on whether the sequence of characters in the right operand is a substring of the left operand. For example:
    
    ```objectscript
     Set L="Steam Locomotive",S="Steam"
     Write L[S
    ```
    
*   The binary follows operator (`]`) tests whether the characters in the left operand come after the characters in the right operand in ASCII collating sequence.
    
*   The binary sorts after operator (`]]`) tests whether the left operand sorts after the right operand in numeric subscript collation sequence.
    
*   The indirection operator (`@`) allows you to perform dynamic runtime substitution of part or all of a command argument, a variable name, a subscript list, or a pattern. InterSystems IRIS performs the substitution before execution of the associated command.
    

## Commands

This section provides an overview of the commands that you are most likely to use and to see in ObjectScript. These include commands that are similar to those in other languages, as well as others that have no equivalent in other languages.

The names of commands are not case-sensitive, although they are shown in running text in all upper case by convention.

### Familiar Commands

ObjectScript provides commands to perform familiar tasks such as the following:

*   To define variables, use `SET` as shown previously.
    
*   To remove variables, use `KILL` as shown previously.
    
*   To control the flow of logic, use the following commands:
    
    *   `IF`, `ELSEIF`, and `ELSE`, which work together
        
    *   `FOR`
        
    *   `WHILE`, which can be used on its own
        
    *   `DO` and `WHILE`, which can be used together
        
    *   `QUIT`, which can also return a value
        
    
    There are other commands for flow control, but they are used less often.
    
*   To trap errors, use `TRY` and `CATCH`, which work together. See Using TRY-CATCH.
    
*   To write a value, use `WRITE`. This writes values to the current device (for example, the Terminal or a file).
    
    Used without an argument, this command writes the values of all local variables. This is particularly convenient in the Terminal.
    
    This command can use a small set of format control code characters that position the output. In existing code, you are likely to see the exclamation point, which starts a new line. For example:
    
    ```objectscript
     write "hello world",!,"another line"
    ```
    
*   To read a value from the current device (for example, the Terminal), use `READ`.
    
*   To work with devices other than the principal device, use the following commands:
    
    *   `OPEN` makes a device available for use.
        
    *   `USE` specifies an open device as the current device for use by `WRITE` and `READ`.
        
    *   `CLOSE` makes a device no longer available for use.
        
*   To control concurrency, use `LOCK`. Note that the InterSystems IRIS lock management system is different from analogous systems in other languages. It is important to review how it works; see Locking and Concurrency Control.
    
*   To manage transactions, use `TSTART`, `TCOMMIT`, `TROLLBACK`, and related commands. See Transaction Processing.
    
*   For debugging, use `ZBREAK` and related commands.
    
*   To suspend execution, use `HANG`.
    

### Commands for Use with Multidimensional Arrays

In ObjectScript, you can work with multidimensional arrays in the following ways:

*   To define nodes, use the `SET` command.
    
*   To remove individual nodes or all nodes, use the `KILL` command.
    
    For example, the following removes an entire multidimensional array:
    
    ```objectscript
     kill myarray
    ```
    
    In contrast, the following removes the node `myarray("2 Dec 2010")` and all its children:
    
    ```objectscript
     kill myarray("2 Dec 2010")
    ```
    
*   To delete a global or a global node but none of its descendent subnodes, use `ZKILL`.
    
*   To iterate through all nodes of a multidimensional array and write them all, use `ZWRITE`. This is particularly convenient in the Terminal. The following sample Terminal session shows what the output looks like:
    
    ```objectscript
    TESTNAMESPACE>ZWRITE ^myarray
    ^myarray(1)="value A"
    ^myarray(2)="value B"
    ^myarray(3)="value C"
    ```
    
    This example uses a global variable rather than a local one, but remember that both can be multidimensional arrays.
    
*   To copy a set of nodes from one multidimensional array into another, preserving existing nodes in the target if possible, use `MERGE`. For example, the following command copies an entire in-memory array (`sourcearray`) into a new global (`^mytestglobal`):
    
    ```objectscript
     MERGE ^mytestglobal=sourcearray
    ```
    
    This can be a useful way of examining the contents of an array that you are using, while debugging your code.
    

## System Functions

This section introduces some of the most commonly used ObjectScript functions, grouped by purpose. The names of these functions are not case-sensitive.

*   Choosing values: `$SELECT` and `$CASE`
    
*   Testing for existence of a variable (or of a node of a variable): `$DATA` and `$GET`
    
*   Creating and working with native-list format lists: `$LISTBUILD`, `$LISTGET`, `$LIST`, and others. See Lists in ObjectScript, which also introduces alternatives.
    
*   Working with multidimensional arrays: `$ORDER`, `$QUERY`, `$DATA`, and `$GET`. See Multidimensional Arrays, which also introduces alternatives.
    
*   Creating characters that cannot be typed, for inclusion in strings: `$CHAR`. Given an integer, `$CHAR` returns the corresponding ASCII or Unicode character. Common uses:
    
    *   `$CHAR(9)` is a tab.
        
    *   `$CHAR(10)` is a line feed.
        
    *   `$CHAR(13)` is a carriage return.
        
    *   `$CHAR(13,10)` is a carriage return and line feed pair.
        
    
    The function `$ASCII` returns the ASCII value of the given character. See Strings in ObjectScript.
    

For a compact, full list, see ObjectScript Function Reference.

The InterSystems IRIS class library also provides a large set of APIs. See the InterSystems Programming Tools Index.

## Special Variables

This section introduces some InterSystems IRIS special variables. The names of these variables are not case-sensitive.

Some special variables provide information about the environment in which the code is running. These include the following:

*   `$HOROLOG`, which contains the date and time for the current process, as given by the operating system. See Date and Time Values.
    
*   `$USERNAME` and `$ROLES`, which contain information about the username currently in use, as well as the roles to which that user belongs.
    
    ```objectscript
     write "You are logged in as: ", $USERNAME, !, "And you belong to these roles: ",$ROLES
    ```
    
*   `$ZVERSION`, which contains a string that identifies the currently running version of InterSystems IRIS.
    

Others include `$JOB`, `$ZTIMEZONE`, `$IO`, and `$ZDEVICE`.

Other variables provide information about the processing state of the code. These include `$STACK`, `$TLEVEL`, `$NAMESPACE`, and `$ZERROR`.

### $SYSTEM Special Variable

The special variable `$SYSTEM` provides easy access to a large set of utility methods.

The special variable `$SYSTEM` is an alias for the `%SYSTEM` package, which contains classes that provide class methods that address a wide variety of needs. The customary way to refer to methods in `%SYSTEM` is to build a reference that uses the `$SYSTEM` variable. For example, the following command executes the `SetFlags()` method in the %SYSTEM.OBJ class:

```objectscript
 DO $SYSTEM.OBJ.SetFlags("ck")
```

Because names of special variables are not case-sensitive (unlike names of classes and their members), the following commands are all equivalent:

```objectscript
 DO ##class(%SYSTEM.OBJ).SetFlags("ck")
 DO $System.OBJ.SetFlags("ck")
 DO $SYSTEM.OBJ.SetFlags("ck")
 DO $system.OBJ.SetFlags("ck")
```

The classes all provide the `Help()` method, which can print a list of available methods in the class. For example:

```objectscript
TESTNAMESPACE>do $system.OBJ.Help()
'Do $system.OBJ.Help(method)' will display a full description of an individual method.

Methods of the class: %SYSTEM.OBJ

CloseObjects()
     Deprecated function, to close objects let them go out of scope.

Compile(classes,qspec,&errorlog,recurse)
     Compile a class.

CompileAll(qspec,&errorlog)
     Compile all classes within this namespace
....
```

You can also use the name of a method as an argument to `Help()`. For example:

```objectscript
TESTNAMESPACE>d $system.OBJ.Help("Compile")
Description of the method:class Compile:%SYSTEM.OBJ

Compile(classes:%String="",qspec:%String="",&errorlog:%String,recurse:%Boolean=0)
Compile a class.
<p>Compiles the class <var>classes</var>, which can be a single class, a comma separated list,
a subscripted array of class names, or include wild cards. If <var>recurse</var> is true then
do not output the intial 'compiling' message or the compile report as this is being called inside
another compile loop.<br>
<var>qspec</var> is a list of flags or qualifiers which can be displayed with
'Do $system.OBJ.ShowQualifiers()'
and 'Do $system.OBJ.ShowFlags()
```

## Potential Pitfalls

The following items can confuse programmers who are new to ObjectScript, particularly if those who are responsible for maintaining code written by other programmers:

*   Within a routine or a method, every line must be indented by at least one space or one tab unless that line contains a label. That is, if there is text of any kind in the first character position, the compiler and your IDE treat it as a label.
    
    There is one exception: A curly brace is accepted in the first character position.
    
*   There must be exactly one space (not a tab) between a command and its first argument. Otherwise, your IDE indicates that you have a syntax error.
    
    Similarly, the ObjectScript shell displays a syntax error as follows:
    
    ```objectscript
    TESTNAMESPACE>write  5
    
    WRITE  5
           ^
    <SYNTAX>
    TESTNAMESPACE>
    ```
    
*   Operator precedence in ObjectScript is strictly left-to-right; within an expression, operations are performed in the order in which they appear. You can use explicit parentheses within an expression to force certain operations to be carried ahead of others.
    
    Typically you use parentheses even where you do not strictly need them. It is useful to other programmers (and to yourself at a later date) to do this because it makes the intent of your code clearer.
    
*   For reasons of history, ObjectScript does not consider an empty string (`""`) to equal the ASCII NULL value. To represent the ASCII NULL value, use `$CHAR(0)`. (`$CHAR` is a system function that returns an ASCII character, given its decimal-based code.) For example:
    
    ```objectscript
     write "" = $char(0)
    ```
    
    Similarly, when ObjectScript values are projected to SQL or XML, the values `""` and `$CHAR(0)` are treated differently. For information on the SQL projections of these values, see Null and the Empty String. For information on the XML projections of these values, see Handling Empty Strings and Null Values.
    
*   Some parts of ObjectScript are case-sensitive while others are not. The case-insensitive items include names of commands, functions, special variables, namespaces, and users.
    
    The case-sensitive items include names of most of the elements that you define: routines, variables, classes, properties, and methods. For more details, see Syntax Rules.
    
*   Most command names can be represented by an abbreviated form. Therefore, `WRITE`, `Write`, `write`, `W`, and `w` are all valid forms of the `WRITE` command. For a list, see Abbreviations Used in ObjectScript.
    
*   For many of the commands, you can include a postconditional expression (often simply called a postconditional).
    
    This expression controls whether InterSystems IRIS executes the command. If the postconditional expression evaluates to true (nonzero), InterSystems IRIS executes the command. If the expression evaluates to false (zero or null), InterSystems IRIS ignores the command and continues with the next command.
    
    For example:
    
    ```objectscript
     Set count = 6
     Write:count<5 "Print this if count is less than five"
     Write:count>5 "Print this if count is greater than five"
    ```
    
    The preceding generates the following output: `Print this if count is greater than five`
    
    > **Note:**
    > 
    > If postconditionals are new to you, you might find the phrase “postconditional expression” somewhat misleading, because it suggests (incorrectly) that the expression is executed after the command. Despite the name, a postconditional is executed before the command.
    
    Postconditionals are also permitted for specific arguments of specific commands.
    
*   You can include multiple commands on a single line. For example:
    
    ```objectscript
     set myval="hello world" write myval
    ```
    
    When you do this, beware that you must use two spaces after any command that does not take arguments, if there are additional commands on that line; if you do not do so, a syntax error occurs.
    
*   The `IF`, `ELSE`, `FOR`, and `DO` commands are available in two forms:
    
    *   A newer block form, which uses curly braces to indicate the block. For example:
        
        ```objectscript
         if (testvalue=1) {
             write "hello world"
          }
        ```
        
        InterSystems recommends that you use the block form in all new code.
        
    *   An older line-based form, which does not use curly braces. For example:
        
        ```objectscript
         if (testvalue=1) write "hello world"
        ```
        
*   As a result of the preceding items, ObjectScript can be written in a very compact form. For example:
    
    ```objectscript
     s:$g(%d(3))'="" %d(3)=$$fdN3(%d(3)) q
    ```
    
    The class compiler automatically generates compact code of the form shown above (although not necessarily with abbreviated commands as in this example). Sometimes it is useful to look at this generated code, to track down the source of a problem or to understand how something works.
    
*   There are no truly reserved words in ObjectScript, so it is theoretically possible to have a variable named `set`, for example. However, it is prudent to avoid names of commands, functions, SQL reserved words, and certain system items; see Syntax Rules.
    
*   InterSystems IRIS allocates a fixed amount of memory to hold the results of string operations. If a string expression exceeds the amount of space allocated, a <MAXSTRING> error results. See string length limit.
    
    For class definitions, the string operation limit affects the size of string properties. InterSystems IRIS provides a system object (called a stream) that you can use when you need to work with strings that exceed this limit; in such cases, you use the stream interface classes.
    

## See Also

To learn more about ObjectScript, you can also refer to:

*   The ObjectScript Tutorial for an interactive introduction to most language elements.
    
*   The ObjectScript Reference for details on individual commands and functions.
