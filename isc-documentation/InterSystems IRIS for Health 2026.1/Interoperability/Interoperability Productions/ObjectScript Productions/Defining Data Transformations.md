# Defining Data Transformations

This page discusses data transformations.

## Introduction to Defining Data Transformations

A data transformation creates a new message that is a transformation of another message. When you transform a message, your data transformation sends a new message body that is a transformation of the original. Some of the transformations that occur during this process can include:

*   Copying values from properties on the source to properties on the target.
    
*   Performing calculations using the values of properties on the source.
    
*   Copying the results of calculations to properties on the target.
    
*   Assigning literal values to properties on the target.
    
*   Ignoring any properties on the source that are not relevant to the target.
    

## Defining DTL Transformations

A DTL transformation is a class based on Ens.DataTransformDTL. In this case, you can create and edit the transformation visually in the DTL editor, which you can access in the Management Portal or in an IDE. The DTL editor is meant for use by nontechnical users. See Developing DTL Transformations.

## Defining Custom Transformations

A custom transformation is a subclass of Ens.DataTransform that specifies:

*   The name of the input (source) message class
    
*   The name of the output (target) message class
    
*   A series of operations that assign values to the properties of the output object
    

Each assignment operation consists of a call to the Ens.DataTransform class method `Transform()`. The argument is a simple expression that is evaluated to provide the value for one of the properties in the output class. The expression can contain:

*   Literal values
    
*   Any property in the general-purpose execution context variable called `context`
    
*   Properties on the source object
    
*   Functions and operators from the expression language
    
*   Calls to methods provided by InterSystems IRIS data platform
    
*   Calls to user-provided methods
