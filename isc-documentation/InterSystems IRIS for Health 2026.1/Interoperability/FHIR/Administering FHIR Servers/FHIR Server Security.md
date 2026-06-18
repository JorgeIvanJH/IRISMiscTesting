# FHIR Server Security

You can control which clients can make requests to the FHIR server and the interactions they can perform using the following:

*   InterSystems security strategies
    
*   OAuth 2.0
    

## Using Basic Authentication with a FHIR server

By default, the FHIR server enforces basic authentication in which any user with credentials to an InterSystems product can access the FHIR server by including those credentials in the header of the REST call. In this security strategy, the user’s authorization within the InterSystems product is not a factor; any authenticated user can perform CRUD interactions on the FHIR server.

### Adding Authorization Requirements

By adding authorization requirements to basic authentication, you can restrict server access to InterSystems users who are authorized to work with a specific security resource (which is unrelated to an HL7 FHIR resource). In InterSystems security terms, only users who belong to roles that have privileges to the security resource are authorized to perform interactions on the server. Users with a Write privilege to the required security resource can perform create, delete, update, and conditional update interactions on the FHIR server. Users with a Read privilege to the security resource can perform all interactions except the ones that require write access.

> **Note:**
> 
> FHIR transactions are recursive. If a transaction request contains both read and write interactions, a user must hold Write privileges.

The following is a basic overview of how to create a security resource, assign privileges to the security resource for a role, and assign users to the role. For a detailed description of InterSystems authorization, see the Authorization Guide; for an introduction to security, see About InterSystems Security.

1.  To create the security resource that controls whether users are authorized to perform interactions on the server, open the Management Portal and navigate to `Home` > `System Administration` > `Security` > `Resources`. Setting the `Public Permission` to Read allows all authenticated users to perform Read interactions on the server. For more information, see Create or Edit a Resource.
    
2.  To create a role that will have privileges to the security resource, navigate to `Home` > `System Administration` > `Security` > `Roles`. Most commonly, there will be two roles, one for users who should have Read access and another for users who should have Write access. For more information, see Create Roles.
    
3.  To grant privileges to a role:
    
    1.  Click `Add` in the `Privileges` section of the role’s `General` tab.
        
    2.  Select the security resource that will control server authorization, and click `OK`.
        
    3.  Click `Edit` next to the new Privilege.
        
    4.  Select the permissions you want the role to have for the security resource.
        
    
    For more information, see Give New Privileges to a Role.
    
4.  Now that you have a role that has permissions to the security resource, select the `Members` tab and add the users that you want to have those permissions. For more information, see Assign Users or Roles to the Current Role.
    

#### Configuring a FHIR Server to Require a Security Resource

Once you have created or chosen the security resource that will control a user’s ability to perform FHIR interactions, configure the server to require this security resource in one of the following ways:

##### Adding a Security Resource to a FHIR Server Using the Management Portal

Navigate to the FHIR Server Management page, and under FHIR Server Authorization Settings, select a security resource. The management portal only allows you to add a security resource to an existing FHIR server.

##### Adding a Security Resource to a FHIR Server Using the REST API

In the FHIR Config REST API, set the value of `endpoint.service_config_data.required_resource` to identify the chosen security resource:

*   using the `POST /endpoint` method when creating a new FHIR server.
    
*   using the `PUT /endpoint` method when adding a security resource to an existing FHIR server.
    

##### Adding a Security Resource to a FHIR Server Programmatically

In the terminal or using a custom method, in the namespace of an existing FHIR server:

```
 set config = ##class(HS.FHIRServer.ServiceAdmin).GetInstanceConfigData(serviceId)
 set config.Resource = "my_resource"
 do ##class(HS.FHIRServer.ServiceAdmin).SetInstanceConfigData(serviceId,config)
```

Where `my_resource` indicates the chosen security resource, and `serviceID` identifies the desired endpoint.

##### Adding a Security Resource to a FHIR Server Using the Command Line Interface

