# DTL <default>

Executes contents if none of the <case> elements in a <switch> element evaluate to true, within a DTL transformation.

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

None.

## Elements

<table><tr><th>Element</th><th>Purpose</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_annotation">&lt;annotation&gt;</a></td><td>Optional. A text string that describes the &lt;default&gt; element.</td></tr></table>

## Description

The <default> element appears at the end of the <switch> element, and is executed if none of the <case> elements evaluate to true.
