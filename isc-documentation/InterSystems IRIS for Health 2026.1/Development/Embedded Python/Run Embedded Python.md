# Run Embedded Python

This page details several ways to run Embedded Python.

## From the Python Shell

You can start the Python shell from an InterSystems Terminal session or from the command line.

### Start the Python Shell from Terminal

Start the Python shell from an InterSystems Terminal session by calling the `Shell()` method of the %SYS.Python class. This launches the Python interpreter in interactive mode. The user and namespace from the Terminal session are passed to the Python shell.

Exit the Python shell by typing the command `quit()`.

The following example launches the Python shell from the `USER` namespace in a Terminal session. It prints the first few numbers in the Fibonacci sequence and then uses the InterSystems IRIS `%SYSTEM.OBJ.ShowClasses()` method to print a list of classes in the current namespace.

```objectscript
USER>do ##class(%SYS.Python).Shell()

Python 3.9.5 (default, Jul  6 2021, 13:03:56) [MSC v.1927 64 bit (AMD64)] on win32
Type quit() or Ctrl-D to exit this shell.
>>> a, b = 0, 1
>>> while a < 10:
...     print(a, end = ' ')
...     a, b = b, a + b
...
0 1 1 2 3 5 8 >>>
>>> status = iris._SYSTEM.OBJ.ShowClasses()
User.Company
User.Person
>>> print(status)
1
>>> quit()

USER>
```

The method `%SYSTEM.OBJ.ShowClasses()` returns an InterSystems IRIS %Status value. In this case, a 1 means that no errors were detected.

### Start the Python Shell from the Command Line

Start the Python shell from the command line by using the `irispython` command. This works much the same as starting the shell from Terminal, but you must pass in the InterSystems IRIS username, password, and namespace.

The following example launches the Python shell from the Windows command line:

```
C:\InterSystems\IRIS\bin>set IRISUSERNAME=<username>

C:\InterSystems\IRIS\bin>set IRISPASSWORD=<password>

C:\InterSystems\IRIS\bin>set IRISNAMESPACE=USER

C:\InterSystems\IRIS\bin>irispython
Python 3.9.5 (default, Jul  6 2021, 13:03:56) [MSC v.1927 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

On UNIX-based systems, use `export` instead of `set`.

```
/InterSystems/IRIS/bin$ export IRISUSERNAME=<username>
/InterSystems/IRIS/bin$ export IRISPASSWORD=<password>
/InterSystems/IRIS/bin$ export IRISNAMESPACE=USER
/InterSystems/IRIS/bin$ ./irispython
Python 3.9.5 (default, Jul 22 2021, 23:12:58)
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

> **Note:**
> 
> If you see a message saying `IRIS_ACCESSDENIED`, enable `%Service_Callin`. In the Management Portal, go to `System Administration` > `Security` > `Services`, select `%Service_CallIn`, and check the `Service Enabled` box.

## In a Python Script File (.py)

You can also use the `irispython` command to execute a Python script. Note that in this case, you have to include a step (`import iris`) that provides access to InterSystems IRIS.

Consider a file `C:\python\test.py`, on a Windows system, containing the following code:

```
# print the members of the Fibonacci series that are less than 10
print('Fibonacci series:')
a, b = 0, 1
while a < 10:
    print(a, end = ' ')
    a, b = b, a + b

# import the iris module and show the classes in this namespace
import iris
print('\nInterSystems IRIS classes in this namespace:')
status = iris._SYSTEM.OBJ.ShowClasses()
print(status)
```

You could run `test.py` from the command line, as follows:

```
C:\InterSystems\IRIS\bin>set IRISUSERNAME=<username>

C:\InterSystems\IRIS\bin>set IRISPASSWORD=<password>

C:\InterSystems\IRIS\bin>set IRISNAMESPACE=USER

C:\InterSystems\IRIS\bin>irispython \python\test.py
Fibonacci series:
0 1 1 2 3 5 8
InterSystems IRIS classes in this namespace:
User.Company
User.Person
1
```

On UNIX-based systems, use `export` instead of `set`.

```
/InterSystems/IRIS/bin$ export IRISUSERNAME=<username>
/InterSystems/IRIS/bin$ export IRISPASSWORD=<password>
/InterSystems/IRIS/bin$ export IRISNAMESPACE=USER
/InterSystems/IRIS/bin$ ./irispython /python/test.py
Fibonacci series:
0 1 1 2 3 5 8
InterSystems IRIS classes in this namespace:
User.Company
User.Person
1
```

> **Note:**
> 
> If you try to run `import iris` and see a message saying `IRIS_ACCESSDENIED`, enable `%Service_Callin`. In the Management Portal, go to `System Administration` > `Security` > `Services`, select `%Service_CallIn`, and check the `Service Enabled` box.

## In a Method in an InterSystems IRIS Class

You can write Python methods in an InterSystems IRIS class by using the `Language` keyword. You can then call the method as you would call a method written in ObjectScript.

For example, take the following class with a class method written in Python:

```objectscript
Class User.EmbeddedPython
{

/// Description
ClassMethod Test() As %Status [ Language = python ]
{
    # print the members of the Fibonacci series that are less than 10
    print('Fibonacci series:')
    a, b = 0, 1
    while a < 10:
        print(a, end = ' ')
        a, b = b, a + b

    # import the iris module and show the classes in this namespace
    import iris
    print('\nInterSystems IRIS classes in this namespace:')
    status = iris._SYSTEM.OBJ.ShowClasses()
    return status
}

}
```

You can call this method from ObjectScript:

```objectscript
USER>set status = ##class(User.EmbeddedPython).Test()
Fibonacci series:
0 1 1 2 3 5 8
InterSystems IRIS classes in this namespace:
User.Company
User.EmbeddedPython
User.Person

USER>write status
1
```

Or from Python:

```
>>> import iris
>>> status = iris.User.EmbeddedPython.Test()
Fibonacci series:
0 1 1 2 3 5 8
InterSystems IRIS classes in this namespace:
User.Company
User.EmbeddedPython
User.Person
>>> print(status)
1
```

## In SQL Functions and Stored Procedures

You can also write a SQL function or stored procedure using Embedded Python by specifying the argument `LANGUAGE PYTHON` in the `CREATE FUNCTION` statement. The example below returns a random uppercase character:

```
CREATE FUNCTION random_letter()
   RETURNS VARCHAR
   LANGUAGE PYTHON
{
   import random
   import string
   return random.choice(string.ascii_uppercase)
}
```

While this example uses built-in Python modules, you can also use modules you install yourself.

The following `SELECT` statement uses the function to return all sample persons whose name starts with a random character:

```
SELECT Name FROM Sample.Person WHERE Name %STARTSWITH random_letter()
```

The function returns something like:

```
O'Donnell,Alice Z.
O'Donnell,Brendan V.
O'Donnell,Elmo H.
O'Rielly,Edward A.
O'Rielly,Greta W.
Olsen,Edgar H.
Orlin,Alvin R.
Ott,Edgar O.
Ott,Heloisa K.
Ott,Stavros J.
```
