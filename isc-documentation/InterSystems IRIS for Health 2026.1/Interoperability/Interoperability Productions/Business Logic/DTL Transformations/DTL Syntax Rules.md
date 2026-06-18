# DTL Syntax Rules

This topic describes the syntax rules applicable to various DTL actions within data transformations for interoperability productions.

## References to Message Properties

In most actions within a transformation, it is necessary to refer to properties of the source or target messages. The rules for referring to a property are different depending on the kind of messages you are working with.

*   For messages other than virtual documents, use syntax like the following:
    
    ```
    source.propertyname
    ```
    
    Or:
    
    ```
    source.propertyname.subpropertyname
    ```
    
    Where `propertyname` is a property in the source message, and `subpropertyname` is a property of that property.
    
    If the message includes a collection property, see Special Variations for Repeating Fields. Some of the information there applies to both virtual documents and standard messages.
    
*   For virtual documents other than XML virtual documents, use the syntax described in Syntax Guide for Virtual Property Paths. Also see the following subsection.
    
*   For XML virtual documents, see Routing XML Virtual Documents in Productions.
    

## Literal Values

When you assign a value to a target property, you often specify a literal value. Literal values are also sometimes suitable in other places, such as the value in a `TRACE` action.

A literal value is either of the following:

*   A numeric literal is just a number. For example: 42.3
    
*   A string literal is a set of characters enclosed by double quotes. For example: `"ABD"`
    
    > **Note:**
    > 
    > This string cannot include XML reserved characters. For details, see XML Reserved Characters.
    > 
    > For virtual documents, this string cannot include separator characters used by that virtual document format. See Separator Characters in Virtual Documents and When XML Reserved Characters Are Also Separators.
    

### XML Reserved Characters

Because DTL transformations are saved as XML documents, you must use XML entities in the place of XML reserved characters:

<table><tr><th>To include this character...</th><th>Use this XML entity...</th></tr><tr><td><code>&gt;</code></td><td><code>&amp;gt;</code></td></tr><tr><td><code>&lt;</code></td><td><code>&amp;lt;</code></td></tr><tr><td><code>&amp;</code></td><td><code>&amp;amp;</code></td></tr><tr><td><code>'</code></td><td><code>&amp;apos;</code></td></tr><tr><td><code>"</code></td><td><code>&amp;quot;</code></td></tr></table>

For example, to assign the value `Joe’s "Good Time" Bar & Grill` to a target property, set `Value` equal to the following:

```
"Joe&apos;s &quot;Good Time&quot; Bar &amp; Grill"
```

This restriction does not apply inside `CODE` and `SQL` actions, because InterSystems IRIS automatically wraps a CData block around the text that you enter into the editor. (In the XML standard, a CData block encloses text that should not be parsed as XML. Thus you can include reserved characters in that block.)

### Separator Characters in Virtual Documents

In most of the virtual document formats, specific characters are used as separators between segments, between fields, between subfields, and so on. These characters may vary from one clinical application to another. If you need to include any of these characters as literal text when you are setting a value in the message, you must instead use the applicable escape sequence, if any, for that document format.

Except for EDIFACT, the only supported way to modify the separators for a virtual document is to specify the `Separators` setting; that is, if you use DTL to modify the separator field, that has no effect.

See the following topics:

*   EDIFACT Separators
    
*   X12 Separators
    
*   HL7 Separators
    
*   ASTM Separators
    

> **Important:**
> 
> In a data transformation, the separator characters and escape sequences can be different for the source and target messages. InterSystems IRIS automatically adjusts values as needed, after performing the transformation. This means that you should consider only the separator characters and escape sequences that apply to the source message.

### When XML Reserved Characters Are Also Separators

*   If the character (for example, `&`) is a separator and you want to include it as a literal character, use the escape sequence that applies to the virtual document format.
    
*   In all other cases, use the XML entity as shown previously in XML Reserved Characters.
    

### Numeric Character Codes

You can include decimal or hexadecimal representations of characters within literal strings.

The string `&#n;` represents a Unicode character when `n` is a decimal Unicode character number. One example is `&#233;` for the Latin e character with acute accent mark (é).

Alternatively, the string `&#xh;` represents a Unicode character when `h` is a hexadecimal Unicode character number. One example is &#x00BF; for the inverted question mark (¿).

## Valid Expressions

When you assign a value to a target property, you can specify an expression, in the language that you selected for the data transformation. You also use expressions in other places, such as the condition for an `IF` action, the value in a `TRACE` action, statements in a `CODE` action, and so on.

The following are all valid expressions:

*   Literal values, as described in the previous section.
    
*   Function calls, as described in Utility Functions for Use in Productions. InterSystems IRIS provides a wizard for these.
    
*   References to properties, as described in References to Properties.
    
*   References to the `aux` variable passed by the rule. If the data transformation is called from a rule, it supplies the following information in the `aux` variable:
    
    *   aux.BusinessRuleName—Name of the rule.
        
    *   aux.RuleReason—Reason that the rule was fired. It is the same name as used in the logging. An example value is 'rule#1:when#1'. If the RuleReason is longer than 2000 characters, it is truncated to 2000 characters.
        
    *   aux.RuleUserData—Value that was assigned in the rule to the property 'RuleUserData'. The value of 'RuleUserData' is always the last value that it was set to.
        
    *   aux.RuleActionUserData—Value that was assigned in the rule when or otherwise clause to the property 'RuleActionUserData’.
        
    
    If the data transformation is called directly from code and not from a rule, the code can pass the auxiliary data in the third parameter. If your data transformation may be called from code that does not set the third parameter, your DTL code should check that the `aux` variable is an object in an `IF` action using the `$ISOBJECT` function.
    
*   Any expression that combines these, using the syntax of the scripting language you chose for data transformation. See Specifying Transformation Details. Note the following:
    
    *   In ObjectScript, the concatenation operator is the _ (underscore) character, as in:
        
        `value='"prefix"_source.{MSH:ReceivingApplication}_"suffix"'`
        
    *   To learn about useful ObjectScript string functions, such as $CHAR and $PIECE, see the ObjectScript Reference.
        
    *   For a general introduction, see Using ObjectScript.
        

## See Also

*   Introduction to the DTL Editor
    
*   Creating Data Transformations
    
*   Adding and Editing Actions
    
*   Testing Data Transformations
