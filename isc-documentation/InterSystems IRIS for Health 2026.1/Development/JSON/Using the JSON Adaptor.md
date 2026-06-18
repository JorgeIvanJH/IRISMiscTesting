# Using the JSON Adaptor

The JSON Adaptor is a means for mapping ObjectScript objects (registered, serial or persistent) to JSON text or dynamic entities. This chapter covers the following topics:

*   Exporting and Importing — introduces JSON enabled objects and demonstrates %JSON.Adaptor import and export methods.
    
*   Mapping with Parameters — describes property parameters that control how object properties are converted to JSON fields.
    
*   Using XData Mapping Blocks — describes a way to apply multiple parameter mappings to a single class.
    
*   Formatting JSON — demonstrates how to format JSON strings with %JSON.Formatter.
    
*   %JSON Quick Reference — provides a brief description of each %JSON class member discussed in this chapter.
    

## Exporting and Importing

Any class you would like to serialize from and to JSON needs to subclass %JSON.Adaptor, which includes the following methods:

*   %JSONExport() serializes a JSON enabled class as a JSON document and writes it to the current device.
    
*   %JSONExportToStream() serializes a JSON enabled class as a JSON document and writes it to a stream.
    
*   %JSONExportToString() serializes a JSON enabled class as a JSON document and returns it as a string.
    
*   %JSONImport() imports either JSON as a string or stream, or a subclass of %DynamicAbstractObject, and returns an instance of the JSON enabled class.
    

To demonstrate these methods, the examples in this section will use these two classes:

### JSON enabled classes Model.Event and Model.Location

```
  Class Model.Event Extends (%Persistent, %JSON.Adaptor)
  {
    Property Name As %String;
    Property Location As Model.Location;
  }
```

and

```
  Class Model.Location Extends (%Persistent, %JSON.Adaptor)
  {
    Property City As %String;
    Property Country As %String;
  }
```

As you can see, we have a persistent event class, which links to a location. Both classes inherit from %JSON.Adaptor. This enables us to populate an object graph and directly export it as a JSON string.

### Exporting an object to a JSON string

```
  set event = ##class(Model.Event).%New()
  set event.Name = "Global Summit"
  set location = ##class(Model.Location).%New()
  set location.City = "Boston"
  set location.Country = "United States of America"
  set event.Location = location
  do event.%JSONExport()
```

This code displays the following JSON string:

```
  {"Name":"Global Summit","Location":{"City":"Boston","Country":"United States of America"}}
```

You can assign the JSON string to a variable by using `%JSONExportToString()` instead of `%JSONExport()`:

```
  do event.%JSONExportToString(.jsonEvent)
```

Finally, you can reverse the process and convert the JSON string back to an object with `%JSONImport()`. This example takes string variable `jsonEvent` from the previous example and converts it back to a `Model.Event` object:

### Importing a JSON string into an object

```
  set eventTwo = ##class(Model.Event).%New()
  do eventTwo.%JSONImport(jsonEvent)
  write eventTwo.Name,!,eventTwo.Location.City
```

writes:

```
  Global Summit
  Boston
```

Both import and export work for arbitrarily nested structures.

## Mapping with Parameters

You can specify the mapping logic for each individual property by setting corresponding parameters. (If you are familiar with the %XML.Adaptor, this is a similar process).

We can change the mapping for the `Model.Event` class (defined in the previous section) by specifying property parameters:

```
  Class Model.Event Extends (%Persistent, %JSON.Adaptor)
  {
    Property Name As %String(%JSONFIELDNAME = "eventName");
    Property Location As Model.Location(%JSONINCLUDE = "INPUTONLY");
  }
```

This mapping introduces two changes:

*   The property `Name` will be mapped to a JSON field named `eventName`.
    
*   The `Location` property will still be used as input by `%JSONImport()`, but will be ignored by `%JSONExport()` and other export methods.
    

Previously, `%JSONExport()` was called on an instance of the unmodified `Model.Event` class, and the following JSON string was returned:

```
  {"Name":"Global Summit","Location":{"City":"Boston","Country":"United States of America"}}
```

If we call `%JSONExport()` on an instance of the remapped `Model.Event` (using the same property values), the following string will be returned:

```
  {"eventName":"Global Summit"}
```

There are various parameters available to allow you to tweak the mapping:

*   %JSONFIELDNAME (properties only) sets the string to be used as the field name in JSON content (value is the property name by default).
    
*   %JSONIGNOREINVALIDFIELD controls handling of unexpected fields in the JSON input.
    
*   %JSONIGNORENULL allows the developer to override the default handling of empty strings for string properties.
    
*   %JSONINCLUDE (properties only) specifies whether this property will be included in the JSON output or input (valid values are `"inout"` (the default), `"outputonly"`, `"inputonly"`, or `"none"`).
    
*   %JSONNULL specifies how to store empty strings for string properties.
    
*   %JSONREFERENCE specifies how to project object references to JSON fields. Options are `"OBJECT"` (the default), `"ID"`, `"OID"` and `"GUID"`.
    

See the reference section “%JSON.Adaptor Class and Property Parameters” later in this chapter for more information.

## Using XData Mapping Blocks

Instead of setting the mapping parameters on the property level, you can specify a mapping in a special XData Mapping block and apply the mapping when you call an import or export method.

The following code defines another version of the `Model.Event` class used in the previous two sections. In this version, no property parameters are specified, but we define an XData Mapping block named `OnlyLowercaseTopLevel` that specifies the same parameter settings as the properties in the previous version:

```
  Class Model.Event Extends (%Persistent, %JSON.Adaptor)
  {
    Property Name As %String;
    Property Location As Model.Location;

    XData OnlyLowercaseTopLevel
    {
      <Mapping xmlns="http://www.intersystems.com/jsonmapping">
        <Property Name="Name" FieldName="eventName"/>
        <Property Name="Location" Include="INPUTONLY"/>
      </Mapping>
    }
  }
```

There is one important difference: JSON mappings in XData blocks do not change the default behavior, but you can apply them by specifying the block name in the optional `%mappingName` parameter of the import and export methods. For example:

```
  do event.%JSONExport("OnlyLowercaseTopLevel")
```

displays:

```
  {"eventName":"Global Summit"}
```

just as if the parameters had been specified in the property definitions.

If there is no XData block with the provided name, the default mapping will be used. With this approach, you can configure multiple mappings and reference the mapping you need for each call individually, granting you even more control while making your mappings more flexible and reusable.

### Defining an XData Mapping Block

A JSON enabled class can define an arbitrary number of additional mappings. Each mapping is defined in a separate XData block of the following form:

```
  XData {MappingName}
  {
    <Mapping  {ClassAttribute}="value" [...] xmlns="http://www.intersystems.com/jsonmapping".>
      <{Property Name}="PropertyName" {PropertyAttribute}="value" [...] />
      [... more Property elements]
    </Mapping>
  }
```

where `{MappingName}`, `{ClassAttribute}`, `{Property Name}`, and `{PropertyAttribute}` are defined as follows:

*   `MappingName`
    
    The name of the mapping for use by the %JSONREFERENCE parameter or Reference attribute.
    
*   `ClassAttribute`
    
    Specifies a class parameter for the mapping. The following class attributes can be defined:
    
    *   `Mapping` — name of an XData mapping block to apply.
        
    *   `IgnoreInvalidField` — specifies class parameter %JSONIGNOREINVALIDFIELD.
        
    *   `Null` — specifies class parameter %JSONNULL.
        
    *   `IgnoreNull` — specifies class parameter %JSONIGNORENULL.
        
    *   `Reference` — specifies class parameter %JSONREFERENCE.
        
*   `PropertyName`
    
    The name of the property which is being mapped.
    
*   `PropertyAttribute`
    
    Specifies a property parameter for the mapping. The following property attributes can be defined:
    
    *   `FieldName` — specifies property parameter %JSONFIELDNAME (same as property name by default).
        
    *   `Include` — specifies property parameter %JSONINCLUDE (valid values are `"inout"` (the default), `"outputonly"`, `"inputOnly"`, or `"none"`).
        
    *   `Mapping` — name of a mapping definition to apply to an object property.
        
    *   `Null` — overrides class parameter %JSONNULL.
        
    *   `IgnoreNull` — overrides class parameter %JSONIGNORENULL.
        
    *   `Reference` — overrides class parameter %JSONREFERENCE.
        

## Formatting JSON

%JSON.Formatter is a class with a very simple interface that allows you to format your dynamic objects and arrays and JSON strings into a more human-readable representation. All methods are instance methods, so you always start by retrieving an instance:

```
  set formatter = ##class(%JSON.Formatter).%New()
```

The reason behind this choice is that you can configure your formatter to use certain characters for line terminators and indentation once (for example, whitespaces vs. tabs; see the property list at the end of this section), and then use it wherever you need it.

The `Format()` method takes either a dynamic entity or a JSON string. Here is a simple example using a dynamic object:

```
  dynObj = {"type":"string"}
  do formatter.Format(dynObj)
```

The resulting formatted string is displayed on the current device:

```
  {
    "type":"string"
  }
```

Format methods can direct the output to the current device, a string, or a stream:

*   Format() formats a JSON document using the specified indentation and writes it to the current device.
    
*   FormatToStream() formats a JSON document using the specified indentation and writes it to a stream.
    
*   FormatToString() formats a JSON document using the specified indentation and writes it to a string, or serializes a JSON enabled class as a JSON document and returns it as a string.
    

In addition, the following properties can be used to control indentation and line breaks:

*   Indent specifies whether the JSON output should be indented
    
*   IndentChars specifies the sequence of characters to be used for each indent level (defaults to one space per level).
    
*   LineTerminator specifies the character sequence to terminate each line when indenting.
    

## %JSON Quick Reference

This section provides a quick reference for the %JSON methods, properties, and parameters discussed in this chapter. For the most complete and up to date information, see %JSON in the class reference.

### %JSON.Adaptor Methods

These methods provide the ability to serialize from and to JSON. See “Exporting and Importing” for more information and examples.

#### %JSONExport()

`%JSON.Adaptor.%JSONExport()` serializes a JSON enabled class as a JSON document and writes it to the current device.

```
   method %JSONExport(%mappingName As %String = "") as %Status
```

parameters:

*   `%mappingName` (optional) — the name of the mapping to use for the export. The base mapping is represented by "" and is the default.
    

#### %JSONExportToStream()

`%JSON.Adaptor.%JSONExportToStream()` serializes a JSON enabled class as a JSON document and writes it to a stream.

```
   method %JSONExportToStream(ByRef export As %Stream.Object,
      %mappingName As %String = "") as %Status
```

parameters:

*   `export` — stream containing the serialized JSON document.
    
*   `%mappingName` (optional) — the name of the mapping to use for the export. The base mapping is represented by "" and is the default.
    

#### %JSONExportToString()

`%JSON.Adaptor.%JSONExportToString()` serializes a JSON enabled class as a JSON document and returns it as a string.

```
   method %JSONExportToString(ByRef %export As %String,
      %mappingName As %String = "") as %Status
```

parameters:

*   `export` — string containing the serialized JSON document.
    
*   `%mappingName` (optional) — the name of the mapping to use for the export. The base mapping is represented by "" and is the default.
    

#### %JSONImport()

`%JSON.Adaptor.%JSONImport()` imports JSON or dynamic entity input into this object.

```
   method %JSONImport(input, %mappingName As %String = "") as %Status
```

parameters:

*   `input` — either JSON as a string or stream, or a subclass of %DynamicAbstractObject.
    
*   `%mappingName` (optional) — the name of the mapping to use for the import. The base mapping is represented by "" and is the default.
    

#### %JSONNew()

`%JSON.Adaptor.%JSONNew()` gets an instance of an JSON enabled class. You may override this method to do custom processing (such as initializing the object instance) before returning an instance of this class. However, this method should not be called directly from user code.

```
   classmethod %JSONNew(dynamicObject As %DynamicObject,
      containerOref As %RegisteredObject = "") as %RegisteredObject
```

parameters:

*   `dynamicObject` — the dynamic entity with the values to be assigned to the new object.
    
*   `containerOref` (optional) — the containing object instance when called from `%JSONImport()`.
    

### %JSON.Adaptor Class and Property Parameters

Unless noted otherwise, a parameter can be specified either for a class or for an individual property. As a class parameter, it specifies the default value of the corresponding property parameter. As a property parameter, it specifies a value that overrides the default. See “Mapping with Parameters” for more information and examples.

#### %JSONENABLED

Enables generation of property conversion methods.

```
  parameter %JSONENABLED = 1;
```

Valid values are:

*   `1` — (the default) JSON enabling methods will be generated.
    
*   `0` — method generators will not produce a runnable method.
    

