# [Setting Up a New Feeder Gateway](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

This chapter describes how to set up a new Feeder Gateway, with optional mirroring. If you have already configured your Feeder Gateway and want to migrate it to use mirroring, see the chapter “[Migrating the Feeder Gateway to Use Mirroring](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAMIG_migfeeder)” instead.

> **Important:**
> 
> If you plan to use mirroring, then before you begin, InterSystems strongly recommends that you read and understand the [Mirroring](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror) chapter of the InterSystems IRIS data platform High Availability Guide. It contains important information about network and deployment considerations that you must plan for before you install and configure a mirrored HealthShare Health Insight. When reading the chapter, keep in mind that you will be configuring a mirror that:
> 
> *   has two failover members
>     
> *   uses a VIP (Virtual IP address)
>     
> *   uses an arbiter and an ISCAgent
>     
> *   uses SSL/TLS
>     

> **Note:**
> 
> Also, if you plan to use mirroring, be sure to plan for the following:
> 
> *   A second machine on the same subnet as your existing Feeder Gateway to host the second failover mirror member.
>     
> *   A machine to host the arbiter.
>     
> *   X.509 certificates for SSL/TLS encryption of mirrored communication.
>     
> *   A Virtual IP address for the mirror.
>     

To create a new Feeder Gateway (with or without mirroring), follow the steps outlined below and detailed in the sections that follow:

1.  [Use the installer](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_install).
    
2.  [Optionally set up mirroring for the instance](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_mirrorsetup).
    
3.  [Create the Feeder Gateway production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_production).
    
4.  [Configure the Feeder Gateway production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_config).
    
5.  [Create a custom business host on the Registry to handle AnalyticsQRequest messages](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_analyticsqrequest).
    
6.  [Set up production message purge](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_purge).
    

## [Step 1: Use the Installer](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_install)

If you have not already done so, install one or two instances of HealthShare, depending on whether you plan to mirror the Feeder Gateway. In either case, follow the steps outlined in the chapter “[Installing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_install).”

If you want to use mirroring, install two instances that are on separate machines. Keep in mind the following:

*   The machines hosting the instances must be on the same subnet.
    
*   Use the same superserver port and web server port. Record these values as you will need them in a later step.
    
*   Designate one instance as instance A and the other as instance B. As you follow the instructions in this document, these designations will make the instructions easier to follow.
    

> **Note:**
> 
> Record the instance name, superserver port, and web server port of each instance, as you will need them in a later step.

Instance A and instance B will be your two failover members.

Or, if you do not plan to mirror Feeder Gateway, install only one instance.

## [Step 2: Set Up Mirroring for the Feeder Gateway Instance](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_mirrorsetup)

If you are using mirroring, set up mirroring before creating the Feeder Gateway production. (Otherwise skip to the [next section](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_production).)

