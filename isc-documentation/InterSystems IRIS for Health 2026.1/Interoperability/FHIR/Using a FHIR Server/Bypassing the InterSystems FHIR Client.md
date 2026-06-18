# Bypassing the InterSystems FHIR Client

When using a server-side application to make HL7 FHIR requests to the internal FHIR server, your application should usually use the standard FHIR client. For details about using these built-in classes, see FHIR Client.

However, you may want to use a custom ObjectScript class so you can interact with the repository without making a request through the Service. For example, you might want to perform a write operation even though the server restricts requests to read-only interactions. In this case, you can bypass the Service.

In other cases, you may want to use the same method that the FHIR client and REST handler use, but from a custom class. For details, see Direct Calls to `DispatchRequest`

Your ObjectScript application can also validate a resource.

## Bypassing the Service

A server-side application can call the methods of an Interactions subclass directly instead of submitting programmatic requests via the Service. For example, an application could call the Interactions subclass’ `Add()` method directly rather than sending a POST request to the Service. This is especially useful to avoid the overhead of normal protocol-level checks done by the Service if you have written an ObjectScript app that complies with FHIR and with the CapabilityStatement of the repo with which you are interacting, and if you are aware that you must submit valid FHIR.

Programmatic calls to methods of the Interactions class pass FHIR data as dynamic objects.

## Direct Calls to DispatchRequest

An ObjectScript application can also act as a FHIR client by calling `DispatchRequest()` directly, which is the method used by the standard FHIR client and the internal FHIR server’s REST handler.

### GET Resources

Your ObjectScript application can use the server’s Service to retrieve resources. For example, assuming `178.16.235.12` is the IP address of InterSystems server and `52783` is the superserver port, a REST call might be:

`GET http://178.16.235.12:52783/fhirapp/namespace/fhir/r4/patient/1`

Using ObjectScript to access the same endpoint looks like:

```objectscript
 set url = "/fhirapp/namespace/fhir/r4"
 set fhirService = ##class(HS.FHIRServer.Service).EnsureInstance(url)
 set request = ##class(HS.FHIRServer.API.Data.Request).%New()
 set request.RequestPath = "/Patient/1"
 set request.RequestMethod = "GET"
 do fhirService.DispatchRequest(request, .response)
```

In this example, the response is a data object (HS.FHIRServer.API.Data.Response) with the JSON response represented in a dynamic object.

> **Note:**
> 
> The first request to the server must instantiate the FHIR service by calling the `EnsureInstance()` method. It does not cause problems to make this call before every request, but it takes a miniscule amount of time to check whether the service has been modified.

### POST Resources

You can also post data to the FHIR server programmatically. In the following example, suppose the application is creating a Patient resource that is described in a JSON object in the file MyPatient.json. The ObjectScript code might look like:

```objectscript
 set url = "/csp/fhirapp/namespace/fhir/r4/"
 set fhirService = ##class(HS.FHIRServer.Service).EnsureInstance(url)
 set request = ##class(HS.FHIRServer.API.Data.Request).%New()
 set request.RequestPath = "/Patient"
 set request.RequestMethod = "POST"
 set request.Json = {}.%FromJSONFile("c:\resources\MyPatient.json")
 do fhirService.DispatchRequest(request, .response)
```

In this example, the source of the JSON stored in the request could have come from a dynamic object in your application rather than an external file.

## Handling FHIR Data as XML

When you use a REST client to perform CRUD operations on the FHIR server, the FHIR server automatically accepts or returns FHIR data as XML based on the incoming request. However, when you are performing CRUD operations programmatically from a custom ObjectScript class, all data going into the FHIR service must be in JSON format. Likewise, all data returned by the service is in JSON format. The FHIR server provides helper methods to convert XML to JSON and JSON to XML.

To send XML data into the FHIR service, put the XML into a stream object and send it to the HS.FHIRServer.Service.StreamToJSON() method, specifying that the format is XML. For example, the following code turns the XML payload into a JSON request that can be passed to the FHIR service:

```objectscript
 set url = "/csp/fhirapp/namespace/fhir/r4/"
 set fhirService = ##class(HS.FHIRServer.Service).EnsureInstance(url)
 set request = ##class(HS.FHIRServer.API.Data.Request).%New()
 set request.Json= fhirService.StreamToJSON(MyStream,"XML")
```

To convert a JSON response from the FHIR service into XML, use the HS.FHIRServer.Util.JSONToXML.JSONToXML() method.

## Handling FHIR Data as a Stream

The HS.FHIRServer.Service.StreamToJSON() method converts an XML or JSON stream into a JSON object so it can be passed to the FHIR service as part of a request. The FHIR service cannot handle a stream directly. The method accepts two arguments: the stream and the format of the data in the stream. For example, the following lines of code turn a JSON stream into a JSON object so it can be sent to the FHIR service:

```objectscript
 set url = "/csp/fhirapp/namespace/fhir/r4/"
 set fhirService = ##class(HS.FHIRServer.Service).EnsureInstance(url)
 set request = ##class(HS.FHIRServer.API.Data.Request).%New()
 set request.Json= fhirService.StreamToJSON(MyStream,"JSON")
```

For XML streams, simply pass `XML` as the second argument.

## Validating FHIR Resources

Your ObjectScript application can programmatically validate a resource against the FHIR server’s metadata without using the FHIR `$validate` operation as long as the resource is represented as a dynamic object. For example, the following code validates a Patient resource against the server’s FHIR Release 4 metadata, which includes the schema for the Patient resource. When calling the `LoadSchema()` method, you can specify the common name of the FHIR version (for example, `R4` or `STU3`) or the name of the server’s base metadata (for example, `HL7v40` or `HL7v30`).

```objectscript
 // Put JSON representation of Patient resource into a dynamic object
 set patient = ##class(%DynamicObject).%FromJSONFile("c:\localdata\myPatient.json")

 //Validate the patient resource
 set schema = ##class(HS.FHIRServer.Schema).LoadSchema("R4")
 set resourceValidator = ##class(HS.FHIRServer.Util.ResourceValidator).%New(schema)

 do resourceValidator.ValidateResource(patient)
```
