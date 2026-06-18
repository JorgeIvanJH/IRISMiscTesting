# [Configuration Procedure for a New Health Insight Instance](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

The procedure on this page describes how to set up a new instance of HealthShare Health Insight, with optional mirroring. If you have already configured your Health Insight instance and want to migrate it to use mirroring, use the [Migrating a Health Insight Instance to Use Mirroring](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAMIG_mighi) procedure instead.

> **Important:**
> 
> If you plan to use mirroring, then before you begin, InterSystems strongly recommends that you read and understand the [Mirroring](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror) chapter of the InterSystems IRIS data platform High Availability Guide. It contains important information about network and deployment considerations that you must plan for before you install and configure a mirrored Health Insight. When reading the chapter, keep in mind that you will be configuring a mirror that:
> 
> *   has two failover members
>     
> *   uses a VIP (Virtual IP address)
>     
> *   uses an arbiter and an ISCAgent
>     
> *   uses SSL/TLS
>     
> 
> Be sure to plan for the following:
> 
> *   Two machines on the same subnet to host the primary and backup failover mirror members.
>     
> *   A machine to host the arbiter.
>     
> *   X.509 certificates for SSL/TLS encryption of mirrored communication.
>     
> *   A Virtual IP address for the mirror.
>     

To install and configure a newly installed Health Insight instance, with or without mirroring, follow the steps outlined below and detailed in the sections that follow:

1.  [Install the Health Insight instances](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_install).
    
2.  [Configure security](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_security).
    
3.  (Mirror-only) — [Create the mirror](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_mirror).
    
4.  [Create additional Health Insight databases](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_databases).
    
5.  [Create the Health Insight production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_production).
    
6.  [Map Globals to Your Additional Databases](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_globals).
    
7.  (Mirror-only) — [Create the ^ZMIRROR routine](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_ZMIRROR).
    
8.  [Configure the Health Insight production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_config).
    
9.  [Set up production message purge](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_purge).
    
10.  (Mirror-only) — [Fail over and perform the final mirror configuration procedures](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_1stfailover).
     

[Next steps in a Health Insight implementation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_next_steps).

## [Step 1: Install the Health Insight Instances](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_install)

> **Note:**
> 
> Skip this step if you have already installed your Health Insight instance(s).

If you have not already installed Health Insight, then:

### [For a mirrored deployment](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13202)

You will require two instances of Health Insight:

*   The machines hosting the instances must be on the same subnet.
    
*   Use the same superserver port and web server port on each instance.
    
*   Designate one instance as instance A and the other as instance B. Instance A and instance B will be your two failover members.
    
    As you follow the instructions in this procedure, these designations will make the instructions easier to follow.
    

### [For a non-mirrored deployment](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13205)

You will require one instance of Health Insight.

1.  Follow the [Installing a HealthShare Kit](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSDEPLOY_install) procedure to install your instances.
    
2.  Record the instance name, superserver port, and web server port of each instance you install, as you will need them in a later step.
    

## [Step 2: Configure Security](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_security)

On each of your Health Insight instances, perform the first five steps of the procedure in [Setting Up Secure Communication](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ASecureComm).

This will ensure that Health Insight is secure, and that it communicates securely with Unified Care Record.

Once your security configuration is complete:

*   If you plan to mirror Health Insight, go to the next step, [Create the Mirror](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_mirror).
    
*   If you do not plan to mirror Health Insight, skip the next step and all of its sub-procedures and go directly to the following step, [Create Additional Databases for Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_databases).
    

## [Step 3: Create the Mirror](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_mirror)

*   If you plan to mirror Health Insight, complete all of the sub-procedures in this step.
    
*   If you do not plan to mirror Health Insight at this time, skip this entire step and all of its sub-procedures and go directly to the following step, [Create Additional Databases for Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_databases).
    

### [Mirror Step 3A: Create a Virtual IP Address and DNS Names](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_create_VIP)

A virtual IP address (VIP) allows external applications to interact with the mirror using a single address, ensuring continuous access on failover.

