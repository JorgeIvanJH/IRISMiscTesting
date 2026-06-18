# FHIR Adapter for Interoperability Productions

Not all solutions require a FHIR server that routes requests to an internal repository. For example, an implementation may need to receive an HL7 FHIR request and forward it to an external FHIR server without ever storing its payload in an InterSystems product. In cases where you need to process a FHIR request without leveraging the internal repository of a FHIR server, you can use the FHIR Adapter for Interoperability Productions to receive requests into an interoperability production. For Health Connect implementations that are not licensed to install a FHIR server with a repository, incoming FHIR requests are processed by installing a FHIR Adapter for Interoperability Productions.

Installing the FHIR Adapter for Interoperability Productions creates a new interoperability REST endpoint that uses special business hosts to process FHIR requests in a production.

> **Note:**
> 
> This interoperability REST endpoint does not appear with the FHIR server endpoints in the Management Portal, and the adapter does not leverage the Inbound Adapter classes.

## Installing an Adapter

### Installing an Adapter Not Protected by OAuth 2.0

To install a FHIR Adapter that is not protected by OAuth 2.0:

1.  Create a namespace with an interoperability production.
    
2.  Open the InterSystems Terminal and change to the namespace that you just created. For example, enter:
    
    ```objectscript
     set $namespace = "myFHIRNamespace"
    ```
    
3.  Run the following command, specifying the URL of the interoperability REST endpoint:
    
    ```objectscript
     set status = ##class(HS.FHIRServer.Installer).InteropAdapterConfig("/MyEndpoint/r5")
    ```
    
    The URL of the Adapter’s endpoint must start with a slash (`/`).
    
4.  To ensure the command executed successfully, enter:
    
    ```objectscript
     write status
    ```
    
    The response should be `1`.
    
5.  If this was the first FHIR Adapter created for the namespace, navigate to `Interoperability` > `List` > `Productions`, open your production, and do one of the following:
    
    *   If you see an `Update` button, select it.
        
    *   If the `Update` button does not appear and you are ready to test your production, select `Start` to start the production.
        

### Installing an Adapter Protected by OAuth 2.0

To install a FHIR adapter protected by OAuth 2.0:

1.  Create a business service instance of HS.FHIRServer.Interop.Service in an interoperability production as follows:
    
    1.  Open the `Production Configuration` screen by navigating to `Interoperability` > `Foundation Namespace` > `Configure` > `Production`.
        
    2.  Open the `Business Service Wizard` by clicking the plus (+) icon next to the `Services` column header.
        
    3.  From the `Service Class` dropdown, choose HS.FHIRServer.Interop.Service.
        
    4.  In the `Service Name` field, give the service a name, then click `OK`.
        
2.  Use a source code editor to extend the class HS.FHIRServer.HC.FHIRInteropAdapter to a new class, and override the class parameter `ServiceConfigName` to the service class of your new business service:
    
    ```
    Class HS.Demo.MyInterop Extends HS.FHIRServer.HC.FHIRInteropAdapter
    {
    Parameter ServiceConfigName As %String = "<MyServiceName>";
    }
    ```
    
3.  Create a CSP REST application with Dispatch Class set to the new class, as follows:
    
    1.  Navigate to `System Administration` > `Security` > `System Security` > `Authentication/Web Session Options`, and enable `Allow OAuth2 authentication` checkbox.
        
    2.  Navigate to `System Administration` > `Security` > `Applications` > `Web Applications` > `Create New Web Application`, and fill out the form:
        
        *   `Namespace`: the namespace of the FHIR endpoint
            
        *   `Enable`: check the radio button for REST
            
        *   `Dispatch Class`: the class you created earlier by extending HS.FHIRServer.HC.FHIRInteropAdapter
            
        *   Uncheck the `Unauthenticated` checkbox and check `Password` and `OAuth2`
            
4.  On the `Production Configuration` screen, configure your production with additional settings and functionality as needed.
    
5.  Create an OAuth 2.0 Resource Server for the new endpoint. For information about creating an OAuth 2.0 Resource Server, see “Server-Type Configuration” in Using an InterSystems IRIS Web Application as an OAuth 2.0 Resource Server.
    

## Adapter Components

Installing the FHIR Adapter creates:

*   A web application with the specified URL
    
*   A new business service in the interoperability production called `InteropService`. If you install multiple Adapters, they all use the same `InteropService` business service. If you want an Adapter to use a different business service, see Using a Custom Business Service.
    
*   A new business operation in the interoperability production called `InteropOperation`. This is a placeholder business operation that can be extended or replaced according to your use case. Until you modify `InteropOperation` to implement custom functionality, it returns an `501 Unimplemented` error when a FHIR request is received by the new interoperability REST endpoint.
    
    > **Note:**
    > 
    > When using a production, you must explicitly set the `ContentType` property of an HS.FHIRServer.Interop.Response to create the HTTP response Content-Type header. Setting the `ResponseFormatCode` in the HS.FHIRServer.API.Data.Response is not sufficient.
    

For details about other production components that can be used in conjunction with the FHIR Adapter, see Interoperability Productions.

## Using a Custom Business Service

By default, if you install multiple FHIR Adapters, they all share the same business service, `InteropService`. If you want requests received by the adapter endpoints to be routed to different business services, you need to create a subclass of the REST handler and specify it as the Dispatch Class of the Adapter’s CSP application. This process of using a custom business service consists of the following steps:

1.  Using an IDE, create a subclass of HS.FHIRServer.HC.FHIRInteropAdapter.
    
2.  Use your subclass’ `ServiceConfigName` parameter to specify the name of the custom business service that will receive the FHIR requests.
    
3.  In the Management Portal, navigate to `System Administration` > `Security` > `Applications` > `Web Applications`.
    
4.  Select the URL of your FHIR Adapter.
    
5.  Using the `Enable` field on the `General` tab, specify the name of your subclass in the `Dispatch` text box.
    
6.  Select `Save`.
    

## FHIR Adapter Requests and Responses

See FHIR Production Requests and Responses.

## Security

Security of the interoperability REST endpoint depends on the security settings of the web application created for the FHIR Adapter. For example, you can configure the web application to require that the user making the FHIR request have privileges to an InterSystems resource. The security settings for the web application are available by navigating to `System Administration` > `Security` > `Applications` > `Web Applications`. The web application is identified by the URL of the interoperability REST endpoint. For details about the security settings, see Edit a Web Application.

The FHIR Adapter for Interoperability Productions does not provide extensive OAuth 2.0 support. If a request to the adapter contains an OAuth 2.0 token, it is examined with basic tests that determine if the token is in the Authorization header, is non-blank, and is on a secure connection. Unlike a FHIR server, it does not examine the token’s contents like scope and patient context value. If the token passes the adapter’s basic tests, it is added to the request message in the `AdditionalInfo` property of HS.FHIRServer.API.Data.Request.
