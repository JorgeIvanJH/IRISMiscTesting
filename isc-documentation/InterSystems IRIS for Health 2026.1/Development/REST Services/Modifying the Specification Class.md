# Modifying the Specification Class

This topic summarizes how and why to modify the specification class for a REST service.

This topic assumes that you have previously generated REST service classes as described in Creating and Editing REST Services.

## Overview

The following table lists reasons for modifying the specification class and briefly summarizes the needed changes:

<table><tr><th>Reason</th><th>Changes</th></tr><tr><td>To update or replace the specification</td><td>Modify the <code>OpenAPI</code> XData block manually or by regenerating the specification class.</td></tr><tr><td>Enable REST service to support CORS</td><td>Modify the <code>OpenAPI</code> XData block manually; also add a class parameter and create a custom dispatch superclass. See <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GREST_specification#GREST_specification_cors">Supporting CORS in REST Services</a>.</td></tr><tr><td>Enable REST service to support web session</td><td>Add a class parameter. See <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GREST_specification#GREST_specification_websess">Using Web Sessions with REST</a>.</td></tr><tr><td>Specify privileges needed to use endpoints</td><td>Modify the <code>OpenAPI</code> XData block manually. See <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GREST_securing">Securing REST Services</a>.</td></tr><tr><td>Override the default content type, response character set, or input stream handling</td><td>Add class parameters. See the <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GREST_specification#GREST_specification_parms">next section</a>.</td></tr><tr><td>Specify a non-default name for a service method</td><td>Modify the <code>OpenAPI</code> XData block manually. See <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GREST_specification#GREST_specification_methodname">Overriding the Name of a Service Method</a>.</td></tr></table>

Whenever you compile the specification class, the compiler regenerates the dispatch class in the same package and updates the implementation class (see How InterSystems Updates the Implementation Class).

## Overriding the Content Type or Input Stream Handling

You can override several key aspects of the REST service simply by adding class parameters to the specification class and recompiling.

*   By default, the REST service expects the `application/json` content type. To override this, add the following to the specification class:
    
    ```
    Parameter CONTENTTYPE = "some-content-type";
    ```
    
    Where `some-content-type` is a MIME content type.
    
*   By default, the REST service converts input character streams to Unicode. To not do this, add the following to the specification class:
    
    ```
    Parameter CONVERTINPUTSTREAM = 0";
    ```
    

Then recompile. These changes are then copied to the dispatch class.

## Overriding the Name of a Service Method

By default, the compiler uses the `operationId` of an operation to determine the name of method invoked by the corresponding REST call. You can specify a different name. To do so, add the following to the operation within the `OpenAPI` XData block of the specification class:

```
"x-ISC_ServiceMethod":"alternatename"
```

For example:

```
    "/pets":{
      "get":{
        "description":"Returns all pets from the system that the user has access to",
        "operationId":"findPets",
        "x-ISC_ServiceMethod":"ReturnPets",
        "produces":[
          "application/json",
          "application/xml",
          "text/xml",
          "text/html"
        ],
```

Then recompile. The compiler then adds this new method to the dispatch and implementation classes. Be sure to edit the implementation class and provide an implementation for this new method.

## Supporting CORS in REST Services

Cross-Origin Resource Sharing (CORS) allows a script running in another domain to access a service.

Typically, when a browser is running a script from one domain, it allows XMLHttpRequest calls to that same domain but disallows them when they are made to another domain. This browser behavior restricts someone from creating a malicious script that can misuse confidential data. The malicious script could allow the user to access information in another domain using permissions granted to the user, but then, unknown to the user, make other use of confidential information. To avoid this security problem, browsers generally do not allow this kind of cross-domain call.

Without using CORS, a web page with a script accessing REST services typically must be in the same domain as the server providing the REST services. In some environments, it is useful to have the web pages with scripts in a different domain than the servers providing the REST services. CORS enables this arrangement.

The following provides a simplified description of how a browser can handle an XMLHttpRequest with CORS:

1.  A script in a web page in domain DomOne contains an XMLHttpRequest to an InterSystems IRIS data platform REST service that is in domain DomTwo. The XMLHttpRequest has a custom header for CORS.
    
2.  A user views this web page and runs the script. The user’s browser detects the XMLHttpRequest to a domain different from the one containing the web page.
    
3.  The user’s browser sends a special request to the InterSystems IRIS REST service that indicates the HTTP request method of the XMLHttpRequest and the domain of the originating web page, which is DomOne in this example.
    
