# Defining Business Operations

This page describes how to define business operation classes.

> **Tip:**
> 
> InterSystems IRIS data platform provides specialized business operation classes that use specific outbound adapters, and one of those might be suitable for your needs. If so, no programming would be needed. For a partial list, see Connectivity Options.

## Introduction to Defining Business Operations

A business operation is responsible for sending requests from InterSystems IRIS to an external application or system. The following figure shows how it works:

[Image: Diagram showing how the XData block for a business operation defines how each message type is handled]

Note that this figure shows only the input flow of data, not the optional response.

A business operation is responsible for the following activities:

*   Waiting for requests from business services or business processes.
    
*   Dispatching, via a message map, the request to a specific method within the business operation. Each method within a business operation class represents a specific action within an external application.
    
*   Transforming the request object into a form usable by the associated outbound adapter and asking the outbound adapter to send a request to the external application.
    
*   Returning, if requested, a response object to the caller.
    

Each business operation contains a message map that specifies which external operation to perform, depending on the type of request message that it received. The message map contains one or more entries, each of which corresponds to one invocation of the associated outbound adapter.

## Key Principles for Business Operations

First, be sure to read Programming in InterSystems IRIS.

By convention, a business operation is an extremely specific operation that contains very little logic and does what is requested of it without calling further operations or branching in any way. When the design of the production demands logic, this is contained in a business process.

Many productions provide a large set of extremely simple business operations. In these cases, business processes contain the logic that determines when each operation should be called.

Also see Key Principles for Business Services.

## Defining a Business Operation Class

To create a business operation class, define a class as follows:

*   The class must extend Ens.BusinessOperation (or a subclass).
    
*   The `ADAPTER` parameter should usually equal the name of the adapter class for this business service to use.
    
    Or you can define a business operation with no associated outbound adapter class. In this case, the business operation itself must contain the logic needed to communicate with an external application.
    
*   The `INVOCATION` parameter must specify the invocation style you want to use, which must be one of the following.
    
    *   `Queue` means the message is created by the sending component’s job and placed on a queue. The receiving component’s job takes the message from the queue and processes it. This is the most common setting.
        
    *   `InProc` means the message is created and processed by the sending component’s job. (`InProc` stands for “in the same process.”) Although the message trace display suggests that the message is sent to another job, the sending component’s job just executes code in the receiving component’s class. There is no message queue.
        
*   The class should define a message map that includes at least one entry. A message map is an XData block entry that has the following structure:
    
    ```
    XData MessageMap
    {
    <MapItems>
      <MapItem MessageType="messageclass">
        <Method>methodname</Method>
      </MapItem>
      ...
    </MapItems>
    }
    ```
    
    See Defining a Message Map.
    
*   The class must define all the methods named in the message map. These methods are known as message handlers. Each message handler should have the following signature:
    
    ```objectscript
    Method Sample(pReq As RequestClass, Output pResp As ResponseClass) As %Status {}
    ```
    
    Here `Sample` is the name of the method, `RequestClass` is the name of a request message class, and `ResponseClass` is the name of a response message class. In general, these methods will refer to properties and methods of the `Adapter` property of your business operation. For details, see Defining Message Handler Methods.
    
*   If `INVOCATION` is `Queue`, the class can define the optional `CONTEXT` parameter, which is a comma-separated list of variables to retain in the context between messages. If this parameter is set, all variables except those specified in this list will be killed before each message.
    
    This parameter is ignored if `INVOCATION` is `InProc`.
    
*   The class can add or remove settings. See Adding and Removing Settings.
    
*   The class can implement any or all of the startup and teardown methods. See Overriding Start and Stop Behavior.
    
    InterSystems IRIS is an integration platform potentially communicating with many other heterogeneous devices; therefore, it does not make property values dependent on server platform, time zone, time formatting, or other localization issues that may apply. Rather, InterSystems recommends you handle such cases in your production implementation. If your production requires different initial settings for property values, set the value in the `OnInit()` method of the business operation. See Overriding Start and Stop Behavior.
    