```objectscript
 do ##class(HS.FHIRServer.ConsoleSetup).Setup()
```

Using option 4 `Configure a FHIRServer Endpoint` set the value of `RequiredResource` to identify the chosen security resource.

## Using OAuth 2.0 with a FHIR Server

You can set up your FHIR server as an OAuth 2.0 resource server. This allows the FHIR server to reject a client FHIR request unless the client presents a valid access token that it obtained from an OAuth 2.0 authorization server. A FHIR request’s access token is checked twice, once by the REST handler and again when it reaches the FHIR server’s internal Service. Because the access token is enforced when the request reaches the REST handler, the token has already been validated when it enters an interoperability production (if the FHIR server has been configured to use a production).

The REST handler and the Service use the same class to validate the token, which is the class specified by the `OAuth2TokenHandlerClass` parameter of the server’s Interactions class.

The FHIR server’s default `OAuth2TokenHandlerClass` is HS.FHIRServer.Util.OAuth2Token. This default token handling class enforces access as described in Access Token Scopes to ensure SMART on FHIR compatibility.

> **Important:**
> 
> If you are using an InterSystems IRIS for Health OAuth 2.0 authorization server (InterSystems OAuth server) to issue authorization tokens for your FHIR server, configure your OAuth 2.0 server to use or extend the classes in the `HS.HC.OAuth2.Server` package, as described in Configuring an OAuth Server for FHIR. Doing so ensures that the OAuth server behaves as expected by the FHIR server’s default token handing class.
> 
> If your InterSystems OAuth server is on the same instance as your FHIR server, you can invoke the ConfigureInternalOAuthClients() method of the HS.HC.OAuth2.Client.Installer class to quickly set up client configurations.

From the point of view of an OAuth authorization server, a FHIR resource server is a client. You can use the `OAuth FHIR Client Quickstart` in the Management Portal to connect your FHIR resource server to any OAuth 2.0 authorization server, as follows:

Prerequisites:

*   If you have not already done so, you must configure the Network Host Name before executing these steps.
    
*   If you wish to use an internal OAuth server, you must first set up secure communication. For details, see Setting Up Secure Communication for a Foundation Production.
    

Instructions:

1.  In the Management Portal, navigate to `Home` > `Health` > `FHIR` (or `Home` > `Health` > `foundationNamespace` > `FHIR Server Management`).
    
2.  Click `OAuth FHIR Client Quickstart` in the left-hand navigation bar.
    
3.  Choose whether to use an existing FHIR server or to create a new one, by clicking the tile that matches your choice, then click `Next`.
    
4.  Identify the desired FHIR server by doing one of the following:
    
    *   If you chose to create a new FHIR server, complete the `Create New FHIR Server` form. For field help, see Installing a FHIR Server. Then click `Next`.
        
    *   If you chose to use an existing FHIR server, choose the desired `Namespace` and FHIR server `URL` from the dropdowns in the `Use an Existing FHIR Server` form, then click `Next`.
        
5.  Connect your selected FHIR server to an OAuth server by clicking the tile that matches your choice, then click `Next`.
    
    > **Note:**
    > 
    > To use an internal OAuth server you must have previously set up secure communication.
    
6.  > **Note:**
    > 
    > This step is needed only if you chose an external OAuth Server.
    
    Enter the issuer endpoint, then click `Test`. The system now tests to see whether the issuer endpoint is discoverable. This verifies the identity of the issuer endpoint as an OAuth 2.0 server. When the test has succeeded and the `Next` button appears, click `Next`.
    
7.  Review the selections you have made. To confirm your selections, click `Confirm`.
    
8.  Upon success, your OAuth server is associated with your FHIR resource server, and a list of configurations is displayed. If something goes wrong, you will instead see a list of the errors that occurred. You can use the `Back` button and edit configuration choices to eliminate errors.
    

### Connecting a Server to an OAuth Server

