# Quick Reference for Dynamic Entity Methods

This section provides an overview and references for each of the available dynamic entity methods. Dynamic entities are instances of %Library.DynamicObject or %Library.DynamicArray, both of which extend %Library.DynamicAbstractObject. Each listing in this chapter includes a link to the appropriate online class reference documentation.

## Method Details

This section lists all available dynamic entity methods, briefly describing each one and providing links to further information. All methods are available for both objects and arrays, with the exception of `%Push()` and `%Pop()`, which apply only to arrays.

### %FromJSON()

Given a valid JSON string, parse it and return an object of datatype %DynamicAbstractObject containing the parsed JSON. If an error occurs during parsing, an exception will be thrown. See “Converting Dynamic Entities to and from JSON” for details and examples.

```
   classmethod %FromJSON(str) as %DynamicAbstractObject
```

parameters:

*   `str` — The input can be from any one of the following sources:
    
    *   string value containing the source. The value can be an empty string (`""`), but an error will be thrown if the string contains only white space characters.
        
    *   stream object to read the source from. An error will be thrown if the stream does not contain any characters.
        

see also: `%FromJSONFile()`, `%ToJSON()`, Serializing Large Dynamic Entities to Streams

class reference: `%DynamicAbstractObject.`%FromJSON()

### %FromJSONFile()

Given a valid JSON source, parse the source and return an object of datatype %DynamicAbstractObject containing the parsed JSON. See “Converting Dynamic Entities to and from JSON” for details and examples.

```
   classmethod %FromJSONFile(filename) as %DynamicAbstractObject
```

parameters:

*   `filename` — name of file URI where the source can be read. The file must be encoded as UTF-8. An exception will be thrown if the file does not contain any characters.
    

see also: `%FromJSON()`, `%ToJSON()`, Serializing Large Dynamic Entities to Streams

class reference: `%DynamicAbstractObject.`%FromJSON()

### %Get()

Given a valid object key or array index, returns the value. If the value does not exist, a null string `""` is returned. See “Using %Set(), %Get(), and %Remove()” for details and examples.

```
   method %Get(key, default, type) as %RawString
```

parameters:

*   `key` — the object key or array index of the value to be retrieved. An array index must be passed as a canonical integer value.
    
    Note that Array indexes begin at position 0, unlike most array structures in InterSystems IRIS.
    
*   `default` — optional value to be returned when the selected array element is undefined. Defaults to empty string if not specified.
    
*   `type` — if defined, indicates that the value of `key` should be returned as the specified type (see `%DynamicObject.`%Get() and `%DynamicArray.`%Get() for details on how values are converted). If this argument is specified, the value must be one of the following strings:
    
    *   `""` (empty string) — same as calling %Get(key) without conversions
        
    *   `"string"` — convert to text string
        
    *   `"string>base64"` — convert to text string then encode into base64
        
    *   `"string<base64"` — convert to text string then decode from base64
        
    *   `"stream"` — place string conversion into %Stream
        
    *   `"stream>base64"` — string encoded into base64 into %Stream
        
    *   `"stream<base64"` — string decoded from base64 into %Stream
        
    *   `"json"` — convert to JSON representation
        

see also: `%Set()`, `%Remove()`, `%Pop()`

class reference: `%DynamicObject.`%Get() and `%DynamicArray.`%Get()

### %GetIterator()

Returns a `%Iterator` object allowing iteration over all members of a dynamic entity. See “Iterating over a Dynamic Entity with %GetNext()” for details and examples.

```
   method %GetIterator() as %Iterator.AbstractIterator
```

see also: `%GetNext()`

class reference: `%DynamicObject.`%GetIterator(), `%DynamicArray.`%GetIterator(), %Iterator.Object, %Iterator.Array

### %GetNext()

This is a method of the `%Iterator` object returned by `%GetIterator()`. It advances the iterator and returns `true` if the iterator is positioned on a valid element, `false` if it is beyond the last element. The `key` and `value` arguments return values for a valid element at the current iterator position. The optional `type` argument returns the original type of `value`. See “Iterating over a Dynamic Entity with %GetNext()” for details and examples.

