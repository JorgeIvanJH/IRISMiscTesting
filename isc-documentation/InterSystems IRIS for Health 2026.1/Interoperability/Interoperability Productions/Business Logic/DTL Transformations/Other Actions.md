# Other Actions

This topic provides details for actions that do not modify values, within a DTL data transformation for interoperability productions.

For information on performing these tasks with the legacy UI, see Other Actions (Legacy UI).

## Adding an IF Action

An `IF` action executes other actions conditionally, depending on the value of an expression that you provide. InterSystems IRIS represents each `IF` action as a connector line in the DTL diagram.

To add an `IF` action:

1.  Add an action, choosing `IF` from the `New` drop-down list.
    
    The `Actions` area contains two new rows, labeled as follows:
    
    *   `IF`—This row marks the beginning of actions to perform if the condition is true.
        
    *   `ELSE`—This row marks the beginning of actions to perform if the condition is false.
        
2.  In the `IF` row, edit the `condition` field so that it contains an expression that evaluates to either true or false.
    
    For example:
    
    ```
    source.ABC = "XYZ"
    ```
    
    Notes:
    
    *   To create an expression that uses a function, click the Find Functions button , select a function, and click `Save`.
        
    *   To create a more complex expression, type the expression into the `Value` field. See Valid Expressions. Make sure that the expression is valid in the scripting language you chose for the data transformation; see Specifying Transformation Details.
        
3.  To add actions to perform when the condition is true:
    
    1.  Click the `IF` row.
        
    2.  Select an item from the `New` drop-down list.
        
    3.  Edit the new action as needed.
        
    4.  Repeat as necessary.
        
4.  To add actions to perform when the condition is false:
    
    1.  Click the `ELSE` row.
        
    2.  Continue as described in the preceding item.
        

> **Note:**
> 
> It is not required to have any actions for the `IF` branch or for the `ELSE` branch. If there are no actions in either branch, the `IF` action has no effect.

## Adding a FOR EACH Action

The `FOR EACH` action enables you to define a sequence of actions that is executed iteratively, once for each member of one of the following:

*   A collection property (for a standard message).
    
*   A repeating property (for a virtual document).
    
*   A set of subdocuments in a document (for a virtual document).
    

InterSystems IRIS represents each `FOR EACH` action as a connector line in the DTL diagram.

You can break out of a `FOR EACH` loop at any time by adding a `BREAK` action within the loop.

To add a `FOR EACH` action:

1.  Add an action, choosing `FOR EACH` from the `New` drop-down list.
    
2.  For the `target` field, specify a collection or repeating property in the source message.
    
    For the `FOR EACH` action, the `key` field specifies the name of an iterator variable.
    
    The `target` field should not include the iterator key within the parentheses. For example, the following is correct:
    
    ```
    source.{PID:PatientIdentifierList( )}
    ```
    
    The `FOR EACH` iterates through the `PatientIdentifierList` repeating fields, starting with the first one (numbered 1) and ending with the last one.
    
3.  The `Unload` check box controls whether to generate code to unload open objects or segments.
    
    If the `Unload` is checked for a `FOR EACH` action, then code is generated in the Transform method to try to unload/unswizzle open object(s) or segment(s) for the property collection at the end of each loop. Unsaved virtual document segments are saved and finalized. If the property is the source object, the source object is usually already saved.
    
    You may still need to manually add actions to unload the target collection’s objects or segments. For details on some strategies, see Unloading Target Collections.
    
    The unload of the `FOR EACH` property collection may be unnecessary – for example, for HL7, code generated using CopyValues does not instantiate the source segments.
    
4.  To add actions to the `FOR EACH` block, click the `FOR EACH` action and then add the appropriate actions.
    

The details are then shown in the block below the DTL diagram.

If the `FOR EACH` applies to a collection property in a message, the sequence of activities is executed iteratively, once for every element that exists within the collection property. If the element is null, the sequence is not executed. The sequence is executed if the element has an empty value, that is, the separators are there but there is no value between them, but is not executed for a null value, that is, the message is terminated before the field is specified.

### Shortcuts for the FOR EACH Action

