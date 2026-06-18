# ObjectScript Syntax Basics

This topic describes the basic rules of ObjectScript syntax. Additional pages describe more syntax rules.

## Left-to-Right Precedence

Operator precedence in ObjectScript is strictly left-to-right; within an expression, operations are performed in the order in which they appear. This is different from other languages in which certain operators have higher precedence than others. For more information, see Operator Precedence.

## Case Sensitivity

Some parts of ObjectScript are case-sensitive while others are not. The following overview covers many but not all the cases:

*   Not case-sensitive: ObjectScript commands, functions, and system variables are not case sensitive.
    
*   Usually not case-sensitive: Case sensitivity of the following is platform-dependent: device names, file names, directory names, disk drive names. The exponent symbol is usually not case-sensitive, but this depends on your system configuration.
    
*   Case-sensitive: variable names (other than the ObjectScript system variables) are case-sensitive. Names of routines and their entry points, names of include files and macros are also all case sensitive.
    

Also, when you use ObjectScript syntax to refer to a package, class, or class member, you must match its case exactly. However, you cannot create packages or classes that differ only in case. For example, if you create the class `A.B`, you must use that case when referring to that class, for example: `##class(A.B).MyMethod()`. However, you cannot now create classes named `a.b`, `A.b`, or `a.B`; you also cannot create new classes in any packages named `a.b`, `A.b`, or `a.B`.

## Identifiers

An identifier is the name of a variable, package, class, class member, routine, or label. In general, legal identifiers consist of letter and number characters; with few exceptions, punctuation characters are not permitted in identifiers. Identifiers are case-sensitive.

> **Note:**
> 
> SQL identifiers, in contrast, are not case-sensitive.

For variables, the variable name determines the kind of variable it is, which determines its scope and special characteristics. See Variables.

For reference information on identifiers, including variable names to avoid, see Rules and Guidelines for Identifiers.

## Reserved Words

There are no reserved words in ObjectScript; you can use any valid identifier as a variable name, function name, or label. At the same time, it is best to avoid using identifiers that are command names, function names, or other such strings. Also, since ObjectScript code includes support for embedded SQL, it is prudent to avoid naming any function, object, variable, or other entity with an SQL reserved word, as this may cause difficulties elsewhere.

## Expressions

An ObjectScript expression is one or more tokens that can be evaluated to yield a value. The simplest expression is simply a literal or variable:

```objectscript
 SET expr = 22
 SET expr = "hello"
 SET expr = x
```

You can create more complex expressions using operators and functions:

```objectscript
 SET expr = +x
 SET expr = x + 22
 SET expr = array(1)
 SET expr = ^data("x",1)
 SET expr = $Length(x)
```

An expression may consist of, or include, an object property, instance method call, or class method call:

```objectscript
 SET expr = person.Name
 SET expr = obj.Add(1,2)
 SET expr = ##class(MyApp.MyClass).Method()
```

You can directly invoke an ObjectScript routine call within an expression by placing $$ in front of the routine call:

```objectscript
 SET expr = $$MyFunc^MyRoutine(1)
```

## Commands

All the execution tasks in ObjectScript are performed by commands. Every command consists of a command keyword followed by (in most cases) one or more command arguments. Note the following syntax rules:

*   Command names are not case-sensitive. Most command names can be represented by an abbreviated form. Therefore, WRITE, Write, write, W, and w are all valid forms of the `WRITE` command. For a list of command abbreviations, see Table of Abbreviations.
    
*   Command keywords are not reserved words. It is therefore possible to use a command keyword as a user-assigned name for a variable, label, or other identifier.
    
*   Within code, an ObjectScript command cannot appear in column 1; see the discussion later on whitespace.
    
    The same restriction does not apply when issuing a command from the ObjectScript shell or the `XECUTE` command.
    
*   If the command accepts arguments, there must be exactly 1 space between the command and the first argument.
    
*   You can include multiple commands (with their arguments) on the same line.
    
    The commands are executed in strict left-to-right order, and are functionally identical to commands appearing on separate lines. A command with arguments must be separated from the command following it by one space character. An argumentless command must be separated from the command following it by two space characters. A label can be followed by one or more commands on the same line. A comment can follow one or more commands on the same line.
    
    For the maximum length of a line of source code, see General System Limits.
    
