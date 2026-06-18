# Actions That Set or Clear Values

This topic provides details on setting or clearing values within your DTL data transformations for interoperability productions.

For information on performing these tasks with the legacy UI, see Assign Actions (Legacy UI).

> **Important:**
> 
> For virtual documents other than XML virtual documents:
> 
> *   Do not use the `CLEAR`, `APPEND`, or `INSERT`. (To clear a property value in a virtual document, use `SET` with an empty string.)
>     
> *   Do not manually change escape sequences in the data transformation; InterSystems IRIS handles these automatically.
>     

## Introduction

There are five kinds of actions that set or clear values: `SET`, `CLEAR`, `REMOVE`, `APPEND`, and `INSERT`.

The DTL diagram shows each of them with a connector line.

### Objects and Object References

If you use any of these actions to set a value from the top-level source object or any object property of another object as your source, the target receives a cloned copy of the object rather than the object itself. This prevents inadvertent sharing of object references and saves the effort of generating cloned objects yourself. There is an exception: if the object has a property that is a list or array of objects, only the list reference is cloned, the actual objects within the list retain their original reference, thus still pointing to the source objects.

If you instead want to share object references between source and target, you must `SET` from the source to an intermediate temporary variable, and then `SET` from that variable to the target.

## Adding a SET Action

A `SET` action assigns a value to one or more properties in the target message. To create a `SET` action:

1.  Add an action, choosing `SET` from the `New` drop-down list.
    
2.  In the new action, specify the following details:
    
    *   `target`—Identifies the property into which the new value will be written. This may be an object property or a virtual document property path. Generally it is a property of the target message used by the transformation. You must enter the target property.
        
        To refer to a property of the target message, type `target` into this field; the editor then displays a menu listing properties of the target message.
        
    *   `source`—Specifies the value to use; this can be a property, a literal value, or a more general expression.
        
        To refer to a property of the source message, type `source` into this field; the editor then displays a menu listing properties of the source message. You could also refer to a different property of the target message.
        
        A numeric literal is just a number. For example: 42.3
        
        A string literal is a set of characters enclosed by double quotes. For example: `"ABD"`
        
        > **Note:**
        > 
        > This string cannot include XML reserved characters. For virtual documents, this string cannot include separator characters used by that virtual document format. For details, see Syntax Rules.
        
        To create an expression that uses a function, click the Find Functions button . This invokes the Function Wizard.
        
        To create a more complex expression, type the expression into the `source` field. See Valid Expressions. Make sure that the expression is valid in the scripting language you chose for the data transformation; see Specifying Transformation Details.
        
    *   `key`—Option is relevant only for collection properties; see below.
        
    *   `comment`—Specifies an optional description.
        
    *   `language`—Select the language for the `source` expression.
        

## Shortcuts for Adding a SET Action

The DTL Editor provides quick ways to add `SET` actions for some simple scenarios.

### Copying the Source Message

To create a `SET` action that copies the source message:

1.  Click within the `source` box. This box then becomes yellow.
    
2.  Click within the `target` box. This box then becomes yellow.
    

A connector is drawn between the boxes, and the `Actions` area shows a new `SET` action. The new action looks like this:

[Image: target:target and source:source]

### Copying a Value from a Source Property to a Target Property

To create a `SET` action that copies a value from a source property to a target property:

1.  Click within the box for the source property. This box then becomes yellow.
    
2.  Click within the box for the target property. This box then becomes yellow.
    

A connector is drawn between the boxes, and the `Actions` area shows a new `SET` action. The new action looks something like this:

[Image: target:target.ABC and source:source.ABC]

## Using the Function Wizard

To access and use the `Function Wizard`:

1.  Click the Find Functions button .
    
2.  Select a `Function` from the drop-down list.
    
    More fields display as needed to define the expression.
    
    If you select `Repeat Current Function` from the drop-down list, a copy of the current function is inserted as a parameter of the itself, which creates a recursive call to the function.
    
