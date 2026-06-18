# Creating and Modifying Dynamic Entities

This chapter provides basic information on how dynamic entities work. The following topics are discussed:

*   Using JSON Literal Constructors
    
*   Using Dynamic Expressions and Dot Syntax
    
*   Using %Set(), %Get(), and %Remove()
    
*   Method Chaining
    
*   Error Handling
    

## Using JSON Literal Constructors

Dynamic entities are instances of %DynamicObject or %DynamicArray, which are designed to integrate JSON data manipulation seamlessly into ObjectScript applications. Although you can create instances of these classes with the standard `%New()` method, dynamic entities support a much more flexible and intuitive set of constructors. JSON literal constructors allow you to create dynamic entities by directly assigning a JSON string to a variable. For example, the following code creates empty instances of %DynamicObject and %DynamicArray:

```
   set dynamicObject = {}
   set dynamicArray = []
   write dynamicObject,!,dynamicArray

3@%Library.DynamicObject
1@%Library.DynamicArray
```

Unlike the `%New()` constructor, literal constructors `{}` and `[]` can accept a string in JSON format as an argument. For example, the following code creates a dynamic object with a property named `prop1`:

```
   set dynamicObject = {"prop1":"a string value"}
   write dynamicObject.prop1

a string value
```

In fact, JSON literal constructors `{}` and `[]` can be used to specify any valid JSON array or object structure. In simple terms, any valid JSON literal string is also a valid ObjectScript expression that evaluates to a dynamic entity.

