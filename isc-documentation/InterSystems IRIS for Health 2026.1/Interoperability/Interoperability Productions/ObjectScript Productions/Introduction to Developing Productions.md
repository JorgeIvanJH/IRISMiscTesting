# Introduction to Developing Productions

This page introduces the process of developing interoperability productions.

For information on how productions work, see Core Concepts When Monitoring Interoperability Productions.

## Environmental Considerations

You can use productions only within an interoperability-enabled namespace that has a specific web application. When you create classes, you should avoid using reserved package names. The following subsections give the details.

### Production-enabled Namespaces

An interoperability-enabled namespace is a namespace that has global mappings, routine mappings, and package mappings that make the classes, data, and menus that support productions available to it. For general information on mappings, see Configuring Namespaces. (You can use the information in that section to see the actual mappings in any interoperability-enabled namespace; the details may vary from release to release, but no work is necessary on your part.)

The system-provided namespaces that are created when you install InterSystems IRIS are not interoperability-enabled, except, on the community edition, the USER namespace is an interoperability-enabled namespace. Any new namespace that you create is by default interoperability-enabled. If you clear the `Enable namespace for interoperability productions` check box when creating a namespace, InterSystems IRIS data platform creates the namespace with productions disabled.

> **Important:**
> 
> All system-provided namespaces are overwritten upon reinstallation or upgrade. For this reason, InterSystems recommends that customers always work in a new namespace that you create. For information on creating a new namespace, see Configuring Data.

### Web Application Requirement

Also, you can use a production in a namespace only if that namespace has an associated web application that is named `/csp/namespace`, where namespace is the namespace name. (This is the default web application name for a namespace.) For information on defining web applications, see Applications.

### Reserved Package Names

In any interoperability-enabled namespace, avoid using the following package names: `Demo`, `Ens`, `EnsLib`, `EnsPortal`, or `CSPX`. These packages are completely replaced during the upgrade process. If you define classes in these packages, you would need to export the classes before upgrading and then import them after upgrading.

Also, InterSystems recommends that you avoid using any package names that start with `Ens` (case-sensitive). There are two reasons for this recommendation:

*   When you compile classes in packages with names that start with `Ens`, the compiler writes the generated routines into the `ENSLIB` system database. (The compiler does this because all routines with names that start with `Ens` are mapped to that database.) This means that when you upgrade the instance, thus replacing the `ENSLIB` database, the upgrade removes the generated routines, leaving only the class definitions. At this point, in order to use the classes, it is necessary to recompile them.
    
    In contrast, when you upgrade the instance, it is not necessary to recompile classes in packages with names that do not start with `Ens`.
    
*   If you define classes in packages with names that start with `Ens`, they are available in all interoperability-enabled namespaces, which may or may not be desirable. One consequence is that it is not possible to have two classes with the same name and different contents in different interoperability-enabled namespaces, if the package name starts with `Ens`.
    

## A Look at a Production Definition

Although you create and configure productions in the Management Portal, it is instructive to get started by looking at the definition of a existing production class in your choice of IDE. This following shows a simple example of a production:

```xml
Class Demo.FloodMonitor.Production Extends Ens.Production
{

XData ProductionDefinition
{
<Production Name="Demo.FloodMonitor.Production">
  <ActorPoolSize>1</ActorPoolSize>
  <Item Name="Demo.FloodMonitor.BusinessService"
        ClassName="Demo.FloodMonitor.BusinessService"
        PoolSize="1" Enabled="true" Foreground="false" InactivityTimeout="0">
  </Item>
  <Item Name="Demo.FloodMonitor.CustomBusinessProcess"
        ClassName="Demo.FloodMonitor.CustomBusinessProcess"
        PoolSize="1" Enabled="true" Foreground="false" InactivityTimeout="0">
  </Item>
  <Item Name="Demo.FloodMonitor.GeneratedBusinessProcess"
        ClassName="Demo.FloodMonitor.GeneratedBusinessProcess"
        PoolSize="1" Enabled="true" Foreground="false" InactivityTimeout="0">
  </Item>
  <Item Name="Demo.FloodMonitor.BusinessOperation"
        ClassName="Demo.FloodMonitor.BusinessOperation"
        PoolSize="1" Enabled="true" Foreground="false" InactivityTimeout="0">
  </Item>
</Production>
}
}
```

Note the following points:

*   The production is a class, specifically is a subclass of Ens.Production.
    
*   The XData ProductionDefinition block holds the configuration information for the production.
    
*   Each <Item> is a business host; these are also called configuration items.
    
*   Each business host refers to a class. ClassName specifies the class on which this host is based. This means that when the production creates an instance of this business host, it must create an instance of the specified class.
    
*   The Name of a business host is an arbitrary string. Sometimes, it can be convenient to use the class name for this purpose, as in this example. This convention does not work when you create a large number of business hosts that use the same class.
    
    It is important to establish naming conventions at an early point during development. See Best Practices for Creating Productions. An absence of naming conventions will lead to confusion.
    
*   The other values in the XData block are all settings. At the top, <ActorPoolSize> is a setting for the production. Within the business host definitions, PoolSize, Enabled, Foreground, and InactivityTimeout are settings for those business hosts.
    

## Development Tools and Tasks

Productions consist primarily of class definitions and some supporting entities. The process of creating a production can require a small amount of programming or possibly a large amount, depending on your needs. As noted earlier, InterSystems IRIS provides graphical tools that enable nontechnical users to create business logic visually. These tools generate class definitions as needed.

While you develop a production, you use both the Management Portal and your choice of IDE as follows.

### Portal Tasks

In the Management Portal, you use UIs to define and compile the following:

*   Productions
    
*   BPL business processes
    
*   DTL transformations
    
*   Business rules
    

You also use the Management Portal for the following additional tasks:

*   Defining reusable items for use in settings; these include production credentials, business partners, and so on. See Configuring Productions.
    
*   Starting and stopping the production. See Starting and Stopping Productions.
    
*   Examining the message flow, as part of your testing and debugging process. See Monitoring Productions.
    
*   Testing specific business hosts. See Testing and Debugging.
    

### IDE Tasks

In an IDE, you define and compile the following classes:

*   Message classes.
    
*   Business service classes. Note that InterSystems IRIS provides business service classes that directly use specific adapters. You might be able to use one of them rather than create your own.
    
*   Custom business Process classes.
    
*   Business operation classes. Note that InterSystems IRIS provides business operation classes that directly use specific adapters. You might be able to use one of them rather than create your own.
    
*   Custom data transformation classes.
    
*   Custom adapter classes. See Less Common Tasks.
    

Also see other topics in Less Common Tasks.

## Available Specialized Classes

InterSystems IRIS provides many specialized adapter and business host classes that can reduce your development and testing time. For a summary of the most common options, see Other Production Options.
