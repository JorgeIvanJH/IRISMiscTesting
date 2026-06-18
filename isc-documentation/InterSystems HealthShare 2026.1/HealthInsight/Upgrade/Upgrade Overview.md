# [Health Insight Upgrade Overview](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_up#HSAAUP_up)

> **Note:**
> 
> This book applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

This book describes how to upgrade an existing HealthShare Health Insight instance that uses the Feeder Gateway to the current version of Health Insight.

*   To upgrade a non-mirrored deployment of Health Insight, read this page and perform each procedure as directed.
    
*   To upgraded a Health Insight mirror, go to the [Upgrade a Health Insight Mirror](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror) procedure. That procedure contains additional instruction and links back to the other procedures in this book.
    

Refer to the [Supported Upgrade Paths](https://docs.intersystems.com/hs20261/csp/docbook/hssupportedbrowsers/HS_Platforms.pdf#page=2) document for a list of versions that you can upgrade from.

Please consider the important notices below about significant changes in Health Insight.

> **Important:**
> 
> ## [System Index Upgrades Not Supported](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_up#HSAAUP_nosysindex)
> 
> Upgrading to Health Insight version 2026.1 is [not supported](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20261#HSAARN_20261_sysindex) for customers who use a System Index-based feed. If your Health Insight deployment uses System Index, do not proceed with the upgrade.
> 
> ## [Private Web Server](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_up#HSAAUP_webserver)
> 
> Beginning with version 2024.2, the private Apache web server is no longer distributed and installed with any InterSystems product kits.
> 
> While your production systems likely already use a third-party web server, your development instances may not.
> 
> Upgrading customers must have a third-party web server installed on their system in order to use this, and all future versions of Health Insight. Before upgrading to this version of Health Insight, InterSystems strongly recommends installing and [configuring a third-party web server](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GCGI_private_web) for each instance if you haven’t already done so. Performing this configuration before you upgrade reduces the complexity of untangling any potential post-upgrade issues that may arise.
> 
> ## [Upgrading in a HealthShare Federation](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_up#HSAAUP_federation)
> 
> If you are upgrading Health Insight, you must upgrade other parts of your HealthShare federation as well. Before performing any upgrades, read the upgrade instructions for all of the components in your federation and create an overall upgrade plan. In your upgrade plan, make sure to upgrade the different components of your federation in the correct order. For information, see the [Unified Care Record Upgrade Guide](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEUPGRADE_overview).
> 
> Note that Health Insight version 2026.1:
> 
> *   can only receive data from version 2026.1 of HealthShare Unified Care Record.
>     
> *   is only compatible with version 2026.1 of the Clinical Viewer.
>     
> 
> ## [ChangedObjects Updates](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_up#HSAAUP_changedobjects)
> 
> Starting in version 2025.2, the behavior and management of [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) has been revised. During the upgrade to 2025.2, if the `Enable source data tracking` setting was selected prior to the upgrade, two system tasks — Peek HSAA.ChangedObjects and Purge HSAA.ChangedObjects — will be automatically scheduled as part of the upgrade. These tasks are only scheduled when source data tracking is enabled. Additionally, [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) is no longer cleared during analytics batch processing. Previously, changes were purged at the end of batch runs. Now, purging is handled independently by the Purge ChangedObjects task.
> 
> These changes may require updates to downstream systems. See the [post-upgrade reactivation procedure](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade) for guidance.
> 
> ## [Update Readmission Custom Methods](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_up#HSAAUP_readmissions)
> 
> Starting in version 2025.2, the implementation of the default method to calculate readmissions has changed. If you previously used a custom method to calculate readmissions and wish to continue doing so, it must be [updated accordingly](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade).

To upgrade a non-mirrored Feeder Gateway-based Health Insight deployment, perform the following procedures in order:

1.  [Run the pre-upgrade steps](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_preupgrade).
    
2.  [Perform the software upgrade](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_upgrade).
    
3.  [Perform the Health Insight post-upgrade reactivation procedure](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade).
    
4.  [Perform the Feeder Gateway post-upgrade reactivation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder).
    
5.  [Perform the Feeder Gateway post-upgrade restart](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgradefeeder).
    
6.  [Perform the post-upgrade cleanup steps](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_finalsteps).
