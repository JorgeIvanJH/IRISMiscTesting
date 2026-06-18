# FHIRPath

FHIRPath is a language, similar to XPath, that allows you to navigate an HL7 FHIR resource to evaluate and extract data from its fields using a straightforward syntax that includes paths, functions, and operations. For example, you could evaluate whether the given name of a Patient contained a value: `Patient.name.given.empty()`. Or you could extract the value of the Patient resource’s `telecom` field, but only if `offical` is the value of its `use` field: `Patient.telecom.where(use = 'official')`.

In FHIRPath, expressions are collection-based. Each function works on one input collection and each binary operator operates on two input collections, and the values returned by the expression are gathered into an output collection. Some functions and operations place constraints on the size of their input collections.

For complete details about FHIRPath including how to build an expression, see the HL7 FHIRPath specification. InterSystems supports a subset of the functions and operations that are defined in the specification.

## Workflow

With InterSystems technology, the process of using FHIRPath to evaluate and extract data from a resource is straightforward:

[Image: Instantiate FHIRPath object, parse FHIRpath expression, evaluate a resource, and work with collection of results]

The following sections provide details about each step in the workflow.

1.  Instantiate HS.FHIRPath.API
    
2.  Parse the FHIRPath Expression
    
3.  Evaluate the Resource
    
4.  Work with the Results
    

Workflow examples:

*   evaluate() Method
    
*   evaluateArray() Method
    
*   evaluateToJson() Method
    

### Instantiate HS.FHIRPath.API

The process of using FHIRPath to evaluate and extract data from a resource begins with calling HS.FHIRPath.API.getInstance(). When you call this method, you must specify the FHIR package that corresponds to a version of FHIR. For example, if the resources you are evaluating conform to FHIR R4, the corresponding package ID is currently `hl7.fhir.r4.core@4.0.1`. In this case, instantiating HS.FHIRPath.API would look like:

```objectscript
 set fhirPathAPI = ##class(HS.FHIRPath.API).getInstance($lb("hl7.fhir.r4.core@4.0.1"))
```

You can obtain the IDs of the currently loaded packages using the Management Portal or ObjectScript:

*   Management Portal — Navigate to `Home` > `Health` > `MyFHIRNamespace` > `FHIR Configuration`, and select the `Package Configuration` card. The package ID is obtained by appending the `@` symbol and version number to the name of the package. For example, the ID of the following package is `hl7.fhir.r4.core@4.0.1`:
    
    [Image: name of FHIR package: hl7.fhir.r4.core]
*   ObjectScript — To list package IDs programmatically, see Listing Available Packages.
    

The HS.FHIRPath.API object includes the methods used to parse FHIRPath expressions and evaluate resources. This object is also included as a property on the HS.FHIRMeta.API object under the `FHIRPathAPI` property.

### Parse the FHIRPath Expression

Once you have instantiated the HS.FHIRPath.API object, you are ready to parse the FHIRPath expression. The method that parses the expression, HS.FHIRPath.API.parse(), returns a tree structure that is used by the methods that evaluate a resource. For example, assuming you have an object named `fhirPathAPI` instantiated as shown in the previous section:

```objectscript
 set tree = fhirPathAPI.parse("name.given.empty()")
```

### Evaluate the Resource

Once you have parsed the FHIRPath expression, you can use its tree structure to evaluate or extract data from a resource. Two evaluation methods are available:

*   HS.FHIRPath.API.evaluate() — The `evaluate()` method returns the results of the evaluation in a multidimensional array.
    
*   HS.FHIRPath.API.evaluateToJson() — The `evaluateToJson()` method returns the collection in a dynamic array.
    

In both cases, the resource being evaluated is passed into the method as a dynamic object. The tree that was returned by the `parse()` method is also passed as an argument. For example:

```objectscript
 set tree = fhirPathAPI.parse("name.given.empty()")
 // myResource is a dynamic object
 do fhirPathAPI.evaluate(myResource, tree, .OUTPUT)
 set DynArray = fhirPathAPI.evaluateToJson(myResource, tree)
```

An additional method, HS.FHIRPath.API.evaluateArray(), can be used to parse the multidimensional array returned by the `evalaute()` method.

### Work with the Results

While working with results in a dynamic array that is produced by `evaluateToJson()` has its benefits, the multidimensional array produced by `evaluate()` contains additional information that is not otherwise available. The following provides a guide to the data in the multidimensional array, assuming that your response to `evaluate()` was returned in a variable named `OUTPUT`.

<table><tr><th>Node</th><th>Description</th></tr><tr><td><code>OUTPUT</code></td><td>Number of nodes in the array that contain values.</td></tr><tr><td><code>OUTPUT(n)</code></td><td>Value of the <code>n</code>th element of the array.</td></tr><tr><td><code>OUTPUT(n,"t")</code></td><td>Data type of the <code>n</code>th element in the array, including identifying FHIR data types.</td></tr></table>

You can further parse the returned multidimensional array using the `evaluateArray()` method.

