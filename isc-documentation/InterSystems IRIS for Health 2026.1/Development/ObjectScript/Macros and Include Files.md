# Macros and Include Files

This page describes how to define and use macros and include files (which contain macros). InterSystems IRIS data platform provides system macros that you can use as well.

> **Important:**
> 
> The phrase include file is used for historical reasons but unfortunately also creates some confusion. In InterSystems IRIS, an include file is not actually a separate standalone file in the operating system. As with classes and routines, an include file is a unit of code stored within an InterSystems IRIS database.
> 
> Your IDE provides an option for creating an include file, and will store the code correctly in the database — the same as with any other code element. Similarly, if the IDE is connected to a source control system, each code element is projected to an external file that is managed via source control.

## Macro Basics

A macro is a convenient substitution that you can define and use as follows:

1.  You define the macro via special syntax, typically the #define directive. For example:
    
    ```objectscript
    #define StringMacro "Hello, World!"
    ```
    
    This syntax defines a macro called `StringMacro`. Note that macro names are case-sensitive.
    
2.  Later, you invoke the macro with the syntax `$$$macroname`, for example:
    
    ```objectscript
      write $$$StringMacro
    ```
    
    The previous is equivalent to the following:
    
    ```objectscript
      write "Hello, World!"
    ```
    

The substitution occurs when the code (a class or routine) is compiled. Specifically, the class or routine itself is unchanged, but the generated .INT code shows the substitutions. (For a fuller picture of how code is compiled, see How These Code Elements Work Together.)

Remember that macros are text substitutions. After the substitution is performed, the resulting statement must be syntactically correct. Therefore, the macro defining an expression should be invoked in a context requiring an expression; the macro for a command and its argument can stand as an independent line of ObjectScript; and so on.

## Include File Basics

Typically, you define macros within an include file, which you then include within other code, which enables that code to refer to the macros. This works as follows:

1.  An include file is a specific kind of unit of code stored in the database. The following shows a partial example:
    
    ```objectscript
    #; Optional comment lines
    #define RELEASEID $GET(^MyGlobal("ReleaseID"),"")
    #define RELEASENUMBER $GET(^MyGlobal("ReleaseNumber"),"")
    #define PRODUCT $GET(^MyGlobal("Product"),"")
    #define LOCALE $GET(^MyGlobal("Locale"),"en-us")
    ```
    
    Notice that each line is either a comment line or starts with a #define directive. Blank lines are also permitted. There are alternatives to #define that enable you to define more complex macros; these are discussed elsewhere in more detail.
    
    In the typical scenario, you create an include file in your IDE and save it with a specific name, such as `MyMacros`.
    
2.  Within a class or routine that needs to use the macros, include the include file. For example:
    
    ```objectscript
    include MyMacros
    
    Class MyPackage.MyClass {
    
    //
    }
    ```
    
    In this example, the name of the include file is `MyMacros`.
    
    This step makes macros of `MyMacros` available for use within the class or routine.
    
    For all the syntax variations, which are different for routines, see Including Include Files.
    
3.  Within that same class or routine, use the syntax `$$$macroname` to refer to the macro. For example:
    
    ```objectscript
     set title=$$$PRODUCT_" "_$$$RELEASENUMBER
    ```
    

> **Note:**
> 
> In running text, it is common to append `.inc` to the include file name; for example, a set of useful system macros are defined in the `%occStatus.inc` and `%occMessages.inc` include files.

## Defining Macros

In their most basic form, macros are created with a #define directive as shown in Macro Basics.

There are additional directives that enable you to define macros that accept arguments and that support more complex scenarios. Also you can use ##continue to continue a #define directive to the next line. See Preprocessor Directives Reference for more.

This section provides information on where you can define macros, what macro definitions can contain, the rules that macro names must follow, use of whitespace in macros, and macro comments.

### Where to Define Macros

You can define macros in the following locations, each of which affects the availability of the macros:

*   You can define macros in an include file. In this case, the macros are available within any code that includes the necessary include file.
    
    Note that when a class includes an include file, any subclass of that class automatically includes the same include file.
    
*   You can define macros within a method. In this case, the macros are available within that method.
    
*   You can define macros within a routine. In this case, the macros are available within that routine.
    

### Allowed Macro Definitions

Supported functionality includes:

*   String substitutions, as demonstrated above.
    
*   Numeric substitutions:
    
    ```objectscript
    #define NumberMacro 22
    ```
    
    ```objectscript
    #define 25M ##expression(25*1000*1000)
    ```
    
    As is typical in ObjectScript, the definition of the numeric macro does not require quoting the number, while the string must be quoted in the string macro’s definition.
    
*   Variable substitutions:
    
    ```objectscript
    #define VariableMacro Variable
    ```
    
    Here, the macro name substitutes for the name of a variable that is already defined. If the variable is not defined, there is an <UNDEFINED> error.
    
*   Command and argument invocations:
    
    ```objectscript
    #define CommandArgumentMacro(%Arg) WRITE %Arg,!
    ```
    
    Macro argument names must start with the `%` character, such as the `%Arg` argument above. Here, the macro invokes the `WRITE` command, which uses the `%Arg` argument.
    
*   Use of functions, expressions, and operators:
    
    ```objectscript
    #define FunctionExpressionOperatorMacro ($ZDate(+$Horolog))
    ```
    
    Here, the macro as a whole is an expression whose value is the return value of the `$ZDate` function. `$ZDate` operates on the expression that results from the operation of the `+` operator on the system time, which the system variable `$Horolog` holds. As shown above, it is a good idea to enclose expressions in parentheses so that they minimize their interactions with the statements in which they are used.
    
