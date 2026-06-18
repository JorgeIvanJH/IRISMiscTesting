# Supported FHIR Interactions

When using the Resource Repository storage strategy provided with the FHIR server, the server supports the following interactions and operations. If your custom FHIR server extends the Resource Repository, it also supports these interactions and operations by default.

HL7 FHIR interactions are the set of actions that a FHIR client can take on resources. These interactions can be grouped according to whether they act upon an instance, a type, or the whole system. An instance is a specific instance of a resource, for example, `Patient/1` refers to an instance of a Patient resource with an `id` of `1`. A type refers to a particular FHIR resource, for example, a Patient or Observation.

The following table summarizes the support for FHIR interactions in the Resource Repository, or a custom FHIR server that has extended the Resource Repository. Click on an interaction to see how it is defined in the HL7 REST API and how to use it.

<table><tr><th>Interaction</th><th>Level of Support</th></tr><tr><td><a href="https://www.hl7.org/fhir/http.html#create">create</a></td><td>Fully supported, including conditional create.</td></tr><tr><td><a href="https://www.hl7.org/fhir/http.html#read">read</a></td><td>Conditional read is not supported.</td></tr><tr><td><a href="https://www.hl7.org/fhir/http.html#vread">vread</a></td><td>Conditional read is not supported.</td></tr><tr><td><a href="https://www.hl7.org/fhir/http.html#update">update</a></td><td>Fully supported, including conditional update.</td></tr><tr><td><a href="https://www.hl7.org/fhir/http.html#patch">patch</a></td><td>Supported for JSON patch documents only. Conditional patch is supported.</td></tr><tr><td><a href="https://www.hl7.org/fhir/http.html#delete">delete</a></td><td>Fully supported, including conditional delete.</td></tr><tr><td><a href="https://www.hl7.org/fhir/http.html#history">history</a></td><td><p>Supported for instance interactions only, not type or system. For example, <code>GET [baseURL]/Patient/1/_history</code> is supported, but not <code>GET [baseURL]/Patient/_history</code> or <code>GET [baseURL]/_history</code>.</p><p>The <code>_count</code> and <code>_at</code> parameters are not supported.</p><p>Paging is not supported.</p></td></tr><tr><td><a href="https://www.hl7.org/fhir/http.html#transaction">batch</a></td><td>Fully supported</td></tr><tr><td><a href="https://www.hl7.org/fhir/http.html#transaction">transaction</a></td><td>Circular references within the bundle are not supported.</td></tr><tr><td>search</td><td>Supported with some limitations. For details, see <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXFHIRSTD_interactions#HXFHIRSTD_search">FHIR Search Interaction</a>.</td></tr></table>

The Search Interaction

FHIR clients use the search interaction to retrieve resources from the Resource Repository. For full details about the search interaction, refer to FHIR specification. The sections below summarize the default support for the search interaction when the FHIR server is using or extending the Resource Repository:

*   Searching for Resources of Multiple Types
    
*   Search Parameter Types
    
*   Parameters
    
*   Modifiers
    
*   Prefixes
    
*   Search Result Parameters
    

## Searching for Resources of Multiple Types

The resource repository supports searching for resources of multiple types in the following contexts:

### System-level Search

If you search without specifying one particular compartment or resource type, your search will potentially look at all resources in the repository.

The generic format for system-level searching is `GET [base]?[parameter_list]`

For example, to search for all resources updated since January 29, 2025:

```
GET [base]?_lastUpdated=ge2025-01-29
```

To search for multiple resource types at the System level, you can search a specified set of resource types by using `_type`; in this case, all parameters must be common to all specified types. If you do not specify a set of resource types using `_type`, resources of all types will be searched; in this case all parameters must be supported by all resource types.

For example, because both the MedicationRequest and MedicationDispense resources support the `medication` parameter, you can search for all MedicationRequest and MedicationDispense resources that have a relationship to a specific medication:

```
GET [base]?_type=MedicationRequest,MedicationDispense&medication=Medication/med1
```

### Compartment-level Search

You can search within a specific resource compartment, a logical structure that identifies all resources related to a particular Patient, Encounter, RelatedPerson, Practitioner, or Device resource. Compartments can streamline searching.

The generic format for compartment-level searching is `GET [base]/[compartment_type]/[compartment_ID]/[type]?[parameter_list]`

To search for multiple resource types within the same compartment, you can use the wildcard character (*) in the `[type]` position of the query URL, and you can use the `$everything` operation:

*   A simple example of how to use the wildcard character: `GET [base]/Patient/100000001/*` returns all resources in the compartment.
    
