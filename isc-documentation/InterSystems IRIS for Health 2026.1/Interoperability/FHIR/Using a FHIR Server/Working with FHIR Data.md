# Working with FHIR Data

Within the FHIR server architecture, HL7 FHIR data is represented in dynamic objects, so working with the data is a combination of knowing how to manipulate dynamic objects and how FHIR resources are represented in JSON. Consult the FHIR specification for details about JSON representations of FHIR resources.

If a FHIR payload is in JSON, for example in an Interoperability request or response, you can convert it to a dynamic object for manipulation using the %FromJSON method.

## FHIR Data and Dynamic Objects

Since FHIR data is often represented as dynamic objects within InterSystems products, knowing how to work with dynamic objects is essential. The following code fragments provide an introduction to manipulating with dynamic objects that contain FHIR data. As you’ll see, you need to be familiar enough with the FHIR specification to know the structure of fields in the JSON representation of a FHIR resource. For complete details on handling dynamic objects, see Using JSON.

These code examples assume you have a variable `patient` that is a dynamic object containing a FHIR Patient resource.

### Searching for a Value

The following code searches through identifiers of the Patient resource looking for a particular system using two different approaches. In order to write this code, you would need to be familiar enough with the FHIR specification to know that the JSON structure of a Patient resource contains an `identifier` that has a `system` name/value pair.

```objectscript
 // Put JSON representation of Patient resource into a dynamic object
 set patient = ##class(%DynamicObject).%FromJSONFile("c:\localdata\myPatient.json")

 //Searching for a identifier with a specific system
 set mySystem = "urn:oid:1.2.36.146.595.217.0.1"

 //Approach 1: Use an Iterator
 if $isobject(patient.identifier)
 {
   set identifierIterator = patient.identifier.%GetIterator()
   while identifierIterator.%GetNext(, .identifier)
   {
     if identifier.system = mySystem
     {
       write "Found identifier: " _ identifier.value,!
     }
   }
 }

 //Approach 2: Use a 'for' loop
 if $isobject(patient.identifier)
 {
   for i=0:1:patient.identifier.%Size()-1
   {
     set identifier = patient.identifier.%Get(i)
     if identifier.system = mySystem
     {
       write "Found identifier: " _ identifier.value,!
     }
   }
 }
```

### Extracting a Value

The following code fragment extracts the family name from the Patient resource.

```objectscript
 if $isobject(patient.name) && (patient.name.%Size() > 0)
 {
   set myFamilyname = patient.name.%Get(0).family
 }
```

### Modifying a Value

The following code fragment sets the Patient resource’s `active` field, which is a boolean, to `0`.

```objectscript
 do patient.%Set("active", 0, "boolean")
```

### Adding a New JSON Object

When you want to add a new JSON object to an existing dynamic object, you can choose whether to use an ObjectScript syntax or a JSON syntax. For example, the following code adds a new `identifier` to the patient, using two different approaches that have the same result.

```objectscript
 set mySystem = "urn:oid:1.2.36.146.595.217.0.1"
 set myValue = "ABCDE"

 // Approach 1: Use JSON syntax
 if '$isobject(patient.identifier) {
   set patient.identifier = ##class(%DynamicArray).%New()
  }

 do patient.identifier.%Push({
   "type": {
     "coding": [
       {
         "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
         "code": "MR"
       }
     ]
   },
   "system": (mySystem),
   "value": (myValue)
 })

 //Approach 2: Use ObjectScript syntax
 set identifier = ##class(%DynamicObject).%New()

 set typeCode = ##class(%DynamicObject).%New()
 set typeCode.system = "http://terminology.hl7.org/CodeSystem/v2-0203"
 set typeCode.code = "MR"

 set identifier.type = ##class(%DynamicObject).%New()
 set identifier.type.coding = ##class(%DynamicArray).%New()
 do identifier.type.coding.%Push(typeCode)
 set identifier.system = mySystem
 set identifier.value = myValue

 if '$isobject(patient.identifier)
  {
   set patient.identifier = ##class(%DynamicArray).%New()
  }
  do patient.identifier.%Push(identifier)
```

## FHIR Object Classes

The FHIR standard defines a huge number of resource types, with numerous elements, structures, and data constraints. Remembering the exact syntactic details for all of the resource types is a burden, and something as simple as misspelling a field name can result in errors and failure. FHIR payloads typically reside in %DynamicAbstractObject (DAO) structures, which are invisible to the auto-completion tooling within the InterSystems IRIS for Health ecosystem.

