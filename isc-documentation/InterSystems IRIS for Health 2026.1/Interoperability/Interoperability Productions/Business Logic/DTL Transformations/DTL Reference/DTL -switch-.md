# DTL <switch>

Evaluates <case> elements and executes the contents of the first one that evaluates to true, within a DTL transformation.

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

<table><tr><th>Element</th><th>Purpose</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_annotation">&lt;annotation&gt;</a></td><td>Optional. A text string that describes the &lt;switch&gt; element.</td></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_case">&lt;case&gt;</a></td><td>The first &lt;case&gt; element that evaluates to true is executed.</td></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_default">&lt;default&gt;</a></td><td>Optional. If none of the &lt;case&gt; elements evaluate to true, the contents of the &lt;default&gt; element are executed.</td></tr></table>

## Description

The <switch> element contains one or more <case> elements along with an optional <default> element. The contents of a <case> element are executed if the condition evaluates to true. Once a <case> element evaluates to true, none of the other <case> elements nor the <default> element are evaluated. The contents of the <default> element are executed if none of the <case> elements evaluate to true.
