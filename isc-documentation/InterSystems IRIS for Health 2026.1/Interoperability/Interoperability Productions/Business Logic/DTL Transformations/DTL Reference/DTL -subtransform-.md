# DTL <subtransform>

Invokes another data transformation, within a DTL transformation.

## Syntax

```
<subtransform class='class-name'
                     targetObj='target-value}'
                     sourceObj='source-value'/>
```

## Attributes

<table><tr><th>Attribute</th><th>Description</th><th>Value</th></tr><tr><td><code>class</code></td><td><p>Required. Name of the class that contains the data transformation to be invoked. This class must be in the same namespace as the class that invokes it.</p><p>Often, <code>class</code> is a DTL data transformation defined using a DTL &lt;transform&gt; element, as shown in the examples in this topic.</p><p>Alternatively, <code>class</code> can identify a custom subclass of <a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=Ens.DataTransform">Ens.DataTransform</a> that implements the <code>Transform</code> method and does not use DTL.</p></td><td>The full package and class name.</td></tr><tr><td><code>sourceObject</code></td><td><p>Required. Identifies the property being transformed. This may be an object property or a virtual document property. Generally it is a property of the source object identified by the containing &lt;transform&gt; element’s <code>sourceClass</code> and (for virtual documents) <code>sourceDocType</code>. In this case it is referenced using dot syntax as follows:</p><p><code>source.property</code> or <code>source.{propertyPath}</code></p></td><td>Property name. For virtual documents and their segments, use virtual property syntax.</td></tr><tr><td><code>targetObject</code></td><td><p>Required. Identifies the property into which the transformed value will be written. This may be an object property or a virtual document property. Generally it is a property of the target object identified by the containing &lt;transform&gt; element’s <code>targetClass</code> and (for virtual documents) <code>targetDocType</code>.In this case it is referenced using dot syntax as follows:</p><p><code>target.property</code> or <code>target.{propertyPath}</code></p><p>In the case of a subtransform with <code>Create</code> as <code>new</code> or <code>copy</code>, it is not necessary to have a pre-existing target object.</p></td><td>Property name. For virtual documents and their segments, use virtual property syntax.</td></tr></table>

## Elements

<table><tr><th>Element</th><th>Purpose</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_annotation">&lt;annotation&gt;</a></td><td>Optional. A text string that describes the &lt;subtransform&gt; element.</td></tr></table>

## Description

The <subtransform> element invokes another data transformation. Making a call to <subtransform> allows the containing <transform> element to invoke other data transformations to complete segments of its work. This allows developers greater flexibility in maintaining a suite of reusable DTL transformation code.

Before the <subtransform> element was available, every DTL <transform> stood alone. In order to write multiple DTL transformations that contained an identical sequence of actions, it was necessary to copy and paste the corresponding sections of code from one class into another. Now, each of these DTL classes can replace repeated lines with a <subtransform> element that invokes another class to performs the desired sequence.

The source or target objects for a <subtransform> may be ordinary InterSystems IRIS objects, virtual document message objects, or virtual document segment objects representing an individual segment within a virtual document message. The <subtransform> is especially important for interface developers working with Electronic Data Interchange (EDI) formats, where each message or document may contain many independent segments that need to be transformed. Having the <subtransform> available means you can create a reusable library of segment transformations that you can call as needed, without duplicating code in the calling transformation.

For virtual documents and their segments, you must use virtual property syntax, such as the {} curly bracket syntax in the following examples. The property path inside the brackets must refer to a particular segment, not to a field within a segment or to a group of segments. For background information, see Using Virtual Documents in Productions; details are available in Virtual Property Path.
