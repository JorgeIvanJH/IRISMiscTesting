# FHIR Server: An Introduction

Many implementations can use an out-of-the-box FHIR server that stores and retrieves resources from the InterSystems database using the Resource Repository. This FHIR server can be customized without using an interoperability production or developing an entirely new back end. The Resource Repository supports a variety HL7 FHIR interactions and operations.

FHIR requests can be routed through an interoperability production before reaching the server’s infrastructure, but this is not a requirement. FHIR servers that do not use an interoperability production can be significantly faster.

Though less frequent, it is possible to build a FHIR server with an entirely custom backend; this implementation leverages the same internal architecture used by the Resource Repository, but you must develop your own FHIR processing logic.

If your InterSystems product is not licensed to install the FHIR server, you can use the FHIR Adapter for Interoperability Productions to receive and process FHIR requests through an interoperability production.

## Product Architecture

FHIR servers using the Resource Repository or a custom backend use the same architecture. Tracing a FHIR request through the FHIR server provides a good overview of the major architectural features of these servers. First, the FHIR request must reach the Service, which ensures that the request conforms to the server's FHIR metadata standards and then routes it to the appropriate component to handle the request. The FHIR request can reach this Service in three ways: from a REST handler, through an interoperability production, or from an ObjectScript FHIR Client. This Service is unrelated to a business service in an interoperability production.

What the Service does with the request depends on the type of request:

*   If the request contains an HTTP method and endpoint that correspond to a FHIR interaction, the Service forwards it to the method of the Interactions class that handles that type of FHIR interaction. For example, requests with a `read` interaction are sent to the `Read()` method of the Interactions class. This Interactions class executes the FHIR interaction, using the InteractionsStrategy class to process the interaction according to the overall purpose of the FHIR server.
    
*   For FHIR operations, the Service forwards the request to a special class designed to perform operations. FHIR servers using the Resource Repository offer out-of-the-box support for certain FHIR operations.
    
*   If the request contains a bundle of type `transaction` or `batch`, the Service forwards the request to a special class that unpacks the bundle to perform the individual HTTP operations.
    

[Image: internal architecture of FHIR server]

### More About the Service

The Service is a singleton class that allows only one instance of itself to be instantiated for an endpoint. This instantiation occurs when the first FHIR request is sent to the Service by the REST Handler or Business Operation; once instantiated, the Service exists until the process ends. For server applications making FHIR requests programmatically, the app must call HS.FHIRServer.Service.EnsureInstance() to retrieve the Service before sending the first request.

In most cases, the Service class (HS.FHIRServer.Service) is ready to uphold the endpoint's FHIR standard and route requests without being subclassed. Custom logic that determines how the FHIR server behaves is written into the Interactions and InteractionsStrategy subclasses, not the Service.

The methods that manage the Service, including creating a new Service for an endpoint and deleting a Service, belong to the subclass of HS.FHIRServer.API.RepoManager.

### More About the InteractionsStrategy

The InteractionsStrategy class dictates the overall strategy for the FHIR server. It is the FHIR server application's backend, creating and implementing the environment in which the FHIR data is processed. The InteractionsStrategy superclass is HS.FHIRServer.API.InteractionsStrategy.

In many cases, the InteractionsStrategy is the "storage strategy" for how the FHIR server stores and retrieves FHIR resources. For example, the Resource Repository is implemented by a subclass of HS.FHIRServer.API.InteractionsStrategy that creates the resource and index tables used to store and retrieve the FHIR data. In applications that are not storing FHIR data, the strategy might set up an environment that communicates with an external FHIR server or any other custom logic that works with the server's FHIR data.

An InteractionsStrategy is associated with a subclass of HS.FHIRServer.API.RepoManager that manages the Services that use the InteractionsStrategy.

### More about the Interactions Class

While the InteractionsStrategy class is the backend of the application, it uses the Interactions class to actually execute the FHIR interactions received by the Service. During this process, the Interactions class often calls methods in the InteractionsStrategy class, especially for structures and logic that are common to the entire FHIR server strategy. Because of their interdependent relationship, the Interactions class and InteractionsStrategy class are subclassed together in a unified approach. The Interactions superclass is HS.FHIRServer.API.Interactions.

The methods in the Interactions class that are called by the Service when processing a FHIR request can also be called directly from a server-side ObjectScript application. For example, a server-side application could call the `Add()` method of the Interactions class rather than sending a `POST` request to the Service. In bypassing the Service, the server application can bypass any restrictions placed on the FHIR server by the Service's metadata. For example, the server application could populate the FHIR server's storage even though the endpoint is read-only for requests going through the Service.

The Interactions class also keeps track of which specialized classes the Service should use to perform FHIR operations, process bundles, and validate FHIR data. The Service obtains the name of these classes from the Interactions object when it needs to take action.

## Resource Repository

The Resource Repository is the default storage strategy for a FHIR server, allowing you to install a fully functioning FHIR server without further development tasks. It automatically stores FHIR data received by the server as dynamic objects that encapsulate the JSON data structures of the FHIR data. To install a FHIR server that uses the Resource Repository, select HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy as the Interactions Strategy Class during installation.

> **Note:**
> 
> Prior to version 2024.1, the Resource Repository architecture was implemented using classes from the `HS.FHIRServer.Storage.Json` package. These legacy architecture classes are still supported in this version; however, they provide a limited set of features compared to the current classes, described in this documentation.
> 
> If you have upgraded an instance with a preexisting Resource Repository to this version from a version prior to 2024.1, see JSON Legacy SQL Strategy for a comparison of supported features and instructions for upgrading your Resource Repository from the legacy classes to the current classes.

*   For a list of the FHIR interactions that are available for a FHIR server that uses the Resource Repository, see Supported Interactions.
    
*   For a list of the FHIR operations that are available for a FHIR server that uses the Resource Repository, see Supported Operations.
    

The Resource Repository consists of the following architectural classes:

<table><tr><th>Architectural Component</th><th>Resource Repository Class</th></tr><tr><td>Interactions</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.FHIRServer.Storage.JsonAdvSQL.Interactions">HS.FHIRServer.Storage.JsonAdvSQL.Interactions</a></td></tr><tr><td>InteractionsStrategy</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy">HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy</a></td></tr><tr><td>RepoManager</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.FHIRServer.Storage.JsonAdvSQL.RepoManager">HS.FHIRServer.Storage.JsonAdvSQL.RepoManager</a></td></tr></table>

You can subclass the Resource Repository to customize the FHIR server. For more information, see Customizing a FHIR Server.