InterSystems IRIS for Health provides a set of FHIR R4 object classes, included in `HSLIB`, that enable your IDE to provide auto-completion prompts for FHIR resources, shifting the cognitive burden from recall to reference. You don’t have to remember how to spell an element name; the IDE reminds you.

[Image: Illustration of IDE autocomplete for FHIR object model.]

### Features of the FHIR Object Classes

Each R4 resource has a corresponding ObjectScript class in the `HS.FHIRModel.R4` package. For example, the HS.FHIRModel.R4.AllergyIntolerance class corresponds to the AllergyIntolerance resource. These classes streamline development by providing a shared, predictable framework of data structures and methods for resources and constituent elements, as defined by the base specification.

Within the `FHIRModel` framework:

*   Elements unique to a resource are modeled by a class within a subpackage named `HS.FHIRModel.R4.[ResourceName]X`, For example, HS.FHIRModel.R4.AllergyIntoleranceX.Reaction models the data structure of an AllergyIntolerance resource’s `reaction` element.
    
*   A collection of elements is modeled by a class named `SeqOf[ElementClassName]`. For a collection that is unique to a resource, this class is implemented within the `[ResourceName]X` subpackage. For example, the HS.FHIRModel.R4.AllergyIntoleranceX.SeqOfAllergyIntoleranceXReaction models the collection of `reaction` elements for an AllergyIntolerance resource.
    
    [Image: Diagram illustrating SeqOf[ElementClassName] structure.]
*   A resource class includes an `Include[ElementName]()` method for each complex element or collection of elements within it. This method adds the appropriate nested data structure for the element or collection to the resource object.
    
*   A collection class includes a `MakeEntry()` method, which adds a new element to the collection object. The following example illustrates both `MakeEntry()` and `Include[ElementName]()`:
    
    ```objectscript
    Set claim = ##class(HS.FHIRModel.R4.Claim).%New()
    Do claim.IncludeInsurance()
    Set ins = claim.insurance.MakeEntry()
    Do ins.includeCoverage()
    Set ins.coverage.display = "Supra Health"
    (...)
    ```
    
*   All classes implement a common set of methods for fetching, navigating, and mutating their contents. These methods are inherited from the `%Library.AbstractSet` class. 
    
*   A dynamic abstract object that represents the JSON for a FHIR resource can be converted to an instance of its corresponding `FHIRModel` class using the `fromDao()` class method. Conversely, an instance of a `FHIRModel` class that represents a FHIR resource can be converted to a dynamic abstract object using the `toDao()` method. It can then be converted to a valid JSON payload using the dynamic object's `%ToJSON()` method. Alternately, you can use the FHIRModel class’s `toString()` method to directly generate the string-formatted JSON payload.
    
*   You can extend the FHIR object classes as needed.
    

### Methods for Use with FHIR Objects

This list includes the methods you will most likely need when converting between FHIR resources represented as Dynamic Abstract Object (DAO) structures and FHIR objects, and when working with FHIR objects. For more detail about these methods, or for additional methods, see the `%Library.AbstractSet` class or the relevant `HS.FHIRModel.R4` subclasses in the class reference.

A likely workflow is something like this:

1.  receive a FHIR resource as a JSON payload.
    
2.  Convert the JSON payload to a %DynamicObject (a subclass of %DynamicAbstractObject), as described in Working with FHIR Data.
    
3.  Convert the %DynamicObject to an object of the analogous `FHIRModel` class using `fromDao()`.
    
4.  Work with the FHIR object as needed.
    
5.  Convert the FHIR object back into JSON format using `toString()`.
    

#### Conversion Methods for FHIR Objects

##### fromDao(dao As %DynamicAbstractObject) As <HS.FHIRModel.R4 subclass>

Converts from DAO to the specified FHIR object. For example, to convert from a JSON payload `dao` to a FHIR object `cls`:

```
Set rType = dao.resourceType
Set cls = $CLASSMETHOD("I4H.FhirR4."_rType,"fromDao",dao)
```

##### toDao() As %DynamicAbstractObject

Converts from FHIR object to DAO. For example, to convert the FHIR object `cls` to a DAO:

```
Set newDao = cls.toDao()
```

##### toString()

Converts from FHIR object directly to string-formatted JSON payload. For example, to convert the FHIR object `cls` directly to a JSON payload, a string:

```
Set payload = cls.toString()
```

#### Fetch Methods for FHIR Objects

For detailed examples of these fetch methods, see Iteration in the FHIR Object Model.

##### get(key As %DataType) as %Any

