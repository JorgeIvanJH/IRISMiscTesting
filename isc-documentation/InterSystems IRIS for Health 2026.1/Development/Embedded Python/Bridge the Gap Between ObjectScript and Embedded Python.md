# Bridge the Gap Between ObjectScript and Embedded Python

Because of the differences between the ObjectScript and Python languages, you will need to know a few pieces of information that will help you bridge the gap between the languages.

From the ObjectScript side, the %SYS.Python class allows you to use Python from ObjectScript. See the InterSystems IRIS class reference for more information.

From the Python side, the `iris` module allows you to use ObjectScript from Python. From Python, type `help(iris)` for a list of its methods and functions, or see InterSystems IRIS Python Module Reference for more details.

## Access an InterSystems IRIS Class

The `iris` module gives you access to any InterSystems IRIS class from Embedded Python.

There are two ways of referring to an InterSystems IRIS class. The recommended syntax is `iris.<classname>`. You can also use `iris.cls('<classname>')`, and this syntax is required in InterSystems IRIS 2021.1.x through 2024.1.x.

The following examples are equivalent:

```
>>> matcher = iris._Regex.Matcher        #Recomended syntax
>>> matcher = iris.cls('%Regex.Matcher') #Older syntax (required in 2021.1.x through 2024.1.x)
```

If an InterSystems IRIS class name contains a percent sign (as in %Regex.Matcher), substitute an underscore in Embedded Python (as in `_Regex.Matcher`). In the case of `iris.cls('%Regex.Matcher')`, the name of the class is contained in a string argument, so a substitution is not needed.

The following examples are equivalent:

```
>>> p = iris.Sample.Person._New()        #Recomended syntax
>>> p = iris.cls('Sample.Person')._New() #Older syntax (required in 2021.1.x through 2024.1.x)
```

If an InterSystems IRIS method name contains a percent sign (as in `%New()`), substitute an underscore in Embedded Python (as in `_New()`).

## Refer to the Current InterSystems IRIS Class

When you want to refer to class members of the current InterSystems IRIS class in Embedded Python, you can often use `self`, just as you would with a Python class. This is the case for accessing properties or instance methods, for example. However, accessing other class members (such as class parameters or class methods) require a different syntax. For an overview of these and other class members, see Basics Contents of a Class Definition.

The following very simple InterSystems IRIS class definition, `User.RedSoxFan` can be used to describe Red Sox fans:

```objectscript
Class User.RedSoxFan Extends %Library.Persistent
{

Property Name As %String;

Parameter FAVORITETEAM = "Boston Red Sox";

ClassMethod FunFact() [ Language = python ]
{
print('Did you know baseball opening day is in three weeks!')
}

Method Greeting() [ Language = python ]
{
import iris
# option 1
print('Hello, my name is ' + self.Name + '. My favorite team is the ' + iris.User.RedSoxFan._GetParameter('FAVORITETEAM') + '.')
# option 2
# print('Hello, my name is ' + self.Name + '. My favorite team is the ' + iris.cls(__name__)._GetParameter('FAVORITETEAM') + '.')
}

Method Conversation() [ Language = python ]
{
import iris
self.Greeting()
# option 1
iris.User.RedSoxFan.FunFact()
# option 2
# iris.cls(__name__).FunFact()
}
}
```

Red Sox fans have a `Name` (a property, or value that is unique to each instance of the class) and a `FAVORITETEAM` (a class parameter, or value that is constant across all instances of the class). The class also has an instance method, `Greeting()`, that allows a member to print a greeting message to introduce themselves.

Looking at the code, you can see that the `Greeting()` method uses `self.Name` to access the `Name` property of the current fan. But to access the `FAVORITETEAM` parameter, you need to call the built-in method `%GetParameter()`. And instead of using `self` to reference the current class, you need to use `iris.User.RedSoxFan` or `iris.cls(__name__)`. In the second option, `__name__` is a built-in variable in Python that evaluates to the name of the current class. It uses the `iris.cls()` method, which takes a class name and returns a reference to the class.