3.  Edit the fields as needed. For instructions, see the context-sensitive help in the dialog.
    
4.  Click `Save` to save your changes and exit the wizard.
    

For details on the existing functions, see Utility Functions for Use in Productions. For information on adding custom functions, see Defining Custom Utility Functions.

## SET and Collections

Sometimes a target property is a collection, and you want to set a value within that collection, which could be either of the following kinds of collections:

*   Collection properties in standard production messages.
    
*   Repeating fields in XML virtual documents.
    

To change the value of an item from a collection, create a SET action. For `target`, use syntax that refers to the collection item you want to set. For array properties, use the key of the array item. For list properties, use the index of the list item. For repeating fields in virtual documents, use the index of the segment or field.

For example:

```
target.MyArrayProp("key2")
```

Equivalently, specify `target` so that it omits a reference to the collection item. In this case, specify `key` as the item to change.

## Adding an INSERT Action

This section applies to list properties (but not array properties) in standard production messages. You can also use this action with XML virtual documents; see Routing XML Virtual Documents in Productions.

To insert an item into a list:

1.  Add an action, choosing `INSERT` from the `New` drop-down list.
    
2.  In the new action, specify the following details:
    
    *   For `target`, select the target list property, for example: `target.MyListProp`
        
    *   Edit `source` to contain a literal value or other valid expression.
        
        See Valid Expressions. Make sure that the expression is valid in the scripting DTL Editor you chose for the data transformation; see Specifying Transformation Details.
        
    *   For `key`, identify the index position for the new item.
        
        For example: 5
        

## Adding an APPEND Action

This section applies to list properties (but not array properties) in standard production messages. You can also use this action with XML virtual documents; see Routing XML Virtual Documents in Productions.

To append an item into a list:

1.  Add an action, choosing `APPEND` from the `New` drop-down list.
    
2.  In the new action, specify the following details:
    
    *   For `target`, select the target list property, for example: `target.MyListProp`
        
    *   Edit `source` to contain a literal value or other valid expression.
        
        See Valid Expressions. Make sure that the expression is valid in the scripting DTL Editor you chose for the data transformation; see Specifying Transformation Details.
        

## Adding a REMOVE Action

This section applies to properties in virtual documents.

To remove a property:

1.  Add an action, choosing `REMOVE` from the `New` drop-down list.
    
2.  For `target`, select the property to remove.
    

> **Important:**
> 
> When you remove properties from a virtual document, it is necessary to perform an additional step known as building the map for the message. There are two ways that you can do this:
> 
> *   Before the steps that remove properties, set the `AutoBuildMap` property to build the map automatically when the properties are deleted. To do this, include a `SET` action that sets `target.AutoBuildMap` equal to 1.
>     
> *   After the steps that remove properties, call the `BuildMap()` method. To do this, include a `CODE` action that includes this line:
>     
>     ```
>      do target.BuildMap()
>     ```
>     

## REMOVE and Collections

This section applies to collection properties (lists and arrays) in standard production messages. You can also use this action with XML virtual documents; see Routing XML Virtual Documents in Productions.

To remove an item from a collection:

1.  Add an action, choosing `REMOVE` from the `New` drop-down list.
    
2.  In the new action, specify the following details:
    
    *   For `target`, select the collection property.
        
    *   For `key`, identify the item to remove.
        
        For array properties, use the key of the array item. For list properties, use the index of the list item. For repeating fields in virtual documents, use the index of the segment or field.
        
        For example:
        
        ```
        "key2"
        ```
        

## Clearing a Collection Property

This section applies to collection properties (lists and arrays) in standard production messages. You can also use this action with XML virtual documents; see Routing XML Virtual Documents in Productions.

To clear the contents of a collection:

1.  Add an action, choosing `CLEAR` from the `New` drop-down list.
    
2.  For `target`, select the collection property. For example: target.MyArrayProp
    

## See Also

*   Adding and Editing Actions
    
*   DTL Syntax Rules
    
*   Other Actions
    
*   Testing Data Transformations
