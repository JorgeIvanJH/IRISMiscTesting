# Creating Data Transformations

This topic describes generally how to create and edit data transformations for interoperability productions.

You can also visit Online Learning to try Creating a Data Transformation.

> **Note:**
> 
> For information on the legacy DTL Editor, see Introduction to the Legacy Editor.

## Building DTLs During a Migration

If you intend to migrate to InterSystems IRIS for Health from other vendors, and you have a body of existing source and target messages, you can streamline the process of creating the necessary DTLs:

*   You can automatically generate a starting DTL that performs the simpler transformations.
    
*   You can compare the target messages output from the generated DTL to the original target messages, quickly identifying message segments that require attention.
    

To build a post-migration DTL using an existing body of source messages and target messages, follow the instructions at DTL Generator.

## Creating a Transformation

To create a transformation:

1.  Display the DTL Editor.
    
2.  Click `New`.
    
    InterSystems IRIS then displays a dialog box where you can specify the basic information for the transformation.
    
3.  Specify some or all of the following information:
    
    *   `Package` (required)—Enter a package name.
        
        Do not use a reserved package name; see Reserved Package Names.
        
    *   `Name` (required)—Enter a name for your data transformation class.
        
    *   `Description`—Enter an description for the data transformation; this becomes the class description.
        
    *   `Source Class`—Specifies the type of messages that this transformation will receive as input.
        
        If you are using a common input type, click one of the following options:
        
        *   `All Messages`—This transformation can be used with any input message type.
            
        *   `HL7`—The input messages are instances of EnsLib.HL7.Message.
            
        *   `X12`—The input messages are instances of EnsLib.EDI.X12.Document.
            
        *   `ASTM`—The input messages are instances of EnsLib.EDI.ASTM.Document.
            
        *   `EDIFACT`—The input messages are instances of EnsLib.EDI.EDIFACT.Document.
            
        *   `XML`—The input messages are instances of EnsLib.EDI.XML.Document.
            
        
        Otherwise click the search icon and then select the class.
        
    *   `Source Document Type` (applicable only if the messages are virtual documents)—Enter or choose the document type of the source messages. You can choose any type defined in the applicable schemas loaded into this namespace.
        
    *   `Target Type` and `Target Class`—Specifies the type of messages that this transformation will generate as output. See the choices for `Source Class`.
        
    *   `Target Document Type` (applicable only if the messages are virtual documents)—Enter or choose the document type of the target messages. You can choose any type defined in the applicable schemas loaded into this namespace.
        
    
    Apart from `Package` and `Name`, you can edit all these details later.
    
4.  Specify details on the `Transform` tab. See Specifying Transformation Details.
    
5.  Then add actions as needed.
    

## Opening an Existing Transformation

To open a transformation:

1.  Display the DTL Editor.
    
2.  Click `Open`.
    
    If you are currently viewing a transformation and you have made changes but have not yet saved them, InterSystems IRIS prompts you to confirm that you want to proceed (which will discard those changes).
    
3.  Click the package that contains the transformation.
    
    Then click the subpackage as needed.
    
4.  Click the transformation class.
    

## Specifying Transformation Details

To see details that define the transformation as a whole:

1.  Display the DTL Editor.
    
2.  Click the Settings icon .
    

These details are as follows:

*   `DTL Name` (read-only)—Complete package and class name of the data transformation class.
    
*   `Description`—Description of the data transformation. You can edit this manually or you can generate a description from the DTL diagram; see Using the DTL Explainer.
    
*   `Source Class`—Specifies the type of messages that this transformation will receive as input. For details, see Creating a Transformation.
    
*   `Source Document Type` (applicable only if the messages are virtual documents)—Specifies the document type of the source messages.
    
*   `Target Class`—Specifies the type of messages that this transformation will generate as output. For details, see Creating a Transformation.
    
*   `Target Document Type` (applicable only if the messages are virtual documents)—Specifies the document type of the target messages.
    
*   `Mode`—Specifies how the transformation should create the target message. Choose one of the following:
    
    *   `Create new`—Create a new object of the target class (and type, if applicable), before executing the elements within the data transformation. This is the default.
        
    *   `Copy`—Create a copy of the source object to use as the target object, before executing the elements within the transform.
        
    *   `Existing`—Use an existing object, provided by the caller of the data transformation, as the target object. See the following subsection.
        
*   `Report Errors`—Specifies whether InterSystems IRIS should log any errors that it encounters when executing this transform. If you select this option, InterSystems IRIS logs the errors as Warnings in the Event Log. InterSystems IRIS also returns a composite status code containing all errors as its return value. This option is selected by default.
    
