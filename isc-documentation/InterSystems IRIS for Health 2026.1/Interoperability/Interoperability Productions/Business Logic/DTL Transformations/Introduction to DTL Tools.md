# Introduction to DTL Tools

DTL transformations are a form of business logic you can use within interoperability productions. This topic introduces the tools that InterSystems IRIS data platform provides to enable you to develop and test DTL transformations.

## Background

A data transformation creates a new message that is a transformation of another message. It is common for a production to use data transformations, to adjust outgoing messages to the requirements of the target systems.

You can create and edit a DTL transformation visually in the DTL Editor, available in either the Management Portal or your IDE. The DTL Editor is meant for use by nontechnical users. The term DTL represents Data Transformation Language, which is the XML-based language that InterSystems IRIS uses internally to represent the definition of a transformation that you create in this editor.

You can invoke a data transformation from a business process, another data transformation, or a business rule. Note that there is overlap among the options available in business processes, data transformations, and business rules. For a comparison, see Comparison of Business Logic Tools. You can also try using these tools yourself by Creating a Data Transformation.

## Available Tools in the Management Portal

The Management Portal provides the following tools for working with data transformations:

*   The DTL Editor, which enables you to create, edit, and compile DTL transformations.
    
*   The Data Transformation List page, which enables you to test, import, export, and delete either kind of data transformation. It also enables you to open a DTL transformation in the DTL Editor.
    

## Other Tools

You can also invoke a data transformation programmatically, which can be useful for testing purposes. See Testing Data Transformations.

Also, because data transformations are classes, you can edit them and work with them in the same way that you do any other class.

## Using Data Transformations

You can invoke a data transformation from the following parts of a production:

*   From another DTL data transformation. See Adding a Subtransform Action.
    
*   From a BPL business process. See <transform>.
    
*   From a business rule. See Passing Data to a Data Transformation.
    
*   From a custom business process or a custom DTL transformation. To do so, execute it programmatically as described in Testing Data Transformations.
    

> **Note:**
> 
> This section applies to both DTL transformations and custom transformations.

## See Also

*   Comparison of Business Logic Tools
    
*   Introduction to the DTL Editor
    
*   Creating Data Transformations
    
*   Adding and Editing Actions
    
*   DTL Syntax Rules
    
*   Listing and Managing Data Transformations
    
*   Testing Data Transformations