By contrast. when using the `evaluateToJson()` method to produce a dynamic array, you can determine whether the data type is a string, boolean, number, or object from looking at the values in the array, but you cannot determine the FHIR data type.

### Workflow Example: evaluate() Method

This example includes the resource being evaluated, the ObjectScript needed to evaluate the resource, and a look at the multidimensional array produced by the evaluation.

#### Sample Resource

```objectscript
 set myResource = {
   "resourceType":"Patient",
   "telecom": [
     {
       "system": "phone",
       "value": "(03) 5555 6473",
       "use": "official"
    },
    {
      "system": "phone",
      "value": "(03) 5555 6473",
      "use": "home"
    },
    {
      "system": "email",
      "value": "myName@email.com",
      "use": "official"
     }
   ]
 }
```

#### Extracting Data from the Resource

```objectscript
 set fhirVersion = $lb("hl7.fhir.r4.core@4.0.1")
 set fhirPathAPI = ##class(HS.FHIRPath.API).getInstance(fhirVersion)
 set tree = fhirPathAPI.parse("telecom.where(use = 'official')")
 do fhirPathAPI.evaluate(myResource, tree, .OUTPUT)
```

#### Viewing the Multidimensional Array

If you used the `zw OUTPUT` command in the InterSystems Terminal to view the multidimensional array returned by `evaluate()`, the result would be:

```
OUTPUT=2
OUTPUT(1)={"system":"phone","value":"(03) 5555 6473","use":"official"}
OUTPUT(1,"t")="ContactPoint"
OUTPUT(2)={"system":"email","value":"myName@email.com","use":"official"}
OUTPUT(2,"t")="ContactPoint"
```

Notice that the values are identified as a `ContactPoint` FHIR data type.

### Workflow Example: evaluateArray() Method

This example takes the multidimensional array produced by the evaluation in the `evaluate()` example above as input and demonstrates the ObjectScript needed to evaluate the resulting array, and looks at the multidimensional array produced by the evaluation.

#### Extracting Data from the Output Array

```objectscript
 Merge INPUT = OUTPUT
 Kill OUTPUT

 Set tree = fhirPathAPI.parse("ContactPoint.value")

 do fhirPathAPI.evaluateArray(.INPUT, tree, .OUTPUT)
```

#### Viewing the Multidimensional Array

If you used the `zw OUTPUT` command in the InterSystems Terminal to view the multidimensional array returned by `evaluateArray()`, the result would be:

```
OUTPUT=2
OUTPUT(1)="(03) 5555 6473"
OUTPUT(1,"t")="string"
OUTPUT(2)=”myName@email.com"
OUTPUT(2,"t")="string"
```

Notice that the values are identified by their ObjectScript data type (string, boolean, number, or object).

### Workflow Example: evaluateToJson() Method

This example includes the resource being evaluated, the ObjectScript needed to evaluate the resource, and a look at the dynamic array produced by the evaluation.

#### Sample Resource

```objectscript
 set myResource = {
   "resourceType":"Patient",
   "name": [
     {
       "family": "Cooper",
       "given": [
         "James",
         "Fenimore"
       ]
     }]
 }
```

#### Evaluating the Resource

```objectscript
 set fhirVersion = $lb("hl7.fhir.r4.core@4.0.1")
 set fhirPathAPI = ##class(HS.FHIRPath.API).getInstance(fhirVersion)
 set tree = fhirPathAPI.parse("name.given.empty()")
 set dynArray = fhirPathAPI.evaluateToJson(myResource, tree)
```

#### Viewing the Dynamic Array

If you used the `zw dynArray` command in the InterSystems Terminal to view the dynamic array, the result would be:

```
dynArray=[false]
```

## Functions

The FHIRPath specification defines a wide range of functions that can be used in an expression. InterSystems supports a subset of those functions.

### Supported FHIRPath Functions

