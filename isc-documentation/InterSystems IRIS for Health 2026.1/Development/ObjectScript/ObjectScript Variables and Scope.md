# ObjectScript Variables and Scope

A variable is the name of a location in which a value can be stored. Unlike many computer languages, ObjectScript does not require variables to be declared. A variable is created when it is assigned a value.

## Kinds of Variables

Within ObjectScript, there are multiple kinds of variables, as follows:

*   Local variables, which hold data in memory.
    
    Local variables can have public or private scope.
    
*   Global variables or globals, which hold data in a database. All interactions with a global affect the database immediately. For example, when you set the value of a global, that change immediately affects what is stored; there is no separate step for storing values. Similarly, when you remove a global, the data is immediately removed from the database.
    
*   Process-private global variables or PPGs
    
*   i%property instance variables
    
*   Special variables, also called system variables
    

This page primarily discusses local variables and global variables.

## Variable Names

The name of a variable determines what kind of variable it is. The names of variables follow these rules:

*   For most local variables, the first character is a letter, and the rest of the characters are letters or numbers. Valid names include `myvar` and `i`
    
*   For most global variables, the first character is always a caret (`^`). The rest of the characters are letters, numbers, or periods. Valid names include `^myvar` and `^my.var`
    
    Note that InterSystems IRIS provides special treatment for globals with names that start `^IRIS.TempUser` — for example, `^IRIS.TempUser.MyApp`. If you create such globals, these globals are written to the `IRISTEMP` database.
    
*   For a process-private global variable, the first character is a caret. Valid names include `^||MyVar`, `^|"^"|MyVar`, `^["^"]MyVar`, and `^["^",""]MyVar`. See Process-Private Globals.
    

For information on names that avoid collisions with system code, see Rules and Guidelines for Identifiers.

### Percent Variables

For local and global variables, InterSystems IRIS supports a variation known as a percent variable; these are less common. The name of a local percent variable starts with `%`, and the name of a global percent variable starts with `^%`. Percent variables are special in that they are always public; that is they are visible to all code within a process. This includes all methods and all procedures within the calling stack. In the case of a global percent variable, in addition to being public, the variable is available in all namespaces.

To avoid collisions with system code, when you define percent variables, use the following rules:

*   For a local percent variable, start the name with `%Z` or `%z`.
    
*   For a global percent variable, start the name with `^%Z` or `^%z`.
    

For further details on variable names and for variations, see Rules and Guidelines for Identifiers.

## Variable Availability and Scope

ObjectScript supports the following program flow, which is similar (in most ways) to what other programming languages support:

1.  A user invokes a method, perhaps from a user interface.
    
2.  The method executes some statements and then invokes a second method.
    
3.  The second method defines local variables A, B, and C.
    
    Variables A, B, and C are in scope within this method. They are private to this method.
    
4.  The second method also defines the global variable ^D.
    
5.  The second method ends, and control returns to the first method.
    
6.  The first method resumes execution. This method cannot use variables A, B, and C, which are no longer defined. It can use ^D, because that variable was immediately saved to the database.
    

The preceding program flow is quite common. InterSystems IRIS provides other options, however, of which you should be aware.

### Default Variable Scope

Several factors control whether a variable is available outside of the method that defines it. Before discussing those, it is necessary to point out the following environmental details:

*   An InterSystems IRIS instance includes multiple namespaces, including multiple system namespaces and probably multiple namespaces that you define.
    
*   You can run multiple processes simultaneously in a namespace. In a typical application, many processes are running at the same time.
    

The following table summarizes where variables are available (except for process-private global variables, described on another page):

