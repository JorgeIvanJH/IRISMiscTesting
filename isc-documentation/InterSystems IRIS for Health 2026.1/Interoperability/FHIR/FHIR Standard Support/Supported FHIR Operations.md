# Supported FHIR Operations

When using the Resource Repository storage strategy provided with the FHIR server, the server supports the following interactions and operations. If your custom FHIR server extends the Resource Repository, it also supports these interactions and operations by default. See also Supported FHIR Interactions.

For FHIR servers that use or extend the default Resource Repository, the following operations are supported:

<table><tr><th>Operation</th><th>Level of Support</th></tr><tr><td><code>$expand</code></td><td>Partially supported. See <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXFHIRSTD_operations#HXFHIRSTD_operations_expand">Details of $expand Support</a>.</td></tr><tr><td><code>$everything</code></td><td><p>Fully supported for Patient and Encounter.</p><p>Not supported for EpisodeOfCare, Group, MedicinalProduct, or MedicinalProductDefinition.</p></td></tr><tr><td><code>$find</code></td><td>Fully supported</td></tr><tr><td><code>$lastn</code></td><td>Fully supported</td></tr><tr><td><code>$update-functional</code></td><td>Not part of the FHIR specification. See <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXFHIRSTD_operations#HXFHIRSTD_operation_functional_lists">Working With Functional Lists</a> for details.</td></tr><tr><td><code>$validate</code></td><td>Partially supported. See <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXFHIRSTD_operations#HXFHIRSTD_operation_validate">FHIR Profile Validation</a>.</td></tr></table>

> **Note:**
> 
> For FHIR servers developed using InterSystems IRIS for Health 2019.4 or earlier, the data in the old Resource Repository must be migrated before using the new FHIR server architecture.
> 
> See Migrating Data from a Pre–2020.1 Resource Repository

## Details of $expand Support

The `$expand` operation allows you to retrieve a ValueSet resource that is a subset of a given CodeSystem or ValueSet, based on a set of predefined criteria. The output ValueSet could include expanded details. For example, given a CodeSystem that includes insurance codes for pharmaceuticals, you could specify a value set to retrieve a list of medications appropriate for children suffering from acute allergies. The output might list the matching medical codes, along with the chemical name and brand names associated with each medication.

The `$expand` operation is partially supported, as follows:

*   Only the `URL`, `ValueSet`, and `ValueSetVersion` input parameters are supported.
    
*   The `generalizes`, `child-of`, and `descendent-leaf` filter operators are not supported.
    
*   The regular FHIR REST API read function for CodeSystem or ValueSet is only supported for ValueSet, and only for the purpose of supporting the `GET baseURL/ValueSet/id/$expand` use case. In order to use the read function in this way, you must first populate the ValueSet resources into your FHIR repository.
    

For additional information, see the HL7 FHIR specification for $expand.

## Working with Functional Lists

A functional list, also called a current resource list, is a List resource populated with the subset of relevant information that is currently in use. For example, a patient’s `$current-problems` functional list includes only those injuries and illnesses that the patient is currently suffering; this list would not include illnesses and injuries from which the patient has fully recovered. Each functional list is specific to a particular subject resource, often a Patient. For full details about functional lists, see the FHIR specification.

> **Note:**
> 
> The particular functional lists that your FHIR server recognizes are defined in the `Functional List Configuration` field in the `Interactions Strategy Settings` section of the server settings. By default, the following functional lists are defined: `$current-problems`, `$current-medications`, `$current-allergies`, `$current-drug-allergies`. If you wish to work with a functional list that is not defined for the server, you must first add it to the `Functional List Configuration` field.

The `$update-functional` operation facilitates creation and updating of functional lists.

To update a particular functional list, use `$update-functional` in a POST query, specifying the target functional list name in the URL, and including the desired contents of the List resource in the request body, either directly as a standalone List resource or encased in a Parameters resource. If the specified List resource already exists, it will be replaced with the List resource you sent in the request body. If the specified List resource does not yet exist, it will be created with the contents of the List resource you sent.

For example:

```
POST [base]/List/$update-functional?for=[subject_resource_id]&name=[functional_list_name]

In the request body:
{
  "resourceType": "List",
     ...
  "entry": [
      {
        "item": {
           "reference": "Condition/7"
        }
      },
      {
        "item": {
           "reference": "Condition/17"
        }
      },
      {
        "item": {
           "reference": "Condition/20"
        }
      }
    ]
...
}
```

### subject_resource_id

The resource ID of the functional list’s subject. For example, if the functional list being updated is the `$current-problems` list for Patient/123, `subject_resource_id` would be 123, and the syntax would be `for=123`.

### functional_list_name

Set the name parameter equal to the desired functional list name. The initial $ must be escaped using a \ character. For example `name=\$current-problems`