In this example, `Greeting()` is an instance method, while `FunFact()` is a class method. You can think of an instance method as belonging to an instance of the class, while a class method belongs to the class. And in Embedded Python, the syntax for calling an instance method and a class method differ when you call them from within the class. Looking at the `Conversation()` method, you can see that `self` can be used to call the instance method, while `iris.User.RedSoxFan` or `iris.cls(__name__)` are used to call the class method.

The following example shows the class in action:

```
>>> f = iris.User.RedSoxFan._New()
>>> f.Name = "Jane Doe"
>>> f.Conversation()
Hello, my name is Jane Doe. My favorite team is the Boston Red Sox.
Did you know baseball opening day is in three weeks!
```

Of course, if you call a method from outside its class, you need to specify the class name:

```
>>> iris.User.RedSoxFan.FunFact()
Did you know baseball opening day is in three weeks!
>>> iris.User.RedSoxFan.Conversation(f)
Hello, my name is Jane Doe. My favorite team is the Boston Red Sox.
Did you know baseball opening day is in three weeks!
```

## Use ObjectScript and Python Identifier Names

The rules for naming identifiers are different between ObjectScript and Python. For example, the underscore (_) is allowed in Python method names, and in fact is widely used for the so-called “dunder” methods and attributes (“dunder” is short for “double underscore”), such as `__getitem__` or `__class__`. Dunder methods enable instances of a class to interact with Python’s built-in functions and operators. To use such identifiers from ObjectScript, enclose them in double quotes:

```objectscript
USER>set mylist = builtins.list()

USER>zwrite mylist."__class__"
2@%SYS.Python  ; <class list>  ; <OREF>
```

Conversely, InterSystems IRIS methods often begin with a percent sign (%). such as `%New()` or `%Save()`. To use such identifiers from Python, replace the percent sign with an underscore. If you have a persistent class `User.Person`, the following line of Python code creates a new Person object.

```
>>> import iris
>>> p = iris.User.Person._New()
```

## Use Python Builtin Functions

The `builtins` package is loaded automatically when the Python interpreter starts, and it contains all of the language’s built-in identifiers, such as the base object class and all of the built-in datatype classes, exceptions classes, functions, and constants.

You can import this package into ObjectScript to gain access to all of these identifiers as follows:

```
set builtins = ##class(%SYS.Python).Import("builtins")
```

The Python `print()` function is actually a method of the `builtins` module, so you can now use this function from ObjectScript:

```objectscript
USER>do builtins.print("hello world!")
hello world!
```

You can then use the `zwrite` command to examine the `builtins` object, and since it is a Python object, it uses the `str()` method of the `builtins` package to get a string representation of that object. For example:

```objectscript
USER>zwrite builtins
builtins=5@%SYS.Python  ; <module 'builtins' (built-in)>  ; <OREF>
```

By the same token, you can create a Python list using the method `builtins.list()`. The example below creates an empty list:

```objectscript
USER>set list = builtins.list()

USER>zwrite list
list=5@%SYS.Python  ; []  ; <OREF>
```

You can use the `builtins.type()` method to see what Python type the variable `list` is:

```objectscript
USER>zwrite builtins.type(list)
3@%SYS.Python  ; <class 'list'>  ; <OREF>
```

Interestingly, the `list()` method actually returns an instance of Python’s class object that represents a list. You can see what methods the `list` class has by using the `dir()` method on the list object:

```objectscript
USER>zwrite builtins.dir(list)
3@%SYS.Python  ; ['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__', '__delitem__',
'__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__',
'__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__',
'__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__','__repr__', '__reversed__',
'__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append','clear',
'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']  ; <OREF>
```

Likewise, you can use the `help()` method to get help on the list object.

```objectscript
USER>do builtins.help(list)
Help on list object:
class list(object)
 |  list(iterable=(), /)
 |
 |  Built-in mutable sequence.
 |
 |  If no argument is given, the constructor creates a new empty list.
 |  The argument must be an iterable if specified.
 |
 |  Methods defined here:
 |
 |  __add__(self, value, /)
 |      Return self+value.
 |
 |  __contains__(self, key, /)
 |      Return key in self.
 |
 |  __delitem__(self, key, /)
 |      Delete self[key].
.
.
.
```

