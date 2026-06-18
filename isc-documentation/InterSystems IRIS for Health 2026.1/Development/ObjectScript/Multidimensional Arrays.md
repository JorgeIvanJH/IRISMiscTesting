# Multidimensional Arrays

ObjectScript includes support for multidimensional arrays, which you can use to contain and manipulate values that are related in some manner. Multidimensional arrays are supported extensively in ObjectScript and in InterSystems IRIS data platform.

There are class-based alternatives as well.

## Introduction and Terminology

A multidimensional array is a structure consisting of one or more nodes, and each node is identified by a unique subscript or set of subscripts. For example, the `MyVar` array could consist of the following nodes:

*   `MyVar`
    
*   `MyVar(22)`
    
*   `MyVar(-3)`
    
*   `MyVar("MyString")`
    
*   `MyVar(-123409, "MyString")`
    
*   `MyVar("MyString", 2398)`
    
*   `MyVar(1.2, 3, 4, "Five", "Six", 7)`
    

Each node of an array is an ObjectScript variable and holds a single value of any type; you can work with any node in exactly the same way that you work with a variable that does not have a subscript. ObjectScript provides specialized functions that work with the array itself, enabling you to traverse it, selectively remove parts of it, and perform other actions applicable to the structure as a whole.

### Multidimensional Tree Structures

The entire structure of a multidimensional array is called a tree; it begins at the top and grows downwards. The root, `MyVar` above, is at the top. The root, and any other subscripted form of it, are called nodes. Nodes that have no nodes beneath them are called leaves. Nodes that have nodes beneath them are called parents or ancestors. Nodes that have parents are called children or descendants. Children with the same parents are called siblings. All siblings are automatically sorted numerically or alphabetically as they are added to the tree.

### Sparse Multidimensional Storage

Multidimensional arrays are sparse. This means that the example above uses only seven reserved memory locations, one for each defined node. There is no declaration for arrays or their dimensions; all the space that they use is dynamically allocated. As an example, consider an array used to keep track of players’ pieces for a game of checkers; a checkerboard is 8 by 8. In a language that required an 8–by-8 checkerboard-sized array would use 64 memory locations, even though no more than 24 positions are ever occupied by checkers; in ObjectScript, the array would require 24 positions only at the beginning, and would need fewer and fewer during the course of the game.

## Where Multidimensional Arrays Are Supported

Local variables, process-private variables, and global variables can all be multidimensional arrays. Lock names can also be multidimensional arrays. It is not necessary to do any kind of declaration of these items as multidimensional arrays.

Also, a property in a class can be a multidimensional array if it has the `MultiDimensional` keyword in its definition, for example:

```
Property MyProp as %String [ MultiDimensional ];
```

The purpose of this declaration (the `MultiDimensional` keyword) is to affect the code generated for the class. This kind of property cannot be saved to the database.

The phrase “to support an item as a multidimensional array” means that it is syntactically valid to set or refer to a subscript of the item. An alternate phrasing of the idea is “to allow an item to have subscripts.”

For example, `MyVar` is a local variable. Because local variables are supported as multidimensional arrays, it is syntactically valid to use commands like these:

```
 Set MyVar("test subscript")=45
 Write MyVar("test subscript")
```

As described in Subscript Rules, you can use multiple subscripts, not just the single one shown here.

## Subscript Rules

The following list describes the rules for subscripts of multidimensional arrays:

*   A subscript can be a numeric or a string. It can include any characters, including Unicode characters. Valid numeric subscripts include positive and negative numbers, zero, and fractional numbers.
    
*   The empty string (`""`) is not a valid subscript.
    
*   Subscript values are case-sensitive.
    
*   Any numeric subscript is converted to canonical form. Thus, for example, the global nodes `^a(7)`, `^a(007)`, `^a(7.000)`, and `^a(7.)` are all the same because the subscript is actually the same in all cases.
    
*   A string subscript is not converted to canonical form. Thus, for example, `^a("7")`, `^a("007")`, `^a("7.000")`, and `^a("7.")` are all different global nodes because these subscripts are all different. Also, `^a("7")` and `^a(7)` both refer to the same global node, because these subscripts are the same.
    
*   An array node can have multiple subscripts, and the subscripts are not required to have the same data type or to follow any specific system.
    
*   There are limits on the length of a subscript and on the number of subscript levels. See Subscript Limits.
    

Also see General System Limits.

## Manipulating Multidimensional Arrays

InterSystems IRIS provides a comprehensive set of commands and functions for working with multidimensional arrays:

*   Set places values in an array.
    
*   Kill removes all or part of an array structure.
    
*   Merge copies all or part of an array structure to a second array structure.
    
*   $Order and $Query allows you to iterate over the contents of an array.
    
*   $Data allows you to test for the existence of nodes in an array.
    

For details on these commands, see Working with Globals, which applies to globals and all other kinds of multidimensional arrays.

Also, you can use the $QSUBSCRIPT function to return the components (name and subscripts) of a specified variable, or the $QLENGTH function to return the number of subscript levels.

## Class-Based Arrays

Rather than multidimensional arrays, you can use array classes that use a different structure and that provide an object-based API. InterSystems IRIS provides a set of classes you can use as array-form class properties, and another set of classes you can use for standalone arrays.

## See Also

*   General System Limits
    
*   Working with Globals
    
*   Working with Collection Classes
