# [Health Insight Pre-Upgrade Steps](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

Perform the following pre-upgrade steps before you upgrade your Health Insight instance:

1.  [](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_utility)[Run the Medication Administration table utility (upgrades from 2020.1 only)](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_utility).
    
2.  [Run the Security fix (upgrades from 2020.2 or 2021.1 only)](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_security_fix).
    
3.  [Clear the queue](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_queue).
    
4.  [Set Expired Queries task to on demand](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_expired).
    
5.  [Disable the transmit service and stop the Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_stop_feed).
    
6.  [Confirm that Health Insight is idle and stop the Health Insight production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_stop_production).
    
7.  [Purge management data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_purge).
    
8.  [Check for conflicting indexes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_indexes).
    
9.  [Make a note of your current Health Insight settings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_settings).
    
10.  [Next steps](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_next_steps).
     

## [Step 1: Medication Administration Table Utility (Upgrades from 2020.1 only)](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_utility)

> **Note:**
> 
> This step applies only to upgrades from Health Insight version 2020.1. In a mirrored upgrade, perform this step only on the primary mirror member.

An issue in versions 2019.1.1 and 2019.1.2 of Health Insight, where the `Patient` field of the HSAA.MedicationAdministration table was not populated correctly during upgrades because of missing Encounter data, was addressed by utility methods that became available in version 2020.1. The [IsRePopulateMANewPatientNeeded()](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Util.Installer.Upgrade.PostActivation20181#METHOD_IsRePopulateMANewPatientNeeded) utility method correctly repopulates the Patient field in the HSAA.MedicationAdministration table.

1.  Check if you need to run the utility:
    
    In the Terminal, switch to the analytics namespace and use the following commands:
    
    ```objectscript
     set tSC=##class(HSAA.Util.Installer.Upgrade.PostActivation20191).IsRePopulateMANewPatientNeeded(.isNeeded)
     zw isNeeded
    ```
    
    *   If the value of `isNeeded` is `0`, you do not need to run the utility. Proceed to the [next pre-upgrade step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_security_fix).
        
    *   If the value of `isNeeded` is `1`, then you must run the utility before upgrading.
        
2.  If the value of `isNeeded` was `1` in the step above:
    
    Make the following call to run the utility method:
    
    ```objectscript
     do ##class(HSAA.Util.Installer.Upgrade.PostActivation20181).RePopulateMANewPatientRelationship()
    ```
    
    You can use the following call to monitor the progress of this step:
    
    ```objectscript
     do ##class(HSAA.Util.Installer.Upgrade.PostActivation20191).RePopulateMAStatus()
    ```
    
    > **Note:**
    > 
    > If you experience an interruption during the execution of the utility method, you can use the [ResetRePopulateMAStatus()](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Util.Installer.Upgrade.PostActivation20181#METHOD_ResetRePopulateMAStatus) method to reset the status of the method so that you can run it again. Examples of interruptions to execution include a production shutdowns or a Terminal crash. Do not use the reset method when the utility method is running correctly.
    > 
    > To reset the status of the utility method, use the following call:
    > 
    > ```objectscript
    >  do ##class(HSAA.Util.Installer.Upgrade.PostActivation20191).ResetRePopulateMAStatus()
    > ```
    > 
    > Run the [IsRePopulateMANewPatientNeeded()](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Util.Installer.Upgrade.PostActivation20181#METHOD_IsRePopulateMANewPatientNeeded) method again after you reset the status, so that it can finish its work.
    

## [Step 2: Security Fix (Upgrades from 2020.2 or 2021.1 only)](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_security_fix)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary mirror member.

If you are upgrading from version 2020.2 or 2021.1 only, run the following code on each of your instances before you upgrade:

```objectscript
 Do ##class(%ZHSLIB.HealthShareMgr).FixSystemSecurityVersion()
```

*   If you get a `<METHOD DOES NOT EXIST>` error, follow the instructions in the “[CRITICAL Patch Required BEFORE Upgrading](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20221#HSAARN_known_adhoc_20221)” release note to obtain a critical patch for HSIEO-5568 before you proceed with your upgrade.
    
*   If you get the following message:
    
    ```
    Underlying IRIS version is not 2020.1 so this method is not runnable
    ```
    
    then your current version is not affected by the issue, and you may safely proceed with your upgrade.
    
*   If you get the following message:
    
    ```
    Successfully updated security version
    ```
    
    then you may safely proceed with your upgrade.
    

> **Caution:**
> 
> If you do not run this method before upgrading from an affected version, you will experience unplanned downtime after your upgrade, and all of your users will be locked out of the system when your upgrade completes.

## [Step 3: Clear the Queue](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_queue)

> **Note:**
> 
> *   This step is optional, but recommended.
>     
> *   In a mirrored upgrade, perform this step only on the primary mirror member.
>     

[A later step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_stop_feed) in the pre-upgrade procedure disables the transmit service of the Feeder Gateway to ensure that Unified Care Record does not start transmitting data to Health Insight after the upgrade but before Health Insight is in a state that is ready to receive that data.

The optional step described in this step ensures that the queue (the `^HS.AADBQ` global on the Registry instance) is empty before you begin your upgrade:

1.  On the Unified Care Record Registry instance, log in to the Management Portal as user with administrative privileges.
    
2.  Navigate to the globals viewer: `Home` > `System Explorer` > `Globals`.
    
3.  Display the contents of `^HS.AADBQ` in the Registry namespace.
    
    This global, if present, lists any patient data waiting to be sent to Health Insight by the data feed mechanism.
    
4.  If `^HS.AADBQ` is not present, then the queue is clear, so continue directly to the [next pre-upgrade step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_expired).
    
5.  If `^HS.AADBQ` is present:
    
    1.  In the Terminal on your Feeder Gateway instance, change to the Feeder Gateway namespace and execute the following code :
        
        ```objectscript
         set sc=##class(HS.Gateway.Analytics.TransmitService).Start()
        ```
        
    2.  Confirm that the queue of the [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer) contains 0 items
        
    3.  Run the [PauseIngestionStartBatch()](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.API.Transmit#METHOD_PauseIngestionStartBatch) API method in the class [HSAA.API.Transmit](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.API.Transmit).
        
6.  Once the analytics batch has finished, resolve any patient errors and check the contents of `^HS.AADBQ`. If `^HS.AADBQ` is not empty, repeat the procedure in [step 5](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_queue_notempty) to queue any expired queries and run the analytics batch.
    
    *   If you are planning to migrate to a System Index-based feed, then you must resolve all patient errors before you upgrade.
        
    *   If you are not planning to migrate, then you may have to resend all data for errored patients from Unified Care Record to Health Insight after the upgrade if you do not resolve the errors.
        
    
    If you are using Smart Programs or Advanced Clinical Notifications, you may have to repeat this cycle several times.
    
7.  When the `^HS.AADBQ` global is cleared, proceed to the next step.
    

## [Step 4: Set Expired Queries Task to On Demand](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_expired)

> **Note:**
> 
> In a mirrored upgrade perform this step on the primary mirror member and on the backup mirror member.

Set the `Run Expired Queries` task to run on demand:

1.  On the Unified Care Record Registry instance, log in to the Management Portal as user with administrative privileges.
    
2.  Navigate to the `Task Schedule` page: `Home` > `System Operation` > `Task Manager` > `Task Schedule`
    
3.  Select the `Run Expired Queries` task from the list of scheduled tasks.
    
4.  Click `Edit`.
    
5.  Click `Next`.
    
6.  Make a note of the current setting for `How often do you want the Task Manager to execute this task?`
    
    You will need this value in a post-upgrade step.
    
7.  Set `How often do you want the Task Manager to Execute this task?` to `On demand`.
    
8.  Click `Finish`.
    
9.  If you upgrading a mirror, repeat this procedure on the backup mirror member.
    

## [Step 5: Disable the Transmit Service and Stop the Feeder Gateway](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_stop_feed)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary mirror member.

To disable the transmit service and stop the Feeder Gateway:

1.  Log in to the Management Portal on your Feeder Gateway instance as user with administrative privileges.
    
2.  Navigate to `Home` > `HealthShare` > `feederGatewayNamespace`.
    
3.  Click the `Productions` link in the banner.
    
4.  Click `Configure` > `Production`. (If needed, select your Feeder Gateway production and click `Open`.)
    
5.  Click on the [HS.Gateway.Analytics.TransmitService](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.TransmitService) business service.
    
6.  In the `Settings` pane, under `Basic Settings`, deselect the `Enabled` checkbox.
    
7.  Note the value of the `Call Interval` setting, as you will need it later in a post-upgrade step.
    
8.  Click `Apply`.
    
9.  Click `Stop Production`.
    

## [Step 6: Confirm that Health Insight is Idle and Stop the Health Insight Production](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_stop_production)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary mirror member.

1.  Log in to the Management Portal on your Health Insight instance as user with administrative privileges.
    
2.  Navigate to `Home` > `HealthShare` > `analyticsNamespace`.
    
3.  Click the `Productions` link in the banner.
    
4.  Click `Monitor` > `System Monitor`.
    
5.  Confirm that the Health Insight production is idle.
    
6.  Stop your production(s):
    
    *   Click the `HealthShare` link in the banner to return to the analytics namespace management page.
        
    *   Click the `Stop All` link in the banner.
        

## [Step 7: Purge Management Data](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_purge)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary mirror member.

Purge all production messages in the analytics namespace:

1.  Log in to the Management Portal on your Health Insight instance as user with administrative privileges.
    
2.  Navigate to `Home` > `HealthShare` > `analyticsNamespace`.
    
3.  Click the `Productions` link in the banner.
    
4.  Click `Manage` > `Purge Management Data`.
    
5.  Specify the following details in the purge dialog:
    
    *   `Include message bodies` — Select this option (On).
        
    *   `Keep data integrity` or `Purge only completed sessions` — Clear this option (Off).
        
    *   `Do not purge most recent days` — Specify this as 0.
        
6.  Click `Start Purge`.
    

## [Step 8: Check for Conflicting Indexes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_indexes)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary mirror member.

Review the [Indexes Added in Version 2025.1](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_index) section to look for conflicts with your existing indexes.

Check whether you have any equivalent indexes. If you do, remove them. Also check for any custom indexes with the same names as the new ones; if a conflict exists, either remove the custom index or rename it with a `Z` prefix.

## [Step 9: Make a Note of Your Current Settings](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_settings)

> **Note:**
> 
> In a mirrored upgrade, you only have to note the settings on the primary mirror member.

There are several production and other settings that you should make note of as you will need them in later post-upgrade tasks.

Perform the following procedures from the Management Portal on your Health Insight instance:

### [Production Logging Settings](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_settings_production)

1.  Navigate to `Home` > `HealthShare` > `analyticsNamespace`.
    
2.  Click the `Productions` link in the banner.
    
3.  Click `Configure` > `Production`. (If needed, select your Analytics production and click `Open`.)
    
4.  In the `Production Settings` pane, under `Additional Settings`, note the values of the following production settings:
    
    *   `LogTarget`
        
    *   `TargetPath`
        
    *   `LogLevel`
        

## [Step 10: Next Steps](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade#HSAAUP_preupgrade_next_steps)

Now that you have completed the pre-upgrade procedure:

*   If you are upgrading a non-mirrored system, continue to the next section to [perform the software upgrade](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_upgrade).
    
*   If you are upgrading a Health Insight mirror, return to the [referring step in Upgrading a Health Insight Mirror](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_preupgradeA).