4.  If the request is allowed, the response contains the requested information. Otherwise, the response consists only of headers indicating that CORS did not allow the request.
    

### Overview of Enabling a REST Service to Support CORS

By default, InterSystems REST services do not allow the CORS header. You can, however, enable CORS support. There are three parts to enabling support for CORS in a REST service:

*   Enable the REST service to accept the CORS header for some or all HTTP requests. See Accepting the CORS Header.
    
*   Edit your web application in the management portal to allow access only to cross-origin requests that come from a particular origin or include a specific header, ensuring that only trusted data from other origins is passed to your service. This step makes the next step optional, as the default CORS header processing is acceptable when a CORS request originates from a known and permitted source.
    
*   Write code that causes the REST service to examine the CORS requests and decide whether to proceed. InterSystems IRIS provides a simple default implementation, which allows any CORS request from the list of permitted sources you defined in the previous step.
    

### Accepting the CORS Header

To specify that a REST service accepts the CORS header:

1.  Modify the specification class to include the `HandleCorsRequest` parameter.
    
    To enable CORS header processing for all calls, specify the `HandleCorsRequest` parameter as 1:
    
    ```
    Parameter HandleCorsRequest = 1;
    ```
    
    Or, to enable CORS header processing for some but not all calls, specify the `HandleCorsRequest` parameter as `""` (empty string):
    
    ```
    Parameter HandleCorsRequest = "";
    ```
    
2.  If you specified `HandleCorsRequest` parameter as `""`, edit the `OpenAPI` XData block in the specification class in order to indicate which calls support CORS. Specifically, for the operation objects, add the following property name and value:
    
    ```
    "x-ISC_CORS":true
    ```
    
    For example, the OpenAPI XData block might contain this:
    
    ```
    "post":{
      "description":"Creates a new pet in the store.  Duplicates are allowed",
      "operationId":"addPet",
      "produces":[
        "application/json"
      ],
      ...
    ```
    
    Add the `x-ISC_CORS` property as follows:
    
    ```
    "post":{
      "description":"Creates a new pet in the store.  Duplicates are allowed",
      "operationId":"addPet",
      "x-ISC_CORS":true,
      "produces":[
         "application/json"
      ],
      ...
    ```
    
3.  Compile the specification class. This action regenerates the dispatch class, causing the actual change in behavior. It is not necessary to understand the dispatch class in detail, but notice the following changes:
    
    *   It now contains your value for the `HandleCorsRequest` parameter.
        
    *   The URLMap XData block now includes `Cors="true"` for the `<Route>` element that corresponds to the operation you modified.
        

If the `HandleCorsRequest` parameter is 0 (the default), then CORS header processing is disabled for all calls. In this case, if the REST service receives a request with the CORS header, the service rejects the request.

> **Important:**
> 
> An InterSystems IRIS REST service supports the OPTIONS request (the CORS preflight request), which determines whether a REST service supports CORS.
> 
> In non-`Minimal` security installations, users that send such requests should have READ permission on any databases used by the REST service. In configurations that use delegated authentication, the request will be sent by the authenticated user; assign appropriate permissions in the ZAUTHENTICATE routine. In configurations that do not use delegated authentication, this request is sent unauthenticated and is executed by the CSPSystem user; assign appropriate permissions using the management portal. In particular, you must explicitly grant the CSPSystem user access to the database in which the REST application’s dispatch class is defined, regardless of the roles assigned to the web application.
> 
> If these requirements are not met, the service responds with an HTTP 500 error, halting the subsequent POST, PUT, or DELETE request.

### Allow Access to Specific Origins and Headers

REST services that accept the CORS header can accept a CORS request from any origin. This behavior is inadvisable, as it may result in protect data being accessed from an unintended source. However, you can limit the origins that your REST service accepts the CORS header from so that you can be sure you are passing data only to authorized sources.

When creating a new REST service, define a list of allowed origins and headers as described in Edit an Application: The Cross-Origin Setting Tab to create an allow list.

### Defining How to Process the CORS Header

When you enable a REST service to accept the CORS header, by default, the service accepts any CORS request. You can limit the origins it accepts by editing the web application in the Management Portal. If you do not, your REST service should examine the CORS requests and decide whether to proceed. To do this, you need to:

*   Create a subclass of %CSP.REST. In this class, implement the `OnHandleCorsRequest()` method as described in the first subsection.
    
*   Modify the specification class and recompile, regenerating the dispatch class.
    