> **Note:**
> 
> Instead of importing the `builtins` module into ObjectScript, you can call the `Builtins()` method of the %SYS.Python class.

## Use Keyword or Named Arguments

A common practice in Python is to use keyword arguments (also called “named arguments”) when defining a method. This makes it easy to drop arguments when not needed or to specify arguments according to their names, not their positions. As an example, take the following simple Python method:

```
def mymethod(foo=1, bar=2, baz="three"):
    print(f"foo={foo}, bar={bar}, baz={baz}")
```

Since InterSystems IRIS does not have the concept of keyword arguments, you need to create a dynamic object to hold the keyword/value pairs, for example:

```objectscript
USER>set args = { "bar": 123, "foo": "foo"}
```

If the method `mymethod()` were in a module called `mymodule.py` in the directory `<installdir>/mgr/python`, you could import it into ObjectScript and then call it, as follows:

```objectscript
USER>set obj = ##class(%SYS.Python).Import("mymodule")

USER>set args = {"bar": 123, "foo": "foo"}

USER>do obj.mymethod(args...)
foo=foo, bar=123, baz=three
```

Since `baz` was not passed in to the method, it is assigned the value of `"three"` by default.

## Pass Arguments By Reference

Arguments in methods written in ObjectScript can be passed by value or by reference. In the method below, the `ByRef` keyword in front of the second and third arguments in the signature indicates that they are intended to be passed by reference.

```
ClassMethod SandwichSwitch(bread As %String, ByRef filling1 As %String, ByRef filling2 As %String)
{
    set bread = "whole wheat"
    set filling1 = "almond butter"
    set filling2 = "cherry preserves"
}
```

Assume this method is contained in a class called `User.EmbeddedPython`. When calling the method from ObjectScript, place a period before an argument to pass it by reference, as shown below:

```objectscript
USER>set arg1 = "white bread"

USER>set arg2 = "peanut butter"

USER>set arg3 = "grape jelly"

USER>do ##class(User.EmbeddedPython).SandwichSwitch(arg1, .arg2, .arg3)

USER>write arg1
white bread
USER>write arg2
almond butter
USER>write arg3
cherry preserves
```

From the output, you can see that the value of the variable `arg1` remains the same after calling `SandwichSwitch()`, while the values of the variables `arg2` and `arg3` have changed.

Since Python does not support call by reference natively, you need to use the `iris.ref()` method to create a reference to pass to the method for each argument to be passed by reference:

```
>>> import iris
>>> arg1 = 'white bread'
>>> arg2 = iris.ref('peanut butter')
>>> arg3 = iris.ref('grape jelly')
>>> iris.User.EmbeddedPython.SandwichSwitch(arg1, arg2, arg3)
>>> arg1
'white bread'
>>> arg2.value
'almond butter'
>>> arg3.value
'cherry preserves'
```

You can use the `value` property to access the values of `arg2` and `arg3` and see that they have changed following the call to the method.

ObjectScript also has a keyword `Output`, which indicates that an argument is passed by reference and it is expected that this argument is to be used as an output, without any incoming value. From Python, use the `iris.ref()` method to pass the argument the same way as you would for a `ByRef` argument.

> **Note:**
> 
> While passing arguments by reference is a feature of ObjectScript methods, there is no equivalent way to pass arguments by reference to a method written in Python. The `ByRef` and `Output` keywords in the signature of an ObjectScript method are conventions used to indicate to the user that the method expects that an argument is to be passed by reference. In fact, `ByRef` and `Output` have no actual function and are ignored by the compiler. Adding `ByRef` or `Output` to the signature of a method written in Python results in a compiler error.

## Pass Values for True, False, and None

The %SYS.Python class has the methods `True()`, `False()`, and `None()`, which represent the Python identifiers `True`, `False`, and `None`, respectively.

For example:

```objectscript
USER>zwrite ##class(%SYS.Python).True()
2@%SYS.Python  ; True  ; <OREF>
```

