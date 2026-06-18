# Strings in ObjectScript

This page provides an overview of strings in ObjectScript and ways of working with them.

> **Note:**
> 
> In InterSystems SQL, string literals are delimited with single quotation marks, for example, `'sample literal string'` instead of double quotation marks as used in ObjectScript. This is important to remember when you write a mix of ObjectScript and SQL code.

## String Literals

In ObjectScript, a string literal is a set of zero or more characters delimited by double quotation marks, for example:

```
"sample literal string"
```

The value can contain any characters, including whitespace characters, control characters, and Unicode characters that cannot be typed.

To include a double quotation mark within a string, use two double quotation marks with no space between them:

```
"sample literal string with ""quoted"" text"
```

There is a maximum permitted length (see String Length Limit).

The following example shows a string of 8-bit characters, a string of 16-bit Unicode characters (Greek letters), and a combined string:

```objectscript
  DO AsciiLetters
  DO GreekUnicodeLetters
  DO CombinedAsciiUnicode
  RETURN
AsciiLetters()
  SET a="abc"
  WRITE a
  WRITE !,"the length of string a is ",$LENGTH(a)
  ZZDUMP a
  QUIT
GreekUnicodeLetters()
  SET b=$CHAR(945)_$CHAR(946)_$CHAR(947)
  WRITE !!,b
  WRITE !,"the length of string b is ",$LENGTH(b)
  ZZDUMP b
  QUIT
CombinedAsciiUnicode()
  SET c=a_b
  WRITE !!,c
  WRITE !,"the length of string c is ",$LENGTH(c)
  ZZDUMP c
  QUIT
```

## Non-Printing Characters and Unicode Characters

When you create a string, sometimes you need to include characters that cannot be typed. For these, you use the `$CHAR` function. Given an integer, `$CHAR` returns the corresponding ASCII or Unicode character. Common uses:

*   `$CHAR(9)` is a tab.
    
*   `$CHAR(10)` is a line feed.
    
*   `$CHAR(13)` is a carriage return.
    
*   `$CHAR(13,10)` is a carriage return and line feed pair.
    

The function `$ASCII` returns the ASCII value of the given character.

Similarly, you can use the `$CHAR` function to specify Unicode characters that cannot be typed (depending on your keyboard), as shown in the following example:

```objectscript
  SET greekstr=$CHAR(952,945,955,945,963,963,945)
  WRITE greekstr
```

> **Note:**
> 
> How non-printing characters display is determined by the display device. For example, the Terminal differs from browser display of the linefeed character, and other positioning characters. In addition, different browsers display the positioning characters $CHAR(11) and $CHAR(12) differently.

## Null Strings and the Null Character

An empty string, represented by two quotation mark characters (`""`), is known as a null string. A null string is considered to be a defined value; that is, if a variable is set equal to the empty string, the variable is considered defined. An empty string has a length of 0.

The null string is not the same as a string consisting of the ASCII null character ($CHAR(0)), as shown in the following example:

```objectscript
  SET x=""
  WRITE "string=",x," length=",$LENGTH(x)," defined=",$DATA(x)
  ZZDUMP x
  SET y=$CHAR(0)
  WRITE !!,"string=",y," length=",$LENGTH(y)," defined=",$DATA(y)
  ZZDUMP y
```

## String Concatenation

You can concatenate two strings into a single string using the concatenate operator:

```objectscript
 SET a = "Inter"
 SET b = "Systems"
 SET string = a_b
 WRITE string
```

For InterSystems IRIS encoded strings — bit strings, list structure strings, and JSON strings— there are limitations on the concatenate operator. For further details, see Concatenate Encoded Strings.

Some additional considerations apply when concatenating numbers; see Concatenating Numbers.

## String Equality

