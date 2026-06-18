# DTL <transform>

Defines a DTL transformation.

## Syntax

```
<transform sourceClass="MyApp.SAPtoJDE"
           targetClass="AlsoMine.JDE"  />
```

## Attributes

<table><tr><th>Attribute</th><th>Description</th><th>Value</th></tr><tr><td><code>sourceClass</code></td><td>Required. The class name of the input object for the data transformation.</td><td>The name of a valid object and property.</td></tr><tr><td><code>targetClass</code></td><td>Required. The class name of the output object for the data transformation.</td><td>The name of a valid object and property.</td></tr><tr><td><code>sourceDocType</code></td><td>Optional. When the input object is a virtual document, this string identifies its DocType.</td><td>A string.</td></tr><tr><td><code>targetDocType</code></td><td>Optional. When the output object is a virtual document, this string identifies its DocType.</td><td>A string.</td></tr><tr><td><code>language</code></td><td>Optional. Should be <code>objectscript</code></td><td><code>objectscript</code></td></tr><tr><td><code>create</code></td><td>Optional. The create option desired for the target object. If not specified, the default is <code>new</code>.</td><td>This can take one of the following values: <code>new</code>, <code>copy</code>, or <code>existing</code> as detailed in the following description.</td></tr></table>

## Elements

<table><tr><th>Element</th><th>Purpose</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_annotation">&lt;annotation&gt;</a></td><td>Optional. A text string that describes the &lt;transform&gt; element.</td></tr><tr><td>Most activities</td><td>Optional. &lt;transform&gt; may contain zero or more of the following elements in any combination: &lt;assign&gt;, &lt;code&gt;, &lt;foreach&gt;, &lt;if&gt;, &lt;sql&gt;, &lt;subtransform&gt;, or &lt;trace&gt;.</td></tr></table>

## Description

The <transform> element is the outermost element for a DTL document. All the other DTL elements are contained within a <transform> element. Within the <transform>, the two objects have the names `source` and `target`, respectively. For example:

```xml
<transform targetClass='Demo.DTL.ExampleTarget'
           sourceClass='Demo.DTL.ExampleSource'
           create='new'
           language='objectscript'>

       <trace value='"Convert from lowercase to uppercase"'/>
       <assign property='target.UpperCase'
          value='$ZCONVERT(source.LowerCase,"U")'
          action='set'/>

</transform>
```

### Source and Target Objects

The `sourceClass` and `targetClass` may identify standard production message classes, each of which contains a set of properties. If so, the `sourceDocType` and `targetDocType` attributes are not needed.

Alternatively, the `sourceClass` and `targetClass` may identify virtual documents. In this case the `sourceDocType` and `targetDocType` attributes are needed to tell InterSystems IRIS which message structure to expect in the virtual document.

### Values for the create Option

The `create` option for the target object may have one of the following values:

*   `new`—Create a new object of the target type, before executing the elements within the data transformation. This is the default.
    
*   `copy`—Create a copy of the source object to use as the target object, before executing the elements within the transform.
    
*   `existing`—Use an existing object, provided by the caller of the data transformation, as the target object.
