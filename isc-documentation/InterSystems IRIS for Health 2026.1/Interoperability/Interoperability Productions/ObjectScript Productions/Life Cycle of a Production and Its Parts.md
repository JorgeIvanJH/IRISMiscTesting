# Life Cycle of a Production and Its Parts

This page describes the life cycle of a production and its component parts, for reference.

## Life Cycle of a Production

### Production Startup

When a production starts, the sequence of actions is as follows:

1.  The production class is instantiated; its optional `OnStart()` method executes.
    
2.  The production instantiates each business operation and executes its optional `OnProductionStart()` method.
    
3.  The production instantiates each business process and executes its optional `OnProductionStart()` method.
    
4.  The production clears the business metric cache of any metric values left over from a previous run.
    
5.  The production instantiates each business service and executes its optional `OnProductionStart()` method.
    
6.  The production processes any items already placed in queues. This includes asynchronous messages that were queued when the production stopped.
    
7.  The production now accepts input from outside InterSystems IRIS data platform.
    

### Production Shutdown

When a production stops, the sequence of actions is as follows:

1.  The production takes each business service offline and executes its optional `OnProductionStop()` method. This action stops all requests from outside InterSystems IRIS.
    
2.  All business hosts receive a signal to become Quiescent.
    
3.  All queues go into a Quiescent state. This means that from this point forward, business hosts can only process queued messages with High priority (synchronous messages). Asynchronous messages remain on their respective queues.
    
4.  The production finishes processing all synchronous messages to the best of its ability.
    
5.  The production takes each business process offline and executes its optional `OnProductionStop()` method.
    
6.  The production takes each business operation offline and executes its optional `OnProductionStop()` method.
    
7.  The production goes offline. InterSystems IRIS executes the optional `OnStop()` method in the production class.
    

## Life Cycle of a Business Service and Adapter

### Production Startup

When you start a production (or change the configuration of a specific business service), InterSystems IRIS automatically performs the following tasks for each configured business service class (that is, for every business service listed in the production definition):

1.  InterSystems IRIS invokes the business service’s `OnProductionStart()` callback method, if defined.
    
    The `OnProductionStart()` method is a class method that is invoked once for each business service class listed in the production configuration. A business service class can use this callback to perform any class-wide initialization it may require. If the business service does not have an adapter, the business service class can use this callback to check for errors.
    
2.  InterSystems IRIS creates one or more background processes in which to execute the business service.
    
    The number of background processes is determined by the business service’s `PoolSize` property within the production configuration. Each background process is referred to as an instance of the business service and contains an instance of a business service object.
    
    InterSystems IRIS only creates a background process for a business service if the following conditions are true:
    
    *   The business service class must have an associated inbound adapter class as specified by its ADAPTER class parameter.
        
        A business service class with no associated inbound adapter is referred to as an “adapterless service.” Instead of waiting for external events, such a service is invoked in-process (perhaps by a composite application).
        
    *   The business service’s `Enabled` property within the production configuration must be set to 1 (otherwise the business service is considered to be disabled and will not accept input).
        
    *   The business service’s `PoolSize` property within the production configuration must be set to a value greater than 0.
        
    
    If the business service’s `Foreground` property within the production configuration is set to 1, then InterSystems IRIS will create a foreground process (that is, InterSystems IRIS will create a Terminal window) for the business service. This feature facilitates testing and debugging.
    
3.  InterSystems IRIS initializes the system monitoring information used to monitor the status and operating history of the business service.
    
4.  Within each background process, InterSystems IRIS does the following:
    
    1.  Creates an instance of the business service class.
        
    2.  Supplies the most recently configured values of any of the business service’s settings
        
    3.  Invokes the business service’s `OnInit()` callback method (if present). The `OnInit()` method is an instance method that provides a convenient place to execute any initialization logic for a business service.
        
    4.  Creates an instance of the associated adapter class (if one is defined) and supplies the most recently configured values of any of the adapter’s settings.
        

### Runtime

While the production is running, the business service repeatedly calls the inbound adapter’s `OnTask()` method. This OnTask loop is controlled by the business service’s `CallInterval` setting and `%WaitForNextCallInterval` property as follows:

1.  The business service calls the inbound adapter’s `OnTask()` method.
    