These methods are useful if you need to pass `True`, `False`, and `None` to a Python method. The following example uses the method shown in Keyword or Named Arguments.

```objectscript
USER>do obj.mymethod(##class(%SYS.Python).True(), ##class(%SYS.Python).False(), ##class(%SYS.Python).None())
foo=True, bar=False, baz=None
```

If you pass unnamed arguments to a Python method that expects keyword arguments, Python handles them in the order they are passed in.

Note that you do not need to use the methods `True()`, `False()`, and `None()` when examining the values returned by a Python method to ObjectScript.

Say the Python module `mymodule` also has a method `isgreaterthan()`, which is defined as follows:

```
def isgreaterthan(a, b):
    return a > b
```

When run in Python, you can see that the method returns `True` if the argument `a` is greater than `b`, and `False` otherwise:

```
>>> mymodule.isgreaterthan(5, 4)
True
```

However, when called from ObjectScript, the returned value is `1`, not the Python identifier `True`:

```objectscript
USER>zwrite obj.isgreaterthan(5, 4)
1
```

## Use Dictionaries

In Python, dictionaries are commonly used to store data in key-value pairs, for example:

```
>>> mycar = {
...     'make': 'Toyota',
...     'model': 'RAV4',
...     'color': 'blue'
... }
>>> print(mycar)
{'make': 'Toyota', 'model': 'RAV4', 'color': 'blue'}
>>> print(mycar['color'])
blue
```

You can use the method `iris.arrayref()` to place the contents of the dictionary `mycar` into an ObjectScript array and return a reference to that array:

```
>>> a = iris.arrayref(mycar)
>>> print(a.value)
{'color': 'blue', 'make': 'Toyota', 'model': 'RAV4'}
>>> print(a.value['color'])
blue
```

You can then pass the array to an ObjectScript method.

For example, assume you have an InterSystems IRIS class called `User.ArrayTest` that has a method `WriteContents()` that writes the contents of an array:

```
ClassMethod WriteContents(myArray) [ Language = objectscript ]
{
    zwrite myArray
}
```

Then, you can call `WriteContents()` as follows:

```
>>> iris.User.ArrayTest.WriteContents(a)
myArray("color")="blue"
myArray("make")="Toyota"
myArray("model")="RAV4"
```

For more information, see iris.arrayref().

On the ObjectScript side, you can manipulate Python dictionaries using the `dict()` method of the Python `builtins` module:

```objectscript
USER>set mycar = ##class(%SYS.Python).Builtins().dict()

USER>do mycar.setdefault("make", "Toyota")

USER>do mycar.setdefault("model", "RAV4")

USER>do mycar.setdefault("color", "blue")

USER>zwrite mycar
mycar=2@%SYS.Python  ; {'make': 'Toyota', 'model': 'RAV4', 'color': 'blue'}  ; <OREF>

USER>write mycar."__getitem__"("color")
blue
```

The example above uses the dictionary method `setdefault()` to set the value of a key and `__getitem__()` to get the value of a key.

## Use Lists

In Python, lists store collections of values, but without keys. Items in a list are accessed by their index.

```
>>> fruits = ['apple', 'banana', 'cherry']
>>> print(fruits)
['apple', 'banana', 'cherry']
>>> print(fruits[0])
apple
```

In ObjectScript, you can work with Python lists using the `list()` method of the Python `builtins` module:

```objectscript
USER>set l = ##class(%SYS.Python).Builtins().list()

USER>do l.append("apple")

USER>do l.append("banana")

USER>do l.append("cherry")

USER>zwrite l
l=13@%SYS.Python  ; ['apple', 'banana', 'cherry']  ; <OREF>

USER>write l."__getitem__"(0)
apple
```

The example above uses the list method `append()` to append an item to the list and `__getitem__()` to get the value at a given index. (Python lists are zero based.)

If you want to convert an ObjectScript list to a Python list, you can use the `ToList()` and `ToListTyped()` methods in %SYS.Python. Given an ObjectScript list, `ToList()` returns a Python list that contains the same data. Given an ObjectScript list containing data and a second ObjectScript list containing integer ODBC data type codes, `ToListTyped()` returns a Python list that contains the same data as the first list, with each item having the data types specified in the second list.

