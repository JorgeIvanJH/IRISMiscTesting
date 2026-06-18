# Interoperability Productions for FHIR

InterSystems healthcare products provide built-in business hosts that you can use to create an interoperability production that accepts and/or sends out HL7 FHIR requests. Business processes that transform SDA to FHIR and FHIR to SDA are also available.

To explore some of the FHIR implementations that are possible using an interoperability production, see Use Cases.

> **Note:**
> 
> The InterSystems FHIR server does not require an interoperability production; by default, FHIR requests received by an endpoint’s REST handler are sent directly to the FHIR server’s Service. FHIR servers that do not use an interoperability production can be significantly faster.

## Accepting FHIR Requests

FHIR implementations can accept FHIR requests into an interoperability production is two ways:

*   For FHIR servers (implementations that leverage the internal architecture and storage of an InterSystems product), the FHIR request can be sent through HS.FHIRServer.Interop.Service on its way to the repository. For details, see Accepting FHIR Server Requests.
    
*   For implementations that do not use a FHIR server, you can use the FHIR Adapter for Interoperability Productions (FHIR Adapter) to accept FHIR requests into an interoperability production.
    

### Security for Incoming Requests

A FHIR request can enter an interoperability production using a FHIR Adapter or a FHIR Server that uses a production. Security is handled differently depending on which feature you are using to receive the request. If your production is using the FHIR interoperability, see Adapter Security. If your production is using a FHIR server, see Server Security

### Accepting FHIR Server Requests

The built-in business service HS.FHIRServer.Interop.Service is designed to receive FHIR requests that have been sent to a FHIR server endpoint. Once configured, the endpoint’s REST handler routes the request to HS.FHIRServer.Interop.Service rather than the FHIR server’s Service.

Setting up an endpoint to route FHIR server requests through an interoperability production is a two-step process:

1.  Create an interoperability production and add the HS.FHIRServer.Interop.Service business service.
    
2.  Configure an endpoint’s `Service Config Name` field so it specifies the name of the business service that has been added to the interoperability production.
    

These steps can be taken in any order as long as, when the setup is complete, the name of the business service in the endpoint’s configuration matches the name in the interoperability production.

> **Note:**
> 
> This two-step process assumes you are using a FHIR server; if your implementation does not leverage the internal architecture and repository of a FHIR server, use the FHIR Adapter to accept FHIR requests.

#### Creating the Interoperability Production

When the Foundation namespace for the FHIR server endpoint is created, the installation process also creates an interoperability production that should be used as the FHIR production. You need to modify the production to add the required business service that the endpoint uses to route requests through the production.

Interoperability productions that receive FHIR requests from the REST handler must include the HS.FHIRServer.Interop.Service business service. You can give the business service a custom name, but make sure that name matches the one specified for the endpoint’s `Service Config Name` option. For details, see Adding Business Hosts.

#### Configuring the Endpoint

After installing a FHIR server endpoint, the endpoint can be configured to use an interoperability production at any time, including before the production has been created. Specifying the name of the business service while configuring the endpoint does not automatically create the business service in your production.

To configure an existing endpoint so FHIR requests are routed through a production:

1.  Navigate to `Health` > `MyNamespace` > `FHIR Server Management`.
    
2.  In the tile for the desired endpoint, choose `Edit` from the menu.
    
3.  In the `Advanced Configuration` section, from the `Service Config Name` dropdown, choose the name of the business service of the production through which FHIR requests will be routed. For example, if the business service does not have a custom name, specify `HS.FHIRServer.Interop.Service`
    
4.  Click `Save`.
    

## Sending FHIR Requests

Within an interoperability production, business operations are responsible for making sure a FHIR request is sent to a FHIR endpoint. This request can originate from a variety of sources, for example, from an external FHIR client accessing an InterSystems endpoint or from a business process that transforms HL7 messages into FHIR requests. Regardless of its origin, there are two business operations available to send requests:

<table><tr><th>Business Operation Class</th><th>Description</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSLIB&amp;CLASSNAME=HS.FHIRServer.Interop.Operation">HS.FHIRServer.Interop.Operation</a></td><td>Sends a FHIR request to the internal <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXFHIROVW_server_intro#HXFHIROVW_server_arch_service">Service</a> of an InterSystems FHIR server in the local namespace. Except in rare cases where a custom architecture has been implemented, Health Connect users cannot use this business operation unless they have a license to use the <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXFHIROVW_server_intro#HXFHIROVW_storage_json">Resource Repository</a>.<p>This business operation identifies the correct InterSystems FHIR server based on the URL of its endpoint, which is included in the <code>SessionApplication</code> property of the request message. If the message originated from a request sent to the FHIR server’s endpoint through the REST Handler, the endpoint’s URL is already part of the message. If the message was sent from the business process that transforms SDA to FHIR (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process">HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process</a>), the server is identified by the <code>FHIREndpoint</code> setting of the business process.</p></td></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSLIB&amp;CLASSNAME=HS.FHIRServer.Interop.HTTPOperation">HS.FHIRServer.Interop.HTTPOperation</a></td><td>Sends a FHIR request to an internal or external FHIR endpoint over HTTP.<p>If you are using a built-in business host to send the request to this business operation, use that business host’s <code>TargetConfigName</code> setting.</p><p>If you wish to obtain an OAuth token without additional coding, set the following fields:</p><ul><li><p>On the <code>Basic Settings</code> tab: <code>HTTP Server</code>, <code>HTTP Port</code>, <code>URL</code>,<code> Credentials</code></p></li><li><p>On the <code>Connection Settings</code> tab: <code>SSL Configuration</code></p></li><li><p>All settings on the <code>OAuth2</code> tab and the <code>OAuth2 Grant Specific</code> tab.</p></li></ul><blockquote><strong>Note:</strong><p>The <code>ServiceName</code> setting, which refers to an entry in the <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXREG_ch_service_registry">Service Registry</a>, specifies the default HTTP address of the FHIR endpoint.</p></blockquote><p>While this setting is supported, it is better to use the configuration fields listed above.</p></td></tr></table>

If a built-in business host (such as HS.FHIRServer.Interop.Service) sends a request message (HS.FHIRServer.Interop.Request) to the HS.FHIRServer.Interop.HTTPOperation business operation, the request is sent over HTTP without custom code. However, if a FHIR payload is formulated within a custom business host that needs to put the payload into a FHIR request, you should instantiate an interoperability FHIR client to send the message. Similarly, if your custom business host needs to retrieve FHIR data from an endpoint, your production should use the FHIR client.

## Interoperability FHIR Client

InterSystems technology provides a FHIR client object that simplifies the process of formulating a FHIR request from within a custom business host and sending it to a FHIR endpoint over HTTP. The business operation, HS.FHIRServer.Interop.HTTPOperation, that is used by the FHIR client to send the request over HTTP must be added to the interoperability production. Once the production is configured, your custom business host can use the FHIR client by instantiating HS.FHIRServer.RestClient.Interop, then calling the methods that correspond to FHIR interactions and operations.

Not all productions that send out FHIR requests over HTTP need to instantiate the interoperability FHIR client. For example, if SDA is being transformed into FHIR using HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process, the FHIR forwarded from this business process to HS.FHIRServer.Interop.HTTPOperation is sent out via HTTP without the FHIR client. However, when a FHIR payload is formulated by a custom business host within a production, the recommended method of sending it to a FHIR endpoint over HTTP is to instantiate the FHIR client.

When instantiating the FHIR client within the context of a custom business host, the call to the CreateInstance( ) method must contain the following parameters:

*   `pServiceName` — Name of an entry in the Service Registry that points to a FHIR endpoint. This value overrides the `ServiceName` setting of the HS.FHIRServer.Interop.HTTPOperation business operation.
    
*   `pTargetConfigName` — Name of the HS.FHIRServer.Interop.HTTPOperation business operation.
    
*   `pHostObj` — Object instance of the business host that is instantiating the FHIR client. You can use `$this` to specify the current business host object that is instantiating the FHIR client.
    

