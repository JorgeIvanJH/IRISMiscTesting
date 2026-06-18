# Defining Messages

This page describes how to define classes to contain message bodies for an InterSystems IRIS data platform interoperability production.

## Types of Message Bodies

A message body class must be a persistent class; messages sent by a production are all stored in the database until a system administrator purges them. There are two general types of message body classes, standard message bodies and virtual documents. The distinction is that a standard message body contains multiple properties that contain the message data, and a virtual document stores the complete message data in serialized form. Standard message bodies are suitable when the messages always have the same form. When the data is arbitrarily long or complex, it is necessary to use virtual documents instead. For Electronic Data Interchange (EDI) formats, InterSystems IRIS uses virtual documents.

In either case, InterSystems IRIS provides tools to enable you to access specific elements within the message, for the purposes of data transformation, routing, or business rules.

A standard message body can be simple (containing only non-object properties) or can be complex (containing object-valued properties).

For information on virtual documents, see Using Virtual Documents in Productions. The rest of this page discusses only standard message bodies.

## Creating a Simple Message Body Class

To create a simple standard message class, create a class that:

*   Extends %Persistent.
    
    Note that in general it is important to consider how the messages will be stored, in particular to make sure that messages of different types are stored in different tables, for best performance when searching messages. See Message Storage, which also describes alternative approaches to creating a simple standard message class.
    
*   Also extends either Ens.Util.RequestBodyMethods or Ens.Util.ResponseBodyMethods, depending on whether the class is to be used as a request message or a response message, respectively. If you use these classes, you have easy access to the various built-in features for viewing the contents of messages from the Management Portal. These features help developers and administrators detect errors in a running production, especially if the production uses message content to determine where the message should be sent.
    
*   Optionally also extends %XML.Adaptor. In this case, the Management Portal can display the full message in XML format. Also see Controlling the Display.
    
*   Contains properties as needed to represent elements of data to be carried in the message.
    
*   Optionally specifies a value for the `ENSPURGE` parameter; see Specifying Message Purge Behavior.
    

The following shows a simple example:

```objectscript
Class Demo.Loan.Msg.CreditRatingResponse Extends (%Persistent, Ens.Util.ResponseBodyMethods)
{

Property TaxID As %String;

Property CreditRating As %Integer;

}
```

The class can also contain methods. For example:

```objectscript
Class Demo.Loan.Msg.Application Extends (%Persistent, Ens.Util.RequestBodyMethods)
{

Property Amount As %Integer;

Property Name As %String;

Property TaxID As %String;

Property Nationality As %String;

Property BusinessOperationType As %String;

Property Destination As %String;

Method RecordNumber() As %String
{
  If ..%Id()="" Do ..%Save()
  Quit ..%Id()
}

Method GetRecordNumberText(pFormatAsHTML As %Boolean = 0) As %String
{
  Set tCRLF=$s(pFormatAsHTML:"<br>",1:$c(13,10))
  Set tText=""
  Set tText=tText_"Your loan application has been received,"_tCRLF
  Set tText=tText_"and is being processed."_tCRLF
  Set tText=tText_"Your record number is "_..RecordNumber()_"."_tCRLF
  Set tText=tText_"You'll receive a reply from FindRate"_tCRLF
  Set tText=tText_"within 2 business days."_tCRLF
  Set tText=tText_"Thank you for applying with FindRate."_tCRLF
  Quit tText
}

}
```

## Message Storage

It is important to store messages of different types in different globals, for best performance when searching messages. To achieve this goal, you can use any of the following approaches:

*   A message class can extend %Persistent and Ens.Util.RequestBodyMethods or Ens.Util.ResponseBodyMethods, as described previously.
    
*   A message class can extend %Persistent and then Ens.Request or Ens.Response.
    
    > **Important:**
    > 
    > When using multiple persistent superclasses, as in this case, the order of superclasses is important. If Ens.Request or Ens.Response is listed first, the messages will be saved in the same global that stores all other requests or responses, and this can adversely affect performance when querying the message tables. In contrast, if %Persistent is listed first, the messages are saved in their own global and their own table.
    
*   A message class can extend any persistent class and can use the `USEEXTENTSET` and `DEFAULTGLOBAL` class parameters, which provide other ways of ensuring that the data is stored in its own global and its own table; for details, see the class reference for %Persistent.
    

## Controlling the Display

In the Management Portal, both the Message Viewer and the Visual Trace provide two tabs that display the message body:

*   The `Body` tab displays the message body as a table, with one column representing properties of the message class, and the second column displaying the corresponding values. This table does not display any object-valued properties.
    
    By default, this table cannot display more than 99 properties. To increase the number of properties that it can display, enter the following command in the ObjectScript shell in the namespace where this maximum should be increased:
    
    ```objectscript
     set ^CSP.AutoFormMaxProperties=newmaximum
    ```
    
    Where `newmaximum` is an integer that specifies the maximum number of properties to display. (This change also affects the testing service input form form.)
    
*   The `Contents` tab displays the message body in serialized form, if possible. If the message class inherits from %XML.Adaptor, this tab displays the message in XML format.
    

If you want to override this display, you can do so by defining `%GetContentType()` and `%ShowContents()` in your message class. For information, see the class reference for Ens.Util.MessageBodyMethods.

## Creating a Complex Message Body Class

In the previous example, the message body class contained only simple properties. In some cases, you may need to define properties that use other classes. If so, you should carefully consider what to do when you purge message bodies (as described in Purging Data).

When you purge message bodies, InterSystems IRIS deletes only the specific message body object. For example, consider the following message class:

```objectscript
Class MyApp.Messages.Person Extends Ens.Util.RequestBodyMethods
{

Property Name As %String;

Property MRN As %String;

Property BirthDate As %Date;

Property Address As MyApp.Messages.Address;

}
```

The `Address` class is as follows:

```objectscript
Class MyApp.Messages.Address Extends %Persistent
{

Property StreetAddress As %String;

Property City As %String;

Property State As %String;

Property ZIP As %String;

}
```

In this case, if you purge message bodies, InterSystems IRIS deletes instances of `MyApp.Messages.Person`, but does not delete instances of `MyApp.Messages.Address`.

If your message body class uses other classes as properties and if your application requires that any referenced objects should also be purged, use one of the following approaches:

*   Make sure that the referenced classes are serial. For example, redefine the `Address` class as follows:
    
    ```
    Class MyApp.Messages.Address Extends %SerialObject
    {
    ...
    }
    ```
    
    In this case, the data for the `Address` class is stored as part of the `Person` class (and is thus automatically purged at the same time).
    
*   Define the property as a suitable relationship. See Relationships.
    
*   Add a delete trigger or `%OnDelete()` method to the message class so that this class deletes the appropriate records in the referenced classes.
    
*   Optionally include %XML.Adaptor as a superclass so that the properties defined in the referenced class can be displayed in the Management Portal.
    

## Specifying Message Purge Behavior

When you define a message body class, you can include the `ENSPURGE` parameter to specify how InterSystems IRIS handles instances of the class during purge operations. The parameter has two possible values:

*   `0`—InterSystems IRIS does not purge message bodies based on the class, even when the option to purge message bodies is enabled.
    
*   `1`—InterSystems IRIS purges message bodies based on the class when the option to purge message bodies is enabled.
    

The `ENSPURGE` parameter affects all purges from the Management Portal, except for purges of the Enterprise Message Bank. Similarly, it affects programmatic purges using the `Purge()` method of the Ens.MessageHeader class.

For example, consider the `Sample.Person` persistent database class:

```objectscript
Class Sample.Person Extends (%Persistent, %Populate, %XML.Adaptor)

{
Property Name As %String(POPSPEC = "Name()") [ Required ];

Property SSN As %String(PATTERN = "3N1""-""2N1""-""4N") [ Required ];

Property DOB As %Date(POPSPEC = "Date()");

//...
}
```

If you configure a production to send `Sample.Person` objects to a business operation that updates patient information, it might be important to retain the objects. To ensure that the system does not purge any instances of the `Sample.Person` message body class, you could add the `ENSPURGE` parameter to the class definition as follows:

```objectscript
Class Sample.Person Extends (%Persistent, %Populate, %XML.Adaptor)

{
Parameter ENSPURGE As %Boolean = 0;

Property Name As %String(POPSPEC = "Name()") [ Required ];

Property SSN As %String(PATTERN = "3N1""-""2N1""-""4N") [ Required ];

Property DOB As %Date(POPSPEC = "Date()");

//...
}
```

During subsequent purges, the system removes only the headers of messages based on the `Sample.Person` message body class. The message bodies are essentially orphaned and can be removed only programmatically. For more information, see Purging Production Data.

The `ENSPURGE` parameter is inheritable and is not required. The default value is `1`.

## See Also

*   Using Virtual Documents in Productions
    
*   Purging Production Data
