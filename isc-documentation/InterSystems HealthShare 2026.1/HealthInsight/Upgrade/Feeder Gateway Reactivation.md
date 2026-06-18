# [Feeder Gateway Post-Upgrade Reactivation Procedure](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_postupgradefeeder)

> **Note:**
> 
> The post-upgrade steps in this section are specific to systems that will continue to use the Feeder Gateway (AADBQ-based) architecture after the upgrade. If you chose to change to the System Index architecture, go to [Migrating to a System Index-Based Data Feed](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAMIG_migsysindex) instead.

Now that you have completed the [Post-Upgrade Reactivation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade) for your Health Insight instance, perform the following post-upgrade reactivation steps for the Feeder Gateway that are outlined below and detailed in the sections that follow:

1.  [Reactivate the Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_postupgradefeeder_reactivate).
    
2.  [Review the Feeder Gateway activation logs](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_postupgradefeeder_logs).
    
3.  [Set the Health Insight data feed to use the Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_postupgradefeeder_setfeed).
    
4.  [Update the Feeder Gateway settings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_postupgradefeeder_settings).
    
5.  [Update the Feeder Access Gateway settings in Analytics](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_postupgradefeeder_agsettings).
    
6.  [Next Steps](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_postupgradefeeder_next).
    

## [Step 1: Reactivate the Feeder Gateway](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_postupgradefeeder_reactivate)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary Feeder Gateway mirror member.

Reactivate the Feeder Gateway namespace.

To reactivate the Feeder Gateway namespace, use one of the options below:

### [Installer Wizard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_C20820)

Use the Installer Wizard in the Management Portal:

1.  Log in to the Management Portal on your Feeder Access Gateway instance as a user with administrative privileges.
    
2.  Click `HealthShare` to open the HealthShare Management Portal.
    
3.  Click the `Installer Wizard` link in the banner.
    
4.  In the row for your Feeder Access Gateway in the table of configurations:
    
    *   Click `Activate`.
        
    *   In the `Activate Configuration` dialog, click `Start`.
        
    *   Wait for activation to complete. When you see the `Activation Done` message, click `Close`.
        

### [Terminal](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_C20831)

Perform the reactivation in the Terminal:

1.  Open the Terminal on your Feeder Gateway and enter the following command in the `HSLIB` namespace:
    
    ```objectscript
     Set status=##class(HS.Util.Installer).InstallAccessGateway("namespace")
     zw status
    ```
    
    Where `namespace` is the namespace of the Feeder Access Gateway production.
    
2.  If `status` equals 1, the command was successful. If not, enter the following command to learn more:
    
    ```objectscript
     do $system.OBJ.DisplayError()
    ```
    

## [Step 2: Review the Feeder Gateway Activation Logs](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_postupgradefeeder_logs)

Review the activation logs.

HealthShare creates namespace-specific log files for activations in the `<install-dir>\mgr` directory. When your activation completes, check the highest incremented log file for the relevant namespace to confirm that everything worked correctly or to detect any errors. This file will be named `HS.Util.Installer.<namespace>-<#>.log`.

When inspecting the log files, pay particular attention to entries with `[WARNING]` or `[ERROR]`.

*   `[WARNING]` indicates that an action should be taken
    
*   `[ERROR]` indicates that an error occurred during activation.
    

## [Step 3: Set the Data Feed to Feeder Gateway](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_postupgradefeeder_setfeed)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary Analytics mirror member.

1.  Ensure that your Registry production is running.
    
2.  Ensure that your Analytics production is running.
    
3.  In the Terminal on your Analytics namespace, run the following command:
    
    ```
    write ##class(HSAA.API.Config).CheckHIDataFeed()
    ```
    
    If the Terminal displays `AADBQ`, skip the rest of this step. If the Terminal displays `Not Set`, run the following command and select `AADBQ` when prompted:
    
    ```objectscript
     set sc = ##class(HSAA.API.Config).SetHIDataFeed()
    ```
    