For example, to instantiate a FHIR client within a business host with only the required arguments, enter:

```objectscript
 Set fhirClient = ##class(HS.FHIRServer.RestClient.Interop).CreateInstance(
                          "MyFHIR.HTTP.Service",
                          , , , , ,
                          "HS.FHIRServer.Interop.HTTPOperation",
                          $this)
```

The CreateInstance( ) method also accepts optional arguments that specify the value of the FHIR `prefer` header and send an OAuth token with the request.

Once the FHIR client has been instantiated, you can use it to send requests and perform operations. For details on using the FHIR client’s methods to perform these actions, see Interactions and Operations.

> **Note:**
> 
> The interoperability FHIR client class (HS.FHIRServer.RestClient.Interop) can also be used by a standalone ObjectScript application that needs to send a FHIR request through an interoperability production. In this case, the HS.HC.Util.BusinessService business service must be added to the production along with HS.FHIRServer.Interop.HTTPOperation. Instantiating the client is similar, but for standalone applications, the call to `CreateInstance()` should not include an argument for the `pHostObj` parameter.

## Transformations

You can add built-in business processes to your production to invoke SDA-FHIR transformations. For example, a production could consume HL7 messages, use a business process to convert the HL7 to SDA, and then use the built-in SDA-FHIR business process to convert the SDA to FHIR. The production running these transformations must be in a Foundation namespace.

For more information about SDA-FHIR transformations using the built-in business processes, see Transformation Business Processes.

## Use Cases

The following use cases provide examples of how to use the built-in interoperability components to work with FHIR resources.

*   Proxy Server
    
*   Transforming HL7 into FHIR
    
*   Production-Based InterSystems FHIR Server
    

### Proxy Server

InterSystems healthcare products can be used as a proxy server that accepts FHIR requests from an external FHIR client and forwards them to an external FHIR endpoint, then routes responses from the FHIR endpoint back to the external client. In this scenario, the FHIR client might be unaware that the InterSystems product is not the server that is accepting and producing FHIR, and the request or response can be manipulated within the production as needed.

You could implement a simple proxy server by:

*   Installing the FHIR Adapter.
    
*   Adding HS.FHIRServer.Interop.HTTPOperation to the production and editing the `ServiceName` setting to specify the external FHIR endpoint.
    
*   Editing the `TargetConfigName` of `InteropService` to point to HS.FHIRServer.Interop.HTTPOperation.
    

Of course, there are variations on the proxy server use case. For example, you could also add multiple HS.FHIRServer.Interop.HTTPOperation business operations and use a business process to determine which external FHIR endpoint should be the target of the proxy server.

If you wanted to store FHIR data in an internal InterSystems repository along with sending it out to an external FHIR endpoint, you would need to start with a FHIR Server rather than the FHIR Adapter. In this case, you could send requests to external endpoints using HS.FHIRServer.Interop.HTTPOperation, but also use HS.FHIRServer.Interop.Operation to store the data internally.

### Transforming HL7 into FHIR

InterSystems healthcare products simplify the process of extracting clinical data from incoming HL7 messages and transforming that data into FHIR resources. Once transformed into FHIR, the clinical data can be forwarded to external FHIR endpoints or stored in an internal FHIR repository that can be queried by FHIR clients. A basic interoperability production that transforms HL7 messages into FHIR resources would include:

*   Adding a built-in business service that accepts HL7 messages into the production, for example, EnsLib.HL7.Service.HTTPService.
    
*   Using a business host to transform the HL7 into SDA (the InterSystems intermediary data format). The following code added to a business process is enough to transform the HL7 into SDA:
    
    ```
     do ##class(HS.Gateway.HL7.HL7ToSDA3).GetSDA(request,.con)
     set streamContainer = ##class(ENS.StreamContainer).%New()
     set streamContainer.Stream = con
     set sc = ..SendRequestSync("SDAToFHIRProcess",streamContainer,.pResponse)
    ```
    
    For more information about this transformation method, see Data Transformations in InterSystems Healthcare Products.
    
*   Adding the HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process business process to the production; this business process transforms SDA into FHIR.
    
