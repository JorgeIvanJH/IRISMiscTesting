# InterSystems FHIR Components

InterSystems products include the following HL7 FHIR technologies:

## FHIR Server

A FHIR server is an application that receives and processes FHIR requests while leveraging an architecture that is capable of storing and retrieving FHIR resources from an internal repository. In InterSystems products, the out-of-box solution for a FHIR server uses the Resource Repository as its storage.

Depending on your product’s license, you might not be able to install a FHIR server with the Resource Repository. In this case, you should use the FHIR Adapter for Interoperability Productions to receive and process FHIR requests.

When using the FHIR server, requests can be routed through an interoperability production before reaching the server’s internal architecture, but it is not required; FHIR servers that do not use an interoperability production can be significantly faster.

## FHIR Adapter for Interoperability Productions

When your application must receive and process FHIR requests, but does not need to store or retrieve resources from internal storage, your best option is to use the FHIR Adapter rather than a FHIR server. The FHIR Adapter installs the components needed to handle a FHIR request without installing the internal architecture of a FHIR server. The FHIR Adapter always uses an interoperability production to process requests.

## Transformations

InterSystems products can be used to transform health care data captured in a non-FHIR standard such as HL7v2 into FHIR using a set of pre-defined transformations that can be invoked from an interoperability production or directly from an ObjectScript application. Transformations that take FHIR as the input and translate it into another interoperability standard are also provided. At the core of these transformations is the ability to convert FHIR to and from SDA, which is the InterSystems clinical data format.

## FHIR Client

Within InterSystems technology, a FHIR client is an interoperability business host or ObjectScript application that makes requests to a FHIR endpoint, whether it is the endpoint of an external FHIR server or the FHIR server architecture within the same InterSystems product. The FHIR client classes provide straightforward methods for performing FHIR interactions and operations on a FHIR server.

## Amazon HealthLake Adapters

InterSystems products offer inbound and outbound adapters that allow an interoperability production to retrieve, create, delete and update FHIR resources in an Amazon HealthLake data store.

## FHIRPath

FHIRPath is a language that allows you to navigate a FHIR resource to evaluate and extract data from its fields using a straightforward syntax. InterSystems products provide a subset of the FHIRPath functions and operations that you can use to evaluate a resource.

## FHIR SQL Builder

The FHIR SQL Builder, or Builder, allows you to project data stored in a FHIR repository into a relational table that can be queried via InterSystems SQL. After analyzing the contents of a FHIR repository, you can select which resources and fields you would like to project into relational tables.

## Bulk FHIR Coordinator

InterSystems products include a Bulk FHIR Coordinator that mediates the interaction between a client and a FHIR endpoint for HL7 FHIR bulk data requests. You can enter a set of configurations. Each configuration identifies a FHIR endpoint, and defines the authorization type, file location, and other parameters to be used in the bulk FHIR interaction.