4.  If you encounter an error during the execution of the method, resolve the error, then use the [ClearSetErrorStatus()](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.API.Config#METHOD_ClearSetErrorStatus) method of [HSAA.API.Config](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.API.Config) to reset the status that you can run [SetHIDataFeed()](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.API.Config#METHOD_SetHIDataFeed) again.
    

## [Step 4: Update Feeder Gateway Settings](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_postupgradefeeder_settings)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary Feeder Gateway mirror member.

To update and confirm the proper settings, navigate to your Feeder Gateway production:

1.  Log in to the Management Portal on your Feeder Gateway instance as a user with administrative privileges.
    
2.  Navigate to `Home` > `HealthShare` > `feederGatewayNamespace`.
    
3.  Click the `Productions` link in the banner.
    
4.  Click `Configure` > `Production`. (If needed, select your Feeder Gateway production and click `Open`.)
    
5.  Update or confirm the settings in the Feeder Gateway production as shown below.
    

### [HS.Gateway.Analytics.TransmitServiceOpens in a new tab](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_C20878)

Update the `Call Interval` with the value you noted in a [pre-upgrade step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_stop_feed):

1.  Click on the [HS.Gateway.Analytics.TransmitService](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.TransmitService) business service.
    
2.  Change the value of the `Call Interval` setting from as needed to the value you noted [earlier](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_stop_feed).
    
3.  Click `Apply`.
    

### [HS.Gateway.Analytics.RemoteOperationsOpens in a new tab](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_C20888)

Check the service name.

1.  Click on the [HS.Gateway.Analytics.RemoteOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.RemoteOperations) business operation.
    
2.  Ensure that the `ServiceName` setting under `Additional Settings` points to the analytics transfer web service for your system (for example, `HSANALYTICS`).
    
    This should exactly match the `Name` value in the [service registry](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEADM_ch_service_registry) for the service with an `Info` value that ends with:
    
    `/services/HSAA.TransferSDA3.WebServices.cls`
    

### [HS.Gateway.Analytics.WS.RemoteOperationsOpens in a new tab](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_C20898)

Check the service name.

1.  Click on the [HS.Gateway.Analytics.WS.RemoteOperations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.WS.RemoteOperations) business operation.
    
2.  Ensure that the `ServiceName` setting under `Basic Settings` points to the analytics web service for your system (for example, `HSANALYTICS:WebServices`).
    
    This `ServiceName` setting should exactly match the `Name` value in the [service registry](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEADM_ch_service_registry) for the service with an `Info` value that ends with:
    
    `/services/HSAA.WS.WebServices.cls`.
    

## [Step 5: Update Feeder and Viewer Access Gateway Settings in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_postupgradefeeder_agsettings)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary Analytics mirror member.

Confirm the correct Access Gateway service name values in your Health Insight production:

1.  On your Health Insight instance, log in to the Management Portal as user with administrative privileges.
    
2.  Navigate to `Home` > `HealthShare` > `analyticsNamespace`.
    
3.  Click the `Productions` link in the banner.
    
4.  Click `Configure` > `Production`. (If needed, select your analytics production and click `Open`.)
    
5.  Confirm the settings shown below.
    

### [AccessGatewayFeeder](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_C20921)

Confirm the service name:

1.  Click on the `AccessGatewayFeeder` business operation.
    
2.  Confirm that the `ServiceName` setting is set to the Service Name of your Feeder Gateway from the Service Registry, for example `FeederHostname:HSHIFEEDER`.
    

### [AccessGatewayViewer](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_C20929)

Confirm the service name:

1.  Click on the `AccessGatewayViewer` business operation.
    
2.  Confirm that the `ServiceName` setting is set to the Service Name of your Access Gateway from the Service Registry, for example `AccessGatewayHostname:HSACCESS`.
    

For details on these settings, see [Business Operations](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_production#HSAAREF_production_operations) in the Health Insight Production Details appendix.

## [Step 6: Next Steps](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder#HSAAUP_postupgradefeeder_next)

Now that you have reactivated the Feeder Gateway:

*   If you are upgrading a non-mirrored system, continue to the next section to perform the [Feeder Gateway Post-Upgrade Restart Procedure](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart).
    
*   If you are upgrading a Health Insight mirror, return to the [referring step in Upgrading a Health Insight Mirror](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_setfeed).
