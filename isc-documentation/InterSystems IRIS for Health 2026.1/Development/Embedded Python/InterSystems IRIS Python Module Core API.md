# InterSystems IRIS Python Module Core API

This section provides API documentation for the core functions of the InterSystems IRIS Python Module. These functions allow you to access InterSystems IRIS classes and methods, use the transaction processing capabilities of InterSystems IRIS, and perform other core InterSystem IRIS tasks.

## Summary

The following table summaries the core functions of the iris module. To use this module from Embedded Python, use `import iris`.

<table><tr><th>Group</th><th>Functions</th></tr><tr><td>Code Execution</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_check_status">check_status()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_execute">execute()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_routine">routine()</a></td></tr><tr><td>Locking and Concurrency Control</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_lock">lock()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_unlock">unlock()</a></td></tr><tr><td>Reference Creation</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_arrayref">arrayref()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_cls">cls()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_gref">gref()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_ref">ref()</a>,</td></tr><tr><td>Transaction Processing</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_tcommit">tcommit()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_tlevel">tlevel()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_trollback">trollback()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_trollbackone">trollbackone()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_core#GEPYTHON_reference_core_tstart">tstart()</a>,</td></tr></table>

See Transaction Processing for information on using transactions to maintain the logical integrity of your InterSystems IRIS database.

## arrayref(dictionary)

Creates an ObjectScript array from a Python dictionary and returns a reference to the array.

Assume you have an InterSystems IRIS class called `User.ArrayTest` that has the following ObjectScript methods that expect an array as an argument:

```
ClassMethod WriteContents(myArray) [ Language = objectscript ]
{
    zwrite myArray
}

ClassMethod Modify(myArray) [ Language = objectscript ]
{
    set myArray("new") = 123
    set myArray("x","y","z") = "xyz"
}

ClassMethod StoreGlobal(myArray)  [ Language = objectscript ]
{
    kill ^MyGlobal
    if '$data(myArray) return "no data"
    merge ^MyGlobal = myArray
    return "ok"
}
```

The method `WriteContents()` writes the contents of the array, `Modify()` modifies the contents of the array, and `StoreGlobal()` takes the contents of the array and stores it in the global `^MyGlobal`.

From Python, you can create a dictionary `mydict` and use `iris.arrayref()` to place its contents in an ObjectScript array and return a reference to that array. Then you can pass that reference to the three methods in `User.ArrayTest`.

```
>>> mydict = {2:{3:4}}
>>> mydict
{2: {3: 4}}
>>> a = iris.arrayref(mydict)
>>> a.value
{2: {3: 4}}
>>> iris.User.ArrayTest.Modify(a)
>>> iris.User.ArrayTest.WriteContents(a)
myArray(2,3)=4
myArray("new")=123
myArray("x","y","z")="xyz"
>>> iris.User.ArrayTest.StoreGlobal(a)
'ok'
```

Then, from ObjectScript, you can verify that global `^MyGlobal` now contains the same data as the array did:

```objectscript
USER>zwrite ^MyGlobal
^MyGlobal(2,3)=4
^MyGlobal("new")=123
^MyGlobal("x","y","z")="xyz"
```

For information on ObjectScript arrays, see Multidimensional Arrays.

## check_status(status)

Raises an exception if `status` contains an error. Returns None if no error condition occurs.

If you have an InterSystems IRIS class `Sample.Company` that has a `Name` property that is required, trying to save an instance of that class without a `Name` property results in an error status. The following example uses `iris.check_status()` to check the status returned by the `_Save()` method and throws an exception if it contains an error.

```
>>> mycompany = iris.Sample.Company._New()
>>> mycompany.TaxID = '123456789'
>>> try:
...     status = mycompany._Save()
...     iris.check_status(status)
... except Exception as ex:
...     print(ex)
...
ERROR #5659: Property 'Sample.Company::Name(4@Sample.Company,ID=)' required
```

## cls(class_name)

Returns a reference to an InterSystems IRIS class. This allows you access the properties and methods of that class in the same way you would a with a Python class. You can use `iris.cls()` to access both built-in InterSystems IRIS classes or custom InterSystems IRIS classes you write yourself.

