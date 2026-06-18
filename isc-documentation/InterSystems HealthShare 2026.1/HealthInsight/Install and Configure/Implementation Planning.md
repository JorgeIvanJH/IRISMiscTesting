# [Key Points for Planning Your Health Insight Implementation](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_planning)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

As with any other enterprise system, it is necessary to start a HealthShare Health Insight implementation with a planning phase. This chapter introduces some key points that you should consider during the planning phase, so that you can avoid rework during the implementation process.

This chapter does not cover all the points that you should consider during the planning phase; other points would include analysis of your business needs and use cases, and analysis of your end users.

Also review [Roadmap to Implementing Unified Care Record](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEMAP).

> **Note:**
> 
> A Health Insight deployment that uses an AADBQ-based data feed is not supported in containers. In order to deploy in containers, you must use a System Index-based feed.

## [Managing and Deploying Changes in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_intro_changemgmt)

When a complex enterprise system requires changes (such as a software upgrade, a recompilation of classes, or configuration changes), the best practice is to make and test changes on a system other than the live system. Specifically, the best practice is to set up a series of environments as follows:

### [Development Environment](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C12997)

Use this environment to develop and test code and all other changes. This environment should not be mirrored, even if the production environment is mirrored.

### [Test Environment](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13000)

Use the test environment to test changes promoted from your development environment. Changes here can be tested in isolation from any configuration differences and other changes that may exist in your development environment. If your live environment is mirrored, then your test environment should be mirrored as well.

### [User Acceptance Test (UAT) Environment](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13003)

Selected end users access this environment to test changes that passed your testing in the test environment. If your live environment is mirrored, then your UAT environment should be mirrored as well.

### [Production/Live Environment](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13006)

This is the live environment that has end users. This environment may be mirrored.

InterSystems recommends that you set up such environments and that you follow a process in which you first make changes and test changes in the development environment and then promote the changes to the next environment and test them there. If you find a problem with a change, return to the development environment and make adjustments there as needed. Or, if the change passes all testing in the test environment, promote the change to the UAT environment, and then, if accepted, promote the change to the live environment.

InterSystems also recommends using source control software to manage the changes, wherever possible.

## [Ensuring Privacy, Security, and Trust in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_securityconsiderations)

Health Insight ingests sensitive patient information for all patients available in Unified Care Record, including personally identifiable information (PII) and protected health information (PHI). By default, Health Insight includes data about all patients in Unified Care Record. HealthShare consent policies apply when specific users attempt to access patient records. This model cannot be applied to Health Insight, which ingests data to build a dataset independent of any particular user. As a result, your organization is responsible for ensuring appropriate safeguards around who can access Health Insight and how its data is used.

To ensure appropriate security and privacy protections, take the following actions:

*   Ensure that all personnel who are provided direct access to the data (for example, via SQL or the Management Portal) in Health Insight are authorized to access all data contained in Health Insight.
    
*   Ensure that the system is only accessed and operated by trusted personnel who are authorized to access the data.
    
*   If you wish to limit the scope of the data in a Health Insight instance to a particular cohort of patients, set up a separate Health Insight datamart. Note that this configuration requires the use of System Index.
    
*   If you need to limit access at a more granular level (for example, based on patient or user-specific consent), build an application layer to enforce access appropriately.
    
*   If you wish to redact certain sensitive data elements when they are stored in Health Insight, use [source data overrides](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_source_data_overrides).
    
*   If you have downstream applications that access data from Health Insight or make copies of the data, ensure that appropriate controls are in place to limit access to authorized users and permitted purposes.
    
*   To help ensure the security of the application, your organization should determine time-out policies for web applications such as those in Health Insight. For more information, and instructions on how to customize your session time-out settings, consult the [Roadmap to Implementing Unified Care Record](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEMAP_ch_deploy).
    
*   Ensure that your class exports from live systems don't [expose protected health information](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEMAP_ch_deploy#HEMAP_class_export).
    

## [Implementing Customizations that Survive Upgrade and Support Mirroring](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_customization_approach)

InterSystems strongly recommends that you use the following approach for customizing Health Insight. This approach ensures that your customizations both support mirroring and survive system upgrades:

### [Do not modify library classes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13040)

Except where specifically noted, do not modify any classes provided by InterSystems. Instead, use the approved customization mechanisms described in the documentation. One exception is that you can modify Health Insight cube classes one of the reasons listed below and described in details in the procedure to [Customize Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube):

*   You may modify the `DependsOn` option when you define a cube override.
    
*   You may disable a cube.
    
*   You may add relationships to your custom cubes.
    

If you make such changes, you must make the changes while in the `HSAALIB` namespace. Make sure that you track your changes, because when you later upgrade Health Insight, you will need to reapply those changes.