#### %JSONFIELDNAME (properties only)

Sets the string to be used as the field name in JSON content.

```
  parameter %JSONFIELDNAME
```

By default, the property name is used.

#### %JSONIGNOREINVALIDFIELD

Controls handling of unexpected fields in the JSON input.

```
  parameter %JSONIGNOREINVALIDFIELD = 0;
```

Valid values are:

*   `0` — (the default) treat an unexpected field as an error.
    
*   `1` — unexpected fields will be ignored.
    

#### %JSONIGNORENULL

Specifies how to store empty strings for string properties. This parameter applies to only true strings (determined by `XSDTYPE = "string"` and `JSONTYPE="string"`).

```
  parameter %JSONIGNORENULL = 0;
```

Valid values are:

*   `0` — (the default) empty strings in the JSON input are stored as `""` and `$char(0)` is written to JSON as the string `""`. A missing field in the JSON input is always stored as `""` and `""` is always output to JSON according to the %JSONNULL parameter.
    
*   `1` — both empty strings and missing JSON fields are input as `""`, and both `""` and `$char(0)` are output as field value `""`.
    

JSON import will always store both empty value "" and a missing value as string "", no matter how this parameter is defined (0 or 1).

#### %JSONINCLUDE (properties only)

Specifies whether this property will be included in JSON output or input.

```
  parameter %JSONINCLUDE = "inout"
```

Valid values are:

*   `"inout"` (the default) — include in both input and output.
    
*   `"outputonly"` — ignore the property as input.
    
*   `"inputOnly"` — ignore the property as output.
    
*   `"none"` — never include the property.
    

#### %JSONNULL

Controls handling of unspecified properties.

```
  parameter %JSONNULL = 0;
```

Valid values are:

*   `0` — (the default) the field corresponding to an unspecified property is skipped during export.
    
*   `1` — unspecified properties are exported as the null value.
    

#### %JSONREFERENCE

Specifies how to project object references to JSON fields.

```
  parameter %JSONREFERENCE = "OBJECT";
```

Valid values are:

*   `"OBJECT"` — (the default) the properties of the referenced class are used to represent the referenced object.
    
*   `"ID`" — the id of a persistent or serial class is used to represent the reference.
    
*   `"OID`"— the oid of a persistent or serial class is used to represent the reference. The oid is projected to JSON in the form `classname,id`.
    
*   `"GUID"` — the GUID of a persistent class is used to represent the reference.
    

### %JSON.Formatter Methods and Properties

The %JSON.Formatter class can be used to format JSON strings, streams, or objects that subclass %DynamicAbstractObject. See the section on “Formatting JSON” for more information and examples.

#### Format()

`%JSON.Formatter.Format()` formats a JSON document using the specified indentation and writes it to the current device.

```
method Format(input) as %Status
```

parameters:

*   `input` — either JSON as a string or stream, or a subclass of %DynamicAbstractObject.
    

#### FormatToStream()

`%JSON.Formatter.FormatToStream()` formats a JSON document using the specified indentation and writes it to a stream.

```
method FormatToStream(input, ByRef export As %Stream.Object) as %Status
```

parameters:

*   `input` — either JSON as a string or stream, or a subclass of %DynamicAbstractObject.
    
*   `export` — the formatted JSON stream.
    

#### FormatToString()

`%JSON.Formatter.FormatToString()` formats a JSON document using the specified indentation and writes it to a string, or serializes a JSON enabled class as a JSON document and returns it as a string.

```
method FormatToString(input, ByRef export As %String = "") as %Status
```

parameters:

*   `input` — either JSON as a string or stream, or a subclass of %DynamicAbstractObject.
    
*   `export` (optional) — the formatted JSON stream.
    

#### Indent

The `%JSON.Formatter.Indent` property specifies whether the JSON output should be indented. Defaults to true.

```
property Indent as %Boolean [ InitialExpression = 1 ];
```

#### IndentChars

The `%JSON.Formatter.IndentChars` property specifies the character sequence to be used for each indent level if indenting is on. Defaults to one space.

```
property IndentChars as %String [ InitialExpression = " " ];
```

#### LineTerminator

The `%JSON.Formatter.LineTerminator` property specifies the character sequence to terminate each line when indenting. Defaults to `$char(13,10)`.

```
property LineTerminator as %String [ InitialExpression = $char(13,10) ];
```
