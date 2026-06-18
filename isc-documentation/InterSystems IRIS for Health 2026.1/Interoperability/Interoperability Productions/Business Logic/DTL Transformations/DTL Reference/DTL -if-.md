# DTL <if>

Evaluates a condition and performs one action if true, another if false, within a DTL transformation.

## Syntax

```
<if condition="1">
   <true>
     ...
   </true>
   <false>
     ...
   </false>
</if>
```

## Attributes

<table><tr><th>Attribute</th><th>Description</th><th>Value</th></tr><tr><td><code>condition</code></td><td>Required. An ObjectScript expression that, if true, causes the contents of the &lt;true&gt; element to execute. If false, the contents of the &lt;false&gt; element are executed.</td><td>An expression that evaluates to the integer value 1 (if true) or 0 (if false).</td></tr></table>

## Elements

<table><tr><th>Element</th><th>Purpose</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_annotation">&lt;annotation&gt;</a></td><td>Optional. A text string that describes the &lt;if&gt; element.</td></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_true">&lt;true&gt;</a></td><td>Optional. If the condition is true, activities inside the &lt;true&gt; element are executed.</td></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_false">&lt;false&gt;</a></td><td>Optional. If the condition is false, activities inside the &lt;false&gt; element are executed.</td></tr></table>

## Description

The <if> element evaluates an expression and, depending on its value, executes one of two sets of activities (one if the expression evaluates to a true value, the other if it evaluates to a false value).

The <if> element may contain a <true> element and a <false> element which define the actions to execute if the expression evaluates to true or false, respectively.

If both <true> and <false> elements are provided, they may appear within the <if> element in any order.

If the condition is true and there is no <true> element, or if the condition is false and there is no <false> element, no activity results from the <if> element.
