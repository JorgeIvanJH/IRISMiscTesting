# Extended References

In InterSystems IRIS data platform, all code that runs on the server runs in a namespace; see Namespaces and Databases. ObjectScript supports extended references, which is syntax that enables you to refer to specific kinds of items in other namespaces.

## Introduction

An extended reference is a reference to an entity that is located in another namespace. The namespace name can be specified as a string literal enclosed in quotes, as a variable that resolves to a namespace name, as an implied namespace name, or as a null string ("") a placeholder that specifies the current namespace.

All extended references can specify the current namespace, either explicitly by name, or by specifying a null string placeholder.

## Types

There are three types of extended references:

*   An extended global reference references a global variable in another namespace. The following syntactic forms are supported:
    
    ```
    ^["namespace"]global
    ^|"namespace"|global
    ```
    
    Note that the rule about the maximum length of a global reference applies to extended global references as well as to the more common global references.
    
*   An extended routine reference references a routine in another namespace.
    
    *   The DO command, the $TEXT function, and user-defined functions support the following syntactic form:
        
        ```
        |"namespace"|routine
        ```
        
    *   The JOB command supports the following syntactic forms: :
        
        ```
        routine|"namespace"|
        routine["namespace"]
        routine:"namespace"
        ```
        
    
    In all these cases, the reference is prefaced by a ^ (caret) character to indicate that the specified entity is a routine (rather than a label or an offset). This caret is not part of the routine name. For example, `DO ^|"SAMPLES"|fibonacci` invokes the routine named fibonacci, which is located in the SAMPLES namespace. The command `WRITE $$fun^|"SAMPLES"|house` invokes the user-defined function fun() in the routine house, located in the SAMPLES namespace.
    
*   An extended SSVN reference references a structured system variable (SSVN) in another namespace. The following syntactic forms are supported:
    
    ```
    ^$["namespace"]ssvn
    ^$|"namespace"|ssvn
    ```
    
    For further details, refer to the ^$GLOBAL, ^$LOCK, and ^$ROUTINE structured system variables.
    

To keep the language simple, the rest of this page discusses extended global references specifically.

## Forms and Syntaxes

There are two forms of extended references, differing in how they refer to the location of the global:

*   Explicit namespace reference — This form explicitly includes the name of the namespace where the global is located.
    
*   Implied namespace reference — Rather than using the namespace name, this form includes the database directory and, optionally, the system name. In this case, no global mappings apply, because the physical dataset (directory and system) is given as part of the global reference.
    
    > **Note:**
    > 
    > The examples shown here use the Windows directory structure. In practice, the form of such references is operating-system dependent.
    

Explicit namespace references are preferred, because they allow for redefinition of logical mappings externally, as requirements change, without altering your application code.

For each of these forms of extended references, InterSystems IRIS supports two syntaxes:

*   Bracket syntax, which encloses the extended reference with square brackets ([ ]).
    
*   Environment syntax, which encloses the extended reference with vertical bars (| |).
    

## Bracket Syntax

You can use bracket syntax to specify an extended global reference with either an explicit namespace or an implied namespace:

Explicit namespace:

```
^[nspace]glob
```

Implied namespace:

```
^[dir,sys]glob
```

In an explicit namespace reference, `nspace` is a defined namespace that the global `glob` has not currently been mapped or replicated to. In an implied namespace reference, `dir` is a directory (the name of which includes a trailing backslash: `\`), `sys` is a system, and `glob` is a global within that directory. If `nspace` or `dir` is specified as a carat (`^`), the reference is to a process-private global.

You must include quotation marks around the directory and system names or the namespace name unless you specify them as variables. The directory and system together comprise an implied namespace. An implied namespace can reference either:

*   The specified directory on the specified system.
    
*   The specified directory on your local system, if you do not specify a system name in the reference. If you omit the system name from an implied namespace reference, you must supply a double caret (^^) within the directory reference to indicate the omitted system name.
    

To specify an implied namespace on a remote system:

```
["dir","sys"]
```

To specify an implied namespace on the local system:

```
["^^dir"]
```

For example, to access the global SAMPLE in the `C:\BUSINESS\` directory on a machine called SALES:

```objectscript
  Set x = ^["C:\BUSINESS\","SALES"]SAMPLE
```

To access the global SAMPLE in the `C:\BUSINESS\` directory on your local machine:

```objectscript
   Set x = ^["^^C:\BUSINESS\"]SAMPLE
```

To access the global SAMPLE in the defined namespace MARKETING:

```objectscript
   Set x = ^["MARKETING"]SAMPLE
```

To access the process-private global SAMPLE:

```objectscript
   Set x = ^["^"]SAMPLE
```

## Bracket Syntax with References to Databases

InterSystems IRIS provides special bracket syntaxes to represent databases within extended references.

You can create an extended reference that includes a database name, as specified in the CPF file. Use the format `:ds:DB_name`. For example

```
["^^:ds:MYDATABASE"]
```

A similar syntax is available for an extended reference that refers to a database on a mirror. Use the format `:mirror:mirror_name:mirror_DB_name`. For example, when referring to the database with the mirror database name mirdb1 in the mirror CORPMIR, you could form an implied reference as follows:

```
["^^:mirror:CORPMIR:mirdb1"]
```

The mirrored database path can be used for both local and remote databases.

## Environment Syntax

The environment syntax is defined as:

```
^|"env"|global
```

`"env"` can have one of five formats:

*   The null string (`""`) — The current namespace on the local system.
    
*   `"namespace"` — A defined namespace that `global` is not currently mapped to. Namespace names are not case-sensitive. If `namespace` has the special value of `"^"`, it is a process-private global.
    
*   `"^^dir"` — An implied namespace whose default directory is the specified directory on your local system, where `dir` includes a trailing backslash (`\`).
    
*   `"^system^dir"` — An implied namespace whose default directory is the specified directory on the specified remote system, where `dir` includes a trailing backslash (`\`).
    
*   omitted — If there is no `"env"` at all, it is a process-private global.
    

To access the global SAMPLE in your current namespace on your current system, when no mapping has been defined for SAMPLE, use the following syntax:

```objectscript
   Set x = ^|""|SAMPLE
```

This is the same as the simple global reference:

```objectscript
   Set x = ^SAMPLE
```

To access the global SAMPLE mapped to the defined namespace MARKETING:

```objectscript
   Set x = ^|"MARKETING"|SAMPLE
```

You can use an implied namespace to access the global SAMPLE in the directory `C:\BUSINESS\` on your local system:

```objectscript
   Set x = ^|"^^C:\BUSINESS\"|SAMPLE
```

You can use an implied namespace to access the global SAMPLE in the directory `C:\BUSINESS` on a remote system named SALES:

```objectscript
   Set x = ^|"^SALES^C:\BUSINESS\"|SAMPLE
```

To access the process-private global SAMPLE:

```objectscript
   Set x = ^||SAMPLE
   Set x=^|"^"|SAMPLE
```

## See Also

*   Introduction to Globals
    
*   Process-Private Globals
