# [Health Insight Roles and Resources](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq).

## [Overview of the Security Roles in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_overview)

Health Insight is designed to be used by multiple users in different roles. There are four default security roles. The end user role is designed to support the functions that a care provider or hospital administrator might need. The analyst role is designed to support data analysis. The modeler role is designed to support users who extend the Health Insight model. The operator role is designed to grant the access necessary for a high-level technician responsible for facilitating the transmission of data to Health Insight.

## [The End User Role in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_end)

The end user role includes the privileges needed by someone who is strictly consuming the data displayed by Health Insight. Such an individual might be a care provider or a hospital administrator.

The end user has the fewest privileges of the four security roles. This role can view dashboards, pivot tables, and listings. This role also has access to the Mini Analyzer, which may be available on dashboards. The end user role can access these functions via the [Health Insight Home Page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_intro#HSAAADM_home_page).

> **Note:**
> 
> The end user role has access to the Analyzer, because the Analyzer and the Mini Analyzer are secured via the same resource. However, the Analyzer is not useful to end users because the role is designed for running predefined dashboards, not exploring the data as someone in the analyst or modeler role might do.

## [The Analyst Role in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_analyst)

The analyst role includes the privileges needed by someone who creates the dashboards. This role could also be used by a consumer of data with more sophisticated understanding of InterSystems IRIS Business Intelligence, such as a more technically inclined hospital administrator.

The analyst role includes all of the end user privileges as well as the ability to modify dashboards, create pivot tables, create listings on the listings page, use the model browser, and define analytics query definitions. The analyst role can access these functions via the [Health Insight Home Page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_intro#HSAAADM_home_page).

> **Note:**
> 
> This role is a member of the %Developer role so that analysts can use the SQL pages in the Management Portal.

## [The Modeler Role in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_modeler)

The modeler role includes the privileges needed by someone who prepares the data.

This role includes all of the analyst privileges as well as the ability to use the Business Intelligence Architect, modify cubes, define overrides, and use Studio. Modelers can access many of these functions via the [Health Insight Home Page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_intro#HSAAADM_home_page); however they will need to use the Management Portal for full functionality.

## [The Operator Role in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_operator)

The operator role is separate from the other three roles. It includes the privileges necessary for someone who is responsible for maintaining the transmission of data to Health Insight such as a system administrator or database administrator.

The operator has the privileges to use the Terminal, reset data, build and synchronize cubes, transfer data, use the Platform Information dashboards, and use the configuration pages. Operators can access these functions via the Management Portal.

## [Health Insight Security Roles In Detail](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail)

The four user security roles are based on a larger set of internal security roles. The following sections detail the resource, role, and SQL table permissions of the [Health Insight User Security Roles](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_user) and the [Health Insight Internal Security Roles](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_internal).

Also see the discussion of the %DB_HSAACACHE and %DB_HSAAFACT roles in [Step 3: Create Additional Databases for Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi#HSAAIC_newhi_databases) in the [Configuration Procedure for a New Health Insight Instance](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_newhi).

Note that it is necessary for an administrator with `%All` to activate productions. Productions should be accessed through the HealthShare menu (Management Portal > `HealthShare`).

### [Health Insight User Security Roles](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_user)

#### [%HSAA_EndUser](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_end)

<table><tr><th>Assigned Resources</th><th>Assigned Roles</th></tr><tr><td><p>%HS_PatientRetrieval — RU</p><p>%HS_PatientSearch — U</p></td><td><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_dbbase">%HSAA_Internal_DBBase</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_modelbrowser">%HSAA_Internal_ModelBrowser</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_rundashboard">%HSAA_Internal_RunDashboard</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_runlisting">%HSAA_Internal_RunListing</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_sourcetablesread">%HSAA_Internal_SourceTablesRead</a></p></td></tr></table>

#### [%HSAA_Analyst](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_analyst)

<table><tr><th>Assigned Resources</th><th>Assigned Roles</th></tr><tr><td><p>%DeepSee_Admin — U</p><p>%HSAA_QueryDefinitionRegistry — U</p></td><td><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSA_config_roles#GSA_config_roles_predefined">%Developer</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_end">%HSAA_EndUser</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_dbother">%HSAA_Internal_DBOther</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_modifydashboard">%HSAA_Internal_ModifyDashboard</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_modifylisting">%HSAA_Internal_ModifyListing</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_modqdef">%HSAA_Internal_ModifyQueryDefinitionRegistry</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSA_config_roles#GSA_config_roles_predefined">%SQL</a></p></td></tr></table>

#### [%HSAA_Modeler](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_modeler)

<table><tr><th>Assigned Resources</th><th>Assigned Roles</th></tr><tr><td>%DeepSee_ReportBuilder — U</td><td><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_analyst">%HSAA_Analyst</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_configure">%HSAA_Internal_Configure</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_modifymodel">%HSAA_Internal_ModifyModel</a></p></td></tr></table>

#### [%HSAA_Operator](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_operator)

<table><tr><th>Assigned Resources</th><th>Assigned Roles</th></tr><tr><td><p>%Admin_Operate — U</p><p>%Admin_Task — U</p><p>%HSAA_DataManagement — RW</p><p>%DeepSee_Admin — U</p><p>%HSAA_OperationalDashboard — U</p></td><td><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSA_config_roles#GSA_config_roles_predefined">%Developer</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=EGMG_security#EGMG_security_roles">%EnsRole_Administrator</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_buildcube">%HSAA_Internal_BuildCube</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_configure">%HSAA_Internal_Configure</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_dbother">%HSAA_Internal_DBOther</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_modelbrowser">%HSAA_Internal_ModelBrowser</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_resetdata">%HSAA_Internal_ResetData</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_runtransfer">%HSAA_Internal_RunTransfer</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEAUTHORIZE_ch_roles#HEAUTHORIZE_HS_Administrator">%HS_Administrator</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_consistencycheck">%HSAA_Internal_ConsistencyCheck</a></p></td></tr></table>

### [Health Insight Internal Security Roles](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_internal)

For reference, this section provides detail on the internal security roles on which the preceding roles are based.

#### [%HSAA_Internal_Analyzer](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_analyzer)

Allows the user to work with the Analyzer.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td><p>%DeepSee_AnalyzerEdit — U</p><p>%DeepSee_Portal — U</p><p>%HSAA_DataManagement — U</p><p>%HSAA_Pivots — RW</p></td><td><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_cubedataread">%HSAA_Internal_CubeDataRead</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_sourcetablesread">%HSAA_Internal_SourceTablesRead</a></p></td></tr></table>

#### [%HSAA_Internal_BuildCube](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_buildcube)

Allows the user to build and synchronize cubes.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td><p>%HSAA_BuildCube — U</p><p>%HSAA_CubeClasses — R</p></td><td><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_cubedatawrite">%HSAA_Internal_CubeDataWrite</a></td></tr></table>

#### [%HSAA_Internal_Configure](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_configure)

Allows the user to use the configuration pages.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td>%HSAA_Configure — U</td><td>none</td></tr></table>

#### [%HSAA_Internal_ConsistencyCheck](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_consistencycheck)

Allows the user to run the Consistency Check Tool.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td>%HSAA_ConsistencyCheck — U</td><td>none</td></tr></table>

#### [%HSAA_Internal_CubeDataRead](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_cubedataread)

Provides read access to the cube data [SQL SELECT].

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td>none</td><td>%HS_Internal_DB_HSAACACHE</td></tr></table>

#### [%HSAA_Internal_CubeDataWrite](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_cubedatawrite)

Provides write access to the cube data [SQL SELECT, INSERT, UPDATE, DELETE].

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td>none</td><td><p>%HS_Internal_DB_HSAAFACT</p><p>%HSAA_Internal_CubeDataRead</p></td></tr></table>

#### [%HSAA_Internal_CustomOverride](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_customoverride)

Allows the user to modify cube overrides.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td>%HSAA_CustomizeOverride — U</td><td>none</td></tr></table>

#### [%HSAA_Internal_DBBase](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_dbbase)

Allows the user to access databases that every role needs.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td>none</td><td><p>%HS_Internal_DB_DOCBOOK</p><p>%HS_Internal_DEV_HSAALIB</p><p>%HS_Internal_DB_HSAALIB</p><p>%HS_Internal_DB_HSCUSTOM</p></td></tr></table>

#### [%HSAA_Internal_DBOther](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_dbother)

Allows the user to access other databases that some roles need.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td>none</td><td><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_dbbase">%HSAA_Internal_DBBase</a></p><p>%HS_Internal_DB_HSLIB</p><p>%HS_Internal_DB_SAMPLES</p><p>%HS_Internal_DB_USER</p></td></tr></table>

#### [%HSAA_Internal_EDCreate](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_edcreate)

Deprecated.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td>none</td><td>none</td></tr></table>

#### [%HSAA_Internal_EDLogin](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_edlogin)

Deprecated.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td>none</td><td>none</td></tr></table>

#### [%HSAA_Internal_EDQuery](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_edquery)

Deprecated.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td>none</td><td>none</td></tr></table>

#### [%HSAA_Internal_ModelBrowser](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_modelbrowser)

Allows the user to use the model browser.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td>%HSAA_ModelBrowser — U</td><td>none</td></tr></table>

#### [%HSAA_Internal_ModifyDashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_modifydashboard)

Allows the user to modify dashboards.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td><p>%DeepSee_PortalEdit — U</p><p>%HSAA_Dashboards — RW</p><p>%HSAA_Pivots — RW</p></td><td><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_modifylisting">%HSAA_Internal_ModifyListing</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_rundashboard">%HSAA_Internal_RunDashboard</a></p></td></tr></table>

#### [%HSAA_Internal_ModifyListing](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_modifylisting)

Allows the user to modify listings in cubes.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td><p>%DeepSee_AnalyzerEdit — U</p><p>%HSAA_Listings — RW</p><p>%DeepSee_ListingGroupEdit — U</p><p>%DeepSee_ListingGroupSQL — U</p></td><td>none</td></tr></table>

#### [%HSAA_Internal_ModifyModel](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_modifymodel)

Allows the user to modify the model.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td><p>%DeepSee_Architect — U</p><p>%DeepSee_ArchitectEdit — U</p><p>%DeepSee_Portal — U</p><p>%HSAA_CubeClasses — RW</p></td><td><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_customoverride">%HSAA_Internal_CustomOverride</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_modifylisting">%HSAA_Internal_ModifyListing</a></p></td></tr></table>

#### [%HSAA_Internal_ModifyQueryDefinitionRegistry](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_modqdef)

Allows the user to modify analytics query definitions.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td>%HSAA_QueryDefinitionRegistry — RW</td><td>none</td></tr></table>

#### [%HSAA_Internal_ResetData](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_resetdata)

Allows the user to reset source table data.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td>%HSAA_ResetData — U</td><td><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_sourcetableswrite">%HSAA_Internal_SourceTablesWrite</a></td></tr></table>

#### [%HSAA_Internal_RunDashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_rundashboard)

Allows the user to use dashboards.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td><p>%DeepSee_Analyzer — U</p><p>%DeepSee_Portal — U</p><p>%HSAA_CubeClasses — R</p><p>%HSAA_Dashboards — U</p><p>%HSAA_DataManagement — U</p><p>%HSAA_Pivots — U</p></td><td><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_cubedataread">%HSAA_Internal_CubeDataRead</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_runlisting">%HSAA_Internal_RunListing</a></p></td></tr></table>

#### [%HSAA_Internal_RunListing](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_runlisting)

Allows the user to use listings in cubes.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td><p>%DeepSee_Analyzer — U</p><p>%HSAA_Listings — U</p></td><td>none</td></tr></table>

#### [%HSAA_Internal_RunTransfer](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_runtransfer)

Allows the user to perform the transfer from HealthShare Unified Care Record to source tables.

<table><tr><th>Resources Available to This Role</th><th>Component Roles in This Role</th></tr><tr><td><p>%DB_HSSYS</p><p>%HSAA_RunTransfer — U</p></td><td><a href="https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_sourcetableswrite">%HSAA_Internal_SourceTablesWrite</a></td></tr></table>

#### [%HSAA_Internal_SourceTablesRead](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_sourcetablesread)

Provides read access to the source (or base) tables [SQL SELECT].

#### [%HSAA_Internal_SourceTablesWrite](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_roles#HSAAADM_roles_detail_int_sourcetableswrite)

Provides write access to the source (or base) tables [SQL SELECT, INSERT, UPDATE, DELETE].
