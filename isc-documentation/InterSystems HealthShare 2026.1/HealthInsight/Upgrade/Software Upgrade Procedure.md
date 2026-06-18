# [Perform the Health Insight Software Upgrade](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_upgrade#HSAAUP_upgrade)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

Now that you have completed the [pre-upgrade steps](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade), perform the software upgrade as follows:

*   If you are upgrading a kit-based deployment, on the machine that hosts your Health Insight instance, follow the upgrade instructions for your operating system as detailed in the InterSystems IRIS Installation Guide:
    
    *   [Windows Upgrade Procedure](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GCI_winup)
        
    *   [UNIX, Linux, and macOS Upgrade Procedure](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GCI_unixup)
        
*   If you are upgrading a container-based deployment, follow the instructions for [swapping a container image](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSDEPLOY_swap), remembering to change the image path and update the `HS_IMAGE_VERSION` variable as needed.
    

> **Important:**
> 
> After running the installer for an upgrade, check the status of your license key to confirm that it is appropriate to the version you upgraded to. Some upgrades require that you obtain a new license key.

Once the software upgrade has completed return here:

*   for a non-mirrored upgrade, continue to the [Health Insight Post-Upgrade Reactivation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade) procedure.
    
*   if you are upgrading a Health Insight mirror, return to the appropriate referring step in Upgrading a Health Insight Mirror:
    
    *   [Upgrade Instance B](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_upgradeB)
        
    *   [Upgrade Instance A](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_upgradeA)
        

> **Note:**
> 
> Note that HSAALIB and HSAA package compilation error messages like the following will sometimes appear in `ensinstall.log` during the upgrade:
> 
> ```
> Compiling class HSAA.Patient
> ERROR #5480: Property parameter not declared: HSAA.Patient:Comments:MAXLEN
>               > ERROR #5030: An error occurred while compiling class 'HSAA.Patient'
> ```
> 
> ```
> Dropping orphaned table: HSAA.<source-table>
> ```
> 
> In most cases, these errors are benign and will disappear from `ensinstall.log` after the upgrade and post-upgrade steps have completed. Contact the WRC if these errors do not disappear after you have completed all post-upgrade steps.