<table><tr><th>Variable availability, broken out by kind of variable</th><th>Outside of code that defines it (but in the same process)</th><th>In other processes in the same namespace</th><th>In other namespaces within same InterSystems IRIS instance</th></tr><tr><td>Local variable, private scope</td><td>No</td><td>No</td><td>No</td></tr><tr><td>Local variable, public scope</td><td>Yes</td><td>No</td><td>No</td></tr><tr><td>Local percent variable</td><td>Yes</td><td>No</td><td>No</td></tr><tr><td>Global variable (not percent)</td><td>Yes</td><td>Yes</td><td>Not unless global mappings permit this†</td></tr><tr><td>Global percent variable</td><td>Yes</td><td>Yes</td><td>Yes</td></tr></table>

By default, variables defined in a procedure or a method are private to that procedure or method, as noted before. Also, in a procedure or method, you can declare variables as public variables, although this practice is not preferred. See PublicList.

†Each namespace has default databases for specific purposes and can have mappings that give access to additional databases. Consequently, a global variable can be available to multiple namespaces, even if it is not a global percent variable. See Namespaces and Databases.

### The NEW Command

InterSystems IRIS provides another mechanism to enable you to control the scope of a variable: the `NEW` command. The argument to this command is one or more variable names, in a comma-separated list. The variables must be public variables and cannot be global variables.

This command establishes a new, limited context for the variable (which may or may not already exist). For example, consider the following routine:

```objectscript
 ; demonew
 ; routine to demo NEW
 NEW var2
 set var1="abc"
 set var2="def"
 quit
```

After you run this routine, the variable `var1` is available, and the variable `var2` is not, as shown in the following example Terminal session:

```objectscript
TESTNAMESPACE>do ^demonew

TESTNAMESPACE>write var1
abc
TESTNAMESPACE>write var2

write var2
^
<UNDEFINED> *var2
```

If the variable existed before you used `NEW`, the variable still exists after the scope of `NEW` has ended, and it retains its previous value. For example, consider the following Terminal session, which uses the routine defined previously:

```objectscript
TESTNAMESPACE>set var2="hello world"

TESTNAMESPACE>do ^demonew

TESTNAMESPACE>write var2
hello world
```

## Length of Value

The length of a value of a variable must be less than the string length limit.

## Variable Existence and Undefined Variables

You usually define a variable with the `SET` command. As noted earlier, when you define a global variable, that immediately affects the database.

A global variable becomes undefined only when you kill it (which means to remove it via the `KILL` command). This also immediately affects the database.

A local variable can become undefined in one of three ways:

*   It is killed.
    
*   The process (in which it was defined) ends.
    
*   It goes out of scope within that process.
    

To determine whether a variable is defined, you use the `$DATA` function. For example, the following shows a Terminal session that uses this function:

```objectscript
TESTNAMESPACE>write $DATA(x)
0
TESTNAMESPACE>set x=5

TESTNAMESPACE>write $DATA(x)
1
```

In the first step, we use `$DATA` to see if a variable is defined. The system displays 0, which means that the variable is not defined. Then we set the variable equal to 5 and try again. Now the function returns 1.

If you attempt to access an undefined variable, you get the <UNDEFINED> error. For example:

```objectscript
TESTNAMESPACE>WRITE testvar

WRITE testvar
^
<UNDEFINED> *testvar
```

## #dim (Optional)

ObjectScript does not require variables to be declared. You can, however, use the #dim preprocessor directive as an aid to documenting code.

The syntax forms of `#dim` are:

```objectscript
#dim VariableName As DataTypeName
#dim VariableName As List Of DataTypeName
#dim VariableName As Array Of DataTypeName
```

where `VariableName` is the variable for which you are naming a data type and `DataTypeName` specifies that data type.

## Global Variables and Journaling

InterSystems IRIS treats a `SET` or `KILL` of a global as a journaled transaction event; rolling back the transaction reverses these operations. Locks may be used to prevent access by other processes until the transaction that made the changes has been committed. Refer to Transaction Processing for further details.

In contrast, InterSystems IRIS does not treat a `SET` or `KILL` of a local variable or a process-private global as a journaled transaction event; rolling back the transaction has no effect on these operations.

## See Also

*   Multidimensional Arrays
    
*   Working with Globals
    
*   Process-Private Globals