When you are working with virtual documents, InterSystems IRIS provides a shortcut notation that iterates through every instance of a repeating field within a document structure. This means you do not actually need to set up multiple nested `FOR EACH` loops to handle repeating fields; instead you create a single `assign` action using a virtual property path with empty parentheses within the curly bracket { } syntax. For information, see Curly Bracket {} Syntax.

> **Note:**
> 
> If the source and target types are different, you cannot use this shortcut for the `FOR EACH` action. Use an explicit `FOR EACH` action in these cases.

### Unloading Target Collections

While the `Unload` option automatically removes objects from a source collection, you need to add custom code at the end of a `FOR EACH` action to remove objects from a target collection. In a simple example in which the target is a complex record, you could use the following code to save the current target record and then unload it:

```
Do target.Record16.GetAt(k1).%Save(0)
Do target.Record16.%UnSwizzleAt(k1)
```

In other scenarios, it might be better to avoid loading the target altogether in order to avoid issues where the target is not unloaded. For example, suppose you have an object that has a parent/child property with many children. Within the `FOR EACH` action, you have a subtransform combined with `propSetObjectId(parentId))`, where `prop` is the name of the property.

In this example, the target is the batch object, the target class is `Demo.RecordMapBatch.Map.TrainDataOut.BatchOut` and the record class is `Demo.RecordMapBatch.Transform.Optimized.Record`

Before your `FOR EACH` loop, you need to create an empty target and assign its ID to a property `BatchOutID`:

```
<assign value='target.%Save()' property='tSC' action='set' />
<assign value='target.%Id()' property='BatchOutID' action='set' />
<assign value='target' property='' action='set' />
```

Then, in the `FOR EACH` loop, you can use code that directly impacts the target without having the target instantiated. For example:

```
<assign value='""' property='record' action='set' />
<subtransform class='Demo.RecordMapBatch.Transform.Optimized.Record' targetObj='record' sourceObj='source.Records.(k1)' />

<comment>
<annotation>Assign record to target directly. </annotation>
</comment>
<assign value='record.%ParentBatchSetObjectId(BatchOutID)' property='tSC' action='set' />
<assign value='record.%Save()' property='tSC' action='set' />
```

Then, before the DTL ends, set the variable `target` back to the expected product of the DTL. For example:

```
<assign value='##class(Demo.RecordMapBatch.Map.TrainDataOut.BatchOut).%OpenId(BatchOutID)' property='target' action='set' />
```

### Avoiding <STORE> Errors with Large Messages

As you loop over segments in messages or object collections, they are brought into memory. If these objects consume all the memory assigned to the current process, you may get unexpected errors. You can avoid these errors in the source collection by using the `Unload` option in the Management Portal. For some strategies for removing objects in a target collection, see Unloading Target Collections.

As another strategy, if you are processing many segments in a `FOR EACH` loop, you can call the `commitSegmentByPath()` method on both the source and target as the last step in the loop. Similarly, for object collections, use the `%UnSwizzleAt()` method.

The method `commitCollectionOpenSegments()` loops through the runtimePath looking for open segments within the specified collection path and calls `commitSegmentByPath()` for each open segment. This method is available from the classes EnsLib.EDI.X12.Document, EnsLib.EDI.ASTM.Document, EnsLib.EDI.EDIFACT.Document, and EnsLib.HL7.Message.

If you cannot make code changes, a temporary workaround is to increase the amount of memory allocated for each process. You can change this by setting the `bbsiz` parameter on the `Advanced Memory Settings` page in the Management Portal. Note that this action requires a system restart, and you should consult with your system administrator before performing it.

## Adding a SUBTRANSFORM Action

A `SUBTRANSFORM` action invokes another transformation (an ordinary transformation), often within a `FOR EACH` loop. Subtransformations are particularly useful with virtual documents, because EDI formats are typically based on a set of segments that are used in many message types. The ability to reuse a transformation within another transformation means that you can create a reusable library of segment transformations that you can call as needed, without duplicating code transformation.

InterSystems IRIS does not represent a `SUBTRANSFORM` action in the DTL diagram.

To add a `SUBTRANSFORM` action:

1.  Add an action, choosing `SUBTRANSFORM` from the `New` drop-down list.
    