Get the element identified by the given key, which may be either a label for key-value collections or a numeric position in a zero-based sequence.

##### iterator() as %Iterator

Return an interator over the members of this set. The object returned will have the following methods:

*   `hasNext()` — returns true (1) if there is more data waiting to be processed.
    
*   `next()` — returns an actual tuple with properties named key and value, drawn from the data in the queue.
    

#### Set and Clear Operations for FHIR Objects

To invoke the set and clear methods, use `Do [object].[method]` syntax. For example, for the `add()` method:

```
Do item.IncludeEncounter()
Set ref = item.encounter.MakeEntry()
Set ref.reference = "urn:uuid:d8c2b161-7e3e-4e7f-9adc-ae464a9608bc"
Do item.encounter.add(ref)
```

##### add(value As %Any) as %AbstractSet

Sequences only. Append the new member `value` to the sequence.

##### addAll(values As %AbstractSet) as %AbstractSet

Sequences only. Append all members of the sequence `values` to the current sequence.

##### clear()

Remove all elements from the current set.

##### put(key As %DataType, value As %Any) as %AbstractSet

Labeled sets only. Put `value` into the set and associated it with the label `key`. If an element is already associated with the label `key`, replace it with the new `value`.

##### putAll(keys As %AbstractSet, values As %AbstractSet) as %AbstractSet)

Labeled sets only. Put all `{keys[n], values[n]}` elements into the set for all `n` in `values`.

##### remove(key As %DataType) as %Any

Remove the member identified by `key` from the set.

##### replace(key As %DataType, value As %Any) as %AbstractSet

Labeled sets only. Replace the value of the element identified by `key` with the new `value` provided.

#### Introspection Operations for FHIR Objects

##### apply(expression As %Any) as %AbstractSet

Return an array of members matching the provided SQL/JSON Path Language (JPL) expression. For example, to find the email address or addresses associated with a particular doctor resource:

```
Set key = "system"
Set value = "email"
Set query = "$[*]?(@."_key_"=='"_value_"')"
Set email = doctor.telecom.apply(query)
```

##### contains(key As %DataType) as %Boolean

Returns `true` (1) if `key` is currently a non-null member of the set or sequence; otherwise returns `false` (0). If the set is labeled, `key` should be a string; if dealing with a sequence, `key` should be a numeric value greater than or equal to zero.

##### containsAll(array As %DynamicArray) as %Boolean

Returns `true` (1) if the set contains all keys listed in `array`.

##### size() as %Integer

Returns the number of non-null members in this set.

### Practical Hints for the FHIR Object Model

The following topics offer suggestions and examples of ways to make the most effective use of the FHIR object model.

#### Iteration in the FHIR Object Model

The following coding pattern may be applied anywhere in the FHIR object model, whether the underlying data resides in dynamic or static objects:

1.  Use the `iterator()` method to request an iterator from a container class.
    
2.  Use the `hasNext()` method to loop as long as there is new data to visit. Within the loop:
    
    1.  Use the `next()` method to fetch the next key/value or index/value pair.
        
    2.  Use `.key` and `.value` to process the data as needed.
        

The following example starts with `list`, a collection of FHIR resource records in sequence, such as you might find in the entry collection of a Bundle resource. It iterates over the collection, inspecting the `resourceType` field of each entry, and populates `summary`, a dynamic object with a count of how many of each type of resource was discovered:

```
Set summary = {}
Set itr = list.iterator()
While (itr.hasNext()) {
     Set rsc = itr.next().value
     Set rscName = rsc.resourceType
     Set count = summary.%Get(rscName,0)+1
     Do summary.%Set(rscName,count)
}
```

We can follow the same pattern to output the results, even though we have explicitly told the system that the summary object was a DAO. In this case, we see the keys as well as the values, rather than simply visiting each node in order:

```
Write !,"BUNDLE SUMMARY:",!
Write $J("RESOURCE TYPE",35)_"   COUNT",!
Set itr = summary.iterator()
While (itr.hasNext()) {
     Set node = itr.next()
     Write $J(node.key,35)_"   "_node.value,!
}
```

#### Focusing the IDE’s FHIR Object Model Autocompletion Suggestions

If you provide a few hints to the IDE, it can offer more meaningful suggestions regarding class, method, and property names when offering auto-completion options.

##### #dim Directives

One of the simplest ways to empower the IDE to provide useful hints is to make use of the `#dim` directive. For example:

```
#dim info As HS.HC.FHIRModel.R4.ClaimX.SupportingInfo
```