> **Note:**
> 
> JSON property names must always be quoted
> 
> The JSON language specification (see https://json.org/) is a subset of JavaScript Object Notation, and enforces stricter rules in some areas. One important difference is that the JSON specification requires all property names to be enclosed in double-quotes. JavaScript syntax, on the other hand, permits unquoted names in many cases.

A dynamic entity stores an exact representation of each object property or array element in the JSON string. Any dynamic entity can use the `%ToJSON()` method to return the stored data as a JSON string. There is no loss or corruption of data when converting to or from a literal string. The following example creates a dynamic array and then calls `%ToJSON()` to construct and return a new JSON string representing the stored data:

```
   set dynamicArray = [[1,2,3],{"A":33,"a":"lower case"},1.23456789012345678901234,true,false,null,0,1,""]
   write dynamicArray.%ToJSON()

[[1,2,3],{"A":33,"a":"lower case"},1.23456789012345678901234,true,false,null,0,1,""]
```

This dynamic array has stored and returned several significant values:

*   The first two elements are a nested array and a nested object. In JSON syntax, array and object structures can be nested to any depth.
    
*   Property names are case-sensitive. The nested object has two distinct properties named `"A"` and `"a"`.
    
*   The third value is a very high-precision decimal number. This value would have been rounded down if it were stored as a standard floating point number, but the dynamic array has retained an exact representation of the original value.
    
*   The final six elements contain JSON datatype values `true`, `false`, and `null`, and corresponding ObjectScript values `0`, `1`, and `""`. Once again, dynamic entities preserve an exact representation of each value.
    

## Using Dynamic Expressions and Dot Syntax

There are significant differences between the way values are stored in JSON and the way they are expressed in ObjectScript. JSON data storage would not be very useful if you had to convert an ObjectScript value to or from JSON syntax every time you wanted to use it, so dynamic entities are designed to make this conversion process transparent. You can always store and retrieve an ObjectScript value without worrying about its representation in JSON syntax.

Literal JSON constructors are no exception to this rule. So far, all of our examples have been entirely in JSON syntax, but literal constructors can also accept values defined in dynamic expressions, which are simply ObjectScript expressions enclosed in parentheses.

For example, the following dynamic array constructor stores two Unicode characters. At runtime, the literal constructor evaluates each element and stores the evaluated value. The first element is defined in JSON syntax and the second element is an ObjectScript function call, but the resulting stored values are identical:

```
   write ["\u00E9",($CHAR(233))].%ToJSON()

["é","é"]
```

You can think of an ObjectScript expression as the code on the right side of a `set` statement. Any ObjectScript expression that evaluates to a value rather than an object reference can be serialized to a JSON literal string. The following example stores a $LIST value (which is a delimited string, not an object) in object property `obj.list`. It then creates `array` and extracts each list item in `obj.list` to a separate element:

```
   set obj = {"list":($LISTFROMSTRING("Deborah Noah Martha Bowie"," "))}
   set array = [($LIST(obj.list,1)),($LIST(obj.list,2)),($LIST(obj.list,3)),($LIST(obj.list,4))]
   write obj.%ToJSON(),!,array.%ToJSON()

{"list":"\t\u0001Deborah\u0006\u0001Noah\b\u0001Martha\u0007\u0001Bowie"}
["Deborah","Noah","Martha","Bowie"]
```

You cannot use a dynamic expression to define a property name (although there are ways to define property names programmatically. See “Using %Set(), %Get(), and %Remove()” for details).

Of course, literal constructors are not the only way to manipulate object properties and array elements. For example, the following code creates an empty dynamic object and uses standard object dot syntax to define the contents:

```
   set dynArray = []
   set dynArray."0" = "200" + "33"
   set dynArray."1" = {}
   set dynArray."1".foo = $CHAR(dynArray."0")
   write dynArray.%ToJSON()

[233,{"foo":"é"}]
```

In this example, literal constructors are used only to create empty dynamic entities. The assignment statements obey a few simple rules:

*   The assigned values are standard ObjectScript expressions. The value for `dynArray."0"` is evaluated as a numeric expression and the sum is returned as canonical form integer `233`. The $CHAR function later uses that value to return ASCII character 233, which is `"é"`.
    
*   Array elements are addressed by array index numbers, which must be numeric literals enclosed in double quotes. Dynamic arrays are zero-based.
    
*   Object properties are addressed by property names. Although property names are string literals, double quotes are optional if the property name is a valid class member name.
    
*   If the specified entity member does not yet exist, it will be created when you assign a value to it.
    

As previously mentioned, values are always stored and retrieved in ObjectScript format regardless of how they are represented in JSON syntax. The following examples demonstrate a few more facts that you should be aware of when using dot syntax.

### Creating dynamic object properties with dot syntax

This example uses a literal constructor and dot syntax to create dynamic object `dynObj`, containing properties named `A`, `a`, and `spaced name`. In the literal string, all property names must be quoted. In the `set` statements and the `write` statement, quotes are not required for property names `a` or `A`, but must be used for `spaced name`:

```
   set dynObj = {"a":"change this property"}
   set dynObj.a = " property a (quotes optional) "
   set dynObj."spaced name" = " property ""spaced name"" must be quoted "
   set dynObj.A = " property A is not property a "
   write !,dynObj.%ToJSON()

{"a":" property a (quotes optional) ","spaced name":" property \"spaced name\" must be quoted ","A":" property A is not property a "}
```

Dynamic objects are unordered lists, so values will not necessarily be stored in the order they were created. See “Iterating over a Dynamic Entity with %GetNext()” for examples that demonstrate this.

### Creating dynamic array elements with dot syntax

Dynamic arrays are zero-based. This example assigns a value to array element `3` before defining element `2`. Elements do not have to be defined in order, and element `2` could have been left undefined. See “Understanding Sparse Arrays and Unassigned Values” for detailed information.

```
   set dynArray = [true,false]
   set dynArray."3" = "three"
   set dynArray."2" = 0
   write dynArray.%ToJSON()

[true,false,0,"three"]
```

Although the first two elements were defined and stored as JSON boolean values `true` and `false`, they are returned as integers `1` and `0`, which are the equivalent ObjectScript boolean values:

```
   write "0="_dynArray."0"_", 1="_dynArray."1"_", 2="_dynArray."2"_", 3="_dynArray."3"

0=1, 1=0, 2=0, 3=three
```

Since stored values are always returned in ObjectScript format, JSON `true`, `false`, and `null` are returned as ObjectScript `0`, `1`, and `""` (empty string). However, the original JSON values are preserved in the dynamic entity and can be recovered if necessary. See “Working with Datatypes” for information on identifying the original datatype of a stored value.

> **Note:**
> 
> Dot syntax should not be used with very long property names
> 
> Although dynamic object properties can have names of any length, ObjectScript cannot use property names longer than 180 characters. If a dynamic object property name exceeds this limit, an attempt to use the name in dot syntax will result in a misleading `<PROPERTY DOES NOT EXIST>` error, even though the property exists and the name is valid. You can avoid this error by using the `%Set()` and `%Get()` methods, which accept property names of any length.

## Using %Set(), %Get(), and %Remove()

Although literal constructors and dot syntax can be used to create dynamic entity members and manipulate values, they are not adequate for all purposes. Dynamic entities provide `%Set()`, `%Get()`, and `%Remove()` methods for full programmatic control over create, read, update, and delete operations.

One of the most important advantages to these methods is that member identifiers (property names and array index numbers) do not have to be literals. You can use ObjectScript variables and expressions to specify both values and identifiers.

### Specifing values and identifiers programmatically with %Set(), %Get(), and %Remove()

The following example creates an object using literal constructor `{}`, and calls the `%Set()` method of the new object to add a series of properties named `prop`n with a value of `100+`n. Both names and values are defined by ObjectScript expressions:

```
   set dynObj = {}
   for i=1:1:5 { do dynObj.%Set("prop"_i,100+i) }
   write dynObj.%ToJSON()

{"prop1":101,"prop2":102,"prop3":103,"prop4":104,"prop5":105}
```

The same variables can be used with `%Get()` to retrieve the property values:

```
   for i=1:1:5 { write dynObj.%Get("prop"_i)_" " }

101 102 103 104 105
```

The `%Remove()` method deletes the specified member from the dynamic entity and returns the value. This example removes three of the five properties and concatenates the return values to string `removedValues`. The `write` statement displays the string of removed values and the current contents of `dynObj`:

```
   set removedValues = ""
   for i=2:1:4 { set removedValues = removedValues_dynObj.%Remove("prop"_i)_" " }
   write "Removed values: "_removedValues,!,"Remaining properties: "_dynObj.%ToJSON()

Removed values: 102 103 104
Remaining properties: {"prop1":101,"prop5":105}
```

> **Note:**
> 
> Although a `for` loop is used in these simple examples, the normal iteration method would be `%GetNext()` (described later in “Iterating over a Dynamic Entity with %GetNext()”).

Both `%Get()` and `%Remove()` return an ObjectScript value for the specified member, but there is an important difference in how embedded dynamic entities are returned:

*   `%Get()` returns the value by reference. The return value is an OREF (object reference) to the property or element, which in turn contains a reference to the embedded entity.
    
*   `%Remove()` destroys the specified property or element (making the member OREF invalid), but returns a valid OREF that points directly to the formerly embedded entity.
    

### Retrieving a nested dynamic entity with %Get() and %Remove()

In the following example, the value of property `dynObj.address` is a dynamic object. The `%Get()` statement stores a reference to the property (not the property value) in variable `addrPointer`. At this point, `addrPointer` can be used to access the `road` property of embedded entity `address`:

```
   set dynObj = {"name":"greg", "address":{"road":"Old Road"}}
   set addrPointer = dynObj.%Get("address")
   set dynObj.address.road = "New Road"
   write "Value of "_addrPointer_" is "_addrPointer.road

Value of 2@%Library.DynamicObject is New Road
```

The `%Remove()` statement destroys the property and returns a new OREF to the property value.

```
   set addrRemoved =  dynObj.%Remove("address")
   write "OREF of removed property: "_addrPointer,!,"OREF returned by %Remove(): "_addrRemoved

OREF of removed property: 2@%Library.DynamicObject
OREF returned by %Remove(): 3@%Library.DynamicObject
```

After the call to `%Remove()`, `addrRemoved` contains a valid OREF to the formerly embedded dynamic object.

```
   write addrRemoved.%ToJSON()

{"road":"New Road"}
```

You can use the `%Remove()` method to remove members in any order. This has different implications for objects and arrays, as demonstrated in the following examples.

### Removing an object property

Object properties have no fixed order. This means that properties can be destroyed in any order, but removing a property and adding another may also change the order in which properties are serialized and returned. The following example creates a dynamic object, and defines three properties with three consecutive calls to `%Set()`:

```
   set dynObject={}.%Set("propA","abc").%Set("PropB","byebye").%Set("propC",999)
   write dynObject.%ToJSON()

{"propA":"abc","PropB":"byebye","propC":999}
```

Now `%Remove()` is called to destroy property `PropB`, after which new property `PropD` is added. The resulting dynamic object does not serialize its properties in the order they were created:

```
   do dynObject.%Remove("PropB")
   set dynObject.propD = "added last"
   write dynObject.%ToJSON()

{"propA":"abc","propD":"added last","propC":999}
```

This also affects the order in which iterator method `%GetNext()` returns properties. See Iterating over a Dynamic Entity with %GetNext() for a similar example that uses `%GetNext()`.

### Removing an array element

An array is a zero-based ordered list. When you call `%Remove()` on an element, all elements after that one will have their array index number decremented by 1. The following example makes three consecutive calls to `%Remove(1)`, removing a different element each time:

```
   set dynArray = ["a","b","c","d","e"]
   set removedValues = ""
   for i=1:1:3 { set removedValues = removedValues_dynArray.%Remove(1)_" " }
   write "Removed values: "_removedValues,!,"Array size="_dynArray.%Size()_": "_dynArray.%ToJSON()

Removed values: b c d
Array size=2: ["a","e"]
```

A stack operation is usually implemented with `%Push()` and `%Pop()` rather than `%Set()` and `%Remove()`, but you can implement a queue by replacing `%Pop()` with `%Remove(0)` (see “Using %Push and %Pop with Dynamic Arrays”).

`%Remove()` works the same way with all arrays, including those that contain elements with undefined values. See “Understanding Sparse Arrays and Unassigned Values” for an example demonstrating how `%Remove()` works with sparse arrays.

### Assigning Dynamic Entities as Property Values

You can use `%Set()` or `%Push()` to nest a dynamic entity within another dynamic entity. For example, you can assign a dynamic object as a property value or an array element. An earlier example in this chapter showed how to retrieve a nested object (see “Retrieving a nested dynamic entity with %Get() and %Remove()”). The following example demonstrates one way to create a nested object.

#### Assigning a dynamic entity as a property value

This example creates a dynamic object with a property named `myData`, which has another dynamic object as its value:

```
   {"myData":{"myChild":"Value of myChild"}}
```

The following code creates this object. It is not necessary to specify `%Set()` arguments as variables, but doing so will allow you to assign any valid name or value at runtime:

```
   set mainObj = {}
   set mainPropName="myData"

   set nestedObj = {}
   set nestedPropName="myChild"
   set nestedPropValue="Value of myChild"

   do nestedObj.%Set(nestedPropName, nestedPropValue)
   do mainObj.%Set(mainPropName,nestedObj)
   write mainObj.%ToJSON()
```

This code produces the following output:

```objectscript
USER>write mainObj.%ToJSON()
{"myData":{"myChild":"Value of myChild"}}
```

> **Note:**
> 
> Do not use the type parameter with object values
> 
> The `%Set()` method has an optional `type` parameter that allows you to specify the datatype of the `value` argument in some limited cases (see “Overriding a Default Datatype with %Set() or %Push()”). The `type` parameter cannot be used when the `value` argument is a dynamic entity. An error will be thrown if you attempt to do so.

## Method Chaining

The `%Set()`, and `%Push()` methods return a reference to the entity that they have modified. The returned reference can immediately be used to call another method on the same entity, within the same expression.

The dynamic entity that begins a chain can be either a constructor (`{}`, or `[]`) or an existing entity. Methods `%Set()` and `%Push()` return chainable references and can be called from anywhere in the chain. The last item in a chain can be any method available to the entity.

In the following example, a single `write` statement uses chained calls to `%FromJSON()`, `%Set()`, `%Push()`, and `%ToJSON()` to create, modify, and display a dynamic array:

```
   set jstring = "[123]"
   write [].%FromJSON(jstring).%Set(1,"one").%Push("two").%Push("three").%Set(1,"final value").%ToJSON()

[123,"final value","two","three"]
```

`%FromJSON()` is only useful as the first method call in a chain, since it does not return a modified version of the calling entity. Instead, it simply ignores the calling entity and returns an entirely new instance deserialized from a JSON string. For more information, see “Converting Dynamic Entities to and from JSON”.

You could also start a chain by retrieving a nested entity with `%Get()`, `%Pop()`, `%GetNext()`, or `%Remove()`.

## Error Handling

Dynamic entities throw exceptions in the case of an error, rather than returning a %Status value. In the following example, the thrown exception includes enough information to conclude that the second character in the method argument is invalid (`property` should be enclosed in quotes):

```
   set string = "{property:1,}"
<THROW>%FromJSON+37^%Library.DynamicAbstractObject.1 *%Exception.General Parsing error 3 Line 1 Offset 2
```

When dealing with dynamic data, it is always wise to assume that some data will not fit your expectations. Any code that makes use of dynamic objects should be surrounded with a `TRY-CATCH` block at some level (see “The TRY-CATCH Mechanism” in Using ObjectScript) so your code can provide error handling. For example, wrapping this exception in a try-catch allows the exception data to be accessed via the standard %Exception.AbstractException object:

```
  try {
    set string = "{property:1,}"
    set json = ##class(%DynamicObject).%FromJSON(string)
  } catch ex {
    write "Trapped error ", ex.Code_": "_ex.Name_", "_ex.Location, !
  }
```

```
Trapped error 3: Parsing error, Line 1 Offset 2
```

The following table may help you deduce more about where an exception originated.

### JSON Error Messages

<table><tr><th>Error constant</th><th>code</th><th>Name (explanation)</th></tr><tr><td>JSON_ERROR_OKAY</td><td>1</td><td>Compilation okay</td></tr><tr><td>JSON_ERROR_NOSTRING</td><td>2</td><td>Cannot get string from source (source wasn't a string)</td></tr><tr><td>JSON_ERROR_PARSEFAIL</td><td>3</td><td>Parsing error (while parsing JSON string)</td></tr><tr><td>JSON_ERROR_INTERNAL_ERROR</td><td>4</td><td>Internal error</td></tr><tr><td>JSON_ERROR_NO_MEMORY</td><td>5</td><td>Insufficient memory (memory allocation failure)</td></tr><tr><td>JSON_ERROR_INVALID_HEX</td><td>6</td><td>Escaped hex sequence invalid (in \uXXXX string)</td></tr><tr><td>JSON_ERROR_OVERFLOW_HEX</td><td>7</td><td>Escaped hex sequence too large (too big for 8-bit systems)</td></tr><tr><td>JSON_ERROR_INVALID_ESCAPE</td><td>8</td><td>Escape sequence invalid</td></tr><tr><td>JSON_ERROR_MAX_NUMERIC</td><td>9</td><td>Numeric exceeds %d characters (numeric is too large)</td></tr><tr><td>JSON_ERROR_READ_ERROR</td><td>10</td><td>READ error while reading input stream</td></tr><tr><td>JSON_ERROR_MAX_DEPTH</td><td>11</td><td>Depth exceeds %d levels</td></tr><tr><td>JSON_ERROR_UNEXPECTED_EOF</td><td>12</td><td>Premature end of data</td></tr><tr><td>JSON_ERROR_DUPLICATE_KEY</td><td>13</td><td>Duplicate key</td></tr><tr><td>JSON_ERROR_IRIS_KERNEL</td><td>14</td><td>System error %s</td></tr><tr><td>JSON_ERROR_METADATA</td><td>15</td><td>Output exceeded maximum size of %d (metadata missing or illegal)</td></tr><tr><td>JSON_ERROR_CORRUPT_STRUCTURE</td><td>16</td><td>Corrupt internal array structure</td></tr><tr><td>JSON_ERROR_INVALID_ZU_ARGS</td><td>17</td><td>Array metadata missing or illegal (invalid arguments passed to $zu(210))</td></tr><tr><td>JSON_ERROR_MAXSIZE</td><td>18</td><td>Output variable exceeded maximum size</td></tr></table>
