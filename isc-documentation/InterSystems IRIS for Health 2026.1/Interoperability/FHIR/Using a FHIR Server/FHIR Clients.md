# FHIR Clients

InterSystems products come with standard FHIR client classes that your application can use to send an HL7 FHIR request to a FHIR REST endpoint:

*   A request to a FHIR endpoint may be made over HTTP or it may be a request to a local InterSystems FHIR server.
    
*   Your application may be either a standalone ObjectScript application, or it may be an interoperability production.
    

There are three FHIR client classes to choose from, but because they all extend the same HS.FHIRServer.RestClient.Base base class, your application will use the same methods to make requests in each one. The calling pattern is to:

1.  First instantiate the client class.
    
2.  Then set the request and response formats.
    
3.  Finally, call the method that corresponds to the desired HL7 FHIR interaction or HL7 FHIR operation.
    

The three FHIR client classes are:

## HS.FHIRServer.RestClient.HTTPOpens in a new tab

Sends a FHIR request over HTTP to a FHIR endpoint. When instantiating the class, the URL of the FHIR server’s endpoint is identified by an entry in the Service Registry.

## HS.FHIRServer.RestClient.FHIRServiceOpens in a new tab

Sends a FHIR request to the Service of an InterSystems FHIR server in the same namespace. When instantiating the class, the InterSystems FHIR server is identified by the server’s endpoint (for example, `/fhirapp/fhir/r4`)

## HS.FHIRServer.RestClient.InteropOpens in a new tab

Uses an interoperability production to send a FHIR request over HTTP to a FHIR endpoint. It has two variations:

*   Send out a FHIR payload that has been formulated within a custom business host or retrieve FHIR data from within a business host.
    
*   Route a FHIR request from a standalone ObjectScript application through an interoperability production before being sent over HTTP.
    

For details about this interoperability FHIR client, see Interoperability FHIR Client.

*   Invoking Interactions and Operations
    
*   Customizing Requests and Responses
    
*   Requests without FHIR Client Class
    

## Invoking Interactions and Operations

Within the RESTful architecture of the FHIR specification, a FHIR client works with resources on the server through interactions and operations.

An interaction is when the FHIR client executes a CRUD process and the server only executes that process in response. For example, adding a new medication to a Patient resource is an interaction.

An operation is more complex, perhaps involving multiple interactions, or triggering additional processes. An example of an operation: $emancipate code that finds a specified underage Patient in the server, then performs all the actions required to reflect emancipation from parents (such as the ability to make personal medical decisions without parental sign-off) on records associated with that Patient resource.

The FHIR client provides separate methods for each supported type of interaction, but there is a single method to invoke any of the supported operations.

*   For details on invoking interactions, see Calling an Interaction Method below.
    
*   For details on invoking an operation, see the Operation( ) method of HS.FHIRServer.RestClient.Base.
    
*   For details on including custom headers in your FHIR request, see Including Custom Headers.
    

### Calling an Interaction Method

If your FHIR client is writing to the server with interactions like `update`, it must use the `SetRequestFormat()` method to specify the format of the payload being written to the server. Possible formats are `JSON`, `XML`, `Form`, `XPatch`, and `JPatch`. Similarly, your FHIR client can specify the preferred format of the resources returned by the FHIR server using the `SetResponseFormat`. Possible formats are `JSON` and `XML`.

Unless the request and response formats change for individual interactions, your application can set them once and have them applied to all interaction methods. For example, a standalone FHIR client sending requests to a FHIR server over HTTP might set the request and response formats immediately after instantiating the client.

```objectscript
 Set clientObj = ##class(HS.FHIRServer.RestClient.HTTP).CreateInstance("MyFHIR.HTTP.Service")
 Do clientObj.SetRequestFormat("JSON")
 Do clientObj.SetResponseFormat("JSON")
```

Once the FHIR client class has been instantiated and the request and response formats set, the application can call methods that correspond to the FHIR interactions they want to perform on the server. To explore the FHIR interaction methods, including signatures, that are available to a FHIR client, refer to HS.FHIRServer.RestClient.Base in the Class Reference. Note that FHIR interactions that allow conditional actions have two different methods. For example, your application can call `Update()` or `ConditionalUpdate()` depending on whether the `update` interaction is conditional.

The data type of the payload that is passed as an argument is determined by the type of FHIR client that has been instantiated.

*   For clients accessing a FHIR server over HTTP, the payload argument can be a string or stream.
    
*   For clients accessing an InterSystems FHIR server in the local namespace, the payload argument can be a string, stream, or dynamic object.
    

The following is an example of instantiating a FHIR client and performing a `read` interaction on the external FHIR server:

```objectscript
 Set clientObj = ##class(HS.FHIRServer.RestClient.HTTP).CreateInstance("MyFHIR.HTTP.Service")
 Do clientObj.SetResponseFormat("JSON")
 Set clientResponseObj = clientObj.Read("GET", "Patient", "123")
```

### Including Custom Headers

If your FHIR request requires custom header information, for example to pass in an API key, use the SetOtherRequestHeaders() method. This method takes as an input a multidimensional array by reference, where each custom header has a subscript in the array. To populate an array with a custom header, provide a `header name` and a `header value`:

```objectscript
 Set otherHeaders("X-API-Key") = "123"
 Do clientObj.SetOtherRequestHeaders(.otherHeaders)
```

To clear the “other headers” collection for the Rest `clientObj` instance, use the ClearOtherRequestHeaders() API method. This method takes no arguments:

```objectscript
  Do clientObj.ClearOtherRequestHeaders()
```

## Customizing Requests and Responses

Internally, each interaction method calls three overridable methods that can be customized to modify how a request is sent or to manipulate the response received by the request. These three methods, `MakeRequest()`, `InvokeRequest()`, and `MakeClientResponseFromResponse()` are implemented by each type of FHIR client, not in the base class. Refer to the comments in the FHIR client class for more information (HS.FHIRServer.RestClient.HTTP, HS.FHIRServer.RestClient.FHIRService, or HS.FHIRServer.RestClient.Interop).

## Requests without FHIR Client Class

Though using a FHIR client class is recommended when making requests to an internal FHIR server from an ObjectScript application, it is possible to write custom classes that perform CRUD operations on the server without these standard client methods. For example, you can write a custom class to interact with the FHIR server without going through the Service, thereby bypassing restrictions on the interactions that are allowed. You can also make direct calls to the Service with the `DispatchRequest()` method. For more information about these special cases, see ObjectScript Applications.
