# IRIS System API

This section provides documentation for the classes in the `system` package of the InterSystems IRIS Python Module. These classes allow you to access some common System API classes in the InterSystems IRIS `%SYSTEM` package.

## Summary

The following table summaries the classes of the `system` package of the InterSystems IRIS Python Module. To access these classes from Embedded Python, use `iris.system.<classname>`.

<table><tr><th>Class</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_system#GEPYTHON_reference_system_docdb">DocDB</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_system#GEPYTHON_reference_system_encryption">Encryption</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_system#GEPYTHON_reference_system_error">Error</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_system#GEPYTHON_reference_system_event">Event</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_system#GEPYTHON_reference_system_monitor">Monitor</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_system#GEPYTHON_reference_system_process">Process</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_system#GEPYTHON_reference_system_sql">SQL</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_system#GEPYTHON_reference_system_sys">SYS</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_system#GEPYTHON_reference_system_security">Security</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_system#GEPYTHON_reference_system_semaphore">Semaphore</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_system#GEPYTHON_reference_system_status">Status</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_system#GEPYTHON_reference_system_util">Util</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_system#GEPYTHON_reference_system_version">Version</a></td></tr></table>

This summary of the classes in the `iris.system` package does not attempt to document all of the methods available in each class, some of which number in the dozens. For information how to find complete documentation on InterSystems IRIS classes, see Locating and Exploring Class Reference Documentation.

> **Note:**
> 
> You can access `%SYSTEM` classes not included in `iris.system` by using the InterSystems IRIS class directly. For example, list all InterSystems IRIS classes in the current namespace by using the command `iris._SYSTEM.OBJ.ShowClasses()`.

## DocDB

The %SYSTEM.DocDB class provides an interface for managing Document Databases.

The following example uses the `Exists()` method of the `iris.system.DocDB` class to check for the existence of a document database called `People`. Not finding the database, it then uses the `CreateDatabase()` method to create it:

```
>>> iris.system.DocDB.Exists('People')
0
>>> db = iris.system.DocDB.CreateDatabase('People')
>>> iris.system.DocDB.Exists('People')
1
```

For more information, see Introducing InterSystems IRIS Document Database.

## Encryption

The %SYSTEM.Encryption class provides class functions to perform data encryption, Base64 encoding, hashing, and generation of message authentication codes.

The following example uses the `ListEncryptionKeys()` method of the `iris.system.Encryption` class to list the key IDs of all active encryption keys, which can be used for data element encryption for applications.

```
>>> iris.system.Encryption.ListEncryptionKeys()
'1E5C9E0D-1257-4707-8864-3428E17A6FCE'
```

The following example uses the `CreateEncryptionKey()` method to create a 32-byte (256–bit) encryption key. The method returns the key ID of the generated encryption key. Creating and activating keys need to be done in the `%SYS` namespace.

```
>>> iris.system.Process.SetNamespace('%SYS')
'%SYS'
>>> st = iris.ref('')
>>> iris.system.Encryption.CreateEncryptionKey('c:\\temp\\mykeyfile.txt','<username>','<password>',32,st)
'C861F668-435A-4AE8-A302-FBD4ED528432'
>>> st.value
1
```

The `CreateEncryptionKey()` method passes back a %Status by reference in the last argument, so the example above uses `iris.ref()` to create a reference to the variable `st`. Access the `value` property of `st` to retrieve the actual status.

The following example uses the `ActivateEncryptionKey()` method to activate the encryption key created in the previous example. Then it calls `ListEncryptionKeys()` again to show it is now active.

```
>>> status = iris.system.Encryption.ActivateEncryptionKey('c:\\temp\mykeyfile.txt','<username>','<password>')
>>> status
1
>>> iris.system.Encryption.ListEncryptionKeys()
'1E5C9E0D-1257-4707-8864-3428E17A6FCE,C861F668-435A-4AE8-A302-FBD4ED528432'
```

For more information on using encryption in InterSystems IRIS, see Encryption.

## Error

The %SYSTEM.Error class is a generic error container used to return error information reported from various sources, in various different forms. The class has properties that can store a %Status, a $ZERROR code, a SQLCODE, and/or a free text message. It can also contains methods that convert a %SYSTEM.Error to an InterSystems IRIS exception and vice-versa.

