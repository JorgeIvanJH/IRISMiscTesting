# Creating Test Cases: The %UnitTest.TestCase Class

This is the general workflow to set up unit tests using the `%UnitTest` framework:

1.  Extend the %UnitTest.TestCase class, adding one test method for each method to be tested. Test method names must begin with the word `Test`. See Extending the %UnitTest.TestCase Class.
    
2.  A single test method can contain multiple tests. Typically a test method will contain one test for each aspect of the method to be tested. Within each test method, devise one or more tests using the $$$AssertX macros. Typically, the macro will call the method to be tested, comparing its output to some expected value. If the expected value matches the macro output, the test will be considered successful. See Macros of the %UnitTest.TestCase Class.
    
3.  Add code to the preparation and cleanup methods to perform needed tasks. For example, if a test seeks to delete an element from a list, that list must first exist and it must contain the element to be deleted. See %UnitTest.TestCase Class Preparation and Cleanup Methods.
    
    > **Note:**
    > 
    > Preparation methods and cleanup methods are also often called setup methods and teardown methods.
    

## Extending the %UnitTest.TestCase Class

Create a class that extends %UnitTest.TestCase to contain the test methods that execute your unit tests. This process is designed to be flexible, to accommodate your particular testing needs.

Most likely, you will add test methods, and you might add properties as well. Test methods will be executed by the `RunTest()` method from the %UnitTest.Manager class, which looks for and executes methods whose names begin with ‘Test’. You can add other helper methods to your class, but a method will be run as a unit test when you call `RunTest()` only if its name begins with ‘Test’.

> **Note:**
> 
> Test methods are executed in alphabetical order, so, for example, `TestAssess()` would be executed before `TestCreate()`.

Within a test method, create one or more tests. Use an $$$AssertX macro for each test. See Macros of the %UnitTest.TestCase Class for details about $$$AssertX macros.

You may decide to create a test method for each class method you wish to test. For example, suppose your class `MyPackage.MyClassToBeTested` contains a method `Add()`, which calls for multiple tests — you might want to create test method `MyTests.TestAdd()` to contain the code that executes the needed tests.

You may also wish to test object instances. In this case, you would create a method like `MyTests.TestMyObject()`, which could contain tests to make sure the object’s properties and functionality are correct.

In addition to creating test methods, you may wish to create properties in your extended class. This enables your test methods to share information. Consider the following points when adding properties:

*   Declare your custom properties in the class itself.
    
*   Set the properties by adding code to the preparation methods `OnBeforeOneTest()` and `OnBeforeAllTests()`, using `..<property>` syntax.
    
*   Access the properties by adding code to your test methods and/or to the cleanup methods `OnAfterOneTest()` and `OnAfterAllTests()`, using `..<property>` syntax.
    
    > **Note:**
    > 
    > For example, if your custom property is called `PropertyValue`, you would set it or access it using `..PropertyValue`.
    

### Example: Extended %UnitTest.TestCase Class

```objectscript
Class MyPackage.MyClassToBeTested
{
  ClassMethod Add (Addend1 as %Integer, Addend2 as %Integer) As %Integer
  {
    Set Sum = Addend1 + Addend2
    Return Sum
  }
}

Class MyPackage.MyTests Extends %UnitTest.TestCase
{
  Method TestAdd()
  {
    do $$$AssertEquals(##class(MyPackage.MyClassToBeTested).Add(2,3),5, "Test 2+3=5")
    do $$$AssertNotEquals(##class(MyPackage.MyClassToBeTested).Add(3,4),5, "Test 3+4 '= 5")
  }
}
```

## Macros of the %UnitTest.TestCase Class

Within each of your test methods, use one of the following `$$$AssertX` macros to test each testable aspect of the class method. For example, if a test method is designed to test the `Add()` method, it might contain a test, using `$$$AssertEquals`, to ensure that it adds 2+3 equals 5, and a second test, using `$$$AssertNotEquals`, to ensure that it does not add 3+4 equals 5.

Select the macro that best matches the desired test outcome. Another way to think of this principle is to write your test from the perspective that the assertion succeeds. If you expect two values to be equal, use `$$$AssertEquals`; if you expect the values not to be equal, use `$$$AssertNotEquals`.

A test fails if the specified `$$$AssertX` macro returns false; otherwise the test passes.

The `$$$AssertX` macros can take the following arguments:

*   `arg1` — Typically either the output from the method being tested or a value calculated from that output.
    
*   `arg2` — When present, a value compared by the macro to `arg1`.
    
