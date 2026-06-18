# Iteration and Sparse Arrays

Dynamic entities use a standard iteration method, `%GetNext()`, that works with both objects and arrays. You can also iterate over an array by addressing each element in sequence (with a `for` loop or similar structure), but this may require some knowledge of sparse arrays, which have elements that do not contain values. Since `%GetNext()` avoids problems by skipping those elements, it should be the preferred iteration method whenever possible.

This chapter discusses when and how to use each iteration method. The following topics are covered:

*   Iterating over a Dynamic Entity with %GetNext()
    
*   Understanding Sparse Arrays and Unassigned Values
    
    *   Sparse Array Iteration with %Size()
        
    *   Using %IsDefined() to Test for Valid Values
        
*   Using %Push and %Pop with Dynamic Arrays
    

## Iterating over a Dynamic Entity with %GetNext()

All dynamic entities provide the `%GetIterator()` method, which returns an instance of `%Iterator` (either %Iterator.Object or %Iterator.Array) containing pointers to members of the dynamic object or array. The `%Iterator` object provides a `%GetNext()` method to get the key and value of each member.

Each call to the `%GetNext()` method advances the iterator cursor and returns `1` (true) if it is positioned on a valid member or `0` (false) if it is beyond the last member. The name or index number of the member is returned in the first output argument and the value in the second. For example:

```
   set test = ["a","b","c"]  // dynamic arrays are zero-based
   set iter = test.%GetIterator()
   while iter.%GetNext(.key, .value) { write "element:"_key_"=/"_value_"/  "}

element:0=/a/  element:1=/b/  element:2=/c/
```

The iterator cursor only moves in one direction; it cannot go back to a previous member or iterate arrays in reverse order. `%GetNext()` return values become undefined when the elements of a dynamic entity are either deleted or added.

When iterating over a sparse array, the iterator skips elements with no assigned value. When iterating over an object, properties are not necessarily returned in a predictable order. The following examples demonstrate these differences between array iteration and object iteration.

### Iterating over an array

This example creates a sparse array. The array is zero-based and has six elements, but only elements `0`, `1`, and `5` have an assigned value. The null elements displayed in the JSON string are just placeholders for the unassigned values:

```
   set dynArray=["abc",999]
   set dynArray."5" = "final"
   write dynArray.%Size()_" elements: "_dynArray.%ToJSON()

6 elements: ["abc",999,null,null,null,"final"]
```

`%GetNext()` will return only the three elements with values, skipping all unassigned elements:

```
   set iterator=dynArray.%GetIterator()
   while iterator.%GetNext(.key,.val) { write !, "Element index: "_key_", value: "_val }

Element index: 0, value: abc
Element index: 1, value: 999
Element index: 5, value: final
```

See the next section (“Understanding Sparse Arrays and Unassigned Values”) for more on sparse arrays.

### Iterating over an object

Object properties have no fixed order, which means that properties can be created and destroyed in any order without creating unassigned values, but changing the object may also change the order in which properties are returned by `%GetNext()`. The following example creates an object with three properties, calls `%Remove()` to destroy one property, and then adds another property:

```
   set dynObject={"propA":"abc","PropB":"byebye","propC":999}
   do dynObject.%Remove("PropB")
   set dynObject.propD = "final"
   write dynObject.%Size()_" properties: "_dynObject.%ToJSON()

3 properties: {"propA":"abc","propD":"final","propC":999}
```

When we iterate over the object, `%GetNext()` does not return items in the order they were created:

```
   set iterator=dynObject.%GetIterator()
   while iterator.%GetNext(.key,.val) { write !, "Property name: """_key_""", value: "_val }

Property name: "propA", value: abc
Property name: "propD", value: final
Property name: "propC", value: 999
```

> **Note:**
> 
> `%GetNext()` return values become undefined when the elements of a %DynamicAbstractObject are either deleted or added. 

## Understanding Sparse Arrays and Unassigned Values

