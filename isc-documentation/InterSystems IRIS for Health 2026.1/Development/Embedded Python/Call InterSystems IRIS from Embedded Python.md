# Call InterSystems IRIS from Embedded Python

The key to calling InterSystems IRIS from Embedded Python is the `iris` Python module. The `iris` module provides a number of methods that unlock the functionality of InterSystems IRIS from Embedded Python and also allows you to access any InterSystems IRIS class as if it were a Python class.

This section provides a few basic examples of how to use the capabilities of InterSystems IRIS from Embedded Python:

*   Use the iris Module
    
*   Use an InterSystems IRIS Class
    
*   Use InterSystems SQL
    
*   Run an Arbitrary ObjectScript Command
    

For additional examples, see Call the InterSystems IRIS APIs from Python.

See InterSystems IRIS Python Module Reference for detailed descriptions of the most important APIs exposed by the `iris` module.

## Use the iris Module

The `iris` Python module enables you to interact with InterSystems IRIS to use its transaction processing functionality, access globals (the underlying data structure for all storage in InterSystems IRIS), access InterSystems IRIS APIs and classes, or call utility methods that help Embedded Python operate smoothly with ObjectScript.

Use the `iris` module from Embedded Python just as you would any Python module, by using the `import` command:

```
import iris
```

> **Note:**
> 
> You do not need to import the `iris` module explicitly when running the Python shell using the `Shell()` method of the %SYS.Python class. In this context only, the import is done for you behind the scenes.

After you import the `iris` module, call its methods just as you would with any other Python module.

For example, the `tstart()` method is used to indicate the start of a transaction in InterSystems IRIS:

```
iris.tstart()
```

## Use an InterSystems IRIS Class

You can use the `iris` module to return a reference to an InterSystems IRIS class. This gives you easy access to both built-in system classes and any custom classes you or someone on your team may have written.

If a system class has a name starting with a percent sign (%), it means that you can access the class from any namespace. If a system class does not begin with a percent sign, you must access the class from the `%SYS` namespace.

For instance, the class %Regex.Matcher creates an object that does pattern matching using regular expressions. The following example finds all of the area codes in a string and replaces them with the area code 212.

Using the method `%New()` is the standard way for creating a new instance of an InterSystems IRIS class.

Remember, class names and method names in Python cannot use the `%` character, so you must substitute an underscore (_), instead.

```
>>> import iris
>>> matcher = iris._Regex.Matcher
>>> m = matcher._New('\((\d{3})\)')
>>> m.Text = '(617) 555-1212, (202) 555-1313, (415) 555-1414'
>>> print(m.ReplaceAll('(212)'))
(212) 555-1212, (212) 555-1313, (212) 555-1414
```

You can find out more about this and other system classes by looking in the InterSystems Class Reference.

Custom classes work much the same way. They can create a logical grouping for a number of related methods, and often they extend the class %Persistent (short for %Library.Persistent), which enables you to store objects of the class in the InterSystems database.

You can find sample classes (including sample data) to learn from in the Samples-Data repository on GitHub: https://github.com/intersystems/Samples-Data. InterSystems recommends that you create a dedicated namespace called `SAMPLES` and load samples into that namespace.

Following is an excerpt from the class `Sample.Person`:

```objectscript
Class Sample.Person Extends (%Persistent, %Populate, %XML.Adaptor)
{
/// Person's name.
Property Name As %String(POPSPEC = "Name()") [ Required ];

/// Person's Social Security number. This is validated using pattern match.
Property SSN As %String(PATTERN = "3N1""-""2N1""-""4N") [ Required ];

/// Person's Date of Birth.
Property DOB As %Date(POPSPEC = "Date()");

/// A collection of strings representing the person's favorite colors.
Property FavoriteColors As list Of %String(JAVATYPE = "java.util.List",
POPSPEC = "ValueList("",Red,Orange,Yellow,Green,Blue,Purple,Black,White""):2");

/// Person's age.
/// This is a calculated field whose value is derived from DOB.
Property Age As %Integer [ Calculated, SqlComputeCode = { Set {Age}=##class(Sample.Person).CurrentAge({DOB})
}, SqlComputed, SqlComputeOnChange = DOB ];

/// This class method calculates a current age given a date of birth date.
/// This method is used by the Age calculated field.
ClassMethod CurrentAge(date As %Date = "") As %Integer [ CodeMode = expression ]
{
$Select(date="":"",1:($ZD($H,8)-$ZD(date,8)\10000))
}
}
```

You can see that a person object has several properties, including `Name`, `SSN`, `DOB`, `FavoriteColors`, and `Age`. The `DOB` property is the person’s birth date in $HOROLOG format. The `FavoriteColors` property is a list of strings. The `Age` property is a computed field that uses a method `CurrentAge()` to calculate it from the person’s date of birth.

