# Configuring an Existing FHIR Server

To configure an existing FHIR server, you can:

*   Use the FHIR Server Management page
    
*   Use the OAuth FHIR Client Quickstart menu
    
*   Use an ObjectScript API
    
*   Use the FHIR Server Management REST API
    
*   Use the command-line interface
    

## Configuring a FHIR Server from FHIR Server Management

You can edit the configuration settings of an existing FHIR server using the `FHIR Server Management` page.

To edit the configuration settings of an existing FHIR server:

1.  Open the `FHIR Server Management` page.
    
    Either of the following paths in the Management Portal will take you to the page:
    
    *   Navigate to `Home` > `Health` (or `Home` > `HealthShare` ) and click `FHIR` in the banner.
        
    *   Navigate to `Home` > `Health` > `FHIRServerNamespace` > `FHIR Server Management`.
        
2.  Click the menu icon in the tile for the desired server.
    
3.  Select `Edit`.
    
    The various configuration options are described in Basic Configuration Options and Advanced Configuration Options, below.
    
4.  When you have finished modifying the configuration, click `Save` to save your changes. To start over instead, click `Cancel`.
    

> **Note:**
> 
> If you expect to post Bundles containing 10,000 or more entries, increase the value of the Web Gateway’s Server Response Timeout parameter to prevent a timeout from interrupting your data loads.

### Basic FHIR Server Configuration Options

You can modify the basic FHIR server configuration options using the following descriptions as a guide:

#### Namespace

You cannot modify the namespace of an installed FHIR server.

#### Name

Optionally change the server name in the `Name` field. `Name` is a required field when configuring a FHIR server using the `FHIR Server Management` page.

#### FHIR Version

You cannot modify the FHIR version of an installed FHIR server.

#### URL

Optionally edit the endpoint `URL`. Ensure that the URL begins with a slash (`/`).

#### Custom Packages

*   If there are custom packages associated with the FHIR version of this server, you may select one from the `Custom Packages` dropdown.
    
*   If this dropdown is not present, there are no custom packages associated with this FHIR version.
    

For more information about packages, see Profiles and FHIR Adaptations.

In particular, for information about managing packages programmatically, see Package APIs.

> **Note:**
> 
> Enabling a custom package automatically triggers the system to re-index search tables when you save your changes.

### Advanced FHIR Server Configuration Options

The `Advanced Configuration` pane of the dialog has four sections, as shown in the image below:

[Image: generated description: server advanced config]

Expand a section to edit the settings. Use the following descriptions as a guide.

*   FHIR Server Service Configuration
    
*   FHIR Server Authorization Settings
    
*   FHIR Server Request Settings
    
*   Interactions Strategy Settings
    

#### FHIR Server Service Configuration

##### Data Organization Strategy

You cannot edit the data organization strategy for an existing FHIR server. To use a different strategy, create a new server.

##### Resource Database/Resource History Database

You cannot edit the database locations from the `FHIR Server Management` page once the databases contain resources.

##### Service Config Name

The name of the service configuration.

To route FHIR requests through an interoperability production before they reach the FHIR server, select the package and name of the business service that will receive the requests. Unless the business service has a custom name, this entry is `HS.FHIRServer.Interop.Service`.

> **Note:**
> 
> For a business service to appear in this dropdown, it must extend the HS.FHIRServer.Interop.Service class, and it must be included in an interoperability production in this namespace.

For more details, see

*   Interoperability Productions
    
*   Adding Business Hosts
    

#### FHIR Server Authorization Settings

##### OAuth Client Name

The FHIR server is an OAuth resource server. From the point of view of the OAuth 2.0 authorization server, it is a client for validating the token. Specify the application (client) name for the FHIR server resource server to use when contacting the OAuth 2.0 authorization server. Select the desired OAuth client name from the dropdown list. For more information about OAuth 2.0 support, see Using OAuth 2.0 with a FHIR Server under FHIR Security.

##### Required Resource

To configure the FHIR server such that a FHIR client requires a particular security resource in order to send a request, select that security resource from the dropdown.

To add a security resource for your FHIR client, see Adding Authorization Requirements.

##### Filter Search Results According to SMART-on-FHIR scopes

Checking this checkbox enables search to be filtered based on SMART-on-FHIR scopes. This means that if a search query’s results set would include items that are not permitted based on the scopes indicated by the query’s access token, the returned results will omit unpermitted items — returning only resources that are permitted by the SMART-on-FHIR scopes.