*   The class can contain methods to accomplish work internal to itself.
    

The following example shows the general structure that you need:

```xml
Class MyProduction.NewOperation Extends Ens.BusinessOperation
{
Parameter ADAPTER = "MyProduction.MyOutboundAdapter";

Parameter INVOCATION = "Queue";

Method SampleCall(pRequest As Ens.Request, Output pResponse As Ens.Response) As %Status
{
  Quit $$$ERROR($$$NotImplemented)
}

XData MessageMap
{
<MapItems>
  <MapItem MessageType="Ens.Request">
    <Method>SampleCall</Method>
  </MapItem>
</MapItems>
}
}
```

For examples of business operation classes, see the adapter guides.

## Defining a Message Map

A message map is an XML document, contained within an XData MessageMap block in the business operation host class. For example:

```xml
Class MyProduction.Operation Extends Ens.BusinessOperation
{

XData MessageMap
{
<MapItems>
  <MapItem MessageType="MyProduction.MyRequest">
    <Method>MethodA</Method>
  </MapItem>
  <MapItem MessageType="Ens.StringRequest">
    <Method>MethodB</Method>
  </MapItem>
</MapItems>
}

}
```

The operation of the message map is straightforward. When the business operation receives an incoming request, it searches, starting at the top of the message map, through each `MapItem` until it finds the first one whose `MessageType` attribute matches the type of the incoming message. It then invokes the operation method associated with this `MapItem`.

Some things to keep in mind about message maps:

*   The message map is searched from top to bottom; once a match is found, no more searching is performed.
    
*   If the incoming request object is a subclass of a given `MessageType` then it is considered a match. If you want to filter out subclasses, be sure to place them above any super classes within the message map.
    
*   If the incoming request does not match any of the `MapItem` entries, then the `OnMessage` method is called.
    

## Defining Message Handler Methods

When you create a business operation class, typically the biggest task is writing message handlers for use with this adapter, that is, methods that receive production messages and then invoke methods of the adapter in order to communicate with targets outside the production.

Each message handler method should have the following signature:

```objectscript
Method Sample(pReq As RequestClass, Output pResp As ResponseClass) As %Status {}
```

Here `Sample` is the name of the method, `RequestClass` is the name of a request message class, and `ResponseClass` is the name of a response message class.

In general, the method should do some or all of the following:

1.  Optionally set properties of the business operation class (at any appropriate time). See Business Operation Properties.
    
2.  Examine the input object.
    
3.  Create an instance of the response class.
    
4.  Call the applicable method or methods of the adapter. These methods are available via the `Adapter` property of your business operation. For example:
    
    ```objectscript
        Set tSc=..Adapter.SendMail(email,.pf)
    ```
    
    This method is discussed after these steps.
    
    Or, to send messages to a target within the production, see Sending Messages to a Target within the Production.
    
5.  Examine the response.
    
6.  Use information in the response to create a response message (an instance of Ens.Response or a subclass), which the method returns as output.
    
    For information on defining message classes, see Defining Messages.
    
7.  Make sure that you set the output argument (`pOutput`). Typically you set this equal to the response message. This step is required.
    
8.  Return an appropriate status. This step is required.
    

## Business Operation Properties

Within an operation method, the following properties of the business operation class are available:

<table><tr><th>Property</th><th>Description</th></tr><tr><td><code>%ConfigName</code></td><td>The configuration name for this business operation.</td></tr><tr><td><code>%SessionId</code></td><td>The session ID of the current message being processed.</td></tr><tr><td><code>Adapter</code></td><td>The associated outbound adapter for this business operation.</td></tr><tr><td><code>DeferResponse</code></td><td>To defer the response from this business operation for later delivery, set the <code>DeferResponse</code> property to the integer value 1 (true) and obtain a deferred response delivery token before exiting the business operation.</td></tr><tr><td><code>FailureTimeout</code></td><td>The length of time (in seconds) during which to continue retry attempts. After this number of seconds has elapsed, give up and return an error code. See <code>Retry</code> and <code>RetryInterval</code>.</td></tr><tr><td><code>Retry</code></td><td>Set this property to the integer value 1 (true) if you want to retry the current message. Typically, the retry feature is used when the external application is not responding and you wish to retry without generating an error. See <code>RetryInterval</code> and <code>FailureTimeout</code>.</td></tr><tr><td><code>RetryInterval</code></td><td>How frequently (in seconds) to retry access to the output system if this message is marked for retry. See <code>Retry</code> and <code>FailureTimeout</code>.</td></tr><tr><td><code>SuspendMessage</code></td><td>Set this property to the integer value 1 (true) if you want the business operation to mark its current in-progress message as having Suspended status. See the section <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EGDV_busop#EGDV_busop_suspend">Suspending Messages</a>.</td></tr></table>

## Calling Adapter Methods

Most commonly, a business operation does not contain the logic used to communicate with the external system. Rather, the business operation uses an outbound adapter that handles this logic. Once the business operation has been associated with an outbound adapter, it calls the adapter’s methods to send and receive data. For details on invoking adapter methods, see Accessing Properties and Methods from a Business Host.

## Sending Requests to Targets within the Production

Although a business operation is primarily responsible for delivering a request to the specific external application, it can also send messages to other business operations or to business processes, as needed. To send messages to a target within the production, call `SendRequestSync()`, `SendRequestAsync()`, or `SendDeferredResponse()`.

For information on these methods, see Sending Request Messages in Defining Business Services.

Ens.BusinessOperation defines an additional method that you can use: `DeferResponse()`.

### The DeferResponse() Method

This method returns a %Status value indicating success or failure. It provides one by-reference argument, `token`, which returns the deferred response delivery token required for a later call to `SendDeferredResponse()`. For example:

```objectscript
   Set sc=..DeferResponse(.token)
   // Send the token out somewhere...
   Quit $$$O
```

For an overview of deferred sending, see Using Deferred Sending in Programming in InterSystems IRIS.

## Suspending Messages

If you want the business operation to mark its current in-progress message as having Suspended status, set the business operation property `SuspendMessage` to the integer value 1 (true). Typically a business operation will do this for messages that have been rejected by the external system for some reason.

InterSystems IRIS places a Suspended message on a special queue so that a system administrator can diagnose the problem, fix the problem, and then resend the message. The system administrator can perform a simple resend (to the original target) or can send it to a new destination. For information, see Resending Messages.

The following sample method is from a business operation that sends a document to an external system. The method sets the `SuspendMessage` property to 1 if an error returns from the call to `Validate()` the document that is about to be sent:

```objectscript
Method validateAndIndex(pDoc As MyX12.Document) As %Status
{
  If ""=..Validation||'$method($this,"OnValidate",pDoc,..Validation,.tSC) {
    Set tSC=##class(MyX12.Validator).Validate(pDoc,..Validation)
  }
  Set:'$D(tSC) tSC=$$$OK
  If $$$ISERR(tSC) {
    Set ..SuspendMessage=1
    Do ..SendAlert(##class(Ens.AlertRequest).%New($LB(
        ..%ConfigName,"Suspended document "_pDoc.%Id()_
        " because it failed validation using spec '"
        _..Validation_"' with error "_
        $$$StatusDisplayString(tSC))))
    Quit tSC
  }
  If ""'=..SearchTableClass {
    TRY {
      Set tSCStore=$classmethod(..SearchTableClass,"IndexDoc",pDoc)
      If $$$ISERR(tSCStore)
        $$$LOGWARNING("Failed to create SearchTable entries")
    }
    CATCH errobj {
      $$$LOGWARNING("Failed to invoke SearchTable class")
     }
  }
  Quit $$$OK
}
```