Dynamic arrays can be sparse arrays, meaning that not all elements of the array contain values. You can, for example, assign a value to element `100` of a dynamic array even if the array does not already contain elements `0` to `99`. Space in memory is allocated only for the value at element `100`. Elements `0` to `99` are unassigned, meaning that `0` to `99` are valid element identifiers but do not point to any values in memory. The `%Size()` method would return an array size of `101`, but the `%GetNext()` method would skip over the unassigned elements and return only the value in element `100`.

The following example creates a sparse array by assigning new values to elements `8` and `11`:

```
   set array = ["val_0",true,1,"",null,"val_5"] // values 0 through 5
   do array.%Set(8,"val_8")                     // undefined values 6 and 7 will be null
   set array."11" = "val_11"                    // undefined values 9 and 10 will be null
   write array.%ToJSON()

["val_0",true,1,"",null,"val_5",null,null,"val_8",null,null,"val_11"]
```

No values have been assigned to elements `6`, `7`, `9`, and `10`, and they take no space in memory, but they are represented in the JSON string by `null` values because JSON does not support undefined values.

### Using %Remove in sparse arrays

The `%Remove()` method treats an unassigned element just like any other element. It is possible to have an array that consists of nothing but unassigned values. The following example creates a sparse array and then removes unassigned element `0`. It then removes element `7`, which is now the only element containing a value:

```
   set array = []
   do array.%Set(8,"val_8")
   do array.%Remove(0)
   do array.%Remove(7)
   write "Array size = "_array.%Size()_":",!,array.%ToJSON()

Array size = 7:
[null,null,null,null,null,null,null]
```

See “Using %Set(), %Get(), and %Remove()” for more examples demonstrating `%Remove()`.

> **Note:**
> 
> JSON cannot preserve the distinction between null and unassigned values
> 
> Dynamic entities contain metadata that allows them to distinguish between `null` and `unassigned` values. JSON does not specify a separate `undefined` datatype, so there is no canonical way to preserve this distinction when a dynamic entity is serialized to a JSON string. If you do not want the extra `null` values in your serialized data, you must either remove the unassigned elements before serializing (see “Using %IsDefined() to Test for Valid Values”), or use some application-dependent means to record the distinction as metadata.

### Sparse Array Iteration with %Size()

The `%Size()` method returns the number of properties or elements in a dynamic entity. For example:

```
   set dynObject={"prop1":123,"prop2":[7,8,9],"prop3":{"a":1,"b":2}}
   write "Number of properties: "_dynObject.%Size()

Number of properties: 3
```

In sparse arrays, this number includes elements with unassigned values, as demonstrated in the following example. The array created in this example has six elements, but only elements `0`, `1`, and `5` have an assigned value. The null elements displayed in the JSON string are just placeholders for the unassigned values:

```
   set test=["abc",999]
   set test."5" = "final"
   write test.%Size()_" elements: "_test.%ToJSON()

6 elements: ["abc",999,null,null,null,"final"]
```

Elements `2`, `3`, and `4` do not have assigned values, but are still treated as valid array elements. Dynamic arrays are zero-based, so the index number of the final element will always be `%Size()-1`. The following example iterates through all six elements of array `test` in reverse order and uses `%Get()` to return their values:

```
   for i=(test.%Size()-1):-1:0 {write "element "_i_" = /"_test.%Get(i)_"/",!}

element 5 = /final/
element 4 = //
element 3 = //
element 2 = //
element 1 = /999/
element 0 = /abc/
```

The `%Get()` method will return `""` (empty string) for numbers greater than `%Size()-1`, and will throw an exception for negative numbers. See “Working with Datatypes” for information on how to distinguish between unassigned values, empty strings, and `null` values.

> **Note:**
> 
> The iteration technique shown here is useful only for specialized purposes (such detecting unassigned values in an array or iterating over an array in reverse order). In most cases you should use `%GetNext()`, which skips over unassigned elements and can be used for dynamic objects as well as dynamic arrays. See the previous section (“Iterating over a Dynamic Entity with %GetNext()”) for details.

### Using %IsDefined() to Test for Valid Values

The `%IsDefined()` method tests for the existence of a value at a specified property name or array index number. The method returns `1` (true) if the specified member has a value, and `0` (false) if the member does not exist. It will also return false for elements in a sparse array that do not have assigned values.