2.  In the new action, specify the following details:
    
    *   `target`—Identifies the property into which the transformed value will be written. This may be an object property or a virtual document property path. Generally it is a property of the target message used by the transformation. You must enter the target property.
        
    *   `source`—Identifies the property being transformed. This may be an object property or a virtual document property path. Generally it is a property of the source message used by the transformation. You must enter the source property.
        
    *   `auxiliary property`—Optionally, specifies a value to be passed to the subtransform. The subtransform accesses the value as the `aux` variable. To pass multiple values:
        
        1.  Create an array variable with subscripts as in the following example:
            
            ```
             set MyVar(1)="first value"
             set MyVar(2)="second value"
            ```
            
        2.  Include a period immediately before the name of this variable, within the `auxiliary property` field. (The period indicates that this variable is passed by reference, which is the required way to pass a variable that has subscripts.)
            
            Within the subtransform, you can access these values as `aux(1)` and `aux(2)`. That is, the `aux` variable has the same subscripts that you specified in the input array variable.
            
    *   `class`—Specifies the data transformation class to use. This can be either a DTL transformation or a custom transformation. For information on custom transformations, see Defining Custom Transformations. You must enter the class.
        
    *   `comment`—Specifies an optional comment.
        
    
    > **Note:**
    > 
    > In the case of a `SUBTRANSFORM` with `Mode` as `Create new` or `Copy`, it is not necessary to have a pre-existing target object.
    

## Adding a TRACE Action

A `TRACE` action generates a trace message, which is helpful for diagnosis. If the Log Trace Events setting is enabled for the parent business host, this message is written to the Event Log. If the Foreground setting is enabled for the parent business host, the trace messages are also written to the Terminal window.

InterSystems IRIS does not represent a `TRACE` action in the DTL diagram.

To add a `TRACE` action:

1.  Add an action, choosing `TRACE` from the `New` drop-down list.
    
2.  In the new action, specify the following:
    
    *   `source`—Specify a literal value or other valid expression.
        
        See Valid Expressions. Make sure that the expression is valid in the selected language.
        
    *   `comment`—Specify an optional description.
        
    *   `language`—Select the language for this expression.
        

The `TRACE` action generates trace message with User priority; the result is the same as using the `$$$TRACE` macro in ObjectScript.

## Adding a CODE Action

A `CODE` action enables you to execute one or more lines of user-written code within a DTL data transformation. This option enables you to perform tasks that are difficult to express using the DTL elements. InterSystems IRIS does not represent a `CODE` action in the DTL diagram.

To add a `CODE` action:

1.  Add an action, choosing `CODE` from the `New` drop-down list.
    