The following example shows how to create a new generic error object from a %Status, after trying to create and save an object of an InterSystems IRIS class called `Sample.Company`:

```
>>> my_company = iris.Sample.Company._New()
>>> my_company.TaxID = '123456789'
>>> status = myCompany._Save()
>>> e = iris.system.Error._New(status)
>>> print(e.Message)
ERROR #5659: Property 'Sample.Company::Name(8@Sample.Company,ID=)' required
```

For more information, see iris.system.Status, Working with %Status Values, $ZERROR (ObjectScript), and SQL Error Messages.

## Event

The %SYSTEM.Event class provides an interface to the Event API. It allows processes to go to sleep waiting for a particular resource, which can be a named resource or a process ID. The `Wait()` method of the `iris.system.Event` class causes a process to wait on a resource, while the `Signal()` method wakes up a process waiting for a resource.

A named resource is a string representation of a valid identifier, much the same as that used for locks. Named resources are explicitly created and deleted, using the `Create()` and `Delete()` methods respectively.

A process ID is automatically created when a process is created and automatically deleted when a process exits. A process may wait only on its own process identifier.

In the following example, a process creates a named resource called `MyResource` by using the `Create()` method of `iris.system.Event`:

```
>>> iris.system.Event.Create('MyResource')
1
```

A second process can then use the `Wait()` method of `iris.system.Event` to wait on this resource before continuing, as shown in this Python module, `waiter.py`:

```
import iris

def run():
    print('Waiting for signal')
    ret = iris.system.Event.Wait('MyResource',30)
    if ret == 1:
        print('Signal received')
    elif ret == -1:
        print('Resource deleted')
    elif ret == 0:
        print('Wait timed out')
```

The `run()` function of the `waiter` module prints “Waiting for signal,” and then calls the `Wait()` method of `iris.system.Event`. It then waits up to 30 seconds for `MyResource` to become available before continuing along one of three paths, depending on the return value of the `Wait()` method.

If the first process then uses the `Signal()` method of the `iris.system.Event` class, it wakes up the second process:

```
>>> iris.system.Event.Signal('MyResource')
1
```

If no process is waiting for the resource, the wakeup is queued, and when another process waits for the resource, it is awakened immediately.

Executing the `run()` function of the `waiter` module might look something like this:

```
>>> import waiter
>>> waiter.run()
Waiting for signal
<process sleeps for up to 30 seconds>
Signal received
```

If the first process uses the `Delete()` method of the `iris.system.Event` class instead, the `run()` function prints “Resource deleted.”

If no response is received after 30 seconds, the output is “Wait timed out.”

For more information, see %SYSTEM.Event and iris.lock().

## Monitor

The %SYSTEM.Monitor class provides an interface for accessing the System Monitor, allowing you to perform such functions as getting the number of alerts posted to `messages.log`, reading the messages in `alerts.log`, or checking the system state.

The following example uses the `State()` method of the `iris.system.Monitor.State` class to return the current system state as an integer:

```
>>> iris.system.Monitor.State()
2
```

System states are determined by the number of system alerts posted to `messages.log` during or following startup. In this case, a system state of 2 means Alert (or RED). For further details on system states, see System Monitor Health State.

Use the `Alerts()` method to return the current number of system alerts:

```
>>> iris.system.Monitor.Alerts()
10
```

The following example (for InterSystems IRIS 2023.2 or later) calls the `GetAlerts()` method of the `iris.system.Monitor` class, which returns the number of alerts in `alerts.log`, the text of the alerts as an array of messages, and a string containing the text of the most recent alert:

```
>>> alerts = iris.ref(0)
>>> messages = iris.arrayref({})
>>> last_alert = iris.ref('')
>>> status = iris.system.Monitor.GetAlerts(alerts, messages, last_alert)
>>> for x in range(1, alerts.value + 1):
...    print(messages[x])
...
12/02/24-14:31:55:470 (68232) 2 [Generic.Event] Failed to allocate 1592MB shared memory using large pages.  Switching to small pages.
12/02/24-14:31:57:762 (56676) 2 [Utility.Event] Preserving journal files C:\InterSystems\IRIS\mgr\journal\20241128.002 and later for journal recovery and transaction rollback
12/03/24-06:29:54:435 (66624) 2 [Utility.Event] LMF Error:  Could not send startup message to license server
12/03/24-19:48:32:895 (66624) 2 [Utility.Event] LMF Error:  Could not send startup message to license server
12/04/24-11:18:43:264 (66624) 2 [Utility.Event] LMF Error:  Could not send startup message to license server
12/04/24-12:41:12:897 (66624) 2 [Utility.Event] LMF Error:  Could not send startup message to license server
12/07/24-07:35:44:424 (66624) 2 [Utility.Event] LMF Error:  Could not send startup message to license server
12/10/24-00:52:38:787 (45112) 2 [Utility.Event] Preserving journal files c:\intersystems\iris\mgr\journal\20241207.002 and later for journal recovery and transaction rollback
12/10/24-05:42:01:245 (66624) 2 [Utility.Event] LMF error:  Could not connect to license server (127.0.0.1,4002).
12/10/24-15:29:54:916 (42260) 2 [Generic.Event] Process terminated abnormally (pid 13056, jobid 0x0002001b)
>>> last_alert.value
'12/10/24-15:29:54:916 (42260) 2 [Generic.Event] Process terminated abnormally (pid 13056, jobid 0x0002001b)'
```

The `GetAlerts()` method’s three arguments are all passed by reference, so it is necessary to use iris.ref() and iris.arrayref() to pass in references to the Python variables that will hold the returned results.

For more information, see Using System Monitor and Monitoring InterSystems IRIS Logs.

## Process

The %SYSTEM.Process class allows you to monitor and manipulate a process.

Some of the methods in `iris.system.Process` require a process ID (pid) to be passed as an argument, such as `State()`, which returns the current state of the process:

```
>>> iris.system.Process.State(8608)
'READ'
```

Some of its methods act upon the current process, such as `SetNamespace()`, which sets the namespace of the current process:

```
>>> iris.system.Process.SetNamespace('USER')
'USER'
```

Other methods work on either the current process or another process, such as `NameSpace()`, which returns the current namespace for a given process:

```
>>> iris.system.Process.NameSpace()
'USER'
>>> iris.system.Process.NameSpace(44828)
'%SYS'
```

For more information, see %SYSTEM.Process.

## SQL

The %SYSTEM.SQL class provides a mechanism for preparing and executing SQL queries. The key methods of `iris.system.SQL` are `Prepare()` and `Execute()`.

The following examples use the `Sample.Person` class described in Use an InterSystems IRIS Class.

The example below executes a SQL query that requests the name, age, and date of birth of the first 10 rows in the table `Sample.Person` and places the result set in the variable `rs1`:

```
>>> rs1 = iris.system.SQL.Execute('SELECT TOP 10 Name,Age,DOB FROM Sample.Person','DISPLAY')
```

The second argument in the call to `Execute()` is the SelectMode, which in this case tells the method to print the Display values of each field, rather than the Logical values. For example, a human-readable format for the DOB field will be used, rather than the internal `$HOROLOG` format.

The result set is an instance of the class %SQL.StatementResult, so you can manipulate the result set using the methods in that class, such as `%Display()` to print the contents of the result set:

```
>>> rs1._Display()
Name    Age     DOB
Avery,Zelda O.  40      05/13/1984
Quincy,Debby I. 48      06/11/1976
Schaefer,Barb G.        20      03/08/2005
Newton,Angela L.        46      05/30/1978
Thompson,Emily Y.       23      11/11/2001
O'Brien,James D.        71      10/12/1953
Baker,Valery F. 73      09/22/1951
Kratzmann,Frances T.    68      09/07/1956
Quixote,Janice I.       32      05/25/1992
Tsatsulin,Danielle P.   42      08/04/1982

10 Rows(s) Affected
```

The next example stores a similar query in a variable `q`:

```
q = iris.system.SQL.Prepare('SELECT TOP ? Name,Age,DOB FROM Sample.Person','DISPLAY')
```