The following example changes the current namespace to the `SAMPLES` namespace, creates a new instance of `Sample.Person`, sets its properties, and saves it to the database:

```
>>> import iris
>>> iris.system.Process.SetNamespace('SAMPLES')
'SAMPLES'
>>> p = iris.Sample.Person._New()
>>> p.Name = 'Doe,John'
>>> p.SSN = '000-00-0000'
>>> p.DOB = iris._Library.Date.DisplayToLogical('04/24/1999')
>>> print(p.Age)
25
>>> p.FavoriteColors.Insert('Red')
1
>>> p.FavoriteColors.Insert('Blue')
1
>>> p._Save()
1
>>> print(p._Id())
201
```

As you saw earlier, the `%New()` method creates an instance of `Sample.Person`, while the `%Save()` method saves it to the database. The `%Library.Date.DisplayToLogical()` method takes a date string and converts it to `$HOROLOG` format for storage. Finally, the `Insert()` method of a list property inserts a new element into a list.

Notice that the `Insert()` and `%Save()` methods in this example all return 1. These are examples of InterSystems IRIS status codes, and a 1 indicates that no error occurred during the execution of a method. Often, you will want to check this status code using iris.check_status() to handle any possible error cases.

InterSystems IRIS automatically assigns an ID to the object when it is stored, in this case, 201.

> **Note:**
> 
> Effective with InterSystems IRIS 2024.2, an optional shorter syntax for referring to an InterSystems IRIS class from Embedded Python has been introduced. Either the new form or the traditional form are permitted.

## Use InterSystems SQL

Persistent classes in InterSystems IRIS are projected to SQL, allowing you to access the data using a query using InterSystems SQL. The class `Sample.Person`, described above, projects to a table of the same name.

The example below selects the ID, name, and age of all persons having red as one of their favorite colors:

```
>>> sql = iris.sql.prepare('SELECT ID, Name, Age FROM Sample.Person WHERE FOR SOME %ELEMENT(FavoriteColors) (%Value = ?)')
>>> rs = sql.execute('Red')
>>> for idx, row in enumerate(rs):
...     print(f'{idx} = {row}')
...
0 = ['14', 'Roentgen,Sally S.', 78]
1 = ['30', 'Vanzetti,Jane A.', 73]
2 = ['38', 'Vanzetti,Heloisa W.', 8]
3 = ['61', 'Gibbs,Zoe J.', 81]
4 = ['72', 'Klingman,Pat E.', 55]
5 = ['89', 'Beatty,Mario Q.', 91]
6 = ['91', 'Ott,Jeff Z.', 54]
7 = ['97', 'Van De Griek,Kirsten B.', 49]
8 = ['101', 'Newton,Barbara A.', 51]
9 = ['105', 'Hertz,Yan M.', 90]
10 = ['129', 'Leiberman,Mo U.', 54]
11 = ['133', 'Zubik,George X.', 95]
12 = ['137', 'Jung,Lawrence T.', 83]
13 = ['147', 'Ubertini,Nataliya D.', 71]
14 = ['150', 'Ravazzolo,Sally S.', 84]
15 = ['187', 'Nichols,Terry F.', 64]
16 = ['196', 'Houseman,David D.', 97]
17 = ['200', 'Ng,James T.', 36]
18 = ['201', 'Doe,John', 25]
```

You can see that 19 records are returned, including that of John Doe, whom we entered earlier.

## Run an Arbitrary ObjectScript Command

Sometimes it can be handy to be able to run an arbitrary command in ObjectScript. You may want to test an ObjectScript command from Embedded Python, or you may want to access an ObjectScript function or “special variable.”

If you ever need to contact customer support, sometimes they will ask you for the InterSystems IRIS version string, `$ZVERSION` (or `$ZV` for short). This special variable contains a string that has the version of InterSystems IRIS you are using and additional details, like build number.

The following example shows how to write the value of `$ZVERSION` from Embedded Python:

```
>>> iris.execute('write $zversion, !')
IRIS for Windows (x86-64) 2024.1 (Build 267_2U) Tue Apr 30 2024 16:35:10 EDT
```

Or you can return the value of `$ZVERSION` and put its value in a Python variable:

```
>>> zv = iris.execute('return $zversion')
>>> print(zv)
IRIS for Windows (x86-64) 2024.1 (Build 267_2U) Tue Apr 30 2024 16:35:10 EDT
```

In this case, there is an equivalent way to get `$ZVERSION` using an API, but this will not always be true for other special variables and functions.

```
>>> print(iris.system.Version.GetVersion())
IRIS for Windows (x86-64) 2024.1 (Build 267_2U) Tue Apr 30 2024 16:35:10 EDT
```
