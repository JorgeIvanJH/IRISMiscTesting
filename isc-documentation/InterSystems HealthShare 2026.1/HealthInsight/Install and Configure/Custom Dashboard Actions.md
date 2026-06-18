# [Adding Custom Actions to Health Insight Dashboards](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_actions#HSAAIC_actions)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

An action is any custom code that you want to execute on a dashboard, such as opening a different web page or application with data about the currently selected patient or patients. This chapter describes how to create custom actions and add them to dashboards.

## [Defining Custom Actions](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_actions#HSAAIC_actions_defining)

To define custom actions, do the following:

1.  Create a KPI class that defines the `%OnDashboardAction()` method as described in “[Defining Custom Actions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2IMP_ch_action)” in [Implementing InterSystems IRIS Business Intelligence](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2IMP).
    
    A KPI class can define a KPI (key performance indicator), a set of actions, or both. In this case, the class needs only to define actions. The [following subsection](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_actions#HSAAIC_actions_sampleclass) provides a template that you can easily reuse.
    
    For information on the recommended location of the class, see “[Ensuring That Your Customizations Support Mirroring and Easier Upgrades](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_customization_approach),” earlier in this book.
    
2.  Compile this class.
    
    It is not necessary to rebuild any cubes after compiling the KPI class.
    
3.  Navigate to the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page).
    
4.  Select `Customization` > `Additional Settings`.
    
5.  For `Patient Actions`, enter the fully qualified name of the action class, for example `Implementation.MyPatientActionClass`
    

### [Sample KPI/Action Class](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_actions#HSAAIC_actions_sampleclass)

The following is a sample of a KPI class that only defines actions:

```xml
Class HSAA.Demo.PatientActions Extends %DeepSee.KPI
{

Parameter DOMAIN = "MYANALYTICSAPP";

/// This XData definition defines the KPI.
XData KPI [ XMLNamespace = "http://www.intersystems.com/deepsee/kpi" ]
{
<kpi xmlns="http://www.intersystems.com/deepsee/kpi"
 name="PatientActions" sourceType="mdx"
 caption="PatientActions"
>
<action name="AddPatientToProgram" displayName="Add to Cohort"/>
<action name="AssignToCareManager" displayName="Assign to Care Manager"/>
<action name="ViewPatientRecord" displayName="View Patient Record" />
</kpi>
}

/// This callback is invoked from a dashboard when an action defined by this dashboard is invoked.
ClassMethod %OnDashboardAction(pAction As %String, pContext As %ZEN.proxyObject) As %Status
{
  // pAction is the name of the action (as defined in the XML list).
  // pContext contains information from the client
  // and can be used to return information.
  If ((pAction = "Add to Program") || (pAction = "AddPatientToProgram")) {
    Set pContext.command =
    "popup:/csp/healthshare/hsregistry/Analytics.ProgramSelect.cls?PatIDs="_pContext.valueList_";"
  }
  If ((pAction = "Assign to Care Manager") || (pAction = "AssignToCareManager")) {
    Set pContext.command =
    "popup:/csp/healthshare/hsregistry/Analytics.SelectCareManager.cls?PatIDs="_pContext.valueList_";"
  }
  If ((pAction = "View Patient Record") || (pAction = "ViewPatientRecord")) {
    Set pContext.command =
    "newWindow:/csp/healthshare/analytics/ViewPatient.CSP?HSAAID="_pContext.valueList_";"
  }
  Quit $$$OK
}

}
```

Note the following points:

*   The `DOMAIN` parameter controls the domain that contains any localizable strings in this class.
    
*   The XData block provides metadata that the Dashboard Designer uses.
    
*   Within `<kpi>`, you must specify values for `name` and for `sourceType`. The `sourceType` is ignored if the class does not define a query. You can just use `"mdx"` for this value, as shown in the example.
    
*   Within `<kpi>`, you must include one `<action>` element for each action that you are defining. Within this element, `name` is required. `displayName` is optional but enables you to localize your application. The best practice is to always include a value for `displayName`.
    
*   The `%OnDashboardAction()` method defines the actions. This method should always have the argument list and return value as shown in this example. The method should always return a [%Status](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&CLASSNAME=%25Library.Status) value.
    
