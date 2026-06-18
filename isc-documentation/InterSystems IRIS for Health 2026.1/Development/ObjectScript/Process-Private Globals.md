# Process-Private Globals

An ObjectScript process-private global is a variable that is only accessible by the process that created it. When the process ends, all of its process-private globals are deleted.

Process-private globals are written to the `IRISTEMP` database. In contrast to global variables, InterSystems IRIS does not treat a SET or KILL of a local variable or a process-private global as a journaled transaction event; rolling back the transaction has no effect on these operations.

## Introduction

A process-private global has the following characteristics:

*   Process-specific: a process-private global can only be accessed by the process that created it, and it ceases to exist when the process completes. This is similar to local variables.
    
*   Always public: a process-private global is always a public variable. This is similar to global variables.
    
*   Namespace-independent: a process-private global is accessible from all namespaces.
    
*   Unaffected by argumentless `KILL`, `NEW`, `WRITE`, or `ZWRITE`. A process-private global can be specified as an argument to `KILL`, `WRITE`, or `ZWRITE`. This is similar to global variables.
    

## Naming Conventions

A process-private global name takes one of the following forms:

```
^||name
^|"^"|name
^["^"]name
^["^",""]name
```

These four prefix forms are equivalent, and all four refer to the same process-private global. The first form (^||name) is the most common, and the one recommended for new code. The second, third, and fourth forms are provided for compatibility with existing code that defines globals.

Apart from the prefix, process-private globals use the same naming conventions as regular globals, as given in Rules and Guidelines for Identifiers. Briefly:

*   The first character (after the second vertical bar) must be either a letter or the percent (%) character.
    
    Process-private variable names starting with `%` are known as “percent variables” and have different scoping rules. In your code, for these variables, start the name with `%Z` or `%z`; other names are reserved for system use. For example: `^||%zmyvar`.
    
*   Unlike local variables, no global name (including process-private globals) can contain Unicode letters — letter characters above ASCII 255. Attempting to include a Unicode letter in a process-private global name results in a <WIDE CHAR> error.
    
*   All variable names are case-sensitive, and this includes process-private global names.
    
*   A process-private global name must be unique within its process.
    
*   Unlike local variables, process-private global names are limited to 31 characters, exclusive of the prefix characters. You may specify a name longer than 31 characters, but only the first 31 characters are used. Therefore, a process-private global name must be unique within its first 31 characters.
    
*   Like other variables, process-private globals can take subscripts.
    

## Listing Process-Private Globals

You can use the `^$||GLOBAL()` syntax form of ^$GLOBAL() to return information about process-private globals belonging to the current process.

You can use the `^GETPPGINFO` routine to display the names of all current process-private globals and their space allocation, in blocks. `^GETPPGINFO` does not list the subscripts or values for process-private globals. You can display process-private globals for a specific process by specifying its process Id (pid), or for all processes by specifying the "*" wildcard string. You must be in the %SYS namespace to invoke `^GETPPGINFO`.

The following example uses `^GETPPGINFO` to list the process-private globals for all current processes:

```objectscript
  SET ^||flintstones(1)="Fred"
  SET ^||flintstones(2)="Wilma"
  NEW $NAMESPACE
  SET $NAMESPACE="%SYS"
  DO ^GETPPGINFO("*")
```

The `^GETPPGINFO` routine takes arguments as follows:

```objectscript
 do ^GETPPGINFO("pdf","options","outfile")
```

These arguments are as follows:

*   `pdf` can be a process Id or the * wildcard.
    
*   `options` can be a string containing any combination of the following characters:
    
    *   `b` (return values in bytes)
        
    *   `Mnn` (list only processes with process-private globals that use `nn` or more blocks)
        
        Use `M0` to include processes without any process-private globals in the listing.
        
        Use `M1` to exclude processes without any process-private globals from the listing, but include processes having only a global directory block. (This is the default.)
        
        Use `M2` to exclude processes without any process-private globals from the listing, as well as those having only a global directory block.
        
    *   `S` (suppress screen display; used with `outfile`)
        
    *   `T` (display process totals only).
        
*   `outfile` is the file path for a file in CSV (comma-separated values) format that will be used to receive `^GETPPGINFO` output.
    

The following example writes process-private globals to an output file named `ppgout`. The S option suppresses screen display; the M500 option limits output to only processes with process-private globals that use 500 or more blocks:

```objectscript
  NEW $NAMESPACE
  SET $NAMESPACE="%SYS"
  DO ^GETPPGINFO("*","SM500","/home/myspace/ppgout")
```

You can also query the %SYS.ProcessQuery table for information on process-private globals. For example:

```sql
SELECT PID, Routine, PrivateGlobalBlockCount
       FROM %SYS.ProcessQuery
       WHERE PrivateGlobalBlockCount>0
       ORDER BY PrivateGlobalBlockCount DESC
```

## See Also

*   Variables in ObjectScript
    
*   Multidimensional Arrays
