# Defining Business Processes

Business processes are responsible for the higher level processing within a production. This page introduces them and discusses how to design and develop business process classes.

## Introduction to Defining Business Processes

By convention, business processes contain most of the logic of the production. They can contain their own logic and they can call business rules and data transformations, each of which also contains specialized logic. The following figure illustrates this:

[Image: Diagram showing the various activities that can occur within a business process]

Note that this figure shows only the request messages.

There are many possible uses for business processes. In some cases, a business process coordinates a series of actions in one or more external applications. It contains the logic to determine the processing and it calls business operations or other business processes as needed. Business processes can also include human interaction; for details, see Developing Workflows.

InterSystems IRIS data platform provides the following general types of business process:

*   BPL processes, which are based on the class Ens.BusinessProcessBPL.
    
    Only BPL processes support the business process execution context and a graphical display of logic.
    
*   Routing processes, which are based on the class EnsLib.MsgRouter.RoutingEngine or EnsLib.MsgRouter.VDocRoutingEngine.
    
    InterSystems IRIS provides a set of classes to route specific kinds of messages. To use these subclasses, no coding is generally necessary. See Types of Business Processes.
    
*   Custom business processes, which are based on the class Ens.BusinessProcess.
    

A production can include any mix of these business processes.

Note that Ens.BusinessProcessBPL, EnsLib.MsgRouter.RoutingEngine, and EnsLib.MsgRouter.VDocRoutingEngine are all based on Ens.BusinessProcess.

## Comparison of Business Logic Tools

You will probably develop business processes in conjunction with the data transformations and business rules that they use. Data transformations and business rules are intended to contain specific kinds of logic:

*   Data transformations alter the message
    
*   Business rules return values or specify where to send messages (or potentially both)
    

There is, however, overlap among the options available in business processes, data transformations, and business rules. To assist you in determining how to create these items, the following table compares them. It discusses BPL (the most common business process), DTL (the most common data transformations), and business rules.

