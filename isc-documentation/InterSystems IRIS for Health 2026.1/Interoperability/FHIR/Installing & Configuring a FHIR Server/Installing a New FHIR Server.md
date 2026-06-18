# Installing a New FHIR Server

> **Important:**
> 
> Before you install a FHIR server, consider whether you want to customize it now or in the future. In many cases, a FHIR server using the Resource Repository cannot be customized unless you subclass the InteractionsStrategy before you create the endpoint.
> 
> For example, modifying how bundles are processed or post-processing search results requires that you subclass the Resource Repository. For information about preparing for these customizations before installing the FHIR server, see Pre-Installation Subclassing.
> 
> In a HealthShare ODS, always use the `HS.ODS.FHIR.Storage.InteractionsStrategy`. Customizing the InteractionsStrategy is not supported with the ODS.

To install a new FHIR server:

*   Use the FHIR Server Management page
    
*   Use the OAuth FHIR Client Quickstart menu
    
*   Install a FHIR server programmatically using an ObjectScript API
    
*   Install a FHIR server using the FHIR Server Management REST API
    
*   Install a FHIR server using the command-line interface
    

> **Note:**
> 
> If you plan to mirror your FHIR server, see Configuring Mirroring for Healthcare Products for special instructions.

In all cases, consult the namespace requirements for a FHIR server before you begin.

## Namespace Requirements For Installing A New FHIR Server

Before you install a new FHIR server, confirm that you have satisfied the following namespace requirements:

*   To install a FHIR server, you must have a health care interoperability-enabled namespace:
    
    *   In IRIS for Health and Health Connect, this means that you must have a Foundation namespace. If you do not already have one, follow the procedure to create and activate a Foundation namespace before you begin. When creating your Foundation namespace, if you plan to mirror the database that includes your FHIR server, see Configuring Mirroring for Healthcare Products for special instructions.
        
    *   In a HealthShare context, the ODS namespace is enabled for health care interoperability.
        
*   The user that installs or configures a FHIR server must have the `%HSAdmin_InstallationManagement` resource and the `%HS_DB_{NAMESPACE}` role assigned for the namespace.
    

> **Note:**
> 
> You can install more than one FHIR server in a particular namespace.

## Installing a New FHIR Server from FHIR Server Management

The `FHIR Server Management` page allows you to install a new FHIR server. A FHIR server must be first be installed, only then can it be configured.

To install a new FHIR server:

1.  Confirm that you have met the namespace requirements.
    
2.  Open the `FHIR Server Management` page.
    
    Either of the following paths in the Management Portal will take you to the page:
    
    *   Navigate to `Home` > `Health` (or `Home` > `HealthShare`) and click `FHIR` in the banner.
        
    *   Navigate to `Home` > `Health` > `healthNamespace` > `FHIR Server Management`.
        
        Where `healthNamespace` is your healthcare-enabled namespace.
        
3.  Click the `+ Add new server` tile.
    
4.  Fill out the basic configuration pane as follows:
    
    ### Namespace
    
    Select the name of your healthcare-enabled namespace from the dropdown.
    
    ### Name
    
    Enter a name for your new FHIR server. `Name` is a required field when configuring a FHIR server on the `FHIR Server Management` page.
    
    ### FHIR Version
    
    Select a core FHIR package from the `FHIR Version` dropdown.
    
    Each package corresponds to a version of the HL7 FHIR standard. So, for example, to configure a FHIR endpoint that supports FHIR R5, select the `hl7.fhir.r5.core@5.0.0` package.
    
    Choosing the core FHIR package automatically populates the `URL` field with an appropriate endpoint.
    
    > **Note:**
    > 
    > For a FHIR server installed in a HealthShare FHIR Gateway or ODS namespace, select only STU3 or R4. The SDA-to-FHIR transformation set for R5 is not complete enough to achieve consistent results on the breadth of data stored in Unified Care Record.
    
    ### URL
    
    An endpoint `URL` is automatically generated when you choose a FHIR version. You can edit the endpoint’s URL if desired, but ensure that it begins with a forward-slash (`/`).
    
    ### Custom Packages
    
    From the dropdown, select any custom packages that you want your endpoint to support.
    
    *   For more information about packages in the HealthShare ODS, see Profiles and FHIR Adaptations.
        
    *   For more information about packages in IRIS for Health and Health Connect, see Profiles and FHIR Adaptations.
        
    *   In particular, for information about managing packages programmatically, see Package APIs.
        
    