If search filtering is disabled (that is, if this checkbox is unchecked), no results would be returned if any included resources are not permitted; instead the query response would be a 403 Forbidden error.

#### FHIR Server Request Settings

##### Default Search Page Size

Search result page size to use when a search does not contain a `_count` parameter.

##### Max Search Page Size

Maximum search result page size to prevent an excessive user-specified page size.

##### Max Search Results

Maximum number of resources that can be selected by a search before the server responds to the query with an error. This number only includes resources selected by the actual search; it does not include resources included using an `_include` search parameter. This value does not affect the size of pages returned by a search. Overly broad searches that select large numbers of resources take a lot of system resources to fulfill, and are probably more broad than the client actually needs.

##### Default Prefer Handling

Specifies what happens by default when a search request contains an unknown parameter:

*   To ignore an unknown parameter in a search request and return a bundle in which the OperationOutcome resource identifies the issue, specify `lenient`.
    
*   To reject a search request with an unknown parameter and return an error, specify `strict`.
    

A FHIR search request that includes the “prefer header” overrides this default.

##### Max Conditional Deletes

Maximum allowable number of resources to delete using conditional delete. If the conditional delete search finds more than this number of resources, then the conditional delete as a whole is rejected with an HTTP 412 “Precondition Failed” error.

##### FHIR Session Timeout

Maximum number of seconds between requests to the service before any session data is considered stale.

#### Interactions Strategy Settings

> **Note:**
> 
> Which options appear under `Interactions Strategy Settings` depend upon which `Data Organization Strategy` you selected when you installed your FHIR server. The list below describes the options available across all interaction strategies. You may see only a subset of these options in your FHIR server.

##### SMART on FHIR Capabilities

Specify the server’s SMART on FHIR capabilities by entering them as a comma-delimited list into this field. This list does not control the functionality of the endpoint; rather, it specifies the capabilities that are returned in the JSON document when a client appends `/.well-known/smart-configuration` to the endpoint’s URL. For example:

```
launch-ehr, context-ehr-patient, permission-patient, client-public, client-confidential-symmetric
```

For more details about SMART on FHIR capabilities retrieved with Well-Known URIs, see FHIR Authorization Endpoint and Capabilities Discovery using Well-Known Uniform Resource Identifiers (URIs).

##### Silence search parameter indexing errors

Select this option to prevent search parameter indexing errors from aborting FHIR resource save.

> **Caution:**
> 
> Enable this setting only when necessary.

##### Prematurely limit the number of resources...with _max_results

Select this option to make FHIR search queries more efficient by adding a SQL operation `TOP N` where `N` is the value of the `_maxresults` search result parameter.

> **Caution:**
> 
> Use this setting only if you do not have `PostProcessSearch()` logic, since post processing filters could remove some or all of the hits from the results set, leading the query to return a number of hits fewer than `_maxresults`.
> 
> Refer to the hovertext for the field in the management portal for additional discussion of the tradeoffs in selecting this option.

##### Disable FHIR Audit

Select this option to disable FHIR auditing for this endpoint.

##### Functional List Configuration

> **Note:**
> 
> The Functional List Configuration field displays only for FHIR endpoints that use or extend the HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy Data Organization Strategy.

Comma-delimited string of configurations for functional lists. Each list element is a colon-delimited string of three items:

*   `functional list name` — the names available in the default interactions strategy are:
    
    *   `$current-problems`
        
    *   `$current-medications`
        
    *   `$current-allergies`
        
    *   `$current-drug-allergies`
        
*   `list subject search parameter` — can be `patient`, `subject`, or `source`
    
*   `list subject resource type` — for example, `Patient`
    

The default value is:

```
$current-problems:patient:Patient,
$current-medications:patient:Patient,
$current-allergies:patient:Patient,
$current-drug-allergies:patient:Patient
```

## Configuring a FHIR Server Programmatically

> **Note:**
> 
> You can also configure a FHIR server programmatically using the FHIR Server Management REST API.

Once you have installed a FHIR server, you can configure it programmatically using the UpdateInstance() method of HS.FHIRServer.Installer. This method accepts several arguments that configure the server, including one that accepts the server’s HS.FHIRServer.API.ConfigData object, which contains most of the server’s configuration options.

In addition to the options defined with the ConfigData object, a few of the server’s settings (`serviceConfigName`, `OAuthClient` name, and `enabled`) are specified using a dedicated parameter of the `UpdateInstance()` method (as shown in the example below). For a list of these configuration options, see the class reference description for UpdateInstance().

