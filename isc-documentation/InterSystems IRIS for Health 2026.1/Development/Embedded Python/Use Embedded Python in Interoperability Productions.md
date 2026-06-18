# Use Embedded Python in Interoperability Productions

If you are writing custom business host classes or adapter classes for interoperability productions in InterSystems IRIS, any callback methods must be written in ObjectScript because their signatures make use of `ByRef` and `Output` keywords. A callback method is an inherited method that does nothing by default, but is designed to be implemented by the user. The ObjectScript code in a callback method can, however, make use of Python packages or call other methods implemented in Python.

The following example shows a business operation that takes the string value from an incoming message and uses the Amazon Web Services (AWS) `boto3` SDK for Python to send that string to a phone in a text message via the Amazon Simple Notification Service (SNS). The details of this package is out of scope for this discussion, but you can see in the example that the `OnInit()` and `OnMessage()` callback methods are written in ObjectScript, while the methods `PyInit()` and `SendSMS()` are written in Python.

```objectscript
/// Send SMS via AWS SNS
Class dc.opcua.SMS Extends Ens.BusinessOperation
{

Parameter INVOCATION = "Queue";

/// AWS boto3 client
Property client As %SYS.Python;

/// json.dumps reference
Property tojson As %SYS.Python;

/// Phone number to send SMS to
Property phone As %String [ Required ];

Parameter SETTINGS = "phone:SMS";

Method OnMessage(request As Ens.StringContainer, Output response As Ens.StringContainer) As %Status
{
    #dim sc As %Status = $$$OK
    try {
        set response = ##class(Ens.StringContainer).%New(..SendSMS(request.StringValue))
        set code = +{}.%FromJSON(response.StringValue).ResponseMetadata.HTTPStatusCode
        set:(code'=200) sc = $$$ERROR($$$GeneralError, $$$FormatText("Error sending SMS,
            code: %1 (expected 200), text: %2", code, response.StringValue))
    } catch ex {
        set sc  = ex.AsStatus()
    }

    return sc
}

Method SendSMS(msg As %String) [ Language = python ]
{
    response = self.client.publish(PhoneNumber=self.phone, Message=msg)
    return self.tojson(response)
}

Method OnInit() As %Status
{
    #dim sc As %Status = $$$OK
    try {
        do ..PyInit()
    } catch ex {
        set sc = ex.AsStatus()
    }
    quit sc
}

/// Connect to AWS
Method PyInit() [ Language = python ]
{
    import boto3
    from json import dumps
    self.client = boto3.client("sns")
    self.tojson = dumps
}

}
```

> **Note:**
> 
> The code in the `OnMessage()` method, above, contains an extra line break for better formatting when printing this document.

The following business service example is known as a poller. In this case, the business service can be set to run at intervals and generates a request (in this case containing a random string value) that is sent to a business process for handling.

```objectscript
Class Debug.Service.Poller Extends Ens.BusinessService
{

Property Target As Ens.DataType.ConfigName;

Parameter SETTINGS = "Target:Basic";

Parameter ADAPTER = "Ens.InboundAdapter";

Method OnProcessInput(pInput As %RegisteredObject, Output pOutput As %RegisteredObject,
    ByRef pHint As %String) As %Status [ Language = objectscript ]
{
    set request = ##class(Ens.StringRequest).%New()
    set request.StringValue = ..RandomMessage()
    return ..SendRequestSync(..Target, request, .pOutput)
}

ClassMethod RandomMessage() As %String [ Language = python ]
{
    import iris
    import random
    fruits = ["apple", "banana", "cherry"]
    fruit = random.choice(fruits)
    return fruit + ' ' + iris.Debug.Service.Poller.GetSomeText()
}

ClassMethod GetSomeText() As %String [ Language = objectscript ]
{
    quit "is something to eat"
}

}
```

For more information on programming for interoperability productions, see Programming Business Services, Processes and Operations.

## Other Options

While the traditional approach to creating business hosts for interoperability productions is limited when using Embedded Python, you have some other options when it comes to developing productions using Python.

*   PEX (Production EXtension) is a framework in InterSystems IRIS that enables you to develop components for interoperability productions using Python as an external language. For more information, see Introduction to PEX.
    
*   PyProd (InterSystems Python Productions) is a Python library that enables developers to build interoperability components entirely in Python. For more information, see intersystems-pyprod.
    
    > **Note:**
    > 
    > InterSystems PyProd is an experimental feature.
