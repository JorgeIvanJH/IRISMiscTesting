# Numeric Values in ObjectScript

This page describes numeric values in ObjectScript, as well as operators for working with them.

## Numeric Literals

Numeric literals do not require any enclosing punctuation. You can specify a number using any valid numeric characters. InterSystems IRIS evaluates a number as syntactically valid, then converts it to canonical form.

The syntactic requirements for a numeric literal are as follows:

*   It can contain the decimal numbers 0 through 9, and must contain at least one of these number characters. It can contain leading or trailing zeros. However, when InterSystems IRIS converts a number to canonical form it automatically removes leading integer zeros. Therefore, numbers for which leading integer zeros are significant must be input as strings. For example, United State postal Zip Codes can have a leading integer zero, such as 02142, and therefore must be handled as strings, not numbers.
    
*   It can contain any number of leading plus and minus signs in any sequence. However, a plus sign or minus sign cannot appear after any other character, except the “E” scientific notation character. In a numeric expression a sign after a non-sign character is evaluated as an addition or subtraction operation. In a numeric string a sign after a non-sign character is evaluated as a non-numeric character, terminating the number portion of the string.
    
    InterSystems IRIS uses the PlusSign and MinusSign property values for the current locale to determine these sign characters (“+” and “-” by default); these sign characters are locale-dependent. To determine the PlusSign and MinusSign characters for your locale, invoke the GetFormatItem() method:
    
    ```objectscript
      WRITE ##class(%SYS.NLS.Format).GetFormatItem("PlusSign"),!
      WRITE ##class(%SYS.NLS.Format).GetFormatItem("MinusSign")
    ```
    
*   It can contain at most one decimal separator character. In a numeric expression a second decimal separator results in a <SYNTAX> error. In a numeric string a second decimal separator is evaluated as the first non-numeric character, terminating the number portion of the string. The decimal separator character may be the first character or the last character of the numeric expression. The choice of decimal separator character is locale-dependent: American format uses a period (.) as the decimal separator, which is the default. European format uses a comma (,) as the decimal separator. To determine the DecimalSeparator character for your locale, invoke the GetFormatItem() method:
    
    ```objectscript
      WRITE ##class(%SYS.NLS.Format).GetFormatItem("DecimalSeparator")
    ```
    
*   It can contain at most one letter “E” (or “e”) to specify a base-10 exponent for scientific notation. This scientific notation character (“E” or “e”) must be preceded by a integer or fractional number, and followed by an integer.
    

Numeric literal values do not support the following:

*   They cannot contain numeric group separators. These are locale-dependent: American format uses commas, European format uses periods. You can use the `$INUMBER` function to remove numeric group separators, and the `$FNUMBER` function to add numeric group separators.
    
*   They cannot contain currency symbols, hexadecimal letters, or other nonnumeric characters. They cannot contain blank spaces, except before or after arithmetic operators.
    
*   They cannot contain trailing plus or minus signs. However, the `$FNUMBER` function can display a number as a string with a trailing sign, and the `$NUMBER` function can take a string in this format and convert it to a number with a leading sign.
    
*   They cannot specify enclosing parentheses to represent a number as a negative number (a debit). However, the `$FNUMBER` function can display a negative number as a string with a enclosing parentheses, and the `$NUMBER` function can take a string in this format and convert it to a number with a leading negative sign.
    

A number or numeric expression can containing pairs of enclosing parentheses. These parentheses are not part of the number, but govern the precedence of operations. By default, InterSystems IRIS performs all operations in strict left-to-right order.

### Scientific Notation

To specify scientific (exponential) notation in ObjectScript, use the following format:

```
[-]mantissaE[-]exponent
```

where