## Operation Query Parameters

For specific operations, certain operation query parameters are supported:

<table><tr><th>Operation</th><th>Query Parameter</th></tr><tr><td><code>$everything</code></td><td><ul><li><p><code>_since</code> is supported for Patient and Encounter, and accepts a dateTime value.</p></li><li><p><code>_type</code> is supported for Patient and Encounter. See “<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXFHIRSTD_operations#HXFHIRSTD_operation_query_parameters_type">Recursive Behavior of the _type Operation Query Parameter for $everything</a>” for details.</p></li></ul></td></tr><tr><td><code>$lastn</code></td><td><code>max</code> is supported.</td></tr></table>

### Recursive Behavior of the _type Operation Query Parameter for $everything

When a list of resource types is provided in the `_type` query parameter for the `$everything` operation, the compartment search will return only resources of the type listed. Recursive resource reference retrieval in the compartment will skip over references to resource types that are not specified in the `_types` parameter. Some examples illustrate how the `_type` query parameter for `$everything` operates on the Patient compartment:

1.  `/Patient/123/$everything?_type=DiagnosticReport,Observation` — returns DiagnosticReport and Observation resources but not the Patient resource.
    
2.  `/Patient/123/$everything?_type=Observation` — returns the patient's Observation resources, even though the referring DiagnosticReport resources are not included, because Observation is also in the Patient compartment.
    
3.  `/Patient/123/$everything?_type=Practitioner` — returns nothing. Practitioner is not in the Patient compartment, and no other resource type that could refer to Practitioner was specified.
    
4.  `/Patient/123/$everything?_type=Patient,DiagnosticReport,Practitioner` — returns the Patient resource, all of the DiagnosticReport resources, and only the Practitioner resources directly referred to by the returned DiagnosticReport resources.
    

## FHIR Profile Validation

> **Note:**
> 
> Profile validation is currently designed to work only with FHIR version R4. Later releases will target R5.

InterSystems IRIS for Health supports profile validation by implementing part of the FHIR standard for the `$validate` operation, which checks a resource against the most recent version of a specified profile.

> **Note:**
> 
> Although the standard allows use of a snapshot or a differential, profile validation provided by InterSystems IRIS for health requires the use of a snapshot.

The following query syntax options are supported:

*   You can specify the profile in the query URL:
    
    <table><tr><td>Query URL</td><td><code>POST &lt;FHIR Endpoint&gt;/&lt;Resource Type&gt;/$validate?profile=&lt;Profile URL&gt;|&lt;Profile Version Number&gt;</code></td></tr><tr><td>Body</td><td>Resource details in XML or JSON format</td></tr></table>
    
    `<Profile Version Number>` is required. Note that the character separating `<Profile URL>` from `<Profile Version Number>` is a pipe, not a slash.
    
*   You can provide the profile in the query body, optionally specifying a supported mode:
    
    <table><tr><td>Query URL</td><td><code>POST &lt;FHIR Endpoint&gt;/&lt;Resource Type&gt;/&lt;Optional Resource ID&gt;/$validate</code></td></tr><tr><td>Body</td><td>A <code>Parameters</code> block, which must include the resource details, and which may include the mode and a profile, in XML or JSON format.</td></tr></table>
    
    Providing a profile is optional. If no profile is provided, validation is performed based on the core schema for the resource type.
    
    `<Optional Resource ID>` may be required or forbidden, based on the value of the `mode` parameter, as follows:
    
    <table><tr><td>Value of mode</td><td>ID Required?</td><td>Checks Performed by $validate</td></tr><tr><td><code>create</code></td><td>Forbidden</td><td><code>$validate</code> operation confirms that no resource ID is included, and compares the potential new resource to the profile or the core schema for the resource type, if no profile is provided.</td></tr><tr><td><code>update</code></td><td>Required</td><td><code>$validate</code> operation checks that a resource ID is included in the request URL and matches the ID in the query body, that the resource URL resource type matches the resource included in the query body, and compares the potential outcome of the update to the profile or the core schema for the resource type, if no profile is provided.</td></tr><tr><td><code>delete</code></td><td>Required</td><td><code>$validate</code> operation checks to ensure that a resource ID is included in the request URL. This ID is required for the deletion operation, but no profile validation occurs.</td></tr><tr><td><code>profile</code></td><td>Required</td><td><code>$validate</code> operation checks to ensure that a resource ID is included in the request URL, and that a profile is specified either in the request body (in a <code>Parameters</code> resource) or as a query parameter in the request URL.</td></tr><tr><td>unspecified</td><td>Forbidden</td><td><code>$validate</code> operation checks the resource in the query body against the profile or the core schema for the resource type, if no profile is provided.</td></tr></table>
