# FHIR Profiles and Adaptations

The HL7 FHIR standard is intended to be adapted for specific healthcare environments and implementations. At the core of these adaptations are FHIR profiles, which define the allowable fields of a specific resource. These profiles extend or constrain the resource definitions that are found in the base FHIR specification. Profiles and other FHIR artifacts are achieved through conformance resources; for example, profiles are defined by StructureDefinition resources, search parameters are defined by SearchParameter resources, codes are defined by ValueSet and CodeSystems resources, and so on.

In most cases, a complete, robust FHIR adaptation is defined by an Implementation Guide, which is a coherent collection of conformance resources that includes documentation explaining the adaptation-specific profiles and other artifacts. Most commonly, these Implementation Guides are distributed as NPM-like packages that are downloadable from distribution sites. In InterSystems products, you control what a FHIR server supports by adding a FHIR package of conformance resources to an endpoint, even when the package does not contain an entire Implementation Guide.

An InterSystems FHIR endpoint can support multiple FHIR packages. For example, a FHIR endpoint can support the package of the US Core Implementation Guide while simultaneously supporting a unique Patient profile or search parameter from a custom package. This allows FHIR clients to search and use resources that conform to all of the supported packages.

In adherence to the FHIR specification, an InterSystems FHIR server does not automatically verify whether a resource that it receives from a FHIR client conforms to a supported profile. The FHIR client asserts that a resource conforms to one or more profiles using the `meta` element of the resource, but the FHIR server does not check whether that assertion is true. A FHIR client can use the `_profile` search parameter to retrieve resources that claim to conform to a profile.

Because FHIR servers support variations of the core FHIR specification, it is important that FHIR clients be able to determine exactly what is acceptable and possible with the FHIR server. To meet this need, every FHIR server must provide a Capability Statement that identifies the APIs, FHIR operations, search parameters, and resources that it supports. FHIR clients can retrieve this Capability Statement with a call to `GET [EndpointBaseURL]/metadata`.

## Working with FHIR Packages

Within InterSystems products, a FHIR package is a collection of conformance resources, like StructureDefinitions and SearchParameters. In this way, packages contain the profiles for a healthcare environment. A package can contain the standard conformance resources for a version of FHIR or it can extend or constrain a version of FHIR for a specific purpose. These packages are distributed and imported as NPM packages of JSON files. The contents of a package can vary widely; it can be used to distribute a national Implementation Guide (for example, US Core) or be limited to a Patient profile that is unique to a health network. In some cases, you might need to configure an endpoint using a standard, published package that can be downloaded from a distribution site. In other cases, you might develop your own package that contains custom profiles and search parameters.

If you need to work with packages programmatically, see Package APIs.

### Creating Custom Packages

You can use a custom package to configure your FHIR endpoint to support a custom profile or search parameter. For example, to add a custom search parameter, define a SearchParameter resource in a JSON file on your local machine. Then, create a file called package.json in the same directory. At a minimum, this file must include the name, version, and dependencies of the package. For example, the package.json file might look like:

```
{
  "name":"myorg.implementation.r5",
  "version":"0.0.1",
  "dependencies": {
    "hl7.fhir.r5.core":"5.0.0"
  }
}
```

Once you have JSON files with conformance resource definitions and a package.json file in a directory, you are ready to import the new package.

### Applying Packages to an Endpoint

When you create a new FHIR endpoint, you can select a set of packages that the endpoint will support. Only those packages that have been imported are available when creating the endpoint; InterSystems products come with a few published packages already imported.

You can also apply new packages to an existing endpoint. To add a package to an existing endpoint:

1.  In the Management Portal, navigate to `Home` > `Health` > `[MyFHIRNamespace]` > `FHIR Server Management`.
    
2.  In the tile for the desired endpoint, open the menu and choose `Edit`.
    
3.  If this namespace contains packages appropriate for the selected server, the `Custom Packages` dropdown is displayed. For example, if only packages dependent on FHIR R4 are available, this dropdown does not appear on a server configured for FHIR R3 or R5.
    
    In the `Custom Packages` dropdown, select the desired packages. If you do not see a desired package in the list, make sure you have imported it.
    
    > **Note:**
    > 
    > Adding one or more packages to the set of custom packages that are enabled for an endpoint triggers the system to re-index search tables when you save your changes.
    
4.  Select `Save`.
    

### Package APIs

If your implementation needs to work with packages directly without using the user interface, you can leverage the following API methods.

#### Importing Packages

The InterSystems FHIR server uses packages to determine which FHIR profiles and other assets it supports. While InterSystems products come with pre-loaded packages that correspond to base FHIR versions and popular Implementation Guides, you can also import new packages by specifying a directory that contains the JSON files that define conformance resources like StructureDefinition and ValueSet. For more information about FHIR packages, see Working with Packages.

The API for importing a new package so it can be added to an endpoint is HS.FHIRMeta.Load.NpmLoader.importPackages(). For example, the following code would import a custom package:

```objectscript
 do ##class(HS.FHIRMeta.Load.NpmLoader).importPackages($lb("C:\fhir-packages\node_modules\myorg.fhir.myPackage\"))
```

#### Listing Available Packages

To obtain a list of the packages that have been imported into the namespace, use the HS.FHIRMeta.Storage.Package.GetAllPackages() method. For example, the following code displays the identifiers of the available packages:

```objectscript
 set packages = ##class(HS.FHIRMeta.Storage.Package).GetAllPackages()
 for i=1:1:packages.Count()
   { write packages.GetAt(i).id,! }
```

#### Specifying a Package when Creating an Endpoint

The `pPackageList` parameter of the `InstallInstance()` method allows you to specify the packages you want applied to a new endpoint. For more details, see installing a FHIR server programmatically.

#### Adding Packages to an Existing Endpoint

If you need to add a package to an existing endpoint, you can leverage the HS.FHIRServer.Installer.AddPackagesToInstance() method. Note that enabling a custom package on an existing endpoint triggers the system to re-index search tables.

#### Uninstalling a Package

You can use HS.FHIRMeta.Load.NpmLoader.UninstallPackage() to remove a package from the FHIR server’s namespace if it is not a dependency of another package and has not been applied to an existing endpoint. Uninstalling a package does not delete the local JSON files that were used to import the package. You can determine the id of the package you want to uninstall by Listing Available Packages. As an example, the call to uninstall a package might look like:

```objectscript
 do ##class(HS.FHIRMeta.Load.NpmLoader).UninstallPackage("myorg.r5@1.0.0")
```

## Custom Search Parameters

Adding a custom search parameter to an endpoint consists of creating a custom package with the SearchParameter resource and applying it to the endpoint. To complete the process:

*   Use a text editor or third-party tool to create a SearchParameter JSON file.
    
*   Put the JSON file and a `package.json` file into a file directory so it can be imported as a custom package. For details, see Creating Custom Packages.
    
*   Import the package.
    
*   Apply the package to your endpoint.
    
*   If you applied the package to an existing endpoint, the system will also re-index the endpoint.
    

## Extensions

The FHIR server accepts a resource with extensions as long as it is well-formed according to the syntax for extensions defined by the base FHIR specification. In adherence to the FHIR specification, the FHIR server does not automatically verify whether those extensions are valid or conform to the profile specified in the resource’s `meta` field.

For information about adding custom search parameters for an extension, see Custom Search Parameters.
