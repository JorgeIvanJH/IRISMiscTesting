# Testing Data Transformations

After you compile a data transformation class, you can (and should) test it. This topic describes how to do so.

> **Note:**
> 
> This topic applies to both DTL transformations and custom transformations.

## Using the Transformation Testing Page

The Management Portal provides the `Test Transform` wizard. You can access this from the following locations in the Management Portal:

*   Click `Test` from the `Tools` tab in the Data Transformation Builder
    
*   Select the transformation and click `Test` on the Data Transformation List page.
    

Initially the `Output Message` window is blank and the `Input Message` window contains a text skeleton in a format appropriate to the source message. To test:

1.  If your DTL code references the properties of the aux, context, or process systems objects, enter values for these properties to see the results as if the data transformation was invoked with these objects instantiated. The table for entering values appears only if the DTL references the internal properties of aux, process, or context systems objects.
    
2.  Edit the `Input Message` so that it contains appropriate data. What displays and what you enter in the input box depends on your source type and class:
    
    *   For EDI messages, the window displays raw text; have some saved text files ready so that you can copy and paste text from these files into the `Input Message` box.
        
    *   For regular production messages, the window displays an XML skeleton with an entry for each of the properties in the message object; type in a value for each property.
        
    *   For record maps, complex record maps, and batch record maps, you can enter raw text or XML.
        
3.  Click `Test`.
    
4.  Review the results in the `Output Message` box.
    

## Testing a Transformation Programmatically

To test a transformation programmatically, do the following in the Terminal (or write a routine or class method that contains these steps):

1.  Create an instance of the source message class.
    
2.  Set properties of that instance.
    
3.  Invoke the `Transform()` class method of your transformation class. This method has the following signature:
    
    ```
    classmethod Transform(source As %RegisteredObject, ByRef target As %RegisteredObject) as %Status
    ```
    
    Where:
    
    *   `source` is the source message.
        
    *   `target` is the target message created by the transformation.
        
4.  Examine the target message and see if it has been transformed as wanted. For an easy way to examine both messages in XML format, do the following:
    
    1.  Create an instance of %XML.Writer.
        
    2.  Optionally set the `Indent` property of that instance equal to 1.
        
        This adds line breaks to the output.
        
    3.  Call the `RootObject()` method of the writer instance, passing the source message as the argument.
        
    4.  Kill the writer instance.
        
    5.  Repeat with the target message.
        

For example:

```objectscript
 //create an instance of the source message
 set source=##class(DTLTest.Message).CreateOne()
 set writer=##class(%XML.Writer).%New()
 set writer.Indent=1 do writer.RootObject(source)
 write !!
 set sc=##class(DTLTest.Xform1).Transform(source,.target)
 if $$$ISERR(sc)
  {do $system.Status.DisplayError(sc)}
 set writer=##class(%XML.Writer).%New()
 set writer.Indent=1
 do writer.RootObject(target)
```

## See Also

*   Introduction to DTL Tools
    
*   Introduction to the DTL Editor
    
*   Creating Data Transformations
    
*   DTL Syntax Rules
    
*   Listing and Managing Data Transformations
