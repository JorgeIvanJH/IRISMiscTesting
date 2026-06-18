# Using JSON in ObjectScript

InterSystems ObjectScript syntax includes integrated support for JSON (https://json.org/). A set of fast, simple, powerful features allow you to work with JSON data structures as easily as you do with objects or tables:

*   With ObjectScript syntax for JSON, you can use standard ObjectScript assignment statements rather than method calls to create and alter dynamic entities at run time. The values of object properties and array elements can be specified either as JSON string literals or as ObjectScript dynamic expressions.
    
*   Two classes, %Library.DynamicObject and %Library.DynamicArray, provide a simple, efficient way to encapsulate and work with standard JSON data structures. Instances of these classes are called dynamic entities.
    
*   Dynamic entities contain methods for JSON serialization (conversion between dynamic entities and canonical JSON format), iteration, data typing, create/read/update/delete operations, and other useful functions.
    

See the Table of Contents for a detailed listing of the subjects covered in this document.

## JSON Features in Action

Here are some examples of the JSON features available in ObjectScript:

### Create and manipulate dynamic entities at runtime

You can create dynamic entities and define an arbitrary schema for them at run time:

```
   set dynObject1 = ##class(%DynamicObject).%New()
   set dynObject1.SomeNumber = 42
   set dynObject1.SomeString = "a string"
   set dynObject1.SomeArray = ##class(%DynamicArray).%New()
   set dynObject1.SomeArray."0" = "an array element"
   set dynObject1.SomeArray."1" = 123
```

### Create dynamic entities with literal JSON constructors

You can also create a dynamic entity by assigning a literal JSON string. Literal JSON constructors `{}` and `[]` are can be used in place of the `%New()` constructor. For example you can create a dynamic array with `set x=[]` rather than `set x=##class(%DynamicArray).%New()`. Unlike `%New()`, a literal JSON constructor can also take a JSON literal string that specifies properties or elements. This means you can create an object identical to `dynObject1` in the previous example with these simple assignment statements:

```
   set dynObject2 = {"SomeNumber":42,"SomeString":"a string"}
   set dynObject2.SomeArray = ["an array element",123]
```

This example uses a statement for each constructor, but the array constructor could just as easily be nested inside the object constructor.

To demonstrate that `dynObject1` and `dynObject2` are identical, we can display them as serialized JSON strings returned by the `%ToJSON()` method:

```
   write "object 1: "_dynObject1.%ToJSON(),!,"object 2: "_dynObject2.%ToJSON()

object 1: {"SomeNumber":42,"SomeString":"a string","SomeArray":["an array element",123]}
object 2: {"SomeNumber":42,"SomeString":"a string","SomeArray":["an array element",123]}
```

### Define values with dynamic expressions

The text enclosed in literal constructors `{}` and `[]` must use valid JSON syntax, with one exception. For the value of an element or property, you can use an expression enclosed in parentheses rather than a JSON literal. This ObjectScript dynamic expression (equivalent to the right side of a `set` statement) will evaluated at runtime and converted to a valid JSON value. The dynamic expression in this example includes a call to the `$ZDATE` function:

```
   set dynObj = { "Date":($ZD($H,3)) }
```

The evaluated dynamic expression value is displayed when we retrieve `dynObject.Date`:

```
   write "Value of dynamic expression is: "_dynObject.Date

Value of dynamic expression is: 2016-07-27
```

(See “Dynamic Expressions and Dot Syntax” for a detailed discussion of these topics).

### Convert between dynamic entities and canonical JSON strings

Dynamic entities have serialization methods that allow them to be converted to and from JSON strings. In the following example, a literal constructor is used to create a dynamic object, and the object's `%ToJSON()` method is called to serialize it to `myJSONstring`:

```
   set myJSONstring = {"aNumber":(21*2),"aDate":($ZD($H,3)),"anArray":["string",123]}.%ToJSON()
```

This serialized JSON object can be stored and retrieved like any other string. Class methods `%FromJSON()` and `%FromJSONFile()` can take a valid JSON string from any source and convert it to a dynamic object. The following code deserializes `myJSONstring` to dynamic object `myObject` and uses `%ToJSON()` to display it:

```
   set myObject = ##class(%DynamicAbstractObject).%FromJSON(myJSONstring)
   write myObject.%ToJSON()

{"aNumber":42,"aDate":"2016-08-29","anArray":["string",123]}
```

(See “Converting Dynamic Entities to and from JSON” for more information on serialization).

### Chain dynamic entity methods

Some dynamic entity methods can be chained. This example creates a dynamic array with two elements, and then chains the `%Push()` method to add three more elements to the end of the array. A final chained call to `%ToJSON()` displays the serialized string:

```
   set dynArray = ["a","b"]
   write dynArray.%Push(12).%Push({"a":1,"b":2}).%Push("final").%ToJSON()

["a","b",12,{"a":1,"b":2},"final"]
```

(See “Method Chaining” for more information on chainable methods).

### Iteration and datatype discovery

Dynamic entity methods are also provided for purposes such as iteration and datatype discovery. This example creates two JSON strings, deserializes one of them to `dynEntity` (either one will work), and then gets an iterator for `dynEntity` :

```
   set arrayStr = [12,"some string",[1,2]].%ToJSON()
   set objectStr = {"a":12,"b":"some string","c":{"x":1,"y":2}}.%ToJSON()
   set dynEntity = {}.%FromJSON(objectStr)
   set itr = dynEntity.%GetIterator()
```

For each iteration of the `while` loop, `%GetNext()` will return the property name or array index in `key` and the member value in `val`. The return value of `%GetTypeOf()` is a string indicating the datatype of the value:

```
   while itr.%GetNext(.key,.val) {write !,key_": "_"/"_val_"/, type: "_dynEntity.%GetTypeOf(key)}

a: /12/, type: number
b: /some string/, type: string
c: /1@%Library.DynamicObject/, type: object
```

(See “Iteration and Sparse Arrays” and “Working with Datatypes” for more information on these and related methods).

## Overview of Dynamic Entity Methods

Dynamic entity methods can be grouped into the following categories:

### Create, read, update, delete

`%Set()` can either change the value of an existing dynamic entity member (property or element), or create a new member and assign a value to it. `%Remove()` removes an existing member. `%Get()` retrieves the value of a member. See “Creating and Modifying Dynamic Entities” for details.

### Iteration and Sparse Arrays

`%GetIterator()` returns an iterator containing pointers to each member of a dynamic entity. `%GetNext()` returns the key and value of a member identified by the iterator, and advances the cursor to the next member. `%Size()` returns the number of members (including unassigned elements in a sparse array). `%IsDefined()` tests whether a member has an assigned value. See “Iteration and Sparse Arrays” for details.

### Stack functions

`%Push()` adds a new element to the end of a dynamic array. `%Pop()` removes the final element of the array and returns its value. These methods are not available for dynamic objects because object properties are not stored in a predictable sequence. See “Using %Push and %Pop with Dynamic Arrays” for details.

### JSON serialization and deserialization

`%FromJSON()` converts a JSON string, and `%FromJSONFile()` converts a JSON string stored within a file, to a dynamic entity. `%ToJSON()` serializes a dynamic entity to a canonical JSON string. See “Converting Dynamic Entities to and from JSON” for details.

### Datatype information

`%GetTypeOf()` returns a string indicating the datatype of a specified member value. `%Set()` and `%Push()` provide an optional third argument to explicitly specify the datatype of a value. See “Working with Datatypes” for details.

See the “Quick Reference for Dynamic Entity Methods” for a description of each method and links to further information.
