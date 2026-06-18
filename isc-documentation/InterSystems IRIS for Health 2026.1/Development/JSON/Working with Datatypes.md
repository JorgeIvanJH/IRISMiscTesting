# Working with Datatypes

ObjectScript has no distinct constants equivalent to JSON `true`, `false`, and `null`, and JSON has no concept of array elements with undefined values. This chapter discusses these mismatches and describes the tools provided to deal with them.

*   Discovering the Datatype of a Value with %GetTypeOf()
    
*   Overriding a Default Datatype with %Set() or %Push()
    
*   Resolving JSON Null and Boolean Values
    
*   Resolving Null, Empty String, and Unassigned Values
    

## Discovering the Datatype of a Value with %GetTypeOf()

You can use the `%GetTypeOf()` method to get the datatype of a dynamic entity member. A dynamic object property or array element can have any one of following datatypes:

*   An object datatype:
    
    *   `array` — a dynamic array reference
        
    *   `object` — a dynamic object reference
        
    *   `oref` — a reference to an object that is not a dynamic entity
        
*   A literal value:
    
    *   `number` — a canonical numeric value
        
    *   `string` — a string literal or an expression that evaluates to a string literal
        
*   A JSON literal:
    
    *   `boolean` — a JSON literal `true` or `false`
        
    *   `null` — a JSON literal `null`
        
*   No datatype:
    
    *   `unassigned` — the property or element exists, but has no assigned value.
        

### Using %GetTypeOf with objects

When you use this method with an object, the argument is the name of the property. For example:

```
   set dynobj={"prop1":123,"prop2":[7,8,9],"prop3":{"a":1,"b":2}}
   set iter = dynobj.%GetIterator()
   while iter.%GetNext(.name) {write !,"Datatype of "_name_" is "_(dynobj.%GetTypeOf(name))}

Datatype of prop1 is number
Datatype of prop2 is array
Datatype of prop3 is object
```

### Using %GetTypeOf with arrays

When you use this method with an array, the argument is the index of the element. The following example examines a sparse array, where element `2` does not have an assigned value. The example uses a `for` loop because `%GetNext()` would skip the unassigned element:

```
   set dynarray = [12,34]
   set dynarray."3" = "final"
   write dynarray.%ToJSON()
[12,34,null,"final"]

   for index = 0:1:3 {write !,"Datatype of "_index_" is "_(dynarray.%GetTypeOf(index))}
Datatype of 0 is number
Datatype of 1 is number
Datatype of 2 is unassigned
Datatype of 3 is string
```

### `array`

Distinguishing between or `object` and `oref`

The datatype of a dynamic entity will be either `array` or `object`. An InterSystems IRIS object that is not a dynamic entity will be datatype `oref`. In the following example, each property of object `dyn` is one of these three datatypes. Property `dynobject` is class %DynamicObject, property `dynarray` is %DynamicArray, and property `streamobj` is %Stream.GlobalCharacter:

```
   set dyn={"dynobject":{"a":1,"b":2},"dynarray":[3,4],"streamobj":(##class(%Stream.GlobalCharacter).%New())}
   set iterator=dyn.%GetIterator()
   while iterator.%GetNext(.key,.val) { write !, "Datatype of "_key_" is: "_dyn.%GetTypeOf(key) }

Datatype of dynobject is: object
Datatype of dynarray is: array
Datatype of streamobj is: oref
```

## Overriding a Default Datatype with %Set() or %Push()

By default, the system automatically interprets a `%Set()` or `%Push()` value argument as an object datatype (`object`, `array`, or `oref`) or an ObjectScript literal datatype (`string` or `number`). You can not directly pass JSON literals `null`, `true` or `false` as values because the argument is interpreted as an ObjectScript literal or expression. For example, the following code throws an error because the value `true` is interpreted as a variable name:

```
   do o.%Set("prop3",true)

DO o.%Set("prop3",true)
^
<UNDEFINED> *true
```

ObjectScript uses `""` (an empty string) for null, `0` for boolean false, and a non-zero number for boolean true. To deal with this problem, `%Set()` and `%Push()` take an optional third argument to specify the datatype of the value. The third argument can be JSON `boolean` or `null`. For example:

```
   write {}.%Set("a",(2-4)).%Set("b",0).%Set("c","").%ToJSON()
{"a":-2,"b":0,"c":""}

   write {}.%Set("a",(2-4),"boolean").%Set("b",0,"boolean").%Set("c","","null").%ToJSON()
{"a":true,"b":false,"c":null}
```

The third argument can also be `string` or `number` if the value could be interpreted as a number:

```
   write [].%Push("023"_"04").%Push(5*5).%ToJSON()
["02304",25]

   write [].%Push(("023"_"04"),"number").%Push((5*5),"string").%ToJSON()
[2304,"25"]
```

## Resolving JSON Null and Boolean Values

In JSON syntax, the values `true`, `false`, and `null` are distinct from values `1`, `0`, and `""` (empty string), but ObjectScript does not make this distinction. When JSON values are retrieved from an element or property, they are always cast to ObjectScript-compatible values. This means that JSON `true` is always returned as `1`, `false` as `0`, and `null` as `""`. In most cases this will be the desired result, since the return value can be used in an ObjectScript expression without first converting it from JSON format. The dynamic entity retains the original JSON or ObjectScript value internally, so you can use `%GetTypeOf()` to identify the actual datatype if necessary.

In the following example, the dynamic array constructor specifies JSON `true`, `false`, and `null` values, numeric and string literal values, and ObjectScript dynamic expressions (which evaluate to ObjectScript boolean values `1` and `0`):

```
   set test = [true,1,(1=1),false,0,(1=2),"",null]
   write test.%ToJSON()
```

```
[true,1,1,false,0,0,"",null]
```

As you can see above, the values assigned in the constructor have been preserved in the resulting dynamic array, and are displayed properly when serialized as a JSON string.

The following example retrieves and displays the array values. As expected, JSON values `true`, `false`, and `null` are cast to ObjectScript-compatible values `1`, `0`, and `""`:

```
   set iter = test.%GetIterator()
   while iter.%GetNext(.key,.val){write "/"_val_"/ "}
```

```
/1/ /1/ /1/ /0/ /0/ /0/ // //
```

This example uses `%GetNext()`, but you would get the same results if you retrieved values with `%Get()`, `%Pop()`, or dot syntax.

When necessary, you can use the `%GetTypeOf()` method to discover the original datatype of the value. For example:

```
   set iter = test.%GetIterator()
   while iter.%GetNext(.key,.val) {write !,key_": /"_test.%Get(key)_"/ = "_test.%GetTypeOf(key)}
```

```
0: /1/ = boolean
1: /1/ = number
2: /1/ = number
3: /0/ = boolean
4: /0/ = number
5: /0/ = number
6: // = string
7: // = null
```

> **Note:**
> 
> Datatypes in Dynamic Objects
> 
> Although this chapter concentrates on dynamic arrays, the same datatype conversions apply to dynamic object values. The examples in this section will work exactly the same if dynamic array `test` is replaced with the following dynamic object:
> 
> ```
>    set test = {"0":true,"1":1,"2":(1=1),"3":false,"4":0,"5":(1=2),"6":"","7":null}
> ```
> 
> Except for this line, none of the example code has to be changed. The property names in this object are numeric strings corresponding to the index numbers of the original array, so even the output will be identical.

## Resolving Null, Empty String, and Unassigned Values

Although you can assign a JSON `null` value to an element or property, the value will always be returned as `""` (ObjectScript empty string). An empty string will also be returned if you attempt to get the value of an unassigned element. You can use `%GetTypeOf()` to identify the actual datatype in each case.

This example will test a sparse array containing a JSON `null` value and an empty string. Although array element `2` has no assigned value, it will be represented in the JSON string by a `null`:

```
   set array = [null,""]
   do array.%Set(3,"last")
   write array.%ToJSON()
```

```
[null,"",null,"last"]
```

In most cases you would use `%GetNext()` to retrieve array values, but this example uses a `for` loop to return unassigned values that `%GetNext()` would skip. The index number of the last element is `array.%Size()-1`, but the loop counter is deliberately set to go past the end of the array:

```
   for i=0:1:(array.%Size()) {write !,i_". value="""_array.%Get(i)_""" type="_array.%GetTypeOf(i)}
```

```
0. value="" type=null
1. value="" type=string
2. value="" type=unassigned
3. value="last" type=string
4. value="" type=unassigned
```

In this example, `%Get()` returns an empty string in four different cases:

1.  element `0` is a JSON `null` value, which `%GetTypeOf()` identifies as datatype `null`.
    
2.  element `1` is an empty string, which is identified as datatype `string`.
    
3.  Element `2` has no value, and is identified as datatype `unassigned`.
    
4.  Although element `3` is the last one in the array, the example attempts to get a datatype for non-existent element `4`, which is also identified as datatype `unassigned`. Valid array index numbers will always be less than `array.%Size()`.
    

> **Note:**
> 
> The distinction between `null` and `unassigned` is ObjectScript metadata that will not be preserved when a dynamic entity is serialized to a JSON string. All `unassigned` elements will be serialized as `null` values. See “Understanding Sparse Arrays and Unassigned Values” for details.
