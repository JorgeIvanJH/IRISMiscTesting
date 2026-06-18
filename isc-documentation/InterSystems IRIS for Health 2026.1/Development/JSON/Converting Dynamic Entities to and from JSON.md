# Converting Dynamic Entities to and from JSON

You can use the `%ToJSON()` method to serialize a dynamic entity (convert it to a JSON string) and the `%FromJSON()` and `%FromJSONFile()` methods to deserialize (convert JSON to a dynamic entity).

## Serializing a dynamic entity to JSON

The following example creates and modifies a dynamic object, and then uses `%ToJSON()` to serialize it and display the resulting string:

```
   set dynObject={"prop1":true}.%Set("prop2",123).%Set("prop3","foo")
   set objString = dynObject.%ToJSON()
   write objString

{"prop1":true,"prop2":123,"prop3":"foo"}
```

A dynamic array is serialized in the same way:

```
   set dynArray=[].%Push("1st value").%Push("2nd value").%Push("3rd value")
   set arrayString = dynArray.%ToJSON()
   write arrayString

["1st value","2nd value","3rd value"]
```

Both of these examples use method chaining (see “Method Chaining” earlier in this chapter).

## Deserializing from JSON to a dynamic object

The `%FromJSON()` method converts a JSON string to a dynamic entity. The following example constructs a dynamic array and serializes it to string `jstring`. A call to `%FromJSON()` deserializes `jstring` to a new dynamic entity named `newArray`, which is then modified and displayed:

```
   set jstring=["1st value","2nd value","3rd value"].%ToJSON()
   set newArray={}.%FromJSON(jstring)
   do newArray.%Push("new value")
   write "New entity:"_newArray.%ToJSON()

New entity:["1st value","2nd value","3rd value","new value"]
```

Notice this example calls `%FromJSON()` from a dynamic object constructor (`{}`) even though the returned value is a dynamic array. `%FromJSON()` is a class method of %DynamicAbstractObject, and can therefore be called from any dynamic entity or constructor.

If you have JSON data stored in a `.json` file, you can deserialize the data by using the `%FromJSONFile()` method instead of `%FromJSON()`.

## Cloning with %ToJSON() and %FromJSON()

Since each call to `%FromJSON()` creates a new dynamic entity, it can be used to duplicate an existing entity or initialize a set of identical entities.

In the following example, the value of property `dynObj.address` is a dynamic object. The property is referenced by variable `addrPointer`, and the property value is cloned by calling `%FromJSON()` to create new dynamic object `addrClone`:

```
   set dynObj = {}.%FromJSON({"name":"greg", "address":{"road":"Dexter Ave."}}.%ToJSON())
   set addrPointer = dynObj.address
   set addrClone = {}.%FromJSON(dynObj.address.%ToJSON())
```

Variable `addrPointer` is just a reference to property `dynObj.address`, but `addrClone` is an independent instance of %DynamicObject that can be modified without affecting the original value:

```
   set addrPointer.road = "Wright Ave."
   set addrClone.road = "Sinister Ave."
   write !,"Property = "_dynObj.address.%ToJSON(),!,"Clone = "_addrClone.%ToJSON()

Property = {"road":"Wright Ave."}
Clone = {"road":"Sinister Ave."}
```

If you have JSON data stored in a `.json` file, you can clone the data by using the `%FromJSONFile()` method instead of `%FromJSON()`.

## Serializing Large Dynamic Entities to Streams

If a dynamic entity is large enough, the output of `%ToJSON()` may exceed the maximum possible length for a string (see “String Length Limit”). The examples in this section use a maximum length string named `longStr`. The following code fragment demonstrates how `longStr` is generated:

```
   set longStr=""
   for i=1:1:$SYSTEM.SYS.MaxLocalLength() { set longStr = longStr_"x" }
   write "Maximum string length = "_$LENGTH(longStr)

Maximum string length = 3641144
```

Whenever an expression uses the return value of `%ToJSON()`, the string is built on the program stack, which is subject to the string length limit. For example, a read/write statement such as `write dyn.%ToJSON()` or an assignment statement such as `set x=dyn.%ToJSON()` will attempt to put the string on the stack. The following example adds two copies of `longStr` to a dynamic array and attempts to assign the serialized string to a variable, causing ObjectScript to return a `<MAXSTRING>` error:

```
   set longArray = [(longStr),(longStr)]
   set tooBig = longArray.%ToJSON()
```

```
SET tooBig = longArray.%ToJSON()
^
<MAXSTRING>
```

The general solution to this problem is to pass the `%ToJSON()` output by reference in a `DO` command, without actually examining the return value. Output is written directly to the current device, and there is no limit on the length of the output. In the following examples, the device is a stream.

### Writing to a file stream

This example writes dynamic object `longObject` to a file and then retrieves it. Variable `longStr` is the value defined at the beginning of this section:

```
   set longStr=""
   for i=1:1:$SYSTEM.SYS.MaxLocalLength() { set longStr = longStr_"x" }
   set longObject = {"a":(longStr),"b":(longStr)}
   set file=##class(%File).%New("c:\temp\longObjectFile.txt")
   do file.Open("WSN")
   do longObject.%ToJSON(file)
   do file.Close()

   set newObject = {}.%FromJSONFile(file.Name)
   write !,"Property newObject.a is ",$LENGTH(newObject.a)," characters long."

Property newObject.a is 3641144 characters long.
```

This solution can also be used to read input from other streams.

### Reading and writing global character streams

In this example, we serialize two large dynamic entities (using temporary streams because `%ToJSON()` can only serialize one entity per stream). Standard stream handling methods are used to store each temporary stream as a separate line in stream `bigLines`:

```
   set tmpArray = ##class(%Stream.GlobalCharacter).%New()
   set dyn = [(longStr),(longStr)]
   do dyn.%ToJSON(tmpArray)

   set tmpObject = ##class(%Stream.GlobalCharacter).%New()
   set dyn = {"a":(longStr),"b":(longStr),"c":(longStr)}
   do dyn.%ToJSON(tmpObject)

   set bigLines = ##class(%Stream.GlobalCharacter).%New()
   do bigLines.CopyFrom(tmpArray)
   do bigLines.WriteLine()
   do bigLines.CopyFrom(tmpObject)
```

Later, we can deserialize each dynamic entity from `bigLines`:

```
   do bigLines.Rewind()
   while ('bigLines.AtEnd) {
      write !,{}.%FromJSON(bigLines.ReadLineIntoStream())
   }

7@%Library.DynamicArray
7@%Library.DynamicObject
```
