# SDA-FHIR Transformations

InterSystems provides transformations that convert SDA objects into HL7 FHIR resources (and vice-versa) using the data transformation language (DTL). SDA is an intermediary clinical format that makes it easier to go from one standard to another. For example, rather than transform HL7v2 to FHIR directly, a system can convert HL7v2 to SDA and then SDA to FHIR. For more information about SDA, see SDA: InterSystems Clinical Data Format.

The bi-directional SDA-FHIR transformations can provide useful functionality in many different use cases, including:

*   Taking content from an SDA-aware system and providing it to a FHIR system.
    
*   Taking content from an SDA-aware system and storing it in a FHIR repository.
    
*   Taking content from multiple SDA-aware systems and normalizing it for use or storage in a FHIR system.
    
*   Taking content from a FHIR system and providing it to an SDA-aware system.
    

> **Note:**
> 
> Transformations between SDA and FHIR are available for FHIR R4 and earlier, but not supported for FHIR R5.

You have two options for invoking the DTL transformations that convert SDA objects into FHIR resources and vice-versa. You can invoke the DTL transformations by adding a built-in business process to an interoperability production, or you can call the transformation APIs directly, for example, from a custom business process.

## Transformation Business Processes

You can use built-in business processes to invoke SDA-FHIR transformations in an SDA to FHIR Production or FHIR to SDA Production. For example, a production could consume HL7 messages, use a business process to convert the HL7 to SDA, and then use the built-in SDA-FHIR business process to convert the SDA to FHIR.

For more information about the underlying transformation code used by the built-in business processes, see Transformation APIs. These APIs can be called directly from a custom business process.

### SDA to FHIR Productions

A built-in business process, HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process, can be added to a production to transform SDA objects and containers to FHIR bundles. This production must exist in a Foundation namespace.

Once added to the production, the business process:

*   Accepts an SDA container as input and loops through each contained object.
    
*   Converts the SDA container to FHIR content, in the form of a FHIR `BundleOpens in a new tab` resource.
    
*   Forwards the FHIR content to the business host specified by the `TargetConfigName` setting.
    
*   Receives a response from the business host.
    
*   Returns a response (based on what it received) to the business host that originally called it.
    

The business process in the SDA to FHIR production calls a method of the HS.FHIR.DTL.Util.API.Transform.SDA3ToFHIR class to perform the transformation. For details about how this class handles the transformation, see Transformation Details.

#### Adding the Business Process

To begin, open your production in the Production Configuration window of the Management Portal and add the HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process business process. Once added, you can modify the business process settings that impact the transformation. For an introduction to adding business processes to an interoperability production, see InterSystems IRIS Basics: Connecting Systems Using Interoperability Productions.

#### Business Process Settings

Settings of HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process that influence SDA to FHIR conversions include:

##### TargetConfigName

Specifies the business host to which HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process sends its output. This setting is located in the `Basic Settings` section of the `Settings` tab in the Production Configuration window.

##### TransmissionMode

Specifies how the business process transmits the FHIR bundle for further processing:

*   `transaction` — The business process sends the bundle of resources in a single interaction and the processing succeeds or fails for the whole of the bundle; if processing any single resource fails, processing for the other resources (and the entire bundle) stops. This is the default.
    
*   `individual` — The business process sends each resource from the bundle separately as its own interaction.
    
    This setting is located in the `Additional Settings` section of the `Settings` tab in the Production Configuration window.
    

##### FullTransactionResponse

If selected, the FHIR request message that this process sends is created with a "PREFER" header value set to "return=representation". Per the FHIR spec, this header indicates to a FHIR server that every created or updated resource should be returned in its entirety as it is saved (i.e., with any modifications applied by the server). Whether the server actually does this depends on the server.

In general, this setting should be left unchecked except during debugging or if the FHIR client has a specific need to receive back the created/updated resources, as requesting this information is likely to increase response time from the FHIR server. This setting is located in the `Additional Settings` section of the `Settings` tab in the Production Configuration window.

##### FHIRFormat

Specifies whether the content is in XML or JSON format. This setting is located in the `Additional Settings` section of the `Settings` tab in the Production Configuration window.

##### FormatFHIROutput

Specifies whether or not content is formatted for readability. If selected, this setting has a performance impact, and as such should be enabled only during development and testing. This setting is located in the `Additional Settings` section of the `Settings` tab in the Production Configuration window.

##### CallbackClass

Deprecated.

##### ValidResourceRequired

Deprecated.

##### OutputToQuickStream

If selected, the FHIR payload sent by this business process is placed in an HS.SDA3.QuickStream object, and the id of the QuickStream object is placed in the `QuickStreamId` property of the request message. If left unselected, the FHIR output from the transformation is placed in the `Payload` property of the request message. This setting is located in the `Additional Settings` section of the `Settings` tab in the Production Configuration window.

##### TransformClass

Specifies name of the class that performs the transformation. If you subclass HS.FHIR.DTL.Util.API.Transform.SDA3ToFHIR to customize the transformation behavior, you need to specify the name of that subclass.

##### FHIRMetadataSet

Specifies the version of the outgoing FHIR based on a package. All available packages appear in the drop-down list.

##### FHIREndpoint

Specifies the endpoint of a FHIR server. This setting is required if your business process is sending the outgoing FHIR to an `HS.FHIRServer.Interop.Operation` business operation on its way to the FHIR server’s Service.

#### Assigning a Patient ID

You can use the `AdditionalInfo` property of the SDA message sent to HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process to assign an ID to the Patient resource that is created by the SDA-FHIR transformation. When the SDA message contains an `AdditionalInfo` item named `PatientResourceId`, the transformation takes the value of `PatientResourceId` and assigns it to the Id field of the generated Patient resource.

> **Note:**
> 
> The underlying class, HS.FHIR.DTL.Util.API.Transform.SDA3ToFHIR, used by the transformation business process contains a method that can be overridden to assign Ids to resources, including patient resources. For more information, see Customizing Transformation API Classes.

#### Messages

The request message to HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process is either Ens.Container or HS.Message.XMLMessage.

There is no response message from HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process. It returns a success or failure status instead.

### FHIR to SDA Productions