This example informs the IDE that the variable will refer to an instance of a SupportingInfo data structure within a Claim resource, significantly narrowing down the set of likely auto-completion options.

##### %New() Directives

A `%New()` directive will both allocate a new top-level resource and inform the IDE of the base type to be associated with the ORef. For example:

```
Set claim = ##class(HS.HC.FHIRModel.R4.Claim).%New()
```

Based on this directive, the IDE can offer suggestions for method and property names for any token prefixed by ‘claim.’ based on the class definition for `Claim.cls`.

##### ClassMethod Declarations

FHIR object classes are simply type definitions for ORefs, and they can be used when defining parameters to any method, providing crucial hints to the IDE to offer meaningful auto-completion suggestions. For example:

```
ClassMethod ExtractData(bundle As HS.HC.FHIRModel.R4.Bundle)
```

This example tells the system to treat the incoming ORef as an instance of a Bundle resource, while also enabling the IDE to offer suggestions regarding the proper structure and functionality of a Bundle class whenever ‘bundle.’ is referenced.

## Data Load Utility

> **Note:**
> 
> You can access the data load utility directly, as described in this topic. Alternatively, you can access the data load utility via the management portal. To do so:
> 
> 1.  Navigate to `Home > Health`, click `FHIR` in the banner
>     
> 2.  On the card for the desired FHIR server, open the menu and choose `Load Resources`.
>     

The Data Load utility sends resources and bundles that are stored in a local system directory directly to the FHIR server with or without going over HTTP. The local FHIR data fed into the Data Load utility can be individual resources, bundles, or both. The data can be provided in any combination of JSON, NDJSON, and XML files with valid file extensions (`.json`, `.ndjson`, `.xml`). A common use of this utility is feeding large amounts of synthetic data from open source patient generators into the FHIR server.

If getting data to the FHIR server as fast as possible is the objective, it is better to send it directly to the server without using HTTP. In this case, pass the `FHIRServer` argument to the Data Load utility along with the server’s endpoint. For example, suppose the server’s endpoint is `/fhirapp/fhir/r4` and the directory that contains FHIR bundles is `c:\localdata`. To run the Data Load utility, enter

```objectscript
 Set status = ##class(HS.FHIRServer.Tools.DataLoader).SubmitResourceFiles(
                      "c:\localdata",
                      "FHIRServer",
                      "/fhirapp/fhir/r4")
```

The utility should print `Completed Successfully` when it is done processing the files. If it does not, you can print any errors by entering `Do $SYSTEM.Status.DisplayError(status)`.

Alternatively, you can send all the bulk data over HTTP by passing `HTTP` along with the name of a Service Registry HTTP service. For more information about creating a HTTP service, see Managing the Service Registry. For example, you could run:

```objectscript
 Set status = ##class(HS.FHIRServer.Tools.DataLoader).SubmitResourceFiles(
                      "c:\localdata",
                      "HTTP",
                      "MyUniqueServiceName")
```

The Data Load utility’s `SubmitResourceFiles()` utility takes optional arguments which control whether it displays progress, logs statistics, limits the number of files in the directory that it will process, or applies a translate table. In addition, you have the option to specify the number of workers to process the files as a multi-threaded operation. For details on these arguments, see HS.FHIRServer.Tools.DataLoader.SubmitResourceFiles().

The utility also provides an API for loading FHIR data asynchronously. Using the methods in this API, you can initiate a new Data Load operation using Job(). The Job() method returns a job ID for this operation by reference, which you can then use to check its status (using Status()), cancel it (using Cancel()), and clean up associated globals after it is complete (using CleanUp()).

### Loading Bundles Using the Management Portal

> **Note:**
> 
> This option is available only for non-production FHIR servers.

You can also load custom bundles using the convenient `Load Bundles` menu option in the Management Portal, as follows:

1.  In the Management Portal, navigate to `Home` > `Health` > `[MyFHIRNamespace]` > `FHIR Server Management`.
    
2.  In the tile for the relevant FHIR server, open the menu and choose `Load Bundles`.
    
3.  The resulting dialog allows you to load `Custom FHIR bundles`, as follows:
    
    #### Custom FHIR bundles
    
    Allows a client to upload files to the server, then directly submits the FHIR resources to the FHIR server without going over HTTP.
    
    1.  Choose the radio button for `Custom FHIR bundles` and click `Next`.
        
    2.  Click `Select custom bundles` and browse to the desired bundles.
        
    3.  Click `Load`.
        
    

For more details about data loading, or for instructions about using the Data Load Utility to load bundles and resources, see Data Load Utility.
