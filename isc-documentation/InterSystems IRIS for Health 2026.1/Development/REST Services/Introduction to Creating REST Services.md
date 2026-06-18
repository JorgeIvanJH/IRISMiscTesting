# Introduction to Creating REST Services

This page introduces REST and REST services in InterSystems IRIS data platform. You can use these REST interfaces with UI tools, such as Angular, to provide access to databases and interoperability productions. You can also use them to enable external systems to access InterSystems IRIS applications. For an interactive introduction to REST services, try Developing REST Interfaces.

## Introduction to REST

REST, which is named from “Representational State Transfer,” has the following attributes:

*   REST is an architectural style rather than a format. Although REST is frequently implemented using HTTP for transporting messages and JSON for passing data, you can also pass data as XML or plain text. REST makes use of existing web standards such as HTTP, URL, XML, and JSON.
    
*   REST is resource oriented. Typically a resource is identified by a URL and uses operations based explicitly on HTTP methods, such as GET, POST, PUT, DELETE, and OPTIONS.
    
*   REST typically has a small overhead. Although it can use XML to describe data, it more commonly uses JSON which is a lightweight data wrapper. JSON identifies data with tags but the tags are not specified in a formal schema definition and do not have explicit data types.
    

## Introduction to InterSystems REST Services

There are two ways to define REST interfaces in InterSystems IRIS 2019.2 and later:

*   Specification-first definition — you first create an OpenAPI 2.0 specification and then use the API Management tools to generate the code for the REST interface.
    
*   Manually coding the REST interface.
    

Using a specification-first definition, an InterSystems REST service formally consists of the following components:

*   A specification class (a subclass of %REST.Spec). This class contains the OpenAPI 2.0 specification for the REST service. InterSystems supports several extension attributes that you can use within the specification.
    
*   A dispatch class (a subclass of %CSP.REST). This class is responsible for receiving HTTP requests and calling suitable methods in the implementation class.
    
*   An implementation class (a subclass of %REST.Impl). This class defines the methods that implement the REST calls.
    
    The API management tools generate a stub version of the implementation class, which you then expand to include the necessary application logic. (Your logic can of course invoke code outside of this class.)
    
    The %REST.Impl class provides methods that you can call in order to set HTTP headers, report errors, and so on.
    
*   An InterSystems web application, which provides access to the REST service via the InterSystems Web Gateway. The web application is configured to enable REST access and to use the specific dispatch class. The web application also controls access to the REST service.
    

InterSystems follows a strict naming convention for these components. Given an application name (`appname`), the names of the specification, dispatch, and implementation class are `appname.spec`, `appname.disp`, and `appname.impl`, respectively. The web application is named `/csp/appname` by default but you can use a different name for that.

InterSystems supports the specification-first paradigm. You can generate initial code from the specification, and when the specification changes (for example, by acquiring new end points), you can regenerate that code. Later sections provide more details, but for now, note that you should never edit the dispatch class, but can modify the other classes. Also, when you recompile the specification class, the dispatch class is regenerated automatically and the implementation class is updated (preserving your edits).

### Manually Coding REST Services

In releases before 2019.2, InterSystems IRIS did not support the specification-first paradigm. A REST service formally consisted only of a dispatch class and a web application. The documentation refers to this way to define REST services as manually-coded REST services. The distinction is that a REST service defined by newer REST service includes a specification class, and a manually-coded REST service does not. Creating a REST Service Manually describes how to create REST services using the manual coding paradigm. Similarly, some of the API management utilities enable you to work with manually-coded REST services.

## Introduction to InterSystems API Management Tools

To help you create REST services more easily, InterSystems provides the following API management tools:

*   A REST service named `/api/mgmnt`, which you can use to discover REST services on the server, generate OpenAPI 2.0 specifications for these REST services, and create, update, or delete REST services on the server.
    
*   The `^%REST` routine, which provides a simple command-line interface that you can use to list, create, and delete REST services.
    