```
   method getNext(Output key, Output value, Output type...) as %Integer
```

parameters:

*   `key` — returns the object key or array index of the element at the current position
    
*   `value` — returns the value of the element at the current position.
    
*   `type` — (optional) returns a string containing a `%GetTypeOf()` return value representing the original type of `value`. When this third argument variable is present it changes some of the conversion rules for converting the element into an ObjectScript value (see `%Iterator.Object.`%GetNext() and `%Iterator.Array.`%GetNext() for detailed conversion rules).
    

see also: `%GetIterator()`

class reference: `%Iterator.Object.`%GetNext() and `%Iterator.Array.`%GetNext()

### %GetTypeOf()

Given a valid object key or array index, returns a string indicating the datatype of the value. See “Working with Datatypes” for details and examples.

```
   method %GetTypeOf(key) as %String
```

parameters:

*   `key` — the object key or array index of the value to be tested.
    

return values:

One of the following strings will be returned:

*   `"null"` — a JSON null
    
*   `"boolean"` — a zero (“false”) or non-zero (“true”) numeric value
    
*   `"number"` — any canonical numeric value
    
*   `"oref"` — a reference to another object
    
*   `"object"` — a nested object
    
*   `"array"` — a nested array
    
*   `"string"` — a standard text string
    
*   `"unassigned"` — the property or element exists, but does not have an assigned value
    

see also: `%IsDefined()`

class reference: `%DynamicAbstractObject.`%GetTypeOf()

### %IsDefined()

Tests if the item specified by `key` is defined within an object. Returns false if the item is unassigned or does not exist. See “Using %IsDefined() to Test for Valid Values” for details and examples.

```
   method %IsDefined(key) as %Boolean
```

parameters:

*   `key` — the object key or array index of the item to be tested. An array index must be passed as a canonical integer value. Array indexes begin at position 0.
    

see also: Resolving Null, Empty String, and Unassigned Values

class reference: `%DynamicObject.`%IsDefined() and `%DynamicArray.`%IsDefined()

### %Pop()

Returns the value of the last member of the array. The value is then removed from the array. If the array is already empty, the method returns the empty string, `""`. See “Using %Push and %Pop with Dynamic Arrays” for details and examples.

```
   method %Pop() as %RawString
```

see also: `%Push()`, `%Get()`, `%Remove()`, Resolving Null, Empty String, and Unassigned Values

class reference: `%DynamicArray.`%Pop()

### %Push()

Append a new value to the end of the current array, increasing the length of the array. Returns an oref pointing to the current modified array so that calls to `%Push()` can be chained. See “Using %Push and %Pop with Dynamic Arrays” for details and examples.

```
   method %Push(value, type) as %DynamicAbstractObject
```

parameters:

*   `value` — value to be assigned to the new array element.
    
*   `type` — (Optional) string indicating the datatype of `value` (see `%DynamicArray.`%Push() for details on how values are converted). The following strings may be used:
    
    *   `"null"` — a JSON `null`. The `value` argument must be `""` (empty string).
        
    *   `"boolean"` — zero/nonzero becomes JSON false/true
        
    *   `"number"` — convert `value` to a canonical numeric value
        
    *   `"string"` — convert `value` to a text string
        
    *   `"string>base64"`   — convert to text string then encode into base64
        
    *   `"string<base64"`   — convert to text string then decode from base64
        
    *   `"stream"`      — %Stream contents converted to text string
        
    *   `"stream>base64"` — %Stream contents are encoded into base64 string
        
    *   `"stream<base64"` — %Stream is decoded from base64 into byte string
        
    
    NOTE: The optional `type` parameter cannot be used if the specified `value` is an object or an oref. For example, if the specified `value` is a dynamic entity, an error will be thrown no matter what value you specify for `type`. See “Overriding a Default Datatype with %Set() or %Push()” for more information.
    

see also: `%Pop()`, `%Set()`, Method Chaining

class reference: `%DynamicArray.`%Push()

### %Remove()