*   `test_description` — A string that appears in the displayed test outcome listing, and describes what the macro has tested. This has no effect on the outcome of the test. Don’t forget that this argument can include concatenations, variables, and methods. For example, its value could be:
    
    ```
    “Failed to create” _ maxObjects _ "objects: " _ $system.Status.GetErrorText(status)
    ```
    

### `$$$AssertEquals (arg1, arg2, test_description)`

Returns true if `arg1` and `arg2` are equal.

```
do $$$AssertEquals (##class(MyPackage.MyClassToBeTested).Add(2,3), 5, “Test Add(2,3) = 5”)
```

### `$$$AssertNotEquals (arg1, arg2, test_description)`

Returns true if `arg1` and `arg2` are not equal.

```
do $$$AssertNotEquals (##class(MyPackage.MyClassToBeTested).Add(3,4), 5, "Test Add(3,4) '= 5")
```

### `$$$AssertStatusOK (arg1, test_description)`

Returns true if the returned status code is 1.

```
do $$$AsserStatusOK(##class(MyPackage.MyClassToBeTested).SaveContact(valid_contact_ID),
          "Test that valid contact is saved")
```

### `$$$AssertStatusNotOK (arg1, test_description)`

Returns true if the returned status code is not 1.

```
do $$$AssertStatusNotOK(##class(MyPackage.MyClassToBeTested).SaveContact(invalid_contact_ID),
          "Test that invalid contact is not saved")
```

### `$$$AssertTrue (arg1, test_description)`

Returns true if the expression is true.

```
do $$$AssertStatusTrue(##class(MyPackage.MyClassToBeTested).IsContactValid(valid_contact_ID),
          "Test that valid contact is valid")
```

### `$$$AssertNotTrue (arg1, test_description)`

Returns true if the expression is not true.

```
do $$$AssertStatusNotTrue(##class(MyPackage.MyClassToBeTested).IsContactValid(invalid_contact_ID),
          "Test that invalid contact is not valid")
```

### `$$$AssertFilesSame (arg1, arg2, test_description)`

Returns true if two files are identical.

```
do $$$AssertFilesSame(##class(MyPackage.MyClassToBeTested).FetchFile(URL), control_file,
          "Test that fetched file is identical to control file")
```

### `$$$AssertFilesSQLUnorderedSame (arg1, arg2, test_description)`

Returns true if two files containing SQL query results contain the same unordered results.

```
do $$$AssertFilesSQLUnorderedSame(output.log,reference.log,"Comparing output.log to reference.log")
```

### `$$$AssertSuccess(test_description)`

Unconditionally log success. This assertion is intended to replace the convention of passing 1 to `$$$AssertTrue`

### `$$$AssertFailure(test_description)`

Unconditionally log failure. This assertion is intended to replace the convention of passing 0 to `$$$AssertTrue`.

### `$$$AssertSkipped(test_description)`

Logs a message that the test has been skipped for the reason described in `test_description`. This might be used, for instance, if the preconditions for a test have not been met.

> **Note:**
> 
> `OnBeforeAllTests()` does not support this macro. Calls to `$$$AssertSkipped` in `OnBeforeAllTests()` could result in false positives.

### `$$$LogMessage (message)`

Writes the value of `message` as a log entry, independent of any particular test. This can, for instance, be very useful for providing context and organization in your log.

```
do $$$LogMessage("-- ALL TEST OBJECTS CREATED -- ")
```

> **Note:**
> 
> For the latest list of macros, see %UnitTest.TestCase in the Class Reference.

## %UnitTest.TestCase Class Preparation and Cleanup Methods

### OnBeforeOneTest()

Executes immediately before each test method in the test class.

### OnBeforeAllTests()

Executes only once, before any test methods in the test class.

### OnAfterOneTest()

Executes immediately after each test method in the test class.

### OnAfterAllTests()

Executes only once, after all of the test methods in the test class have executed.

### Example: Preparation Method

The code in this method will execute once, before execution of the test suite. It creates a single contact for use during testing. To execute preparation tasks multiple times, once before each test in the suite, add code to `OnBeforeOneTest()` instead.

```
Method OnBeforeAllTests()
{
  Do ##class(MyPackage.Contact).Populate(1)
  Return $$$OK
}
```

### Example Cleanup Method

The code in this method will execute once, after execution of the entire test suite. It kills all contacts in the extent once testing is complete. To execute cleanup tasks multiple times, once after each test in the suite, add code to `OnAfterOneTest()` instead.

```
Method OnAfterAllTests()
{
  Do ##class(MyPackage.Contact).%KillExtent()
  Return $$$OK
}
```