For details on this step, see “[Mirroring a New Unified Care Record System](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEMRR_ch_mirroring#HEMRR_ch_Mirroring)” in Mirroring Unified Care Record. You have already installed the instances, so start with the step that follows installation. From that chapter, the last step to perform is defining the ^ZMIRROR routine on both instances.

## [Step 3: Create the Feeder Gateway Production](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_production)

Whether or not you are using mirroring, it is necessary to use the HealthShare Installer Wizard to create the Feeder Gateway production. (Note that if you are using mirroring, do this only on the primary instance.)

The steps are as follows:

1.  Open the Management Portal, select the `HealthShare` tab and then select the `Installer Wizard` link at the top left of the screen.
    
2.  Select `Configure Access Gateway` and specify values as follows:
    
    *   `Local Name` — This string is used as the namespace name.
        
    *   `Template` — [HS.Sample.Production.AccessGateway.AnalyticsFeedProduction](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Sample.Production.AccessGateway.AnalyticsFeedProduction).
        
    *   `Enter a Hub Host` — Name of the server that hosts the Registry.
        
    *   `Enter a Hub Port` — Port of the HealthShare instance that hosts the Registry.
        
    *   `Enter a Hub Name` — Namespace in which the Registry is running.
        
    *   For `Connect to Hub Securely`, select this if this is a production system. Optionally select it for a development or test system.
        
        *   The web server on your Registry instance should be configured to only allow secure connections to the Registry.
            
        *   You should have an SSL/TLS configuration on this instance that can communicate with the Registry (see [Create an SSL/TLS Configuration for each Instance in the Federation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ASecureComm#ASecureComm_ssl_configuration) in Setting Up Secure Communication in HealthShare Instances). This SSL/TLS configuration should have the same name as the SSL/TLS configuration on the Registry instance, as all instances in a federation share a single service registry, and the HSREGISTRY service registry entry identifies which SSL/TLS configuration to use.
            
        
        Once you select `Connect to Hub Securely`, enter the SSL/TLS configuration in the `SSL Configuration` field that appears. Now, the Hub endpoint URL will be created using “https” rather than “http”, and the identified SSL/TLS configuration will allow the Gateway to connect to the registry securely at initial startup.
        
    *   `Alternate Database Location` — A location for the production database other than the default. The default location for the production database, `IRIS.DAT`, is `installDir/mgr/localName`. To specify a location for the database other than the default, enter the alternate location in the `Alternate Database Location` field. If you specify an absolute location, then that location will be created if it does not exist. Your database will be in `alternateDatabaseLocation/localName`. If you specify a relative location then the database will be created in `installDir/mgr/hslib/alternateDatabaseLocation/localName`.
        
3.  Select `Save`.
    
4.  Select the `Activate` button in the newly added row and wait for the activation to complete.
    

## [Step 4: Configure the Feeder Gateway Production](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_config)

Whether or not you are using mirroring, it is necessary to configure the Feeder Gateway production. (Note that if you are using mirroring, you should perform the following steps only on the primary instance, with the exception of step 3. Since mirroring does not keep files in local filesystems synchronized, step 3 must be performed on all mirror members, so that all Feeder instances have identical `AnonymizationConfig.xml` files.)

The steps are as follows:

1.  Display the Feeder Gateway production in the Management Portal.
    
2.  Optionally modify the following setting of [HS.Gateway.Analytics.TransmitService](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.TransmitService):
    
    <table><tr><th>Setting</th><th>Purpose</th></tr><tr><td><code>Call Interval</code></td><td>Specifies the interval, in seconds, at which this production will send new data to Health Insight. The default is 300.</td></tr></table>
    
3.  Review the anonymization configuration. If any changes are needed, create a custom file by following the instructions below.
    
    By default, the anonymization configuration file does not perform any anonymization of data.
    
    You can modify the anonymization configuration file to cause the Feeder Access Gateway to remove the MPIID and other patient identifiers from the data that it sends to Health Insight; the resulting data may not have enough content to support useful analysis. To customize what is removed, copy the following XML configuration file on the machine that is running the Feeder Access Gateway:
    
    ```
    install-directory/csp/xslt/SDA3/Analytics/AnonymizationConfig.xml
    ```
    
    Paste the file to the following location:
    
    ```
    install-directory/csp/xslt/SDA3/Analytics/Custom/AnonymizationConfig.xml
    ```
    
    Where `install-directory` is the directory where you installed the Feeder Gateway HealthShare instance.
    
    Make any changes to this file that you need. Files in the `Custom` folder are not overwritten on an upgrade.
    
    Also see the `SampleAnonymizationConfig.xml`, which is a sample that shows how to make use of the anonymization feature of Health Insight.
    
    The custom anonymization configuration file must be named `AnonymizationConfig.xml` and it must have specific XML contents. The required root element is `<AnonymizationConfig>`, which contains one `<Anonymizations>` element. The `<Anonymizations>` element can contain any number of `<AnonymizationInfo>` elements, each of which specifies how to anonymize a specific type of streamlet, which is a unit or subunit of data that HealthShare Unified Care Record can send.
    
    `<AnonymizationInfo>` contains the following elements:
    
    ### [`<StreamletType>`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_C13834)
    
    Use one of the streamlet types listed below. Each streamlet type corresponds to a class of the same name, within the package `HS.SDA3.Streamlet` and obtains its properties from a persistent class of the same name in the package `HS.SDA3`. For example, `Patient` corresponds to the streamlet class [HS.SDA3.Streamlet.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSLIB&CLASSNAME=HS.SDA3.Streamlet.Patient), which obtains its properties from the persistent class [HS.SDA3.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSLIB&CLASSNAME=HS.SDA3.Patient).
    
    <table><tr><td><p>Patient</p><p>(The basic patient information)</p></td><td><p>GenomicsOrder</p><p>(not used in Health Insight)</p></td><td>PharmacyExplanationOfBenefit</td></tr><tr><td>AdvanceDirective</td><td>Goal</td><td>PhysicalExam</td></tr><tr><td>Alert (deprecated)</td><td>HealthConcern</td><td>Problem</td></tr><tr><td>Allergy</td><td>IllnessHistory</td><td>Procedure</td></tr><tr><td>Appointment</td><td><p>LabOrder</p><p>(includes lab results)</p></td><td><p>ProgramMembership</p><p>(not used in Health Insight)</p></td></tr><tr><td>CarePlan</td><td>MedicalExplanationOfBenefit</td><td><p>RadOrder</p><p>(not used in Health Insight)</p></td></tr><tr><td>ClinicalRelationship</td><td>Medication</td><td>Referral</td></tr><tr><td><p>DeviceItem</p><p>(not used in Health Insight)</p></td><td>MemberEnrollment</td><td>SocialDeterminant</td></tr><tr><td>Diagnosis</td><td>Observation</td><td>SocialHistory</td></tr><tr><td>Document</td><td>ObservationGroup</td><td>Vaccination</td></tr><tr><td>Encounter</td><td><p>OtherOrder</p><p>(not used in Health Insight)</p></td><td>&nbsp;</td></tr><tr><td>FamilyHistory</td><td>PharmacyClaim</td><td>&nbsp;</td></tr></table>
    
    ### [`<AnonymizationType>`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_C13846)
    
    Specifies the kind of anonymization to perform for this type of streamlet. Use one of the following values:
    
    *   `SomeProperties` — Use this value if you plan to list the properties for the Feeder Access Gateway to remove before it sends data to Health Insight.
        
    *   `AllData` — Use this value to remove all data within this type of streamlet before it sends data to Health Insight.
        
    *   `XSLT` — Use this value if you plan to use a custom XSLT transform to perform the anonymization.
        
    *   `Class` — Use this value if you plan to create and use a custom class method to perform the anonymization.
        
    
    ### [`<Properties>`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_C13849)
    
    Include this element only if you used `XSLT` for `<AnonymizationType>`. In this case, for `<XSLTFile>`, specify the name of the XSLT transformation file to apply to this streamlet type. This file would be in the same directory as this configuration file or in the equivalent Site directory.
    
    ### [`<XSLTFile>`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_C13852)
    
    Include this element only if you used `Class` for `<AnonymizationType>`. In this case, for `<ClassName>`, specify the name of your custom class with a class method named `Anonymize`. This class method will be applied to this streamlet type.
    
    ### [`<ClassName>`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_C13856)
    
    Create the custom class on your Feeder Gateway HealthShare instance. The `Anonymize` method should have a signature like the following:
    
    ```objectscript
    ClassMethod Anonymize (pSDAString As %String, Output pAnonymizedString As %String, pProperties As %String) {}
    ```
    
    The following shows part of this sample file:
    
    ```xml
    <AnonymizationInfo>
      <StreamletType>LabOrder</StreamletType>
      <AnonymizationType>SomeProperties</AnonymizationType>
      <Properties>Result/ResultText,DocumentName,Stream,DocumentURL,DocumentNumber,
            Result/Comments,Result/ResultItems/LabResultItem/Comments</Properties>
    </AnonymizationInfo>
    ```
    
    The following shows an example custom class with an `Anonymize` method, which you might use if you chose an `AnonymizationType` of `Class`:
    
    ```objectscript
     Class HS.Custom.PatientAnon
     {
    
      ClassMethod Anonymize(
              pSDAString As %String,
              Output pAnonymizedString As %String,
              pProperties As %String
                            ) As %Status
      {
       #DIM reader As %XML.Reader = ##class(%XML.Reader).%New()
       #DIM patient As HS.SDA3.Patient
       #DIM doctor As HS.SDA3.CodeTableDetail.FamilyDoctor
       #DIM address As HS.SDA3.Address
    
       /// use the XML reader
       set sc = reader.OpenString(pSDAString) quit:'sc sc
    
       /// since Patient class corresponds to the streamlet class
       /// HS.SDA3.Streamlet.Patient, which inherits properties
       /// from HS.SDA3.Patient, we have the following lines
       do reader.CorrelateRoot("HS.SDA3.Patient")
       do {
           return:'reader.Next(.patient,.sc) $CASE(sc,$$$OK:$$$ERROR($$$GeneralError,"No patient object found."),:sc)
          }
       while '$ISOBJECT(patient)
       set mpiid=patient.MPIID
       set $EXTRACT(mpiid,1,*-3) = "*****"
       set patient.MPIID=mpiid
       set patient.Name = ##class(HS.SDA3.Name).%New()
       do patient.ToQuickXMLString(.pAnonymizedString)
    
       quit $$$OK
      }
    
     }
    ```
    
    The `Anonymize` method in the above example replaces patient MPIIDs with the string `*****`.
    
4.  Copy the `AnonymizationConfig.xml` file to the backup failover member, if you are using mirroring.
    
5.  Start the production. Or start the production later, when you send the initial data feed (see the chapter “[Performing a Bulk Load](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload)”).
    

### [Modify Data via Anonymization](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_config_truncate)

In some cases, it may be necessary to modify certain properties via anonymization on the Feeder Gateway. For example, you may need to truncate properties in incoming data that cause `MAXLEN` errors. The following provides an example of how to truncate the ObservationValue field:

`AnonymizationConfig.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<AnonymizationConfig>
<Anonymizations>
<AnonymizationInfo>
<StreamletType>Observation</StreamletType>
<AnonymizationType>XSLT</AnonymizationType>
<XSLTFile>testTruncation.xslt</XSLTFile>
</AnonymizationInfo>
</Anonymizations>
</AnonymizationConfig>
```

`testTruncation.xslt`:

```xml
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="xml" omit-xml-declaration="yes" indent="no"/>
<xsl:template match="//@* | //node()">
<xsl:copy>
<xsl:apply-templates select="@*"/>
<xsl:apply-templates select="node()"/>
</xsl:copy>
</xsl:template>
<xsl:template match="//Observation/ObservationValue[string-length(.) &gt; 999]/text()">
<xsl:value-of select="substring(., 1, 999)" />
</xsl:template>
</xsl:stylesheet>
```

Copy the `testTruncation.xslt` and `AnonymizationConfig.xml` files to the following locations:

```
install-directory/csp/xslt/SDA3/Analytics/Custom/testTruncation.xslt
```

```
install-directory/csp/xslt/SDA3/Analytics/Custom/AnonymizationConfig.xml
```

Where `install-directory` is the directory where you installed the Feeder Gateway HealthShare instance.

In this example, any incoming ObservationValue field that is part of an Observation streamlet and has a length greater than 999 characters is truncated to a length of 999 characters.

### [Other Key Settings](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_config_other)

In the Feeder production, the business operation [HS.Gateway.Analytics.RemoteOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.RemoteOperations) determines the location of the Health Insight instance that is being fed by this production. The relevant setting is named `ServiceName`. This must match the name of a service in the Service Registry. The typical name is `HSANALYTICS`. This `ServiceName` setting should exactly match the `Name` value in the Service Registry for the service with an `Info` value that ends with `/services/HSAA.TransferSDA3.WebServices.cls`. See “[Modifying the Service Definitions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_service)” in the chapter “[Configuring Unified Care Record to Send Data to Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig).”

## [Step 5: Create a Custom Business Host on the Registry to Handle AnalyticsQRequest Messages](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_analyticsqrequest)

AnalyticsQRequest messages are sent from the Feeder Gateway to the Registry in order to identify the patients with information that needs to be sent to Health Insight. Each AnalyticsQRequest message contains a single MPIID. The Registry responds to these messages with AnalyticsQResponse messages, which contain information on the requested patient and can also contain information on how to update data for that patient.

You should create a dedicated Registry production component that processes AnalyticsQRequest messages. Doing so can potentially improve Registry performance when handling AnalyticsQRequest messages. To do so, perform the following steps:

1.  Switch to the Registry namespace on your Registry instance and navigate to the `Production List` page (`Interoperability` > `List` > `Productions`). Select your Registry production and click `Open`.
    
2.  Add a business operation called `AnalyticsQRequestMessageOperations`. Select [HS.Hub.Management.Operations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Hub.Management.Operations) for the `Operation Class`.
    
3.  Select `Enable Now`.
    
4.  Select your new business operation on the `Production Configuration` page. On the right pane, under `Additional Settings`, change the `Pool Size` of the operation to be `2`.
    
    Note that you can potentially change this value based on the needs of your system. This custom business operation is not bound by FIFO constraints, and can thus have a pool size greater than `1`. InterSystems recommends starting off with a `Pool Size` of `2`. Afterwards, if the performance of your Registry production is insufficient, you can use the `Production Monitor` (Health Insight namespace > `Interoperability` > `Monitor` > `Production Monitor`) to monitor the custom business host for performance issues. As a rough guideline, if the queue size of the new custom component never exceeds the current pool size, then you are not likely to see performance improvements by increasing the pool size. If the queue size does exceed the pool size, then you may see a performance improvement by increasing pool size by 1. You should ultimately decide what pool size is best based on your observations and systems.
    
5.  Select [HS.Hub.HSWS.WebServices](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Hub.HSWS.WebServices). In the right pane, under `Additional Settings`, set the `AnalyticsQRequestTarget` to be `AnalyticsQRequestMessageOperations`.
    
6.  Restart the Registry production.
    

## [Step 6: Set Up Nightly Interoperability Message Purges](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder#HSAAIC_newfeeder_purge)

Nightly production message purging is an important part of Health Insight management. In the Feeder Gateway namepsace, there should be a nightly task to purge messages, with the following configuration options:

*   `Include message bodies` — Select this option.
    
*   `Purge only completed sessions` — Clear this option.
    

The `Do not purge most recent days` option specifies how many days of messages to keep. A value between 7 and 30 days is typical. For more information on how to configure production message purging, see [Purging Production Data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=EGMG_purge).
