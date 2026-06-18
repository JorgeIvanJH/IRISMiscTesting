# FHIR Requests, Responses, and Payloads

> **Note:**
> 
> This topic discusses the requests and responses used by FHIR servers when a production is not in use.
> 
> *   For information about requests and responses when a production is in use, see FHIR Production Requests and Responses.
>     
> *   For information about requests and responses used by the InterSystems FHIR client, see FHIR Clients.
>     

## Non-Production FHIR Server Requests and Responses

For a FHIR server that does not use an interoperability production:

*   The message class that the server architecture uses to pass HL7 FHIR requests is HS.FHIRServer.API.Data.Request.
    
*   The message class that the server architecture uses to pass responses from the server to the FHIR client where the request originated is HS.FHIRServer.API.Data.Response.
    

### Accessing FHIR Payloads

By default, when a FHIR request is received by the REST handler, it stores the FHIR payload in the `Json` property of a Request object (HS.FHIRServer.API.Data.Request), which automatically puts the JSON structure into a dynamic object. FHIR requests that contain XML are converted to JSON before being represented as a dynamic object in the `Json` property. Responses from the FHIR server (HS.FHIRServer.API.Data.Response) also contain a `Json` property for FHIR data.

Working with FHIR data begins by getting access to the `Json` property of the request or response. Once you have the FHIR payload, you can manipulate it as a dynamic object. For examples, see FHIR Data.

## Retrieving FHIR Resources Using an ObjectScript Application

If an ObjectScript application needs to retrieve resources from the Resource Repository, it can build a non-production request object (HS.FHIRServer.API.Data.Request) before dispatching it to the endpoint’s Service. If the application is retrieving data, it is returned as the non-production response object (HS.FHIRServer.API.Data.Response). For more details, see Direct Calls to DispatchRequest.

### Setting the Client-Visible URL

In some cases—notably, when requests are forwarded to a FHIR endpoint through a proxy—the URL at which the FHIR server received a request may differ from the URL which was originally requested by a REST client.

In such cases, the FHIR Server’s rest handler determines the client-visible base URL from the content of a request object’s FORWARDED or X-FORWARDED HTTP headers. This logic is implemented by the GetBaseURL() class method of the HS.FHIRServer.Util.BaseURL class.

If your FHIR server must construct the client-visible URL according to a different logic, simply define a custom `GetBaseURL()` in the HS.Local.FHIRServer.Util.BaseURL class. A method defined in this class will override the original.
