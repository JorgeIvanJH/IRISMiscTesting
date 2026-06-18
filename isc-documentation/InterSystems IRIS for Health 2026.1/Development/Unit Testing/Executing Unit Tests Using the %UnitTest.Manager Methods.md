# Executing Unit Tests Using the %UnitTest.Manager Methods

Launch tests using the methods included in the %UnitTest.Manager class.

This is the general workflow to execute unit tests using the `%UnitTest` framework:

1.  Inform the system where to find your tests by setting the `^UnitTestRoot` global:
    
    ```objectscript
    USER>set ^UnitTestRoot = "C:\UnitTests"
    ```
    
2.  Execute your tests, using the `RunTest()` or `DebugRunTestCase()` method of the %UnitTest.Manager class:
    
    ```objectscript
    USER>do ##class(%UnitTest.Manager).RunTest("MyTests")
    ```
    
    > **Note:**
    > 
    > Test execution will stop if any of the following system errors occur: `INTERRUPT`, `FILEFULL`, `DISKHARD`, `DATABASE`, `SYSTEM`, `STORE`, `EXTERNALINTERRUPT`, `ALARM`, `DSKFUL`. When these errors occur, the system is in a troubled state, and any other processing is suspect.
    
3.  View the results of your tests.
    

> **Note:**
> 
> By default, `RunTest()` loads any test classes it finds within the `^UnitTestRoot` directory, compiles them, executes any tests they contain, and deletes them from memory.
> 
> However, this may not be the most efficient paradigm when you are developing your code. That is, you may not want to reload and recompile your tests every time you make a small change to the method being tested. As a result, unit test classes are often stored externally. You can use the arguments of the RunTest() method to explicitly control whether to load tests and from where, whether to delete them, and other considerations.

## %UnitTest Test Execution Methods

The default behavior when running unit tests is for the tests to be loaded into InterSystems IRIS, compiled, executed, and then deleted. This prevents test code from cluttering your InterSystems IRIS namespace. To deviate from this default behavior, you can either use `DebugRunTestCase()` or you can add flags to the `qualifiers` argument of either of these methods. For example, you may want to develop your test cases locally, within your namespace, without having to reload them every time you make a change. In that case, you could pass the `/nodelete` flag as part of the `qualifiers` argument.

### RunTest (“testSpec”, “qualifiers”, “userparam”)

Executes a test or set of tests within the directory specified in the global `^UnitTestRoot`. Once tests are executed, deletes from InterSystems IRIS all loaded tests and test classes.

```objectscript
USER>Do ##class(%UnitTest.Manager).RunTest("MyTests")
```

See RunTest() in the class reference for a detailed description of how to use this method and its arguments.

### DebugRunTestCase (“testSpec”, “qualifiers”, “userparam”)

Executes a test or set of tests without loading or deleting any test classes.

```objectscript
USER>Do ##class(%UnitTest.Manager).DebugRunTestCase("MyTests", "/display=none/debug", "/log")
```

See DebugRunTestCase() in the class reference for more information.

> **Note:**
> 
> Occasionally, one of your unit tests may change the value of a SQL Configuration Option (such as `AutoParallel` or `AutoParallelThreshold`, for example) or may leave behind a lock or an open transaction or similar, triggering an error notification that states the problem. The unit test manager, %UnitTest.Manager, automatically resets the value of the changed SQL Configuration Option, deletes the leftover lock, or closes the transaction before executing the next unit test.
