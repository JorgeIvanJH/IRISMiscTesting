# Introduction to ObjectScript Operators

ObjectScript supports many different operators, which perform various actions, including mathematical actions, logical comparisons, and so on. Operators act on expressions, which are variables or other entities that are ultimately evaluated to a value. This topic describes expressions and the operators.

## Introduction

Operators are symbolic characters that specify the action to be performed on their associated operands. Each operand consists of one or more expressions or expression atoms. When used together, an operator and its associated operands have the following form:

[`operand`] operator `operand`

Some operators take only one operand and are known as unary operators; others take two operands and are known as binary operators.

An operator and any of its operands taken together constitute an expression.

### Assignment

Within ObjectScript the SET command is used along with the assignment operator ( = ) to assign a value to a variable. The right-hand side of an assignment command is an expression:

```objectscript
 SET value = 0
 SET value = a + b
```

Within ObjectScript it is also possible to use certain functions on the left-hand side of an assignment command:

```objectscript
 SET pies = "apple,banana,cherry"
 WRITE "Before: ",pies,!

 // set the 3rd comma-delimited piece of pies to coconut
 SET $Piece(pies,",",3) = "coconut"
 WRITE "After: ",pies
```

## Operator Precedence

Operator precedence in ObjectScript is strictly left-to-right; within an expression operations are performed in the order in which they appear. This is different from other languages in which certain operators have higher precedence than others. You can use explicit parentheses within an expression to force certain operations to be carried ahead of others. For example:

```objectscript
USER>WRITE "1 + 2 * 3 = ", 1 + 2 * 3
1 + 2 * 3 = 9
USER>WRITE 1 + 2 * 3
9
USER>WRITE 2 * 3 + 1
7
USER>WRITE 1 + (2 * 3)
7
USER>WRITE 2 * (3 + 1)
8
```

Note that in InterSystems SQL, operator precedence is configurable, and may (or may not) match the operator precedence in ObjectScript.

### Unary Negative Operators

ObjectScript gives the unary negative operator precedence over the binary arithmetic operators. ObjectScript first scans a numeric expression and performs any unary negative operations. Then, ObjectScript evaluates the expression and produces a result. For example:

```objectscript
USER>WRITE -123 - 3
-126
USER>WRITE -123 + - 3
-126
USER>WRITE -(123 - 3)
-120
```

### Parentheses and Precedence

You can change the order of evaluation by nesting expressions within each other with matching parentheses. The parentheses group the enclosed expressions (both arithmetic and relational) and control the order of operations. For example:

```objectscript
USER>SET TorF = ((4 + 7) > (6 + 6))

USER>WRITE TorF
0
```

Here, because of the parentheses, four and seven are added, as are six and six; this results in the logical expression `11 > 12`, which is false. Compare this to:

```objectscript
USER>SET Value = (4 + 7 > 6 + 6)

USER>WRITE Value
7
```

In this case, precedence proceeds from left to right, so four and seven are added. Their sum, eleven, is compared to six; since eleven is greater than six, the result of this logical operation is one (TRUE). One is then added to six, and the result is seven.

Note that the precedence even determines the result type, since the first expression’s final operation results in a boolean and the second expression’s final operation results in a numeric.

The following example shows multiple levels of nesting:

```objectscript
USER>WRITE 1+2*3-4*5
25
USER>WRITE 1+(2*3)-4*5
15
USER>WRITE 1+(2*(3-4))*5
-5
USER>WRITE 1+(((2*3)-4)*5)
11
```

Precedence from the innermost nested expression and proceeds out level by level, evaluating left to right at each level.

> **Tip:**
> 
> For all but the simplest ObjectScript expressions, it is good practice to fully parenthesize expressions. This is to eliminate any ambiguity about the order of evaluation and to also eliminate any future questions about the original intention of the code.

For example, because the `&&` operator, like all operators, is subject to left-to-right precedence, the final statement in the following code fragment evaluates to 0:

```objectscript
USER>SET x = 3

USER>SET y = 2

USER>WRITE x && y = 2
0
```

This is because, within the last step, the evaluation occurs as follows:

1.  The first action is to check if `x` is defined and has a non-zero value. Since `x` equals 3, evaluation continues.
    
