# [Resending Data to Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_resend#HSAAADM_resend)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq).

You can resend existing HealthShare Unified Care Record data to HealthShare Health Insight.

> **Note:**
> 
> Feeder Gateway is short for Health Insight Feeder Access Gateway. In previous releases, this gateway was known as the dedicated Access Gateway.

## [Options for Resending Data to Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_resend#HSAAADM_resend_options)

There are four ways to resend data to Health Insight:

*   In the Terminal, call API methods in the Health Insight namespace as described in the rest of this chapter.
    
*   Use the procedure described in “[Performing a Bulk Load of Data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload)” in the Health Insight Installation and Configuration Guide.
    
*   If your system was set up to include the persistent request feature, resend the data contained in the persistent requests. See “[Using Persistent Requests to Retransmit Data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_read)” in the Health Insight Installation and Configuration Guide.
    
*   Use the `Resend Patient to Health Insight` page to resend patients to Health Insight with high priority.
    

In all cases, if you resend a large amount of data, before you load the data, follow the steps in “[Phase 1: Before Loading Data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkloadphase1)” in the Health Insight Installation and Configuration Guide. Similarly, after you load the data, follow the steps in “[Phase 3: After Loading Data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkloadphase3).”

## [Using Methods to Resend Data to Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_resend#HSAAADM_resend_overview)

This section describes how to call methods in the Terminal to resend existing Unified Care Record data to Health Insight. To do so:

Identify the kind of data to resend. This determines which method to use:

<table><tr><th>To resend ...</th><th>Use the method ...</th><th>See ...</th></tr><tr><td>All data for the given patient</td><td rowspan="4"><code>RequeueForAnalytics()</code></td><td rowspan="4"><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api">API for Monitoring and Managing Health Insight</a></td></tr><tr><td>All data from the given Edge Gateway</td></tr><tr><td>All data from the Registry</td></tr><tr><td>All data available in Unified Care Record</td></tr></table>

You can also use various API methods to resend specific streamlets. For example, if you need to backfill the data for medications and medications orders after performing an upgrade, you can use the `RequeueExistingMedOrdersForAnalytics()` method to cause the resend of only the specific streamlets (of the appropriate types) that are needed. For more information, see [API for Monitoring and Managing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api).

## [Using the Resend Patient to Health Insight Page](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_resend#HSAAADM_resend_operator)

You can use the `Resend Patient to Health Insight` page to resend a patient to Health Insight with high [priority](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_phase2_priority).

To do so, navigate to the `Resend Patient to Health Insight` page ([Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_intro#HSAAADM_home_page) > `Internal Data Management` > `Resend Patient to Health Insight`). Enter a single MPIID or a comma-separated list of MPIIDs of the patients that you want to resend to Health Insight and click `Resend`. The patient record(s) will be placed on the data feed queue with the highest priority for resend.

In order to facilitate more frequent high-priority resends, you can configure the Feeder Gateway Transmit batch size by changing the value of the `Transmit batch size` field on the `Additional Settings` [page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional). In this case, the Feeder Gateway batch size should be at least the number of patients that you want to resend to Health Insight. For example, if you entered 100 patients on the `Resend Patient to Health Insight` page, `Transmit batch size` should be at least 100.

After the resend has completed, you can revert the `Transmit batch size` field back to its previous setting.