*   One or more commands may follow a label on the same line; the label and the command are separated by one or more spaces.
    
*   No end-of-command or end-of-line delimiter is required or permitted. You can specify an in-line comment following a command, indicating that the rest of the command line is a comment. A blank space is required between the end of a command and comment syntax, with the exception of `##;` and `/* comment */` syntax. A `/* comment */` multiline comment can be specified within a command as well as at the end of one.
    
*   Many commands can use a postconditional expression; this phrase refers to a logical expression that determines whether to execute the command. If the expression evaluates to true, the command is executed; otherwise it isn’t.
    

## Command Postconditional Expressions

In most cases, when you specify an ObjectScript command you can append a postconditional.

A postconditional is an optional expression that is appended to a command or (in some cases) a command argument that controls whether InterSystems IRIS executes that command or command argument. If the postconditional expression evaluates to TRUE (defined as nonzero), InterSystems IRIS executes the command or the command argument. If the postconditional expression evaluates to FALSE (defined as zero), InterSystems IRIS does not execute the command or command argument, and execution continues with the next command or command argument.

All ObjectScript commands can take a postconditional expression, except the flow-of-control commands (`IF`, `ELSEIF`, and `ELSE`; `FOR`, `WHILE`, and `DO WHILE`) and the block structure error handling commands (`TRY`, `CATCH`).

The ObjectScript commands `DO` and `XECUTE` can append postconditional expressions both to the command keyword and to their command arguments. A postconditional expression is always optional; for example, some of the command’s arguments may have an appended postconditional while its other arguments do not.

If both a command keyword and one or more of that command’s arguments specify a postconditionals, the keyword postconditional is evaluated first. Only if this keyword postconditional evaluates to TRUE are the command argument postconditionals evaluated. If a command keyword postconditional evaluates to FALSE, the command is not executed and program execution continues with the next command. If a command argument postconditional evaluates to FALSE, the argument is not executed and execution of the command continues with the next argument in left-to-right sequence.

### Postconditional Syntax

To add a postconditional to a command, place a colon (:) and an expression immediately after the command keyword, so that the syntax for a command with a postconditional expression is:

```
Command:pc
```

where `Command` is the command keyword, the colon is a required literal character, and `pc` can be any valid expression.

A command postconditional must follow these syntax rules:

*   No spaces, tabs, line breaks, or comments are permitted between a command keyword and its postconditional, or between a command argument and its postconditional. No spaces are permitted before or after the colon character.
    
*   No spaces, tabs, or line breaks are permitted within a postconditional expression, unless either an entire postconditional expression is enclosed in parentheses or the postconditional expression has an argument list enclosed in parentheses. Spaces, tabs, and line breaks are permitted within parentheses.
    
*   Spacing requirements following a postconditional expression are the same as those following a command keyword: there must be exactly one space between the last character of the keyword postconditional expression and the first character of the first argument; for argumentless commands, there must be two or more spaces between the last character of the postconditional expression and the next command on the same line, unless the postconditional is immediately followed by a close curly brace. (If parentheses are used, the closing parenthesis is treated as the last character of the postconditional expression.)
    

Note that a postconditional expression is not technically a command argument (though in the ObjectScript reference pages the explanation of the postconditional is presented as part of the Arguments section). A postconditional is always optional.

### Evaluation of Postconditionals

InterSystems IRIS evaluates a postconditional expression as either True or False. Most commonly these are represented by 1 and 0, which are the recommended values. However, InterSystems IRIS performs postconditional evaluation on any value, evaluating it as False if it evaluates to 0 (zero), and True if it evaluates to a nonzero value.

*   InterSystems IRIS evaluates as True any valid nonzero numeric value. It uses the same criteria for valid numeric values as the arithmetic operators. Thus, the following all evaluate to True: 1, “1”, 007, 3.5, -.007, 7.0 , 3 little pigs, $CHAR(49), 0_"1".
    
*   InterSystems IRIS evaluates as False the value zero (0), and any nonnumeric value, including a null string ("") or a string containing a blank space (" "). Thus, the following all evaluate to False: 0, -0.0, A, -, $, The 3 little pigs, $CHAR(0), $CHAR(48), "0_1".
    