The net result is that the dispatch class inherits from your custom class instead of from %CSP.REST and thus uses your definition of `OnHandleCorsRequest()`, which overrides the default CORS header processing.

#### Defining OnHandleCorsRequest()

In your subclass of %CSP.REST, define the `OnHandleCorsRequest()` method, which needs to examine the CORS requests and set the response header appropriately.

To define this method, you must be familiar with the details of the CORS protocol (not discussed here).

You also need to know how to examine the requests and set the response headers. For this, it is useful to examine the method that is used by default, the `HandleDefaultCorsRequest()` method of %CSP.REST. This section explains how this method handles the origin, credentials, header, and request method and suggests variations. You can use this information to write your `OnHandleCorsRequest()` method.

The following code gets the origin and uses it to set the response header.

```
#; Get the origin
Set tOrigin=$Get(%request.CgiEnvs("HTTP_ORIGIN"))

#; Allow requested origin
Do ..SetResponseHeaderIfEmpty("Access-Control-Allow-Origin",tOrigin)
```

The following lines specify that the authorization header should be included.

```
#; Set allow credentials to be true
Do ..SetResponseHeaderIfEmpty("Access-Control-Allow-Credentials","true")
```

The following lines get the headers and the request method from the incoming request. Your code should test if the headers and request method are allowed. If they are allowed, use them to set the response headers. If not, set the response header to an empty string.

```
#; Allow requested headers
Set tHeaders=$Get(%request.CgiEnvs("HTTP_ACCESS_CONTROL_REQUEST_HEADERS"))
Do ..SetResponseHeaderIfEmpty("Access-Control-Allow-Headers",tHeaders)

#; Allow requested method
Set tMethod=$Get(%request.CgiEnvs("HTTP_ACCESS_CONTROL_REQUEST_METHOD"))
Do ..SetResponseHeaderIfEmpty("Access-Control-Allow-Method",tMethod)
```

#### Modifying the Specification Class

After defining your custom subclass of %CSP.REST including an implementation of the `OnHandleCorsRequest()`, do the following:

1.  Edit the OpenAPI XData block in the specification class so that the `info` object contains a new property named `x-ISC_DispatchParent`. The value of this property must be the fully qualified name of your custom class.
    
    For example, suppose that the OpenAPI XData block looks like this:
    
    ```
      "swagger":"2.0",
      "info":{
        "version":"1.0.0",
        "title":"Swagger Petstore",
        "description":"A sample API that uses a petstore as an example to demonstrate features in the swagger-2.0 specification",
        "termsOfService":"http://swagger.io/terms/",
        "contact":{
          "name":"Swagger API Team"
        },
    ...
    ```
    
    Suppose that the custom subclass of %CSP.REST is named `test.MyDispatchClass`. In this case, you would modify the XData block as follows:
    
    ```
      "swagger":"2.0",
      "info":{
        "version":"1.0.0",
        "title":"Swagger Petstore",
        "description":"A sample API that uses a petstore as an example to demonstrate features in the swagger-2.0 specification",
        "termsOfService":"http://swagger.io/terms/",
        "x-ISC_DispatchParent":"test.MyDispatchClass",
        "contact":{
          "name":"Swagger API Team"
        },
    ...
    ```
    
2.  Compile the specification class. This action regenerates the dispatch class. You will notice that the class now extends your custom dispatch superclass. Thus it will use your `OnHandleCorsRequest()` method.
    

## Using Web Sessions with REST

One of the goals of REST is to be stateless; that is, no knowledge is stored on the server from one REST call to the next. Having a web session preserved across REST calls breaks the stateless paradigm, but there are two reasons why you might want to preserve a web session:

*   Minimize connection time — if each REST call creates a new web session, it needs to establish a new session on the server. By preserving a web session, the REST call connects faster.
    
*   Preserve data across REST calls — in some cases, preserving data across REST calls may be necessary to efficiently meet your business requirements.
    

To enable using a single web session over multiple REST calls, set the `UseSession` parameter to 1 in the specification class. For example:

```
Parameter UseSession As Integer = 1;
```

Then recompile this class.

If `UseSession` is 1, InterSystems IRIS preserves a web session across multiple REST service calls. If the parameter is 0 (the default), InterSystems IRIS uses a new web session for each REST service call.

> **Note:**
> 
> When you recompile the specification class, the `UseSession` parameter is copied to the dispatch class, which causes the actual change in behavior.