*   Modifying the `TargetConfigName` setting of the business host that contains the HL7–to-SDA transformation method to specify the name of HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process.
    

Once the HL7 data has been transformed into FHIR, it can be sent to an external FHIR endpoint or, in the case of FHIR server, stored in an internal Resource Repository. You control where the FHIR data is forwarded by adding a business operation that performs a specific function. For details about these business operations, see Sending FHIR Requests. If you are using the business operation that forwards requests to the internal storage of the FHIR server, use the `FHIREndpoint` setting of HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process to specify the InterSystems FHIR server’s endpoint.

For a hands-on example of integrating HL7 message with a FHIR server, see FHIR R4 Integration QuickStart.

### Production-Based InterSystems Server

By default, requests to an InterSystems FHIR server do not go through an interoperability production, however you may want to use a production in some cases. For example, you may want to use a production during development to leverage message tracing and other advantages of productions, then make a small modification to send requests directly to the server’s Service when it goes live. In an alternate use case, you might want to manipulate the FHIR requests using a business process before they reach the InterSystems FHIR server.

In its simplest form, a production-based FHIR server consists of configuring the production as described in Accepting FHIR Server Requests, then adding HS.FHIRServer.Interop.Operation as described in Sending FHIR Requests. Once both business hosts are added to the production, modify the `TargetConfigName` setting of HS.FHIRServer.Interop.Service to specify the name of the HS.FHIRServer.Interop.Operation business operation.

If your aim is to use a production during development, then switch to a FHIR server that sends a request directly to the Service, simply reconfigure the Server’s endpoint by removing the value in the `Service Config Name` field when the server goes live.

## FHIR Production Requests, Responses, and Payloads

> **Note:**
> 
> This topic discusses the requests and responses used by FHIR servers when a production is in use.
> 
> *   For information about requests and responses when a production is not in use, see FHIR Requests, Responses, and Payloads.
>     

For a FHIR server, FHIR Adapter, or FHIR client that leverages an interoperability production:

*   The message class used to pass FHIR requests through the production is HS.FHIRServer.Interop.Request.
    

*   The message class used to pass a response through the production HS.FHIRServer.Interop.Response.
    
    > **Note:**
    > 
    > If you construct a HS.FHIRServer.Interop.Response object, you must explicitly set the `ContentType` property in order to create the HTTP response Content-Type header. Setting the `ResponseFormatCode` in the HS.FHIRServer.API.Data.Response is not sufficient.
    

These classes include a property `QuickStreamId` that points to the FHIR payload.

### Accessing FHIR Payloads in a Production

When a FHIR implementation is using an interoperability production, you access the FHIR payload of the message object differently than implementations where a production is not used. In production-based implementations, the request and response messages (HS.FHIRServer.Interop.Request and HS.FHIRServer.Interop.Response) contain a `QuickStreamId` that is used to access a QuickStream object containing the FHIR payload. Though an interoperability request message also contains a `Request` property of type HS.FHIRServer.API.Data.Request, this `Request` property cannot be used to access the FHIR payload because its `Json` property is transient (the same is true for interoperability responses). As a result, a business host in the production that needs to access the FHIR payload must use the `QuickStreamID` to obtain the payload.

If the payload is in JSON format, the business host can access the payload and convert it to a dynamic object in order to modify it. For example, a BPL business process could use the following code to access and modify the FHIR payload of a request message that is in JSON format:

```objectscript
 //Identify payload as a Patient resource and convert to dynamic object
 if ((request.Request.RequestMethod="POST") & (request.Request.RequestPath="Patient"))
 {
   set stream = ##class(HS.SDA3.QuickStream).%OpenId(request.QuickStreamId)
   set myPatient = ##class(%DynamicObject).%FromJSON(stream)

   // Modify Patient resource
   do myPatient.%Set("active", 0, "boolean")

   //Update payload with modified Patient resource
   do myPatient.%ToJSON(stream)
   do stream.%Save()
 }
```

For more examples of manipulating FHIR data as dynamic objects, see FHIR Data.