2.  `OnTask()` checks outside the InterSystems IRIS production for input events of interest to the business service:
    
    *   If it finds input, `OnTask()` calls the internal `ProcessInput()` method of the associated business service object.
        
    *   If it does not find input, `OnTask()` returns control to the business service, which waits for the next `CallInterval` to elapse before returning to step 1.
        
    *   Multiple input events may exist. For example, if the business service uses `File.InboundAdapter`, there may be several files waiting in the designated directory.
        
        If there are multiple input events:
        
        *   Typically, the `OnTask()` method calls the `ProcessInput()` method as many times as is necessary to process all the available input events until no more are found.
            
        *   Alternatively, an inbound adapter can restrict `OnTask()` to call `ProcessInput()` only once per `CallInterval`, even if multiple input events exist. Rather than processing all the input events, `OnTask()` goes to sleep after processing the first event found.
            
3.  The internal `ProcessInput()` method sets the business service `%WaitForNextCallInterval` property to 0 (false) and calls `OnProcessInput()` to handle the input event.
    
4.  Upon completion, the internal `ProcessInput()` method returns control to `OnTask()`.
    
5.  At this point, `OnTask()` may set `%WaitForNextCallInterval` to 1 (true). This restricts the business service to processing only one input event per `CallInterval`, even when multiple input events exist.
    
    Usually you want the business service to process all available input events without delay, so usually you do not want to do anything to change `%WaitForNextCallInterval` at this step. It should retain the 0 (false) value set by the internal `ProcessInput()` method.
    
    The adapter base class Ens.InboundAdapter has an `OnTask()` method that calls the internal `ProcessInput()` method, sets `%WaitForNextCallInterval` to 1, and returns.
    
    > **Tip:**
    > 
    > If you simply want a business service to wake up and run its `ProcessInput()` method once per `CallInterval` without concern for events outside InterSystems IRIS, use the adapter class Ens.InboundAdapter.
    
6.  `OnTask()` returns.
    
7.  The business service tests the value of its `%WaitForNextCallInterval` property:
    
    *   If 1 (true), the business service waits for the `CallInterval` to elapse before returning to step 1.
        
    *   If 0 (false), the business service immediately returns to step 1. The `CallInterval` does not come into play until `OnTask()` discovers there is no more input (see step 2).
        

### Production Shutdown

When a production stops, the following events related to business services occur:

1.  InterSystems IRIS disables each business service; no more incoming requests are accepted for this production.
    
2.  The `OnTearDown()` method in each inbound adapter is called.
    
3.  All inbound adapter and business service objects are destroyed and their background processes are killed.
    
4.  Each business service’s `OnProductionStop()` class method is called, once for each configured item of that class in the production.
    

When a business service is disabled by a system administrator, or becomes inactive according to its configured schedule, the production continues to run but the associated inbound adapter is shut down, and its `OnTearDown()` method is executed.

## Life Cycle of a Business Process

Each time a production starts, InterSystems IRIS creates the public actor pool for the production. The value of the `ActorPoolSize` setting determines the number of jobs in the pool.

Within each job in the actor pool, there is an instance of an Ens.Actor object whose responsibility it is to manage the use of its job by business processes. This Ens.Actor instance is called an actor.

The business processes in a production can share the public message queue called Ens.Actor. This public queue is the target of all messages sent to any business process within a production that does not have its own, private queue. Actors listen on the Ens.Actor queue whenever they are free to host a business process. When a request arrives on the Ens.Actor queue, any actor that is free may assign its job to host the business process named in the request. Requests on the Ens.Actor queue are processed in the order in which they are received. Each successive request is claimed by the next available actor, on an ongoing basis.

For information on pools, see Pool Size and Actor Pool Size.

Unlike the lifecycle of business services and business operations, the `OnInit` and `OnTearDown` methods of a business process are not called when the business process is started or stopped. Rather, these methods are executed every time a request is processed by the business process (InProc or Queued). You can implement the `OnProductionStart` method of the business process class to execute custom code when the production is started or when the business process is restarted. The class’ `OnProductionStop` method is called when the production is stopped.

### Life Cycle in the Public Queue

The life cycle of a business process that uses the public queue is as follows:

1.  The initial request is addressed to the business process. The request message arrives on the Ens.Actor queue.
    
2.  As soon as an actor becomes available, it pulls the request message off the Ens.Actor queue.
    
3.  The actor creates a new instance of the appropriate business process class. The `OnInit()` method of the business process is invoked. The actor supplies the most recent values of the settings of the business process and invokes the `OnRequest()` method of that instance. The business process instance is now ongoing.
    
