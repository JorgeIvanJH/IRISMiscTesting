# DTL <code>

Executes one or more lines of custom code, within a DTL transformation.

## Syntax

```
<code>
   <![CDATA[ target.Name = source.FirstName & " " & source.LastName]]>
</code>
```

## Elements

<table><tr><th>Element</th><th>Purpose</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_annotation">&lt;annotation&gt;</a></td><td>Optional. A text string that describes the &lt;code&gt; element.</td></tr></table>

## Description

The DTL <code> element executes one or more lines of user-written code within a DTL data transformation. You can use the <code> element to perform special tasks that are difficult to express using the DTL elements. Any properties referenced by the <code> element must be properties within the source or target object for the data transformation.

The scripting language for a DTL <code> element is specified by the `language` attribute of the containing <transform> element. The value should be `objectscript`. Any expressions found in the data transformation, as well as lines of code within <code> elements, must use the specified language.

For further information, see the following items:

*   Using ObjectScript
    
*   ObjectScript Reference
    

Typically a developer wraps the contents of a <code> element within a `CDATA` block to avoid having to worry about escaping special XML characters such as the apostrophe (') or the ampersand (&) . For example:

```xml
<code>
  <![CDATA[ target.Name = source.FirstName & " " & source.LastName]]>
</code>
```

In order to ensure that execution of a data transformation can be suspended and restored, you should follow these guidelines when using the <code> element:

*   The execution time should be short; custom code should not tie up the general execution of the data transformation.
    
*   Do not allocate any system resources (such as taking out locks or opening devices) without releasing them within the same <code> element.
    
*   If a <code> element starts a transaction, make sure that the same <code> element ends the transactions in all possible scenarios; otherwise, the transaction can be left open indefinitely. This could prevent other processing or can cause significant downtime.
    

## Available Variables

The variables that are available in a DTL <code> element are dependent upon the method used to call the element. Refer to the following table to see the available variables and their properties:

<table><tr><th>Variable Name</th><th>Purpose</th><th>Available when DTL is called through:</th></tr><tr><td><code>source</code></td><td>Contains properties of the source message.</td><td>All methods</td></tr><tr><td><code>target</code></td><td>Contains properties of the target message.</td><td>All methods</td></tr><tr><td><code>process</code></td><td>The <code>process</code> object represents the current instance of the BPL business process object (an instance of the BPL class). This object has one property for each property defined in that class. You can invoke methods of the <code>process</code> object; for example: <code>process.SendRequestSync()</code></td><td>BPL business processes</td></tr><tr><td><code>context</code></td><td>The <code>context</code> object is a general-purpose data container for the business process. <code>context</code> has no automatic definition. To define properties of this object, use the <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_context">&lt;context&gt;</a> element. That done, you may refer to these properties anywhere inside the <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_process">&lt;process&gt;</a> element using dot syntax, as in: <code>context.Balance</code></td><td>BPL business processes</td></tr><tr><td><code>aux</code></td><td>Contains information from the business rule that called the DTL.</td><td>Business rules</td></tr></table>