<table><tr><th>Option</th><th>Supported in BPL?</th><th>Supported in DTL?</th><th>Supported in business rules?</th></tr><tr><td>Retrieving information about the business process</td><td>Yes (business execution <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_vars">context</a> variables)</td><td>No</td><td>No</td></tr><tr><td>Assigning a value</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_assign">&lt;assign&gt;</a>)</td><td>Yes (<code>assign</code> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_assign">action</a>)</td><td>Yes (<code>assign</code> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBUS_rulesets#EBUS_ruleset_actions">action</a>)</td></tr><tr><td>Calling a data transformation</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_transform">&lt;transform&gt;</a>)</td><td>Yes (<code>subtransform</code> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_subtransform">action</a>)</td><td>Yes (<code>send</code> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBUS_rulesets#EBUS_ruleset_actions">action</a>)</td></tr><tr><td>Calling a business rule</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_call">&lt;call&gt;</a>)</td><td>No</td><td>Yes (<code>delegate</code> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBUS_rulesets#EBUS_ruleset_actions">action</a>)</td></tr><tr><td>Calling custom code</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_code">&lt;code&gt;</a>)</td><td>Yes (<code>code</code> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_code">action</a>)</td><td>No</td></tr><tr><td>Invoking SQL</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_sql">&lt;sql&gt;</a>)</td><td>Yes (<code>sql</code> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_sql">action</a>)</td><td>No</td></tr><tr><td>Conditional logic</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_if">&lt;if&gt;</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_switch">&lt;switch&gt;</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_branch">&lt;branch&gt;</a>)</td><td>Yes (<code>if</code> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_if">action</a>)</td><td>No</td></tr><tr><td>Looping</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_foreach">&lt;foreach&gt;</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_while">&lt;while&gt;</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_until">&lt;until&gt;</a>)</td><td>Yes (<code>for each</code> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_foreach">action</a> )</td><td>No</td></tr><tr><td>Sending an alert</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_alert">&lt;alert&gt;</a>)</td><td>No</td><td>No</td></tr><tr><td>Including trace elements</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_trace">&lt;trace&gt;</a>)</td><td>Yes (<code>trace</code> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EDTL_trace">action</a>)</td><td>Yes (<code>trace</code> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBUS_rulesets#EBUS_ruleset_actions">action</a>)</td></tr><tr><td>Sending a request message to a business operation or process</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_call">&lt;call&gt;</a>)</td><td>No</td><td>Yes (<code>send</code> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBUS_rulesets#EBUS_ruleset_actions">action</a>)</td></tr><tr><td>Waiting for a response from asynchronous requests</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_sync">&lt;sync&gt;</a>)</td><td>No</td><td>No</td></tr><tr><td>Deleting the message</td><td>No</td><td>No</td><td>Yes (<code>delete</code> <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBUS_rulesets#EBUS_ruleset_actions">action</a>)</td></tr><tr><td>Performing error handling</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_throw">&lt;throw&gt;</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_catch">&lt;catch&gt;</a>, and others)</td><td>No</td><td>No</td></tr><tr><td>Delaying execution for a specified duration or until a future time</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_delay">&lt;delay&gt;</a>)</td><td>No</td><td>No</td></tr><tr><td>Sending a primary response before execution is complete</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_reply">&lt;reply&gt;</a>)</td><td>No</td><td>No</td></tr><tr><td>Using XPATH and XSLT</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_xpath">&lt;xpath&gt;</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_xslt">&lt;xslt&gt;</a>)</td><td>No</td><td>No</td></tr><tr><td>Storing a message temporarily to acknowledge a milestone</td><td>Yes (<a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EBPL_milestone">&lt;milestone&gt;</a>)</td><td>No</td><td>No</td></tr></table>

For details on DTL transformations and business rules, see Developing DTL Transformations and Developing Business Rules.

## Key Principles for Business Processes

First, be sure to read Programming in InterSystems IRIS.

When you develop business processes, consider the following key principles:

*   Sometimes it is desirable to make the response object be a modified version of the incoming request object, and it may be useful to make modifications in stages. However, do not modify the incoming request object. Instead copy it to a context variable (or, for a custom business process, copy data to local variable). Then modify the copy.
    
*   Be careful when sending messages synchronously (which you can do only within a custom business process or within <code> in BPL).
    
    When a business process A calls business process B synchronously, process A does not continue until the response is received. If process A requires completion of calls to other processes (B) in order to complete itself, and if those processes share the pool of actor jobs, the actor pool can become deadlocked if there is no free actor job to process the called business process (B).
    
    This happens because the calling business process cannot complete and free the actor job until the called business process returns, but the called business process cannot execute because there is no free actor job to execute it.
    
    Also note that InterSystems IRIS cannot shut down during a true synchronous call.
    
    It is better to use `SendRequestAsync()` and handle response messages in the `OnResponse()` method. If you need to call synchronously, you can avoid this problem by configuring the called business process (B) to use its own job pool.
    
*   If a single-job business process makes a request and waits for the response, the process loses FIFO capability.
    
    Because synchronous calls from BPL are implemented asynchronously by the compiler, the business process will go to disk after issuing the call. The actor can then continue to dequeue fresh business process or responses to other business processes.
    
    FIFO processing is only guaranteed for a single-job business process if it makes no call requests that need a response. If a business process must make a call and still maintain FIFO, it must use a <code> activity that invokes `SendRequestSync()`. However, in that case the preceding bullet item applies.
    
*   BPL provides a useful advantage: It handles every aspect of synchronous and asynchronous messaging in a streamlined and elegant way that prevents common problems with contention and deadlocks. Even when a call is marked synchronous, if any wait time is required, the production framework quietly frees the job that was executing the call on behalf of the BPL business process so that it can do other work while BPL waits for the synchronous response. Later on, the framework silently coordinates receipt of the synchronous response and wakes up the BPL business process to resume its work.
    
    If you use custom code, it is very easy to (accidentally) design a production prone to deadlock. All you need to do is to create a sequence of business processes that send synchronous requests and use a limited actor pool. If the production then receives the same number of messages as actors, and a synchronous send occurs simultaneously for all the messages, the production ends up in a deadlock where all the actor processes are in the state of waiting for another process to release messages from queues. The most dangerous aspect of this issue is that testing does not necessarily produce the conditions that cause the deadlock. It is quite possible that the deadlock will first be encountered after deployment. At this point it will not be clear why the production has seized up, and the costs of this unforeseen problem may be high.
    

## Defining BPL Business Processes

A BPL business process is a class based on Ens.BusinessProcessBPL. In this case, you can create and edit the process visually within either the Management Portal or an IDE. For information, see Developing BPL Processes.

## Defining Custom Business Processes

To create a custom business process class, define a class as follows:

*   The class must extend Ens.BusinessProcess (or a subclass).
    
*   The class must implement the `OnRequest()` and `OnResponse()` methods, as described in next two sections.
    
*   The class can add or remove settings. See Adding and Removing Settings.
    
*   The class can implement any or all of the startup and teardown methods. See Overriding Start and Stop Behavior.
    
*   The class can contain methods to accomplish work internal to itself.
    

### Implementing the OnRequest() Method

A custom business process class must implement the `OnRequest()` method. A production calls this method whenever an initial request for a specific business process arrives on the appropriate queue and is assigned a job in which to execute.

This method has the following signature:

```objectscript
method OnRequest(request As %Library.Persistent, Output response As %Library.Persistent) as %Status {}
```

Where:

*   `request`—The incoming request object.
    
*   `response`—The response returned by this business process.
    
    Note that if the business process received a message via `SendRequestAsync()`, no response is expected. In such a case, if the business process returns a response, that response is saved without a message header. If that is not what you want, the business process can programmatically check to see if a response is expected and create the response object only if needed. To see if a response is expected, use the `ReturnQueueName` property or the `needsReply()` method of the `..%PrimaryRequestHeader`. For example:
    
    ```objectscript
     if ..%PrimaryRequestHeader.ReturnQueueName'="" {
        //create the response object
     }
    ```
    
    Or:
    
    ```objectscript
     if ..%PrimaryRequestHeader.needsReply() {
        //create the response object
     }
    ```
    

#### Example

The following is an example of an `OnRequest()` method:

```objectscript
Method OnRequest(request As Demo.Loan.Msg.Application, Output response As Demo.Loan.Msg.Approval)
       As %Status
{
  Set tSC=$$$OK
  $$$TRACE("received application for "_request.Name)
    #;
  If $zcrc(request.Name,2)#5=0 {
    Set tRequest = ##class(Demo.Loan.Msg.PrimeRateRequest).%New()
    Set tSC =..SendRequestAsync("Demo.Loan.WebOperations",tRequest,1,"PrimeRate")
    If $$$ISOK(tSC){
      Set tRequest = ##class(Demo.Loan.Msg.CreditRatingRequest).%New()
      Set tRequest.SSN = request.SSN
      Set tSC =..SendRequestAsync("Demo.Loan.WebOperations",tRequest,1,"CreditRating")
      If $$$ISOK(tSC){
        Set tSC = ..SetTimer("PT15S")
      }
    }
  } Else {
      Set response = ##class(Demo.Loan.Msg.Approval).%New()
      Set response.BankName = "BankUS"
      Set response.IsApproved = 0
      $$$TRACE("application is denied because of bank holiday")
    }
  Return tSC
}
```

### Implementing the OnResponse() Method

A custom business process class must implement the `OnResponse()` method. A production calls this method whenever a response for a specific business process arrives on the appropriate queue and is assigned a job in which to execute. Typically this is a response to an asynchronous request made by the business process.

This method has the following signature:

```objectscript
method OnResponse(request As %Library.Persistent,
                  ByRef response As %Library.Persistent,
                  callrequest As %Library.Persistent,
                  callresponse As %Library.Persistent,
                  pCompletionKey As %String) as %Status {}
```

This method takes the following arguments:

*   `request`—The initial request object sent to this business process.
    
*   `response`—The response object that will eventually be returned by this business process.
    
*   `callrequest`—The request object associated with the incoming response.
    
*   `callresponse`—The incoming response object.
    
*   `pCompletionKey`—The completion key value associated with the incoming response. This is set by the call to the `SendRequestAsync()` method that made the request.
    

#### Example

The following is an example of an `OnResponse()` method:

```objectscript
/// Handle a 'Response'
Method OnResponse(request As Ens.Request,
                  ByRef response As Ens.Response,
                  callrequest As Ens.Request,
                  callresponse As Ens.Response,
                  pCompletionKey As %String) As %Status
{
    Set tSC=$$$OK
    If pCompletionKey="PrimeRate" {
        Set ..PrimeRate = callresponse.PrimeRate
    } Elseif pCompletionKey="CreditRating" {
        Set ..CreditRating = callresponse.CreditRating
    }
    Return tSC
}
```

### Methods to Use in OnRequest() and OnResponse()

When you implement `OnRequest()` and `OnResponse()`, you can use the following methods of the Ens.BusinessProcess class:

*   `SendDeferredResponse()`
    
*   `SendRequestSync()`
    
    But see Key Principles for Business Processes.
    
*   `SendRequestAsync()`
    
*   `SetTimer()`
    
*   `IsComponent()`
    

For details on these methods, see Ens.BusinessProcess.
