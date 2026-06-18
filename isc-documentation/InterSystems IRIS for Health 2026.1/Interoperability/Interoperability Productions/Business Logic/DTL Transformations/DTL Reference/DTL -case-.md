# DTL <case>

Executes a block of actions within a <switch> element when the specified condition is met, within a DTL transformation.

## Syntax

```
<switch>
   <case condition="1">
   ...
   </case>
   <default>
   ...
   </default>
</switch>
```

## Attributes

<table><tr><th>Attribute</th><th>Description</th><th>Value</th></tr><tr><td><code>condition</code></td><td>Required. An ObjectScript expression that, if true, causes the contents of the &lt;case&gt; element to be executed.</td><td>An expression that evaluates to the integer value 1 (if true) or 0 (if false).</td></tr></table>

## Elements

<table><tr><th>Element</th><th>Purpose</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_annotation">&lt;annotation&gt;</a></td><td>Optional. A text string that describes the &lt;case&gt; element.</td></tr></table>

## Description

The <switch> element contains one or more <case> elements. The elements within a <case> element are executed if the condition evaluates to true.