Unassigned values will be encountered if you use a `for` loop to iterate through a sparse array. The following example creates an array where the first three elements are a JSON `null`, an empty string, and an unassigned value. The `for` loop is deliberately set to go past the end of the array and test for an element with array index `4`:

```
   set dynarray = [null,""]
   set dynarray."3" = "final"
   write dynarray.%ToJSON()
[null,"",null,"final"]

   for index = 0:1:4 {write !,"Element "_index_": "_(dynarray.%IsDefined(index))}

Element 0: 1
Element 1: 1
Element 2: 0
Element 3: 1
Element 4: 0
```

`%IsDefined()` returns `0` in two cases: element `2` does not have an assigned value, and element `4` does not exist.

ObjectScript returns `""` (empty string) for JSON `null` values such as element `0` in this example. If you need to test for `""` and `null` as well as unassigned values, use `%GetTypeOf()` rather than `%IsDefined()` (see “Resolving Null, Empty String, and Unassigned Values”).

> **Note:**
> 
> As mentioned in the previous section, you should not use a `for` loop for iteration except in a few unusual situations. In most cases you should use the `%GetNext()` method, which skips unassigned values (see “Iterating over a Dynamic Entity with %GetNext()”).

The `%IsDefined()` method can also be used to test for the existence of an object property. The following code creates dynamic array `names` with three string values, and then uses the first two strings to create object `dynobj` with properties `prop1` and `prop2`.

```
   set names = ["prop1","prop2","noprop"]
   set dynobj={}.%Set(names."0",123).%Set(names."1",456)
   write dynobj.%ToJSON()

{"prop1":123,"prop2":456}
```

The following code uses `%IsDefined()` to determine which strings have been used as property names in `dynobj`:

```
   for name = 0:1:2 {write !,"Property "_names.%Get(name)_": "_(dynobj.%IsDefined(names.%Get(name)))}

Property prop1: 1
Property prop2: 1
Property noprop: 0
```

## Using %Push and %Pop with Dynamic Arrays

The `%Push()` and `%Pop()` methods are only available for dynamic arrays. They are work exactly like `%Set()` and `%Remove()` except that they always add or remove the last element of the array. For example, the following code produces the same results with either set of methods (see “Method Chaining” for details about calling `%Set()` or `%Push()` several times in the same statement):

```
   set array = []
   do array.%Set(array.%Size(), 123).%Set(array.%Size(), 456)
   write "removed "_array.%Remove(array.%Size()-1)_", leaving "_array.%ToJSON()

removed 456, leaving [123]

   set array = []
   do array.%Push(123).%Push(456)
   write "removed "_array.%Pop()_", leaving "_array.%ToJSON()

removed 456, leaving [123]
```

Although `%Push()` and `%Pop()` are intended for stack operations, you could implement a queue by substituting `%Remove(0)` for `%Pop()`.

The following example builds an array with `%Push()`, and then removes each element in reverse order with `%Pop()`.

### Using %Push() and %Pop() to build an array and tear it down

Build an array containing a nested array. The final call to `%Push()` specifies the optional `type` argument to store a boolean value as JSON `false` rather than ObjectScript `0` (see “Overriding a Default Datatype with %Set() or %Push()”):

```
   set array=[]
   do array.%Push(42).%Push("abc").%Push([])
   do array."2".%Push("X").%Push(0,"boolean")
   write array.%ToJSON()

[42,"abc",["X",false]]
```

Remove all elements of the nested array. Like all dynamic entity methods, `%Pop()` will return ObjectScript `0` rather than JSON `false`:

```
   for i=0:1:1 {write "/"_array."2".%Pop()_"/ "}
/0/ /X/

   write array.%ToJSON()
[42,"abc",[]]
```

Now remove all elements of the main array, including the empty nested array:

```
   for i=0:1:2 {write "/"_array.%Pop()_"/ "}
/2@%Library.DynamicArray/ /abc/ /42/

   write array.%ToJSON()
[]
```

These examples use hard coded `for` loops for simplicity. See “Sparse Array Iteration with %Size()” for more realistic examples of array iteration.
