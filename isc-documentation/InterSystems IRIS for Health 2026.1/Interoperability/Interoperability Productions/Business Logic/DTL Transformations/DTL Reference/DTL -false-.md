# DTL <false>

Performs a set of activities when the condition for an <if> element is false, within a DTL transformation.

## Syntax

```
<if condition="0">
   <true>
     ...
   </true>
   <false>
     ...
   </false>
</if>
```

## Attributes

None.

## Elements

<table><tr><th>Element</th><th>Purpose</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_annotation">&lt;annotation&gt;</a></td><td>Optional. A text string that describes the &lt;false&gt; element.</td></tr><tr><td>Most activities</td><td>Optional. &lt;false&gt; may contain zero or more of the following elements in any combination: &lt;assign&gt;, &lt;code&gt;, &lt;foreach&gt;, &lt;if&gt;, &lt;sql&gt;, &lt;subtransform&gt;, or &lt;trace&gt;.</td></tr></table>

## Description

A <false> element is used within an <if> to contain elements that need to be executed if the condition is false.