Follow the instructions in the section “[Configuring a Mirror Virtual IP (VIP)](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror_set_config#GHA_mirror_set_virtualip)” of the InterSystems IRIS High Availability Guide to configure your VIP.

Once you create your VIP, assign a DNS name for it on your DNS server to make it easier to refer to the VIP in your productions.

The table below shows how this might be set up:

<table><tr><th>&nbsp;</th><th>IP Address</th><th>DNS Name</th></tr><tr><td>Instance A</td><td>10.1.1.10</td><td>HS-HealthInsight-nodeA.<code>my-company</code>.com</td></tr><tr><td>Instance B</td><td>10.1.1.11</td><td>HS-HealthInsight-nodeB.<code>my-company</code>.com</td></tr><tr><td>Mirror</td><td>10.1.1.100</td><td>HS-HealthInsight-mirror.<code>my-company</code>.com</td></tr></table>

The VIP will serve as the `network host name` when you configure Health Insight.

> **Note:**
> 
> Record the IP address, DNS name, CIDR mask, and network interface as you will need these values in a later step.

### [Mirror Step 3B: Set Up and Configure an Arbiter](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_configure_arbiter)

InterSystems strongly recommends the use of an arbiter in a mirrored Health Insight. An arbiter will ensure fast, reliable failovers. Follow the instructions in the section “[Installing the Arbiter](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror_set_config#GHA_mirror_set_config_arbiter)” in the InterSystems IRIS High Availability Guide.

> **Note:**
> 
> Record the hostname and IP address of your arbiter as well as the port used by its ISCAgent process (2188 by default). You will need this information in a later step.

### [Mirror Step 3C: Create SSL/TLS Configurations for the Mirror](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_SSL)

Follow the instructions in “[Configuring InterSystems IRIS to Use TLS with Mirroring](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ROARS_tls_mirroring)” to create SSL/TLS configurations for your mirror. You must perform the procedure on both instance A and instance B. As part of this procedure, you will enable mirroring on each instance.

> **Note:**
> 
> While SSL/TLS is not strictly required for mirror communications, InterSystems strongly recommends its use for systems that deal with confidential health data.

### [Mirror Step 3D: Configure the ISCAgents](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_ISCAgent)

Follow the instructions in the “[Configuring the ISCAgent](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror_set_config#GHA_mirror_set_agent)” section of the InterSystems IRIS High Availability Guide to configure the ISCAgent on instance A and instance B. It is crucial that the ISCAgent is configured to start automatically when the operating system starts on both instance A and instance B.

> **Note:**
> 
> Record the ISCAgent port number if you use a value other than the default, as you will need it in a later step.

### [Mirror Step 3E: Set the HealthShare Network Host Name to the Mirror VIP](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_set_HealthShare_network_host_name)

The network host name forms part of each URL that is created when you configure your productions in Health Insight. Since this is a mirrored system, it is important that this value reflect the mirror VIP rather than the network name of each individual instance.

1.  On instance A, log in to the Management Portal with administrator privileges.
    
2.  Click `HealthShare` to open the HealthShare Management portal.
    
3.  Select the `HealthShare` > `Installer Wizard` link in the banner.
    
4.  Select `Configure Network Host Name`.
    
5.  Enter the VIP or DNS name in the `Network Host Name` field.
    
6.  Click `Save`.
    
7.  Repeat this procedure on instance B.
    

### [Mirror Step 3F: Create and Configure the Mirror](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_create_mirror)

Review the instructions in the “[Configuring Mirroring](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror_set_config)” section of the InterSystems IRIS High Availability Guide. In the steps described under the section “[Creating a Mirror](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror_set_config#GHA_mirror_set_configmembers)”.

> **Note:**
> 
> You have already performed the following procedures:
> 
> *   Installing the arbiter
>     
> *   Starting the ISCAgent
>     
> *   Securing the mirror with SSL/TLS
>     

Refer to the table below for the settings to use as you continue to configure the mirror:

<table><tr><th>Setting</th><th>Value</th><th>Value on Your System</th></tr><tr><td><code>First Failover Member</code></td><td>The instance name you noted earlier for Instance A</td><td>&nbsp;</td></tr><tr><td><code>Second Failover Member</code></td><td>The instance name you noted earlier for Instance B</td><td>&nbsp;</td></tr><tr><td><code>Mirror Name</code></td><td>Select a name using 1 to 15 alphanumeric characters.</td><td>&nbsp;</td></tr><tr><td><code>Require SSL/TLS</code></td><td>Yes. You should have configured this in an earlier step.</td><td>&nbsp;</td></tr><tr><td><code>Use Arbiter</code></td><td>Yes. Provide the hostname, IP and port you noted in an earlier step.</td><td>&nbsp;</td></tr><tr><td><code>Use Virtual IP</code></td><td>Yes. Provide the VIP or DNS name, CIDR mask, and network interface value you noted in an earlier step.</td><td>&nbsp;</td></tr><tr><td><code>Mirror Member Name</code></td><td>For example, “MyInsight_Mirror_A” and “MyInsight_Mirror_B”.</td><td>&nbsp;</td></tr><tr><td><code>Superserver Address</code></td><td>Accept the default.</td><td>&nbsp;</td></tr><tr><td><code>ISCAgent Port</code></td><td>Enter the ISCAgent port number on this instance that you noted in an earlier step. The default is 2188.</td><td>&nbsp;</td></tr><tr><td><code>Quality of Service Timeout</code></td><td>Accept the default. You can adjust this later if issues arise.</td><td>&nbsp;</td></tr><tr><td><code>Mirror Private Address</code></td><td>Accept the default.</td><td>&nbsp;</td></tr><tr><td><code>Compression Mode for Failover</code></td><td>Accept the default, <code>System Selected</code></td><td>&nbsp;</td></tr><tr><td><code>Compression Mode for Async</code></td><td>Accept the default, <code>System Selected</code></td><td>&nbsp;</td></tr></table>

Perform the following steps to complete the configuration of your mirror:

> **Note:**
> 
> Some of the instructions in the referenced sections below exclude the submenu `Mirror Settings`. If you do not see the menu option that is referenced, click `Mirror Settings` and you will see the option.

1.  Configure instance A as the first failover member as described in “[Create a Mirror and Configure the First Failover Member](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror_set_config#GHA_mirror_set_configmembers_first)”.
    
2.  Configure instance B as the second failover member as described in “[Configure the Second Failover Member](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror_set_config#GHA_mirror_set_configmembers_second)”.
    
3.  On instance A, perform the steps in “[Authorize the Second Failover Member](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror_set_config#GHA_mirror_set_configmembers_third)”.
    
4.  Confirm that your mirror is configured correctly and is running as described in “[Review Failover Member Status in the Mirror Monitor](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror_set_config#GHA_mirror_set_configmembers_monitor)”.
    
5.  STOP. Do not add any databases to the mirror.
    

Now your mirror contains two failover members:

*   Instance A is the primary failover member
    
*   Instance B is the backup failover member.
    

> **Note:**
> 
> Going forward, this document will refer to “primary failover member” and “backup failover member” rather than “instance A” and “instance B”.

> **Important:**
> 
> Do not add any databases to the mirror yet.

### [Mirror Step 3G: Add HSSYS to the Mirror, Copy and Catch Up HSSYS](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_catchup_db)

This step consists of the following sub-procedures:

*   [Add HSSYS to the mirror](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_add_HSSYS)
    
*   [Copy HSSYS to the backup failover member](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_copy_HSSYS)
    
*   [Activate and catch up the HSSYS database](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_catchup_HYSSYS)
    

#### [Add HSSYS to the Mirror](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_add_HSSYS)

Now that you have created the mirror, you can mirror the databases. For a new installation, you only have to mirror one database, `HSSYS`. When you configure Health Insight using the Installer Wizard (or an installer script), all of the databases that are created in that process will then be automatically mirrored.

Review the instructions in the “[Add an Existing Database to the Mirror](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror_set_config#GHA_mirror_set_configdbs_existing)” section of the InterSystems IRIS High Availability Guide.

To add the `HSSYS` database to the mirror:

1.  On the primary failover member, log in to the Management Portal with administrator privileges.
    
2.  Select `System Administration` > `Configuration` > `System Configuration` > `Local Databases`.
    
3.  Select `HSSYS` > `Add to Mirror <your_Mirror_name>` .
    
4.  Click `Add` to confirm the procedure.
    

#### [Copy HSSYS to the Backup Failover Member](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_copy_HSSYS)

The simplest way to create a copy of the `HSSYS` database on the backup failover member is to use the copy command as described in the procedure below.

> **Note:**
> 
> Alternatively, you can use a backup/restore procedure to create a backup on the primary member and restore it on the backup member. Refer to the “[Add an Existing Database to the Mirror](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror_set_config#GHA_mirror_set_configdbs_existing)” section of the High Availability Guide for backup/restore considerations and links to information about backup/restore strategies. Also see the “[Run Database Backups](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEOPS_db_backup)” section of the HealthShare Monitoring and Operations Guide for Healthshare-specific guidance on backup and restore strategies. If you do use an alternate method, remember to stop your instances as described below before proceeding.

1.  Stop the instances in your mirror:
    
    1.  Stop instance B, the backup failover member first, to prevent mirror failover.
        
    2.  Stop instance A, the primary failover member.
        
2.  Copy the `HSSYS` database from the primary to the backup:
    
    1.  Copy the `<installdir>/mgr/hssys/IRIS.DAT` file from the primary member to the same directory on the backup member, overwriting the existing `IRIS.DAT` file.
        
    2.  If you are on a UNIX system: on the backup member, set UNIX permissions on the `IRIS.DAT` file as described in the “[UNIX Users, Groups and Permissions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSA_using_unix#GSA_using_unix_users)” section of the “Using InterSystems IRIS on UNIX, Linux, and Mac OS X” chapter of the InterSystems IRIS System Administration Guide.
        
3.  Restart the instances in your mirror:
    
    1.  Start instance A so it comes up as the primary failover member.
        
    2.  Next start instance B. It will start as the backup.
        

#### [Activate and Catch Up the HSSYS Database on the Backup Failover Member](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_catchup_HYSSYS)

Now that the `HSSYS` database is copied over, activate and catch up the database on the backup failover member:

1.  Log in to the Management Portal on the backup failover member with administrator privileges.
    
2.  Select `System Operation` > `Mirror Monitor`.
    
3.  In the mirrored database list, select `Catchup` for `HSSYS` from the list of available databases. The catchup operation will also activate if necessary.
    

### [Mirror Step 3H: Start the Mirror Agent](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_Mirror_Monitor_Agent)

Mirroring in HealthShare products uses a mirror agent (in addition to the ISCAgent you configured earlier) to keep the instance GUIDs of the two mirror members synchronized.

Follow the procedure below to refresh the mirror agent on your mirror members by stopping the agent and restarting it:

1.  Log in to the Management Portal on the primary failover member with administrator privileges.
    
2.  Select `HealthShare` to open the HealthShare Management Portal.
    
3.  Select the `Mirror Agent Monitor` link in the banner.
    
4.  The agent auto-starts every five minutes, so it may already be running.
    
5.  If the agent is running, toggle the Agent off, and wait for the toggle to indicate that the Agent is not running.
    
6.  Toggle the Agent on.
    
7.  Repeat this procedure on the backup failover member.
    

## [Step 4: Create Additional Databases for Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_databases)

> **Note:**
> 
> In a mirrored Health Insight deployment, perform this step on the primary mirror member. In a [later step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_1stfailover_databases), you will make the same change on the other mirror member when it is the primary.

For better performance, InterSystems recommends that you configure the analytics instance so that [specific data is stored in additional databases](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2IMP_ch_setup#D2IMP_setup_global_mapping). For details on creating databases, see the chapter “[Configuring Databases](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSA_config_database)” in the InterSystems IRIS System Administration Guide.

Create the following additional databases:

<table><tr><th>Suggested Name</th><th>Options</th><th>Purpose</th></tr><tr><td><code>HSAACACHE</code></td><td>Create a resource for this database</td><td>Store analytics cache information</td></tr><tr><td><code>HSAAFACT</code></td><td>Create a resource for this database.</td><td>Store the generated fact tables and index global</td></tr></table>

You will define global mappings to these new databases in a [later step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_globals).

Note that you should never mirror `HSAACACHE`. The `HSAACACHE` database should be placed on a local database residing on a high-performance storage volume.

You may mirror `HSAAFACT`, but only do so if you understand the implications:

<table><tr><th>Advantages of Mirroring HSAAFACT</th><th>Disadvantages of Mirroring HSAAFACT</th></tr><tr><td><ul><li><p>Immediate Business Intelligence cube query support following failover</p></li></ul></td><td><ul><li><p>Slower cube sync and build performance</p></li><li><p>Risk of deadlock</p></li><li><p>Increased journaling file usage</p></li></ul></td></tr></table>

When you define a database, the Management Portal provides an option to create a resource and associate it with the database. Use this option for these databases, and use the default resource names provided by the Management Portal. These names are %DB_HSAACACHE and %DB_HSAAFACT, respectively.

When you create the resources, the Management Portal also creates the associated roles %DB_HSAACACHE and %DB_HSAAFACT.

> **Important:**
> 
> Make a note of your selections, as you will perform this procedure again on the other mirror member in a later step.

### [Journaling Recommendations (When not Mirroring)](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_journal_rec)

The following journaling recommendations apply only if you are not mirroring Health Insight:

<table><tr><th>Database</th><th>Journaling Recommendation</th><th>Notes</th></tr><tr><td><code>HSAACACHE</code></td><td>Off</td><td>Cached globals can be fully regenerated</td></tr><tr><td><code>HSAAFACT</code></td><td>Off during initial cube build after bulk data load; on at all other times</td><td>Generated fact tables and indexes can be regenerated, but if the cube builds take a long time it is best to journal after the initial build</td></tr><tr><td><code>HSANALYTICS</code></td><td>On</td><td>All source table data is stored here. You will create this database as part of your analytics namespace activation in the <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_production">next step</a>.</td></tr></table>

## [Step 5: Create the Health Insight Namespace, Production, and Database](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_production)

> **Note:**
> 
> In a mirrored Health Insight deployment, perform this step on the primary mirror member.

In this step you will use the HealthShare Installer Wizard to create the Health Insight production.

The steps are as follows:

1.  Open the Management Portal.
    
2.  Select the `HealthShare` tab and then select the `Installer Wizard` link at the top left of the screen.
    
3.  Select `Configure Health Insight` and set the following fields:
    
    *   `Local Name` — Specify the value you choose as the namespace for the analytics instance. The suggested name is `HSANALYTICS`.
        
    *   `Mirror Database` — Select this if you are using mirroring and are already on a mirrored system. This option is unavailable if you are not on a mirrored system.
        
    *   `Enter a Hub Host` — Specify the network name of the HealthShare Unified Care Record Registry, which is either a machine name or a virtual IP address (if the Registry is mirrored).
        
    *   `Enter A Hub Port` — Specify the port of the HealthShare instance that hosts the Unified Care Record Registry.
        
    *   `Enter a Hub Name` — Specify the namespace associated with the Registry.
        
    *   For `Connect to Hub Securely`, select this if this is a production system. Optionally select it for a development or test system.
        
        *   The web server on your Registry instance should be configured to only allow secure connections to the Registry.
            
        *   You should have an SSL/TLS configuration on this instance that can communicate with the Registry (see [Create an SSL/TLS Configuration for each Instance in the Federation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ASecureComm#ASecureComm_ssl_configuration) in Setting Up Secure Communication in HealthShare Instances). This SSL/TLS configuration should have the same name as the SSL/TLS configuration on the Registry instance, as all instances in a federation share a single service registry, and the HSREGISTRY service registry entry identifies which SSL/TLS configuration to use.
            
        
        Once you select `Connect to Hub Securely`, enter the SSL/TLS configuration in the `SSL Configuration` field that appears. Now, the Hub endpoint URL will be created using “https” rather than “http”, and the identified SSL/TLS configuration will allow the Gateway to connect to the registry securely at initial startup.
        
    
    > **Important:**
    > 
    > When you run the Installer Wizard, accept the default value in the `Network Name` field. This value should default to `<Network Host Name>:<Local Name>`. Since you set the network host name to the mirror VIP or DNS name in an earlier step, the Installer Wizard will create your Health Insight production correctly for mirroring only if you use the default value.
    
    > **Note:**
    > 
    > Record the value you entered for `Local Name` in the Installer Wizard for each production you create, as you will need it in a later step.
    
4.  Select `Save`.
    
5.  In the table labeled `The Following Configurations Have Been Defined`, find the row for the new Analytics configuration and select `Activate`.
    
6.  In the `Activation Configuration` window, select `Start`.
    
    The wizard creates a new namespace and database to contain the analytics instance. The namespace contains mappings that provide access to the needed system code. The wizard also defines the Health Insight production. A [later subsection](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_setup_ns_contents) provides an overview of the contents of the `HSANALYTICS` namespace.
    
    The wizard also enables a set of [menu options](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page) that apply to Health Insight. These are available in the `HSANALYTICS` namespace.
    

### [Alternative Setup (Demo Instance)](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_setup_demo)

To set up Health Insight for a demo installation, perform the following steps:

1.  Open the Terminal and switch to the `HSLIB` namespace.
    
2.  Enter the following command:
    
    ```objectscript
     do ##class(HS.Util.Installer).InstallDemo()
    ```
    

You may also use the `InstallBusDemo` method, in which case the call is:

```objectscript
 do ##class(HS.Util.Installer).InstallBusDemo()
```

Both of these demo installation methods include Health Insight. For more information on these installation methods, see [Creating a Unified Care Record Demo System](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEDEMO_app_demo).

### [Contents of the HSANALYTICS Namespace](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_setup_ns_contents)

The `HSANALYTICS` namespace contains the following items:

*   `CSPX`, `Ens`, `EnsLib`, and `EnsPortal` packages.
    
*   `HS` package, used by other parts of HealthShare.
    
*   `Analytics` package. This contains abstract cubes on which the Health Insight cubes are based. These classes are not intended for direct use.
    
*   `HSAA` package. This includes the following items:
    
    *   Classes that contain the source records used by the cube. These classes are not in subpackages and do not have names ending in `Cube`. For an introduction, see the chapter “[Introduction to the SQL Data Model](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel)” in the Health Insight User Guide.
        
    *   Cube classes. These have names ending in `Cube`, such as `PatientCube`.
        
    *   `Cubes` class. This contains utility methods for working with the Health Insight cubes.
        
    *   `Dashboards` subpackage. This contains classes that define the Health Insight dashboards.
        
    *   `KPI` subpackage. This contains KPI classes defined for Health Insight, including the patient action class ([HSAA.KPI.PatientActions](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.KPI.PatientActions)).
        
    *   `TransferSDA3` subpackage. This contains the sample production that the Installer Wizard copies to create your Health Insight production.
        
    *   `Local` subpackage. This contains SDA extensions.
        
    *   `Actions` subpackage. This contains definitions of dashboard actions.
        
    
    Ignore other items in this package. Note that `Health Insight` contains a generated subpackage for each cube.
    
*   `NAMESPACEPKG` package, where `NAMESPACE` is the value provided to the `Local Name` field of the Installer Wizard. This package contains the Health Insight production, which Health Insight uses to receive data from the Feeder Gateway in Unified Care Record.
    

## [Step 6: Map Globals to Your Additional Databases](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_globals)

> **Note:**
> 
> In a mirrored Health Insight deployment, perform this step on the primary mirror member. In a [later step](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_1stfailover_databases), you will make the same change on the other mirror member when it is the primary.

Define the following [global mappings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GGBL_mapping) in the new `HSANALYTICS` namespace:

### [Map to HSAACACHE database](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13474)

`^DeepSee.BucketList`

`^DeepSee.Cache.*`

`^DeepSee.JoinIndex`

`^DeepSee.UpdateCounter`

### [Map to HSAAFACT database](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13479)

`^DeepSee.Fact`

`^DeepSee.FactRelation`

`^DeepSee.Index`

## [Step 7: Create the ^ZMIRROR Routine](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_ZMIRROR)

> **Note:**
> 
> *   If you are mirroring Health Insight, complete this step on both mirror members.
>     
> *   If you are not mirroring Health Insight, skip this step and go to the following step [Configure the Health Insight Production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_config).
>     

The ^ZMIRROR routine implements configuration-specific logic and mechanisms for specific mirroring events, such as a failover member becoming primary. The ^ZMIRROR has four entry points. The routine below uses the `NotifyBecomePrimary` entry point to start the Health Insight productions on failover, and to reset the analytics agents in your audit namespace.

Create a ^ZMIRROR routine on your primary and backup failover members as follows:

1.  Connect to the primary failover member using [your IDE](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides).
    
2.  Change to the `%SYS` namespace.
    
3.  Create a new `ObjectScript Routine`.
    
4.  Enter the following code:
    
    ```objectscript
    ZMIRROR //For Health Insight
       quit
    NotifyBecomePrimary() public
       // Start productions after failover
       new $namespace
       set $namespace="HSLIB"
    
       // Comment out the following line if you are using production auto-start
       do ##class(HS.Director).StartAll()
    
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
    
    Refer to the “[Using the ^ZMIRROR Routine](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror_set_config#GHA_mirror_set_tunable_params_zmirror_routine)” section of the “Mirroring” chapter of the InterSystems IRIS High Availability Guide for more details on the ^ZMIRROR routine.
    
5.  Save the routine as `ZMIRROR.mac` .
    
6.  Compile the routine.
    
7.  Duplicate this routine on the backup failover member.
    
8.  Save and compile it.
    

> **Note:**
> 
> The production auto-start feature may be used in Health Insight if you employ appropriate `Relative Startup Priority` values, as documented in [Enabling and Disabling Automatic Production Startup](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEENS_ch_emp#HEENS_emp_auto_start), since the order in which the productions start is important. HealthShare also provides the [HS.Director.StartAll()](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSLIB&CLASSNAME=HS.Director#METHOD_StartAll) method, which starts the productions in the correct order without additional configuration. You should use production auto-start instead of calling [HS.Director.StartAll()](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSLIB&CLASSNAME=HS.Director#METHOD_StartAll) in your ^ZMIRROR routine.

## [Step 8: Configure the Health Insight Production](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_config)

> **Note:**
> 
> In a mirrored Health Insight deployment, perform this step on the primary mirror member.

In this step you will configure the Health Insight production.

The steps are as follows:

1.  Display the Health Insight production (`NAMESPACE PKG.HSAAProduction`, where `NAMESPACE` is the name of the analytics namespace, usually `HSANALYTICS`).
    
2.  Review the settings in this production and make changes as needed. The default settings are suitable for a live system. While you are developing and testing your system, you might want to use different settings; if so, remember to readjust the settings when your system goes live.
    
    First examine the following settings of the production. These settings control how and where this production writes the Health Insight log, which records information about the transfer of data to Health Insight. This log can be quite large.
    
    Note that the Health Insight log displays only errors related to processing streamlets; be sure to examine the production Event Log for errors of other kinds.
    
    ### [LogTarget](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_config_logtarget)
    
    Specifies where to write the Health Insight log. Choose one of the following:
    
    ### [Console](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13522)
    
    Write logging information to the Terminal. This option applies only if the business host ([HSAA.TransferSDA3.WebServices](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.WebServices), [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer), [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer) or [HSAA.TransferSDA3.Operation.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Batch)) is running in the foreground (has the Foreground setting enabled).
    
    ### [File](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13525)
    
    Write logging information to files in the directory specified by the `TargetPath` setting. By default, the files are written to the directory `install-dir/mgr/Temp`. Ensure that the target path both exists and is writable.
    
    ### [Global](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13528)
    
    Write logging information to the global specified by the `TargetPath` setting. By default, the global is `^IRIS.HSAA.TransferLog`.
    
    ### [Table](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13531)
    
    This is the default. Write logging information to the table `HSAA_Report.Log`.
    
    ### [TargetPath](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_config_targetpath)
    
    Specifies the name of the directory or global to which the production should write the Health Insight log. This option applies only if `LogTarget` is File or Global.
    
    ### [LogLevel](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_config_loglevel)
    
    Specifies the amount of information to include in the Health Insight log. Choose one of the following values. The logging levels listed below are ordered by how much information is written:
    
    ### [NONE](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13539)
    
    This option does not create a log. This option can be useful during initial setup. InterSystems highly recommends that you do not use this option for a live system.
    
    ### [ERROR](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13542)
    
    This option logs errors.
    
    ### [WARNING](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13545)
    
    This is the default. This option logs errors and warnings. A warning typically indicates a condition that should be examined. An error indicates a condition that should be corrected.
    
    ### [INFO](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13548)
    
    This is the usual option during development and testing.
    
    ### [DEBUG](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13551)
    
    This option is typically used only for debugging.
    
    ### [TRACE](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13554)
    
    This option writes the most possible information to the log.
    
    When you choose a logging level, take care to consider the disk space consumed by logging.
    
    ### [LogTimeFormat](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_config_logtimeformat)
    
    Specifies the time format used in the log (except when `LogTarget` is `Table`). Specify a comma-separated string in which the first item is an integer code specifying the date format, the second item is an integer code specifying the time format, and the third item is the precision. See the documentation for [$ZDATETIME](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=RCOS_fzdatetime) for details.
    
    When `LogTarget` is `Table`, the log time is written as a standard ODBC time stamp.
    
3.  Optionally modify the following settings of the [HSAA.TransferSDA3.Service.Interrupt](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Service.Interrupt):
    
    ### [Call Interval](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13568)
    
    Specifies the interval, in seconds, at which an analytics batch will interrupt the data ingestion process and run. The minimum value is 300.
    
    The interrupt will disable the [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer) activity.
    
    Note that decreasing the call interval will not necessarily equate to an increase in performance. If you are uncertain regarding appropriate `Call Interval` values, please contact the [InterSystems Worldwide Response Center (WRC)](https://www.intersystems.com/support-learning/support/).
    
4.  Optionally modify the following settings of the [HSAA.TransferSDA3.Process.Batch](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Batch):
    
    ### [EnableDeferredACNQueries](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13577)
    
    Specifies whether to enable deferred [analytics queries](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_query) (which are analytics queries defined with `Notification` as `Transfer Complete` or `Synchronization Complete`). If you disable this setting, Health Insight does not notify the Edge Gateways and any deferred queries are never run (unless they are part of a dynamic cohort).
    
    If you are not using Advanced Clinical Notifications (ACN) or you are using only queries that run in Immediate mode, disable this setting to avoid the additional overhead required for deferred queries.
    
    This setting has no effect on immediate queries or dynamic cohorts.
    
    By default, this setting is not selected.
    
    ### [MaxNumQuery](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13582)
    
    Determines how many [analytics query definitions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_query) are run during each analytics batch.
    
    The default setting is 5. A setting of -1 will cause all queries in the [HS.Message.Analytics.QueryRequest](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.Message.Analytics.QueryRequest) table to be run.
    
5.  Optionally modify the `ToFile`, `FileTarget`, `ToSQL`, and `SQLTarget` settings of the [HSAA.TransferSDA3.Process.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.Transfer). These settings are used for the optional [persistent requests](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist) feature.
    
6.  If you are using [analytics query definitions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_query), either for clinical message delivery or for cohort membership, you may optionally modify the following settings of the [HSAA.Query.Process](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Query.Process):
    
    ### [Pool Size](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13590)
    
    Determines how many queries can be run in parallel. The recommended pool size can vary based on your specific hardware. If you are uncertain regarding appropriate `Pool Size` values, please contact the [InterSystems Worldwide Response Center (WRC)](https://www.intersystems.com/support-learning/support/).
    
7.  Optionally modify the following settings of the [HSAA.TransferSDA3.Operation.Transfer](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Operation.Transfer):
    
    ### [Pool Size](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13599)
    
    Determines how many requests can be processed in parallel. The recommended pool size can vary based on your specific hardware. If you are uncertain regarding appropriate `Pool Size` values, please contact the [InterSystems Worldwide Response Center (WRC)](https://www.intersystems.com/support-learning/support/).
    
    > **Important:**
    > 
    > The `Pool Size` setting affects performance, as do many of the production settings. There is no single best set of recommendations for these values, because environments are highly variable.
    
8.  If you want to enable users to use the `View Patient Record` action, modify the following setting of `AccessGatewayViewer`:
    
    ### [ServiceName](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13606)
    
    Specifies the Viewer Access Gateway that will retrieve and display the patient record. This Viewer Access Gateway must be part of the HealthShare federation.
    
    For details on setting this value, see [Business Operations](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_production#HSAAREF_production_operations) in the Health Insight Production Details.
    
9.  Apply any changes.
    
10.  If you are using cubes, navigate to the `Cube Sync Settings` [page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent#HSAAIC_cubescurrent_sync_enable) to verify that the proper cube groups are included in the Health Insight cube synchronization process. A new installation of Health Insight will have a predefined cube registry with two cube groups, the Health Insight Reporting Group and the [deprecated](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20261#HSAARN_20261_cube_deprecate) Health Insight Clinical Group. By default, cubes are disabled, meaning that these groups are not scheduled for cube sync. You can choose to enable cubes at a later time if needed.
     
     If you are not using cubes, [set up a task to periodically clear ^OBJ.DSTIME](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent#HSAAIC_cubescurrent_disable).
     
11.  Start the production. Or start the production later, when you send the initial data feed.
     
     For more details on the Health Insight production, see [Health Insight Production Details](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_production).
     

### [Suppressing the Transfer of Large Data Sets](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_config_suppress)

Certain data sets in Unified Care Record can be very large. Health Insight has the option to disable the transmission event/care provider/site and document stream data from Unified Care Record. These options should be set before sending the initial data feed.

To disable the transmission of either event/care provider/site data or document stream data, see [Additional Settings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional) in [Customizing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube).

If you disable the transmission of event/care provider/site data, the `Event/Care Provider/Sites` cube becomes unavailable. For information on this cube, see [Orientation to the Cubes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube) in the Health Insight User Guide.

If you disable the transmission of document stream data, the `Stream` property of the `Document` object is no longer available. Although this has no direct effect on the `Document` cube, it prevents the use of any listings that use the `Stream` property of the `Document` object.

## [Step 9: Set Up Nightly Interoperability Message Purges](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_purge)

> **Note:**
> 
> In a mirrored Health Insight deployment, configure the purge task on both mirror members.

Nightly production message purging is an important part of Health Insight management. In the Health Insight namespace, there should be a nightly task to purge messages, with the following configuration options:

*   `Include message bodies` — Select this option.
    
*   `Purge only completed sessions` — Clear this option.
    

The `Do not purge most recent days` option specifies how many days of messages to keep. A value between 7 and 30 days is typical. For more information on how to configure production message purging, see [Purging Production Data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=EGMG_purge).

Now that your purge task is configured on all of your instances:

*   If your Health Insight deployment is mirrored, continue to the next step [Perform Final Mirror Configuration](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_1stfailover).
    
*   If your Health Insight is not mirrored, your configuration is now complete. Skip directly to [Next Steps in a Health Insight Implementation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_next_steps).
    

## [Step 10: Perform Final Mirror Configuration](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_1stfailover)

*   In a mirrored Health Insight deployment, perform the procedures in this step to complete the configuration of the second mirror member.
    
*   If your Health Insight is not mirrored, then your Health Insight configuration is now complete. Skip this entire step and go directly to [Next Steps in a Health Insight Implementation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_next_steps).
    

Perform the following procedures to complete the mirror configuration. When this step is complete, the mirror members will be configured identically.

1.  [Fail over](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_1stfailover_fail).
    
2.  [Reactivate Analytics on the new primary](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_1stfailover_reactivate).
    
3.  [Create the additional databases on the new primary](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_1stfailover_databases).
    
4.  [Map globals to the new databases on the new primary](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_1stfailover_map).
    

### [Mirror Step 10A: Fail Over](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_1stfailover_fail)

Perform a controlled failover. The backup member will become the primary.

1.  Stop the primary member:
    
    *   Use the `iris stop` command (or stop the instance from the Windows HealthShare cube).
        
    
    For details on failing over, see [Mirror Outage Procedures](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GHA_mirror_set_member_change) in the InterSystems IRIS High Availability Guide.
    
2.  Confirm that the former backup (instance B) is now the primary in the Mirror Monitor ( `Home` > `System Operation` > `Mirror Monitor` .
    
3.  Restart instance A. It will come up as the backup failover member:
    
    *   Use the `iris start` command (or start the instance from the Windows HealthShare cube).
        

### [Mirror Step 10B: Reactivate Analytics](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_1stfailover_reactivate)

Reactivate the Analytics namespace on the new primary mirror member:

1.  On the primary mirror member, open the Management Portal.
    
2.  Select the `HealthShare` tab and then click the `Installer Wizard` link in the banner.
    
3.  Locate your Analytics production in the table of configurations. In the row for your Analytics production:
    
    1.  Click `Activate`.
        
    2.  In the `Activate Configuration` dialog, click `Start`.
        
    3.  Wait for activation to complete.
        
    4.  When you see the `Activation Done` message, click `Close`.
        

### [Mirror Step 10C: Create Databases](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_1stfailover_databases)

On the primary mirror member, create the following additional databases to exactly match those you created earlier:

<table><tr><th>Suggested Name</th><th>Options</th><th>Purpose</th></tr><tr><td><code>HSAACACHE</code></td><td>Create a resource for this database</td><td>Store analytics cache information</td></tr><tr><td><code>HSAAFACT</code></td><td>Create a resource for this database.</td><td>Store the generated fact tables and index global.</td></tr></table>

Configure the databases exactly as you did previously on the [other mirror member](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_databases).

### [Mirror Step 10D: Map Globals](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_1stfailover_map)

Now map globals to the new databases exactly as you did previously on the [other mirror member](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_globals).

1.  #### [Map to HSAACACHE database](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13693)
    
    `^DeepSee.BucketList`
    
    `^DeepSee.Cache.*`
    
    `^DeepSee.JoinIndex`
    
    `^DeepSee.UpdateCounter`
    
    #### [Map to HSAAFACT database](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_C13698)
    
    `^DeepSee.Fact`
    
    `^DeepSee.FactRelation`
    
    `^DeepSee.Index`
    
2.  On the primary mirror member, update any other global, routine, or package mappings in the `HSANALYTICS` namespace or any other namespaces on the instance to exactly match those that you may have created on your other mirror member.
    
3.  Check that any directories or files used for logging are accessible to the current primary mirror member.
    
    > **Important:**
    > 
    > If you are using files for logging, place them in a directory that can be accessed by both mirror members.
    

## [Next Steps in a Health Insight Implementation](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_next_steps)

Now that you have installed Health Insight and configured the Analytics production, the next steps in an implementation are to:

1.  Set up the [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newfeeder).
    
2.  Configure Unified Care Record to [send data to Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_hsconfig).
    
3.  Send the [initial feed of data to Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload).
    
4.  Get acquainted with the Health Insight cubes, dashboards, and pivot tables.
    
    See [Orientation to the Cubes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube) and [Orientation to the Dashboards and Pivot Tables](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_dborient) in the Health Insight User Guide.
    
5.  Start the process of customizing these items cubes, dashboards and pivots.
    
6.  Inspect the `%HSAA_EndUser` role to ensure that it has `Use` permissions for the `%HS_PatientRetrieval` resource. For more information, see the [Known Issues](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20211#HSAARN_20211_knownissues) section of [New Features In Health Insight 2021.1](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20211).
    
7.  If you use [analytics queries](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_qdefs), decide whether to run them as part of the analytics batch or via the [Execute Queries task](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch).
    

### [Considerations for Mirrored Systems](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_considermirror)

If Health Insight is mirrored, review [Planning for Mirroring as You Implement Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_intro_mirroring), which contains important information about implementing a Health Insight deployment that is mirrored. As you implement Health Insight, remember that actions that you perform on the primary failover member that are external to the mirrored databases must be manually replicated on the backup failover member. Examples are detailed in the [linked mirror planning section](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_intro_mirroring).