> **Note:**
> 
> For a table of ODBC data types, see Integer Codes for Data Types.
> 
> Some ODBC data types may translate to the same Python data type.
> 
> Some data types require the Python package `numpy` to be installed.

In the example below, a Python method `Loop()` in the class `User.Lists` iterates over the items in a list and prints their value and data type.

```
ClassMethod Loop(pyList) [ Language = python ]
{
    for x in pyList:
        print(x, type(x))
}
```

You can then use `ToList()` and `ToListTyped()` as follows:

```objectscript
USER>set clist = $listbuild(123, 456.789, "hello world")

USER>set plist = ##class(%SYS.Python).ToList(clist)

USER>do ##class(User.Lists).Loop(plist)
123 <class 'int'>
456.789 <class 'float'>
hello world <class 'str'>

USER>set clist = $listbuild(42, 42, 42, 42)

USER>set tlist = $listbuild(-7, 2, 3, 4)

USER>set plist = ##class(%SYS.Python).ToListTyped(clist, tlist)

USER>do ##class(User.Lists).Loop(plist)
True <class 'bool'>
42.0 <class 'float'>
42 <class 'decimal.Decimal'>
42 <class 'int'>
```

## Use Globals

Most of the time, you will probably access data stored in InterSystems IRIS either by using SQL or by using persistent classes and their properties and methods. However, there may be times when you want to directly access the underlying native persistent data structures, called globals. This is particularly true if you are accessing legacy data or if you are storing schema-less data that doesn’t lend itself to SQL tables or persistent classes.

Though it is an oversimplification, you can think of a global as a dictionary of key-value pairs. (See Introduction to Globals for a more accurate description.)

Consider the following class, which has two class methods written in Python:

```
Class User.Globals
{
ClassMethod SetSquares(x) [ Language = python ]
{
    import iris
    square = iris.gref('^square')
    for key in range(1, x):
        value = key * key
        square.set([key], value)
}
ClassMethod PrintSquares() [ Language = python ]
{
    import iris
    square = iris.gref('^square')
    key = ''
    while True:
        key = square.order([key])
        if key == None:
            break
        print('The square of ' + str(key) + ' is ' + str(square.get([key])))
}
}
```

The method `SetSquares()` loops over a range of keys, storing the square of each key at each node of the global `^square`. The method `PrintSquares()` traverses the global and prints each key and the value stored at the key.

Let’s launch the Python shell, instantiate the class, and run the code to see how it works.

```objectscript
USER>do ##class(%SYS.Python).Shell()

Python 3.9.5 (default, May 31 2022, 12:35:47) [MSC v.1927 64 bit (AMD64)] on win32
Type quit() or Ctrl-D to exit this shell.
>>> g = iris.User.Globals
>>> g.SetSquares(6)
>>> g.PrintSquares()
The square of 1 is 1
The square of 2 is 4
The square of 3 is 9
The square of 4 is 16
The square of 5 is 25
```

Now, let’s look at how some of the methods of the built-in `iris` module allow us to access globals.

In method `SetSquares()`, the statement `square = iris.gref('^square')` returns a reference to the global `^square`, also known as a gref:

```
>>> square = iris.gref('^square')
```

The statement `square.set([key], value)` sets the node of `^square` with key `key` to the value `value`, for example you can set node 12 of `^square` to the value 144:

```
>>> square.set([12], 144)
```

You can also set the node of a global with the following shorter syntax:

```
>>> square[13] = 169
```

In method `PrintSquares()`, the statement `key = square.order([key])` takes a key as input and returns the next key in the global, similar to the `$ORDER` function in ObjectScript. A common technique for a traversing a global is to continue using `order()` until it returns None, indicating that no more keys remain. Keys do not need to be consecutive, so `order()` returns the next key even if there are gaps between keys:

```
>>> key = 5
>>> key = square.order([key])
>>> print(key)
12
```

Then, `square.get([key])` takes a key as input and returns the value at that key in the global:

```
>>> print(square.get([key]))
144
```

Again, you can use the following shorter syntax:

```
>>> print(square[13])
169
```

Note that nodes in a global don’t have to have a key. The following statement stores a string at the root node of `^square`:

```
>>> square[None] = 'Table of squares'
```

To show that these Python commands did in fact store values in the global, exit the Python shell and then use the `zwrite` command in ObjectScript to print the contents of `^square`:

```objectscript
>>> quit()

USER>zwrite ^square
^square="Table of squares"
^square(1)=1
^square(2)=4
^square(3)=9
^square(4)=16
^square(5)=25
^square(12)=144
^square(13)=169
```

See Global Reference API for more details on how to access and manipulate globals from Python.

## Change Namespaces

InterSystems IRIS has the concept of namespaces, each of which has its own databases for storing code and data. This makes it easy to keep the code and data of one namespace separate from the code and data of another namespace. For example, if one namespace has a global with a certain name, another namespace can use a global with the same name without the danger of conflicting with the other global.

If you have two namespaces, `NSONE` and `NSTWO`, you could create a global called `^myFavorite` in `NSONE`, using ObjectScript in Terminal, as shown below. Then you could set the `$namespace` special variable to change to `NSTWO` and create a separate global called `^myFavorite` in that namespace. (To replicate this example, you can configure these two namespaces on your InterSystems IRIS instance or use two namespaces you already have.)

```objectscript
NSONE>set ^myFavorite("fruit") = "apple"

NSONE>set $namespace = "NSTWO"

NSTWO>set ^myFavorite("fruit") = "orange"
```

Here, `^myFavorite("fruit")` has the value `"apple"` in `NSONE` and the value `"orange"` in `NSTWO`.

When you call Embedded Python, it inherits the current namespace. We can test this by calling the `NameSpace()` method of the `iris.system.Process` class from Python, which displays the name of the current namespace, and by confirming that `^myFavorite("fruit") = "orange"`.

```objectscript
NSTWO>do ##class(%SYS.Python).Shell()

Python 3.9.5 (default, Jun  2 2023, 14:12:21) [MSC v.1927 64 bit (AMD64)] on win32
Type quit() or Ctrl-D to exit this shell.
>>> iris.system.Process.NameSpace()
'NSTWO'
>>> myfav = iris.gref('^myFavorite')
>>> print(myfav['fruit'])
orange
```

You’ve seen how to use `$namespace` to change namespaces in ObjectScript. In Embedded Python, you use the `SetNamespace()` method of the `iris.system.Process` class. For example, you can change to the namespace `NSONE` and confirm that `^myFavorite("fruit") = "apple"`.

```
>>> iris.system.Process.SetNamespace('NSONE')
'NSONE'
>>> myfav = iris.gref('^myFavorite')
>>> print(myfav['fruit'])
apple
```

Finally, when you exit from the Python shell, you remain in namespace `NSONE`.

```objectscript
>>> quit()

NSONE>
```

## Run an ObjectScript Routine from Embedded Python

You may encounter older ObjectScript code that uses routines instead of classes and methods and want to call a routine from Embedded Python. In such cases, you can use the method `iris.routine()` from Python.

The following example, when run in the `%SYS` namespace, calls the routine `^SECURITY`:

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

## Handle Exceptions

The InterSystems IRIS exception handler can handle Python exceptions and pass them seamlessly to ObjectScript. Building on the earlier Python package example, the following example shows what happens if you try to call `canvas.drawImage()` using a non-existent file. Here, ObjectScript catches the exception in the special variable `$zerror`:

```objectscript
USER>try { do canvas.drawImage("C:\Sample\bad.png", 150, 600) } catch { write "Error: ", $zerror, ! }
Error: <THROW> *%Exception.PythonException <THROW> 230 ^^0^DO canvas.drawImage("W:\Sample\isc.png", 150, 600)
<class 'OSError'>: Cannot open resource "W:\Sample\isc.png" -
```

In this case, `<class 'OSError'>: Cannot open resource "W:\Sample\isc.png"` is the exception passed back from Python.

For more information on `$zerror`, see $ZERROR (ObjectScript).