<table><tr><th>Element</th><th>Description</th></tr><tr><td>-</td><td>Optional — One or more Unary Minus or Unary Plus operators. These PlusSign and MinusSign characters are configurable. Conversion to canonical form resolves these operators after resolving the scientific notation.</td></tr><tr><td><code>mantissa</code></td><td>An integer or fractional number. May contain leading and trailing zeros and a trailing decimal separator character.</td></tr><tr><td><code>E</code></td><td>An operator delimiting the exponent. The uppercase “E” is the standard exponent operator; the lowercase “e” is a configurable exponent operator, using the <code>ScientificNotation()</code> method of the <a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25SYSTEM.Process">%SYSTEM.Process</a> class.</td></tr><tr><td>-</td><td>Optional — A single Unary Minus or Unary Plus operator. Can be used to specify a negative exponent. These PlusSign and MinusSign characters are configurable.</td></tr><tr><td><code>exponent</code></td><td>An integer specifying the exponent (the power of 10). Can contain leading zeros. Cannot contain a decimal separator character.</td></tr></table>

For example, to represent 10, use `1E1`. To represent 2800, use `2.8E3`. To represent .05, use `5E-2`.

No spaces are permitted between the `mantissa`, the `E`, and the `exponent`. Parentheses, concatenation, and other operators are not permitted within this syntax.

Because resolving scientific notation is the first step in converting a number to canonical form, some conversion operations are not available. The `mantissa` and `exponent` must be numeric literals, they cannot be variables or arithmetic expressions. The `exponent` must be an integer with (at most) one plus or minus sign.

See the ScientificNotation() method of the %SYSTEM.Process class.

## Arithmetic

The arithmetic operators interpret their operands as numeric values and produce numeric results. When operating on a string, an arithmetic operator treats the string as its numeric value, according to the rules in String-to-Number Conversion. The arithmetic operators are as follows:

### Unary Positive (+)

The unary positive operator gives its single operand a numeric interpretation. It does this by sequentially parsing the characters of the string as a number, until it encounters a character that cannot be interpreted as a number. It then returns whatever leading portion of the string was a well-formed numeric (or it returns 0 if no such interpretation was possible). For example:

```objectscript
USER>WRITE + "32 dollars and 64 cents"
32
```

### Unary Negative (-)

The unary negative operator reverses the sign of a numerically interpreted operand. For example:

```objectscript
USER>SET x = -60

USER>WRITE x
-60
USER>WRITE -x
60
```

ObjectScript gives the unary negative operator precedence over the binary (two-operand) arithmetic operators.

To return the absolute value of a numeric expression, use the `$ZABS` function.

### Addition (+)

The addition operator adds two numeric values. For example:

```objectscript
USER>WRITE 2936.22 + 301.45
3237.67
```

### Subtraction (-)

The subtraction operator subtracts one numeric value from another. For example:

```objectscript
USER>WRITE 2936.22 - 301.45
2634.77
```

### Multiplication (*)

The multiplication operator multiplies two numeric values. For example:

```objectscript
USER>WRITE 9 * 5.5
49.5
```

### Division (/)

The division operator divides one numeric value with another. For example:

```objectscript
USER>WRITE 355 / 113
3.141592920353982301
```

### Integer Division ( \ )

The integer division operator divides one numeric value with another and discards any fractional value. For example:

```objectscript
USER>WRITE 355 \ 113
3
```

### Modulo (#)

When the two operands are positive, then the modulo operator returns the remainder of the left operand integer divided by the right operand. For example:

```objectscript
USER>WRITE 37 # 10
7
USER>WRITE 12.5 # 3.2
2.9
```

### Exponentiation (**)

The exponentiation operator raises one numeric value to the power of the other numeric value. For example:

```objectscript
USER>WRITE 9 ** 2
81
```

Exponentiation can also be performed using the `$ZPOWER` function.

## Numeric Equality