The question mark in the query allows you to pass in an argument when you execute the query, in this case, specifying how many rows to place in the result set.

The query is an instance of the class %SQL.Statement, so you can manipulate the query using the methods in that class, such as `%Execute()` to run the query. This example requests the top 5 rows in the table and places the result set in the variable `rs2`.

```
>>> rs2 = q._Execute('5')
```

You can use the `%Next()` method of the of the class %SQL.StatementResult to iterate through the result set:

```
>>> while rs2._Next():
...    print(f'{rs2.Name} is {rs2.Age} years old and was born on {rs2.DOB}')
...
Avery,Zelda O. is 40 years old and was born on 05/13/1984
Quincy,Debby I. is 48 years old and was born on 06/11/1976
Schaefer,Barb G. is 20 years old and was born on 03/08/2005
Newton,Angela L. is 46 years old and was born on 05/30/1978
Thompson,Emily Y. is 23 years old and was born on 11/11/2001
```

For more information, see Using Dynamic SQL.

Use the `iris.sql` class to return a result set that can be iterated in a more Python-like way. See Use InterSystems SQL for more information.

## SYS

The %SYSTEM.SYS class provides a language-independent way to access selected system variables, also known as “special variables.”

The `Horolog()` method of the `iris.system.SYS` class gets the value of system variable `$HOROLOG`, which contains the local date and time in internal format. The first number is the current day, where day 1 is January 1, 1841, and the second number is the number of seconds since midnight of the current day. See $HOROLOG for details.

```
>>> iris.system.SYS.Horolog()
'67292,57639'
```

The `TimeStamp()` method gets the UTC date and time in internal format. See $ZTIMESTAMP for details.

```
>>> iris.system.SYS.TimeStamp()
'67292,72041.4628646'
```

Subtracting the number of seconds since midnight in the above examples indicates that the current time is 4 hours behind UTC.

The `TimeZone()` method retrieves the offset from the Greenwich meridian in minutes. See $ZTIMEZONE for details.

```
>>> iris.system.SYS.TimeZone()
300
```

This shows that the local time in this example is 5 time zones from the Greenwich meridian. This apparent discrepancy arises due to the fact that UTC is unaffected by daylight saving time or other time variants that may affect local time.

For more information, see %SYSTEM.SYS.

## Security

The %SYSTEM.Security class provides an interface for performing certain tasks related to user permissions.

For example, role escalation can be used when a user occasionally needs to perform certain functions that require a higher level of permissions than the user would normally have. This requires that the user already have the `%DB_IRISSYS:W` and `%Service_EscalateLogin:U` privileges.

You can check to see if a user has a particular privilege by using the `CheckUserPermission()` method of the `iris.system.Security` class, for example:

```
>>> iris.system.Security.CheckUserPermission('userone','%DB_IRISSYS')
'READ,WRITE'
>>> iris.system.Security.CheckUserPermission('userone','%Service_EscalateLogin')
'USE'
```

or

```
>>> iris.system.Security.CheckUserPermission('userone','%DB_IRISSYS','WRITE')
1
>>> iris.system.Security.CheckUserPermission('userone','%Service_EscalateLogin','USE')
1
```

The user also needs to have the role with the higher level of privilege defined as an escalation role. This can be configured in the Management Portal by going to `System` > `Security Management` > `Users` and selecting the user you wish to have an escalation role. Then click the `EscalationRoles` tab, where you can assign roles that the user can escalate to.

Then, to escalate the user to a new role, use the `EscalateLogin()` method. The following example escalates the current user to the `%Manager` role:

```
>>> iris.system.Security.EscalateLogin('%Manager')

Escalated Login for User: userone (Role: %Manager)
Password: *********

USER (%Manager)#
```

This drops you back to the ObjectScript shell with `%Manager` role. You can then execute commands in ObjectScript or re-enter the Python shell with the new level of permissions.

For more information, see Roles.

## Semaphore

The %SYSTEM.Semaphore class provides an interface for managing semaphores. Whereas a lock can be used to ensure that only one process can use a given resource, a semaphore can be used when multiple copies of a resource can exist. For example, you might want to allow a certain number of concurrent connections to a database, forcing an additional process to wait for a resource to become available.

