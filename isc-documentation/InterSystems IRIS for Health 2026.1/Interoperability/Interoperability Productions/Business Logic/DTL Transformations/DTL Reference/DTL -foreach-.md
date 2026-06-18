# DTL <foreach>

Defines a sequence of activities to be executed iteratively, within a DTL transformation.

## Syntax

```
<foreach property="P1" key="K1">
   ...
</foreach>
```

## Attributes

<table><tr><th>Attribute</th><th>Description</th><th>Value</th></tr><tr><td><code>property</code></td><td>Required. The collection property (list or array) to iterate over. It must be the name of a valid object and property in the execution context.</td><td>A string of one or more characters.</td></tr><tr><td><code>key</code></td><td>Required. The index used to iterate through the collection. It must be a name of a valid object and property in the execution context. It is assigned a value for each element in the collection.</td><td>A string of one or more characters.</td></tr></table>

## Elements

<table><tr><th>Element</th><th>Purpose</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_annotation">&lt;annotation&gt;</a></td><td>Optional. A text string that describes the &lt;foreach&gt; element.</td></tr><tr><td>Most activities</td><td>Optional. &lt;foreach&gt; may contain zero or more of the following elements in any combination: &lt;assign&gt;, &lt;code&gt;, &lt;foreach&gt;, &lt;if&gt;, &lt;sql&gt;, &lt;subtransform&gt;, or &lt;trace&gt;.</td></tr></table>

## Description

The <foreach> element defines a sequence of activities that are executed iteratively, once for every element that exists within a specified collection property. If the element is null, the sequence is not executed. The sequence is executed if the element has an empty value, that is, the separators are there but there is no value between them, but is not executed for a null value, that is, the message is terminated before the field is specified.

For example:

```xml
<foreach key='i' property='target.{PID:3()}'>
   <assign property='target.{PID:3(i).4}' value='"001"' action='set'/>
 </foreach>
```

Or:

```xml
<foreach key='key' property='source.{PID:PatientIDInternalID()}'>
 <if condition='source.{PID:PatientIDInternalID(key).identifiertypecode}="PAS"'>
  <true>
   <assign property='target.{PID:PatientIdentifierList(key).identifiertypecode}'
           value='"MR"'
           action='set'/>
  </true>
 </if>
 <if condition='source.{PID:PatientIDInternalID(key).identifiertypecode}="GMS"'>
  <true>
   <assign property='target.{PID:PatientIdentifierList(key).identifiertypecode}'
           value='"MC"'
           action='set'/>
   <assign property='target.{PID:PatientIdentifierList(key).assigningfacility}'
           value='"AUSHIC"'
           action='set'/>
  </true>
 </if>
</foreach>
```

The properties referenced by the <foreach> element must be properties in the source or target object for the data transformation.

### Nested <foreach>

Nesting of <foreach> elements is allowed, but see the next subsection for an alternative.

### Shortcuts for <foreach>

When you are working with a document-based message or “virtual document” type, the <assign> statement offers a shortcut notation that iterates through every instance of a repeating field within a document structure. This means you do not actually need to set up <foreach> loops with 'i' 'j' and 'k' just for the purpose of handling repeating fields. Instead, you can use a much simpler notation with empty parentheses. See Iterating Through Repeating Fields.

### Avoiding <STORE> Errors with Large Messages

As you loop over segments in a message or object collections, they are brought into memory. If these objects consume all the memory assigned to the current process, you may get unexpected errors.

To avoid this, remove the objects from memory after you no longer need them. For example, if you are processing many segments in a <foreach> loop, you can call the `commitSegmentByPath` method on both the source and target as the last step in the loop. Similarly, for object collections, use the `%UnSwizzleAt` method.

If you cannot make code changes, a temporary workaround is to increase the amount of memory allocated for each process. You can change this by setting the `bbsiz` parameter on the `Advanced Memory Settings` page in the Management Portal. Note that this requires a system restart and should only occur after consulting with your system administrator.