A built-in business process, HS.FHIR.DTL.Util.HC.FHIR.SDA3.Process, can be added to a production to transform FHIR resources and bundles into SDA objects and containers. This production must exist in a Foundation namespace.

Once added to the production, the business process:

*   Accepts a FHIR resource or bundle as input.
    
*   Converts the FHIR content to an SDA container.
    
*   Forwards the container to the business host specified by the `TargetConfigName` setting.
    
*   Receives the response from the business host.
    
*   Returns a FHIR response (based on what it received) to the business host that originally called it.
    

The business process in the SDA to FHIR production calls a method of the HS.FHIR.DTL.Util.API.Transform.FHIRToSDA3 class to perform the transformation. For details about how this class handles the transformation, see Transformation Details.

#### Adding the Business Process

To begin, open your production in the Production Configuration window of the Management Portal and add the HS.FHIR.DTL.Util.HC.FHIR.SDA3.Process business process. Once added, you can modify the business process settings that impact the transformation. For an introduction to adding business processes to an interoperability production, see First Look: Connecting Systems Using Interoperability Productions.

#### Business Process Settings

Settings of HS.FHIR.DTL.Util.HC.FHIR.SDA3.Process that influence FHIR to SDA conversions include:

*   `TargetConfigName` — Specifies the business host where the XMLMessage that includes the SDA3 stream is sent after it is transformed from FHIR by the DTL transformation. This setting is located in the `Basic Settings` section of the `Settings` tab in the Production Configuration window.
    
*   `CallbackClass` — Deprecated.
    
*   `OutputToQuickStream` — By default, the output of HS.FHIR.DTL.Util.HC.FHIR.SDA3.Process is an HS.Message.XMLMessage object that contains the SDA3 stream produced by the DTL transformation. If this setting is checked, the SDA3 stream is placed in a separate HS.SDA3.QuickStream object, and the QuickStreamID of the QuickStream object is placed in the `AdditionalInfoItem` property of the XMLMessage. If this setting is not selected, the SDA3 stream is placed in the `ContentStream` property of the XMLMessage. This setting is located in the `Additional Settings` section of the `Settings` tab in the Production Configuration window.
    
*   `TransformClass` — Specifies name of the class that performs the transformation. If you subclass HS.FHIR.DTL.Util.API.Transform.FHIRToSDA3 to customize the transformation behavior, you need to specify the name of that subclass.
    
*   `FHIRMetadataSet` — Specifies the version of the incoming FHIR based on a package. All available packages appear in the drop-down list.
    

## Transformation APIs

Your application has access to both:

*   SDA to FHIR APIs
    
*   FHIR to SDA APIs
    

### SDA to FHIR APIs

The APIs that your code uses to transform SDA to FHIR are found in HS.FHIR.DTL.Util.API.Transform.SDA3ToFHIR. Your application can call the `TransformStream()` or `TransformObject()` method, depending on whether the SDA is in a %Stream.Object or an SDA object.

Both of these methods return a transformation object (HS.FHIR.DTL.Util.API.Transform.SDA3ToFHIR) that contains the FHIR output in its `bundle` property, which is of type `%DynamicObject`. This Bundle contains all of the resources generated by the transformation with all references resolved.

Your code could serialize this `bundle` property from a dynamic object to JSON or XML with the following code. It assumes that `SDA3ToFHIRObject` is the transformation object returned by one of the transformation methods.

```objectscript
 Set stream = ##class(%Stream.TmpCharacter).%New()
 Set metadataSetKey = "R4"
 If format="JSON"
  {
    Do SDA3ToFHIRObject.bundle.%ToJSON(stream)
  }
  ElseIf format="XML"
  {
   Set schema = ##class(HS.FHIRServer.Schema).LoadSchema(metadataSetKey)
   Do ##class(HS.FHIRServer.Util.JSONToXML).JSONToXML(SDA3ToFHIRObject.bundle, stream, schema)
  }
 Do stream.Rewind()
```

*   Using the `TransformStream` method
    
*   Using the `TransformObject` method
    
*   Transformation details
    

#### Using the TransformStream Method

The `TransformStream()` method of HS.FHIR.DTL.Util.API.Transform.SDA3ToFHIR takes in SDA as a `%Stream` and transforms it into a FHIR bundle. Its signature is:

```objectscript
ClassMethod TransformStream(stream As %Stream.Object,
                            SDAClassname As %String,
                            fhirVersion As %String,
                            patientId As %String = "",
                            encounterId As %String = "") {}
```

Parameters:

*   `stream` — A `%Stream` representation of an SDA object or Container.
    
*   `SDAClassname` — The classname for the object contained in the stream (for example, HS.SDA3.Container).
    
*   `fhirVersion` — The version of FHIR produced by the transformation. For example, `STU3` or `R4`.
    
*   `patientId` — If this optional parameter is specified, the `Id` field of the generated Patient resource will have the specified value.
    
*   `encounterId` — If this optional parameter is specified, the `Id` field of the generated Encounter resource will have the specified value. This parameter is ignored if the `stream` parameter is a SDA Container because a Container can have multiple encounters, making it impossible to determine which FHIR Encounter should be given the specified resource id.
    

#### Using the TransformObject Method

The `TransformObject()` method of HS.FHIR.DTL.Util.API.Transform.SDA3ToFHIR takes in SDA as a container or object class and transforms it into a FHIR bundle. Its signature is:

```objectscript
ClassMethod TransformObject(source,
                            fhirVersion As %String,
                            patientId As %String = "",
                            encounterId As %String = "") {}
```

Parameters:

*   `source` — The SDA container or SDA object class that will be converted into FHIR.
    
*   `fhirVersion` — The version of FHIR produced by the transformation. For example, `STU3` or `R4`.
    
*   `patientId` — If this optional parameter is specified, the `Id` field of the generated Patient resource will have the specified value.
    
*   `encounterId` — If this optional parameter is specified, the `Id` field of the generated Encounter resource will have the specified value. This parameter is ignored if the `stream` parameter is an SDA Container because a Container can have multiple encounters, making it impossible to determine which FHIR Encounter should be given the specified id.
    

#### Transformation Details