<table><tr><th>Function</th><th>Example</th></tr><tr><td><a href="https://hl7.org/fhirpath/#index-integer-collection"><code>[ ]</code> (index)</a></td><td><code>Practitioner.name[1]</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#aggregateaggregator-expression-init-value-value"><code>aggregate</code></a></td><td><code>item.factor.aggregate($total+$this,0)</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#astype-type-specifier"><code>as</code></a></td><td><code>Condition.abatement.as(string)</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#children-collection"><code>children</code></a></td><td><code>Encounter.participant.children().ofType(Reference)</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#descendants-collection"><code>descendants</code></a></td><td><code>Bundle.descendants().ofType(Patient)</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#empty-boolean"><code>empty</code></a></td><td><code>Patient.contact.where(relationship = 'N').name.empty()</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#endswithsuffix-string-boolean"><code>endsWith</code></a></td><td><code>'abcdefg'.endsWith('efg')</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#existscriteria-expression-boolean"><code>exists</code></a></td><td><code>Patient.telecom.exists(system = 'phone')</code></td></tr><tr><td><a href="https://hl7.org/fhir/fhirpath.html#functions"><code>extension</code></a></td><td><code>extension('http://intersystems.com/fhir/extn/sda3/lib/code-table-detail-care-provider-description').value as string</code></td></tr><tr><td><code>firstOpens in a new tab</code></td><td><code>Patient.telecom.where(system = 'phone').first()</code></td></tr><tr><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSLIB&amp;CLASSNAME=HS.FHIRPath.Runtime#METHOD_IFNhasExtension"><code>hasExtension</code></a></td><td>Returns <code>true</code> if any of the input collection have an extension with the specified URL. (This function is not in the FHIRPath v2.0.0 specification.)</td></tr><tr><td><a href="https://hl7.org/fhirpath/#iifcriterion-expression-true-result-collection-otherwise-result-collection-collection"><code>iif</code></a></td><td><code>iif(1=1,2,3)</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#indexofsubstring-string-integer"><code>indexOf</code></a></td><td><code>'abcdefg'.indexOf('cd')</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#istype-type-specifier"><code>is</code></a></td><td><code>Condition.abatement.is(dateTime)</code></td></tr><tr><td><code>lastOpens in a new tab</code></td><td><code>Patient.name.first().given.last()</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#not-boolean"><code>not</code></a></td><td><code>Bundle.entry.resource.ofType(Patient).gender.not()</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#oftypetype-type-specifier-collection"><code>ofType</code></a></td><td><code>Bundle.entry.resource.ofType(Patient)</code></td></tr><tr><td><a href="https://hl7.org/fhir/fhirpath.html#functions"><code>resolve</code></a></td><td><code>Organization.partOf.resolve()</code></td></tr><tr><td><code>skipOpens in a new tab</code></td><td><code>Bundle.entry.resource.ofType(Encounter).skip(5)</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#startswithprefix-string-boolean"><code>startsWith</code></a></td><td><code>'abcdefg'.startsWith('abc')</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#substringstart-integer-length-integer-string"><code>substring</code></a></td><td><code>'abcdefg'.substring(1, 2)</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#tail-collection"><code>tail</code></a></td><td><code>Bundle.entry.resource.ofType(Observation).tail()</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#takenum-integer-collection"><code>take</code></a></td><td><code>Patient.name.take(1)</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#unionother-collection"><code>union</code></a></td><td><code>Practitioner.name.family.union(Practitioner.id)</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#wherecriteria-expression-collection"><code>where</code></a></td><td><code>Patient.telecom.where(use = 'official')</code></td></tr></table>

## Operations

The FHIRPath specification defines a wide range of operations that can be used in an expression. InterSystems supports a subset of those operations.

### Supported FHIRPath Operations

<table><tr><th>Operation</th><th>Example</th></tr><tr><td><a href="https://hl7.org/fhirpath/#addition"><code>+</code> (addition)</a></td><td><p><code>8 + 3</code></p><p><code>5 seconds + 3 seconds</code></p><p><code>'string1' + ' and ' + 'string2'</code></p></td></tr><tr><td><a href="https://hl7.org/fhirpath/#string-concatenation"><code>&amp;</code> (string concatenation)</a></td><td><code>'string1' &amp; ' and ' &amp; 'string2'</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#equals"><code>=</code> (equals)</a></td><td><p><code>Practitioner.name[0].family = 'Cooper'</code></p><p><code>Practitioner.meta.versionId = 10</code></p></td></tr><tr><td><a href="https://hl7.org/fhirpath/#not-equals"><code>!=</code> (not equals)</a></td><td><code>Practitioner.name[1].family != 'Smith'</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#union-collections"><code>|</code> (union collections)</a></td><td><code>Practitioner.name.family | Practitioner.id</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#and"><code>and</code></a></td><td><code>true and false</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#as-type-specifier"><code>as</code></a></td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=HXFHIR_fhirpath#HXFHIR_as_imp_note">See implementation notes.</a></td></tr><tr><td><a href="https://hl7.org/fhirpath/#implies"><code>implies</code></a></td><td><code>Patient.name.given.exists() implies Patient.name.family.exists()</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#is-type-specifier"><code>is</code></a></td><td><code>Practitioner.name[0] is HumanName</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#or"><code>or</code></a></td><td><code>true or false</code></td></tr><tr><td><a href="https://hl7.org/fhirpath/#xor"><code>xor</code></a></td><td><code>true xor false</code></td></tr></table>

Implementation Notes for as

According to the FHIRPath specification, the left operand of the `as` operation must be a collection with a single item. However, the InterSystems implementation of FHIRPath allows this collection to have multiple values. For example, suppose you have an Observation with multiple extensions that reference a Patient. With the InterSystems implementation of FHIRPath, the following expression would still be valid: `extension.value as Reference`.

## Improving Performance

InterSystems provides an in-memory cache that can store parsed FHIRPath expressions, improving performance when you have a set of expressions that are repeated frequently. Once the cache is enabled, tree structures produced by the `parse()` method are stored until the cache is cleared.

To enable the in-memory cache, call:

```objectscript
 do fhirPathAPI.enableCache(1)
```

To disable the cache, call:

```objectscript
 do fhirPathAPI.enableCache(0)
```