*   You can also use the wildcard character in conjunction with any search parameters common to all the resource types the search is targeting. This is especially useful if you use the `_type` parameter. For example: `GET [base]/Patient/100000001/*?status=final&_type=Observation,DiagnosticReport` is supported because both the Observation and DiagnosticReport resource type include the `status` element. This query searches all Observation and DiagnosticReport resources associated with the specified patient, and returns those that are in final status.
    
*   The wildcard syntax provides a different result than the `$everything` operation. `GET [base]/Patient/100000001/*` returns any and all resources associated with the specified Patient—including, for example, a Patient’s DiagnosticReport resources. By contrast, `GET [base]/Patient/100000001/$everything` returns all resources associated with the Patient resource as well as resources associated with those resources. Compared with the previous search, this search would also include Practitioner resources associated with the Patient’s DiagnosticReport resources.
    

> **Note:**
> 
> *   For detailed information about the `_type` parameter, see the FHIR specification.
>     
> *   By definition, searching in the Type context searches against a single specified resource type.
>     

## Search Parameter Types

Each search parameter has a search parameter type that determines how the parameter behaves.

<table><tr><th>Parameter Type</th><th>Level of Support</th></tr><tr><td><a href="https://www.hl7.org/fhir/search.html#composite">composite</a></td><td>Not supported</td></tr><tr><td><a href="https://www.hl7.org/fhir/search.html#date">date</a></td><td>Fully supported</td></tr><tr><td><a href="https://www.hl7.org/fhir/search.html#number">number</a></td><td>Fully supported</td></tr><tr><td><a href="https://www.hl7.org/fhir/search.html#quantity">quantity</a></td><td>Fully supported</td></tr><tr><td><a href="https://www.hl7.org/fhir/search.html#reference">reference</a></td><td>Fully supported</td></tr><tr><td><a href="https://www.hl7.org/fhir/search.html#string">string</a></td><td>Fully supported</td></tr><tr><td><a href="https://www.hl7.org/fhir/search.html#token">token</a></td><td>Fully supported</td></tr><tr><td><a href="https://www.hl7.org/fhir/search.html#uri">uri</a></td><td>Fully supported</td></tr></table>

In addition to the reference search functionality described in the FHIR specification, chained search is supported for canonical references, including the use of the `_include` and `_revinclude` search result parameters.

## Search Parameters

The following summarizes FHIR server support for standard search parameters when retrieving resources from the Resource Repository.

<table><tr><th>Parameter</th><th>Level of Support</th></tr><tr><td><code>_content</code></td><td>Not supported</td></tr><tr><td><code>_filter</code></td><td>Not supported</td></tr><tr><td><code>_has</code></td><td>Fully supported as described in the <a href="https://www.hl7.org/fhir/search.html#has">official specification</a></td></tr><tr><td><code>_id</code></td><td>Fully supported as described in the <a href="https://www.hl7.org/fhir/search.html#id">official specification</a></td></tr><tr><td><code>_lastUpdated</code></td><td>Fully supported as described in the <a href="https://www.hl7.org/fhir/search.html#lastUpdated">official specification</a></td></tr><tr><td><code>_list</code></td><td>Fully supported for Type-level search and Type-level + functional list search as described in the <a href="https://hl7.org/fhir/search.html#_list">official specification</a>. Supported for system-level search only when the <code>_list</code> value is a resource ID. (For example, system-level search on a functional list, which requires a scoping search parameter, is not supported)</td></tr><tr><td><code>_profile</code></td><td>Fully supported as described in the <a href="https://www.hl7.org/fhir/search.html#profile">official specification</a></td></tr><tr><td><code>_query</code></td><td>Not supported</td></tr><tr><td><code>_security</code></td><td>Fully supported as described in the <a href="https://www.hl7.org/fhir/search.html#security">official specification</a></td></tr><tr><td><code>_source</code></td><td>Fully supported</td></tr><tr><td><code>_tag</code></td><td>Fully supported as described in the <a href="https://www.hl7.org/fhir/search.html#tag">official specification</a></td></tr><tr><td><code>_text</code></td><td>Not supported</td></tr><tr><td><code>_type</code></td><td>Fully supported as described in the <a href="https://www.hl7.org/fhir/search.html#_type">official specification</a>.</td></tr></table>

## Modifiers in Search

Modifiers can be added to the end of a parameter to affect the results of the search.