You can use the equals (=) and does not equal ('=) operators to compare two strings. String equality comparisons are case-sensitive. Exercise caution when using these operators to compare a string to a number, because this comparison is a string comparison, not a numeric comparison. Therefore only a string containing a number in canonical form is equal to its corresponding number. ("-0" is not a canonical number.) This is shown in the following example:

```objectscript
  WRITE "Fred" = "Fred",!  // TRUE
  WRITE "Fred" = "FRED",!  // FALSE
  WRITE "-7" = -007.0,!    // TRUE
  WRITE "-007.0" = -7,!    // FALSE
  WRITE "0" = -0,!         // TRUE
  WRITE "-0" = 0,!         // FALSE
  WRITE "-0" = -0,!        // FALSE
```

Because string equality comparisons are case-sensitive, depending on the use case, it may be appropriate to first use the `$ZCONVERT` function to convert the strings to all uppercase letters or all lowercase letters. This functionj does not affect non-letter characters. A few letters only have a lowercase letter form. For example, the German eszett ($CHAR(223)) is only defined as a lowercase letter. Converting it to an uppercase letter results in the same lowercase letter. For this reason, when converting alphanumeric strings to a single letter case it is always preferable to convert to lowercase.

The <, >, <=, or >= operators cannot be used to perform a string comparison. These operators treat strings as numbers and always perform a numeric comparison.

## Other String Relational Operators

In addition to the equals and does not equal operators, ObjectScript provides additional operators that interpret their operands as strings. You can precede any of them with the NOT logical operator (') to obtain the negation of the logical result. ObjectScript provides the following string relational operators:

### Contains ([)

Tests whether the sequence of characters in the right operand is a substring of the left operand. If the left operand contains the character string represented by the right operand, the result is TRUE (1). If the left operand does not contain the character string represented by the right operand, the result is FALSE (0). If the right operand is the null string, the result is always TRUE.

For example:

```objectscript
USER>SET L="Steam Locomotive"

USER>SET S="Steam"

USER>WRITE LS
1
```

See the [Contains ([) and Does Not Contain ('[) reference pages.

### [Follows (])](https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GCOS_strings#GCOS_C61492)

Tests whether the characters in the left operand come after the characters in the right operand in ASCII collating sequence. Follows tests both strings starting with the left most character in each.

For example:

```objectscript
USER>WRITE "LAMPOON"]"LAMP"
1
```

See the [Follows (])](https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RCOS_op_strrel_binfol) and [Not Follows ('])](https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RCOS_op_strrel_binnotfol) reference pages.

### [Sorts After (]])](https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GCOS_strings#GCOS_C61498)

Tests whether the left operand sorts after the right operand in numeric subscript collation sequence. In numeric collation sequence, the null string collates first, followed by canonical numbers in numeric order with negative numbers first, zero next, and positive numbers, followed lastly by nonnumeric values.

For example:

```objectscript
USER>WRITE 122]]2
1
```

See the [Sorts After (]])](https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RCOS_op_strrel_binaft) and [Not Sorts After (']])](https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RCOS_op_strrel_binnotaft) reference pages.

## Pattern Match Operator (?)

The ObjectScript pattern match operator tests whether the characters in its left operand are correctly specified by the pattern in its right operand.

For example, the following tests a couple of strings to see if they are valid U.S. Social Security Numbers:

```objectscript
USER>SET test1="123-45-6789"

USER>SET test2="123-XX-6789"

USER>WRITE test1 ? 3N1"-"2N1"-"4N
1
USER>WRITE test2 ? 3N1"-"2N1"-"4N
0
```

See the Pattern Match (?) reference page.

> **Note:**
> 
> ObjectScript also supports regular expressions, a pattern match syntax supported (with variants) by many software vendors. Regular expressions can be used with the `$LOCATE` and `$MATCH` functions, and with methods of the %Regex.Matcher class. For details, see the Regular Expressions reference page.
> 
> These pattern match systems are wholly separate and use different syntaxes with different patterns and flags.

## Commonly Used String Functions

The most commonly used ObjectScript functions for operating on strings include:

*   The `$LENGTH` function returns the number of characters in a string: For example, the code:
    
    ```objectscript
     WRITE $LENGTH("How long is this?")
    ```
    
    returns 17, the length of a string.
    
*   `$JUSTIFY` returns a right-justified string, padded on the left with spaces (and can also perform operations on numeric values). For example, the code:
    
    ```objectscript
     WRITE "one",!,$JUSTIFY("two",8),!,"three"
    ```
    
    justifies string `two` within eight characters and returns:
    
    ```
    one
         two
    three
    ```
    
*   `$ZCONVERT` converts a string from one form to another. It supports both case translations (to uppercase, to lowercase, or to title case) and encoding translation (between various character encoding styles). For example, the code:
    
    ```objectscript
     WRITE $ZCONVERT("cRAZy cAPs","t")
    ```
    
    returns:
    
    ```
    CRAZY CAPS
    ```
    
*   The `$FIND` function searches for a substring of a string, and returns the position of the character following the substring. For example, the code:
    
    ```objectscript
     WRITE $FIND("Once upon a time...", "upon")
    ```
    
    returns 10 character position immediately following “upon.”
    
*   The `$TRANSLATE` function performs a character-by-character replacement within a string. For example, the code:
    
    ```objectscript
     SET text = "11/04/2008"
     WRITE $TRANSLATE(text,"/","-")
    ```
    
    replaces the date’s slashes with hyphens.
    
*   The `$REPLACE` function performs string-by-string replacement within a string; the function does not change the value of the string on which it operates. For example, the following code performs two distinct operations:
    
    ```objectscript
     SET text = "green leaves, brown leaves"
     WRITE text,!
     WRITE $REPLACE(text,"leaves","eyes"),!
     WRITE $REPLACE(text,"leaves","hair",15),!
     WRITE text,!
    ```
    
    In the first call, `$REPLACE` replaces the string `leaves` with the string `eyes`. In the second call, `$REPLACE` discards all the characters prior to the fifteenth character (specified by the fourth argument) and replaces the string `leaves` with the string `hair`. The value of the `text` string is not changed by either `$REPLACE` call.
    
*   The `$EXTRACT` function, which returns a substring from a specified position in a string. For example, the code:
    
    ```objectscript
     WRITE $EXTRACT("Nevermore"),$EXTRACT("prediction",5),$EXTRACT("xon/xoff",1,3)
    ```
    
    returns three strings. The one-argument form returns the first character of the string; the two-argument form returns the specified character from the string; and the three-argument form returns the substring beginning and ending with specified characters, inclusive. In the example above, there are no line breaks, so the return value is:
    
    ```
    Nixon
    ```
    

## See Also

*   ObjectScript Operators
    
*   ObjectScript Functions