The following describes the default behavior of SDA to FHIR transformations. For an introduction to methods that can be overridden to customize transformation behavior, see SDA to FHIR Overridable Methods.

*   The incoming stream or object is broken down into individual streamlets, which are in turn transformed into FHIR resources.
    
*   By default, UUIDs are generated and assigned to the `fullUrl` field of the Bundle resource. In this case, the resource itself does not have an `Id`. If you would rather provide a resource id, override the `GetId` method. In this case, the value for `fullUrl` is `baseURL/resourceType/id` and the resource references are `resourceType/id`.
    
*   The methods do not modify incoming URLs at all by default. This behavior can be overridden with the `GetBaseURL()` method: for example, if you are posting to a specific repository, you can provide the URL prefix for the repository.
    
*   Resources will contain references to other resources regardless of the mechanism used to assign IDs.
    
*   Patient and Encounter references will be added to all available resources using the Patient and Encounter streamlets. Encounter references can be made successfully only if the `EncounterNumber` fields in the SDA streamlets are used. If they are empty, no references will be generated.
    
*   In the case of shared resources such as Organization, Practitioner, or Medication, a hash of the first 32 kilobytes of each resource is added to a hash table. Each subsequent shared resource is checked for duplication by searching the hash table for a direct match. If a match is found, the resource will be marked as a duplicate. This behavior can be changed by overriding the `IsDuplicate()` method.
    
*   Each resource is validated before being added to the Bundle. If a resource fails validation, an error is thrown and processing stops, which means the Bundle is not returned. This default behavior can be changed by overriding the `HandleInvalidResource()` method.
    
*   When one or more SDA properties do not map to a FHIR resource field in the target schema, the transformation maps the SDA data to a FHIR extension. For more information, see FHIR Extensions.
    
*   For details about how a specific SDA object or property maps to the target FHIR resource or field, see Understanding SDA-FHIR Mappings.
    

### FHIR to SDA APIs

The APIs that your code uses to transform FHIR to SDA are found in HS.FHIR.DTL.Util.API.Transform.FHIRToSDA3. This class contains multiple APIs that can be used to transform FHIR to SDA, depending on your use case.

In most cases, if your application needs to transform a single FHIR resource or bundle, it should call the class method `TransformStream()` or `TransformObject()`, depending on whether the FHIR is in a %Stream.Object or a dynamic object. However, in cases where you are transforming multiple FHIR bundles or resources in succession, it might be more efficient to instantiate the transformation class once and then call the `Transform()` method multiple times.

All of these transformation methods return a transformation object (HS.FHIR.DTL.Util.API.Transform.FHIRToSDA3) that contains the SDA output in its `container` property, which is of type HS.SDA3.Container. The transformation object’s `object` property contains the last SDA container or object that was generated by the transformation. If the last input was a bundle, the `object` property is an SDA container; if the last input was an individual resource, `object` is an SDA object.

*   Using the `TransformStream` method
    
*   Using the `TransformObject` method
    
*   Using the `Transform` method
    
*   Transformation details
    

#### Using the TransformStream Method

The `TransformStream()` method of HS.FHIR.DTL.Util.API.Transform.FHIRToSDA3 takes in a FHIR resource or bundle represented as a `%Stream` and transforms it into an SDA Container. Resource references are honored only if a FHIR bundle is passed to the method. Its signature is:

```objectscript
ClassMethod TransformStream(stream As %Stream.Object,
                            fhirVersion As %String,
                            fhirFormat As %String) {}
```

Parameters:

*   `stream` — A `%Stream` representation of the FHIR resource or bundle.
    
*   `fhirVersion` — The version of the FHIR resource or bundle being transformed. For example, “STU3” or “R4”.
    
*   `fhirFormat` — Specifies the format of the FHIR resource or bundle. Acceptable values are “JSON” and “XML”.
    

#### Using the TransformObject Method

The `TransformObject()` method of HS.FHIR.DTL.Util.API.Transform.FHIRToSDA3 takes in a FHIR resource or bundle as a dynamic object and transforms it into an SDA Container. Resource references are honored only if a bundle is passed to the method. Its signature is:

```objectscript
ClassMethod TransformObject(source As %DynamicObject,
                            fhirVersion As %String) {}
```

Parameters:

*   `source` — The FHIR resource or bundle represented as a dynamic object.
    
*   `fhirVersion` — The version of the FHIR resource or bundle being transformed. For example, “STU3” or “R4”.
    

#### Using the Transform Method

The `Transform()` method of HS.FHIR.DTL.Util.API.Transform.FHIRToSDA3 takes in a FHIR bundle as a dynamic object and transforms it into an SDA Container. Resource references are honored only if a bundle is passed to the method.

`Transform()` is the method called by the class methods that transform FHIR into SDA. You might want to call it directly if you are transforming multiple FHIR resources in succession so you do not need to instantiate a HS.FHIR.DTL.Util.API.Transform.FHIRToSDA3 object every time. For example, the following code would transform a Patient resource, Encounter resource, and Observation resource using the same transformation object:

```objectscript
 set r4schema = ##class(HS.FHIRServer.Schema).LoadSchema("R4")
 set transformer = ##class(HS.FHIR.DTL.Util.API.Transform.FHIRToSDA3).%New(r4Schema)
 do transformer.Transform(patient)
 do transformer.Transform(encounter)
 do transformer.Transform(Observation)
```

The signature of the `Transform()` method is:

```objectscript
ClassMethod Transform(source As %DynamicObject) {}
```

Parameters:

*   `source` — The FHIR resource or bundle represented as a dynamic object.
    

#### Transformation Details

The following is an overview of the default behavior of FHIR to SDA transformations. For an introduction to methods that can be overridden to customize transformation behavior, see FHIR to SDA Overridable Methods.

*   An incoming FHIR Bundle is broken down into individual resources, and those resources transformed into SDA3 streamlets.
    
*   If a resource referenced by another resource within the incoming FHIR bundle is not present in the bundle, the transformation of the bundle continues. To change this behavior, override the `HandleMissingResource()` method.
    
*   When a transformation is attempting to convert a reference to an object, no object will be created in the SDA streamlet if:
    
    *   A subtransformation exists but the referenced resource has no values for any of the elements with mappings.
        
    *   There is no subtransformation from the referenced resource type to the datatype in the SDA3 object.
        
