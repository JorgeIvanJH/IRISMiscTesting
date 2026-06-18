# Defining Business Services

This page describes how to define business service classes.

> **Tip:**
> 
> InterSystems IRIS data platform provides specialized business service classes that use specific inbound adapters, and one of those might be suitable for your needs. If so, no programming would be needed. For a partial list, see Connectivity Options.

## Introduction to Defining Business Services

A business service is responsible for accepting requests from external applications into InterSystems IRIS. The following figure shows how it works:

[Image: Diagram showing the methods used by an inbound adapter and business service to receieve and forward a message from an externa]

Note that this figure shows only the input flow of data, not the optional response.

A business service is responsible for the following activities:

*   Waiting for a specific external event (such as notification from an application, receipt of a TCP message, etc.).
    
*   Reading, parsing, and validating the data accompanying such an event,
    
*   Returning, if required, an acknowledgment to the external application indicating that the event was received.
    
*   Creating an instance of a request message and forwarding it on to the appropriate business process or business operation for processing.
    

The purpose of a business service is usually to receive data input. In most cases, a business service has an inbound adapter associated with it. However, in some cases an adapter is not required, either because an application is capable of sending request messages into the service or because the business service has been written to handle external calls of a particular kind, for example from a composite application. A business service of this type is called an adapterless business service.

When a business service has an inbound adapter, it is in the data pulling (as opposed to pushing) mode. In this mode, the business service polls the adapter at regular intervals to see if it has data. Meanwhile, if the adapter encounters input data at any time, it calls the business service to process the input.

When a business service does not have an adapter, it does not pull data. Instead, client applications call the business service and tell it to process input (this is a data pushing mode).

## Key Principles for Business Services

First, be sure to read Programming in InterSystems IRIS.

Within a business service, you can access properties and methods of the associated adapter, which is available as the `Adapter` property of the business service. This means that you can alter the default behavior of the adapter; it may or may not be appropriate to do so. It is useful to remember the principle of encapsulation. The idea of encapsulation is that the adapter class should be responsible for the technology-specific logic, while the business service class should be responsible for the production-specific logic.

If you find that it is necessary to greatly or frequently alter the behavior of an adapter class from within a business service class, it might be more appropriate to create a customized subclass of the adapter class. See Less Common Tasks.

This principle also applies to business operations.

## Defining a Business Service Class

To create a business service class, define a class as follows:

*   The class must extend Ens.BusinessService (or a subclass).
    
*   The `ADAPTER` parameter must equal the name of the adapter class for this business service to use.
    
    > **Tip:**
    > 
    > If you simply want a business service to wake up and run periodically without concern for events outside InterSystems IRIS, use the adapter class Ens.InboundAdapter.
    
*   The class must implement the `OnProcessInput()` method, as described in Implementing the OnProcessInput() Method.
    
*   The class can add or remove settings. See Adding and Removing Settings.
    
*   The class can implement any or all of the startup and teardown methods. See Overriding Start and Stop Behavior.
    
*   The class can contain methods to accomplish work internal to itself.
    

For examples of business service classes, see the adapter guides.

## Implementing the OnProcessInput() Method

Within your business service class, your `OnProcessInput()` method should have the following generic signature:

```objectscript
Method OnProcessInput(pInput As %RegisteredObject, Output pOutput As %RegisteredObject) As %Status {}
```

Here `pInput` is the input object that the adapter will send to this business service, and `pOutput` is the output object.

First look at the adapter class that you have selected. InterSystems recommends that you edit the `OnProcessInput()` method signature to use the specific input argument needed with the adapter.

The `OnProcessInput()` method should do some or all of the following:

1.  Optionally set properties of the business service class (at any appropriate time). The business service property of greatest interest is `%WaitForNextCallInterval`. Its value controls how frequently InterSystems IRIS invokes the `OnTask()` method of the adapter.
    
    For other properties, see the class reference for Ens.BusinessService.
    
2.  Validate, if necessary, the input object.
    
3.  Examine the input object and decide how to use it.
    
4.  Create an instance of a request message class, which will be the message that your business service sends.
    
    For information on creating messages, see Creating Messages.
    
5.  For the request message, set its properties as appropriate, using values in the input object.
    
6.  Determine where you want to send the request message. When you send the message, you will need to use the configuration name of a business host within the production.
    
7.  Send the request message to a destination within the production (a business process or business operation). See the next section.
    
8.  Make sure that you set the output argument (`pOutput`). Typically you set this equal to the response message that you have received. This step is required.
    
9.  Return an appropriate status. This step is required.
    