2.  In the new action, specify the following:
    
    *   `code`—Specify one or more lines of code in the specified language. For rules about expressions in this code, see Syntax Rules.
        
        If you are using ObjectScript, make sure that each line starts with a space.
        
        InterSystems IRIS automatically wraps your code within a `CDATA` block. This means that you do not have to escape special XML characters such as the apostrophe (') or the ampersand (&),
        
        Also see the notes below.
        
    *   `comment`—Specify an optional description.
        
    *   `language`—Select the language for this expression.
        

> **Tip:**
> 
> To write custom code that you can debug easily, write the code within a class method or a routine so that it can be executed in the Terminal. Debug the code there. Then call the method or routine from within the code action of the DTL.

### Guidelines for Using Custom Code in DTL

In order to ensure that execution of a data transformation can be suspended and restored, you should follow these guidelines when using a code action:

*   The execution time should be short; custom code should not tie up the general execution of the data transformation.
    
*   Do not allocate any system resources (such as taking out locks or opening devices) without releasing them within the same code action.
    
*   If a code action starts a transaction, make sure that the same action ends the transactions in all possible scenarios; otherwise, the transaction can be left open indefinitely. This could prevent other processing or can cause significant downtime.
    

If you are using ObjectScript, make sure that each line starts with a space.

## Adding an SQL Action

An `SQL` action enables you to execute an SQL SELECT statement from within the DTL transformation. InterSystems IRIS does not represent an `SQL` action in the DTL diagram.

To add an `SQL` action:

1.  Add an action, choosing `SQL` from the `New` drop-down list.
    
2.  In the new action, specify the following:
    
    *   `code`—Specify a valid SQL SELECT statement.
        
        InterSystems IRIS automatically wraps your SQL within a `CDATA` block. This means that you do not have to escape special XML characters such as the apostrophe (') or the ampersand (&).
        
        Also see the notes below.
        
    *   `comment`—Specify an optional description.
        

### Guidelines for Using SQL in DTL

Be sure to use the following guidelines:

*   Always use the fully qualified name of the table, including both the SQL schema name and table name, as in:
    
    `MyApp.PatientTable`
    
    Where `MyApp` is the SQL schema name and `PatientTable` is the table name.
    
*   Any tables listed in the FROM clause must either be stored within the local InterSystems IRIS database or linked to an external relational database using the SQL Gateway.
    
*   Within the INTO and WHERE clauses of the SQL query, you can refer to a property of the source or target object. To do so, place a colon (`:`) in front of the property name. For example:
    
    ```
      SELECT Name INTO :target.Name FROM MainFrame.EmployeeRecord WHERE SSN = :source.SSN AND City = :source.Home.City
    ```
    
*   Only the first row returned by the query will be used. Make sure that the WHERE clause correctly specifies the desired row.
    

## Adding a SWITCH Action

A `SWITCH` action contains a sequence of one or more `CASE` actions and a `DEFAULT` action. When a `SWITCH` action is executed, it begins evaluating each `CASE` condition. When an expression evaluates to true, then the contents of the corresponding `CASE` block are executed; otherwise, the expression for the next `CASE` action is evaluated. As soon as one of the `CASE` actions is executed, the execution path of the transformation leaves the `SWITCH` block without evaluating any other conditions. If no `CASE` condition is true, the contents of the `DEFAULT` action are executed and then control leaves the `SWITCH` block.

To add an `SWITCH` action:

1.  Add an action, choosing `SWITCH` from the `New` drop-down list.
    
    This adds three rows to the `Actions` area, labeled `SWITCH`, `CASE`, and `DEFAULT`.
    
2.  In the `SWITCH` row, specify the following:
    
    *   `comment`—Specify an optional description.
        
    *   `language`—Select the language for the expressions used in this action.
        
3.  Add more `CASE` actions if needed.
    
4.  Modify the `CASE` rows as follows:
    
    *   `condition`, specify the condition. You can click the magnifying glass to add a function as part of the condition.
        
    *   `comment`—Specify an optional description.
        
5.  Optionally modify the `DEFAULT` row. It is not necessary to include any steps within the `DEFAULT` action.
    
6.  In each of these branches, add actions to perform in the given scenarios. For example, you may want to set a target property a specific way when a condition is true.
    

## Adding a CASE Action

Use the `CASE` action within a `SWITCH` block to execute a block of actions when a condition is matched. When a `CASE` condition is met and the block of actions performed, the execution path of the transformation leaves the `SWITCH` block without evaluating any other conditions.

To add a `CASE` action:

1.  Select a `SWITCH` action in the `Actions` area.
    
2.  Select `CASE` from the `New` drop-down list.
    
3.  For `condition`, specify the condition. You can click the magnifying glass to add a function as part of the condition.
    
4.  With the `CASE` action selected in the `Actions` area, use the `New` drop-down to add the actions that will be executed if the condition evaluates to true.
    

## Adding a Default Action

You cannot add a `DEFAULT` block by using the `New` drop-down list. Rather, the `DEFAULT` action is automatically added to a `SWITCH` block when you add the `SWITCH` action. The actions contained in the `DEFAULT` block are executed if none of the `CASE` conditions in the `SWITCH` block are met. If you do not want anything to happen when none of the `CASE` conditions are met, simply leave the `DEFAULT` block empty.

## Adding a Break Action

Add a `BREAK` action to a `FOR EACH` loop to leave the loop as soon as the `BREAK` action is executed. After the `BREAK` action is executed, the data transformation continues to process the action immediately following the `FOR EACH` loop.

If you add a `BREAK` action outside of a `FOR EACH` loop, the data transformation terminates as soon as the `BREAK` action is executed.

## Adding a COMMENT Action

To help annotate the actions in a data transformation, you can add a comment that appears in the list of actions. After selecting `Add Action > Comment`, enter the comment in the `Description` text boxin the `Actions` area.

## See Also

*   Adding and Editing Actions
    
*   DTL Syntax Rules
    
*   Actions That Set or Clear Values
    
*   Testing Data Transformations