The following example uses `iris.cls()` to return a reference to the built-in InterSystems IRIS class %SYS.System. It then calls its `GetInstanceName()` method.

```
>>> system = iris.cls('%SYS.System')
>>> print(system.GetInstanceName())
IRIS2023
```

> **Note:**
> 
> Effective with InterSystems IRIS 2024.2, an optional shorter syntax for referring to an InterSystems IRIS class from Embedded Python has been introduced. Either the new form or the traditional form are permitted.

## execute(statements)

Executes an ObjectScript statement and optionally returns a value.

The following example uses `iris.execute()` to write the value of `$HOROLOG`, an ObjectScript special value that contains the current local date and time in the internal InterSystems IRIS format.

```
>> iris.execute('write $horolog,!')
66682,45274
```

The following example returns the value of `$HOROLOG`, converted to a human-readable string by the ObjectScript `$ZDATE` function.

```
>>> today = iris.execute('return $zdate($horolog)')
>>> print(today)
07/27/2023
```

## gref(global_name)

Returns a reference to an InterSystems IRIS global. The global may or may not already exist.

The following example uses `iris.gref()` to set variable `day` to a reference to global `^day`.

```
>>> day = iris.gref('^day')
```

The next example prints the value stored at `^day(1, "name")`, and since no value is currently stored for those keys, it prints None. Next it stores the value `"Sunday"` at that location and retrieves and prints the stored value.

```
>>> print(day[1, 'name'])
None
>>> day[1, 'name'] = 'Sunday'
>>> print(day[1, 'name'])
Sunday
```

For information on the methods that can be used on an InterSystems IRIS global reference, see Global Reference API.

For background information on globals, see Introduction to Globals.

## lock(lock_list, timeout_value, locktype)

Sets locks, given a list of lock names, an optional timeout value (in seconds), and an optional lock type. If `locktype` is `"S"`, this indicates a shared lock.

In InterSystems IRIS, a lock is used to prevent more than one user or process from accessing or modifying the same resource (usually a global) at the same time. For example, a process that writes to a resource should request an exclusive lock (the default) so that another process does not attempt to read or write to that resource simultaneously. A process that reads a resource can request a shared lock so that other processes can read that resource at the same time, but not write to that resource. A process can specify a timeout value, so that it does not wait forever waiting for a resource to become available.

The following example uses `iris.lock()` to request exclusive locks on locks named `^one` and `^two`. If the request is successful, the call returns True.

```
>>> iris.lock(['^one','^two'])
True
```

If another process then requests a shared lock on `^one`, and the first process does not release the lock within 30 seconds, the call below returns False.

```
>>> iris.lock(['^one'],30,'S')
False
```

A process should use unlock() to relinquish locks when the resources they protect are no longer being used.

For more information on how locks are used in InterSystems IRIS, see Locking and Concurrency Control.

## ref(value)

Creates an iris.ref object with a specified value. This is useful for situations when you need to pass an argument to an ObjectScript method by reference.

The following example uses `iris.ref()` to create an iris.ref object with the value 2000.

```
>>> calories = iris.ref(2000)
>>> calories.value
2000
```

Assume an InterSystems IRIS class `User.Diet` has a method called `Eat()` that takes as arguments the name of a food you’re about to consume and your current calorie count for the day, and that `calories` is passed in by reference and is updated with your new calorie count. The following example shows that after the call to `Eat()`, the value of the variable calories has been updated from 2000 to 2250.

```
>>> iris.User.Diet.Eat('hamburger', calories)
>>> calories.value
2250
```

For information on passing arguments by reference in ObjectScript, see Indicating How Arguments Are to Be Passed.

## routine(routine, args)

Invokes an InterSystems IRIS routine, optionally at a given tag. Any arguments that need to be passed in the call are comma-delimited, following the name of the routine.

The following example, when run in the `%SYS` namespace, uses `iris.routine()` to call the routine `^SECURITY`:

```
>>> iris.routine('^SECURITY')

1) User setup
2) Role setup
3) Service setup
4) Resource setup
.
.
.
```

If you have a routine `^Math` that has a function `Sum()` that adds two numbers, the following example adds 4 and 3:

```
>>> sum = iris.routine('Sum^Math',4,3)
>>> sum
7
```