*   Standard equivalence rules apply. Thus, the following evaluate to True: 0=0, 0="0", "a"=$CHAR(97), 0=$CHAR(48), and (" "=$CHAR(32)). The following evaluate to False: 0="", 0=$CHAR(0), and (""=$CHAR(32)).
    

In the following example, which `WRITE` command is executed depends on the value of the variable `count`:

```objectscript
 FOR count=1:1:10 {
   WRITE:count<5 count," is less than 5",!
   WRITE:count=5 count," is 5",!
   WRITE:count>5 count," is greater than 5",!
 }
```

## Command Arguments

Following a command keyword, there can be zero, one, or multiple arguments that specify the object(s) or the scope of the command. If a command takes one or more arguments, you must include exactly one space between the command keyword and the first argument. For example:

```objectscript
 SET x = 2
```

Spaces can appear within arguments or between arguments, so long as the first character of the first argument is separated from the command itself by exactly one space (as appears above). Thus the following are all valid:

```objectscript
  SET a = 1
  SET b=2
  SET c=3,d=4
  SET e= 5   ,  f =6
  SET g
      =            7
  WRITE a,b,c,d,e,f,g
```

If a command takes a postconditional expression, there must be no spaces between the command keyword and the postconditional, and there must be exactly one space between the postconditional and the beginning of the first argument. Thus, the following are all valid forms of the `QUIT` command:

```objectscript
 QUIT x+y
 QUIT x + y
 QUIT:x<0
 QUIT:x<0 x+y
 QUIT:x<0 x + y
```

No spaces are required between arguments, but multiple blank spaces can be used between arguments. These blank spaces have no effect on the execution of the command. Line breaks, tabs, and comments can also be included within or between command arguments with no effect on the execution of the command. For further details, see White Space.

### Multiple Arguments

Many commands allow you to specify multiple independent arguments. The delimiter for command arguments is the comma ,. That is, you specify multiple arguments to a single command as a comma-separated list following the command. For example:

```objectscript
   SET x=2,y=4,z=6
```

This command uses three arguments to assign values to the three specified variables. In this case, these multiple arguments are repetitive; that is, the command is applied independently to each argument in the order specified. Internally, InterSystems IRIS data platform parses this as three separate `SET` commands. When debugging, each of these multiple arguments is a separate step.

In the command syntax provided in the command reference pages, arguments that can be repeated are followed by a comma and ellipsis: `,...`. The comma is a required delimiter character for the argument, and the ellipsis (...) indicates that an unspecified number of repetitive arguments can be specified.

Repetitive arguments are executed in strict left-to-right order. Therefore, the following command is valid:

```objectscript
   SET x=2,y=x+1,z=y+x
```

but the following command is not valid:

```objectscript
   SET y=x+1,x=2,z=y+x
```

Because execution is performed independently on each repetitive argument, in the order specified, valid arguments are executed until the first invalid argument is encountered. In the following example, `SET x` assigns a value to `x`, `SET y` generates an <UNDEFINED> error, and because `SET z` is not evaluated, the <DIVIDE> (divide-by-zero) error is not detected:

```objectscript
   KILL x,y,z
   SET x=2,y=z,z=5/0
   WRITE "x is:",x
```

### Arguments with Their Own Arguments and Postconditionals

Some command arguments accept their own arguments and even their own postconditionals.

The following sample command shows a comma between the two arguments. Each argument is followed by a colon-separated list of its own arguments:

```objectscript
 VIEW X:y:z:a,B:a:y:z
```

For a few commands (`DO`, `XECUTE`, and `GOTO`), a colon following an argument specifies a postconditional expression that determines whether or not that argument should be executed.

### Argumentless Commands

Commands that do not take an argument are referred to as argumentless commands. A postconditional expression appended to the keyword is not considered an argument.

There are a small number of commands that are always argumentless. For example, `HALT`, `CONTINUE`, `TRY`, `TSTART`, and `TCOMMIT` are argumentless commands.

Several commands are optionally argumentless. For example, `BREAK`, `CATCH`, `FOR`, `GOTO`, `KILL`, `LOCK`, `NEW`, `QUIT`, `RETURN`, `TROLLBACK`, `WRITE`, and `ZWRITE` all have argumentless syntactic forms. In such cases, the argumentless command may have a slightly different meaning than the same command with an argument.