2.  Next, there is a check if `y` is defined and has a non-zero value. Since `y` equals 2, evaluation continues.
    
3.  Next, the value of `3 && 2` is evaluated. Since neither 3 nor 2 equal 0, this expression is true and evaluates to 1.
    
4.  The next action is to compare the returned value to 2. Since 1 does not equal 2, this evaluation returns 0.
    

For those accustomed to many programming languages, this is an unexpected result. If the intent is to return True if `x` is defined with a non-zero value and if `y` equals 2, then parentheses are required:

```objectscript
USER>SET x = 3

USER>SET y = 2

USER>WRITE x && (y = 2)
1
```

### Functions and Precedence

Some types of expressions, such as functions, can have side effects. Suppose you have the following logical expression:

```objectscript
 IF var1 = ($$ONE + (var2 * 5)) {
    DO ^Test
 }
```

ObjectScript first evaluates `var1`, then the function `$$ONE`, then `var2`. It then multiplies `var2` by 5. Finally, ObjectScript tests to see if the result of the addition is equal to the value in `var1`. If it is, it executes the `DO` command to call the `Test` routine.

As another example, consider the following example:

```objectscript
USER>SET var8=25,var7=23

USER>WRITE var8 = 25 * (var7 < 24)
1
```

ObjectScript evaluates expressions strictly left-to-right. The programmer must use parentheses to establish any precedence. In this case, ObjectScript first evaluates the logical expression `var8 = 25`, resulting in 1. It then multiplies this result with the results of `(var7 < 24)`. The expression `(var7 < 24)` evaluates to 1. Therefore, ObjectScript multiplies 1 by 1, resulting in 1.

## Numeric Operators

You can use the Equals operator (`=`) to test for numeric equality if both operands have a numeric value. Other ObjectScript operators interpret their operands as numeric values and can be used only when the operands can be interpreted as numbers. These operators are as follows:

*   `+`
    
*   `-`
    
*   `*`
    
*   `/`
    
*   `\`
    
*   `#`
    
*   `**`
    
*   `<`
    
*   `>`
    
*   `<=`
    
*   `>=`
    

See Numeric Values in ObjectScript.

## String Operators

With the Equals operator (`=`), if the operands cannot be interpreted as numbers, the operator tests for string equality.

Other ObjectScript operators always interpret their operands as strings. These operators are as follows:

*   `_` (the concatenate operator)
    
*   `[` (the contains operator)
    
*   `]` (the follows operator)
    
*   `]]` (the sorts after operator)
    
*   ? (the pattern match operator)
    

See Strings in ObjectScript.

## Boolean Operators

ObjectScript provides operators that always interpret their operands as logical values. These are as follows:

*   `'` (logical NOT)
    
*   `&` and `&&` (logical AND)
    
*   `!` and `||` (logical OR)
    

Unlike some other languages, ObjectScript does not provide specialized representations of Boolean literal values. Instead, any expression that be interpreted as a nonzero numeric value is considered true; any other expression is false. See String-to-Number Conversions.

See Boolean Values in ObjectScript.

## Indirection Operator (@)

Indirection is a technique that provides dynamic runtime substitution of part or all of a command line, a command, or a command argument by the contents of a data field.

Indirection is specified by the indirection operator (@) and, except for subscript indirection, takes the form:

`@variable`

where `variable` identifies the variable from which the substitution value is to be taken. All variables referenced in the substitution value are public variables, even when used in a procedure. The variable can be an array node.

The following routine illustrates that indirection looks at the entire variable value to its right.

```objectscript
IndirectionExample
 SET x = "ProcA"
 SET x(3) = "ProcB"
 ; The next line will do ProcB, NOT ProcA(3)
 DO @x(3)
 QUIT
ProcA(var)
 WRITE !,"At ProcA"
 QUIT
ProcB(var)
 WRITE !,"At ProcB"
 QUIT
```

For details, see the Indirection (@) reference page.

> **Note:**
> 
> Although indirection can promote more economical and more generalized coding than would be otherwise available, it is never essential. You can always duplicate the effect of indirection by other means, such as by using the XECUTE command.

## See Also

*   Numeric Values in ObjectScript, which includes String-to-Number Conversions
    
*   Strings in ObjectScript
    
*   Boolean Values in ObjectScript
    
*   ObjectScript Operator Reference