The following sample module, `sem.py`, shows how semaphores can be used to regulate a process that generates a resource and a process that consumes a resource.

```
import time
import random
import iris

# Create a semaphore 'resource_sem' with a starting number of resources
def create(num_resources):
    my_sem = iris.system.Semaphore._New()
    my_sem.Create('resource_sem', num_resources)
    print(f'Created semaphore with value {my_sem.GetValue()}.')

# Return current value of semaphore 'resource_sem'
def value():
    my_sem = iris.system.Semaphore._New()
    my_sem.Open('resource_sem')
    return(my_sem.GetValue())

# Produce a resource and increment semaphore 'resource_sem'
def produce():
    my_sem = iris.system.Semaphore._New()
    my_sem.Open('resource_sem')
    time.sleep(random.uniform(4, 8))  # Insert some randomness
    my_sem.Increment(1)  # Increment semaphore
    print('Done producing.')

# Consume a resource and decrement semaphore 'resource_sem'
def consume():
    my_sem = iris.system.Semaphore._New()
    my_sem.Open('resource_sem')
    time.sleep(random.uniform(5, 10))  # Insert some randomness
    result = my_sem.Decrement(1, 10)  # Decrement semaphore with a 10-sec timeout
    if result == 0:
        print('Timed out waiting for semaphore.')
    else:
        print('Done consuming.')

# Delete semaphore 'resource_sem'
def delete():
    my_sem = iris.system.Semaphore._New()
    my_sem.Open('resource_sem')
    print(f'Deleting semaphore with value {my_sem.GetValue()}.')
    my_sem.Delete()
```

The function `create()` instantiates the `iris.system.Semaphore` class, uses the `Create()` method of that class to create a semaphore with the name `resource_sem` and set its initial value to `num_resources`. This semaphore can now be accessed by any process.

The `value()` function uses the `Open()` method of `iris.system.Semaphore` to open the semaphore with the name `resource_sem` and then uses the `GetValue()` method to retrieve the current value of the semaphore. This value represents the current number of resources that are waiting to be consumed.

The `produce()` function represents the production of a resource for later consumption and uses the `Increment()` method of `iris.system.Semaphore` to increment the value of the semaphore.

The `consume()` function represents the consumption of a resource and uses the `Decrement()` method of `iris.system.Semaphore` to decrement the value of the semaphore and indicate that a resource was consumed. If the method finds that the semaphore’s value is 0 at the time `Decrement()` is called, the method will wait up to 10 seconds for a resource to be produced.

Finally, the `delete()` function uses the `Delete()` method of `iris.system.Semaphore` to delete the semaphore.

When run in Terminal, the following example creates a the `num_resources` semaphore and assigns it the initial value 0, which means no resources are yet created. It then produces a resource and shows that the value of the semaphore is now 1, meaning that a resources is ready to be consumed.

```
>>> import sem
>>> sem.create(0)
Created semaphore with value 0.
>>> sem.produce()
Done producing.
>>> sem.value()
1
```

When run in a second Terminal session, the following example shows that you can retrieve the value of the semaphore. Since the value of the semaphore is 1, the process can consume the resource immediately and decrement the semaphore value.

```
>>> import sem
>>> sem.value()
1
>>> sem.consume()
Done consuming.
```

Now, the value of the semaphore is 0, and if a process tries to consume a resource, it will wait up to 10 seconds for a process to produce a new resource. If this happens, it will proceed and consume the resource. Otherwise, the call to `Decrement()` returns 0 to indicate it timed out.

```
>>> sem.value()
0
>>> sem.consume()
Timed out waiting for semaphore.
```

Since semaphores are shared objects, they do not go away unless you delete them explicitly by calling the `Delete()` method of `iris.system.Semaphore`.

```
>>> sem.delete()
Deleting semaphore with value 0.
```

The following sample module, `threads.py`, exercises the sample semaphore code in `sem.py` by spinning up threads for an equal number of producers and consumers.

