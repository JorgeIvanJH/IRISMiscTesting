# [Upgrading a Health Insight Mirror (AADBQ)](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

This page describes the procedure to upgrade a mirrored instance of HealthShare Health Insight to the current version. Refer to the [Supported Upgrade Paths](https://docs.intersystems.com/hs20261/csp/docbook/hssupportedbrowsers/HS_Platforms.pdf#page=2) document for a list of versions that you can upgrade from.

This procedure assumes that you have a synchronous mirror for high availability with two members:

*   The initial primary mirror member shall be called instance A
    
*   The initial backup mirror member shall be called instance B.
    

The Feeder Gateway and Health Insight should be upgraded simultaneously.

Please consider the important notices below about significant changes in Health Insight.

> **Important:**
> 
> ## [Health Insight Architecture](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_architecture)
> 
> When you complete the upgrade of a Health Insight mirror that uses the Feeder Gateway, you can choose to:
> 
> *   Continue with the current architecture.
>     
> *   Set up [mixed mode](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAMIG_mixed), where a Health Insight deployment using the Feeder Gateway coexists in the federation with one or more deployments that use a System Index-based feed, like a dynamic data mart.
>     
> *   Migrate a deployment that uses a Feeder Gateway to use a System Index-based feed instead.
>     
> 
> > **Note:**
> > 
> > When you complete an upgrade to this version of Health Insight from version 2022.1 or earlier, the following business hosts will be automatically added to your Health Insight production in order to facilitate the future use of a System Index-based data feed:
> > 
> > *   [SysIndex.Polling](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.SysIndex.Process)
> >     
> > *   [HSAA.TransferSDA3.Service.PauseSysIndexRunBatch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.PauseSysIndexRunBatch)
> >     
> > *   [HS.Util.Trace.Operations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Util.Trace.Operations)
> >     
> 
> ## [Private Web Server](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_webserver)
> 
> Beginning with version 2024.2, the private Apache web server is no longer distributed and installed with any InterSystems product kits.
> 
> While your production systems likely already use a third-party web server, your development instances may not.
> 
> Upgrading customers must have a third-party web server installed on their system in order to use this, and all future versions of Health Insight. InterSystems strongly recommends that before you upgrade Health Insight to this version, you install and [configure a third-party web server](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GCGI_private_web) for each instance. Performing this configuration before you upgrade reduces the complexity of untangling any potential post-upgrade issues that may arise.
> 
> ## [Upgrading in a HealthShare Federation](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_federation)
> 
> If you are upgrading Health Insight, you must upgrade other parts of your HealthShare federation as well. Before performing any upgrades, read the upgrade instructions for all of the components in your federation and create an overall upgrade plan. In your upgrade plan, make sure to upgrade the different components of your federation in the correct order. For information, see the [Unified Care Record Upgrade Guide](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEUPGRADE_overview).
> 
> Note that Health Insight version 2025.2:
> 
> *   can only receive data from version 2025.2 of HealthShare Unified Care Record.
>     
> *   is only compatible with version 2025.2 of the Clinical Viewer.
>     
> 
> ## [ChangedObjects Downstream Process Updates](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_changedobjects)
> 
> If you have any downstream processes that relied on the old behavior for [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects), update them now to ensure they are compatible with the updated behavior prior to beginning with the post-upgrade reactivation steps. More specifically, if your systems:
> 
> *   Relied on batch-driven purge behavior
>     
> *   Assumed the ChangedObjects table would be empty post-batch
>     
> *   Relied on the old logic where rows were overwritten
>     
> 
> ...you must update those systems to reflect the new model where rows are appended and purging occurs via a scheduled task.
> 
> You may also want to adjust the frequency of the Purge ChangedObjects task to suit your retention requirements. Retention duration is determined by how often this task runs. Ensure that purging runs less frequently than the slowest consumer of [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) data.
> 
> ## [Readmission Custom Method Updates](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_readmission)
> 
> Starting in version 2025.2, the implementation for the default method to calculate readmissions has changed. Previously, both the default and any custom methods directly updated [HSAA.Encounter](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Encounter) relationships using a SQL query. Now, the default method computes readmissions for all encounters of a selected patient. Any custom methods must also follow this pattern. If you previously implemented a custom readmission method and want to continue using it after the upgrade, you must update it to match the new structure. See the Additional Settings documentation for guidance on modifying your custom method.

To upgrade a mirrored instance of Health Insight, follow the steps outlined below and detailed in the sections that follow:

1.  [Mirror the HSCUSTOM database](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_mirhscustom).
    
2.  [Disable failover on instance A](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_disablefailover1A).
    
3.  [Prevent Health Insight production auto-start](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_zmirror1).
    
4.  [Perform pre-upgrade Health Insight steps on instance A](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_preupgradeA).
    
5.  [Shut down the backup member, instance B](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_shutdownB).
    
6.  [Stop and disable the ISCAgent on instance B (Linux only)](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_linux_stopagentB).
    
7.  [Upgrade instance B](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_upgradeB).
    
8.  [Start and enable the ISCAgent on instance B (Linux only)](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_linux_startagentB).
    
9.  [Re-enable failover on instance A](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_renablefailover1A).
    
10.  [Fail over from instance A to instance B](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_failoverA).
     
11.  [Disable failover on instance B](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_disablefailover1B).
     
12.  [Shut down the backup member, instance A](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_shutdownA).
     
13.  [Stop and disable the ISCAgent on instance A (Linux only)](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_linux_stopagentA).
     
14.  [Upgrade instance A](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_upgradeA).
     
15.  [Start and enable the ISCAgent on instance A (Linux only)](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_linux_startagentA).
     
16.  [Reactivate the Analytics Namespace on the Primary (B)](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_reactivatebothB).
     
17.  [Reactivate the Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_setfeed).
     
18.  [Export the Reporting Tasks](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_postactivateB_export).
     
19.  [Verify the upgrade on instance B](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_verifyupgradeB).
     
20.  [Re-enable failover on instance B](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_renablefailover1B).
     
21.  [Failover from instance B to instance A](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_failoverB).
     
22.  [Disable failover on instance A](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_disablefailover2A).
     
23.  [Reactivate the Analytics namespace on instance A](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_reactivateHI).
     
24.  [Re-enable Health Insight production Auto-Start](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_zmirror2).
     
25.  [Import the reporting tasks](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_postactivateA_import).
     
26.  [Re-enable failover on instance A](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_renablefailover2A).
     
27.  [Verify upgrade on instance A](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_verifyupgradeA).
     
28.  [Rebuild the indexes and cubes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_rundefer).
     
29.  [Start the Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_startproductions).
     
30.  [Perform the post-upgrade cleanup steps](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_postactivateA_final).
     

## [Step 1: Mirror HSCUSTOM if Necessary](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_mirhscustom)

If you are performing an upgrade from a version earlier that 2023.2, you must mirror HSCUSTOM before you begin your upgrade.

To do so, follow the instructions in [Adding Databases to the Mirror, Copying Them, and Catching Up](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAMIG_mighi#HSAAMIG_mighi_otherdb) in the procedure to Migrate Health Insight to Use Mirroring, but:

1.  [Add](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAMIG_mighi#HSAAMIG_mighi_add_db) only the `HSCUSTOM` database to your mirror.
    
2.  [Copy](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAMIG_mighi#HSAAMIG_mighi_copy_db) only `HSCUSTOM` to the backup.
    
3.  [Activate and catch up](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAMIG_mighi#HSAAMIG_mighi_catchup_db) only `HSCUSTOM`.
    

## [Step 2: Disable Failover on Instance A](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_disablefailover1A)

On instance A, disable mirror failover:

1.  Open the System Management Portal and navigate to `Home` > `System Operation` > `Mirror Monitor`.
    
2.  On the `Mirror Monitor` page, select `Set No Failover`.
    

Alternatively, you can perform this action from the terminal:

1.  On instance A, open a terminal and enter the following commands:
    
    ```objectscript
     zn "%SYS"
     do ^MIRROR
    ```
    
2.  Select `Option 2) Mirror Management`
    
3.  Select `Option 4) Change No Failover State`
    
4.  Answer `YES` to the question `Do you want to SET "No Failover" state?`
    

## [Step 3: Prevent Health Insight Production Auto-Start](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_zmirror1)

Prevent Health Insight production auto-start on both instance A and instance B.

You may be using the production auto-start feature as documented in [Enabling and Disabling Automatic Production Startup](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEENS_ch_emp#HEENS_emp_auto_start) or you may depend upon the `StartAll()` method in your ^ZMIRROR routine to auto-start productions.

*   If you are using production auto-start:
    
    1.  Follow the instructions to [Disable Automatic Startup for all Productions in a HealthShare Instance](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEENS_ch_emp#HEENS_emp_disable_auto_start) on your primary mirror member.
        
    2.  Repeat the procedure on your backup mirror member.
        
*   If you are depending upon the `StartAll()` method in your ^ZMIRROR routine, modify your ^ZMIRROR routine by performing the following steps using [your IDE](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides):
    
    1.  Switch to the `%SYS` namespace in your Health Insight primary instance.
        
    2.  Edit the ^ZMIRROR routine to prevent auto-start of the Health Insight production. This prevents the productions from automatically starting until the production settings are updated.
        
        The following is an example of how you might alter a sample ^ZMIRROR routine:
        
        ```objectscript
        ZMIRROR //For Health Insight
           quit
        NotifyBecomePrimary() public
           // Start productions after failover
           new $namespace
           set $namespace="HSLIB"
        
           // Comment out only the next line for the mirrored upgrade, and un-comment after upgrade is complete
           // do ##class(HS.Director).StartAll()
        
           // Run tune schema in the HSANALYTICS (or equivalent) namespace
           set $namespace = "HSANALYTICS"
           // using Work Queue Manager - initialize a queue
           new queue
           set queue = ##class(%SYSTEM.WorkMgr).Initialize()
           new sc
           set sc = queue.Queue("##class(HSAA.TransferSDA3.Task.TuneMirroredHSAASchema).OnTask")
           set sc = queue.WaitForComplete()
           // using Work Queue Manager - stops work queue, interrupts WIP, removes queued work
           set sc = queue.Clear(10)
        ```
        
        In this sample code, the following line has been commented out:
        
        ```objectscript
         do ##class(HS.Director).StartAll()
        ```
        
    3.  Repeat this procedure on the backup instance.
        

## [Step 4: Perform the Pre-Upgrade Steps on Instance A](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_preupgradeA)

On instance A, perform the pre-upgrade steps:

1.  Run all of the applicable procedures in the [Health Insight Pre-Upgrade Steps](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade) in the upgrade documentation on Instance A.
    
    > **Note:**
    > 
    > With the exception of the Expired Queries Task step, perform each step only on instance A, your primary mirror member. Because the systems are mirrored, these actions will also occur on instance B.
    > 
    > Run the Expired Queries Task step on both mirror members (this is noted in the step).
    
2.  When you have completed the pre-upgrade procedures, return to this document and continue to the [next step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_shutdownB).
    

## [Step 5: Shut Down Instance B](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_shutdownB)

Shut down instance B:

*   Use the `iris stop` command (or stop the instance from the Windows HealthShare cube).
    

> **Note:**
> 
> After the instance shutdown has completed, you can verify that the instance stopped cleanly by examining `<install-dir>/mgr/cconsole.log`.

## [Step 6: Stop and disable the ISCAgent on Instance B (Linux only)](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_linux_stopagentB)

On Linux systems only, the location of the ISCAgent service has changed. Stop and disable the old version of the service from the command line:

1.  Stop the ISCAgent service:
    
    ```
    sudo systemctl stop ISCAgent.service
    ```
    
2.  Disable the ISCAgent service:
    
    ```
    sudo systemctl disable ISCAgent.service
    ```
    
3.  Check the status of the ISCAgent service and make sure it shows that the service is inactive:
    
    ```
    systemctl status ISCAgent
    ```
    

## [Step 7: Upgrade Instance B](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_upgradeB)

On instance B:

1.  Follow the procedure to [Perform the Health Insight Software Upgrade](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_upgrade) as described in the upgrade documentation.
    
2.  When the software upgrade procedure is complete, return to this document
    
3.  Confirm that instance B has restarted.
    
4.  Continue to the [next step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_linux_startagentB).
    

## [Step 8: Start and Enable the ISCAgent on Instance B (Linux only)](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_linux_startagentB)

On Linux systems only, start and then enable the updated version of the ISCAgent service from the command line:

1.  Start the ISCAgent service:
    
    ```
    sudo systemctl start ISCAgent.service
    ```
    
2.  Enable the ISCAgent service:
    
    ```
    sudo systemctl enable ISCAgent.service
    ```
    
3.  Check the status of the ISCAgent service and make sure it shows that the service is active:
    
    ```
    systemctl status ISCAgent
    ```
    

## [Step 9: Re-Enable Failover on A](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_renablefailover1A)

Now that instance B is upgraded, re-enable mirror failover:

1.  On instance A, open the System Management Portal and navigate to `Home` > `System Operation` > `Mirror Monitor`.
    
2.  On the `Mirror Monitor` page, verify that server B appears with the status of `Backup`.
    
3.  On the `Mirror Monitor` page, select `Clear No Failover`.
    

Alternatively, you can perform this action from the terminal:

1.  On instance A, open a terminal and enter the following commands:
    
    ```objectscript
     zn "%SYS"
     do ^MIRROR
    ```
    
2.  Select `Option 2) Mirror Management`
    
3.  Select `Option 4) Change No Failover State`
    
4.  Answer `YES` to the question `Do you want to CLEAR "No Failover" state?`
    

## [Step 10: Failover from A to B](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_failoverA)

Shut down instance A in order to fail over to instance B.

To shut down instance A:

*   Use the `iris stop` command (or stop the instance from the Windows HealthShare cube).
    

This will promote B to primary and demote A to backup.

## [Step 11: Disable Failover on B](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_disablefailover1B)

Disable mirror failover again.

On instance B:

1.  Open the System Management Portal and navigate to `Home` > `System Operation` > `Mirror Monitor`.
    
2.  On the `Mirror Monitor` page, select `Set No Failover`.
    

Alternatively, you can perform this action from the terminal:

1.  On instance B, open a terminal and enter the following commands:
    
    ```objectscript
     zn "%SYS"
     do ^MIRROR
    ```
    
2.  Select `Option 2) Mirror Management`
    
3.  Select `Option 4) Change No Failover State`
    
4.  Answer `YES` to the question `Do you want to SET "No Failover" state?`
    

## [Step 12: Ensure that Instance A Has Been Shut Down](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_shutdownA)

Ensure that instance A has been shut down. If instance A has not been shut down, you can shut it down:

*   Use the `iris stop` command (or stop the instance from the Windows HealthShare cube).
    

> **Note:**
> 
> After the instance shutdown has completed, you can verify that the instance stopped cleanly by examining `<install-dr>/mgr/cconsole.log`.

## [Step 13: Stop and Disable the ISCAgent on Instance A (Linux only)](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_linux_stopagentA)

On Linux systems only, the location of the ISCAgent service has changed. Stop and disable the old version of the service from the command line:

1.  Stop the ISCAgent service:
    
    ```
    sudo systemctl stop ISCAgent.service
    ```
    
2.  Disable the ISCAgent service:
    
    ```
    sudo systemctl disable ISCAgent.service
    ```
    
3.  Check the status of the ISCAgent service and make sure it shows that the service is inactive:
    
    ```
    systemctl status ISCAgent
    ```
    

## [Step 14: Upgrade Instance A](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_upgradeA)

Now upgrade Instance A:

1.  On instance A, follow the procedure to [Perform the Health Insight Software Upgrade](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_upgrade) as described in the upgrade documentation.
    
2.  When the software upgrade procedure is complete, return to this document
    
3.  Confirm that instance A has restarted.
    
4.  Continue to the [next step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_linux_startagentA).
    

## [Step 15: Start and Enable the ISCAgent on Instance A (Linux only)](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_linux_startagentA)

On Linux systems only, start and then enable the updated version of the ISCAgent service from the command line:

1.  Start the ISCAgent service:
    
    ```
    sudo systemctl start ISCAgent.service
    ```
    
2.  Enable the ISCAgent service:
    
    ```
    sudo systemctl enable ISCAgent.service
    ```
    
3.  Check the status of the ISCAgent service and make sure it shows that the service is active:
    
    ```
    systemctl status ISCAgent
    ```
    

## [Step 16: Reactivate the Analytics Namespace on the Primary (B)](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_reactivatebothB)

> **Note:**
> 
> Depending on your deployment and customization setup, you may need to take the following actions before performing this step.
> 
> ### [ChangedObjects Downstream Process Updates](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_changedobjects_16)
> 
> If instance B has any downstream processes that rely on pre-2025.2 behavior for [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects), see the note at the [beginning of the post-upgrade reactivation procedure](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade) before continuing. You may need to update your downstream processes to accommodate the new append behavior and scheduled purge model.
> 
> If your environment uses a virtual IP or similar setup where downstream ChangedObject consumers connect without targeting a specific instance, you may only need to make this change once, during this step. Otherwise, you may need to update any additional processes for instance A [at a later step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_reactivateHI).
> 
> ### [Readmission Custom Method Updates](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_readmission_16)
> 
> If you previously used a custom method to compute readmissions and want to continue doing so, you must update your custom method. See the [beginning of the post-upgrade reactivation procedure](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade) for guidance on modifying your custom method on Instance B.
> 
> Your custom method changes will be mirrored over to your backup mirror member.

Instance B is now your primary mirror member. To reactivate your analytics namespace:

1.  On instance B, follow the [Health Insight Post-Upgrade Reactivation Procedure](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade) in the upgrade documentation:
    
    *   Each step in the procedure notes whether it should be performed only on the primary (instance B) or on both mirror members.
        
        The following steps indicate that they should be performed on both mirror members:
        
        *   [Confirm that System-Wide Parallel Query Processing is Enabled](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_parallel)
            
        *   [Turn off AutoTune](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_tune)
            
        *   [Reset Expired Queries Task](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_expired)
            
2.  When you have completed the procedure, return to this document and continue to the [next step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_setfeed).
    

## [Step 17: Reactivate the Feeder Gateway on Instance B](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_setfeed)

1.  Perform the [Feeder Gateway Post-Upgrade Reactivation Procedure](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder). Follow the instructions in each step about which instance to use.
    
2.  When you have completed the procedure, return to this document and continue to the [next step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_postactivateB_export).
    

## [Step 18: Export the Reporting Tasks](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_postactivateB_export)

Export the reporting tasks from instance B in preparation for failing over and duplicating them on instance A in a [later step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_postactivateA_import).

1.  On instance B, log in to the Management Portal with administrator privileges.
    
2.  Navigate to `System Operation` > `Task Manager` > `Task Schedule`.
    
3.  Locate the following tasks:
    
    *   `Cube Manager Build - <analytics_namespace>`
        
    *   `Cube Manager Synch - <analytics_namespace>`
        
4.  For each task:
    
    1.  Click the name to view the task details.
        
    2.  Click `Export`.
        
    3.  Provide the path and file name for the export.
        
    4.  Click `Perform Action Now`.
        
5.  Move the export files to a location accessible to backup failover member.
    

## [Step 19: Verify Upgrade on Instance B](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_verifyupgradeB)

On instance B, use SQL queries to confirm the presence of data. Verify the presence of cubes.

## [Step 20: Re-Enable Failover (B)](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_renablefailover1B)

Re-enable mirror failover:

1.  On instance B, open the System Management Portal and navigate to `Home` > `System Operation` > `Mirror Monitor`.
    
2.  On the `Mirror Monitor` page, select `Clear No Failover`.
    

Alternatively, you can perform this action from the terminal:

1.  On instance B, open a terminal and enter the following commands:
    
    ```objectscript
     zn "%SYS"
     do ^MIRROR
    ```
    
2.  Select `Option 2) Mirror Management`
    
3.  Select `Option 4) Change No Failover State`
    
4.  Answer `YES` to the question `Do you want to CLEAR "No Failover" state?`
    

## [Step 21: Fail Over From Instance B to Instance A](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_failoverB)

Shut down instance B in order to fail over to instance A. To shutdown instance B:

*   Use the `iris stop` command (or stop the instance from the Windows HealthShare cube).
    

This will promote instance A to primary and demote instance B to backup.

Restart instance B:

*   Use the `iris start` command (or start the instance from the Windows HealthShare cube).
    

## [Step 22: Disable Failover](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_disablefailover2A)

Disable mirror failover again.

On instance A:

1.  Open the System Management Portal and navigate to `Home` > `System Operation` > `Mirror Monitor`.
    
2.  On the `Mirror Monitor` page, select `Set No Failover`.
    

Alternatively, you can perform this action from the terminal:

1.  On instance A, open a terminal and enter the following command:
    
    ```objectscript
     zn "%SYS"
     do ^MIRROR
    ```
    
2.  Select `Option 2) Mirror Management`
    
3.  Select `Option 4) Change No Failover State`
    
4.  Answer `YES` to the question `Do you want to SET "No Failover" state?`
    

## [Step 23: Reactivate the Analytics Namespace](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_reactivateHI)

> **Note:**
> 
> If instance A has any unique downstream processes that rely on pre-2025.2 behavior for [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects), see the note at the [beginning of the post-upgrade reactivation procedure](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade) before performing the steps here. You may need to update your downstream processes to align with the new append behavior and scheduled purge model.
> 
> If you use a virtual IP or similar setup for downstream processes and have already updated those processes in [a prior step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_reactivatebothB), no additional updates are needed here.
> 
> However, if instance A has any unique downstream processes that rely on the old behavior of [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects), update them now to be compatible with the new append and scheduled purge behavior before reactivating the analytics namespace.

On instance A, reactivate the Analytics namespace.

> **Note:**
> 
> You have already reactivated the Analytics namespace on instance B when it was the primary mirror member. For the Analytics namespace however, activation needs to happen at least once on each member to perform local file system changes when the member is primary.

1.  Repeat only the following two steps in the upgrade documentation on instance A:
    
    *   [Reactivate Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_reactivate)
        
    *   [Review the Health Insight Activation Logs](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_logs)
        
2.  When you have completed the activation and log review, return to this document and continue to the [next step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_postactivateA_import).
    

## [Step 24: Re-enable Health Insight Production Auto-Start](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_zmirror2)

On both instances A and B, re-enable Health Insight production auto-start, either by modifying your [production auto-start configuration](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEENS_ch_emp#HEENS_emp_auto_start), or by editing the ^ZMIRROR routine to allow the Health Insight production to auto-start on failover.

## [Step 25: Import the Reporting Tasks](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_postactivateA_import)

In an [earlier step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_postactivateB_export), you exported the reporting tasks from instance B.

In this step, you will import them into instance A:

1.  On Instance A, log in to the Management Portal as a user with administrator privileges.
    
2.  Navigate to `Home` > `System Operation` > `Task Manager` > `Import Tasks`.
    
3.  Browse for and import the tasks that you exported earlier.
    

## [Step 26: Re-Enable Failover](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_renablefailover2A)

Re-enable mirror failover:

1.  On instance A, open the System Management Portal and navigate to `Home` > `System Operation` > `Mirror Monitor`.
    
2.  On the `Mirror Monitor` page, select `Clear No Failover`.
    

Alternatively, you can perform this action from the terminal:

1.  On instance A, open a terminal and enter the following command:
    
    ```objectscript
     zn "%SYS"
     do ^MIRROR
    ```
    
2.  Select `Option 2) Mirror Management`
    
3.  Select `Option 4) Change No Failover State`
    
4.  Answer `YES` to the question `Do you want to CLEAR "No Failover" state?`
    

## [Step 27: Verify Upgrade](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_verifyupgradeA)

Use your internal procedures to verify that the upgrade went smoothly on instance A, and that all of your systems and customizations are working as expected.

> **Tip:**
> 
> Work out a verification procedure when you upgrade your Test or UAT system in order to minimize system downtime on your Live system.

## [Step 28: Rebuild the Indexes and Cubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_rundefer)

Instance A is your primary. On instance A:

1.  Run the utility to [Rebuild Indexes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_index) in the upgrade documentation. This may take a long time.
    
2.  Follow the procedure to [Rebuild Cubes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_cubes) in the upgrade documentation again on instance A.
    
3.  When you have completed the rebuilds, return to this document and continue to the [next step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_startproductions).
    

## [Step 29: Start the Feeder Gateway](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_startproductions)

Start your Feeder Gateway production by following the [Feeder Gateway Post-Upgrade Restart Procedure](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart).

## [Step 30: Perform the Post-Upgrade Cleanup Steps](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_postactivateA_final)

On Instance A, run all of the applicable procedures in the [Health Insight Post-Upgrade Cleanup Steps](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade) procedure.
