# Listing and Documenting REST APIs

This topic discusses how to discover the REST services that are available on an instance and how to generate documentation for REST services.

## Using the /api/mgmnt Service to Discover REST Services

The `/api/mgmnt` service includes calls you can use to discover REST service classes and REST-enabled web applications.

### Discovering REST Services

To use the `/api/mgmnt` service to discover the REST services that are available on an instance, use the following REST call:

*   For the HTTP action, select or specify GET.
    
*   For the URL, specify a URL of the following form, using the <baseURL> for your instance:
    
    `http://<baseURL>/api/mgmnt/v2/`
    
    Or, if you want to examine only one namespace:
    
    `http://<baseURL>/api/mgmnt/v2/:namespace`
    
    Where `namespace` is the namespace you want to examine.
    

(Note that these calls ignore manually-coded REST services. To discover manually-coded REST applications, use the calls GET /api/mgmnt/ and GET /api/mgmnt/:v1/:namespace/restapps.)

If the call is successful, InterSystems IRIS returns an array that lists the REST services, in JSON format. For example:

```
[
  {
    "name": "%Api.Mgmnt.v2",
    "webApplications": "/api/mgmnt",
    "dispatchClass": "%Api.Mgmnt.v2.disp",
    "namespace": "%SYS",
    "swaggerSpec": "/api/mgmnt/v2/%25SYS/%Api.Mgmnt.v2"
  },
  {
    "name": "myapp",
    "webApplications": "/api/myapp",
    "dispatchClass": "myapp.disp",
    "namespace": "USER",
    "swaggerSpec": "/api/mgmnt/v2/USER/myapp"
  }
]
```

### Discovering REST-Enabled Web Applications

To use the `/api/mgmnt` service to discover the REST-enabled web applications that are available on an instance, use the following REST call:

*   For the HTTP action, select or specify GET.
    
*   For the URL, specify a URL of the following form, using the <baseURL> for your instance:
    
    `http://<baseURL>/api/mgmnt`
    
    Or, if you want to examine only one namespace:
    
    `http://<baseURL>/api/mgmnt/v1/:namespace/restapps`
    
    Where `namespace` is the namespace you want to examine.
    

See the reference sections for GET /api/mgmnt/ and GET /api/mgmnt/:v1/:namespace/restapps.

## Using the %REST.API Class to Discover REST Services

The %REST.API class provides methods you can use to discover REST service classes and REST-enabled web applications.

### Discovering REST Service Classes

To use the %REST.API class to discover the REST services that are available on an instance, use the following methods of that class:

#### GetAllRESTApps()

```
GetAllRESTApps(Output appList As %ListOfObjects) as %Status
```

Returns, as output, a list of the REST services on this server. The output argument `applist` is an instance of %ListOfObjects, and each item in the list is an instance of %REST.Application that contains information about the REST service. This includes any REST services that do not have an associated web application. This method ignores any manually-coded REST services.

#### GetRESTApps()

```
GetRESTApps(namespace as %String,
            Output appList As %ListOfObjects) as %Status
```

Returns, as output, a list of the REST services in the namespace indicated by `namepace`. See `GetAllWebRESTApps()`. See `GetAllRESTApps()`.

### Discovering REST-Enabled Web Applications

To use the %REST.API class to discover the REST-enabled web applications that are available on an instance, use the following methods of that class:

#### GetAllWebRESTApps()

```
GetAllWebRESTApps(Output appList As %ListOfObjects) as %Status
```

Returns, as output, a list of the REST-enabled web applications on this server. The output argument `applist` is an instance of %ListOfObjects, and each item in the list is an instance of %REST.Application that contains information about web application.

#### GetWebRESTApps()

```
GetWebRESTApps(namespace as %String,
               Output appList As %ListOfObjects) as %Status
```

Returns, as output, a list of the REST-enabled web applications in the namespace indicated by `namepace`. See `GetAllWebRESTApps()`.

## Providing Documentation for a REST Service

It is useful to document any API so that developers can easily use the API. In the case of a REST API that follows the OpenAPI 2.0 specification, you can use the Swagger open-source framework to provide interactive documentation for your API, based upon the contents of the specification.

One option is to use Swagger UI and provide a hosted copy of the documentation. For a demo:

1.  Go to https://swagger.io/tools/swagger-ui/
    
2.  Click `Live Demo`.
    
3.  In the box at the top of the page, enter the URL of the OpenAPI 2.0 specification for the REST service, in JSON format.
    
    For example, use the GET /api/mgmnt/v2/:namespace/:application call on the InterSystems IRIS server.
    
4.  Click `Explore`.
    

The lower part of the page then displays the documentation as shown in the following example:

[Image: Swagger editor displaying methods for coffermaker sample including GET, PUT, and DELETE]

Here you can view details about each call, try test calls and see the responses. For more details, see the Swagger web site.

Other third-party tools enable you to generate static HTML. InterSystems has no specific recommendations for this.
