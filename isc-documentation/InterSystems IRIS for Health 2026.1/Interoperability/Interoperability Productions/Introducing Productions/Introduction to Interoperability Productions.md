# Introduction to Interoperability Productions

The purpose of interoperability productions is to enable you to connect systems so that you can transform and route messages between them. To connect systems, you develop, configure, deploy, and manage productions, which integrate multiple software systems. This topic introduces productions and some of the basic terminology.

## Production Basics

An interoperability production is an integration framework for easily connecting systems and for developing applications for interoperability. A production provides built-in connections to a wide variety of message formats and communications protocols. You can easily add other formats and protocols – and define business logic and message transformations either by coding or using graphic interfaces. Productions provide persistent storage of messages, which allow you to trace the path of a message and audit whether a message is successfully delivered. The elements in a production are known as business hosts. There are three kinds of business hosts, with different purposes as follows:

*   Business services connect with external systems and receive messages from them. Business services relay the messages to other business hosts in the production.
    
*   Business processes allow you to define business logic, including routing and message transformation. Business processes receive messages from other business hosts in the production and either process the requests or forward them to other business hosts.
    
*   Business operations connect with external systems and send the messages to them. Business operations receive messages from other business hosts in the production and typically send them to external systems.
    

The following figure provides a conceptual overview of a production and business hosts.

[Image: Diagram of messages flowing from external systems through various business hosts in a production to other external systems]

Business hosts communicate with each other via messages. All messages are stored in the InterSystems IRIS database and can be seen via the Management Portal.

In most cases (but not all), a business service has an associated inbound adapter. The role of an inbound adapter is to accept input from entities external to the production. Similarly, a business operation usually has an associated outbound adapter. The role of an outbound adapter is to send output to entities external to the production. InterSystems IRIS provides a large set of adapters to handle different technologies. For example, you use a different adapter for files than you do for FTP. It is also possible to define your own adapters.

The following figure shows an actual production, as seen in the Management Portal:

[Image: Production Configuration page showing connections between a business process and various business services and operations]

## Settings

A production typically includes a large number of settings. Settings are configurable values that control the behavior of a production. Settings can affect a production in many ways. For example, a setting can specify:

*   The TCP port on which a business service should listen.
    
*   How frequently to check for new input.
    
*   The external data source name (DSN) to use.
    
*   The TLS configuration to use when connecting to an external entity.
    
*   How long to stay connected.
    
*   And so on.
    

An important feature of InterSystems IRIS is that a system administrator can modify settings while a production is running. The changes take effect immediately. The following shows an example of the web page that the system administrator uses to make such changes:

[Image: Setting tab of the Production Configuration page for a file service]

The production and its business hosts have settings provided by InterSystems IRIS; they correspond to properties of the production and business host classes. You can define additional settings in exactly the same way, by defining your own subclasses of InterSystems IRIS classes. You can also remove settings so that the corresponding properties are hardcoded and not configurable.

## Message Flow in a Production

An interoperability production typically processes incoming events as follows:

1.  An inbound adapter receives an incoming event, transforms it into a message object, and passes it to its associated business service.
    
2.  The business service creates a follow-on request message, and passes this new message to a business process or business operation within the production.
    
3.  A business process that receives a request message executes a predefined set of activities, in sequence or in parallel. These activities may include sending follow-on messages to other business hosts. Business processes are also responsible for most or all of the business logic in the production.
    
4.  A business operation encapsulates the capabilities of a resource outside InterSystems IRIS, usually an external software application. The business operation transforms properties of the request message object into a format usable by the external application API.
    
5.  An outbound adapter manages the details of communicating with a specific external system or application from within the production. It transmits the API call to the external entity.
    
6.  The response from the external system or application can trigger a cascade of response messages back to the external entity that started the flow of events. Details depend on the design choices made by the production developers.
    

As a demonstration, the following figure shows a trace of a set of related messages, which a production sent in response to an initial message (in this case sent by the testing service in the Management Portal rather than by an exterior source):

[Image: Message trace illustrating the flow f a message from a business service to various business processes and operations]

The processing can also include workflow, which makes it possible to incorporate human interaction into automated business processes. Uses of workflow within the enterprise might include order entry, order fulfillment, contract approval, or help desk activities. Other Production Options provides more information.
