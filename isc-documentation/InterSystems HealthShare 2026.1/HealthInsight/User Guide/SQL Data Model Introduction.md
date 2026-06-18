# [Introduction to the Health Insight SQL Data Model](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel)

In this chapter, the term SQL data model refers to the analytics source tables on which the cubes are built. You can query these tables directly via SQL. These tables are in the `HSAA` schema in your analytics namespace. This chapter introduces the tables and the SQL Explorer.

> **Note:**
> 
> A full entity relationship diagram (ERD) of the Health Insight tables is available for [download here](https://docs.intersystems.com/hs20261/csp/docbook/hshicubeerd/Health%20Insight%20Tables%202026.1.html).

In version 2019.1 of HealthShare Health Insight, programs were renamed to cohorts. However, in some areas, cohorts are still referred to as programs.

## [Understanding Health Insight SQL Tables and Classes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_background)

If you are not familiar with persistent classes, note that InterSystems IRIS for Health provides a kind of class called a persistent class, and that by default, InterSystems IRIS automatically creates a table to store that data for that class. This means that in order to understand the SQL data model, you might find it necessary to examine both the tables and the corresponding class definitions.

In InterSystems IRIS terminology, the terms class and table are sometimes used interchangeably, when persistent classes are under discussion.

For persistent classes, the short class name is used as the table name, and the package name is used as the schema name. For example, the [HSAA.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Patient) class represents patients and stores data in the `Patient` table, which is in the `HSAA` schema. (To be strictly accurate, if the package name includes periods, each period is replaced with an underscore in the corresponding schema name.)

In general, each unique instance of the class is stored as a record in this table. It is highly recommended that you read [Defining and Using Classes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GOBJ) for information on how properties are projected to SQL fields.

> **Tip:**
> 
> Although this page focuses on the analytics source tables (which are in the `HSAA` schema), you can also use SQL to directly query the generated fact and dimension tables (which are in the schemas that have names like `HSAA_AllergyCube`).

## [Browsing the Health Insight SQL Tables](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_browsing)

To look at the tables of the SQL data model, do the following on your analytics instance:

1.  In the Management Portal, click `HealthShare`.
    
2.  Click the name of your analytics instance.
    
    The Portal then displays a menu on the left.
    
3.  Click `SQL Explorer`.
    
    The Portal then displays the SQL Explorer (which can also be accessed in other ways from the Portal).
    
4.  Type `HSAA.*` into `Filter`.
    
    Or click the `HSAA` schema in the `Schema` drop-down list.
    
5.  Click the triangle by the `Tables` folder to expand it.
    
    The Portal then displays a list of the tables in the `HSAA` schema.
    

Now you can do things like the following:

*   Display a list of the fields in a table. To do so, click the triangle by the table name.
    
*   View details of the field definitions. To do so, click the table name, click `Catalog Details` (on the right), and then click `Fields`.
    
*   Execute queries. To execute a query that obtains the top 1000 rows of a table, click the `Execute Query` tab, and then drag and drop the table name from the left area into the input field on that tab. Or type the query that you want to run.
    
    Click `Show History` to see previously run queries and rerun them.
    

For details, see “[Using the Management Portal SQL Interface](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_smp)” in [Using InterSystems SQL](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL).

## [Information Available in Health Insight SQL Tables](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_info)

The following sections describe information available in the Health Insight SQL tables.

### [Tracking Changes with the ChangedObjects Table](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_info_changedobjects)

You can use the [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) table to track changes in the Health Insight source tables. This change tracking is essential for enabling integration with third-party tools and services. It allows external utilities to accurately detect and respond to record-level changes, supporting both efficient data replication and selective re-computation use cases. Below are two examples of how the ChangedObjects table can be used:

*   Change Data Capture (CDC): Exporting new, updated, or deleted data to a downstream data platform.
    
*   Patient Metric Recalculation: Identifying patients whose data has changed so you can recompute metrics only for those affected.
    

#### [ChangedObjects Table Structure](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_B11305)

<table><tr><th>Attribute</th><th>Description</th></tr><tr><td>HSAAType</td><td>The name of the source table where the change occurred, such as <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Encounter">HSAA.Encounter</a></td></tr><tr><td>ObjectId</td><td>The row ID of the object that changed in the table specified by HSAAType</td></tr><tr><td>HSAAID</td><td>The HSAAID in HSAA.Patient that this change is about</td></tr><tr><td>Tag</td><td>The tag, if any, of the changed object. Note that <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Patient">HSAA.Patient</a> objects do not have tags, so the HSAAID is used instead. Additionally, shared objects such as <code>HSAA.CareProviders</code> and <code>HealthcareFacility</code> objects do not have tags. Health Insight-only concepts like <code>CareProviderSite</code> objects also do not have tags.</td></tr><tr><td>Deletion</td><td>Indicates whether the row was deleted (1) or inserted/updated (0)</td></tr></table>

> **Note:**
> 
> Note: The HSAAID field has a foreign key to [HSAA.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Patient).`HSAAID`, but referential integrity is not enforced.

Whenever an object is deleted, inserted, or updated in a source table, Health Insight records a row in the ChangedObjects table. If the object is deleted, the Deletion column is set to 1.

#### [Understanding HSAA.DailyChangedObjects](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_info_changedobjects_daily)

To support safe and efficient processing of change data, Health Insight maintains a lightweight companion table called [HSAA.DailyChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.DailyChangedObjects). This table records the maximum row ID in [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) as of the beginning of each day. This means the recorded value reflects all changes up to, but not during, that day.

[HSAA.DailyChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.DailyChangedObjects) supports two key scenarios:

*   Defining change intervals: By comparing saved maximum row IDs from two dates, you can determine exactly which rows in [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) were inserted or updated during that period.
    
*   Purging old data: The ChangedObjects purge task uses this table to determine how much of [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) can be safely deleted, based on retention policy.
    

##### [DailyChangedObjects Table Structure](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_B11316)

<table><tr><th>Attribute</th><th>Description</th></tr><tr><td>LogDate</td><td>The date associated with a recorded maximum row ID from <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.ChangedObjects">HSAA.ChangedObjects</a>. Used to determine which rows in <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.ChangedObjects">HSAA.ChangedObjects</a> existed as of the beginning of that day.</td></tr><tr><td>RowID</td><td>The maximum row ID in the <a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.ChangedObjects">HSAA.ChangedObjects</a> table at the beginning of the LogDate.</td></tr></table>

#### [Notes for Integration Developers](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_info_changedobjects_integration)

Integration developers should consider the following when working with [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) and Health Insight data:

*   Health Insight tables often contain embedded objects and lists. Integration developers must understand how to handle these structures and map them appropriately to the downstream system. For example, embedded objects may need to be extracted and written to separate tables.
    
*   When replicating changes per patient, it's important to preserve the order of operations. An insert or update followed by a delete is not equivalent to a delete followed by an insert.
    
*   Health Insight periodically purges the [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) table. You must configure the purge frequency so that it never runs more often than the processes that consume and export changes.
    

#### [Capturing Changed Data for Downstream Synchronization](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_info_changedobjects_cdc)

> **Note:**
> 
> Note: The SQL examples in this section assume the use of InterSystems SQL in ObjectScript, for example via dynamic or embedded SQL. If you are integrating via ODBC, JDBC, or another interface, adapt the syntax accordingly.

You can use the [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) table to identify rows that have been added, updated, or deleted since the last export. This section describes how external tools can leverage [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) to extract change data and replicate it to a downstream system in a reliable, incremental fashion. The following procedure provides an outline of how you might track and export only the data that changed since the last successful export or checkpoint by comparing row IDs in [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects). This method is suited for incremental replication to a downstream system and avoids full-table scans.

1.  Maintain a pointer to the last processed row ID for [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) — for example, rowID1, in a durable location that your process can reliably read from and update, such as a metadata table or configuration file in your environment.
    
2.  Periodically, run a query such as the following on [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) to retrieve the highest row ID currently present:
    
    ```sql
    SELECT MAX(ID) INTO :rowID2 FROM HSAA.ChangedObjects
    ```
    
    This gives you a boundary for the current set of changes and allows you to process everything since your last saved row ID.
    
3.  Run a query such as the following on [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects):
    
    ```sql
    SELECT HSAAType, ObjectId, Deletion FROM HSAA.ChangedObjects WHERE ID > :rowID1 AND ID <= :rowID2
    ```
    
    This query retrieves all the objects that have changed since your last checkpoint. Each row contains the source table for the object (HSAAType), the ID of the row (ObjectId), and whether it was deleted (Deletion). These records represent the delta set to apply to the downstream system. You can store these results so that your process can iterate through them for deletion or export in the next step.
    
4.  For each result:
    
    *   If Deletion = 1, delete the object from downstream.
        
    *   Else, retrieve the full object from its HSAAType table and export it downstream.
        
5.  Update your pointer to reflect that the last processed row ID is now rowID2.
    

#### [Selective Recalculation of Patient Metrics](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_info_changedobjects_recalc)

You can use the [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) table to determine which patients have had relevant data changes since a prior point in time. This allows derived metrics, like quality indicators or dashboard summaries, to be recomputed only for affected patients, rather than for an entire cohort. This section describes how to perform re-calculations selectively based on patient-specific changes.

Say you want to generate clinical quality measures and dashboards periodically—for example, to track the maximum HbA1C value in the past 6 months for a cohort of diabetic patients. The first time you calculate the metric, you must compute it for every patient in the cohort, which can be expensive. However, subsequent updates would only need to recompute values for patients whose data has changed in the interim.

The following procedure provides an outline of how you might identify such patients using [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) and [HSAA.DailyChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.DailyChangedObjects), and then recompute metrics only for them. These steps illustrate how to use date-based logic with [HSAA.DailyChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.DailyChangedObjects) to identify relevant patient changes. However, it is more robust to track the last processed row ID than to rely on dates.

1.  Run a query such as the following on the [HSAA.DailyChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.DailyChangedObjects) table to get the row ID associated with the current date. This value reflects the maximum row ID from [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) recorded as of the beginning of the day.
    
    ```sql
    SELECT rowID INTO :rowID1 FROM HSAA.DailyChangedObjects WHERE LogDate = CURRENT_DATE
    ```
    
    The row ID you obtain from this query marks the upper boundary of the change window for this run. You'll use it as the ending point for the time period where you want to detect patient-level changes.
    
2.  Run a query such as the following on the [HSAA.DailyChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.DailyChangedObjects) table to get the row ID from one month ago:
    
    ```sql
    SELECT rowID INTO :rowID2 FROM HSAA.DailyChangedObjects WHERE LogDate = DATE_ADD('mm', -1, CURRENT_DATE)
    ```
    
    This row ID represents the lower boundary of the change window; in other words, it marks the last date from which you'll measure what has changed. Paired with the current date's row ID, it lets you extract all changes between two known points in time.
    
3.  Run a query such as the following on the [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) table:
    
    ```sql
    SELECT HSAAID FROM HSAA.ChangedObjects WHERE HSAAType = 'HSAA.LabResultItem' AND ID > :rowID2 AND ID <= :rowID1
    ```
    
    This identifies patients with new or updated lab result data in the last month.
    
4.  Iterate through each patient HSAAID in the result set. If the patient belongs to your target cohort, such as diabetes, query their HbA1C lab results from the past 6 months and calculate the maximum value. This per-patient metric can then be used to update a dashboard or feed downstream analytics.
    

#### [Configuring ChangedObjects Tracking](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_info_changedobjects_config)

Change tracking via HSAA.ChangedObjects is disabled by default. To enable it:

1.  Go to `HealthShare` > `Additional Settings` > `System Override`
    
2.  Select the `Enable source data tracking` setting
    

This will schedule the [peek and purge tasks](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_info_changedobjects_maint). If the `Enable source data tracking` setting is cleared, the tasks are removed.

#### [Table Maintenance and Retention](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_info_changedobjects_maint)

Health Insight includes two system tasks that support automated cleanup of the HSAA.ChangedObjects table:

*   Peek HSAA.ChangedObjects: A daily task that records the maximum row ID into the [HSAA.DailyChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.DailyChangedObjects) table.
    
*   Purge HSAA.ChangedObjects: A scheduled task that uses entries in [HSAA.DailyChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.DailyChangedObjects) to determine which rows in [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) should be deleted based on a configured retention period – 31 days by default.
    

For example, on June 1, the purge task looks up the row ID associated with May 1 in [HSAA.DailyChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.DailyChangedObjects) and deletes all rows from [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) with an ID less than that row ID. It also deletes all earlier rows from [HSAA.DailyChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.DailyChangedObjects).

You can modify the purge task schedule, but the retention period will adjust accordingly. If the task is run weekly, the retention period becomes 7 days. InterSystems does not recommend configuring the purge task to run more frequently than daily.

If you require snapshot granularity finer than daily, you can implement your own auxiliary ChangedObjects snapshot table and corresponding peeking task.

> **Note:**
> 
> Always ensure that the purge task runs less frequently than any consumer processes that depend on ChangedObjects, to avoid data loss.

#### [Understanding Streamlet Behavior and Embedded Object Deletions](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_info_changedobjects_embedded)

Health Insight ingests SDA streamlets—snippets of XML representing discrete clinical data types like Allergy, Diagnosis, or Observation. Each streamlet is composed of properties that represent a meaningful unit of patient data and is roughly equivalent to a FHIR resource, an HL7v2 segment, or a CDA entry.

When an SDA streamlet is processed, its contents are mapped into one or more Health Insight source tables. Some streamlets embed other objects, which are also represented as rows in separate tables. Because updates to Health Insight source tables occur at the streamlet level, an update to such a streamlet triggers reprocessing for all the embedded objects it owns, even if only a portion of the data has changed.

For example, a `LabOrder` SDA streamlet arriving in Health Insight may embed a list of ten `Result` objects. In this case, `Result` is a property of `LabOrder`. In the Health Insight source tables, each object is represented as a row. Each `LabOrder` object corresponds to a row in the `HSAA.HSAAOrder` table, which contains pointers to each `Result` row in the `HSAA.LabResults` table that represents a `Result` embedded in that `LabOrder`. If an update arrives that updates one of the `Result` objects, all ten of the `Result` rows embedded in the `LabOrder` are removed and possibly replaced in the `HSAA.LabResults` table. In this case, the `ChangedObjects` table would display two rows for each row change — once with the ObjectID for the deletion, and once with a new ObjectID for the possible insertion. Note that shared objects which are referenced by many types of streamlets, such as `Care Provider` and `HealthCareFacility`, are not removed.

The following streamlets cause other objects to be deleted and possibly replaced when updated:

*   `Patient` — Embeds `PatientNumber`.
    
*   `CarePlan` — Contains `Intervention` and `Outcome`. `Goal` and `HealthConcern` have a many-to-many relationship with `CarePlan`. Health Insight deletes or inserts entries in the corresponding intersection tables when a `CarePlan` is processed. In this case, the intersection tables are `CarePlanGoal` and `CarePlanHealthConcern`.
    
*   `Encounter` — Embeds `EncounterGuarantor` and `EncounterHealthPlan`.
    
*   `LabOrder` — Embeds `LabResult` and `LabResultItem`. If microbiology sensitivity processing is enabled via the `Additional Settings` page, all `MicrobiologyDetail` objects for the `LabOrder` are also reprocessed.
    
*   `OtherOrder` — Embeds `OtherResults`.
    
*   `RadOrder` — Embeds `RadResults`.
    
*   `MedicalClaim` — Embeds `MedicalClaimLines`, `MedicalClaimLineHealthPlans`, `Diagnoses`, `EOBSupportingInfo`, `Procedures`, `ProcessNotes`, and `RelatedClaims`.
    
*   `EOBSupportingInfo` — Embeds `Documents`.
    
*   `Medication` — Embeds `MedicationAdministrations`.
    
*   `PharmacyClaim` — Embeds `PharmacyClaimLines`, `EOBSupportingInfo`, `Procedures`, `ProcessNotes`, and `RelatedClaims`.
    
*   `MedicalExplanationOfBenefit` — Embeds `MedicalEOBLines`, `Diagnoses`, `EOBSupportingInfo`, `ProcessNotes`, `Procedures`, and `RelatedClaims`.
    
*   `PharmacyExplanationOfBenefit` — Embeds `EOBSupportingInfo`, `PharmacyEOBLines`, `Procedures`, `ProcessNotes`, and `RelatedClaims`.
    
*   `MemberEnrollment` — Embeds `MemberPolicyAmount`.
    

The following streamlets do not have other objects to delete:

*   `AdvanceDirective`
    
*   `Allergy`
    
*   `Appointment`
    
*   `ClinicalRelationship`
    
*   `DeviceItem`
    
*   `Diagnosis`
    
*   `Document`
    
*   `EventCareProviderSite`
    
*   `FamilyHistory`
    
*   `Goal`
    
*   `HealthConcern`
    
*   `IllnessHistory`
    
*   `Medication`
    
*   `MemberEnrollment`
    
*   `MessageHeader`
    
*   `Observation`
    
*   `ObservationGroup`
    
*   `PhysicalExam`
    
*   `Problem`
    
*   `Procedure`
    
*   `ProgramMembership`
    
*   `QuestionnaireResponse`
    
*   `Referral`
    
*   `SocialHistory`
    
*   `Survey`
    
*   `Vaccination`
    

The following shared objects and Health Insight-created objects may be related to many other objects and are not deleted even if they are embedded in an object that is updated:

*   `CareProvider`
    
*   `CareProviderSite`
    
*   `Device`
    
*   `EnteredAt`
    
*   `HealthCareFacility`
    
*   `HospitalService`
    
*   `Guarantor`
    
*   `MemberPCPSite`
    

By default, the ChangedObjects table is purged each time a Health Insight batch completes. To use the `ChangedObjects` table to track changes before the data is purged, use a post-transfer hook to either do processing or store the changed object info to a custom, non-volatile table that is managed completely outside of Health Insight processing. For more information on post-transfer hooks, see [Specifying Additional Settings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional), or see Specifying Additional Settings for systems with System Index-based feeds. Customers can use an API method in HSAA.API.Config to disable the automatic purging of `ChangedObjects`. Note that the `ChangedObjects` table will increase in size if it is never purged and thus increase the size of your analytics database.

### [Locating Facility Information With the TagFacility Field](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_info_tagfacility)

For many important clinical analyses, attributing data to the correct facility is critical. To make facility attribution easier, each table in Health Insight that is associated with clinical data has an indexed TagFacility field. TagFacility represents the sending facility associated with the data.

In prior versions of Health Insight, the Tag field was often used to determine the sending facility for clinical data. Most Health Insight tables which hold clinical data have a separate Tag field of the form `FacilityCode^Identifier` that can be used to trace clinical data back to the Edge Gateway from which it originated. The `FacilityCode` section of the Tag field represents the sending facility, and knowing which Edge Gateway processes data from the sending facility determines the sending Edge Gateway. Once you know which Edge Gateway sent the data, the `Identifier` section of the Tag field can be used to locate the row in the `HS_SDA3_Streamlet.Abstract` table that holds the clinical data of interest.

Some Tag fields in Health Insight will have a `Suffix` section appended to the end of the Tag, like `FacilityCode^Identifier_Suffix`. The `Suffix` section of the field contains a string (which is sometimes underscore-delimited) that is used to uniquely label and distinguish data of the same data type within the same streamlet. For example, a record in the HSAA.Guarantor table might have a Tag of `FacilityA^1–2_Suscriber`, while another record in the same table might have the Tag `FacilityA^1–2_PayeeOther`. Both these records would originate from the same MedicalClaim streamlet 1–2 and from a facility with a facility code of FacilityA. The `Suffix` field is intended for internal use only and has no impact on TagFacility.

Note that while the `Identifier` portion of the Tag field is usually equivalent to the ID field of the `HS_SDA3_Streamlet.Abstract` table, there are some exceptions. For example, because a `Medication` is a kind of `Order`, a `Medication` Tag such as `CGH^4-6` will be associated with an `Order` with an “`O`” appended to it, for example `CGH^4-6O`.

You can locate the HealthShare Unified Care Record sending facility and easily determine all facilities for data of a particular type by writing queries against the TagFacility field, such as in the following example:

```
SELECT TagFacility FROM HSAA.Diagnosis
WHERE DATEPART('YYYY',DiagnosisTime)=2018
GROUP BY TagFacility
```

The following tables have a TagFacility field as well as an index on TagFacility to optimize searching for data by facility:

<table><tr><td><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.AdvanceDirective">HSAA.AdvanceDirective</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Allergy">HSAA.Allergy</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Appointment">HSAA.Appointment</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.CarePlan">HSAA.CarePlan</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.ClinicalRelationship">HSAA.ClinicalRelationship</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Device">HSAA.Device</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.DeviceItem">HSAA.DeviceItem</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Diagnosis">HSAA.Diagnosis</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Document">HSAA.Document</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Encounter">HSAA.Encounter</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.EncounterGuarantor">HSAA.EncounterGuarantor</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.EncounterHealthPlan">HSAA.EncounterHealthPlan</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.EncounterParticipant">HSAA.EncounterParticipant</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.EOBSupportingInfo">HSAA.EOBSupportingInfo</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.FamilyHistory">HSAA.FamilyHistory</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Goal">HSAA.Goal</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Guarantor">HSAA.Guarantor</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.HealthConcern">HSAA.HealthConcern</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Order">HSAA.Order</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Procedure">HSAA.Procedure</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.IllnessHistory">HSAA.IllnessHistory</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Intervention">HSAA.Intervention</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.LabResult">HSAA.LabResult</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.LabResultItem">HSAA.LabResultItem</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Location">HSAA.Location</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.MedicalClaim">HSAA.MedicalClaim</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.MedicalClaimLine">HSAA.MedicalClaimLine</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.MedicalClaimLineHealthPlan">HSAA.MedicalClaimLineHealthPlan</a></p></td><td><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.MedicalEOBLine">HSAA.MedicalEOBLine</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.MedicalExplanationOfBenefit">HSAA.MedicalExplanationOfBenefit</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Medication">HSAA.Medication</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.MedicationAdministration">HSAA.MedicationAdministration</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.MemberEnrollment">HSAA.MemberEnrollment</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.MemberPolicyAmount">HSAA.MemberPolicyAmount</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.MessageHeader">HSAA.MessageHeader</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Observation">HSAA.Observation</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.ObservationGroup">HSAA.ObservationGroup</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.OtherResult">HSAA.OtherResult</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Outcome">HSAA.Outcome</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.PatientProgram">HSAA.PatientProgram</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.PharmacyClaim">HSAA.PharmacyClaim</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.PharmacyClaimLine">HSAA.PharmacyClaimLine</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.PharmacyExplanationOfBenefit">HSAA.PharmacyExplanationOfBenefit</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.PharmacyEOBLine">HSAA.PharmacyEOBLine</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.PhysicalExam">HSAA.PhysicalExam</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Problem">HSAA.Problem</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.ProcessNote">HSAA.ProcessNote</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Program">HSAA.Program</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Provenance">HSAA.Provenance</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.ProvenanceAgent">HSAA.ProvenanceAgent</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.RadResult">HSAA.RadResult</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Referral">HSAA.Referral</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.RelatedClaim">HSAA.RelatedClaim</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.SocialDeterminant">HSAA.SocialDeterminant</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.SocialHistory">HSAA.SocialHistory</a></p><p><a href="https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&amp;CLASSNAME=HSAA.Vaccination">HSAA.Vaccination</a></p></td></tr></table>

### [Accessing Patient Identifiers With the PatientNumber Table](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_info_patientnum)

Health Insight stores all patient identifiers in a table called [HSAA.PatientNumber](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.PatientNumber). This table is populated as part of the regular processing of data into Health Insight. If you want to access patient identifiers or search Health Insight for a patient with a specific combination of local identifiers, you can query the [HSAA.PatientNumber](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.PatientNumber) table.

Note that the `PatientNumber` table is based on information coming from Edge Gateways and not the Registry. There will not necessarily be a match between the number of identifiers for a patient in the Registry compared to the `PatientNumber` table, as the `PatientNumber` table takes all patient numbers (SSNs, driver licenses, etc.) from each Edge Gateway.

The following SQL query shows an example of how you might use the `PatientNumber` table, where `Information` is the information you need regarding the patient, for example Age.

```
SELECT (Information)
FROM HSAA.Patient
WHERE ID =
(SELECT Patient FROM HSAA.PatientNumber WHERE ISOAssigningAuthority='CTX'AND NumberType='MRN' AND Number=489671)
```

### [Accessing Time Zone Offset Data in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_info_timezone)

Health Insight supports the ingestion of timestamp data with time zone offsets into the source tables. Each timestamp field in the Health Insight source tables has a corresponding UTC timestamp field, which contains the UTC equivalent of the local time with the time zone offset applied. For example, for an input time of `2020-12-18T11:30:00-05:00` (11:30 AM in the New York time zone), Health Insight stores a timestamp field of `2020-12-18 11:30:00` (the local time), as well as a timestamp field of `2020-12-18 16:30:00` (the corresponding UTC time). Many of these timestamp fields are indexed, and all are available for querying from the Health Insight source tables.

Each UTC timestamp field has the same name as its corresponding local timestamp field, with `UTC` appended to the end of the name. For example, the ExpectedAdmitTimeUTC field of [HSAA.Encounter](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Encounter) has a corresponding local timestamp field of ExpectedAdmitTime.

The following fields in the Health Insight source tables do not support time zone offsets and do not have a corresponding UTC timestamp field. Instead, these fields store only the local time:

*   All LastUpdated properties
    
*   The StreamletTime property of [HSAA.Encounter](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Encounter)
    
*   The EnteredOn, BirthDateTime, DeathTime, and CreatedOn properties of [HSAA.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Patient)
    

Note that the StartDateUTC, EndDateUTC, StartDate, and EndDate fields of [HSAA.MemberPCPSite](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MemberPCPSite) are handled differently based on the availability of data from the Unified Care Record. These fields will match what is sent from the Unified Care Record, unless the sent values are null. If the sent values are null, the StartDate and StartDateUTC fields are set to the current time during data ingestion, while the EndDate and EndDateUTC fields are kept empty. When Health Insight saves a newer MemberPCPSite record for a patient (indicating a new PCP for the patient), the StartDate and StartDateUTC fields from that newer record are used to update empty EndDate and EndDateUtC fields from older MemberPCPSite records.

For more information on how time zones are determined in Unified Care Record, see the chapter [Time Zone](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEFLW_ch_timezone) in the book Data Flow and Message Processing in Unified Care Record.

## [Supported Activities in a Health Insight SQL Table](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_sqlmodel#HSAA_sqlmodel_rules_of_engagement)

When you use these tables, note the following guidelines:

*   Do not alter the tables unless you are adding custom indices. Any other alterations are lost when you upgrade.
    
*   If you write queries that join these tables to your own tables, it is your responsibility for correctly identifying the patients and any other join columns so that the join is correct.
    
*   You can create SQL views of the tables.
    
*   You can extract data from the tables to use, for example, in your own data mart, either on the same instance or elsewhere.
    
*   If you create your own custom tables, they must not have relationships that point to the existing Health Insight tables that come with the product.
