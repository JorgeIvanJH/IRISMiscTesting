# Types of Data in ObjectScript

This page discusses types of data supported in ObjectScript.

> **Note:**
> 
> Although ObjectScript is typeless, InterSystems IRIS data platform does support and enforce types for class properties and table fields. There is an extensive set of data type classes, and InterSystems SQL supports standard SQL data types.

## Introduction

Formally, ObjectScript is a typeless language — you do not have to declare the types of variables. Any variable can contain any kind of value, and usage determines how the value is evaluated. For example, `5` can be treated as a number, a string, or a boolean value. Phrased differently, variables in ObjectScript are weakly, dynamically typed. They are dynamically typed because you do not have to declare the type for a variable, and variables can take any legal value. They are weakly typed because usage determines how they are evaluated.

## Common Types

Although ObjectScript variables do not have types, it is possible to categorize the types of values they can contain, in a generic sense. The most commonly used types of values are as follows:

### numbers

A number is a set of digits, including a leading plus or minus sign, a decimal sign, and an exponentiation sign, if needed.

ObjectScript supports two internal representations of fractional numbers: standard InterSystems IRIS floating point numbers ($DECIMAL numbers) and IEEE double-precision floating-point numbers ($DOUBLE numbers).

See Numeric Values in ObjectScript.

### strings

A string is a set of characters: letters, digits, punctuation, and so on delimited by a matched set of quotation marks ("):

```objectscript
 SET string = "This is a string"
 WRITE string
```

You can include a " (double quote) character as a literal within a string by preceding it with another double quote character:

```objectscript
 SET string = "This string has ""quotes"" in it."
 WRITE string
```

See Strings in ObjectScript. Also see String Length Limit.

### lists

ObjectScript provides a native list format. See Lists in ObjectScript, which also discusses alternatives.

### date and date/time values

ObjectScript has no built-in date type; instead, it includes a number of functions for operating on and formatting date values represented as strings. See Date and Time Values in ObjectScript.

### boolean values

Specific ObjectScript operators, functions, and commands can treat any value as a boolean value (true or false).

Unlike some other languages, ObjectScript does not provide specialized representations of boolean literal values. For simplicity, use 1 for true, and 0 for false.

See Boolean Values in ObjectScript.

### OREFs

A variable can contain an OREF, which is a handle to an in-memory object. An OREF is also called an object value. You can assign an OREF to any local variable:

```objectscript
  SET myperson = ##class(Sample.Person).%New()
  WRITE myperson
```

A global variable cannot equal an OREF. A runtime error occurs if you try to make such an assignment.

See Working with Registered Objects and Working with Persistent Objects.

## Type Conversion Summary

Depending on the context, a string can be treated as a number and vice versa. Similarly, in some contexts, a value may be interpreted as a boolean (true or false) value; anything that evaluates to zero is treated as false; anything else is treated as true. This means that you can assign a string value to a variable and, later on, assign a numeric value to the same variable. As an optimization, InterSystems IRIS may use different internal representations for strings, integers, numbers, and objects, but this is not visible to the application programmer. InterSystems IRIS automatically converts (or interprets) the value of a variable based on the context in which it is used.

The following table summarizes how InterSystems IRIS converts values:

### ObjectScript Type Conversion Rules

<table><tr><th>From</th><th>To</th><th>Rules</th></tr><tr><td>Number</td><td>String</td><td>A string of characters that represents the numeric value is used, such as <code>2.2</code> for the variable <code>num</code> in the previous example.</td></tr><tr><td>String</td><td>Number</td><td>Leading characters of the string are interpreted as a numeric literal, as described in <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GCOS_numbers#GCOS_numbers_from_strings">String-to-Number Conversion</a>. For example, “–1.20abc” is interpreted as <code>-1.2</code> and “abc123” is interpreted as <code>0</code>.</td></tr><tr><td>Object</td><td>Number</td><td>The internal object instance number of the given object reference is used. The value is an integer.</td></tr><tr><td>Object</td><td>String</td><td>A string of the form <code>n@cls</code> is used, where <code>n</code> is the internal object instance number and <code>cls</code> is the class name of the given object.</td></tr><tr><td>Number</td><td>Object</td><td>Not allowed.</td></tr><tr><td>String</td><td>Object</td><td>Not allowed.</td></tr></table>