5.  Select a `Data Organization Strategy` and a database architecture.
    
    Expand the `Advanced Configuration` pane of the dialog and configure the following settings:
    
    > **Note:**
    > 
    > Additional configuration options become available in the `Advanced Configuration` pane once you complete the FHIR server installation procedure.
    
    ### Data Organization Strategy
    
    Select an interaction strategy from the dropdown.
    
    If you created a custom interaction strategy, it should appear in the dropdown for you to select.
    
    *   For IRIS for Health and Health Connect, the default interaction strategy is HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy, which stores FHIR data as JSON in dynamic objects.
        
    *   In a HealthShare ODS, always select `HS.ODS.FHIR.Storage.InteractionsStrategy`.
        
    *   In a HealthShare FHIR Gateway, always select `HS.FHIRGateway.Storage.InteractionsStrategy`.
        
    *   For InterSystems Payer Services, always select `HS.FHIRGateway.Storage.InteractionsStrategy`.
        
    
    ### Use Namespace default database
    
    Each FHIR server has a resource database and a resource history database. The default location for each of these databases is in a subfolder of the `/mgr/` folder of your installation. If you select this checkbox, you can enter a custom location for each database in the `Resource Database Location` and `Resource History Database Location` fields.
    
    ### Resource Database/Resource History Database
    
    If you did not select the default location for the FHIR server’s databases, edit the locations indicated in the `Resource Database Location` and `Resource History Database Location` fields. The resource history database contains previous versions of a resource; because these are not accessed as frequently, you could put this database on a slower, less expensive disk.
    
6.  Select your `Interaction Strategy Settings`.
    
    Which options appear under `Interaction Strategy Settings` in the `Advanced Configuration` pane depend upon which interaction strategy you selected under Data Organization Strategy. The list below describes the options available across all interaction strategies. You may see only a subset of these options in your FHIR server.
    
    Select values for the options that appear in the dialog, which may include:
    
    ### SMART on FHIR Capabilities
    
    Specify the server’s SMART on FHIR capabilities by entering them as a comma-delimited list into this field. This list does not control the functionality of the endpoint; rather, it specifies the capabilities that are returned in the JSON document when a client appends `/.well-known/smart-configuration` to the endpoint’s URL. For example:
    
    ```
    launch-ehr, context-ehr-patient, permission-patient, client-public, client-confidential-symmetric
    ```
    
    For more details about SMART on FHIR capabilities retrieved with Well-Known URIs, see FHIR Authorization Endpoint and Capabilities Discovery using Well-Known Uniform Resource Identifiers (URIs).
    
    ### Silence search parameter indexing errors
    
    Select this option to prevent search parameter indexing errors from aborting FHIR resource save.
    
    > **Caution:**
    > 
    > Enable this setting only when strictly necessary.
    
    ### Prematurely limit the number of resources...with _max_results
    
    Select this option to make FHIR search queries more efficient by adding a SQL operation `TOP N` where `N` is the value of the `_maxresults` search result parameter.
    
    > **Caution:**
    > 
    > Use this setting only if you do not have `PostProcessSearch()` logic, since post processing filters could remove some or all of the hits from the results set, leading the query to return a number of hits fewer than `_maxresults`.
    > 
    > Refer to the hovertext for the field on the `FHIR Server Management` page for additional discussion of the trade-offs in selecting this option.
    
    ### Disable FHIR Audit
    
    Select this option to disable FHIR auditing for this endpoint.
    
    ### Functional List Configuration
    
    > **Note:**
    > 
    > The Functional List Configuration field displays only for FHIR endpoints that use or extend the HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy data organization strategy.
    
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
    
7.  Click `Create` to create the server and its associated endpoint. To start over instead, click `Cancel`.
    

It takes several minutes to create a FHIR server. When the configuration is complete, additional configuration options relating to authorization and requests become available.

As part of creating a new FHIR endpoint, an external server named `FHIR_Validation_Server` is created to perform back-end functions related to profile validation.

> **Important:**
> 
> If you expect to post Bundles containing 10,000 or more entries, you should increase the value of the Web Gateway Server Response Timeout parameter to avoid server timeouts interrupting your data loads.

## Installing a New FHIR Server Programmatically

An application can install a FHIR server programmatically using an ObjectScript API that requires two methods to be called in succession. After you have installed you FHIR server, you can then configure it.

> **Note:**
> 
> You can also install a FHIR server programmatically using the FHIR Server Management REST API.

To install a FHIR server programmatically using the ObjectScript API:

1.  Confirm that you have met the namespace requirements.
    
2.  Prepare the Foundation namespace by calling the following method of HS.FHIRServer.Installer:
    
    ### InstallNamespace()Opens in a new tab
    
    Prepares an existing foundation namespace for the FHIR server by installing elements that make the namespace FHIR-enabled.
    
    If you call the method without an argument, the installer assumes that the active namespace is a foundation namespace and prepares it for the FHIR server.
    
    > **Note:**
    > 
    > This method does not create a new Foundation namespace.
    
3.  Change to your FHIR-enabled namespace.
    