If you use an argumentless command at the end of the line, trailing spaces are not required. If you use an argumentless command on the same code line as other commands, you must place two (or more) spaces between the argumentless command and any command that follows it. For example:

```objectscript
 QUIT:x=10  WRITE "not 10 yet"
```

In this case, `QUIT` is an argumentless command with a postconditional expression, and a minimum of two spaces is required between it and the next command.

#### Argumentless Commands and Curly Braces

Argumentless commands when used with command blocks delimited by curly braces do not have whitespace restrictions:

*   An argumentless command that is immediately followed by an opening curly brace has no whitespace requirement between the command name and the curly brace. You can specify none, one, or more than one spaces, tabs, or line returns. This is true both for argumentless commands that can take an argument, such as `FOR`, and argumentless commands that cannot take an argument, such as `ELSE`.
    
    ```objectscript
     FOR  {
        WRITE !,"Quit out of 1st endless loop"
        QUIT
     }
     FOR{
        WRITE !,"Quit out of 2nd endless loop"
        QUIT
     }
     FOR
     {
        WRITE !,"Quit out of 3rd endless loop"
        QUIT
     }
    ```
    
*   An argumentless command that is immediately followed by a closing curly brace does not require trailing spaces, because the closing curly brace acts as a delimiter. For example, the following is a valid use of the argumentless `QUIT`:
    
    ```objectscript
     IF 1=2 {
        WRITE "Math error"}
     ELSE {
        WRITE "Arthmetic OK"
        QUIT}
     WRITE !,"Done"
    ```
    

## Routine Syntax

Routines are the building blocks of ObjectScript programs. Class definitions (not formally part of the ObjectScript language) are compiled into routines. You can write any combination of routines and class definitions that meets your needs; all this code is ultimately compiled into runtime code.

A routine is a unit of code (generally seen a single unit within an IDE or a source control system) that consists of lines of ObjectScript code, comments, and blank lines. It is generally organized as follows:

1.  One or more comment lines at the start, optionally indicating the name of the routine as well as containing any usage notes or update history.
    
2.  Any number of procedures, which have the following syntax:
    
    ```
    ProcedureName(Arguments) scopekeyword {
        //procedure implementation
    }
    ```
    
    Where:
    
    *   `ProcedureName` is the name of the procedure. This is an ObjectScript label and it must start in column 1 of the line.
        
    *   `Arguments` is an optional comma-separated list of arguments. Even if there are no arguments, you must include the parentheses.
        
    *   The optional `scopekeyword` is one of the following (not case-sensitive):
        
        *   `Public`. If you specify `Public`, then the procedure is public and can be invoked outside of the routine itself.
            
        *   `Private` (the default for procedures). If you specify `Private`, the procedure is private and can be invoked only by other code in the same routine.
            
    *   The implementation consists of zero or more lines of ObjectScript. This code can return a value via RETURN or QUIT.
        
    
    For details, see Defining Procedures.
    

The routine can also contain:

*   Comments and whitespace, both within procedures and between them
    
*   Legacy forms of subroutines
    

## Method Syntax

For completeness, it is also useful to consider methods, which are defined within classes. Class definitions are not part of ObjectScript, but can include ObjectScript in multiple places, and classes are compiled into routines and ultimately into the same runtime code. The most common use for ObjectScript in a class is within methods. A class method (called a static method in some languages) has the following syntax:

```
ClassMethod MethodName(Arguments) as Classname [ Keywords]
{
 //method implementation
}
```

The syntax for an instance method (relevant only in object classes) is similar:

```
Method MethodName(Arguments) as Classname [ Keywords]
{
 //method implementation
}
```

Where:

*   `MethodName` is the name of the method.
    
*   `Arguments` is a comma-separated list of arguments.
    
*   `Classname` is an optional class name that represents the type of value (if any) returned by this method. Omit the `As Classname` part if the method does not return a value.
    
*   `Keywords` represents any method keywords, which control things such as how this method is projected to SQL, whether this method is available outside of the class to which it belongs, and so on. These are optional. See Compiler Keywords.
    