### [Place custom code in HSCUSTOM](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13056)

Best practice is to place all custom Health Insight code in the `HSCUSTOM` database.

Add package mappings so that your custom code in `HSCUSTOM` (or other additional custom code databases) can be accessed from the `HSAALIB` and `HSANALYTICS` namespaces.

In order to support SDA extensions, the `HSANALYTICS` namespace is configured with mappings that place the `HS.Local` and `HSAA.Local` packages in `HSCUSTOM`.

Do not use the following reserved package names in your custom code:

*   `HS`
    
*   `HSAA`
    
*   `HS.Local` (use only in `HSCUSTOM`)
    
*   `HSAA.Local` (use only in `HSCUSTOM`)
    

See [Reserved Package Names](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=EGDV_intro#EGDV_reserved_pkg) for additional reserved package names.

### [Create and name custom views appropriately](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13059)

If you create custom views, ensure that you create them in your Analytics namespace (usually `HSANALYTICS`) under a new, user-defined schema that does not conflict with any existing schemas or packages, such as `HSAA` or `HS`. Note that `User` also cannot be used as a new schema name.

### [Name custom cubes appropriately](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13062)

If you define cubes, do not give them logical names that start with `HSAA`. This precaution avoids collisions with any new cubes that InterSystems might provide in a future release.

### [Do not modify provided dashboards and pivots](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13067)

Do not modify the dashboards and pivot tables provided by Health Insight. Instead, create copies of Health Insight dashboards and pivot tables and modify your copies. You may also create your own dashboards and pivot tables from scratch. See [Creating Dashboards](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2DASH) and [Using the Analyzer](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2ANLY).

When you create custom dashboards and pivot tables, you can specify a folder to contain them. This folder controls how these items are displayed in the Analytics User Portal. Do not place custom dashboards or pivot tables in the `InterSystems` folder. This precaution avoids collisions with any dashboards or pivot tables that InterSystems may provide in a future release, and prevents your custom dashboards from being overwritten during an upgrade.

You can make the Health Insight dashboards and pivot tables read-only so that your users cannot modify them.

### [Identical namespaces, configuration, and code must appear in all mirror members](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13070)

If you are using mirroring, ensure that both the primary member and the backup member contain the same code and the same namespaces (with the same global, package, and routine mappings). All configuration settings must also be the same. The configuration procedures in this book describe how to achieve this goal.

## [Planning for Mirroring as You Implement Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_intro_mirroring)

Database mirroring in InterSystems products provides an economical solution for rapid, reliable, robust automatic failover between two HealthShare instances. Mirroring provides an effective, enterprise-wide high-availability solution for your data. Mirroring is supported in both HealthShare Unified Care Record and in Health Insight, as follows:

*   If you elect to mirror Health Insight, you must also mirror the Feeder Gateway and the rest of the Unified Care Record federation.
    
*   If a few hours of downtime for your analytics solution due to a system failure would not interfere with mission-critical work, you may elect to mirror the Unified Care Record federation but choose not to mirror Health Insight.
    

If you plan to use mirroring, it is important to both understand the basic concepts and develop an implementation plan. The implementation documentation includes procedures to either:

*   [Set up mirroring when you initially deploy and configure Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi).
    
*   [Migrate to mirroring after configuring and using the product](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAMIG_mighi).
    

The remainder of this mirror planning section describes:

*   [Mirror Basics](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_customize_mirror_basics)
    
*   [Considerations When Making Configuration Changes in a Mirrored System](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_newhi_Considerations)
    
*   [Checklist for Implementing Health Insight Features When Using Mirroring](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_mirror_summary)
    

### [Mirror Basics](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_customize_mirror_basics)

Keep the following points in mind when working in a mirrored deployment:

#### [Components of a mirror](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13095)

A mirrored deployment consists of a mirror set composed of two mirror members. At any given time, one Health Insight instance acts as the primary failover member, while the other acts as the backup failover member. If the primary experiences a problem, a failover occurs, and the backup takes over and becomes the primary.

#### [Which databases are mirrored](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13104)

Mirroring is primarily for databases that contain data, rather than code:

*   Code library databases such as `HSLIB` and `HSAALIB` are not mirrored.
    
*   An exception is the `HSCUSTOM` database, which should contain your custom code. `HSCUSTOM` is mirrored, ensuring that the same custom code exists on both mirror members.
    
    If any other non-mirrored databases on your instance also contains custom code, you must ensure that the same code exists on both mirror members.
    

#### [Configuration that is external to a mirrored database](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13108)

Mirroring ensures that HealthShare configuration information for mirrored databases is the same on both mirror members. However, some configuration information for an instance exists outside of the mirrored databases, for example, files, tasks, and InterSystems IRIS configuration settings that are stored in the CPF file.

When you initially set up a mirror, or you later make configuration changes in a mirrored deployment, you must manually ensure that configuration information that lives outside of the mirrored databases is the same on each mirror member. Health Share provides mirror-aware APIs that allow you to make certain configuration changes in a mirror-aware manner. See [Considerations When Making Configuration Changes in a Mirrored System](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_newhi_Considerations) below for more details.

#### [Journalling](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13111)

If a database is mirrored, it must also be journaled.

#### [Making changes on the backup](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_C13114)

On the backup mirror member, each mirrored database becomes read-only. A mirrored database on the backup mirror member can receive updates only from the primary member through the mirroring process. You can, however, log in to a backup mirror member as an IRIS password user in order to make configuration changes outside of the mirrored databases. For example, if you manually modify a task or create an SSL/TLS configuration on the primary, you can use the InterSystems IRIS Management Portal to replicate that change on the backup.

These rules have implications for which databases must be journaled, where you place your custom code, and how you make configuration changes. The following sections, as well as the mirroring configuration procedures, provide more detailed information in context.

> **Important:**
> 
> Database mirroring is only part of an enterprise-wide high-availability strategy. Your overall strategy must also consider items external to the databases.

### [Considerations When Making Configuration Changes in a Mirrored System](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_newhi_Considerations)

As you configure Health Insight, you may make certain changes on the primary failover member that must be manually replicated on the backup failover member. Examples include:

*   Custom database resources or other security items.
    
*   Non-standard global, package, and routine mappings.
    
*   Tasks created in the Task Manager.
    
*   File system locations and information stored in files, for example, custom XSLT transformations.
    
*   Any configuration in the `%SYS` namespace, for example, SSL/TLS configurations.
    
*   System-level settings.
    
*   InterSystems IRIS roles created in the management portal.
    
    If instead you create IRIS roles using the mirror-aware [system configuration API](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAPI_reference_sys_config_roles_resources), they will be automatically replicated on other mirror members.
    

Also see the section, [Implementing Customizations that Survive Upgrade and Support Mirroring](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_customization_approach).

### [Checklist for Health Insight Features When Using Mirroring](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_mirror_summary)

The following table lists Health Insight features and notes any particular steps that are required when your deployment is mirrored. The details on these steps appear in the configuration procedure for each feature.

<table><tr><th>Feature</th><th>Necessary Steps</th></tr><tr><td>Feeder Gateway</td><td>Anonymization file must be present on both instances.</td></tr><tr><td>Logs</td><td>If logs are file-based, there should be one shared directory that is accessible to both Health Insight instances.</td></tr><tr><td>Additional Databases for Analytics Globals</td><td>These databases must be journaled. In each HealthShare namespace on the backup member, make sure to configure all mappings to match the mappings that are present on the primary.</td></tr><tr><td>Custom Listings</td><td>Any time you recompile the <code>HSAA</code> classes or reactivate a Health Insight namespace, use the <code>Reapply Custom Listings for All Cubes</code> option in the Management Portal.</td></tr><tr><td><p>Source Data Overrides</p><p>Cube Overrides</p><p>Post-processing Methods</p></td><td>The database that contains the classes that define the methods for this must be created on, or copied to, all servers. Additionally, ensure that mappings in each HealthShare namespace on the backup match the mappings that are present on the primary.</td></tr><tr><td>SDA3 Extensions</td><td>In each HealthShare namespace on the backup, configure all mappings to match the mappings that are present on the primary. Compile any <code>HSAA</code> classes that have SDA extensions on both members.</td></tr><tr><td>Standard Actions</td><td>For the <code>View Patient Record</code> action, double-check the value of the <code>ServiceName</code> setting of <code>AccessGatewayViewer</code> in the Health Insight production.</td></tr><tr><td>Custom actions</td><td>The database that contains the classes that define the actions must be created on, or copied to, all servers. Additionally, ensure that mappings in each HealthShare namespace on the backup match the mappings that are present on the primary.</td></tr><tr><td>Other settings in <code>Customization</code> &gt; <code>Additional Settings</code></td><td>No action is needed.</td></tr><tr><td><p>Disabling Cubes</p><p>Adding Cube Relationships</p></td><td>See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_customize_mirror">Additional Steps When Customizing Health Insight in a Mirrored Environment</a>.</td></tr><tr><td>Persistent Requests</td><td><p>The persistent requests feature is supported in a mirrored environment only if the persistent requests are stored in a database.The Health Insight production must be configured the same way on both the primary and backup members. See <a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_persist">Setting Up and Using Persistent Requests</a> for details.</p><p>The <code>Consume Persistent Request</code> task must be present on both servers. (When you reactivate the Health Insight production as part of setting up mirroring, the reactivation creates this task.)</p></td></tr></table>
