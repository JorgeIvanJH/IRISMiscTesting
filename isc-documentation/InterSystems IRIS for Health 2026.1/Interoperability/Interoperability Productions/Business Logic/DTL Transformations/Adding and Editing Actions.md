# Adding and Editing Actions

This page describes generally how to add, edit, and rearrange actions within a DTL transformation.

For information on performing these tasks with the legacy UI, see Adding and Editing Actions (Legacy UI).

## Adding an Action

To add an action, do the following in the `Actions` area:

1.  Decide where to place the new action, and click the action just before where you want the new action to be included.
    
2.  Click the `New` menu and then select an action.
    
    The DTL Editor adds the new action below the action you had selected.
    
3.  Edit the details for the new action.
    

Other techniques are possible for `assign` actions, as discussed in Actions That Set or Clear Values.

## Editing an Action

To edit an action, first select it. To do so, do one of the following:

*   If the DTL diagram displays the action, click the icon on the corresponding connector line.
    
*   Click the item in the `Actions` area.
    

Now edit the values in the `Actions` area. Optionally, you can disable the action by selecting it and then clicking the `Disabled` check box. If you disable a `FOR EACH` or `IF` action, all actions within the block are also disabled.

## Rearranging Actions

InterSystems IRIS executes the actions in the order they are listed in the `Actions` area.

To rearrange actions, use the `Actions` area:

1.  Click the check box for the action.
    
2.  Click either the up arrow or the down arrow, as needed:
    

Alternatively, use the Cut , Copy , and Paste buttons.

To delete an action, click the check box or the action and then click the Delete button.

## See Also

*   Introduction to the DTL Editor
    
*   Creating Data Transformations
    
*   Actions That Set or Clear Values
    
*   Other Actions