For more information on how routines are called in ObjectScript, see Invoking Code and Passing Arguments.

## tcommit()

Marks the successful end of an InterSystems IRIS transaction.

Use `iris.tcommit()` to mark the successful end of a transaction and decrement the nesting level by 1:

```
>>> iris.tcommit()
```

To ensure that transactions nest properly, every `iris.tstart()` should be paired with an `iris.tcommit()`.

If `iris.tcommit()` is called when not in a transaction, an exception occurs, with the value `<COMMAND>`.

See also tstart(), tlevel(), trollback(), and trollbackone().

## tlevel()

Detects whether a transaction is currently in progress and returns the nesting level. A call to `iris.tstart()` increments the nesting level, and a call to `iris.tcommit()` decrements the nesting level. A value of zero means not in a transaction.

The following example shows the value returned by `iris.level()` at different transaction nesting levels.

```
>>> iris.tlevel()
0
>>> iris.tstart()
>>> iris.tstart()
>>> iris.tlevel()
2
>>> iris.tcommit()
>>> iris.tlevel()
1
```

See also tstart(), tcommit(), trollback(), and trollbackone().

## trollback()

Rolls back all current transactions in progress and restores all journaled database values to their values at the start of the initial transaction. It also resets the transaction nesting level to 0.

This simple example initializes the global `^a(1)` to the value “hello.” It then starts a transaction and sets `^a(1)` to the value “goodbye.” But before the transaction is committed, it calls `iris.trollback()`. This resets the transaction nesting level to 0 and restores `^a(1)` to the value it had before the start of the transaction.

```
>>> a = iris.gref('^a')
>>> a[1] = 'hello'
>>> iris.tstart()
>>> iris.tlevel()
1
>>> a[1] = 'goodbye'
>>> iris.trollback()
>>> iris.tlevel()
0
>>> a[1]
'hello'
```

See also tstart(), tcommit(), tlevel(), and trollbackone().

## trollbackone()

Rolls back the current level of nested transactions, that is, the one initiated by the most recent `iris.tstart()`. It also decrements the transaction nesting level by 1.

This example initializes the global `^a(1)` to the value 4 and `^b(1)` to the value “lemon.” It then starts a transaction and sets `^a(1)` to 9. Next, it starts a nested transaction and sets `^b(1)` to “lime.” It then calls `iris.trollbackone()` to roll back the inner transaction and calls `iris.commit()` to commit the outer transaction. When all is said and done, `^a(1)` retains its new value, while `^b(1)` is rolled back to its original value.

```
>>> a = iris.gref('^a')
>>> b = iris.gref('^b')
>>> a[1] = 4
>>> b[1] = 'lemon'
>>> iris.tstart()
>>> iris.tlevel()
1
>>> a[1] = 9
>>> iris.tstart()
>>> iris.tlevel()
2
>>> b[1] = 'lime'
>>> iris.trollbackone()
>>> iris.tlevel()
1
>>> iris.tcommit()
>>> iris.tlevel()
0
>>> a[1]
9
>>> b[1]
'lemon'
```

See also tstart(), tcommit(), tlevel(), and trollback().

## tstart()

Marks the start of an InterSystems IRIS transaction.

A transaction is a group of commands that must all complete in order for the transaction to be considered successful. For example, if you have a transaction that transfers a sum of money from one bank account to another, the transaction is only successful if withdrawing the money from the first account and depositing it into the second account are both successful. If the transaction fails, the database can be rolled back to the state it was in before the start of the transaction.

Use `iris.start()` to mark the start of a transaction and increment the transaction nesting level by 1:

```
>>> iris.tstart()
```

See also tcommit(), tlevel(), trollback(), and trollbackone().

For more information on how transaction processing works in InterSystems IRIS, see Transaction Processing.

## unlock(lock_list, timeout_value, locktype)

Removes locks, given a list of lock names, an optional timeout value (in seconds), and an optional lock type.

If your code sets locks to control access to resources, it should unlock them when it is done using those resources.

The following example uses `iris.unlock()` to unlock the locks named `^one` and `^two`.

```
>>> iris.unlock(['^one','^two'])
True
```

See also lock().