You can use the `OAuth Clients` configuration interface to interoperate with any type of server that is protected by an OAuth server. This interface allows an administrator to configure an OAuth client to be used by a FHIR resource server (handling requests and validating scopes), or as an authenticated client wishing to authorize with an OAuth server (e.g. for making requests exernally to any OAuth-protected resource server. This is the Bulk FHIR use case).

1.  To use the `OAuth Clients` configuration interface, in the Management Portal, navigate to `Health->[your foundation namespace]->FHIR Server Management->Security Configuration->OAuth Clients`.
    
2.  In the `OAuth Clients` table, click the pencil-shaped `Edit` icon in the row for the client you wish to edit.
    
3.  Make your edits in the edit window, then click `Save`.
    
    To revert to the previous state, eliminating your changes instead, click `Reset`. To cancel and close the editor, click `Cancel`.
    

### Access Token Scopes and FHIR

> **Note:**
> 
> Although `read`/`write` syntax is supported, permissions are best specified using SMART on FHIR v2-style syntax. See the HL7 specification for details.

This section explains how the FHIR server enforces the scopes of an OAuth 2.0 access token that is passed along with a request.

If your FHIR server needs to interpret scopes differently, you need to customize the FHIR server and override the `OAuth2TokenHandlerClass` parameter to specify your custom token handling class.

Access tokens can have the following scopes:

*   Patient resource scopes (`patient`) limit authorization to resources related to the patient specified in the patient context claim. They are likely to be used, for example, when a patient is looking at their data through a web portal.
    
*   User resource scopes (`user`) allow access to view or manipulate FHIR resource types that the particular user is authorized to access. This kind of authorization is subject to any implementation-specific authorization processing (for example, consent).
    
*   System scopes (`system`) represent external systems. They are used to facilitate system-to-system interactions such as bulk data extracts.
    

> **Note:**
> 
> When a FHIR interaction is authorized by `patient` or `user` resource scopes, it should be subject to any additional implementation-specific processing (such as consent) that may be in use. This type of additional processing is not expected for interactions authorized by `system` scopes.

#### Fine-grained Scopes

You can restrict authorization to a resource type so that it grants access only to a subset of resources of that type. For example, rather than authorizing access to all Observation resources, you can authorize access only to Observation resources that belong to the laboratory category. To do so, add a query string suffix to a scope, starting with a question mark (?) and followed by a fhir query string. For example:

```
patient/Observation.rs?category=http://terminology.hl7.org/CodeSystem/observation-category|laboratory
```

This example uses the Observation resource type `category` parameter.

> **Note:**
> 
> You can mix fine-grained scopes with resource-level scopes.

General syntax to create a fine-grained scope is:

```
<scope_type>/<resource>.<permission>?<fhir_query_string>
```

*   `<scope_type>` – the type of scope in use; possible values are `patient`, `user`, and `system`.
    
*   `<resource>` – the main resource type. For example `patient/Observation`. You can use an asterisk character (`*`) as a wildcard value.
    
*   `<permission>` – SMART-on-FHIR style “cruds” permissions to be granted. For example, `.rs` grants read and search permissions. For details about SMART-on-FHIR “cruds” permissions, see Scopes for requesting FHIR Resources in the HL7 FHIR specification. You can use an asterisk character (`*`) as a wildcard value.
    
*   `<fhir_query_string>` – the fhir query string detailing the subset of resources for the specified resource type. For example, `category=http://terminology.hl7.org/CodeSystem/observation-category|laboratory` limits access to laboratory observations.
    

Interactions Support

*   Fine-grained scopes are supported for `read`, `create`, `update`, `search`, and `delete` interactions.
    
*   Fine-grained scopes are not supported for `history` and `vread`.
    
*   See the interaction tables in the HL7 FHIR specification for details about interactions.
    

Incompatible Search Parameters

The following search parameters are valid for general FHIR searches, but are incompatible with fine-grained scopes. These search parameters are considered invalid, and will cause the entire FHIR request to be rejected with a 401 Unauthorized status:

*   `_include` and `_revinclude`
    
*   `_summary=count`
    
