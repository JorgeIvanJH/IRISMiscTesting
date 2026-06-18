# Listing and Managing Data Transformations

The `Data Transformation List` page enables you to list, import, export, test, and delete data transformations, which are a form of business logic you can use within interoperability productions.

## Introduction

To access the `Data Transformation List` page in the Management Portal, click `Interoperability` > `List` > `Data Transformations`.

The page lists the data transformation classes defined in the current namespace. This page lists two kinds of transformations:

*   DTL transformations are displayed in blue. You can double-click one to open it in the DTL Editor.
    
*   Custom transformations are displayed in black. These classes are based on Ens.DataTransform and do not use DTL. You must edit these in your IDE.
    

## Options on This Page

To use this page, select a data transformation and then click one of the following commands in the ribbon bar:

*   `Edit`—(DTL transformations only) Click to change or view the data transformation using the DTL Editor.
    
*   `Test`—Click to test the selected transformation class using the Test Transform wizard.
    
    For details, see Testing Data Transformations.
    
*   `Delete`—Click to delete the selected transformation class.
    
*   `Export`—Click to export the selected transformation class to an XML file.
    
*   `Import`—Click to import a data transformation that was exported to an XML file.
    

## Related Options

You can also export and import these classes as you do any other class in InterSystems IRIS. You can use the `System Explorer` > `Globals` page of the Management Portal.

## See Also

*   Comparison of Business Logic Tools
    
*   Introduction to DTL Tools
    
*   Introduction to the DTL Editor
    
*   Creating Data Transformations
    
*   Testing Data Transformations
