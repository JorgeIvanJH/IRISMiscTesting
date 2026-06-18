# Custom FHIR Operations

The FHIR server supports HL7 FHIR operations that perform special functions based on requests from the FHIR client using an RPC-like approach rather than a RESTful one. These can be standard FHIR operations like `$everything` or custom ones. FHIR servers using or extending the Resource Repository already support certain standard FHIR operations (see Supported FHIR Operations for a complete list).

The following is an overview of the process of adding FHIR operations to your FHIR server.

1.  Subclass the FHIR server’s architecture. For details, see Pre-Installation Subclassing.
    
2.  Create a subclass of HS.FHIRServer.API.OperationHandler. If you are using the Resource Repository, subclass HS.FHIRServer.Storage.BuiltInOperations instead of HS.FHIRServer.API.OperationHandler so you do not lose the default operations like `$everything`. As a best practice, you might want to create a separate subclass for each operation, and then create a master class that inherits from all of them.
    
3.  In your Interactions subclass, override the value of the `OperationHandlerClass` parameter to be the classname of the operation subclass that you just created.
    
4.  Write a method for each operation in your operation handler subclass.
    
5.  Add the operations to the CapabilityStatement resource.
    

The following sections provide more details on the last two steps of the process.

## Writing Methods for Custom Operations

Operations supported by the FHIR server correspond directly to methods in the operation handler subclass. The names of these methods must conform to the following syntax:

`FHIRScopeOpOperationName`

Within this syntax, the variables are:

*   `Scope` identifies the type of endpoint to which the FHIR client is appending the operation. Possible values are:
    
    *   `System` — Identifies operations that are appended to a “base” FHIR endpoint (for example, http://fhirserver.org/fhir). These operations apply to the entire server.
        
    *   `Type` — Identifies operations that are appended to a FHIR endpoint with a resource type (for example, http://fhirserver.org/fhir/Patient). These operations work with all instances of the specified resource type.
        
    *   `Instance` — Identifies operations that are appended to a FHIR endpoint that points to a specific instance of a resource (for example, http://fhirserver.org/fhir/Patient/1). These operations work solely with a specific instance of a resource.
        
*   `OperationName` is the `$` operation that the FHIR client appends to its call to the server.
    

The following table of examples shows the correlation between method names and the operations called by a FHIR client.

<table><tr><th>Method name</th><th>REST client call to the operation</th></tr><tr><td><code>FHIRSystemOpMyoperation</code></td><td><code>http://fhirserver.org/fhir/$myoperation</code></td></tr><tr><td><code>FHIRTypeOpValidate</code></td><td><code>http://fhirserver.org/fhir/Observation/$validate</code></td></tr><tr><td><code>FHIRInstanceOpEverything</code></td><td><code>http://fhirserver.org/fhir/Patient/1/$everything</code></td></tr></table>

If your operation contains a hyphen (`-`), just remove the hyphen from the method name. For example, if the system-wide operation is `$my-operation`, name the method `FHIRSystemOpMyoperation`.

The following is an example of the method signature for `$everything`:

```objectscript
ClassMethod FHIRInstanceOpEverything(pService As HS.FHIRServer.API.Service,
                                     pRequest As HS.FHIRServer.API.Data.Request,
                                     pResponse As HS.FHIRServer.API.Data.Response) {}
```

## Adding the Operation to Capability Statement

The Capability Statement of the FHIR server should include all of the operations that the server supports. You have two choices for updating the Capability Statement with new operations:

*   Manually add the operations to the Capability Statement. This approach has one drawback: the Capability Statement is sometimes regenerated, for example, when adding a new search parameter, and manual modifications are lost upon regeneration. For details on this process, see Manually Updating Capability Statement.
    
*   Modify the `AddSupportedOperations()` method in your operation handler subclass to automatically add the new operation to the Capability Statement when it is regenerated. See the following section for details on this approach.
    

You can use the following two-step procedure to automatically add a new operation to the Capability Statement.

1.  Add the operation to the `AddSupportedOperations()` method of the operation handler subclass. When the command-line utility generates the server’s Capability Statement, it takes the supported operations from this method. As an example, the operation handling class for a server that supports the `$everything` operations would include a method that looked like:
    
    ```objectscript
    ClassMethod AddSupportedOperations(pMap As %DynamicObject)
      {
        Do pMap.%Set("everything","http://hl7.org/fhir/OperationDefinition/patient-everything")
      }
    ```
    
    If the superclass of your operation handling class already includes some operations, be sure to call the `AddSupportedOperations()` method of that superclass within the `AddSupportedOperations()` of the subclass. For example, the method of the operation handling subclass might look like:
    
    ```objectscript
    ClassMethod AddSupportedOperations(pMap As %DynamicObject)
      {
        Do ##class(HS.FHIRServer.MySuperclass.Validate).AddSupportedOperations(pMap)
        Do pMap.%Set("everything", "http://hl7.org/fhir/OperationDefinition/patient-everything")
      }
    ```
    
    If you created a subclass for each operation and a master class that inherits from all of them, make sure the master class calls the `AddSupportedOperations()` method of each operation’s subclass.
    
2.  Use the command-line utility to regenerate the Capability Statement:
    
    1.  From the InterSystems Terminal, change to the FHIR server’s namespace. For example:
        
        ```objectscript
         set $namespace = "MyFHIRNamespace"
        ```
        
    2.  Run the installation and configuration utility:
        
        ```objectscript
         do ##class(HS.FHIRServer.ConsoleSetup).Setup()
        ```
        
    3.  Choose the option `Update the CapabilityStatement Resource`.
        
    4.  Select the endpoint you are configuring.
        
    5.  Confirm your selection.
