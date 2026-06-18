# Modifying the Implementation Class

This topic discusses how to modify the implementation class for a REST service.

This topic assumes that you have previously generated REST service classes as described in Creating and Editing REST Services.

## Initial Method Definitions

The implementation class initially contains stub methods like the following example:

```
/// Returns all pets from the system that the user has access to<br/>
/// The method arguments hold values for:<br/>
///     tags, tags to filter by<br/>
///     limit, maximum number of results to return<br/>
ClassMethod findPets(tags As %ListOfDataTypes(ELEMENTTYPE="%String"), limit As %Integer) As %Stream.Object
{
    //(Place business logic here)
    //Do ..%SetStatusCode(<HTTP_status_code>)
    //Do ..%SetHeader(<name>,<value>)
    //Quit (Place response here) ; response may be a string, stream or dynamic object
}
```

In each case, these stub methods have signatures that obey the contract defined by the specification of the REST service.

## Implementing the Methods

For each method in the implementation class, edit the method definition (specifically the implementation) as appropriate for the REST call that uses it. Notice that the method is preceded by a comment that is a copy of the description of the corresponding REST call. In the implementation:

*   Return the appropriate value.
    
*   Examine the request message. To do so, use the `%CheckAccepts()`, `%GetContentType()`, and `%GetHeader()` methods of the implementation class. All methods mentioned here are inherited from %REST.Impl, the superclass of your implementation class.
    
*   Set the HTTP status code as needed to indicate, for example, whether the resource was available. To do so, use the `%SetStatusCode()` method. For information on HTTP status codes, see http://www.faqs.org/rfcs/rfc2068.html.
    
*   Set the HTTP response header. To do this, use the `%SetHeader()`, `%SetHeaderIfEmpty()`, and `%DeleteHeader()` methods.
    
*   Report errors if needed. To do so, use the `%LogError()` method.
    

For details on these methods, see the class reference for %REST.Impl.

## Exposing Details of Server Errors

By default, if a REST service encounters an internal error, details of the error are not reported to the client. To change this, add the following to the implementation class and then recompile it:

```
Parameter ExposeServerExceptions = 1;
```

Note that the default `%ReportRESTError()` method checks this parameter. If you override that method (see next heading), you can choose whether your method uses this parameter or not.

## Modifying the Error Response

If you need to format the error response in a non-default way, override the `%ReportRESTError()` method in the implementation class. In your method, use the `%WriteResponse()` method to return the error response.

For details on these methods, see the class reference for %REST.Impl.
