# DTL <trace>

Writes a message to the foreground ObjectScript shell, within a DTL transformation.

## Syntax

```
<trace value='"The time is: "_$ZDATETIME($H,3)' />
```

## Attributes

<table><tr><th>Attribute</th><th>Description</th><th>Value</th></tr><tr><td><code>value</code></td><td>Required. This is the text for the trace message. It can be a literal text string or an ObjectScript expression to be evaluated.</td><td>A string of one or more characters. May be a literal string or an expression.</td></tr></table>

## Elements

<table><tr><th>Element</th><th>Purpose</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_annotation">&lt;annotation&gt;</a></td><td>Optional. A text string that describes the &lt;trace&gt; element.</td></tr></table>

## Description

The <trace> element writes a message to the ObjectScript shell. <trace> messages appear only if the business host that invokes the DTL data transformation has been configured to `Run in Foreground` mode.

Trace messages may be written to the Event Log as well as to the console. A system administrator controls this behavior from the Management Portal Configuration page. If the business host that invokes the DTL data transformation has the `Log Trace Events` option checked, it writes trace messages to the Event Log as well as displaying them at the console. If a trace message is logged, its Event Log entry type is Trace.

The DTL <trace> element generates trace message with User priority; the result is the same as calling the `$$$TRACE` utility from ObjectScript.

> **Note:**
> 
> For details, see Adding Trace Elements.
