# [Configuring Unified Care Record to Send Data to Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

This chapter describes how to configure HealthShare Unified Care Record to send data to HealthShare Health Insight. It discusses the following topics:

*   [How to update and configure the Registry component](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_registry)
    
*   [How to configure Edge Gateways to send data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_edge)
    

For background information, see “[Overview of the Data Feed Mechanism](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed)” in the first chapter.

Also see the chapter “[Setting Up a New Feeder Gateway (With or Without Mirroring)](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder).”

## [Updating and Configuring the Registry Component](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_registry)

This section describes how to update an existing Unified Care Record Registry to support Health Insight. The tasks are as follows:

1.  [Use the AddHub() method](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_addhub)
    
2.  [Set the data feed mechanism](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_datafeed)
    
3.  [Modify the two service definitions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_service)
    
4.  [Optionally specify the translation profile](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_xlate)
    
5.  [Restart the Registry production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_restart)
    

### [Step 1: Use the AddHub() Method](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_addhub)

In the instance that runs the Registry, open the Terminal, change to the namespace that contains the Registry production (usually `HSREGISTRY`), and enter the following command:

```objectscript
 do ##class(HS.Util.Installer.Kit.AnalyticsIntegration).AddHub()
```

This method does the following:

*   Specifies the default Health Insight data feed mechanism to be the System Index (you will change this in a later step).
    
*   Defines an initial version of the services HSANALYTICS and HSANALYTICS:WebServices, both of which you will need to modify; see the [next section](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_service).
    
*   Adds the following business hosts to the Registry production:
    
    *   [HS.Hub.Management.QueryOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Hub.Management.QueryOperations).
        
    *   [HS.Gateway.Analytics.WS.RemoteOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.WS.RemoteOperations).
        
    
    The method also adds new settings to [HS.Hub.HSWS.WebServices](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Hub.HSWS.WebServices).
    

### [Step 2: Set the Data Feed Mechanism](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_datafeed)

Switch to the Health Insight namespace and run the following command:

```objectscript
 do ##class(HSAA.API.Config).SetHIDataFeed()
```

Follow the prompts to set the data feed mechanism to AADBQ.

If you encounter an error during the execution of the method, resolve the error, then use the `ClearSetErrorStatus()` method of [HSAA.API.Config](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.API.Config) to reset the status of `SetHIDataFeed()` so that you can run it again.

### [Step 3: Modify the Service Definitions](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_service)

The `AddHub()` method in the [previous section](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_addhub) defines an initial version of two service definitions: HSANALYTICS and HSANALYTICS:WebServices. Modify each one of these as follows:

1.  Ensure that you are in the namespace for the Registry, usually `HSREGISTRY`.
    
2.  Navigate to the Service Registry from the Management Portal. To do so, select `HealthShare` > `Registry Management` > `Service`.
    
3.  Select the row for the service HSANALYTICS (or HSANALYTICS:WebServices) and modify the following items:
    
    *   `Host` — Name of the server on which you installed the analytics instance.
        
    *   `Port` — Web server port of the analytics instance.
        
4.  Examine the URL for the service and adjust that to use the correct namespace name. For example, `URL` might initially include `/csp/healthshare/hsanalytics/services/`, which assumes that the Analytics namespace is called `hsanalytics`. If you installed Health Insight in the namespace `myanalytics`, replace `hsanalytics` with `myanalytics`:
    
5.  Save the changes.
    

### [Step 4: Specify the Translation Profile (Optional)](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_xlate)

You can also set the `\Terminology\AnalyticsTranslationProfile` key, which specifies the translation profile to use when transmitting data to Health Insight. (For an introduction to translation profiles, see “[Terminology Translation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HETRM_ch_terminology_normalization)” in the book [Translating Terminology in Unified Care Record](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HETRM).) To specify this key, it is necessary to use the configuration registry user interface. To do so:

1.  Log in to the [Management Portal](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEADM_ch_tools#HEADM_tools_HS_portal) on your Registry instance and navigate to `Home` > `HealthShare` > `registryName` > `Registry Management` > `Configuration`.
    
2.  To modify an existing key, select the key in the table. Enter the key and its value in the appropriate fields and select Save.
    

### [Step 5: Restart the Registry Production](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_restart)

Restart your Registry production for the new configurations to take effect.

## [Configuring Edge Gateways to Send Data to Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig#HSAAIC_hsconfig_edge)

This section describes how to configure an existing Edge Gateway to send data to Health Insight.

Use the Management Portal to view each Edge Gateway Production (`Interoperability` > `Configure` > `Production`). If the production contains a setting named `FeedAnalytics` under `Additional Settings`, no configuration is needed. If the production does not contain this setting, do the following:

1.  Open the Terminal, change to the applicable namespace, and enter the following command:
    
    ```objectscript
     do ##class(HS.Util.Installer.Kit.AnalyticsIntegration).AddEdgeGateway()
    ```
    
    This command:
    
    *   Adds the setting `FeedAnalytics` to the production and enables it (sets it equal to true).
        
    *   Modifies the business host `SubscriptionHandler`.
        
    *   Adds the business host `AnalyticsSubscriptionHandler`.
        
    *   Adds the business host [HS.Gateway.Analytics.WS.RemoteOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.WS.RemoteOperations).
        
    *   Modifies the business host [HS.Gateway.HSWS.WebServices](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.HSWS.WebServices).
        
2.  Go to the Production Configuration page of the modified Edge Gateway and select the `Update` button.
    

> **Important:**
> 
> Unlike most changes to productions, the change to `FeedAnalytics` does not take effect until you stop and restart the production. Do not stop and restart the production until you are ready; see the chapter “[Performing a Bulk Load](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload).”