<table><tr><th>Modifier</th><th>Level of Support</th></tr><tr><td><code>:above</code></td><td>Supported for URI</td></tr><tr><td><code>:below</code></td><td>Supported for URI</td></tr><tr><td><code>:code-text</code></td><td>Not supported</td></tr><tr><td><code>:contains</code></td><td>Fully supported (strings and URIs)</td></tr><tr><td><code>:exact</code></td><td>Fully supported</td></tr><tr><td><code>:identifier</code></td><td>Fully supported</td></tr><tr><td><code>:in</code></td><td>Not supported</td></tr><tr><td><code>:iterate</code></td><td>Fully supported</td></tr><tr><td><code>:missing</code></td><td>Fully supported</td></tr><tr><td><code>:not</code></td><td>Fully supported</td></tr><tr><td><code>:not-in</code></td><td>Not supported</td></tr><tr><td><code>:of-type</code></td><td>Fully supported</td></tr><tr><td><code>:text</code></td><td>Supported for references and tokens, not supported for strings</td></tr><tr><td><code>:text-advanced</code></td><td>Not supported</td></tr><tr><td><code>:[type]</code></td><td>Fully supported</td></tr></table>

## Prefixes in Search

When using search parameters of type number, date, and quantity, you can add a prefix to the parameter’s value to affect what resources match the search. For example, `[parameter]=le100` returns values that are less than or equal to 100.

<table><tr><th>Prefix</th><th>Level of Support</th></tr><tr><td><code>eq</code></td><td>Fully supported</td></tr><tr><td><code>ne</code></td><td>Fully supported</td></tr><tr><td><code>gt</code></td><td>Fully supported</td></tr><tr><td><code>lt</code></td><td>Fully supported</td></tr><tr><td><code>ge</code></td><td>Fully supported</td></tr><tr><td><code>le</code></td><td>Fully supported</td></tr><tr><td><code>sa</code></td><td>Fully supported</td></tr><tr><td><code>eb</code></td><td>Fully supported</td></tr><tr><td><code>ap</code></td><td>Fully supported</td></tr></table>

## Search Result Parameters

Search result parameters help manage the resources returned by a search.

<table><tr><th>Search result parameter</th><th>Level of Support</th></tr><tr><td><code>_contained</code></td><td>Not supported</td></tr><tr><td><code>_containedType</code></td><td>Not supported</td></tr><tr><td><code>_count</code></td><td>Fully supported as described in the <a href="https://www.hl7.org/fhir/search.html#count">official specification</a></td></tr><tr><td><code>_elements</code></td><td>Fully supported as described in the <a href="https://www.hl7.org/fhir/search.html#elements">official specification</a></td></tr><tr><td><code>_graph</code></td><td>Not supported</td></tr><tr><td><code>_include</code></td><td>Fully supported as described in the <a href="https://www.hl7.org/fhir/search.html#include">official specification</a></td></tr><tr><td><code>_maxresults</code></td><td>Fully supported as described in the <a href="https://www.hl7.org/fhir/search.html#_maxresults">official specification</a>.<blockquote><strong>Note:</strong><p>Queries using this parameter can be made more efficient by setting the <code>Use TOP for _maxresults</code> FHIR configuration setting. See the table in <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXFHIRINS_server_install_configure">Configuring an Existing FHIR Server</a> for details and important considerations.</p></blockquote></td></tr><tr><td><code>_revinclude</code></td><td>Fully supported as described in the <a href="https://www.hl7.org/fhir/search.html#include">official specification</a></td></tr><tr><td><code>_score</code></td><td>Not supported</td></tr><tr><td><code>_sort</code></td><td>Fully supported as described in the <a href="https://www.hl7.org/fhir/search.html#sort">official specification</a></td></tr><tr><td><code>_summary</code></td><td>Supports <code>_summary=count</code>, <code>_summary=data</code>, and <code>_summary=text</code>. For details, see the <a href="https://www.hl7.org/fhir/search.html#summary">official specification</a>.</td></tr><tr><td><code>_total</code></td><td>Not supported</td></tr></table>

## Search in Legacy Resource Repositories

*   Search in legacy Resource Repositories older than 2024.1
    
*   Search in legacy Resource Repositories older than 2020.1
    

### Search in Legacy Resource Repositories Older than 2024.1

Prior to version 2024.1, the Resource Repository’s search interaction was implemented using a different search strategy. This legacy strategy is still supported in this version; however, the legacy strategy provides a limited set of features compared to the current strategy that is described here.

If you have upgraded an instance with a preexisting Resource Repository to this version from a version prior to 2024.1, see JSON Legacy SQL Strategy for a comparison of supported features and instructions for upgrading your Resource Repository from the legacy strategy to the current strategy.

### Search in Legacy Resource Repositories Older than 2020.1

For FHIR servers developed using InterSystems IRIS for Health 2019.4 or earlier, the data in the old Resource Repository must be migrated before using the new FHIR server architecture.

See Migrating Data from a Pre–2020.1 Resource Repository.