```
# Driver takes starting number of resources
# And number of producer/consumer threads to run
def main(num_resources, num_threads):

    # Create semaphore with specified number of resources
    sem.create(num_resources)

    # Thread to produce a resource
    def start_producer(thread_id):
        print(f'Producer {thread_id} started. Semaphore value is {sem.value()}.')
        sem.produce()

    # Thread to consume a resource
    def start_consumer(thread_id):
        print(f'Consumer {thread_id} started. Semaphore value is {sem.value()}.')
        sem.consume()

   # Spawn multiple threads simulating concurrent producer/consumer requests
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=start_producer, args=(i,))
        time.sleep(2)
        threads.append(t)
        t.start()
        time.sleep(2)
        t = threading.Thread(target=start_consumer, args=(i,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
       t.join()

    # Clean up
    print(f"Exercise complete. Final semaphore value is {sem.value()}.")
    sem.delete()
```

The following example runs `threads.py`, with a starting semaphore value of 0 and spins up 5 producer threads and 5 consumer threads.

```
>>> import threads
>>> threads.main(0,5)
Created semaphore with value 0.
Producer 0 started. Semaphore value is 0.
Consumer 0 started. Semaphore value is 0.
Producer 1 started. Semaphore value is 0.
Done producing.
Consumer 1 started. Semaphore value is 1.
Producer 2 started. Semaphore value is 1.
Done producing.
Consumer 2 started. Semaphore value is 2.
Done consuming.
Producer 3 started. Semaphore value is 1.
Done consuming.
Consumer 3 started. Semaphore value is 0.
Done producing.
Producer 4 started. Semaphore value is 1.
Done producing.
Consumer 4 started. Semaphore value is 2.
Done consuming.
Done consuming.
Done producing.
Done consuming.
Exercise complete. Final semaphore value is 0.
Deleting semaphore with value 0.
```

Since the number of producers and consumers is equal and no timeouts occurred, the final value of the semaphore is 0.

To read about other semaphore scenarios, see Semaphores in InterSystems Products or %SYSTEM.Semaphore.

## Status

The %SYSTEM.Status class provides methods that can display or construct InterSystems IRIS status values, that is, objects of type %Library.Status (or %Status for short). Status values are commonly returned by methods in InterSystems IRIS. If a status has the value 1, it indicates that the method was a success. Otherwise, the status contains one or more error codes and messages to indicate any error conditions that occurred while running the method.

If you call an InterSystems IRIS method that returns a status, `iris.system.Status.IsOK()` returns 1 if the status is not an error, while `iris.system.Status.IsError()` returns 1 if the status is contains one or more errors. The `DisplayError()` method displays the contents of a status, including its error codes and messages.

If you write a method and you want to return a status, `iris.system.Status.OK()` returns a non-error status, while `iris.system.Status.Error()` lets you create and return an error status.

For example, say you are working with a simple persistent class that defines a pet object, which contains two required properties, `Name` and `Species`:

```
Class User.Pet Extends %Library.Persistent
{
Property Name As %String [ Required ];

Property Species As %String [ Required ];
}
```

Creating a new instance of a pet and trying to save it returns a status value, which you can check to see if the save succeeded, as well as display any errors that occur. If you try to save a pet without giving the `Species` property a value, you will see error #5659, indicating a required property is missing.

```
>>> status = iris.system.Status
>>> p = iris.User.Pet._New()
>>> p.Name = 'Fluffy'
>>> st = p._Save()
>>> if status.IsOK(st):
...     print('Pet saved')
... elif status.IsError(st):
...     status.DisplayError(st)
...

ERROR #5659: Property 'User.Pet::Species(8@User.Pet,ID=)' required
```

See InterSystems Error Reference for a list of possible error codes and messages.

You can also `iris.check_status()` to check the status returned by the `_Save()` method and throw a Python exception if it contains an error. This allows you to handle the error in a standard Python Try...Except. See iris.check_status() for more information.

Also, you might find situations where you are writing a method in Python and you need to return a status value, for instance, to some ObjectScript code. For example, you are writing a module `souffle.py` that contains a `bake()` function that needs to return a status that tells the caller if the souffle came out successfully or not.

```
def bake():
    import iris
    import random
    result = random.randint(1,10)
    if result > 6:
        st = iris.system.Status.Error(5001,'The souffle fell.')
    else:
        st = iris.system.Status.OK()
    return st
```