For information on raising an ObjectScript status error as a Python exception, see check_status(status).

## Bytes and Strings

Python draws a clear distinction between bytes objects (of the data type `bytes`), which are sequences of raw 8-bit integers used for binary data, and strings (of the data type `str`), which are sequences of human-readable Unicode characters used for textual data.

InterSystems IRIS makes no distinction between bytes and strings. While InterSystems IRIS supports Unicode strings (UCS-2/UTF-16), any string that contains values of less than 256 could either be a string or bytes. For this reason, the following rules apply when passing strings and bytes to and from Python:

*   InterSystems IRIS strings are assumed to be strings and are converted to UTF-8 when passed from ObjectScript to Python.
    
*   Python strings are converted from UTF-8 to InterSystems IRIS strings when passed back to ObjectScript, which may result in wide characters.
    
*   Python bytes objects are returned to ObjectScript as 8-bit strings. If the length of the bytes object exceeds the maximum string length, then a Python bytes object is returned.
    
*   To pass bytes objects to Python from ObjectScript, use the `##class(%SYS.Python).Bytes()` method, which does not convert the underlying InterSystems IRIS string to UTF-8.
    
*   To turn the bytes object back into a string, use the builtins method `builtins.bytes()`.
    

The following example turns an InterSystems IRIS string to a Python object of type bytes and then converts that object back into a string:

```objectscript
USER>set builtins = ##class(%SYS.Python).Import("builtins")

USER>set b = ##class(%SYS.Python).Bytes("Hello Bytes!")

USER>zwrite b
b=3@%SYS.Python  ; b'Hello Bytes!'  ; <OREF>

USER>zwrite builtins.type(b)
2@%SYS.Python  ; <class 'bytes'>  ; <OREF>

USER>zwrite builtins.list(b)
2@%SYS.Python  ; [72, 101, 108, 108, 111, 32, 66, 121, 116, 101, 115, 33]  ; <OREF>

USER>set s = builtins.bytes(b)

USER>zwrite s
s="Hello Bytes!"

USER>zwrite builtins.type(s)
2@%SYS.Python  ; <class 'str'>  ; <OREF>

USER>zwrite builtins.list(s)
2@%SYS.Python  ; ['H', 'e', 'l', 'l', 'o', ' ', 'B', 'y', 't', 'e', 's', '!']  ; <OREF>
```

To construct Python bytes objects bigger than the 3.8MB maximum string length in InterSystems IRIS, you can use a bytearray object and append smaller chunks of bytes using the `extend()` method. Finally, pass the bytearray object into the builtins `bytes()` method to get a bytes representation:

```objectscript
USER>set ba = builtins.bytearray()

USER>do ba.extend(##class(%SYS.Python).Bytes("chunk 1"))

USER>do ba.extend(##class(%SYS.Python).Bytes("chunk 2"))

USER>zwrite builtins.bytes(ba)
"chunk 1chunk 2"
```

## Standard Output and Standard Error Mappings

When using Embedded Python, standard output is mapped to the InterSystems IRIS console, which means that the output of any print() statements is sent to the Terminal. Standard error is mapped to the InterSystems IRIS `messages.log` file, located in the directory `<install-dir>/mgr`.

As an example, consider this Python method:

```
def divide(a, b):
    try:
        print(a/b)
    except ZeroDivisionError:
        print('Cannot divide by zero')
    except TypeError:
        import sys
        print('Bad argument type', file=sys.stderr)
    except:
        print('Something else went wrong')
```

Assume the method is contained in a module called `mymodule.py` in the directory `<installdir>/mgr/python`. Then, if you test this method in Terminal, you might see the following:

```objectscript
USER>set obj = ##class(%SYS.Python).Import("mymodule")

USER>do obj.divide(5, 0)
Cannot divide by zero

USER>do obj.divide(5, "hello")
```

If you try to divide by zero, the error message is directed to the Terminal, but if you try to divide by a string, the message is sent to `messages.log`:

```
11/19/21-15:49:33:248 (28804) 0 [Python] Bad argument type
```

Only important messages should be sent to `messages.log`, to avoid cluttering the file.