*   The method implementation consists of zero or more lines of ObjectScript. This code can return a value via RETURN or QUIT.
    

## Whitespace

Under certain circumstances, ObjectScript treats whitespace as syntactically meaningful. Unless otherwise specified, whitespace refers to blank spaces, tabs, and line feeds interchangeably. In brief, the rules are:

*   Whitespace must appear at the beginning of each line of code and each single-line comment. Leading whitespace is not required for the following kinds of items:
    
    *   Label (also known as a tag or an entry point): a label must appear in column 1 with no preceding whitespace character. If a line has a label, there must be whitespace between the label and any code or comment on the same line. If a label has a parameter list, there can be no whitespace between the label name and the opening parenthesis for the parameter list. There can be whitespace before, between, or after the parameters in the parameter list.
        
    *   Macro directive: a macro directive such as #define can appear in column 1 with no preceding whitespace character. This is a recommended convention, but whitespace is permitted before a macro directive.
        
    *   Multiline comment: the first line of a multiline comment must be preceded by one or more spaces. The second and subsequent lines of a multiline comment do not require leading whitespace.
        
    *   Blank line: if a line contains no characters, it does not need to contain any spaces. A line consisting only of whitespace characters is permitted and treated as a comment.
        
*   There must be one and only one space (not a tab) between a command and its first argument; if a command uses a postconditional, there are no spaces between the command and its postconditional.
    
*   If a postconditional expression includes any spaces, then the entire expression must be parenthesized.
    
*   There can be any amount of whitespace between any pair of command arguments.
    
*   If a line contains code and then a single-line comment, there must be whitespace between them.
    
*   Typically, each command appears on its own line, though you can enter multiple commands on the same line. In this case, there must be whitespace between them; if a command is argumentless, then it must be followed by two spaces (two spaces, two tabs, or one of each). Additional whitespace may follow these two required spaces.
    

## Labels

Any line of ObjectScript code can optionally include a label (also known as a tag). A label serves as a handle for referring to that line location in the code. A label is an identifier that is not indented; it is specified in column 1. All ObjectScript commands must be indented.

Labels have the following naming conventions:

*   The first character must be an alphanumeric character or the percent character (%). Note that labels are the only ObjectScript names that can begin with a number. The second and all subsequent characters must be alphanumeric characters. A label may contain Unicode letters.
    
*   They can be up to 31 characters long. A label may be longer than 31 characters, but must be unique within the first 31 characters. A label reference matches only the first 31 characters of the label. However, all characters of a label or label reference (not just the first 31 characters) must abide by label character naming conventions.
    
*   They are case-sensitive.
    

> **Note:**
> 
> A block of ObjectScript code specified in an SQL command such as CREATE PROCEDURE or CREATE TRIGGER can contain labels. In this case, the first character of the label is prefixed by a colon (:) specified in column 1. The rest of the label follows the naming and usage requirements describe here.

A label can include or omit parameter parentheses. If included, these parentheses may be empty or may include one or more comma-separated parameter names. A label with parentheses identifies a procedure block.

A line can consist of only a label, a label followed by one or more commands, or a label followed by a comment. If a command or a comment follows the label on the same line, they must be separated from the label by a space or tab character.

The following are all unique labels:

```objectscript
maximum
Max
MAX
%control
```

You can use the $ZNAME function to validate a label name. Do not include parameter parentheses when validating a label name.

Labels are useful for identifying sections of code and for managing flow of control. See Legacy Code and Labels.

## Comments

It is good practice to use comments to provide in-line documentation in code, as they are a valuable resource when modifying or maintaining code. ObjectScript supports several types of comments which can appear in several kinds of locations:

*   Comments in INT Code for Routines and Methods
    
*   Comments in MAC Code for Routines and Methods
    
*   Comments in Class Definitions Outside of Method Code
    

### Comments in INT Code for Routines and Methods

ObjectScript code is written as MAC code, from which INT (intermediate) code is generated. Comments written in MAC code are generally available in the corresponding INT code. You can use the ZLOAD command to load an INT code routine, then use the ZPRINT command or the $TEXT function to display INT code, including these comments. The following types of comments are available, all of which must start in column 2 or greater:

*   The `/* */` multiline comment can appear within a line or across lines. `/*` can be the first element on a line or can follow other elements; `*/` can be the final element on the line or can precede other elements. All lines in a `/* */` appear in the INT code, including lines that consist of just the `/*` or `*/`, with the exception of completely blank lines. A blank line within a multi-line comment is omitted from the INT code, and can thus affect the line count.
    
*   The `//` comment specifies that the remainder of the line is a comment; it can be the first element on the line or follow other elements.
    
*   The `;` comment specifies that the remainder of the line is a comment; it can be the first element on the line or can follow other elements.
    
*   The `;;` comment — a special case of the `;` comment type — makes the comment available to the $TEXT function when the routine is distributed as object code only; the comment is only available to `$TEXT` if no commands precede it on the line.
    
    > **Note:**
    > 
    > Because InterSystems IRIS retains `;;` comments in the object code (the code that is actually interpreted and executed), there is a performance penalty for including them and they should not appear in loops.
    

A multiline comment (`/* comment */`) can be placed between command or function arguments, either before or after a comma separator. A multiline comment cannot be placed within an argument, or be placed between a command keyword and its first argument or a function keyword and its opening parenthesis. It can be placed between two commands on the same line, in which case it functions as the single space needed to separate the commands. You can immediately follow the end of a multiline comment (*/) with a command on the same line, or follow it with a single line comment on the same line. The following example shows these insertions of `/* comment */` within a line:

```objectscript
  WRITE $PIECE("Fred&Ginger"/* WRITE "world" */,"&",2),!
  WRITE "hello",/* WRITE "world" */" sailor",!
  SET x="Fred"/* WRITE "world" */WRITE x,!
  WRITE "hello"/* WRITE "world" */// WRITE " sailor"
```

### Comments in MAC Code for Routines and Methods

The following comment types can be written in MAC code but have different behaviors in the corresponding INT code:

*   The `#;` comment can start in any column but must be the first element on the line. #: comments do not appear in INT code. Neither the comment nor the comment marker (#;) appear in the INT code and no blank line is retained. Therefore, the `#;` comment can change INT code line numbering.
    
*   The `##;` comment can start in any column. It can be the first element on the line or can follow other elements. `##;` comments do not appear in INT code. ##: can be used in ObjectScript code, in Embedded SQL code, or on the same line as a #define, #def1arg or ##continue macro preprocessor directive.
    
    If the `##;` comment starts in column 1, neither the comment nor the comment marker (##;) appear in the INT code and no blank line is retained. However, if the `##;` comment starts in column 2 or greater, neither the comment nor the comment marker (##;) appear in the INT code, but a blank line is retained. In this usage, the `##;` comment does not change INT code line numbering.
    
*   The `///` comment can start in any column but must be the first element on the line. If `///` starts in column 1, it does not appear in INT code and no blank line is retained. If `///` starts in column 2 or greater, the comment appears in INT code and is treated as if it were a `//` comment.
    

### Comments in Class Definitions Outside of Method Code

Within class definitions, but outside of method definitions, several comment types are available, all of which can start in any column:

*   The `//` and `/* */` comments are for comments within the class definition.
    
*   The `///` comment serves as class reference content for the class or class member that immediately follows it. For classes themselves, the `///` comment preceding the beginning of the class definition provides the description of the class for the class reference content which is also the value of description keyword for the class). Within classes, all `///` comments immediately preceding a member (either from the beginning of the class definition or after the previous member) provide the class reference content for that member, where multiple lines of content are treated as a single block of HTML. For more information on the rules for `///` comments and the class reference, see Creating Class Documentation.
    

## Namespaces

In InterSystems IRIS, code always runs within a namespace, which is a logical container for data and code. For information on what is available within a namespace, see Namespaces and Databases. For information on namespace names, see Configuring Namespaces.

For ObjectScript commands that accept a namespace name as an argument, you can use an implied namespace name.

In generated code, InterSystems IRIS replaces punctuation characters in explicit and implied namespace names as follows:

% = p, _ = u, – = d, @ = s, : = s, / = s, \ = s, [ = s, ] = s, ^ = s.

## See Also

*   Procedure Syntax
    
*   Invoking Code and Passing Arguments
    
*   ObjectScript Variables and Scope
    
*   Macros and Include Files