From looking at the code, you can see that there is a 40 percent chance that the souffle will fall. In such cases, the code will create a custom error, using the `iris.system.Status.Error()` method, and return it to the caller. InterSystems IRIS reserves the error codes 83 and 5001 for custom errors. If the souffle comes out successfully, it returns a non-error status, using the `OK()` method.

```objectscript
USER>set souffle = ##class(%SYS.Python).Import("souffle")

USER>set st = souffle.bake()

USER>do ##class(%SYSTEM.Status).DisplayError(st)

ERROR #5001: The souffle fell.
```

For more information, see Working with %Status Values.

## Util

The %SYSTEM.Util class provides an assortment of utility methods that can be useful for a variety of purposes. Just a few of these methods are explained here, to give you an idea of the breadth of this class.

Some of the utility methods in the `iris.system.Util` class can be used to monitor or administer the current state of InterSystems IRIS.

The method `IsDST()` determines whether the timestamp representing the current date and time is in daylight saving time. A return value of 1 indicates daylight saving time is currently in effect. For more information on the InterSystems IRIS date format, see $HOROLOG.

```
>>> iris.system.Util.IsDST()
1
```

The `SetSwitch()` method allows you to set a switch, controlling the instance-level functioning of InterSystems IRIS. For example, switch 12 inhibits new users or processes from logging in to the instance. See Using Switches for more information.

```
>>> iris.system.Util.SetSwitch(12,1)
0
```

Here, `SetSwitch()` is being used to turn on switch 12. The return value of 0 indicates the previous state of the switch 12, which was off. With switch 12 turned on, a user trying to log in to InterSystems IRIS sees the message:

```
<InterSystems IRIS Startup Error: Sign-on and JOB inhibited: Switch 12 is set (0)>
```

Other methods in `iris.system.Util` can be used to check certain attributes at the operating system level. The following examples are for Microsoft Windows.

The `GetEnviron()` method retrieves the value of an environment variable:

```
>>> iris.system.Util.GetEnviron('PATHEXT')
'.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.PY;.PYW'
```

The `InstallDirectory()` method retrieves the directory where the instance of InterSystems IRIS is installed:

```
>>> iris.system.Util.InstallDirectory()
'c:\\intersystems\\iris\\'
```

Still other methods in `iris.system.Util` perform simple tasks that are useful for manipulating data.

The `HexToDecimal()` and `DecimalToHex()` methods convert hex data to decimal and vice versa:

```
>>> iris.system.Util.HexToDecimal('BEAD')
'48813'
>>> iris.system.Util.DecimalToHex(1023)
'3FF'
```

The methods `Compress()` and `Decompress()` can be used to compress and decompress data, for example, with the zlib algorithm:

```
>>> compressed_string = iris.system.Util.Compress('The %SYSTEM.Util class contains useful utility methods','zlib')
>>> compressed_string
'6x\x9c\x0bÉHUP\r\x8e\x0c\x0eqõÕ\x0b-ÉÌQHÎI,.VHÎÏ+IÌÌ+V(-NM+ÍQ(\x05Je\x96T*ä¦\x96dä§\x14\x03\x00\x02 \x13É\x01'
>>> decompressed_string = iris.system.Util.Decompress(compressed_string)
>>> decompressed_string
'The %SYSTEM.Util class contains useful utility methods'
```

For more information, see %SYSTEM.Util.

## Version

The %SYSTEM.Version class provides methods for retrieving product version information.

For example, you can retrieve the entire version string (often referred to as the `$zv` string) or a piece of it:

```
>>> iris.system.Version.GetVersion()
'IRIS for Windows (x86-64) 2024.2 (Build 230U) Mon Jul 1 2024 16:40:47 EDT'
>>> iris.system.Version.GetOS()
'Windows'
```

You can also set the system mode using the `SystemMode()` method, instead of having to use the Management Portal:

```
>>> iris.system.Version.SystemMode('TEST')
'DEVELOPMENT'
```

The example above causes the Management Portal to display “Test System” at the top, to let you quickly identify what environment you are in. The return value of the method is the previous system mode of the InterSystems IRIS instance.

For more information, see %SYSTEM.Version.