4.  While the business process instance is ongoing, whenever it is not active (for example, while it is waiting for input or feedback), it generally returns control to the actor that instantiated it. When this happens:
    
    1.  The actor suspends the business process instance.
        
    2.  The actor saves the current state of the instance to disk.
        
    3.  The actor returns its job to the actor pool.
        
5.  Whenever an ongoing business process has no assigned actor and a subsequent request or response arrives addressed to the business process (for example, when the anticipated input or feedback arrives) the following sequence occurs:
    
    1.  When an actor becomes available, it pulls the new request or response message from the Ens.Actor queue.
        
    2.  The actor restores the corresponding business process object from disk, complete with all of its state information.
        
    3.  The actor invokes the `OnRequest()` or `OnResponse()` instance method, as appropriate.
        
6.  After the business process instance completes execution, its current actor invokes its `OnComplete()` method and marks the instance with the status of IsComplete. The actor also returns its job to the actor pool. No further events are sent to this business process instance. The business process’ `OnTearDown` method is invoked.
    

### Life Cycle in a Private Queue

Alternatively, you can configure business processes to have private queues, bypassing the public Ens.Actor queue. The life cycle of a business process with a private queue runs exactly as described for a public queue, except that:

*   The business process runs in jobs from the private pool only.
    
*   The messages addressed to this business process arrive on its own, private queue, and do not arrive on the Ens.Actor queue.
    

## Life Cycle of a Business Operation and Adapter

InterSystems IRIS automatically manages the life cycle of each business operation.

### Production Startup

When you start a production (or change the configuration of a specific business operation), InterSystems IRIS automatically performs the following tasks for each configured business operation class (that is, for every business operation listed in the production definition):

1.  It invokes the class’ `OnProductionStart()` callback method, if defined.
    
    The `OnProductionStart()` method is a class method that is invoked once for each business operation class listed in the production configuration. A business operation class can use this callback to perform any class-wide initialization it may require.
    
2.  It creates one or more background processes in which to execute the business operation.
    
    The number of background processes is determined by the business operation’s `PoolSize` property within the production configuration. Each background process is referred to as an instance of the business operation and contains an instance of a business operation object.
    
    InterSystems IRIS will only create a background process for a business operation if the following conditions are true:
    
    *   The business operation class must set its `INVOCATION` class parameter to Queue.
        
    *   The business operation’s `Enabled` property within the production configuration must be set to 1 (otherwise the business operation is considered to be disabled). A disabled business operation still has an incoming message queue. Any requests posted to this queue will not be processed until the business operation is enabled.
        
    *   The business operation’s `PoolSize` property within the production configuration must be set to a value greater than 0.
        
    
    If the business operation’s `Foreground` property within the production configuration is set to 1, then InterSystems IRIS will create a foreground process (that is, it will create a Terminal window) for the business operation. This feature facilitates testing and debugging.
    
3.  It initializes the system monitoring information used to monitor the status and operating history of the business operation.
    
4.  Within each background process:
    
    1.  InterSystems IRIS creates an instance of the business operation class, supplies the most recently configured values of any of the business operation’s settings, and invokes the business operation `OnInit()` callback method (if present). The `OnInit()` method is an instance method that provides a convenient place to execute any initialization logic for a business operation.
        
    2.  InterSystems IRIS creates an instance of the associated adapter class (if one is defined) and supplies the most recently configured values of any of the adapter’s settings.
        

### Runtime

At runtime, a business operation does the following:

1.  It waits for requests to be sent (from business services, business processes, and other business operations) to its associated message queue.
    
2.  After the business operation retrieves a request from its message queue, it searches its message map for the operation method that corresponds to the request type. It then invokes that operation method.
    
3.  The operation method, using the data within the request object, makes a request to an external application. Typically it does this by calling methods of its associated outbound adapter object.
    

### Production Shutdown

When a production stops, the following events related to business operations occur:

1.  InterSystems IRIS waits for each business operation to reach a quiescent state (that is, InterSystems IRIS waits until each business operation has completed all of its synchronous requests).
    
2.  The `OnTearDown()` method in each outbound adapter is called.
    
3.  All outbound adapter and business operation objects are destroyed and their background processes are killed.
    
4.  Each business operation’s `OnProductionStop()` class method is called, once for each configured item of that class in the production.
    

When a business operation is disabled by a system administrator, or becomes inactive according to its configured schedule, the production continues to run but the associated outbound adapter is shut down, and its `OnTearDown()` method is executed.