4.  Install the FHIR Service into the current, FHIR-enabled namespace by calling the following method of HS.FHIRServer.Installer:
    
    ### InstallInstance()Opens in a new tab
    
    Installs an instance of a FHIR Service into the current namespace.
    
    This method requires the following arguments:
    
    *   Unique URL of the FHIR endpoint. Be sure the URL begins with a slash (`/`).
        
    *   Classname of the FHIR server’s InteractionsStrategy.
        
    *   List of FHIR packages, for example, the package for an Implementation Guide like US Core.
        
        The `pPackageList` parameter of InstallInstance() accepts a list of FHIR packages that have been loaded into the system. Often, a package corresponds to a specific Implementation Guide, but can also be the core metadata for a version of FHIR. By passing a list of packages to `InstallInstance`, you can configure an endpoint to support one or more packages. For more about packages, see Profiles and FHIR Adaptations.
        
        To obtain a list of the packages that can be passed into the `pPackageList` parameter, use the GetAllPackages() method in HS.FHIRMeta.Storage.Package. For example, the following code displays the identifiers of the available packages
        
        ```objectscript
         set packages = ##class(HS.FHIRMeta.Storage.Package).GetAllPackages()
         for i=1:1:packages.Count()
           { write packages.GetAt(i).id,! }
        ```
        
        The result might look like:
        
        ```
        hl7.fhir.r5.core@5.0.0
        hl7.fhir.r4.core@4.0.1
        hl7.fhir.us.core@3.1.0
        hl7.fhir.r3.core@3.0.2
        ```
        
        Pass in the appropriate package identifiers as arguments to the `pPackageList` parameter of InstallInstance() using `$lb`. For example:
        
        ```objectscript
         Do ##class(HS.FHIRServer.Installer).InstallInstance(
                    myURL,
                    strategyClass,
                    $lb("hl7.fhir.r5.core@5.0.0"))
        ```
        
        For details about the APIs used to create FHIR packages, see Package APIs.
        
    
    There are also optional parameters that can be passed to the method. For complete details on these optional parameters, see InstallInstance() in the class reference.
    

### Programmatic FHIR Server Installation Example

The following ObjectScript code example creates a Foundation namespace called “FHIRNamespace” and then installs a FHIR server that supports one package and uses the default storage strategy (Resource Repository).

```objectscript
 Set appKey = "/myfhirserver/fhir/r5"
 Set strategyClass = "HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy"
 Set metadataPackages = $lb("hl7.fhir.r5.core@5.0.0")

 //Install a Foundation namespace and change to it
 Do ##class(HS.Util.Installer.Foundation).Install("FHIRNamespace")
 Set $namespace = "FHIRNamespace"

 // Install the elements that are required for a FHIR-enabled namespace
 Do ##class(HS.FHIRServer.Installer).InstallNamespace()

 // Install an instance of a FHIR Service into the current namespace
 Do ##class(HS.FHIRServer.Installer).InstallInstance(appKey, strategyClass, metadataPackages)
```

## Installing a FHIR Server Using Command Line Options

You can use a command line interface to install a new FHIR server. A FHIR server must be first be installed, only then can it be configured.

To install a new FHIR server using the command line interface:

1.  Confirm that you have met the namespace requirements.
    
2.  Open the InterSystems Terminal and change to your foundation namespace.
    
3.  Run the following command:
    
    ```objectscript
     do ##class(HS.FHIRServer.ConsoleSetup).Setup()
    ```
    
4.  Choose `Create FHIRServer Endpoint` and then answer the questions as described in the following steps.
    
5.  `Choose the Storage Strategy`
    
    `Json` is the Resource Repository.
    
6.  `Choose the FHIR version for this endpoint`
    
    Select the version of the core FHIR specification that your endpoint supports.
    
7.  `Enter any package numbers`
    
    Packages that have been imported are listed as possibilities. The endpoint can support multiple packages; to specify more than one package, separate the numbers by commas. You can add additional packages later, but you might need to run additional steps if you wait. Use the `Upload a FHIR Metadata Package` option to add a package to the list.
    
8.  `Do you want to create the default repository endpoint?`
    
    Press `Enter` if you want to accept the default URL of the endpoint. If you want your endpoint to have a different URL, specify `N`, and enter the URL (be sure the URL begins with a slash).
    
9.  `Enter the OAuth Client Name for this Endpoint`
    
    If you are using OAuth 2.0 to secure the endpoint, enter the `Client Name` of the FHIR server. (From the point of view of an OAuth 2.0 authentication server, the FHIR server is a client whose type is a resource server.) For more information, see Using OAuth 2.0 with a FHIR Server.
    
10.  `Do you want to create separate database files for your FHIR data?`
     
     If you specify `yes`, FHIR data for the endpoint is stored separately from the FHIR data of other endpoints in the same namespace. If you specify `no`, all FHIR data is stored in the namespace’s database files, even if you have multiple endpoints. If you are creating separate database files, you can accept the default locations or specify alternate locations. The Versions Database contains previous versions of a resource; because these are not accessed as frequently, you could put the Versions Database on a slower, less expensive disk.
     

Console Setup also includes additional options to configure an existing FHIR server using the command line.
