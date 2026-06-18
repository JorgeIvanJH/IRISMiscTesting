# Customizing a FHIR Server

When using a FHIR server, there are two strategies for customizing the behavior of the FHIR server. Like legacy HL7 FHIR technology, you can use logic in interoperability productions to modify the server’s behavior. However, you also have the option of customizing the architecture of the FHIR server to implement custom functionality. This option is important because a FHIR server that does not use an interoperability production can be significantly faster than one that does.

When customizing the server architecture, you are most commonly extending the Resource Repository, only customizing those parts of the server that are unique to your environment. In more rare cases, you may need to write an entirely custom backend for the FHIR server; the FHIR server’s architecture gives you the flexibility to do this. Regardless of whether you are extending the Resource Repository or writing a custom backend, the process of customizing the FHIR server starts with pre-installation subclassing.

Some behavior of the FHIR server is controlled through configuration options that do not require customization of the architecture. For details about these options, see Configuring a FHIR Server.

As you customize your FHIR server, you can update the server’s Capability Statement. For details, see Modifying the Capability Statement.

## Pre-Installation Subclassing

Customizing a FHIR server begins with using an IDE to subclass the architecture and define a few parameters. Because the InteractionsStrategy is specified during installation, this step must occur before the server’s endpoint is created by the installation process.

Most commonly, your FHIR server is extending the architecture of the Resource Repository. In these cases, open an IDE and subclass:

*   HS.FHIRServer.Storage.JsonAdvSQL.Interactions
    
*   HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy
    
*   HS.FHIRServer.Storage.JsonAdvSQL.RepoManager
    

If you are writing an entirely custom backend for your FHIR server instead of using the Resource Repository, subclass the architecture superclasses: HS.FHIRServer.API.Interactions, HS.FHIRServer.API.InteractionsStrategy, and HS.FHIRServer.API.RepoManager.

### Subclass Parameters

After using an IDE to create your Interactions, InteractionsStrategy and RepoManager subclasses, you must modify the following parameters of the InteractionsStrategy and RepoManager.

<table><tr><th>Superclass</th><th>Subclass Parameters</th></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.FHIRServer.API.InteractionsStrategy">HS.FHIRServer.API.InteractionsStrategy</a></td><td><ul><li><p><code>StrategyKey</code> — Specifies a unique identifier for the InteractionsStrategy.</p></li><li><p><code>InteractionsClass</code> — Specifies the name of your Interactions subclass.</p></li></ul></td></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.FHIRServer.API.RepoManager">HS.FHIRServer.API.RepoManager</a></td><td><ul><li><p><code>StrategyClass</code> — Specifies the name of your InteractionsStrategy subclass.</p></li><li><p><code>StrategyKey</code> — Specifies a unique identifier for the InteractionsStrategy. Must match the <code>StrategyKey</code> parameter in the InteractionsStrategy subclass.</p></li></ul></td></tr></table>

Once you have compiled your subclasses, you are ready to install the FHIR server. Simply specify the name of your InteractionsStrategy subclass during installation.

## Activating Custom Code

When making changes to your custom Interactions or InteractionsStrategy code during development, use the `New Server Instance` debugging option to activate your new code when the next FHIR request is made. For details, see Debugging the FHIR Server .

## Customizing the Resource Repository

Once you have subclassed the FHIR server architecture of the Resource Repository, you are ready to customize the server. Most commonly, your customizations involve overriding methods and parameters in the subclass of HS.FHIRServer.Storage.JsonAdvSQL.Interactions. The following is an introduction to the most common customizations that you can make to a FHIR server that uses the Resource Repository.

### Customization Quick Start

