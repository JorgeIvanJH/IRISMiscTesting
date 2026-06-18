# About FHIR

HL7 FHIR, or Fast Healthcare Interoperability Resources, is a healthcare interoperability standard from HL7 that allows a multitude of systems to exchange healthcare information using agreed upon data models. In FHIR, these data models are simple, straightforward, simultaneously human and computer readable, and, when combined, robust enough to convey complex healthcare information.

The following is a brief introduction to key concepts in FHIR; these concepts are described in detail in the official FHIR Specification.

## FHIR Resources

FHIR is built on the concept of resources, which are discrete units of data represented as JSON or XML. For example, all data about a single patient can be encapsulated as a Patient resource, while information about a single doctor's visit can be captured in an Encounter resource. This Encounter resource would usually contain a reference to the Patient resource of the patient who visited the doctor, avoiding the need to include the patient's data in the Encounter resource itself. Because resources can be stored and retrieved individually using RESTful APIs, FHIR requires less bandwidth and computing resources than other interoperability standards. The ability to express a resource as JSON makes exchanging FHIR data even more lightweight.

The base FHIR specification contains a page for every supported resource. For example, the Patient resource in the latest FHIR version is found at hl7.org/fhir/patient.html. Core information about a resource, for example what data fields belong in the resource and the data types of those fields, can be found in the Resource Content section of the specification page, which includes a Structure tab that explains each resource field. When starting out with FHIR resources, it is useful to compare a specific example of a resource with this structure (sample resources are available on the Examples tab of each resource page in the specification). A portion of the structure for the Patient resource looks like:

[Image: Compare the resource field definition in the FHIR specification with a sample resource in a text editor]

For a description of the symbols and icons used on a resource’s `Structure` tab, see Resource Formats.

FHIR also uses resources to define elements of the standard itself. This metadata, known as conformance resources, defines things like the valid fields of a resource, the search parameters that can be used to retrieve a resource from a FHIR server, and the codes used within a particular healthcare environment.

For a list of resources currently found in the base FHIR specification, see the Resource Index.

## FHIR Adaptations

FHIR is intended to be adapted for specific healthcare environments and implementations, and provides straightforward strategies for extending and constraining the FHIR standard for these purposes. It often said that FHIR follows a 80/20 rule; the base FHIR specification contains 80% of what your healthcare environment needs, while custom constraints and extensions provide the remaining 20%. Often, a FHIR server conforms to a standard, published Implementation Guide that represents a complete implementation of FHIR for a specific ecosystem. For example, the US Core Implementation Guide sets the standard for using FHIR in healthcare environments in the United States. Of course, a healthcare environment can extend the base FHIR specification, US Core, or another Implementation Guide to meet its own unique needs.

At the heart of a FHIR adaptation are FHIR profiles, which extend or constrain a specific resource. For example, the US Core Implementation Guide contains a unique profile for the Patient resource, another profile for the Observation resource, and so on. At a technical level, each profile is defined by a StructureDefinition conformance resource. According to the FHIR specification, the term "profiling" should be reserved for the act of using these StructureDefinitions to configure resources for a particular implementation.

An adaptation of FHIR can contain more than resource profiles. For example, an Implementation Guide can contain codes and search parameters that are unique to a healthcare environment. Similar to profiles, these assets are defined with conformance resources like ValueSet and SearchParameter.

A coherent collection of profiles and other conformance resources is known as a FHIR package. The contents of a package can vary widely; it can contain an entire Implementation Guide or a single custom profile. In InterSystems products, you configure a FHIR server to support a particular healthcare ecosystem by adding a package to a FHIR endpoint.

## RESTful APIs

Though FHIR can be used in messaging and document-based frameworks like traditional healthcare interoperability standards, its innovation is the ability to use RESTful API calls to work with healthcare data. Using HTTP verbs like GET and POST, a FHIR client can store, delete, update, and retrieve FHIR resources as needed. These actions that a FHIR client can take on resources are known as interactions. For more information about RESTful APIs and supported interactions, see RESTful API in the FHIR specification.

FHIR also allows FHIR clients to use operations to perform functions on the FHIR server. Because they invoke functions on the server, these operations are more like RPC calls than RESTful ones. For example, the standard `$validate` operation invokes a function on the server that checks whether a resource conforms to a profile. A healthcare environment can implement custom operations to perform a variety of actions at the request of a FHIR client.

## Searching for FHIR Resources

Search is a very powerful FHIR interaction. Because the healthcare data is stored as individual resources, FHIR clients can use complex queries to retrieve only the data they need without having to parse through unrelated data. These queries are performed with a GET HTTP verb and can leverage search parameters to narrow the results to those resources that meet certain criteria. In its simplest form, a search can retrieve all resources of a certain type without specifying a search parameter. For example, the following RESTful API call would retrieve all Patient resources:

```
GET http://myFHIREndpointURL/Patient
```

You can add search parameters to the API call using the `?` character. For example, a search could use the `name` search parameter to find Patient resources that have a specified value in their name field. The API call to retrieve these Patient resources might be:

```
GET http://myFHIREndpointURL/Patient?name=Smith
```

Multiple search parameters can be chained together using the `&` character. For example, the following API call can further limit the results by adding the gender of the patient:

```
GET http://myFHIREndpointURL/Patient?name=Smith&gender=male
```

The FHIR specification contains many other standard search parameters that can be used to perform powerful and complex queries. For details, see Search in the FHIR specification. You can find the search parameters for a specific resource on the resource’s page in the specification.
