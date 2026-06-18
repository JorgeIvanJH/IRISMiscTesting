# Securing REST Services

If your REST service is accessing confidential data, you should use authentication for the service. If you need to provide different levels of access to different users, also specify privileges needed for the endpoints.

This topic assumes that you have previously generated REST service classes as described in Creating and Editing REST Services.

## Setting Up Authentication for REST Services

You can use any of the following forms of authentication with InterSystems IRIS data platform REST services:

*   HTTP authentication headers — This is the recommended form of authentication for REST services.
    
*   Web session authentication — Where the username and password are specified in the URL following a question mark.
    
*   OAuth 2.0 authentication — See the following subsection.
    

### REST Applications and OAuth 2.0

To authenticate a REST application via OAuth 2.0, do all of the following:

*   Configure the resource server containing the REST application as an OAuth 2.0 resource server.
    
*   Make sure that the web application (for the REST application) is configured to use delegated authentication.
    
*   Create a routine named `ZAUTHENTICATE` in the `%SYS` namespace. InterSystems provides a sample routine, `REST.ZAUTHENTICATE.mac`, that you can copy and modify. This routine is part of the Samples-Security sample on GitHub (https://github.com/intersystems/Samples-Security). You can download the entire sample as described in Downloading Samples for Use with InterSystems IRIS, but it may be more convenient to simply open the routine on GitHub and copy its contents.
    
    In your routine, modify the value of `applicationName` and make other changes as needed.
    

Also see Optionally Defining Delegated Authentication for the Web Client.

> **Important:**
> 
> If using authentication with HealthShare, you must use the `ZAUTHENTICATE` routine provided by InterSystems and cannot write your own.

## Specifying Privileges Needed to Use REST Services

To specify privileges needed to execute code or access data, InterSystems technologies use Role-Based Access Control (RBAC). For details, see Authorization: Controlling User Access.

If you need to provide different levels of access to different users, do the following to specify the permissions:

*   Modify the specification class to specify the privileges that are needed to use the REST service or specific endpoints in the REST service; then recompile. A privilege is a permission (such as read or write), combined with the name of a resource.
    
    See the subsection.
    
*   Using the Management Portal:
    
    *   Define the resources that you refer to in the specification class.
        
    *   Define roles that provide sets of privileges. For example, a role could provide read access to an endpoint or write access to a different endpoint. A role can contain multiple sets of privileges.
        
    *   Place users into all the roles needed for their tasks.
        

Additionally, you can use the SECURITYRESOURCE parameter of the %CSP.REST class to perform authorization.

### Specifying Privileges

You can specify a list of privileges for the entire REST service, and you can specify a list of privileges for each endpoint. To do so:

1.  To specify the privileges needed to access the service, edit the OpenAPI XData block in the specification class. For the `info` object, add a new property named `x-ISC_RequiredResource` whose value is a comma-separated list of resource groups that are required to access any endpoint of the REST service. A resource group can take two forms:
    
    *   Standard Form: A resource and its access mode (resource:mode). For example, `"resource1:read"`.
        
    *   Options Form: Two or more standard form resource groups separated by a forward slash ( / ) character. This indicates that at least one of the standard form resource groups is required, but not both. For example, `"resource1:read/resource2:read"` indicates that either `"resource1:read"` or `"resource2:read"` is needed to access the REST service.
        
    
    The following shows an example:
    
    ```
      "swagger":"2.0",
      "info":{
        "version":"1.0.0",
        "title":"Swagger Petstore",
        "description":"A sample API that uses a petstore as an example to demonstrate features in the swagger-2.0 specification",
        "termsOfService":"http://swagger.io/terms/",
        "x-ISC_RequiredResource":["resource1:read","resource2:read/resource3:read","resource4:read"],
        "contact":{
          "name":"Swagger API Team"
        },
    ...
    ```
    
2.  To specify the privileges needed to access a specific endpoint, add the `x-ISC_RequiredResource` property to the operation object that defines that endpoint, as in the following example:
    
    ```
          "post":{
            "description":"Creates a new pet in the store.  Duplicates are allowed",
            "operationId":"addPet",
            "x-ISC_RequiredResource":["resource1:read","resource2:read/resource3:read","resource4:read"],
            "produces":[
              "application/json"
            ],
            ...
    ```
    
3.  Compile the specification class. This action regenerates the dispatch class.
    

### Using the SECURITYRESOURCE Parameter

As an additional authorization tool, dispatch classes that subclass %CSP.REST have a `SECURITYRESOURCE` parameter. The value of `SECURITYRESOURCE` is either a resource and its permission or simply the resource (in which case the relevant permission is Use). The system checks if a user has the required permission on the resource associated with `SECURITYRESOURCE`.

> **Note:**
> 
> If the dispatch class specifies a value for `SECURITYRESOURCE` and the CSPSystem user is not sufficiently privileged, then this may result in unexpected HTTP error codes for failed login attempts. To prevent this from occurring, InterSystems recommends that you give permissions on the specified resource to the CSPSystem user.
