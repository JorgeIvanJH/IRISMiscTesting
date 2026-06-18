# DTL <break>

Terminates a <foreach> loop or stop processing a DTL transformation.

## Syntax

```
<break/>
```

## Attributes

None.

## Elements

<table><tr><th>Element</th><th>Purpose</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_annotation">&lt;annotation&gt;</a></td><td>Optional. A text string that describes the &lt;break&gt; element.</td></tr></table>

## Description

When included in a <foreach> element, the <break> element terminates the For Each loop. If <break> is outside of a For Each loop, the entire data transformation terminates as soon as the break is executed.