*   The `EncounterNumber` field on an Encounter streamlet will be populated starting at 1 and incremented for each encounter that is processed. Any subsequent resources that reference that Encounter resource, when transformed to SDA3, will perform a lookup based on the resource ID and will find the encounter number it should use. The assignment of encounter numbers can be overridden with `GetIdentifier()` method. It can be useful to access the contents of the resource being converted in order to determine what EncounterNumber should be returned. The instance property `%currentReference` contains a FHIR reference object that can be passed into the instance method `GetResourceFromReference()` in order to obtain the resource as a dynamic object.
    
*   Similar to encounter numbers, `ExternalID` values for HealthConcern and Goal resources are populated starting at 1 by default. This behavior can be overridden with the `GetIdentifier()` method.
    
*   The value of the SDA `Container:SendingFacility` property is set as follows: if the Patient’s `managingOrganization` field contains a reference to an Organization, and that Organization is in the Bundle, it is used. Otherwise, the patient identifiers are searched for an MRN with an assigning authority, and that assigning authority is used. If neither of these items is found, the string `FHIR` is used. This behavior can be overridden in the `GetSendingFacility()` method.
    
*   SDA3 extensions are not used. If a field does not exist in SDA3, the content will be dropped.
    
*   If a Bundle comes in without a Patient resource, an error will be thrown. Other than that, no validation will be performed on the container. It will simply be returned as is.
    
*   To view information about containment relationships, refer to the FHIR Annotations (`Health` > `FHIR Annotations`) in the Management Portal for the Bundle resource.
    
*   For details about how a specific FHIR resource or field maps to an SDA object or property, see Understanding SDA-FHIR Mappings.
    

## Understanding SDA-FHIR Mappings

Whether you use the transformation API or a built-in business process to perform an SDA-FHIR transformation, you can use the `FHIR Annotations` tool to understand exactly how the SDA or FHIR data was transformed into the target format. The tool gives you an overview of which SDA object was mapped to a particular FHIR resource (or vice-versa) while providing the ability to drill down into the mapping to understand exactly how the properties of the SDA object resulted into fields of a FHIR resource (or vice-versa). When using the `FHIR Annotations` tool, SDA properties are referred to as fields, for example, mappings are referenced as being field-to-field rather than property-to-field. You can also explore how lookup tables were used to map codes between SDA and FHIR, learn more about the data types involved in the transformation, and discover which ObjectScript methods were used in the transformation.

To understand the logic behind mappings, see Mapping Conventions.

*   Accessing the FHIR Annotations Tool
    
*   Mappings Overview
    
*   Mapping Details
    
*   Lookup Table Mappings
    
*   Mapping Conventions
    

### Accessing the FHIR Annotations Tool

To access the `FHIR Annotations` tool:

1.  Log in to the Management Portal as a user with the `%Ens_EDISchemaAnnotations` role.
    
2.  Navigate to `Health` —> MyFHIRnamespace.
    
3.  Expand the `Schema Documentation` menu option and click `FHIR Annotations`.
    

To begin exploring the mappings, use the `Mapping or Information` drop-down list to select the source and target of the transformations. For example, if you are interested in SDA3 to FHIR R4 mappings, select `SDA3 —> FHIR4`.

[Image: SDA to FHIR mappings in Annotations tool]

While using the `FHIR Annotations` tool to explore the SDA-FHIR mappings, you can select the `Help` and `FAQ` buttons to obtain guidance on using and interpreting the user interface of the tool. In addition, hover text is available over many of the elements of the user interface.

### Mappings Overview

Before drilling down into the details of a particular mapping (including field-to-field mappings), it can be useful to gain an overview of all the mappings between SDA objects and FHIR resources. To view a list of how objects and resources map to each other, select `List <transform> Transformed`.

[Image: SDA object to FHIR resource mappings in Annotations tool]

### Mapping Details

If you are interested in the details of how a specific SDA object or FHIR resource is mapped to the target format, you can select the object or resource from the drop-down lists. For example, to view the mapping of the Appointment resource to SDA3, select `Appointment` from the `FHIR4 by Name` drop-down list.

[Image: How Appointment resource maps to an SDA object]

Each mapping is presented in a table that shows all of the SDA field-FHIR field mappings, cardinality of the source field, data type of the source field, and other useful information. To discover more details about the elements in the table, you can:

*   Hover over each element in the table to obtain additional information.
    
*   Click the links to open more details about that element, including the icons in the `Actions` column. For example, you can click a data type to explore how that data type is mapped.
    
*   Click the Mapping Definition icon ([Image: sunglasses icon]) to drill down into the technical details of the mapping. Once the Mapping Definition opens, you can click the FHIR data types to bring them up in the official FHIR specification. You can also view technical details like cardinality, default values, and the subtransformation or class method used by the mapping. In some cases, there are additional notes that help explain the mapping.
    

The following is a legend of the icons in the `Actions` column of the mapping table:

<table><tr><th>Icon</th><th>Meaning</th></tr><tr><td>[Image: sunglasses icon]</td><td>View the detailed Mapping Definition.</td></tr><tr><td>[Image: magnifying glass icon]</td><td>Mapping uses a subtransformation or class method.</td></tr><tr><td>[Image: mathematical function icon]</td><td>Mapping uses a <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXFHIRPROD_transforms#HXFHIRPROD_transforms_mapping_conventions_conditional">Condition to Set this Field</a> to control whether the mapping is used.</td></tr><tr><td>[Image: gear icon]</td><td>Mapping uses a FHIR extension as its target.</td></tr><tr><td>[Image: checkmark icon]</td><td>Mapping assigns a default value to the target when the source contains missing or invalid data.</td></tr><tr><td>[Image: stack of documents icon]</td><td>When the mapping is used, the transformation appends data to an existing target object, rather than creating a new target object.</td></tr><tr><td>[Image: grid icon]</td><td>View mappings for the subfields of the FHIR resource field.</td></tr></table>

### Lookup Table Mappings