*   `Treat empty repeating fields as null`—Specifies whether InterSystems IRIS skips the following actions for repeating fields when the fields are empty:
    
    *   `foreach` actions—If you select this option, InterSystems IRIS does not execute `foreach` actions on repeating fields that are empty.
        
    *   `assign` actions—If you select this option, InterSystems IRIS does not execute `assign` actions on repeating fields if you use shortcut notation to indicate that both the `source` and `target` fields are repeating fields, and the `source` field is empty. For example, if the `source.{PV1:AdmittingDoctor()}` field is empty and you select this option, then InterSystems IRIS does not execute the following action:
        
        `<assign value='source.{PV1:AdmittingDoctor()}' property='target.{PV1:AdmittingDoctor()}' action='set'`.
        
        However, InterSystems IRIS does execute the following similar action since the `target` field is not a repeating field:
        
        `<assign value='source.{PV1:AdmittingDoctor()}' property='target.{PV1:AdmittingDoctor(1)}' action='set' />`
        
        This option is cleared by default.
        
*   `Allow empty segments in target`—Specifies whether to ignore errors caused by attempts to get field values out of absent source segments of virtual documents or properties of objects. If you select this option, InterSystems IRIS suppresses these errors and does not call subtransforms where the named source is absent. This option is selected by default.
    
    You can precisely control the behavior by including tests and conditional logic branches to confirm that any required elements are present.
    
*   `Language`—Specifies the language you will use in any expressions in this DTL. This can be `python` or `objectscript`.
    
*   `Python From/Import Statements`;Specifies an optional list of Python `from / import` statements, one per line. Use this so that Python code within this DTL can refer to these modules.
    

### When to Use an Existing Object As the Target

For `Mode`, the `Existing` option enables you to specify the target as an existing object, which results in a performance improvement. This option applies when you invoke a series of transformations programmatically (or perform other sequential processing). You would use this option in cases like the following scenario:

*   You have three transformations that you want to perform in sequence:
    
    1.  `MyApp.ADTTransform`—Uses the `Create New` option for `Mode`.
        
    2.  `MyApp.MRNTransform`—Uses the `Existing` option for `Mode`.
        
    3.  `MyApp.LabXTransform`—Uses the `Existing` option for `Mode`.
        
*   You invoke the transforms as follows:
    
    ```
    do MyApp.ADTTransform.Transform(message,.target)
    do MyApp.MRNTransform(target,.newtarget)
    do MyApp.LabXTransform(newtarget,.outmessage)
    ```
    

## Using the DTL Explainer

If your system is configured to include the DTL Explainer, there is a `Generate New` button next to the `Description` text box. This button enables you to generate a description of the DTL. The DTL Explainer is an AI tool that examines the DTL logic and creates a description summarizing the contents of that logic. You can use this description as part or all of your description, and you can edit it if needed. You can also discard it.

> **Note:**
> 
> This is an AI Tool. Errors may occur. See Disclaimer for more information.

To use the DTL Explainer:

1.  Click `Generate New`.
    
    The system then displays a read-only generated description, including a disclaimer.
    
    If the DTL is large, the processing may take some time.
    
2.  If there is currently no text in the `Description` field, the system displays the generated description. Now you can either:
    
    *   To close the generated description without saving it, click the X in the upper right.
        
    *   To insert the generated description, scroll to the bottom and click `Insert`.
        
    
    If there is current text in `Description` field, you have more options:
    
    *   To close the generated description without saving it, click the X in the upper right.
        
    *   To replace the description with the generated description, scroll to the bottom and click `Replace`.
        
    *   To insert the generated description before the existing description, scroll to the bottom and click `Insert` > `Prepend`.
        
    *   To insert the generated description after the existing description, scroll to the bottom and click `Insert` > `Append`.
        
3.  Make and save any additional edits.
    

If you save the generated description, it is fully editable and it no longer contains the disclaimer.

## Undoing and Redoing Changes

To undo the previous change, click the Undo button .

To redo the previous change, click the Redo button .

## Saving a Transformation

To save a transformation, do one of the following:

*   Click `Save`.
    
*   Click `Save As`. Then specify a new package, class name, and description and click `OK`.
    
*   Click `Compile`. This option saves the transformation and then compiles it.
    

## Compiling a Transformation

To compile a transformation, click `Compile`. This option saves the transformation and then compiles it.

## Deleting a Transformation

To delete a transformation, you use a different page in the Management Portal:

1.  In the Management Portal, click `Interoperability` > `List` > `Data Transformations`.
    
2.  Click the row that displays its name.
    
3.  Click the `Delete` button.
    
4.  Click `OK` to confirm this action.
    

## See Also

*   Introduction to the DTL Editor
    
*   Adding and Editing Actions
    
*   Listing and Managing Data Transformations
    
*   Testing Data Transformations