The following code configures an existing FHIR server using the `UpdateInstance()` method.

```objectscript
 Set appKey = "/fhirendpoint/r5"

 //Get and modify FHIR server's configuration object
 Set strategy = ##class(HS.FHIRServer.API.InteractionsStrategy).GetStrategyForEndpoint(appKey)
 Set configData = strategy.GetServiceConfigData()
 Set configData.DefaultPreferHandling = "strict"
 Set configData.DebugMode = 1
 //stringify configData before updating FHIR Server
 Set jsonConfigData = configData.AsJSONString()

 // Define additional settings
 Set enabled = 1
 Set serviceConfigName = "HS.InteropPackage.myBusinessService"
 Set oAuthClient = "OAuthClientName"

 // Update FHIR Server
 Do ##class(HS.FHIRServer.Installer).UpdateInstance(appKey, jsonConfigData, enabled, serviceConfigName, oAuthClient)
```

> **Note:**
> 
> Like all InterSystems IRIS APIs that act on code in a repository, HS.FHIRServer.Installer.UpdateInstance() locks the repository to prevent simultaneous configuration activities and holds the lock until configuration is complete. Before performing configuration tasks on your FHIR server using methods other than InterSystems IRIS APIs, execute the `Lock()` method of the HS.FHIRServer.Repo class to lock the repository explicitly, as follows: `##class(HS.FHIRServer.Repo).Lock()`. If you completely override an InterSystems IRIS method, remember to use the `Lock()` method to prevent conflicts.

## Configuring a FHIR Server Using Command Line Options

You can use a command line configure an existing FHIR server.

To configure an existing FHIR server using the command line interface:

1.  Open the InterSystems Terminal and change to your foundation namespace.
    
2.  Run the following command:
    
    ```objectscript
     do ##class(HS.FHIRServer.ConsoleSetup).Setup()
    ```
    
3.  Choose an option and then answer the questions as described in the sections below.
    
    > **Note:**
    > 
    > The `Create FHIRServer Endpoint` option is described in the installation chapter.
    

The following sections describe the command line configuration options for an existing FHIR server:

### Add a profile package to an endpoint

Adds a FHIR package to an existing endpoint so it can support the package’s profiles, search parameters, and other conformance resources. The FHIR package (an NPM-like package) that contains the conformance resources must be uploaded before you can use this option. You can use the `Upload a FHIR Metadata Package` option to import the FHIR package. Some common packages, for example the US Core Implementation Guide, are already available.

Note that enabling a package triggers the system to re-index search tables.

### Display a FHIRServer Endpoint Configuration

Displays the current configuration options of the FHIR server. To modify these configuration options, use the `Configure a FHIRServer Endpoint` option.

### Configure a FHIRServer Endpoint

Allows you to configure the FHIR server endpoint by providing values for each configuration option. For a description of each configuration item, see Configuring a FHIR Server.

### Decommission a FHIRServer Endpoint

Deletes a FHIR server endpoint, but retains the FHIR data that has been collected by the endpoint. The SQL tables containing the FHIR data are retained. If you want to delete the endpoint and all of the FHIR data, use the `Delete a FHIRServer Endpoint` option.

### Delete a FHIRServer Endpoint

Deletes a FHIR server endpoint and deletes the endpoint’s FHIR data. If you want to delete the endpoint, but retain the FHIR data that has been collected by the endpoint, use the `Decommission a FHIRServer Endpoint` option.

### Update the CapabilityStatement Resource

Updates the Capability Statement of the FHIR server. For more details, see Modifying the Capability Statement.

### Index new SearchParameters for an Endpoint

When you add new search parameters to an existing endpoint using a published or custom package, FHIR clients can use the new parameter to retrieve resources added to the repository after you applied the package. However, resources that existed before you added the new search parameter will not be returned until you re-index the endpoint. If an endpoint has collected a large volume of FHIR data, this option can take a long time to run as it re-processes all existing resources.

### Upload a FHIR metadata package

Used to import a FHIR package of JSON files that define conformance resources. You must use this option before the package can be applied to an endpoint. For information about preparing a custom FHIR package for uploading, see Creating a Custom Package.

### Delete a FHIR metadata package

Deletes a package from the list of available packages that can be applied to an endpoint. This does not delete the FHIR package’s JSON files from your local system. You cannot delete packages that have been applied to an endpoint.