The `FHIR Annotations` tool allows you to view the lookup tables that map codes between SDA and FHIR. For example, you can discover that the code `A` in the `Status` property of a HS.SDA3.Alert object maps to the `in-progress` code of the FHIR `event-status` value set. To explore the lookup tables used to map codes from the source to the target, select `View <transform> Lookup Tables`.

[Image: View Lookup Tables button in the Annotations tool]

To customize a lookup table, see Customizing Lookup Tables.

### Mapping Conventions

This section explains the logic behind the SDA-FHIR mappings.

#### Field-to-Field Mappings

Most mappings are field-to-field: The mapping finds a data value in a source field and assign that value to a target field. For example, the value of a SDA property is assigned to a FHIR field.

#### Conditional Mappings

Some field-to-field mappings are conditional; the value is assigned to the target field only if certain conditions are met. The `FHIR Annotations` tool shows the label `Condition to Set this Field` when it presents this information. The DTL <if> element controls this in the code.

#### Literal Values

Among the defined mappings are mappings of literal values to target fields. One purpose of these mappings is to provide values for required target fields when the source object definition contains no fields that could provide the data required by the target.

Often, mappings of this type are defined conditionally, to be used only when needed.

#### Excluded Fields

SDA fields that contain metadata without clinical significance are not mapped to a FHIR field. For example, the `UpdatedOn` property is not transformed into FHIR.

In addition, SDA fields that are marked as Not Used in the class reference are not transformed into FHIR. For example, the `ExternalId` property of `LabResultItem` is not mapped to a field in the Observation resource.

#### Mapping Single to List

When the source field is single but the target field is a list, the transformation maps the source item to the first entry in a target list. After the transformation, the list contains only one entry. This feature is handled automatically during code generation for transformations. Single to List does not require special attention in the mapping definitions.

#### Mapping List to Single (Values)

When the source field is a list of values, and the target field is limited to a single value, the transformation concatenates the list of values into a single value, separating each value in the list with a semicolon and space.

#### Mapping List to Single (Objects)

For SDA to FHIR: when the incoming SDA is a list of objects, and the target FHIR has only one object, the mapping table contains two mapping entries for the source list field:

*   One mapping maps the source list field to the target single field. The transformation generated from this mapping simply places the first list entry into the target field.
    
*   The other mapping maps the source list field to the target FHIR extension that contains the full list of objects. The FHIR extension URL is the full source field name, including the resource name, but using all-lowercase text separated by hyphens.
    

For FHIR to SDA: when the incoming FHIR has a list of objects, and SDA has one object, the transformation uses the first object and drops all the others.

#### Mapping SDA CodeTableDetail to a FHIR Code

Transformations map an SDA `CodeTableDetail` (or one of its subclasses) to a FHIR coded object such as `Coding` or `CodeableConcept` as follows:

1.  The `Code` value is mapped to the `code` field.
    
2.  The `Description` is mapped to the `display` field.
    
3.  If there is an `OriginalText` field, it is mapped to the `text` field.
    

#### Mapping Coded Values to FHIR using Lookup Tables

The mapping consults a lookup table to find the entry that maps code values from the source schema (SDA or FHIR ) to code values in the target schema (FHIR or FHIR DSTU2) for this mapping.

If the mapping cannot find the lookup table, or cannot find a matching entry in the lookup table and it has a non-empty default value defined, it applies its default value to the code field. Otherwise, the target receives no value from this mapping.

If the mapping is SDA to FHIR, and the source field contains a non-empty value, then by convention there are two mapping entries for this source field. Both entries execute under the same Condition to Set this Field:

*   One entry does the lookup to retrieve the value to assign to the target field.
    
*   The other stores the original source field value in a string-valued FHIR extension.
    

In either case, if there is a `Description` or `OriginalText` along with the `Code` value, it is mapped to FHIR where applicable.

#### Mapping a FHIR Code to SDA CodeTableDetail

When a FHIR primitive code or coded object such as `Coding` or `CodeableConcept` does not use a lookup to transform the code value from FHIR to SDA, it is transformed to SDA `CodeTableDetail` (or one of its subclasses) as follows:

*   `CodeableConcept.text` is transformed to `HS.SDA3.CodeTableTranslated.OriginalText`
    
*   `CodeableConcept.coding.display` (or `Coding.display`) is transformed to `HS.SDA3.CodeTableDetail.Description`
    
*   `CodeableConcept.coding.code` (or `Coding.code`, or simply `code`) is transformed to `HS.SDA3.CodeTableDetail.Code`
    
*   `GetCodeforURI` of `CodeableConcept.coding.system` (or `Coding.system`) is transformed to `HS.SDA3.CodeTableDetail.SDACodingStandard`
    
*   `CodeableConcept.coding.version` (or `Coding.version`) to `HS.SDA3.CodeTableDetail.CodeSystemVersionId`
    

#### Mapping FHIR Coded Values to SDA using Lookup Tables

If you want a mapping to use a code lookup table for FHIR to SDA, the mapping table contains two mapping entries for the source field:

*   One of the two entries consults a lookup table to find the entry that maps a FHIR code value to an SDA Code.
    
*   The other mapping entry in the pair takes over when the lookup table entry is unavailable or does not provide a match. It maps the source FHIR code value (unchanged) into an SDA `CodeTableDetail` object, as described above. That is, if the FHIR code was inside a `Coding` or `CodeableConcept` object, the FHIR code, display, system, version, and text values all are mapped appropriately into SDA `CodeTableDetail` fields.
    

#### Mapping SDACodingStandard

When the transformation encounters the `SDACodingStandard` property of an SDA object, it checks to see if the `SDACodingStandard` value is in the OID registry, and does one of the following:

*   If the `SDACodingStandard` value is an entry in the OID registry that includes a URL, the transformation sets the `system` field of the FHIR Coding resource to the URL.
    
*   If the `SDACodingStandard` value is an entry in the OID registry that does not define a URL, the transformation sets the `system` field of the FHIR Coding resource to the OID.
    
*   If the `SDACodingStandard` value is not an entry in the OID registry, the transformation stores the value in a FHIR extension.
    

#### Mapping String Values to Numeric Values

When the target is FHIR, and a string value is mapped to a numeric value, the string may contain non-numeric text such as units of measurement or instructions. To handle this, there are two mapping entries for the source list field:

*   One of the two entries always assigns the source string value to a FHIR extension that consists of one string-valued field.
    
*   The other mapping entry tests the source string value to see if it is numeric. If so, it maps this numeric value to the target numeric field.
    

#### Multi-Part Literal Values for FHIR Code Objects

For some FHIR target fields that are `Coding` or `CodeableConcept` objects, a set of mappings from literal values forms a multi-part value that is assigned to the field when needed. The full set of fields that such an object can contain are: `code`, `system`, `display`, `text`, `version`, and `userSelected`.

Where this is the case, the DTL annotation element for the code field explains that this code resides within a `Coding` or `CodeableConcept` object that is receiving a multi-part literal value. The FHIR Annotations show that the set of literal value mappings relating to this code all have the same value in the Condition to Set this Field.

#### Mapping to FHIR Extensions

When the target of a transformation is FHIR, one or more SDA properties might not have a corresponding field in the target FHIR schema. In that case, transformations map the SDA data to a FHIR extension. The URL prefix for the extension is `http://intersystems.com/fhir/extn/sda3/lib`. The full URL is the full SDA property name, including the resource name, but using all-lowercase text separated by hyphens.

For example, the FHIR extension for the SDA property `HS.SDA3.Administration:AdministeredAmount` is:

*   Extension name: `administration-administered-amount`
    
*   Full URL for the FHIR extension: `http://www.intersystems.com/fhir/extn/sda3/lib/administration-administered-amount`
    

#### Mapping SDA CustomPairs

The transformations support the legacy `CustomPairs` property in SDA classes of type HS.SDA3.SuperClass.

CustomPairs is a collection of objects of type `HS.SDA3.NVPairs`, each of which has two properties, `Name` and `Value`. When the transformation code encounters this property in customer SDA data, and the target is FHIR, the collection is mapped to a FHIR extension that contains a Parameters resource. This Parameters resource is a collection of paired fields: `name` and `valueString`.

In the example below, the customized SDA Encounter object has an SDA CustomPairs collection with three members, each with the name `PlanOfCareInstructionsText`:

```
{
   "resourceType": "Encounter",
   "contained":
      [
        {
          "resourceType": "Parameters",
          "id": "63",
          "parameter":
            [
              {
                "name": "PlanOfCareInstructionsText",
                "valueString": "Doctor recommends at least 30 minutes of exercise per day"
              },
              {
                "name": "PlanOfCareInstructionsText",
                "valueString": "Use sports heart rate monitor to aid in monitoring effort level"
              },
              {
                "name": "PlanOfCareInstructionsText",
                "valueString": "Read \"South Beach Diet\""
               }
            ]
        }
      ],
   "extension":
      [
        {
          "url": "http://intersystems.com/fhir/extn/sda3/lib/encounter-custom-pairs",
          "valueReference":
            {
              "reference": "#63"
            }
        }
      ],
   "id": "914"
}
```

## Customizing Transformations

Each SDA-FHIR transformation uses a Data Transformation Language (DTL) class to map SDA objects to FHIR resources, and vice versa. You can customize these DTLs using the DTL Editor.

If you want to implement more advanced custom transformation behavior, you can subclass the appropriate transformation API class and override its methods. For more information, see Customizing Transformation APIs. For information about upgrading to the new customization architecture from a legacy FHIR implementation, see Upgrading Pre-2020.2 Transformations

InterSystems products also provide a mechanism for customizing lookup tables used by the transformations.

You customize a transformation within a specific namespace, not for the entire instance, so you can have different customizations in each namespace. If you want multiple namespaces to have the same customized transformations, you must repeat the customization process for each namespace.

*   Implementing custom DTLs
    
*   Customizing transformation API classes
    
*   Customizing lookup tables
    

### Implementing Custom DTLs

The strategy for customizing a DTL that the transformation uses to convert SDA to FHIR (and vice-versa) involves creating a copy of the standard DTL and then modifying it. After you manually specify the package of custom DTL, the transformation will automatically select the custom DTL instead of the standard one.

*   Specifying a package for custom DTLs
    
*   Creating the custom DTL
    
*   Copying custom class to mirror members
    

#### Specifying a Package for Custom DTLs

Before customizing DTLs, you need to specify a single package for all customized DTL classes. InterSystems recommends naming the class package: `HS.Local.FHIR.DTL`. Once you have decided on the package that will be used for all custom DTLs, you need to use the InterSystems Terminal to specify this package. To specify the custom DTL package:

1.  Open the InterSystems Terminal.
    
2.  Change to namespace that contains the SDA-FHIR transformations. For example:
    
    ```objectscript
     set $namespace = "Myfhirnamespace"
    ```
    
3.  To check if a custom DTL package already exists, enter:
    
    ```objectscript
     Write ##class(HS.FHIR.DTL.Util.API.ExecDefinition).GetCustomDTLPackage()
    ```
    
4.  If the custom DTL package does not already exist, enter the following command, replacing `HS.Local.FHIR.DTL` with the name of your custom DTL package:
    
    ```objectscript
     set status = ##class(HS.FHIR.DTL.Util.API.ExecDefinition).SetCustomDTLPackage("HS.Local.FHIR.DTL")
    ```
    
5.  To check that the package was defined successfully, enter:
    
    ```objectscript
     write status
    ```
    
    The response should be: `1`.
    

#### Creating the Custom DTL

You create a custom DTL by saving a copy of the existing standard DTL and then editing it. The package and name of the custom DTL must conform to naming standards so the transformation knows to use the custom DTL rather than the standard one. To create a custom DTL:

1.  Open the Management Portal and navigate to the FHIR namespace.
    
2.  Select `Interoperability` > `List` > `Data Transformations`.
    
3.  Find the name of the transformation that you want to customize. For example, transformations from SDA to FHIR STU3 are prefixed with `HS.FHIR.DTL.SDA3.vSTU3` while transformations from FHIR STU3 to SDA are prefixed with `HS.FHIR.DTL.vSTU3.SDA3` .
    
4.  Double-click the name of the transformation you want to customize to open it in the DTL Editor.
    
5.  Open the InterSystems Terminal.
    