## Sending Request Messages

In your business service class, your implementation of `OnProcessInput()` should send a request message to some destination within the production. To do so, call one of the following instance methods of the business service class, as appropriate for your needs:

*   `SendRequestSync()` sends a message synchronously (waits for a response). For details, see Using the SendRequestSync() Method.
    
*   `SendRequestAsync()` sends a message asynchronously (does not wait for a response). For details, see Using the SendRequestAsync() Method.
    
*   `SendDeferredResponse()` sends a response that was previously deferred. This method is less commonly used. For details, see Using the SendDeferredResponse() Method.
    

Each of these methods returns a status, an instance of %Status.

These methods are also defined—with the identical method signatures—in Ens.BusinessProcess and Ens.BusinessOperation, although their internals are different in those classes. This means that you can invoke these instance methods from within your business process and business operation classes.

### Using the SendRequestSync() Method

To send a synchronous request, use the `SendRequestSync()` method as follows:

```objectscript
  Set tSC = ..SendRequestSync(pTargetDispatchName, pRequest, .pResponse, pTimeout)
```

Where:

*   `pTargetDispatchName`—The configuration name of the business process or business operation to which the request is sent.
    
*   `pRequest`—A request message. See Defining Messages.
    
*   `pResponse`—(By reference) A response message. This object receives the data returned by the response.
    
*   `pTimeout`—(Optional) The number of seconds to wait for a response. The default is –1 (wait forever).
    

This method returns a status, an instance of %Status.

If no response is expected, you can use `SendRequestAsync()` instead of `SendRequestSync()`.

### Using the SendRequestAsync() Method

To send an asynchronous request, use the `SendRequestAsync()` method as follows:

```objectscript
  Set tSC = ..SendRequestAsync(pTargetDispatchName, pRequest)
```

Where:

*   `pTargetDispatchName`—The configuration name of the business process or business operation to which the request is sent.
    
*   `pRequest`—A request message. See Defining Messages.
    

This method returns a status, an instance of %Status.

If you use `SendRequestAsync()` to send a message to a business process and the business process sets the response to a persistent object, the response is saved without a corresponding response message header. This happens whenever the requestor does not ask for a response and the business process creates the response. (If this is not what you want, have the business process set the response to null.)

### Using the SendDeferredResponse() Method

All business hosts support the `SendDeferredResponse()` method. This method permits a business host to participate in the production deferred response mechanism. The business host identifies a previously deferred request, creates the actual response message, and sends this response to the business host that originated the request. See Using Deferred Sending in Programming in InterSystems IRIS.

This topic describes the role of a business service in this mechanism. Suppose an incoming event arrives in a production along with a deferred response token, and suppose the arrival point for this event is a business service. This business service then calls `SendDeferredResponse()` to create a response and direct it to the caller that originated the request. The `SendDeferredResponse()` call looks like this:

```objectscript
   Set sc = ..SendDeferredResponse(token, pResponseBody)
```

Where:

*   `token`—A string that identifies the deferred response so that the caller can match it to the original request. The business service obtains the token string through some mechanism unique to the production.
    
    For example, if the external destination is email, when sending a request for which it is willing to receive a deferred response, a business operation can include the token string in the subject line of the outgoing email. The entity receiving this email can extract this token from the request subject line and use it in the response subject line. This preserves the token so that the business service receiving the response email can use it in a subsequent call to `SendDeferredResponse()`.
    
*   `pResponseBody`—A response message. This object receives the data returned by the response. See Defining Messages.
    

This method returns a status, an instance of %Status.

## Sending Multiple Request Messages

Your implementation of `OnProcessInput()` can send multiple request messages (for example, to different targets within the production). By default, all messages are sent within the same session. If you want each message to be sent within its own session, set the `%SessionId` property of the business service to null between sending messages. For example:

```
 set ..%SessionId=""
 set sc=..SendRequestSync("Test.FileOperation1",pOutput)
 set ..%SessionId=""
 set sc=..SendRequestSync("Test.FileOperation2",pOutput)
 set ..%SessionId=""
 set sc=..SendRequestSync("Test.FileOperation3",pOutput)
```

## Processing Only One Event Per Call Interval

If you want the business service to process only one event per call interval, set the `%WaitForNextCallInterval` property to 1 (true) in your implementation of `OnProcessInput()`:

```objectscript
 set ..%WaitForNextCallInterval=1
```

This restricts the business service to processing only one input event per `CallInterval`, even when multiple input events exist.

This information applies to business services that use an adapter that have a property named `CallInterval` and that use that property as a polling interval.
