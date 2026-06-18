# Business Processes and Business Logic

This topic describes the kinds of logic supported in business processes in interoperability productions.

## Introduction

Business processes are the middle part of any production. They accept requests from host classes inside the production —business services or business processes—and then either process the requests or relay them to other host classes inside the production for processing.

InterSystems recommends the following division of labor within a production: Use business services to receive input from outside of the production and simply forward it (as messages) into the production. Use business processes to handle any needed business logic. Use business operations to receive messages from within the production and simply generate output for destinations outside of the production. That is, centralize the business logic within the business processes.

Accordingly, InterSystems IRIS provides extensive support for complex logic within business processes, and this logic can be defined by nontechnical users.

First, a business process can contain its own complex logic. It can also use the following reusable items:

*   Data transformations calculate and apply changes to message contents.
    
*   Business rules change the behavior of business processes at decision points or send messages to specific destinations based on message type, message contents, or where the message came from.
    

InterSystems IRIS provides tools that enable nontechnical users to define business processes, data transformations, and business rules. These users can view and edit the logic visually without programming or diagramming skills.

Note that there is overlap among the lower-level options available in business processes, data transformations, and business rules. For a comparison, see Comparison of Business Logic Tools. It is worthwhile to review these options before deciding how to organize your logic.

## Types of Business Processes

InterSystems IRIS provides the following general types of business process:

*   BPL processes, which are based on the class Ens.BusinessProcessBPL. To create these processes, you use a graphical editor that is intended for use by nontechnical users. See Developing BPL Processes.
    
    The name of these processes comes from BPL (Business Process Language), which is the XML-based language that InterSystems IRIS uses to represent their definitions.
    
*   Routing processes, which are based on the class EnsLib.MsgRouter.RoutingEngine or EnsLib.MsgRouter.VDocRoutingEngine.
    
    InterSystems IRIS provides a set of classes to route specific kinds of messages. The following links indicate the routing process to use for different kinds of messages:
    
    <table><tr><th>Message Type</th><th>See</th></tr><tr><td>EDIFACT</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EACT">Routing EDIFACT Documents in Productions</a></td></tr><tr><td>X12</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EX12">Routing X12 Documents in Productions</a></td></tr><tr><td>XML</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=EXML">Routing XML Virtual Documents in Productions</a></td></tr></table>
    
    To use these classes, no coding is generally necessary. It is, however, necessary, to provide a set of business rules.
    
*   Custom business processes, which are based on the class Ens.BusinessProcess. Note that all the previously listed business process classes inherit from this class. In this case, it is necessary to use a supported IDE to develop custom code.
    
    For information on defining custom business processes, see Developing Custom Business Processes.
    

A production can include any mix of these business processes.

The following shows a partial example of a BPL business process, as displayed in the BPL editor:

[Image: Business process in the BPL Editor that includes various actions and decision points]

## Data Transformations

A data transformation creates a new message that is a transformation of another message. You can invoke a data transformation from a business process, another data transformation, or a business rule.

When you transform a message, your data transformation swaps out the old message body object (the source) and exchanges it for a new one (the target). Some of the transformations that occur during this process can include:

*   Copying values from properties on the source to properties on the target.
    
*   Performing calculations using the values of properties on the source.
    
*   Copying the results of calculations to properties on the target.
    
*   Assigning literal values to properties on the target.
    
*   Ignoring any properties on the source that are not relevant to the target.
    

A data transformation is a class based on Ens.DataTransform or its subclass, Ens.DataTransformDTL.

*   If you use Ens.DataTransformDTL, the transformation is called a DTL transformation. To create these transformations, you use a graphical editor that is intended for use by nontechnical users. For details, see Developing DTL Transformations.
    
    The name of these transformations comes from DTL (Data Transformation Language), which is the XML-based language that InterSystems IRIS uses to represent their definitions.
    
*   If you use Ens.DataTransform, the transformation is a custom transformation. In this case, you must use a supported IDE. For information on defining these, see Developing Custom Data Transformations.
    

The following shows an example DTL transformation, as seen in the DTL editor:

[Image: DTL Editor section showing the mappings between a sample source message type and target message type]

## Business Rules

A business rule (also known as a business rule set) can return a value, transform data, or both. You can invoke a business rule from a business process or from another business rule.

A business rule is a class based on Ens.Rule.Definition. You define these in the Management Portal, which provides a visual editor for the benefit of nontechnical users. The following shows a partial example, as seen in this editor:

[Image: Business rule set that determines whether the send a message to a file operation]

For details, see Developing Business Rules.

## See Also

*   Comparison of Business Logic Tools
    
*   Developing BPL Processes
    
*   Developing Custom Business Processes
    
*   Developing DTL Transformations
    
*   Developing Custom Data Transformations
    
*   Developing Business Rules