6.  To obtain the required name for the customized DTL class, enter the following in the Terminal:
    
    ```objectscript
     Write ##class(HS.FHIR.DTL.Util.API.ExecDefinition).PreviewDTLCustomClass("standard_class_name")
    ```
    
    Where `standard_class_name` is the full name of the transformation that you are customizing, including packages. It is the name of the transformation that you have open in the DTL Editor. You can view the name on the `Transform` tab, but do not include the `.dtl` extension.
    
7.  Be sure to make note of the response in the Terminal. You need to give your customized DTL class this name.
    
8.  In the DTL Editor, click `Save As` .
    
9.  In the `Package` field, enter the package from the name of the customized DTL class that appeared in the Terminal. For example, if the customized class name in the Terminal was `HS.Local.FHIR.DTL.SDA3.vSTU3.Address.Address`, enter `HS.Local.FHIR.DTL.SDA3.vSTU3.Address` (without the actual class name).
    
10.  In the `Name` field, enter the name of the customized class. For example, if the customized class name in the Terminal was `HS.Local.FHIR.DTL.SDA3.vSTU3.Address.Address`, enter `Address`.
     
11.  Enter a description and click `OK`.
     

#### Copying Custom Class to Mirror Members

If your environment uses mirroring and the package of your customizations resides in a non-mirrored database, you must copy the customized DTL class to the custom package on each mirror member. For example, if you defined the package for customized classes as `HS.Local.FHIR.DTL`, then you must copy the customized DTL class to `HS.Local.FHIR.DTL` on each mirror member because `HS.Local` resides in the HSCUSTOM namespace, which is not mirrored. If your custom package resides in a mirrored database, no further action is required.

### Customizing Transformation API Classes

The transformation API classes contain several methods that can be overridden to implement custom transformation behavior. To override a method, subclass HS.FHIR.DTL.Util.API.Transform.SDA3ToFHIR or HS.FHIR.DTL.Util.API.Transform.FHIRToSDA3 and write your custom method. For example, if you want to select a DTL based on a condition, you can override the `GetDTL()` method. The following is a brief introduction to the overridable transformation methods.

#### SDA to FHIR Overridable Methods

The following methods of the HS.FHIR.DTL.Util.API.Transform.SDA3ToFHIR class can be overridden to implement custom transformation behavior.

##### `GetDTL`

Specifies the DTL class used to transform a given SDA object. You do not need to override this method to use a custom DTL; if you specified a custom DTL package, the `GetDTL()` method finds the custom DTL before using the standard one. However, you can override this method if you want to select a DTL from multiple possibilities based on a condition.

##### `IsDuplicate`

Override this method to change how the transformation checks whether a generated resource that is referenced by another resource in the bundle already exists. For example, you might want to relax what is needed to identify a shared resource like Organization, Practitioner, or Medication as a duplicate. By default, the first 32 kilobytes of a shared resource are added as a hash in a hash table. For each subsequent reference to a shared resource, the transformation determines whether the referenced resource is a duplicate by searching the hash table for a direct match of the JSON.

If the `IsDuplicate()` method determines that a referenced resource already exists, it is not included in the bundle output.

##### `ResourceLookup`

By default, only the bundle created by the transformation is searched for a specified resource when the `ResourceLookup()` method is called. However, you can override this method, for example, if you want the application to search for the specified resource in a repository as well as in the bundle output.

##### `GetReference`

When transforming SDA that has a reference to another streamlet, this method returns the reference to the FHIR resource that is created for the referenced SDA object. For example, when an `EncounterNumber` is passed to this method, it returns a reference to the FHIR Encounter resource that corresponds to the SDA Encounter that was referenced by the specified `EncounterNumber`. Override the method to generate a custom reference to the specified FHIR resource.

##### `GetId`

By default, an individual resource is not assigned an `id` when the transformation produces a bundle. Override the `GetId()` method to assign resources in the bundle an `id`. In this case, the value for the `fullUrl` field of the bundle is `baseURL/resourceType/id` and the resource references in the bundle are `resourceType/id`.

##### `GetBaseURL`

Override the `GetBaseURL()` method to change the URL prefix of each resource. For example, if you are posting FHIR resources to a specific repository, you can provide a URL prefix that identifies the repository.

##### `HandleInvalidResource`

The transformation validates each resource before adding it to the Bundle output. Override the `HandleInvaidResource()` method to customize what happens to a resource that fails validation. By default, an error is thrown and processing stops, which means the Bundle is not returned.

#### FHIR to SDA Overridable Methods

The following methods of the HS.FHIR.DTL.Util.API.Transform.FHIRToSDA3 class can be overridden to implement custom transformation behavior.

##### `GetDTL()`

Specifies the DTL class used to transform a given FHIR resource. You do not need to override this method to use a custom DTL; if you specified a custom DTL package, the `GetDTL()` method finds the custom DTL before using the standard one. However, you can override this method if you want to select a DTL from multiple possibilities based on a condition.

##### `GetResourceFromReference()`

This method controls where the transformation looks for a resource that has been referenced by another resource in the bundle. For example, you could override the method to find the referenced resource in a repository rather than in the same bundle.

##### `GetSendingFacility()`

Override this method to customize how the value of the SDA `SendingFacility` property is set.

By default, the `SendingFacility` property is set as follows: if the Patient’s `managingOrganization` field contains a reference to an Organization, and that Organization is in the Bundle, it is used. Otherwise, the patient identifiers are searched for an MRN with an assigning authority, and that assigning authority is used. If neither of these items is found, the string `FHIR` is used.

##### `GetIdentifier()`

Override this method to customize how certain identifiers are assigned to SDA properties.

For example, this method can be customized to assign values to the `EncounterNumber` field of an Encounter streamlet. In this case it can be useful to access the contents of the resource being converted in order to determine what `EncounterNumber` should be returned. The instance property `%currentReference` contains a FHIR reference object that can be passed into the instance method `GetResourceFromReference()` in order to obtain the resource as a dynamic object. By default, the value of the `EncounterNumber` properties are assigned sequentially, starting at `1`.

Overriding this method can also be useful for assigning the `ExternalID` value for the SDA HealthConcern or Goal. By default, the value of `ExternalID` properties are assigned sequentially, starting at `1`.

##### `HandleMissingResource()`

