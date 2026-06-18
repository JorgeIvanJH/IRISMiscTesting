# Introduction to the DTL Editor

The DTL Editor enables you to create, edit, and compile DTL transformations.

> **Important:**
> 
> After a period of inactivity, the InterSystems Management Portal may log you out and discard any unsaved changes. Inactivity is the time between calls to the InterSystems IRIS server. Not all actions constitute a call to the server. For example, clicking `Save` constitutes a call to the server, but typing in a text field does not. Consequently, if you are editing a data transformation, but have not clicked `Save` for longer than `Session Timeout` threshold, your session will expire and your unsaved changes will be discarded. After a logout, the login page appears or the current page is refreshed. For more information, see Automatic Logout Behavior in the Management Portal.

For information on performing these tasks with the legacy UI, see Creating Data Transformations (Legacy UI).

## Displaying the DTL Editor

To access this page in the Management Portal:

1.  Select `Interoperability` > `Build` > `Data Transformations`.
    
2.  Click `Try the new UI`.
    

You can also access the DTL Editor from the Production Configuration page.

## A Look at the User Interface

When first displayed, the DTL Editor contains two areas. The upper area displays the source and target messages, along with options that enable you to work with the data transformation as a whole:

[Image: generated description: neweditor top]

Notice the name of the DTL being edited (`Scan.ChangeForSafeEmailDTL` in this example) and the names of the source and target message classes (`Scan.CheckEmployeeRequest` in both cases, in this example). This area of the page is meant to provide a quick visual overview of the DTL. In most cases, a DTL copies or modifies parts of the source message class to the target message class, and the connection lines indicate this visually.

The menu bar provides options you can use to do the following:

*   Undo or redo your most recent change, via the buttons on the top left.
    
*   Display the two parts of the page size by side, via the Side by Side button.
    
*   Create a new DTL transform or open an existing one (via the `New` and `Open` buttons, respectively).
    
*   Save the transform or save it to a new name (via the `Save` and `Save As` buttons, respectively).
    
*   Compile the transform (via the `Compile` button).
    
*   Display the test page (via the `Test` button).
    
*   Display other details for the transformation, via the gear icon on the right.
    

In this area, via drag and drop, you can add new actions—specifically the kinds of actions that modify values. To do so, select an option from `Create new` and then hover the cursor over a field in the source message and drag to a field in the target message; you can create `SET`, `APPEND`, `INSERT`, `CLEAR`, and `REMOVE` actions.

The bottom area of the page shows the actual DTL transformation, which is an ordered list of actions. In the following example, the DTL contains four actions.

[Image: generated description: neweditor bottom]

The menu bar of this area allows you to make more detailed changes to the DTL. Here you can do the following:

*   Cut, copy, and paste actions from one spot to another.
    
*   Delete actions.
    
*   Move actions to earlier or later parts of the DTL.
    
*   Disable actions.
    
*   Create new actions, via the `New` dropdown. In contrast to the button in the upper area, this dropdown lets you create any kind of action. When you select an option from this dropdown, a dialog box prompts for details.
    

When you select an action in this list, the display changes so that you can make edits.

## See Also

*   Introduction to DTL Tools
    
*   Creating Data Transformations
    
*   DTL Syntax Rules
    
*   Listing and Managing Data Transformations
    
*   Testing Data Transformations
    
*   Introduction to the Production Configuration Page