You can use the equals (=) and does not equal ('=) operators to compare two numbers.

The equals operator tests whether the left operand equals the right operand. For example:

```objectscript
USER>WRITE 9 = 6
0
```

You can also use the does not equal ('=) operator.

## Other Numeric Comparisons

The equals (=) and does not equal ('=) operators, discussed previously, can be used with strings. In contrast, the operators discussed here are meant for use only with numeric values. The operators here always interpret their operands as numeric values (see String-to-Number Conversion) and then produce a Boolean result.

### Less Than Operator (<)

The less than operator tests whether the left operand is less than the right operand. For example:

```objectscript
USER>WRITE 9 < 6
0
```

### Greater Than Operator (>)

The greater than operator tests whether the left operand is greater than the right operand. For example:

```objectscript
USER>WRITE 15 > 15
0
```

### Less Than or Equal To Operator (<= or '>)

The less than or equal to operator tests whether the left operand is less or equal to than the right operand. For example:

```objectscript
USER>9 <= 6
0
```

### Greater Than or Equal To Operator (>= or '<)

The greater than or equal to operator tests whether the left operand is greater than or equal to the right operand. For example:

```objectscript
USER>WRITE 15 >= 15
1
```

## Canonical Numbers

ObjectScript performs all numeric operations on numbers in their canonical form. For example, the length of the number `+007.00` is 1; the length of the string `"+007.00"` is 7.

When InterSystems IRIS converts a number to canonical form, it performs the following steps:

1.  Scientific notation exponents are resolved. For example 3E4 converts to 30000 and 3E-4 converts to .0003.
    
2.  Leading signs are resolved. First, multiple signs are resolved to a single sign (for example, two minus signs resolve to a plus sign). Then, if the leading sign is a plus sign, it is removed. You can use the `$FNUMBER` function to explicitly specify (prepend) a plus sign to a positive InterSystems IRIS canonical number.
    
    > **Note:**
    > 
    > ObjectScript resolves any combination of leading plus and minus signs. In SQL, two consecutive minus signs are parsed as a single-line comment indicator. Therefore, specifying a number in SQL with two consecutive leading minus signs results in an SQLCODE -12 error.
    
3.  All leading and trailing zeros are removed. This includes removing leading integer zeroes, including the leading integer zero from fractions smaller than 1. For example `0.66` becomes `.66`.
    
    *   To append an integer zero to a canonical fraction use the `$FNUMBER` or `$JUSTIFY` function. `.66` becomes `0.66`.
        
    *   To remove integer zeroes from a non-canonical fraction use the Unary Plus operator to force conversion of a number string to a canonical number. In the following example, the fractional seconds portion of a timestamp, `+$PIECE("65798,00000.66",",",2)`. `00000.66` becomes `.66`.
        
    
    As part of this conversion, zero fractions are simplified to 0. Regardless of how expressed (`0.0`, `.0`, `.000`) all zero values are converted to `0`.
    
4.  A trailing decimal separator is removed.
    
5.  -0 is converted to 0.
    
6.  Arithmetic operations and numeric concatenation are performed. InterSystems IRIS performs these operations in strict left-to-right order. Numbers are in their canonical form when these operations are performed. For further details, see Concatenating Numbers below.
    

InterSystems IRIS canonical form numbers differ from other canonical number formats used in InterSystems software:

*   ODBC: Integer zero fractions converted to ODBC have a zero integer. Therefore, `.66` and `000.66` both become `0.66`. You can use the $FNUMBER or $JUSTIFY function to prepend an integer zero to an InterSystems IRIS canonical fractional number.
    
*   JSON: Only a single leading minus sign is permitted; a leading plus sign or multiple signs are not permitted.
    
    Exponents are permitted but not resolved. 3E4 is returned as 3E4.
    
    Leading zeros are not permitted. Trailing zeros are not removed.
    
    Integer zero fractions must have a zero integer. Therefore, `.66` and `000.66` are not valid JSON numbers, but `0.66` and `0.660000` are valid JSON numbers.
    
    A trailing decimal separator is not permitted.
    
    Zero values are not converted: `0.0`, `-0`, and `-0.000` are returned unchanged as valid JSON numbers.
    

### Concatenating Numbers

A number can be concatenated to another number using the concatenate operator (_). InterSystems IRIS first converts each number to its canonical form, then performs a string concatenation on the results. Thus, the following all result in 1234: 12_34, 12_+34, 12_--34, 12.0_34, 12_0034.0, 12E0_34. The concatenation 12._34 results in 1234, but the concatenation 12_.34 results in 12.34. The concatenation 12_-34 results in the string “12-34”.

InterSystems IRIS performs numeric concatenation and arithmetic operations on numbers after converting those numbers to canonical form. It performs these operations in strict left-to-right order, unless you specify parentheses to prioritize an operation. The following example explains one consequence of this:

```objectscript
  WRITE 7_-6+5 // returns 12
```

In this example, the concatenation returns the string “7-6”. This, of course, is not a canonical number. InterSystems IRIS converts this string to a canonical number by truncating at the first non-numeric character (the embedded minus sign). It then performs the next operation using this canonical number 7 + 5 = 12.

## Floating-Point Numbers

InterSystems IRIS supports two different numeric types that can be used to represent floating-point numbers:

*   Decimal floating-point: By default, InterSystems IRIS represents fractional numbers using its own decimal floating-point standard ($DECIMAL numbers). This is the preferred format for most uses. It provides a higher level of precision than IEEE Binary floating-point. It is consistent across all system platforms that InterSystems IRIS supports. Decimal floating-point is preferred for data base values. In particular, a fractional number such as 0.1 can be exactly represented using decimal floating-point notation, while the fractional number 0.1 (as well as most decimal fractional numbers) can only be approximated by IEEE Binary floating-point.
    
    Internally, Decimal arithmetic is performed using numbers of the form M*(10**N), where M is the integer significand containing an integer value between -9223372036854775808 and 9223372036854775807 and N is the decimal exponent containing an integer value between -128 and 127. The significand is represented by a 64-bit signed integer and the exponent is represented by an 8-bit signed byte.
    
    The average precision of Decimal floating point is 18.96 decimal digits. Decimal numbers with a significand between 1000000000000000000 and 9223372036854775807 have exactly 19 digits of precision and a Decimal significant between 922337203685477581 and 999999999999999999 have exactly 18 digits of precision. Although IEEE Binary floating-point is less precise (with an accuracy of approximately 15.95 decimal digits), the exact, infinitely precise value of IEEE Binary representation as a decimal string can have over 1000 significant decimal digits.
    
    In the following example, `$DECIMAL` functions take a fractional number and an integer with 25 digits and return a Decimal number rounded to 19 digits of precision / 19 significant digits:
    
    ```objectscript
    USER>WRITE $DECIMAL(1234567890.123456781818181)
    1234567890.123456782
    USER>WRITE $DECIMAL(1234567890123456781818181)
    1234567890123456782000000
    ```
    
*   IEEE Binary floating-point: IEEE double-precision binary floating point is an industry-standard way of representing fractional numbers. IEEE floating point numbers are encoded using binary notation. Binary floating-point representation is usually preferred when doing high-speed calculations because most computers include high-speed hardware for binary floating-point arithmetic.
    
    Internally, IEEE Binary arithmetic is performed using numbers of the form S*M*(2**N), where S is the sign containing the value -1 or +1, M is the significand containing a 53-bit binary fractional value with the binary point between the first and second binary bit, and N is the binary exponent containing an integer value between -1022 and 1023. Therefore, the representation consists of 64 bits, where S is a single sign bit, the exponent N is stored in the next 11 bits (with two additional values reserved), and the significand M is >=1.0 and <2.0 containing the last 52 bits with a total of 53 binary bits of precision. (Note that the first bit of M is always a 1, so it does not need to appear in the 64-bit representation.)
    
    Double-precision binary floating point has a precision of 53 binary bits, which corresponds to approximately 15.95 decimal digits of precision. (The corresponding decimal precision varies between 15.35 and 16.55 digits.)
    
    Binary representation does not correspond exactly to a decimal fraction because a fraction such as 0.1 cannot be represented as a finite sequence of binary fractions. Because most decimal fractions cannot be exactly represented in this binary notation, an IEEE floating point number may differ slightly from the corresponding InterSystems Decimal floating point number. When an IEEE floating point number is displayed as a fractional number, the binary bits are often converted to a fractional number with far more than 18 decimal digits. This does not mean that IEEE floating point numbers are more precise than InterSystems Decimal floating point numbers. IEEE floating point numbers are able to represent larger and smaller numbers than InterSystems Decimal numbers.
    
    In the following example, the `$DOUBLE` function take a sequence of 17-digit integers and returns values with roughly 16 significant digits of decimal precision:
    
    ```objectscript
    USER>FOR i=12345678901234558:1:12345678901234569 {W $DOUBLE(i),!}
    12345678901234558
    12345678901234560
    12345678901234560
    12345678901234560
    12345678901234562
    12345678901234564
    12345678901234564
    12345678901234564
    12345678901234566
    12345678901234568
    12345678901234568
    12345678901234568
    ```
    
    IEEE Binary floating-point supports the special values INF (infinity) and NAN (not a number). For further details, see the $DOUBLE function.
    
    You can configure processing of IEEE floating point numbers using the `IEEEError` setting for handling of INF and NAN values, and the `ListFormat` setting for handling compression of IEEE floating point numbers in $LIST structured data. Both can be viewed and set for the current process using %SYSTEM.Process class methods ($SYSTEM.Process.IEEEError(). System-wide defaults can be set using the InterSystems IRIS Management Portal, as follows: from `System Administration`, select `Configuration`, `Additional Settings`, `Compatibility`.
    

You can use the $DOUBLE function to convert an InterSystems IRIS standard floating-point number to an IEEE floating point number. You can use the $DECIMAL function to convert an IEEE floating point number to an InterSystems IRIS standard floating-point number.

By default, InterSystems IRIS converts fractional numbers to canonical form, eliminating all leading zeros. Therefore, `0.66` becomes `.66`. $FNUMBER (most formats) and $JUSTIFY (3-parameter format) always return a fractional number with at least one integer digit; using either of these functions, `.66` becomes `0.66`.

$FNUMBER and $JUSTIFY can be used to round or pad a numeric to a specified number of fractional digits. InterSystems IRIS rounds up 5 or more, rounds down 4 or less. Padding adds zeroes as fractional digits as needed. The decimal separator character is removed when rounding a fractional number to an integer. The decimal separator character is added when zero-padding an integer to a fractional number.

## Extremely Large Numbers

The largest integers that can be represented exactly are the 19-digit integers -9223372036854775808 and 9223372036854775807. This is because these are the largest numbers that can be represented with 64 signed bits. Integers larger than this are automatically rounded to fit within this 64-bit limit. This is shown in the following example:

```objectscript
  SET x=9223372036854775807
  WRITE x,!
  SET y=x+1
  WRITE y
```

Similarly, exponents larger that 128 may also result in rounding to permit representation within 64 signed bits. This is shown in the following example:

```objectscript
  WRITE 9223372036854775807e-128,!
  WRITE 9223372036854775807e-129
```

Because of this rounding, arithmetic operations that result in numbers larger than these 19-digit integers have their low-order digits replaced by zeros. This can result in situations such as the following:

```objectscript
  SET longnum=9223372036854775790
  WRITE longnum,!
  SET add17=longnum+17
  SET add21=longnum+21
  SET add24=longnum+24
  WRITE add17,!,add24,!,add21,!
  IF add24=add21 {WRITE "adding 21 same as adding 24"}
```

The largest InterSystems IRIS decimal floating point number supported is 9.223372036854775807E145. The largest supported $DOUBLE value (assuming IEEE overflow to INFINITY is disabled) is 1.7976931348623157081E308. The $DOUBLE type supports a larger range of values than the InterSystems IRIS decimal type, while the InterSystems IRIS decimal type supports more precision. The InterSystems IRIS decimal type has a precision of approximately 18.96 decimal digits (usually 19 digits but sometimes only 18 decimal digits of precision) while the $DOUBLE type usually has a precision around 15.95 decimal digits (or 53 binary digits). By default, InterSystems IRIS represents a numeric literal as a decimal floating-point number. However, if the numeric literal is larger than what can be represented in InterSystems IRIS decimal (larger than 9.223372036854775807E145) InterSystems IRIS automatically converts that numeric value to $DOUBLE representation.

A numeric value larger than 1.7976931348623157081E308 (308 or 309 digits) results in a <MAXNUMBER> error.

Because of the automatic conversion from decimal floating-point to binary floating-point, rounding behavior changes at 9.223372036854775807E145 (146 or 147 digits, depending on the integer). This is shown in the following examples:

```objectscript
  TRY {
    SET a=1
    FOR i=1:1:310 {SET a=a_1 WRITE i+1," digits = ",+a,! }
  }
  CATCH exp { WRITE "In the CATCH block",!
              IF 1=exp.%IsA("%Exception.SystemException") {
                  WRITE "System exception",!
                  WRITE "Name: ",$ZCVT(exp.Name,"O","HTML"),!
                  WRITE "Location: ",exp.Location,!
                  WRITE "Code: "
                }
              ELSE { WRITE "Some other type of exception",! RETURN }
              WRITE exp.Code,!
              WRITE "Data: ",exp.Data,!
              RETURN
  }
```

```objectscript
  TRY {
    SET a=9
    FOR i=1:1:310 {SET a=a_9 WRITE i+1," digits = ",+a,! }
  }
  CATCH exp { WRITE "In the CATCH block",!
              IF 1=exp.%IsA("%Exception.SystemException") {
                  WRITE "System exception",!
                  WRITE "Name: ",$ZCVT(exp.Name,"O","HTML"),!
                  WRITE "Location: ",exp.Location,!
                  WRITE "Code: "
              }
              ELSE { WRITE "Some other type of exception",! RETURN }
              WRITE exp.Code,!
              WRITE "Data: ",exp.Data,!
              RETURN
  }
```

You can represent a number longer than 309 digits as a numeric string. Because this value is stored as a string rather than a number, neither rounding nor the <MAXNUMBER> error apply:

```objectscript
  SET a="1"
  FOR i=1:1:360 {SET a=a_"1" WRITE i+1," characters = ",a,! }
```

Exponents that would result in a number with more than the maximum permitted number of digits generate a <MAXNUMBER> error. The largest permitted exponent depends on the size of the number that is receiving the exponent. For a single-digit mantissa, the maximum exponent is 307 or 308.

For further details on large number considerations, see Numeric Computing in InterSystems Applications.

## String-to-Number Conversion

Most of the operators introduced on this page interpret their operands as numeric values. This section describes how that interpretation is performed. First, here is the basic terminology:

*   A numeric string is a string literal that consists entirely of numeric characters. For example, `"123"`, `"+123"`, `".123"`, `"++0007"`, `"-0"`.
    
*   A partially numeric string is a string literal that begins with numeric symbols, followed by non-numeric characters. For example, `"3 blind mice"`, `"-12 degrees"`.
    
*   A non-numeric string is a string literal that begins with a non-numeric character. For example, `" 123"`, `"the 3 blind mice"`, `"three blind mice"`.
    

### Numeric Strings

When a numeric string or partially numeric string is used in an arithmetic expression, it is interpreted as a number. This numeric value is obtained by scanning the string from left to right to find the longest sequence of leading characters that can be interpreted as a numeric literal. The following characters are permitted:

*   The digits 0 through 9.
    
*   The PlusSign and MinusSign property values. By default these are the `+` and `-` characters, but are locale-dependent. Use the %SYS.NLS.Format.GetFormatItem() method to return the current settings.
    
*   The DecimalSeparator property value. By default this is the `.` character, but is locale-dependent. Use the %SYS.NLS.Format.GetFormatItem() method to return the current setting.
    
*   The letters `e`, and `E` may be included as part of a numeric string when in a sequence representing scientific notation, such as 4E3.
    

Note that the NumericGroupSeparator property value (the `,` character, by default) is not considered a numeric character. Therefore, the string `"123,456"` is a partially numeric string that resolves to the number `"123"`.

Numeric strings and partial numeric strings are converted to canonical form prior to arithmetic operations (such as addition and subtraction) and greater than/less than comparison operations (<, >, <=, >=). Numeric strings are not converted to canonical form prior to equality comparisons (=, '=), because these operators are also used for string comparisons.

The following example shows arithmetic comparisons of numeric strings:

```objectscript
USER>WRITE "3" + 4
7
USER>WRITE "003.0" + 4
7
USER>WRITE "++--3" + 4
7
USER>WRITE "3 blind mice" + 4
7
```

The following example shows less than (<) comparisons of numeric strings:

```objectscript
USER>WRITE "3" < 4
1
USER>WRITE "003.0" < 4
1
USER>WRITE "++--3" < 4
1
USER>WRITE "3 blind mice" < 4
1
```

The following example shows <= comparisons of numeric strings:

```objectscript
USER>WRITE "4" <= 4
1
USER>WRITE "004.0" <= 4
1
USER>WRITE "++--4" <= 4
1
USER>WRITE "4 horsemen" <= 4
1
```

The following example shows equality comparisons of numeric strings. Non-canonical numeric strings are compared as character strings, not as numbers. Note that –0 is a non-canonical numeric string, and is therefore compared as a string, not a number:

```objectscript
USER>WRITE "4" = 4.00
1
USER>WRITE "004.0" = 4
0
USER>WRITE "++--4" = 4
0
USER>WRITE "4 horsemen" = 4
0
USER>WRITE "-4" = -4
1
USER>WRITE "0" = 0
1
USER>WRITE "-0" = 0
0
USER>WRITE "-0" = -0
0
```

### Non-Numeric Strings

If the leading characters of the string are not numeric characters, the string’s numeric value is 0 for all arithmetic operations. For <, >, '>, <=, '<, and >= comparisons a non-numeric string is also treated as the number 0. Because the equal sign is used for both the numeric equality operator and the string comparison operator, string comparison takes precedence for = and '= operations. You can prepend the PlusSign property value (+ by default) to force numeric evaluation of a string; for example, `"+123"`. This results in the following logical values, when `x` and `y` are different non-numeric strings (for example x=”Fred”, y=”Wilma”).

<table><tr><th>x, y</th><th>x, x</th><th>+x, y</th><th>+x, +y</th><th>+x, +x</th></tr><tr><td><code>x=y</code> is FALSE</td><td><code>x=x</code> is TRUE</td><td><code>+x=y</code> is FALSE</td><td><code>+x=+y</code> is TRUE</td><td><code>+x=+x</code> is TRUE</td></tr><tr><td><code>x'=y</code> is TRUE</td><td><code>x'=x</code> is FALSE</td><td><code>+x'=y</code> is TRUE</td><td><code>+x'=+y</code> is FALSE</td><td><code>+x'=+x</code> is FALSE</td></tr><tr><td><code>x&lt;y</code> is FALSE</td><td><code>x&lt;x</code> is FALSE</td><td><code>+x&lt;y</code> is FALSE</td><td><code>+x&lt;+y</code> is FALSE</td><td><code>+x&lt;+x</code> is FALSE</td></tr><tr><td><code>x&lt;=y</code> is TRUE</td><td><code>x&lt;=x</code> is TRUE</td><td><code>+x&lt;=y</code> is TRUE</td><td><code>+x&lt;=+y</code> is TRUE</td><td><code>+x&lt;=+x</code> is TRUE</td></tr></table>

### Extremely Large Numbers from Strings

Usually, a numeric string is converted to an ObjectScript Decimal value. However, with extremely large numbers (larger than 9223372036854775807E127) it is not always possible to convert a numeric string to a Decimal value. If converting a numeric string to its Decimal value would result in a <MAXNUMBER> error, InterSystems IRIS instead converts it to an IEEE Binary value. InterSystems IRIS performs the following operations in converting a numeric string to a number:

1.  Convert numeric string to Decimal floating point number. If this would result in <MAXNUMBER> go to Step 2. Otherwise, return Decimal value as a canonical number.
    
2.  Check the $SYSTEM.Process.TruncateOverflow() method boolean value. If 0 (the default) go to Step 3. Otherwise, return an overflow Decimal value (see method description).
    
3.  Convert numeric string to IEEE Binary floating point number. If this would result in <MAXNUMBER> go to Step 4. Otherwise, return IEEE Binary value as a canonical number.
    
4.  Check the $SYSTEM.Process.IEEEError() method boolean value. Depending on this value either return INF / -INF, or issue a <MAXNUMBER> error.
    

## See Also

*   ObjectScript Operators
    
*   ObjectScript Functions
    
*   Numeric Computing in InterSystems Applications