By default, if a resource that is referenced by another resource within the incoming FHIR bundle is not present in the bundle, the transformation of the bundles continues. To change what happens when there is a missing resource in the bundle, override the `HandleMissingResource()` method.

### Customizing Lookup Tables

The FHIR Annotations tool allows you to explore the lookup tables that are used by transformations to map codes in the source data format to codes in the target format. You can customize these lookup tables by using a InterSystems Terminal utility or by manually modifying a JSON file that contains the lookup tables.

#### Using the Terminal Utility to Customize a Lookup Table

InterSystems provides a Terminal utility that leads you through the process of customizing a lookup table. To run the customization utility:

1.  Open the InterSystems Terminal.
    
2.  To change to the FHIR namespace, enter:
    
    ```objectscript
     set $namespace = "Myfhirnamespace"
    ```
    
    where `Myfhirnamepace` is the FHIR namespace you have created.
    
3.  To start the utility, enter:
    
    ```objectscript
     do ##class(HS.FHIR.DTL.Util.API.LookupTable).EditLookupTable()
    ```
    
4.  Enter the Mapping Source for the lookup table you are customizing. For example, if you are customizing a lookup table that maps values from SDA3 to STU3, enter `SDA3` .
    
5.  Enter the Mapping Target for the lookup table you are customizing. For example, if you are customizing a lookup table that maps values from SDA3 to STU3, enter `STU3`.
    
6.  Enter the number that corresponds to Mapping Source Value Set in the lookup table you want to customize.
    
7.  If only one lookup table with the Mapping Source Value Set exists, the Mapping Target Value Set is selected automatically and you can skip to the next step. If not, enter the number that corresponds to the Mapping Target Value Set you want to customize.
    
8.  Select the code-to-code mapping you want to edit. If you want to add a new code-to-code mapping in the lookup table, enter `+` .
    
9.  If you are editing the target value of a code-to-code mapping, enter the new target value for the mapping.
    
    If you want to edit the source value of the code-to-code mapping, you must enter `-` to delete the entire code-to-code mapping, then re-run the utility to add a new mapping with the correct source and target values.
    

#### Editing Lookup.json to Customize a Lookup Table

Rather than using the Terminal utility, you can customize lookup tables by adding, deleting, or editing key-value pairs in a JSON file that contains all of the lookup tables used by transformations. Before beginning, you must make a custom copy of the supplied `Lookup.json` file and put it into a namespace-specific directory under the custom directory.

##### Creating a Custom Lookup.json File

To create a custom JSON file in a durable location that will be used by transformations when accessing lookup tables:

1.  Create a custom directory for your FHIR namespace in a durable location:
    
    *   In a kit installation:
        
        ```
        <install-dir>\dev\fhir\lookup\custom\<MYFHIRNAMESPACE>
        ```
        
    *   In a container:
        
        ```
        <ISC_DATA_DIRECTORY>\dev\fhir\lookup\custom\<MYFHIRNAMESPACE>
        ```
        
    
    where `<MYFHIRNAMESPACE>` is the name of your FHIR namespace in all capital letters. For example, if the namespace that contains your FHIR production is called `Myfhirnamespace` , create a directory called `MYFHIRNAMESPACE` .
    
2.  Copy `Lookup.json` from the `<install-dir>\dev\fhir\lookup` directory to the new custom namespace directory you created.
    
    You can now begin to edit the lookup tables in the new copy of `Lookup.json` .
    

##### Editing Custom Lookup.json File

To begin customizing a lookup table, you must gather four pieces of information:

*   Mapping Source
    
*   Mapping Target
    
*   Mapping Source Value Set
    
*   Mapping Target Value Set
    

These values can be found in the FHIR Annotations in the Management Portal. To access these values:

1.  Open the Management Portal and navigate to your FHIR namespace.
    
2.  From the Home page, select `Health` > `Schema Documentation` > `FHIR Annotations` .
    
3.  In the first drop-down list, select the type of transformation that contains the lookup table you are customizing. For example, if you are interested in how SDA3 and FHIR STU3 codes map to each other in a lookup table, select `FHIR3–>SDA3`.
    
    Make note of the Mapping Source and Mapping Target. The first interface format in the transformation pair is the Mapping Source. The second interface format is the Mapping Target. For example, if you select `FHIR3—>SDA3` , vSTU3 is the Mapping Source and SDA3 is the Mapping Target.
    
4.  Click the `View <transformation> Lookup Tables` button, where the full name of the button depends on which transformation pair you selected.
    
5.  Using the `View Lookup Tables` dialog, use the drop-down lists to note the Mapping Source Value Set and Mapping Target Value Set. The Mapping Source Value Set is the name in the left-hand drop-down list. The Mapping Target Value Set is the name in the right-hand drop-down list.
    

Now that you have the Mapping Source, Mapping Target, Mapping Source Value Set, and Mapping Target Value Set, you can edit a lookup table by adding, deleting, or editing the appropriate key-value pair in the custom `Lookup.json` file.

The top-level key-value pair in `Lookup.json` corresponds to the Mapping Source to Mapping Target relationship. For example, a lookup table used by SDA3 to FHIR STU3 transformations looks like:

```
"SDA3" : {
    "vSTU3" : {
```

The next level of key-value pairs corresponds to the Mapping Source Value Set to the Mapping Target Value Set. Search for the correct lookup table by finding the corresponding key-value pair. For example:

```
"HS.SDA3.Alert:Status" :
    {"event-status" : {
```

Once you have located the lookup table, you can add, delete, or edit the key-value pairs that correspond to the code-to-code mappings.

```
"A":"in-progress",
"C":"unknown",
"I":"aborted",
"INT":"completed"
```

##### Loading Custom Lookup.json File

Once you have customized `Lookup.json`, you need to load it using the Terminal before it can be used by the SDA-FHIR transformations. To load the JSON file:

1.  Open the Terminal.
    
2.  Change to your FHIR namespace. For example:
    
    ```objectscript
     set $namespace = "Myfhirnamespace"
    ```
    
3.  Run the following command:
    
    ```objectscript
     set status = ##class(HS.FHIR.DTL.Util.API.LookupTable).ImportLookupJSONToGlobal()
    ```
