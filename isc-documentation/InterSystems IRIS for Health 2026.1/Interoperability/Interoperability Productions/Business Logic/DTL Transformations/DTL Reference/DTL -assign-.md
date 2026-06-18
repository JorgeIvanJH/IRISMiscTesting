# DTL <assign>

Assigns a value to a property of an object, within a DTL transformation.

## Syntax

```
<assign property="propertyname" value="expression" />
```

## Attributes

<table><tr><th>Attribute</th><th>Description</th><th>Value</th></tr><tr><td><code>property</code></td><td>Required. The property that is the target of this assignment.</td><td>A string.</td></tr><tr><td><code>value</code></td><td>Required. Provides a value for the property.</td><td>An ObjectScript expression that provides a valid value for the property.</td></tr><tr><td><code>action</code></td><td>Optional. If <code>value</code> is a collection property (list or array), then use <code>action</code> to specify the type of assignment to perform. The default is a set action.</td><td>One of the following values: <code>set</code>, <code>clear</code>, <code>remove</code>, <code>append</code>, <code>insert</code>. See the <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_assign#EDTL_assign_action">actions</a> section for details.</td></tr><tr><td><code>key</code></td><td>Optional, except in some cases when <code>value</code> is a collection property (list or array). If so, then use this key to specify the element upon which the assignment will be performed.</td><td>A string that is an expression that evaluates to a key.</td></tr></table>

## Elements

<table><tr><th>Element</th><th>Purpose</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_annotation">&lt;annotation&gt;</a></td><td>Optional. A text string that describes the &lt;assign&gt; element.</td></tr></table>

## Description

The DTL <assign> element is used from within a DTL <transform> element to specify a target property and an expression whose value will be assigned to it. Generally, this expression involves values from the source object for the data transformation, but they may also be literal values. All properties involved in a DTL <assign> activity must be properties within the source or target object for the data transformation.

The source and target objects are generally production message body objects, as described in Messages. These consist of a message header and a message body object.

Properties in the standard production message body can be data types, objects, or collections of either. Collection properties are declared with either `[ Collection = list ]` or `[ Collection = array ]` in the class definition. You can refer to the properties on the standard production message body using dot syntax as for any object property.

Properties in a virtual document require the unique syntax described in the following topics:

*   Virtual Property Paths
    
*   Syntax Guide for Virtual Property Paths
    

### Actions of the <assign> Element

There are several types of DTL <assign> operation, as specified by the optional `action` attribute. Aside from the default of set, these variations are intended to handle assignments involving collection properties within a standard production message body. The following table describes the actions of the <assign> element.

<table><tr><th>Assign action</th><th>Description</th><th>Example</th></tr><tr><td>set</td><td>Sets the value of the specified property to that of the <code>value</code> attribute. Note that the <code>value</code> attribute contains an expression and can itself refer to an object or property of an object.</td><td>The following statement sets the value of the target <code>BankName</code> property:&lt;assign property='target.BankName' value='process.BankName' action='set'/&gt;</td></tr><tr><td>append</td><td>Adds the target element to the end of a list property</td><td>&nbsp;</td></tr><tr><td>clear</td><td>Clears the contents of the specified collection property. The <code>value</code> and <code>key</code> attributes are ignored. (Applies to collection properties only.)</td><td>The following statement clears the contents of the collection property <code>List</code>:&lt;assign property='target.List' action='clear' /&gt;</td></tr><tr><td>insert</td><td>Inserts a value into the specified collection property. If the <code>key</code> attribute is present the new value is inserted after the position (an integer) specified by <code>key</code>; otherwise, the new item is inserted at the end. (Applies to list collection properties only.)</td><td>The following statement inserts a value into the array collection property <code>Array</code> using the key <code>primary</code>:&lt;assign property='target.Array' action='insert' key='primary' value='source.Primary' /&gt;</td></tr><tr><td>remove</td><td>Removes an item from the specified collection property. The <code>value</code> attribute is ignored. (Applies to collection properties only.)</td><td>&nbsp;</td></tr></table>

> **Note:**
> 
> Virtual documents do not use any `action` value other than set or remove.

The set action sets the value of the specified property to that of the `value` attribute. Note that the `value` attribute contains an expression and can itself refer to an object or property of an object:

```xml
<assign property='target.SSN' value='source.SSN' />
```

If the target property is an array collection, then the value of the `key` attribute specifies an item in the array, otherwise the `key` attribute is ignored.

If the target property is a collection and the `value` attribute specifies a collection of the same type, then the collection contents are copied into the target collection:

```xml
<assign property='target.List' value='source.List' />
```

The default action for the assign element is the set operation; if `action` is not specified, then the assign specifies a set operation.

### Objects and Object References

If you <assign> from the top-level source object or any object property of another object as your source, the target receives a cloned copy of the object rather than the object itself. This prevents inadvertent sharing of object references and saves the effort of generating cloned objects yourself. However, if you want to share object references between source and target you must <assign> from the source to an intermediate temporary variable, and then <assign> from that variable to the target.

### Wholesale Copy

To create a target object that is an exact copy of the source, do not use:

```
<assign property='target' value='source' />
```

Instead use the `create='copy'` attribute in the containing <transform> element.

The `create` option may have one of the following values:

*   `new`—Create a new object of the target type, before executing the elements within the data transformation. This is the default.
    
*   `copy`—Create a copy of the source object to use as the target object, before executing the elements within the transform.
    
*   `existing`—Use an existing object, provided by the caller of the data transformation, as the target object.
