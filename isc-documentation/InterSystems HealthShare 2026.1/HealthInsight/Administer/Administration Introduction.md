# [Introduction to Administering Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_intro#HSAAADM_intro)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq).

This chapter introduces the [administration tasks](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_intro#HSAAADM_intro_tasks) specific to HealthShare Health Insight and the [user interfaces](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_intro#HSAAADM_home_page) available in the product.

## [The Health Insight Tool](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_intro#HSAAADM_intro_arch)

Health Insight provides near real-time, analytical access to comprehensive clinical data from HealthShare Unified Care Record. Unified Care Record consists of many components, discussed elsewhere. Health Insight adds two components, discussed in this book:

*   A Feeder Gateway, which is responsible for feeding data from Unified Care Record to Health Insight.
    
*   An instance of Health Insight, the “analytics instance,” which includes the Health Insight production. The Health Insight production is responsible for receiving data from the Feeder Gateway and using it to update the InterSystems IRIS Business Intelligence source tables and cubes in Health Insight.
    

> **Note:**
> 
> Feeder Gateway is short for Health Insight Feeder Access Gateway. In previous releases, this gateway was known as the dedicated Access Gateway.

## [Administrative Tasks in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_intro#HSAAADM_intro_tasks)

The most common administrative task for Health Insight is to monitor the data feed. See the chapter “[Monitoring the Data Feed](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor).” This task includes monitoring the Feeder Gateway and the Health Insight production. For general information on managing productions, see [Managing Unified Care Record Productions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEENS), which provides information such as the following:

*   Terminology and basic concepts
    
*   General information on managing productions
    
*   Information on the production Event Log
    
*   Information on displaying and tracing messages
    

Other administrative tasks include the following:

*   Monitoring and managing the disk space on the analytics instance. This book does not discuss this task specifically.
    
*   Monitoring the data feed. See the chapter “[Monitoring the Data Feed](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_monitor).”
    
*   Tracking the flow of specific patient data. See the chapter “[Tracking Data to HealthShare Unified Care Record](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_trace).”
    
*   Troubleshooting data feed problems. See the chapter “[Troubleshooting Data Transfer Problems](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_prob).”
    
*   Resending data from the Unified Care Record to Health Insight. See the chapter “[Resending Data to Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_resend).”
    
*   Using the Consistency Check Tool to verify that data in Unified Care Record is being correctly transmitted to Health Insight. See the chapter “[Working with the Consistency Check Tool](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_consistency).”
    
*   Filtering incoming `AnalyticsUpdateRequest` messages. See the chapter “[Filtering Analytics Update Requests](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_filter).”
    
*   Creating user definitions, for users of the Health Insight instance. For information on creating users, see “[User Accounts](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSA_config_user_accounts).” For information on available roles and resources, see the chapter “[Roles and Resources in Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles).”
    
*   Purging messages. See [Managing Unified Care Record Productions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEENS).
    
*   Managing the persistent cache of messages, if Health Insight is using the persistent request feature. See “[Notes on Managing the Persistent Request Cache](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist#HSAAIC_persist_mng)” in the chapter “[Setting Up and Using Persistent Requests](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist)” in the Health Insight Installation and Configuration Guide.
    
*   Ensuring proper security and privacy protections for Health Insight data. See “[Ensuring Privacy, Security, and Trust in Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_securityconsiderations)”.
    

## [Accessing the Health Insight Home Page](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_intro#HSAAADM_home_page)

To access the home page for Health Insight:

1.  Log in to the Management Portal on the analytics instance.
    
2.  Select `HealthShare`.
    
3.  Select the name of your analytics namespace, typically `ANALYTICS` or `HSANALYTICS`.
    

The menu options on this page are for use by analysts, administrators, and implementers. This book discusses the options relevant to administrators. For a full list of the menu options and their uses, see “[Accessing the Health Insight Home Page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page)” in the Health Insight Installation and Configuration Guide.

Note that as an administrator, you may need to use the following additional tools:

*   Production management pages, which are accessible via a link at the top of the page. For general information, see [Managing Unified Care Record Productions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEENS).
    
*   Terminal. See [Using the Terminal](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GTER). Note that in this release, the Management Portal provides pages that enable you to perform many of the actions that were previously possibly only in the Terminal. You might still find it useful to use the Terminal on occasion.