*   `_count=0`
    
*   `_maxresults`
    
*   `_type` unless the resource type on the scope is the wildcard (`*`).
    

The following search parameters will be silently ignored:

*   `_sort`
    
*   `_count` for values other than `0`
    
*   `_summary` for values other than `count`
    
*   `_total`
    
*   `_elements`
    

> **Note:**
> 
> The `$find` and `$update-functional` operations honor fine-grained scopes only on the List resource type.

See the SMART App Launch Implementation Guide for the full specification of SMART-on-FHIR fine-grained scopes.

#### Basic Processing

The access token that accompanies a request must include at least one scope (system, patient resource, or user resource), or else the request is rejected with an HTTP 403 error. If multiple scopes are present, the union of the scopes is evaluated. For example, if both user resource and patient resource scopes are present, all scopes are potentially evaluated, until any of them authorizes the current FHIR interaction, or until none of them does.

#### Patient Resource Scope / Patient Context Value

If an access token includes a patient resource scope, it must also include a patient context value (also known as “launch context”) that is the Patient resource ID. This patient context value provides access to the specified Patient and its related resources. In most cases, the patient resource scope must provide explicit access to a related resource. For example, if the patient context value is `1234`, and the patient resource scope is `patient/Observation.cruds`, the FHIR server can grant access to an Observation that references the Patient with the id `1234`. In this case, `patient/Observation.cruds` (or another scope granting access to Observations) is required. As an exception to this requirement, a FHIR client can access a resource that is shared among multiple Patients without obtaining a patient resource scope that is specific to that resource. For example, if the scope is `patient/Patient.rs`, then a client can access an Organization referenced by the Patient without having a scope `patient/Organization.rs`.

To obtain the patient context value from the access token, the FHIR server examines the `patient` property of the access token.

#### Search

The FHIR server handles search requests accompanied by a valid access toke in the following manner:

*   If filtered searching is enabled, only permitted resources are returned. The generated SQL queries will only select those resources your scopes allow.
    
*   If filtered searching is disabled, the FHIR query will be generated without considering the scopes. If all resources in the results set are permitted by the scope and context, the response includes the full results set. If any resources are not permitted, the response is a 403 Forbidden error.
    
    *   If a query uses both fine-grained scopes and chaining, the search will not be performed; instead, the response will be a 403 Forbidden error.
        
    *   The search resource type must be allowed by the patient scopes.
        
    *   If the search resource type is not Patient, reference search parameter values must indicate a Patient resource that is in the patient context.</para>
        
    *   If `_include` and <literal>_revinclude</literal> parameters are present they must indicate only pulling in resources that are allowed by the scopes
        
    *   For a Patient search, any <literal>_id</literal> value must match the patient context value.
        

#### `$everything`

If filtered searching is enabled, only those search results that are permitted by the scope and context are provided; results that are not permitted are omitted from the provided results set.

If filtered searching is disabled, requests for the Patient or Encounter `$everything` operation must include an access token that has read access to all of the resources that might be returned by the request. If a resource is encountered in the compartment that is not covered by the scope, then the entire request is rejected with an HTTP 403 Forbidden error.

The practical application of this requirement is:

*   If a `_type` operation query parameter is specified, then the scope must include read access to all of the resource types requested.
    
*   If no types are specified and the access token is using a patient resource scope, it should have a `patient/*.rs` or `patient/*.cruds` scope in order to return any resource encountered in the compartment.
    
*   If no types are specified and the access token is using a user resource scope, it should have a `user/*.rs` or `user/*.cruds` scope in order to return any resource encountered in the compartment.
    

#### `$lastn`

The `$lastn` operation is specific to the Observation resource type. It supports `_include` and `_revinclude`.

When filtered searching is enabled, only those search results that are permitted by the scope and context are provided; results that are not permitted are omitted from the provided results set. When filtered searching is disabled, if the results set includes any resources that are not permitted, the response will be a 403 Forbidden error.

### Configuring an OAuth Server for FHIR