*   References to other macros:
    
    ```objectscript
    #define ReferenceOtherMacroMacro WRITE $$$ReferencedMacro
    ```
    
    Here, the macro uses the expression value of another macro as an argument to the `WRITE` command.
    
    > **Note:**
    > 
    > If one macro refers to another, the referenced macro must appear on a line of code that is compiled before the referencing macro.
    

### Macro Naming Conventions

*   The first character must be an alphanumeric character or the percent character (%).
    
*   The second and subsequent characters must be alphanumeric characters. A macro name may not include spaces, underscores, hyphens, or other symbol characters.
    
*   Macro names are case-sensitive.
    
*   Macro names can be up to 500 characters in length.
    
*   Macro names can contain Japanese ZENKAKU characters and Japanese HANKAKU Kana characters. For further details, refer to the “Pattern Codes” table in Pattern Match Operator.
    
*   Macro names should not begin with `ISC`, because `ISCname`.inc files are reserved for system use.
    

### Macro Whitespace Conventions

*   By convention, a macro directive is not indented and appears in column 1. However, a macro directive may be indented.
    
*   One or more spaces may follow a macro directive. Within a macro, any number of spaces may appear between macro directive, macro name, and macro value.
    
*   A macro directive is a single-line statement. The directive, macro name, and macro value must all appear on the same line. You can use ##continue to continue a macro directive to the next line.
    
*   #if and #elseIf directives take a test expression. This test expression may not contain any spaces.
    
*   An #if expression, an #elseIf expression, the #else directive, and the #endif directive all appear on their own line. Anything following one of these directives on the same line is considered a comment and is not parsed.
    

### Macro Comments and Typeahead Assistance

Macros can include comments, which are passed through as part of their definition. Comments delimited with `/*` and `*/`, `//`, `#;`, `;`, and `;;` all behave in their usual way. See Comments.

Comments that begin with the `///` indicator have a special functionality. If you want your IDE to provide typeahead assistance for a macro that is in an include file, then place a `///` comment on the line that immediately precedes its definition; this causes its name to appear in the IDE typeahead popup. (All macros in the current file appear in that popup, without any intervention on your part.) For example, if the following code were referenced through an `#include` directive, then the first macro would appear in typeahead popup and the second would not:

```objectscript
/// A macro that is visible with IDE Typeahead
#define MyAssistMacro 100
 //
 // ...
 //
 // A macro that is not visible with IDE Typeahead
#define MyOtherMacro -100
```

For information on making macros available through include files, see Including Include Files.

## Including Include Files

This section describes how to include include files in your code.

*   To include an include file in a class or at the beginning of a routine, use a directive of the form:
    
    ```objectscript
    #include MacroIncFile
    ```
    
    where `MacroIncFile` refers to an included file containing macros that is called `MacroIncFile.inc`. Note that the `.inc` suffix is not included in the name of the referenced file when it is an argument of `#include`. The `#include` directive is not case-sensitive.
    
    Note that when a class includes an include file, any subclass of that class automatically includes the same include file.
    
    For example, if you have one or more macros in the file `MyMacros.inc`, you can include them with the following call:
    
    ```objectscript
    #include MyMacros
    ```
    
*   To include multiple include files in a routine, use multiple directives of the same form. For example:
    
    ```objectscript
    #include MyMacros
    #include YourMacros
    ```
    
*   To include multiple include files at the beginning of a class definition, the syntax is of the form:
    
    ```
    include (MyMacros, YourMacros)
    ```
    
    Note that this `include` syntax does not have a leading pound sign; this syntax cannot be used for `#include`.
    

See the reference section on #include.

Note that when you compile a class definition, that process normalizes the class definition in various ways such as removing whitespace. One of these normalizations converts the capitalization of the include directive.

The ObjectScript compiler provides a `/defines` qualifier that permits including external macros. For further details refer to the Compiler Qualifiers table in the `$SYSTEM` reference page.

## Where to See Expanded Macros

As noted above, when you compile classes and routines, the system generates INT code (intermediate ObjectScript) code, which you can display and read the INT code, which is a useful way to perform some kinds of troubleshooting.

> **Note:**
> 
> The preprocessor expands macros before the ObjectScript parser handles any Embedded SQL. The preprocessor supports Embedded SQL in either embedded or deferred compilation mode; the preprocessor does not expand macros within Dynamic SQL.
> 
> The ObjectScript parser removes multiple line comments before parsing preprocessor directives. Therefore, any macro preprocessor directive specified within a /* . . . */ multiple line comment is not executed.

Also, the following globals contain MAC code (the original source code). Use `ZWRITE` to display these globals and their subscripts:

*   `^rINDEX(routinename,"MAC")` contains the timestamp when the MAC code was last saved after being modified, and the character count for this MAC code file. The character count including comments and blank lines. The timestamp when the MAC code was last saved, when it was compiled, and information about #include files used are recorded in the ^ROUTINE global for the INT code. For further details about INT code, refer to the ZLOAD command.
    
*   `^rMAC(routinename)` contains a subscript node for each line of code in the MAC routine, as well as `^rMAC(routinename,0,0)` containing the line count, `^rMAC(routinename,0)` containing the timestamp when it was last saved, and `^rMAC(routinename,0,"SIZE")` containing the character count.
    
*   `^rMACSAVE(routinename)` contains the history of the MAC routine. It contains the same information as `^rMAC(routinename)` for the past five saved versions of the MAC routine. It does not contain information about the current MAC version.
    

## See Also

*   #define
    
*   #include
    
*   Preprocessor Directives Reference
    
*   System Macros