<table><tr><th>Goal</th><th>Action in subclass of <a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.FHIRServer.Storage.JsonAdvSQL.Interactions">HS.FHIRServer.Storage.JsonAdvSQL.Interactions</a></th></tr><tr><td>Customize a specific FHIR interaction</td><td>Override the method that corresponds to the interaction</td></tr><tr><td>Preprocess all requests</td><td>Override <code>OnBeforeRequest</code> to implement logic that is transparent to the user. This overridden method should include a call to the super class, for example: <code>Do ##super(pFHIRService, pFHIRRequest, pTimeout)</code>.<p>If you want FHIR clients to be aware that a request is being handled differently, create a custom FHIR operation.</p></td></tr><tr><td>Post-process all requests</td><td>Override <code>OnAfterRequest</code> to implement logic that is transparent to the user. This overridden method should include a call to the super class, for example: <code>Do ##super(pFHIRService, pFHIRRequest, .pFHIRResponse)</code>.<p>If you want FHIR clients to be aware that a request is being handled differently, create a custom FHIR operation.</p></td></tr><tr><td>Post-process results of a Read interaction</td><td>Override <code>PostProcessRead</code>. (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXFHIRADM_server_customize_arch#HXFHIRADM_server_customize_arch_repo_results">Example</a>)</td></tr><tr><td>Post-process results of a Search interaction</td><td>Override <code>PostProcessSearch</code> (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXFHIRADM_server_customize_arch#HXFHIRADM_server_customize_arch_repo_results">Example</a>)</td></tr><tr><td>Add custom FHIR operation</td><td>Override the <code>OperationHandlerClass</code> parameter to specify the name of your subclass of <code>HS.FHIRServer.Storage.BuiltInOperations</code>. See <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXFHIR_server_customize_operations">Custom FHIR Operations</a>.</td></tr><tr><td>Customize how bundles are processed</td><td>Override the <code>BatchHandlerClass</code> parameter to specify the name of your custom class. The default handler class is <a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.FHIRServer.DefaultBundleProcessor">HS.FHIRServer.DefaultBundleProcessor</a>.</td></tr><tr><td>Customize how OAuth tokens are processed</td><td>Override the <code>OAuth2TokenHandlerClass</code> parameter to specify the name of your custom class. The default handler class is <a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&amp;CLASSNAME=HS.FHIRServer.Util.OAuth2Token">HS.FHIRServer.Util.OAuth2Token</a>.</td></tr></table>

The following code samples demonstrate a few customizations that you could make to a FHIR server that uses the Resource Repository.

### Post-Processing Results

It is common to want to manipulate the results of a Read interaction or Search interaction. For example, you might want to modify data in a Patient that is returned by a Read interaction or remove certain resources from the results of a search. In the following example, results are modified based on Consent rules; the sample code assumes you have written a separate class to handle the Consent processing. The roles extracted from the request are InterSystems security roles.

```objectscript
Class MyCustom.FHIR.Interactions Extends HS.FHIRServer.Storage.JsonAdvSQL.Interactions
{
Property RequestingUser As %String [ Private, Transient ];
Property RequestingUserRoles As %String [ Private, Transient ];

Method OnBeforeRequest(pFHIRService As HS.FHIRServer.API.Service,
                       pFHIRRequest As HS.FHIRServer.API.Data.Request,
                       pTimeout As %Integer)
{
  //Extract the user and roles for this request
  //so consent can be evaluated.
  set ..RequestingUser = pFHIRRequest.Username
  set ..RequestingUserRoles = pFHIRRequest.Roles
}
Method OnAfterRequest(pFHIRService As HS.FHIRServer.API.Service,
                      pFHIRRequest As HS.FHIRServer.API.Data.Request,
                      pFHIRResponse As HS.FHIRServer.API.Data.Response)
{
  //Clear the user and roles between requests.
  set ..RequestingUser = ""
  set ..RequestingUserRoles = ""
}
Method PostProcessRead(pResourceObject As %DynamicObject) As %Boolean
{
  //Evaluate consent based on the resource and user/roles.
  //Returning 0 indicates this resource shouldn't be displayed - a 404 Not Found
  //will be returned to the user.
  if '##class(MyCustom.Consent).Consented(pResourceObject,
                                          ..RequestingUser,
                                          ..RequestingUserRoles) {
    return 0
  }

  //Modify (anonymize) the resource being returned to the client if they don't have
  //permission to see the full record.
  if (pResourceObject.resourceType = "Patient") &&
  ##class(MyCustom.Consent).Anonymize(..RequestingUser, ..RequestingUserRoles) {
    do pResourceObject.%Remove("name")
  }
  return 1
}
Method PostProcessSearch(pRS As HS.FHIRServer.Util.SearchResult,
                         pResourceType As %String) As %Status
{
  //Iterate through each resource in the search set and evaluate
  //consent based on the resource and user/roles.
  //Each row marked as deleted and saved will be excluded from the Bundle.
  do pRS.%SetIterator(0)
  while(pRS.%Next()) {
   set resourceObject = ..Read(pRS.ResourceType, pRS.ResourceId, pRS.VersionId)
   if '##class(MyCustom.Consent).Consented(resourceObject, ..RequestingUser,
                                           ..RequestingUserRoles)
   {
     do pRS.MarkAsDeleted()
     do pRS.%SaveRow()
   }
  }
  do pRS.%SetIterator(0)
  quit $$$OK
}

}
```

> **Tip:**
> 
> When customizing a FHIR server, it can be useful to determine if a resource is a shared resource. Shared resources do not contain Patient information; in FHIR terms, these resource types are not in the Patient compartment. You can use the `IsSharedResourceType()` method to determine if a resource is shared. For example, your custom Interactions class could include the following conditional statement:
> 
> ```
> Class MyCustom.FHIR.Interactions Extends HS.FHIRServer.Storage.JsonAdvSQL.Interactions
> Method OnBeforeRequest(pFHIRService As HS.FHIRServer.API.Service,
>                        pFHIRRequest As HS.FHIRServer.API.Data.Request,
>                        pFHIRResponse As HS.FHIRServer.API.Data.Response)
> {
>   If pFHIRService.Schema.IsSharedResourceType(pFHIRRequest.Type) {
>     //Do x,y,z
> }
> ```

### Assigning Custom IDs to Resources

It is possible to customize a Resource Repository server to assign each resource a custom id when performing Create interactions. The following example assigns a random UUID to the resource when it is stored in the Resource Repository.

```objectscript
Class MyCustom.FHIR.Interactions Extends HS.FHIRServer.Storage.JsonAdvSQL.Interactions
{

Method Add(pResourceObj As %DynamicObject, pResourceIdToAssign As %String = "",
           pHttpMethod = "POST") As %String
{
  //Assign a random UUID for each new resource's ID, except for when processing an
  //Update as Create (when a user uses the PUT method and explicitly defines the ID).
  if pHttpMethod '= "PUT" {
    set pResourceIdToAssign = $zconvert($system.Util.CreateGUID(), "L")
  }
  return ##super(pResourceObj, pResourceIdToAssign, pHttpMethod)
}
}
```

## Modifying the Capability Statement

The FHIR server’s Capability Statement is client-facing metadata that documents how the server behaves; FHIR clients can retrieve the Capability Statement to determine what the server expects and how it will process FHIR requests. As you customize your FHIR server, you may want to update the Capability Statement so FHIR clients have an accurate description of what the server supports. You have two options for updating the Capability Statement:

*   Retrieve the existing Capability Statement, edit its JSON, and then post it back to the server. Though straightforward, there is a limitation to this approach: the Capability Statement is automatically regenerated by certain actions, for example adding a new search parameter, so you might have to restore your customized Capability Statement after taking one of these actions. For details, see Manually Updating Capability Statement.
    
*   Modify the InteractionsStrategy subclass by overriding the methods that generate the Capability Statement. This gives you greater control over the Capability Statement and will not cause problems when it is regenerated. For details, see Overriding Capability Statement Methods.
    

### Manually Updating Capability Statement

You can retrieve the FHIR server’s Capability Statement with a REST client or programmatically, edit it with a text editor or third-party tool, and then update the server with the new version. Be aware that you may need to repeat this procedure after certain actions, for example, adding a new search parameter. Therefore, you may want to store a copy of the revised Capability Statement rather than recreating it when needed.

In the following examples, assume the IP address of the InterSystems server is `172.16.144.98`, the superserver port is `52782`, and the base URL of the endpoint is `/fhirapp/r4`.

*   To retrieve the Capability Statement with a REST client, send a `GET` request to `base-url/metadata`. For example:
    
    `GET http://172.16.144.98:52782/fhirapp/r4/metadata`
    
*   To retrieve the Capability Statement programmatically and save it as a JSON file, enter:
    
    ```objectscript
     set strategy = ##class(HS.FHIRServer.API.InteractionsStrategy).GetStrategyForEndpoint("/fhirapp/r4")
     set interactions = strategy.NewInteractionsInstance()
     set capabilityStatement = interactions.LoadMetadata()
     do capabilityStatement.%ToJSON("c:\localdata\MyCapabilityStatement.json")
    ```
    

Once you have modified the Capability Statement, submit the revised version to the server programmatically from the InterSystems Terminal. In the following example, `/fhirapp/r4` is the endpoint’s base URL and `MyCapabilityStatment.json` is the revised version. The `{}.%FromJSONFile` method takes a JSON file and puts it into a dynamic object.

```objectscript
  set strategy = ##class(HS.FHIRServer.API.InteractionsStrategy).GetStrategyForEndpoint("/fhirapp/r4")
  set interactions = strategy.NewInteractionsInstance()
  set newCapabilityStatement = {}.%FromJSONFile("c:\localdata\MyCapabilityStatement.json")
  do interactions.SetMetadata(newCapabilityStatement)
```

### Overriding Capability Statement Methods

Because the Capability Statement is regenerated automatically when changing certain FHIR server behavior, you might want to override the methods used to generate the server’s Capability Statement rather than manually updating it. This requires development tasks in an IDE, but gives you more control of the generation process. These tasks assume you have extended the Resource Repository by subclassing HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy. The method you need to override in this subclass depends on whether you want to edit basic metadata like the server’s publisher or modify the descriptions of the server’s functionality.

If you just want to change the server’s basic metadata in the Capability Statement, for example, the server’s name, you can modify the JSON template from which the Capability Statement is generated. This JSON template is located in the `GetCapabilityTemplate()` method of the endpoint’s InteractionsStrategy class. To change the server’s metadata strings:

1.  Create a `GetCapabilityTemplate()` method in your subclass of HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy to override the method.
    
2.  Copy the contents of HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy.GetCapabilityTemplate() into your subclass’ `GetCapabilityTemplate()` method.
    
3.  Edit the metadata strings and compile your subclass.
    
4.  Use the Console Setup utility to update the Capability Statement. For details, see Command Line Options.
    

If you want to change the substance of the Capability Statement, for example, what interactions are supported for a resource, you need to override the InteractionsStrategy’s `GetMetadataResource()` method. It is strongly recommend that your overriding method call `##super` to invoke `HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy.GetMetadataResource()Opens in a new tab`, and then post-process the Capability Statement that is returned by the method. You modify the returned Capability Statement as a dynamic object. For example, your subclass might look like:

```objectscript
Class Pkg.MyInteractionsStrategy Extends HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy
{
  Method GetMetadataResource()
   {
    set MyCapabilityStatement = ##super()
    // manipulate MyCapabilityStatement as a DynamicObject
    return MyCapabilityStatement
   }
}
```

Once you have overridden the method that generates the Capability Statement, be sure to update the Capability Statement using the Console Setup. For details, see Command Line Options.