You can configure the InterSystems IRIS for Health OAuth 2.0 authorization server (InterSystems OAuth server) by defining custom classes which implement its behavior. If you are using an InterSystems OAuth server to issue tokens for a FHIR server, InterSystems provides the following implementation classes, which extend the default classes in the %OAuth.Server package to implement compatibility with the FHIR server’s default token handling class:

<table><tr><td>Function</td><td>Class Name</td></tr><tr><td>Authenticate Class</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.HC.OAuth2.Server.Authenticate">HS.HC.OAuth2.Server.Authenticate</a></td></tr><tr><td>Validate User Class</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.HC.OAuth2.Server.Validate">HS.HC.OAuth2.Server.Validate</a></td></tr><tr><td>Session Maintenance Class</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.HC.OAuth2.Server.Session">HS.HC.OAuth2.Server.Session</a></td></tr><tr><td>Generate Token Class</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.HC.OAuth2.Server.Generate">HS.HC.OAuth2.Server.Generate</a> *</td></tr><tr><td>Revoke Token Class</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.HC.OAuth2.Server.Revoke">HS.HC.OAuth2.Server.Revoke</a></td></tr></table>

* Extends %OAuth2.Server.JWT.

To quickly set up an InterSystems OAuth server on your instance which uses these classes, you can issue the following Terminal command:

```objectscript
 do ##class(HS.HC.OAuth2.Server.Installer).ConfigureInternalOAuthServer()
```

The normal token request process includes the Patient and Encounter contexts in the access token when those contexts are requested. To determine the presence or absence of a particular context in an access token, you can use either the `GetIntrospection()` method of the %SYS.OAuth2.AccessToken class or the `ValidateJWT()` method of the %SYS.OAuth2.Validation class.

If you want to further customize the behavior of the InterSystems OAuth server for use with your FHIR server, implement classes which extend these `HS.HC.OAuth2.Server` classes.

### Setting Up SMART on FHIR

You can set up your FHIR server to be compatible with SMART on FHIR client applications.

#### Prerequisite

You must have an OAuth server that is configured to issue tokens as described in the SMART on FHIR specification.

For information about how to configure an InterSystems IRIS for Health OAuth 2.0 server, see Using InterSystems IRIS as an OAuth 2.0 Authorization Server. Ensure that the OAuth 2.0 server is using or extending the classes listed in Configuring the OAuth Server.

For information about how the FHIR server enforces access token scopes, see Access Token Scopes.

1.  Configure a FHIR server, following the instructions in Installing and Configuring a FHIR Server.
    
2.  Create a client definition that registers your FHIR server as a resource server to your OAuth 2.0 server, as described in OAuth 2.0 Authentication. Be sure to specify the following for your FHIR server’s client configuration:
    
    <table><tr><td><code>Application name</code></td><td>Enter the local name of the client application.</td></tr><tr><td><code>Client name</code></td><td>Enter the global name to be used for dynamic registration.</td></tr><tr><td><code>Description</code></td><td>Enter a description of the server.</td></tr><tr><td><code>Enabled</code></td><td>Check this box.</td></tr><tr><td><code>Client Type</code></td><td>Check the <code>Resource server</code> radio button.</td></tr><tr><td><code>SSL/TLS configuration</code></td><td>From this dropdown, select the same SSL option you selected previously.</td></tr><tr><td><code>Authentication Type</code></td><td>Choose the <code>basic</code> radio button.</td></tr></table>
    
    When you finish filling out the form, save your configuration options by clicking `Dynamic Registration and Save`.
    
3.  Configure the FHIR server to use the name in the OAuth 2.0 client registration, as follows:
    
    1.  Navigate to `Home` > `Health > FHIR`.
        
    2.  In the tile representing your FHIR server, open the menu and choose `Edit`.
        
    3.  Under `FHIR Server Authorization Settings`, in the `OAuth Client Name` dropdown, choose the `Client name` that you assigned the FHIR resource server in the step above.
        
    4.  Click `Save`.