*   The %REST.API class, which you can use to discover REST services on the server, generate OpenAPI 2.0 specifications for these REST services, and create, update, or delete REST services on the server.
    

You can set up logging for these tools, as described later.

Helpful third-party tools include REST testing tools such as PostMan (https://www.getpostman.com/) and the Swagger editor (https://swagger.io/tools/swagger-editor/download/).

## Overview of Creating REST Services

The recommended way to create REST services in InterSystems products is roughly as follows:

1.  Obtain (or write) the OpenAPI 2.0 specification for the service.
    
2.  Use the API management tools to generate the REST service classes and the associated web application. See Creating and Editing REST Services.
    
3.  Modify the implementation class so that the methods contain the suitable business logic. See Modifying the Implementation Class.
    
4.  Optionally modify the specification class. See Modifying the Specification Class. For example, do this if you need to support CORS or use web sessions.
    
5.  If security is required, see Securing REST Services.
    
6.  Using the OpenAPI 2.0 specification for the service, generate documentation as described in Discovering and Documenting REST APIs.
    

For step 2, another option is to manually create the specification class (pasting the specification into it) and then compile that class; this process generates the dispatch and stub implementation class. That is, it is not strictly necessary to use either the `/api/mgmnt` service or the `^%REST` routine. This documentation does not discuss this technique further.

## A Closer Look at the REST Service Classes

This section provides a closer look at the specification, dispatch, and implementation classes.

### Specification Class

The specification class is meant to define the contract to be followed by the REST service. This class extends %REST.Spec and contains an XData block that contains the OpenAPI 2.0 specification for the REST service. The following shows a partial example:

```
Class petstore.spec Extends %REST.Spec [ ProcedureBlock ]
{

XData OpenAPI [ MimeType = application/json ]
{
{
  "swagger":"2.0",
  "info":{
    "version":"1.0.0",
    "title":"Swagger Petstore",
    "description":"A sample API that uses a petstore as an example to demonstrate features in the swagger-2.0 specification",
    "termsOfService":"http://swagger.io/terms/",
    "contact":{
      "name":"Swagger API Team"
    },
    "license":{
      "name":"MIT"
    }
  },
...
```

You can modify this class by replacing or editing the specification within the XData block. You can also add class parameters, properties, and methods as needed. Whenever you compile the specification class, the compiler regenerates the dispatch class and updates the implementation class (see How InterSystems Updates the Implementation Class).

### Dispatch Class

The dispatch class is directly called when the REST service is invoked. The following shows a partial example:

```objectscript
/// Dispatch class defined by RESTSpec in petstore.spec
Class petstore.disp Extends %CSP.REST [ GeneratedBy = petstore.spec.cls, ProcedureBlock ]
{

/// The class containing the RESTSpec which generated this class
Parameter SpecificationClass = "petstore.spec";

/// Default the Content-Type for this application.
Parameter CONTENTTYPE = "application/json";

/// By default convert the input stream to Unicode
Parameter CONVERTINPUTSTREAM = 1;

/// Sets the response charset to utf-8
Parameter CHARSET = "utf-8";

XData UrlMap [ XMLNamespace = "http://www.intersystems.com/urlmap" ]
{
<Routes>
  <Route Url="/pets" Method="get" Call="findPets" />
  <Route Url="/pets" Method="post" Call="addPet" />
  <Route Url="/pets/:id" Method="get" Call="findPetById" />
  <Route Url="/pets/:id" Method="delete" Call="deletePet" />
</Routes>
}

/// Override %CSP.REST AccessCheck method
ClassMethod AccessCheck(Output pAuthorized As %Boolean) As %Status
{
   ...
}

...

}
```

Notice that the `SpecificationClass` parameter indicates the name of the associated specification class. The URLMap XData block (the URL map) defines the calls within this REST service. It is not necessary for you to have a detailed understanding of this part of the class.

After these items, the class contains the definitions of the methods that are listed in the URL map. Here is one example:

```objectscript
ClassMethod deletePet(pid As %String) As %Status
{
    Try {
        If '##class(%REST.Impl).%CheckAccepts("application/json") Do ##class(%REST.Impl).%ReportRESTError(..#HTTP406NOTACCEPTABLE,$$$ERROR($$$RESTBadAccepts)) Quit
        If ($number(pid,"I")="") Do ##class(%REST.Impl).%ReportRESTError(..#HTTP400BADREQUEST,$$$ERROR($$$RESTInvalid,"id",id)) Quit
        Set response=##class(petstore.impl).deletePet(pid)
        Do ##class(petstore.impl).%WriteResponse(response)
    } Catch (ex) {
        Do ##class(%REST.Impl).%ReportRESTError(..#HTTP500INTERNALSERVERERROR,ex.AsStatus())
    }
    Quit $$$OK
}
```

Notice the following points:

*   This method invokes a method by the same name in the implementation class (`petstore.impl` in this example). It gets the response from that method and calls `%WriteResponse()` to write the response back to the caller. The `%WriteResponse()` method is an inherited method that is present in all implementation classes, which are all subclasses of %REST.Impl.
    
*   This method does other checking and in case of errors, invokes other methods of %REST.Impl.
    

> **Important:**
> 
> Because the dispatch class is a generated class, you should never edit it. Instead, modify and recompile the specification class.

### Implementation Class

The implementation class is meant to hold the actual internal implementation of the REST service. You can (and should) edit this class. It initially looks like the following example:

```objectscript
/// A sample API that uses a petstore as an example to demonstrate features in the swagger-2.0 specification<br/>
/// Business logic class defined by RESTSpec in petstore.spec<br/>
Class petstore.impl Extends %REST.Impl [ ProcedureBlock ]
{

/// If ExposeServerExceptions is true, then details of internal errors will be exposed.
Parameter ExposeServerExceptions = 0;

/// Returns all pets from the system that the user has access to<br/>
/// The method arguments hold values for:<br/>
///     tags, tags to filter by<br/>
///     limit, maximum number of results to return<br/>
ClassMethod findPets(tags As %ListOfDataTypes(ELEMENTTYPE="%String"), limit As %Integer) As %Stream.Object
{
    //(Place business logic here)
    //Do ..%SetStatusCode(<HTTP_status_code>)
    //Do ..%SetHeader(<name>,<value>)
    //Quit (Place response here) ; response may be a string, stream or dynamic object
}

...
}
```

The rest of the implementation class contains additional stub methods that look similar to this one. In each case, these stub methods have signatures that obey the contract defined by the specification of the REST service. Note that for the `options` method, InterSystems does not generate a stub method for you to implement. Instead, the class %CSP.REST automatically performs all `options` processing.

## Enabling Logging for API Management Features

To enable logging for the API management features, enter the following in the Terminal:

```
 set $namespace="%SYS"
 kill ^ISCLOG
 set ^%ISCLOG=5
 set ^%ISCLOG("Category","apimgmnt")=5
```

Then the system adds entries to the `^ISCLOG` global for any calls to the API management endpoints.

To stop logging, enter the following (still within the `%SYS` namespace):

```
 set ^%ISCLOG=0
 set ^%ISCLOG("Category","apimgmnt")=0
```

By default, the maximum number of entries in the log is 10000. To change this, call the `MaxLogEntriesSet()` method of %Library.SysLog.

### Viewing the Log

Once logging for HTTP requests is enabled, the log entries are stored in the `^ISCLOG` global, which is located in the `%SYS` namespace.

To use the Management Portal to view the log, navigate to `System Explorer` > `Globals` and view the `^ISCLOG` global (not `^%ISCLOG)`. Make sure you are in the `%SYS` namespace.

To write the `ISCLOG` global as a log file (for easier readability), enter the following (still within the `%SYS` namespace):

```
 do ##class(%OAuth2.Utils).DisplayLog("filename")
```

Where `filename` is the full pathname of the file to create. The directory must already exist. If the file already exists, it is overwritten. This method uses the existing data in `^ISCLOG` and generates the given file.