*   The body of the `%OnDashboardAction()` method consists of an If... Elseif... construct, or a series of If commands, as shown.
    
*   An action could, as shown here, display a CSP page or a Zen page (or other web address). The general syntax for this is as follows:
    
    ```objectscript
     Set pContext.command = "popup:complete_or_partial_URL;"
    ```
    
    Or:
    
    ```objectscript
     Set pContext.command = "newWindow:complete_or_partial_URL;"
    ```
    
    Where `complete_or_partial_URL` is either a complete URL (starting with `http` or `https`) or is a URL within the same web application as the dashboard page.
    
    The first version displays a popup window, and the second displays a new browser window.
    
*   If the destination URL permits parameters, include them in the URL string. For examples, see the `PatIDs` and `HSAAID` parameters in the example code. The parameters that are supported depend upon the destination URL. For example, if the destination URL is a Zen page, the code for that page would contain code that supports parameters with specific names.
    
    As the value of a parameter, you might want to pass the analytics IDs of the currently selected patient or patients. To do so, use the variable `pContext.valueList` as shown in the example code.
    

Additionally, in version 2019.1 of HealthShare Health Insight, programs were renamed to cohorts. However, in some areas, cohorts are still referred to as programs.

## [Adding Actions to Dashboards](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_actions#HSAAIC_actions_add_dashboard)

To add an action to a dashboard, add a button (or other control) to a widget on the dashboard as follows:

1.  If the action requires values from the widget, make sure that the dashboard contains an appropriate widget.
    
    When the user selects the action button, the system passes values to that action as follows:
    
    *   For a pivot table widget that displays a pivot table or a KPI, the system passes the value of the first selected cell. If the user has displayed a listing, the system also passes a comma-separated list of values from first column of listing; the listing must not contain commas.
        
    *   For a scorecard widget, the system passes the value of the property that is marked as `Value Column`. (To find this option, go to `Scorecard>Columns`.)
        
    
    For details, see “[Defining Custom Actions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2IMP_ch_action)” in [Implementing InterSystems IRIS Business Intelligence](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2IMP).
    
2.  Access the Dashboard Editor and select the applicable widget.
    
3.  Select `Controls`.
    
4.  Select the plus sign + button.
    
    The system displays a dialog box where you specify the details of the control.
    
5.  Specify the following options:
    
    *   `Location` — Specifies where the control is shown:
        
        *   `Widget` (the default) displays the control on the widget toolbar.
            
            If you use this option, be sure not to hide the toolbar (via the `Toolbar` option in `Settings`).
            
        *   `Dashboard` displays the control in the `Filters` worklist.
            
            Do not use `Dashboard` if this dashboard is a zero-worklist dashboard, because the control would not be visible to users. (To control the number of worklists on a dashboard, use `Dashboard Settings` in the Dashboard Editor.)
            
        *   `Onclick Event` configures the control as an onclick control. No visible indication of the control is given.
            
    *   `Target` — Leave this blank.
        
    *   `Action` — Select the custom action. These are shown at the end of the list.
        
    *   `Type` — Select `button` or `auto` (which is shown as a button in this case)
        
        (Or if `Location` is `Onclick Event`, ignore `Type`.)
        
    *   `Control Label or Icon` — Optionally type the text that you want to display on the button. Or select an icon to display next to the control. For information on adding icons that can be used here, see “[Creating Icons](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2IMP_ch_settings#D2IMP_settings_icons)” in [Implementing InterSystems IRIS Business Intelligence](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2IMP).
        
    *   `Active When` — Specifies when this control is active. Choose one of the following values:
        
        *   `Always` — This control is always active.
            
        *   `Item Selected` — This control is active when the user selects one or more cells in a pivot table. The control is inactive otherwise.
            
        *   `1 Listing Item Selected` — This control is active when the user selects a single row of a listing. The control is inactive otherwise.
            
        *   `Listing Item Selected` — This control is active when the user selects one or more rows of a listing. The control is inactive otherwise.
            
    *   `Control Tooltip` — Specifies a tooltip to display when the user hovers the cursor over the control.
        
    *   `Control Size` — Specifies the width of the control.
        
6.  Select `OK` to add the control.
    
7.  Save the dashboard.
