# Deploying a Production

Typically, you develop a production on a development system and then, after completing and testing the production on a test deployment, you deploy it on a live production system. This page describes how to use the Management Portal to package a deployment from a development system and then to deploy it on another system. It also describes how you can develop and test changes to a production and then deploy those updates to a system running with live business data.

## Overview of Deploying a Production

You can deploy a production using either the Management Portal or an IDE. The Management Portal automates some steps that you need to perform manually using an IDE. If you have a live production that is being used and are developing updates to the production, you need to ensure that the live production is updated without interrupting your processing of business data. At its simplest level deploying a production is done by exporting the XML definition of the production from one system and importing and compiling the XML on a target system. The most important issues for a successful deployment from development to live systems are:

*   Ensuring that the XML deployment file has all required components.
    
*   Testing the deployment file on a test system before deploying it to the live system.
    
*   Ensuring that the deployment file is loaded on the target system without disrupting the live production.
    

Typically, deploying a production to a live system is an iterative process, with the following steps:

1.  Export the production from the development system.
    
2.  Deploy the deployment file on a test system.
    
3.  Ensure that the production has all required components and runs properly on the test system. If any failures are found fix them and repeat step 1.
    
4.  After the production has been deployed to the test system without errors, deploy the deployment file to the live system. Monitor the live system to ensure that the production continues to run correctly.
    

You should ensure that the test system environment matches as closely as possible the environment of the live system. If you are updating an existing production, the production on the test system should match the production on the live system before the update is applied. If you are deploying a production on a new InterSystems IRIS installation, the test system should be a new InterSystems IRIS installation.

In order to update a component in a running production, you must do the following:

1.  Load the updated XML on the system.
    
2.  Compile the XML.
    
3.  Update the running instances of the component to the new code by disabling and re-enabling the component.
    

The deployment process is slightly different depending on whether or not the target system is already running a version of the production. If the target system is running an older version of the production, then the deployment file should contain only the updated components and some configuration items, and, in most cases, it should not contain the definition of the production class. If the target system does not contain the production, the deployment file should contain all production components and settings. If you use the `Interoperability` > `Manage` > `Deploy Changes` > `Deploy` Management Portal page to deploy updates to a running production, the portal automatically does the following:

1.  Creates a rollback and log file.
    
2.  Disables components that have configuration items in the deployment file.
    
3.  Imports and compiles the XML. If there is a compilation error, the portal automatically rolls back the deployment.
    
4.  Enables the disabled components
    

There are some conditions where you have to explicitly stop and restart a component or the entire production. If you are using an IDE or importing the classes from the Management Portal `System Explorer`, then you have to perform these steps manually.

In order to export and deploy a production, you must have the appropriate permissions, for example:

*   `%Ens_Deploy:USE` to access to the `Interoperability` > `Manage` > `Deployment Changes` page and deployment actions
    
*   `%Ens_DeploymentPkg:USE` to export the XML to the server
    
*   `%Ens_DeploymentPkgClient:WRITE` to export the XML locally using the web browser
    
*   `%Ens_DeploymentPkgClient:USE` to deploy the XML using the web browser
    

By default, these resources are granted automatically only to users with the role `%EnsRole_Administrator`. For more information, see Ensemble Resources to Protect Activities.

## Exporting a Production

To export the XML for a production using the Management Portal, open the production, click `Production Settings` and the `Actions` tab and then click the `Export` button. InterSystems IRIS selects all business services, business processes, business operations, and some related classes, and then displays a form to allow you to add export notes and additional components. This form has the following areas:

*   The upper left provides read-only information on the export, including the following details:
    
    *   `Production` — Full name of the production class, including the package or packages.
        
    *   `Namespace` — Namespace in which the export is being performed.
        
    *   `Instance` — Name of the instance in which the export is being performed.
        
    *   `Machine` — Name of the machine on which the export is being performed.
        
    *   `User` — Name of the user performing the export.
        
*   In the upper right, the `Export Notes` field lets you record any notes to include within the export.
    
*   The middle area lets you choose additional items to include in the export package:
    
    [Image: generated description: export itemtypes]
    
    When you click any button in this area, InterSystems IRIS then displays a dialog box where you can choose items of that type to include.
    
*   The lower area lists the items that you have selected to export. These items are shown in two groups: `Manually Added` (which shows the items you manually added as described in the previous bullet), and `Production` (which shows the default items to export).
    

You can also export a business service, process, or operation by selecting the component in the production configuration and then clicking the `Export` button on the `Actions` tab. In both cases, you can add additional components to the package by clicking on one of the buttons and selecting a component. You can remove components from the package by clearing the check box.

You can use the export notes to describe what is in the deployment package. For example, you can describe whether a complete production is in the package or set of components that are an update to a production. The export notes are displayed when you are deploying the package to a target system using the Management Portal.

When you are exporting a deployment package, the first decision you should make is whether the target system has an older version of the production.

If you are deploying the production as a new installation, you should:

*   Include the definition of the production class.
    
*   Include the production settings.
    
*   Include the definitions of all components used in the production.
    
*   Exclude the production settings (ptd file) for each component. This would duplicate the definition in the production class.
    

If you are deploying the production to update a live version of the production, you should:

*   Exclude the definition of the production class.
    
*   Exclude the production settings unless there are changes and you want to override any local settings.
    
*   Include the definition of all components that have been updated.
    
*   Include the production settings (ptd) file for any component whose setting have been changed or that should be disabled before the XML is imported and compiled.
    

Although many components are included by default in the package, you have to add others manually by selecting one of the buttons in the `Add to package` section. For example, if any of the following are used in your production, you need to add them manually:

*   Record maps—the defined and generated classes are included.
    
*   Complex record maps—the defined and generated classes are included.
    
*   Lookup tables
    
*   User classes referenced in code
    
*   System default settings or schedule specifications that are set as deployable
    

The `Production Settings` button allows you to add the production ptd file. This XML defines the following:

*   Production comments
    
*   General pool size
    
*   Whether testing is enabled and whether trace events should be logged.
    

You can deselect any component in the list by clearing its check box. You can select a component by checking its box. The `Select All` button checks all the boxes and the `Unselect All` button clears all check boxes.

Once you have selected the components for the deployment package, create it by clicking `Export`. You can save the export file to the server or locally via the browser’s downloading capability. If you export it to the server, you can specify the file location. If you export it via the web browser, you can specify the file name.

The deployment package contains the following information about how it was created:

*   Name of the system running InterSystems IRIS
    
*   Namespace containing the production
    
*   Name of the source production
    
*   User who exported the production
    
*   UTC timestamp when the production was exported
    

You should keep a copy of the deployment file on your development system. You can use it to create a new deployment package with the latest changes to the components. Keeping a copy of the deployment file saves you from having to manually select the components to be included in the deployment file.

To create a new deployment package using an existing deployment package to select the components, do the following:

1.  On the development system with the updated production, click `Production Settings` and the `Actions` tab and then the `Re-Export` button.
    
2.  Select the file containing the older deployment package.
    
3.  InterSystems IRIS selects the same components from the current production that were included in the older deployment package.
    
4.  If there were any components missing from the older deployment package or if you have added new components to the production, add the missing components manually.
    
5.  Click the `Export` button to save a new deployment package with the updated components.
    

> **Note:**
> 
> If a production uses XSD schemas for XML documents or uses an old format schema for X12 documents, the schemas are not included in the XML deployment file and have to be deployed through another mechanism. InterSystems IRIS can store X12 schemas in the current format, in an old format, or in both formats. When you create a deployment file, it can contain X12 schemas in the current format, but it does not contain any X12 schemas in the old format or any XSD schemas for XML documents. If your production uses an old format X12 schema or uses any XSD XML schema, you must deploy the schemas independently of deploying the production. For the schemas that are not included in the deployment file, they can be deployed to a target system by either of the following means:
> 
> *   If the XML or X12 schema was originally imported from an XSD or SEF file and that file is still available, import the schema on the target system by importing that file. XSD files can be used to import XML schemas and SEF files can be used to import X12 schemas.
>     
> *   Export the underlying InterSystems IRIS global that contains the schema and then import this on the target system. To export a global, select `System Explorer` > `Globals`, select the desired globals and then select `Export`. The X12 schemas are stored in the `EnsEDI.Description`, `EnsEDI.Schema`, `EnsEDI.X12.Description`, and `EnsEDI.X12.Schema` globals. The XML schemas are stored in the `EnsEDI.XML.Schema` global. See Exporting Globalsfor details on exporting globals.
>     

## Deploying a Production on a Target System

The Management Portal automates the process of deploying a production from a development system to a live system. This section describes what InterSystems IRIS does when you are loading a new version of a production on a live system.

Once you have the deployment package XML file, you can load it on a target system. In the Management Portal, select the correct namespace and click `Interoperability`, `Manage`, `Deployment Changes`, `Deploy`, and then click the `Open Deployment` or `Open Local Deployment` button, depending on whether the XML deployment package is located on the server or on the local machine. The `Open Local Deployment` button is not active if you are on the server machine. After you select the XML deployment package file, the form lists the new and changed items in the deployment package, displays the deployment notes that were specified when the package was created and allows you to specify the following deployment settings:

*   Target production—specifies the production that the components will be added to. If the deployment package includes the production class from the source production, then the target production is set to the source production and cannot be changed. Otherwise, InterSystems IRIS sets the default production to the currently open production, but allows you to change it.
    
*   Rollback file—specifies the file to contain the rollback information. The rollback file contains the current definitions of all components that are being replaced by the deployment.
    
*   Deployment log file—contains a log of the changes caused by the deployment.
    

When you have read the deployment notes and made any changes to the deployment settings, complete the deployment by clicking the `Deploy` button. As part of deploying the package, InterSystems IRIS does the following to stop the production, load the new code, and then restart the production.

1.  Create and save the rollback package.
    
2.  Disable the components in the production that have a production settings (ptd) file in the deployment package.
    
3.  Import the XML file and compile the code. If there is an error compiling any component, the entire deployment is rolled back.
    
4.  Update the production settings.
    
5.  Write a log detailing the deployment.
    
6.  Enable the production components that were disabled if their current setting specify that they are enabled.
    

To undo the results of this deployment change, use the `Open Deployment` button to select the rollback file, then click the `Deploy` button.
