# [Performing Actions in a Health Insight Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_actions#HSAA_actions)

An action is an activity that affects one or more patients that you initiate from a dashboard. HealthShare Health Insight provides several standard actions, and your implementation might include additional custom actions. This chapter describes how to find and initiate an action.

## [Finding Actions in a Detail Listing](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_actions#HSAA_actions_finding)

Actions are available only within detail listings. A detail listing is a table that displays data for individual patients. A detail listing can be included directly in a dashboard (the sample `Diabetes Population Analytics` dashboard includes a detail listing in its lower area). The image below illustrates a detail listing with three actions: `Add Patient to Cohort`, `Assign to Care Manager`, and `View Patient Record`.

[Image: Partial image of dashboard with detail listing displayed]

(Sometimes a dashboard displays a button that you can click to display a detail listing.)

Detail listings may include a row of controls at the top. Some of these controls are basic business intelligence system options like sorting and filtering. Others can be actions, either the predefined actions described in this chapter or custom actions added by an implementer.

For information on the basic business intelligence system controls, see [Using Dashboards](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2USER_ch_using). Any control that is not described there is either an action or a basic system control with a custom button.

## [Adding Patients to a Cohort from a Health Insight Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_actions#HSAA_actions_addtoprog)

To add one or more patients to an existing cohort:

1.  Display a dashboard that includes the `Add Patient to Cohort` action (such as the sample dashboard `Diabetes Population Analytics`).
    
2.  If the dashboard does not directly display the listing, select one or more cells in a pivot table or graph and then select the Display Listing button.
    
3.  Select the check box at the start of the row for each patient that you want to add.
    
4.  Select the `Add Patient to Cohort` button.
    
5.  Select a cohort from the drop-down list.
    
6.  Select `OK`.
    

The system then adds the selected patients to the cohort. The change is visible in the Registry of the HealthShare Unified Care Record.

## [Assigning Patients to a Care Manager from a Health Insight Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_actions#HSAA_actions_assigntocaremgr)

To assign one or more patients to a care manager:

1.  Display a dashboard that includes the `Assign to Care Manager` action (such as the sample dashboard `Diabetes Population Analytics`).
    
2.  If the dashboard does not directly display the listing, select one or more cells in a pivot table or graph and then select the Display Listing button.
    
3.  Select the check box at the start of the row for each patient that you want to assign.
    
4.  Select the `Assign to Care Manager` button.
    
5.  Select a care manager from the drop-down list.
    
6.  Select `OK`.
    

## [Viewing a Patient from a Health Insight Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_actions#HSAA_actions_view)

To view details for a patient:

1.  Display a dashboard that includes the `View Patient Record` action (such as the sample dashboard `Diabetes Population Analytics`).
    
2.  If the dashboard does not directly display the listing, select one or more cells in a pivot table or graph and then select the Display Listing button.
    
3.  Select the check box at the start of the row for the patient.
    
4.  Select the `View Patient Record` button.
    
    Note that this button is active only when a single patient has been selected.
    

The system then displays a page with details for the selected patient.
