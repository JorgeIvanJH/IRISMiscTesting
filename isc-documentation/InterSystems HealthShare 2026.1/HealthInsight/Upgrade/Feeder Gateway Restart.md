# [Feeder Gateway Post-Upgrade Restart Procedure](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_postupgraderestart)

> **Note:**
> 
> The post-upgrade steps in this section are specific to systems that will continue to use the Feeder Gateway (AADBQ-based) architecture after the upgrade. If you chose to change to the System Index architecture, go to [Migrating to a System Index-Based Data Feed](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAMIG_migsysindex) instead.

Now that you have completed the [Post-Upgrade Reactivation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade) procedure for the Feeder Gateway, perform the following procedure to restart the Feeder Gateway. The steps are outlined below and detailed in the sections that follow:

1.  [Start the Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_postupgraderestart_start).
    
2.  [Check the status of the productions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_postupgraderestart_check).
    
3.  [Create a business operation on the Registry for AnalyticsQRequest messages](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_analyticsqrequest).
    
4.  [Backfill data, if necessary](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_resend).
    
5.  [Review the platform information dashboards](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_postupgraderestart_dashboard).
    
6.  [Next Steps](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_postupgraderestart_next).
    

## [Step 1: Start the Feeder Gateway](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_postupgraderestart_start)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary Feeder Gateway mirror member.

Enable the [HS.Gateway.Analytics.TransmitService](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.TransmitService) and start the Feeder Gateway production:

1.  Log in to the Management Portal on your Feeder Gateway instance as a user with administrative privileges.
    
2.  Navigate to `Home` > `HealthShare` > `feederGatewayNamespace`.
    
3.  Click the `Productions` link in the banner.
    
4.  Click `Configure` > `Production`. (If needed, select your Feeder Gateway production and click `Open`.)
    
5.  Click on the [HS.Gateway.Analytics.TransmitService](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Gateway.Analytics.TransmitService) in the list of business services.
    
6.  Select the `Enabled` checkbox in under `Basic Settings`.
    
7.  Click `Apply`.
    
8.  Click the `Start` button in the banner to start the production.
    

## [Step 2: Check the Status of the Productions](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_postupgraderestart_check)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary Analytics mirror member and Feeder Gateway mirror member.

Check the status both of the Feeder Gateway production and the Analytics production: `Home` > `Interoperability` > `namespace` > `Monitor` > `Production Monitor`.

## [Step 3: Create a Business Operation on the Registry for AnalyticsQRequest Messages](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_analyticsqrequest)

> **Note:**
> 
> Perform this step only if you upgraded from a version of Health Insight prior to 2021.1.
> 
> In a mirrored upgrade, perform this step only on the primary Registry mirror member.

Version 2021.1 introduced a dedicated Registry production component that processes AnalyticsQRequest messages. This component provides improved Registry performance when handling AnalyticsQRequest messages.

If you are upgrading from a version older than 2021.1, manually create the dedicated Registry production component:

1.  Log in to the Management Portal on your Registry instance as a user with administrative privileges.
    
2.  Navigate to `Home` > `HealthShare` > `registryName`.
    
3.  Click the `Open Production` link in the banner.
    
4.  Add a new business operation to the Registry production:
    
    1.  Click the `+` link next to `Operations`.
        
    2.  Select [HS.Hub.Management.Operations](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Hub.Management.Operations) as the `Operation Class`.
        
    3.  Enter `AnalyticsQRequestMessageOperations` as the `Operation Name`.
        
    4.  Select `Enable Now`.
        
    5.  Click `OK`.
        
5.  Select your new `AnalyticsQRequestMessageOperations` business operation from the list of business operations on the `Production Configuration` page.
    
6.  In the Settings pane, under `Additional Settings`, change the `Pool Size` of the operation to be `2`.
    
    Note that you can potentially change this value based on the needs of your system. This custom business operation is not bound by FIFO constraints, and can thus have a pool size greater than `1`. InterSystems recommends starting off with a `Pool Size` of `2`. Afterwards, if the performance of your Registry production is insufficient, you can use the `Production Monitor` (`Home` > `Interoperability` > `Monitor` > `Production Monitor` in the Analytics namespace) to monitor the custom business host for performance issues. As a rough guideline, if the queue size of the new custom component never exceeds the current pool size, then you are not likely to see performance improvements by increasing the pool size. If the queue size does exceed the pool size, then you may see a performance improvement by increasing pool size by 1. You should ultimately decide what pool size is best based on your observations and systems.
    
7.  Select [HS.Hub.HSWS.WebServices](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Hub.HSWS.WebServices) from the list of business services on the `Production Configuration` page.
    
8.  In the Settings pane under `Additional Settings`, set the `AnalyticsQRequestTarget` to be `AnalyticsQRequestMessageOperations`.
    
9.  Restart the Registry production.
    

## [Step 4: Backfill Data, if Necessary](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_resend)

> **Note:**
> 
> In a mirrored upgrade, perform this step only on the primary Health Insight mirror member.

Click the links to the 2018.1 Release Note sections below to determine if you need to backfill added fields for records previously received by Health Insight. Backfill is achieved by resending data to Health Insight. Resending large amounts of data can be time-consuming, so it is worthwhile to carefully consider which data you need to backfill.

Health Insight provides several API methods that cause the resend of only the specific streamlets (of the appropriate types) that are needed:

For more information on the resend API see [API for Monitoring and Managing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api#HSAAREF_api_methods_transmit).

### [Backfill Lab Results, Rad Results, Other Results](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_C21019)

Use [RequeueExistingMedOrdersForAnalytics()](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.API.Transmit)

### [Backfill MemberEnrollments](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_C21022)

Use [RequeueExistingMemberEnrollmentsForAnalytics()](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.API.Transmit#METHOD_RequeueExistingMemberEnrollmentsForAnalytics)

### [Backfill SocialHistories](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_C21025)

Use [RequeueExistingSocialHistoriesForAnalytics()](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.API.Transmit#METHOD_RequeueExistingSocialHistoriesForAnalytics)

## [Step 5: Review the Platform Information Dashboards](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_postupgraderestart_dashboard)

Review the Platform Information dashboards: `Home` > `HealthShare` > `analyticsNamespace` > `Platform Information`.

## [Next Steps](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgraderestart#HSAAUP_postupgraderestart_next)

Now that you have restarted the Feeder Gateway

*   If you are upgrading a non-mirrored system, continue to the next section to perform the [Post-Upgrade Cleanup Steps](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_finalsteps) procedure.
    
*   If you are upgrading a Health Insight mirror, return to the [referring step in Upgrading a Health Insight Mirror](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_mirror#HSAAUP_mirror_startproductions).