Removes the specified element from a dynamic object or array, and returns the value of the removed element. If the value of the element is an embedded dynamic object or array, all subordinate nodes are removed as well. In a dynamic array, all elements following the removed element will have their subscript position decremented by 1. See “Using %Set(), %Get(), and %Remove()” for details and examples.

```
   method %Remove(key) as %DynamicAbstractObject
```

parameters:

*   `key` — the object key or array index of the element you wish to remove. An array index must be passed as a canonical integer value. Array indexes begin at position 0.
    

see also: `%Set()`, `%Get()`, `%Pop()`

class reference: `%DynamicObject.`%Remove() and `%DynamicArray.`%Remove()

### %Set()

Create a new value or update an existing value. Returns a reference to the modified array, allowing calls to `%Set()` to be nested. See “Using %Set(), %Get(), and %Remove()” for details and examples.

```
   method %Set(key, value, type) as %DynamicAbstractObject
```

parameters:

*   `key` — object key or array index of the value you wish to create or update. An array index must be passed as a canonical integer value. Array indexes begin at position 0.
    
*   `value` — new value with which to update the previous value or create a new value.
    
*   `type` — (Optional) string indicating the datatype of `value` (see `%DynamicObject.`%Set() and `%DynamicArray.`%Set() for details on how values are converted). The following strings may be used:
    
    *   `"null"` — a JSON `null`. The `value` argument must be `""` (empty string).
        
    *   `"boolean"` — a JSON `false` (`value` argument must be `0`) or `true` (`value` argument must be `1`).
        
    *   `"number"` — convert `value` to a canonical numeric value
        
    *   `"string"` — convert `value` to a text string
        
    *   `"string>base64"`   — convert to text string then encode into base64
        
    *   `"string<base64"`   — convert to text string then decode from base64
        
    *   `"stream"`      — %Stream contents converted to text string
        
    *   `"stream>base64"` — %Stream contents are encoded into base64 string
        
    *   `"stream<base64"` — %Stream is decoded from base64 into byte string
        
    
    NOTE: The optional `type` parameter cannot be used if the specified `value` is an object or an oref. For example, if the specified `value` is a dynamic entity, an error will be thrown no matter what value you specify for `type`. See “Overriding a Default Datatype with %Set() or %Push()” for more information.
    

see also: `%Get()`, `%Remove()`, `%Push()`, Method Chaining

class reference: `%DynamicObject.`%Set() and `%DynamicArray.`%Set()

### %Size()

Returns an integer showing the size of a dynamic object or array. In the case of an array, the size includes unassigned entries within the array. In the case of an object, the size only includes elements that have assigned values. See “Sparse Array Iteration with %Size()” for details and examples.

```
   method %Size() as %Integer
```

see also: `%GetNext()`

class reference: `%DynamicAbstractObject.`%Size()

### %ToJSON()

Converts an instance of `%DynamicAbstractObject.` into a JSON string. If `%ToJSON()` doesn’t return an error, it will always return a string containing at least two characters ([] for an array or {} for an object). See “Converting Dynamic Entities to and from JSON” for details and examples.

```
   method %ToJSON(outstrm As %Stream.Object) as %String
```

parameters:

*   `outstrm` — optional. There are a number of possibilities:
    
    *   If `outstrm` is not specified and the method is called via `DO`, the JSON string is written to the current output device.
        
    *   If `outstrm` is not specified and the method is called as an expression, the JSON string becomes the value of the expression.
        
    *   If `outstrm` is specified as an instance of %Stream.Object, the JSON string will be written to the stream (see “Serializing Large Dynamic Entities to Streams” for details and examples).
        
    *   If `outstrm` is an object but is not an instance of %Stream.Object then an exception will be thrown.
        
    *   If `outstrm` is not an object and is not null then it is presumed to be a fully qualified file specification (the full path to the file must be defined). The file is linked to a newly created %Stream.FileCharacter stream, the JSON string is written to the stream, and the stream is saved to the file on completion.
        

see also: `%FromJSON()`, `%FromJSONFile()`

class reference: `%DynamicAbstractObject.`%ToJSON()
