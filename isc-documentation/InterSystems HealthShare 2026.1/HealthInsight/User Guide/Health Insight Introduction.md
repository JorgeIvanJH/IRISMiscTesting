# [Introduction to Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_intro)

HealthShare Health Insight is a HealthShare add-on product, developed to provide near real-time, analytical access to comprehensive clinical data available to your organization from HealthShare Unified Care Record. Using Unified Care Record to collect and normalize data, Health Insight maintains a clinically accurate, patient-centric view of the data, combined with high performing InterSystems IRIS Business Intelligence technology for data analysis.

## [Purpose and Features of Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_intro_purpose)

Health Insight is a platform for developing analytics solutions. This platform uses data that is already being collected and normalized via HealthShare and provides an environment, tools, and solutions that you can use to explore this data and to develop analytics solutions for your customers. Health Insight provides the following features:

*   Example dashboards. These are browser-based displays of data, especially aggregated data (sums, averages, and so on).
    
*   An extensive, customizable analytics model (a set of optional InterSystems IRIS Business Intelligence cubes and the underlying relational tables).
    
*   An analysis environment.
    
*   A patient-centered SQL model of clinical data, based on the composite health record stored in Unified Care Record.
    
    Health Insight uses these tables as the basis for its cubes. You can directly query the tables for your own purposes.
    
*   Data transfer services that update data in near real-time.
    
*   The ability to define analytics query definitions, which are reusable definitions that query data in the analytics instance. These query definitions can be used in two ways:
    
    *   In the delivery of clinical messages. Unified Care Record provides the ability to deliver clinical messages, in a variety of formats and delivery methods. The message delivery system is based upon subscriptions and uses filters of various kinds. One kind of filter is an analytics filter, which uses an analytics query definition.
        
    *   In assigning patients to cohorts. Unified Care Record provides the ability to assign patients to cohorts. Such an assignment can be based on an analytics query definition.
        
*   Pre-built solutions like the Consistency Check Tool.
    

For a high-level summary of the available data, see “[Data Available in Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_intro_available_data).”

## [Accessing the Health Insight Home Page](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_home_page)

To access the home page for Health Insight:

1.  Open the Management Portal on the analytics instance.
    
2.  Select `HealthShare`.
    
3.  Select the name of your analytics namespace, typically `ANALYTICS` or `HSANALYTICS`.
    

The menu options on this page are for use by analysts, administrators, and implementers. This book discusses the menu options relevant to analysts. For a full list of the menu options and their uses, see “[Accessing the Health Insight Home Page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page)” in the [Health Insight Deployment and Configuration Guide](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC), or see “Accessing the Health Insight Home Page” for systems with a System Index-based feed.

## [Data Available in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_intro_available_data)

This section describes the data available in Health Insight.

In version 2019.1 of Health Insight, programs were renamed to cohorts. However, in some areas, cohorts are still referred to as programs.

> **Note:**
> 
> A full entity relationship diagram (ERD) of the Health Insight tables is available for [download here](https://docs.intersystems.com/hs20261/csp/docbook/hshicubeerd/Health%20Insight%20Tables%202026.1.html).

> **Note:**
> 
> `Custom Object` and `NVPair` are sent to Health Insight but not stored. To store custom data, use the new SDA Extension/Custom Object storage mechanism. For more information, see [Registering Custom Container Classes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_customcontainer) in the chapter [Customizing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube) in Health Insight Deployment and Configuration Guide, or see Registering Custom Container Classes for systems with System Index-based feeds.

The following list summarizes the data that is available in Health Insight:

### [Patient](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10101)

*   `SDA Object Class`: [HS.SDA3.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Patient)
    
*   `Table`: [HSAA.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Patient)
    
*   `Relevant Cube`: `Patient`
    

### [Advance Directive](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10110)

*   `SDA Object Class`: [HS.SDA3.AdvanceDirective](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.AdvanceDirective)
    
*   `Table`: [HSAA.AdvanceDirective](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.AdvanceDirective)
    
*   `Relevant Cube`: `Advance Directives`
    

### [Alert — Deprecated](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10120)

Same data as in Advance Directives.

*   `SDA Object Class`: `HS.SDA3.AdvanceDirective.Alert`
    
*   `Table`: [HSAA.AdvanceDirective](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.AdvanceDirective)
    
*   `Relevant Cube`: `Advance Directives`
    

### [Allergy](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10129)

*   `SDA Object Class`: [HS.SDA3.Allergy](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Allergy)
    
*   `Table`: [HSAA.Allergy](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Allergy)
    
*   `Relevant Cube`: `Allergies`
    

### [Appointment](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10138)

*   `SDA Object Class`: [HS.SDA3.Appointment](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Appointment)
    
*   `Table`: [HSAA.Appointment](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Appointment)
    
*   `Relevant Cube`: `Appointments`
    

### [BillingProcessNote](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10144)

The MedicalClaimLine, PharmacyClaimLine, MedicalEOBLine, and PharmacyEOBLine tables all have many-to-many relationships with the ProcessNote table. Each MedicalClaimLine, PharmacyClaimLine, MedicalEOBLine, and PharmacyEOBLine can be related to several ProcessNotes, and vice versa. The BillingProcessNote table represents the many-to-many relationships between these tables and the ProcessNote table.

*   `Table`: [HSAA.BillingProcessNote](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.BillingProcessNote)
    

### [Care Plan](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10153)

*   `SDA Object Class`: [HS.SDA3.CarePlan](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.CarePlan)
    
*   `Table`: [HSAA.CarePlan](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.CarePlan)
    
*   `Relevant Cube`: none
    

### [CarePlanGoal](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10159)

This table represents the many-to-many relationship between Care Plan and Goal.

*   `Table`: [HSAA.CarePlanGoal](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.CarePlanGoal)
    

### [CarePlanHealthConcern](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10165)

This table represents the many-to-many relationship between Care Plan and Health Concern.

*   `Table`: [HSAA.CarePlanHealthConcern](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.CarePlanHealthConcern)
    

### [Care Provider](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10174)

*   `SDA Object Class`: [HS.SDA3.CodeTableDetail.CareProvider](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.CodeTableDetail.CareProvider)
    
*   `Table`: [HSAA.CareProvider](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.CareProvider)
    
*   `Relevant Cube`: `Care Providers`
    

### [CareProviderSite](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10180)

This table represents the many-to-many relationship between Care Provider and Site.

*   `Table`: [HSAA.CareProviderSite](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.CareProviderSite)
    

### [Clinical Relationship](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10189)

*   `SDA Object Class`: [HS.SDA3.ClinicalRelationship](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.ClinicalRelationship)
    
*   `Table`: [HSAA.ClinicalRelationship](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ClinicalRelationship)
    
*   `Relevant Cube`: `Clinical Relationships`
    

### [Cohort](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10199)

This data is defined within Unified Care Record, unlike most of the rest of the data listed here.

*   `SDA Object Class`: `HS.SDA3.Program`
    
*   `Table`: [HSAA.Program](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Program)
    
*   `Relevant Cube`: `Cohorts`
    

### [Cohort Membership](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10209)

This data is defined within Unified Care Record, unlike most of the rest of the data listed here.

*   `SDA Object Class`: [HS.SDA3.ProgramMembership](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.ProgramMembership)
    
*   `Table`: [HSAA.Program](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Program), [HSAA.PatientProgram](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.PatientProgram)
    
*   `Relevant Cube`: `Patient/Cohorts`
    

### [Device](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10224)

In this release, Device objects are either:

*   Embedded in the `Devices` property of a Procedure in `HSAA.HSAAProcedure`
    
*   Stored in the [HSAA.Device](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Device) table and referenced by the parent DeviceItem row in [HSAA.DeviceItem](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.DeviceItem)
    

*   `SDA Object Class`: [HS.SDA3.Device](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Device)
    
*   `Table`: [HSAA.Device](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Device)
    
*   `Relevant Cube`: none
    

### [DeviceItem](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10233)

*   `SDA Object Class`: [HS.SDA3.DeviceItem](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.DeviceItem)
    
*   `Table`: [HSAA.DeviceItem](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.DeviceItem)
    
*   `Relevant Cube`: none
    

### [Diagnosis](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10242)

*   `SDA Object Class`: [HS.SDA3.Diagnosis](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Diagnosis)
    
*   `Table`: [HSAA.Diagnosis](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Diagnosis)
    
*   `Relevant Cube`: `Diagnoses`
    

### [Document](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10251)

*   `SDA Object Class`: [HS.SDA3.Document](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Document)
    
*   `Table`: [HSAA.Document](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Document)
    
*   `Relevant Cube`: `Documents`
    

### [DosageStep](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10260)

*   Serial object within `SDA Object Class`: [HS.SDA3.Medication](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Medication)
    
*   `Table`: none
    
*   `Relevant Cube`: none
    

### [Encounter](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10270)

An encounter is an interaction with a healthcare provider.

*   `SDA Object Class`: [HS.SDA3.Encounter](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Encounter)
    
*   `Table`: [HSAA.Encounter](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Encounter)
    
*   `Relevant Cube`: `Encounters`
    

### [Enrollment Health Plans](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10280)

This data originates from X12 834 Member Enrollment messages.

*   `SDA Object Class`: [HS.SDA3.HealthFund](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.HealthFund)
    
*   `Table`: [HSAA.EnrollmentHealthPlan](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.EnrollmentHealthPlan)
    
*   `Relevant Cube`: `Enrollment Health Plans`
    

### [Encounter Participant](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10289)

*   `SDA Object Class`: [HS.SDA3.EncounterParticipant](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.EncounterParticipant)
    
*   `Table`: [HSAA.EncounterParticipant](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.EncounterParticipant)
    
*   `Relevant Cube`: none
    

### [Event](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10299)

An event is any interaction with a healthcare provider. The event types are Allergy (that is, diagnosis of an allergy), Diagnosis, Document (creation of a document), Encounter, MedicationAdministration (administration of a medication), Observation, Order, Problem (a recording of a problem), Procedure, IllnessHistory, MedicalClaim, ServiceMedicalClaimLine (for a service provider), ReferringMedicalClaimLine (for a referring provider), LabResult (creation of Lab Result Item), LabResultNew (creation of Lab Result), Medication (creation of medication), OtherResult (creation of an Other Result), and RadResult (creation of a Radiology Result). A single encounter can generate multiple events.

*   `SDA Object Class`: [HS.SDA3.CodeTableDetail.HealthCareFacility](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.CodeTableDetail.HealthCareFacility)
    
*   `Table`: [HSAA.EventCareProviderSite](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.EventCareProviderSite)
    
*   `Relevant Cube`: `Event/CareProvider/Sites`
    

### [Explanation of Benefits Supporting Information](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10308)

*   `SDA Object Class`: [HS.SDA3.EOBSupportingInfo](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.EOBSupportingInfo)
    
*   `Table`: [HSAA.EOBSupportingInfo](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.EOBSupportingInfo)
    
*   `Relevant Cube`: none
    

### [Family History](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10317)

*   `SDA Object Class`: [HS.SDA3.FamilyHistory](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.FamilyHistory)
    
*   `Table`: [HSAA.FamilyHistory](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.FamilyHistory)
    
*   `Relevant Cube`: `Family Histories`
    

### [Goal](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10326)

*   `SDA Object Class`: [HS.SDA3.Goal](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Goal)
    
*   `Table`: [HSAA.Goal](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Goal)
    
*   `Relevant Cube`: none
    

### [GoalHealthConcern](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10332)

This table represents the many-to-many relationship between Goal and Health Concern.

*   `Table`: [HSAA.GoalHealthConcern](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.GoalHealthConcern)
    

### [GoalIntervention](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10338)

This table represents the many-to-many relationship between Goal and Intervention.

*   `Table`: [HSAA.GoalIntervention](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.GoalIntervention)
    

### [Guarantor](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10360)

Health Insight provides two kinds of guarantor information:

*   Guarantor information from insurance data (specifically X12 post-adjudicated 837 messages and 834 messages). For this guarantor information, the SDA object class, table, and cubes are as follows:
    
    *   `SDA Object Class`: [HS.SDA3.Guarantor](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Guarantor)
        
    *   `Table`: [HSAA.Guarantor](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Guarantor)
        
    *   `Relevant Cube`: `Guarantor`
        
*   Guarantor information from clinical data. For this guarantor information, the SDA object class, table, and cubes are as follows:
    
    *   `SDA Object Class`: [HS.SDA3.Guarantor](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Guarantor)
        
    *   `Table`: [HSAA.EncounterGuarantor](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.EncounterGuarantor)
        
    *   `Relevant Cube`: `Encounter Guarantor`
        

### [Health Concern](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10369)

*   `SDA Object Class`: [HS.SDA3.HealthConcern](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.HealthConcern)
    
*   `Table`: [HSAA.HealthConcern](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.HealthConcern)
    
*   `Relevant Cube`: none
    

### [Healthcare Facility](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10379)

A facility is generally a physical building; for HL7 messages, this information comes from the MSH:4 segment. Also see Sites.

*   `SDA Object Class`: [HS.SDA3.CodeTableDetail.HealthCareFacility](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.CodeTableDetail.HealthCareFacility)
    
*   `Table`: [HSAA.HealthCareFacility](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.HealthCareFacility)
    
*   `Relevant Cube`: `Healthcare Facilities`
    

### [Health Fund](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10388)

*   `SDA Object Class`: [HS.SDA3.HealthFund](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.HealthFund)
    
*   `Table`: [HSAA.EncounterHealthPlan](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.EncounterHealthPlan) or [HSAA.MedicalClaimLineHealthPlan](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MedicalClaimLineHealthPlan) (depending on its parent object in the SDA object)
    
*   `Relevant Cube`: `Health Plans`
    

### [Hospital Service](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10397)

*   `SDA Object Class`: [HS.SDA3.CodeTableDetail.HealthCareFacility](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.CodeTableDetail.HealthCareFacility)
    
*   `Table`: [HSAA.HospitalService](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.HospitalService)
    
*   `Relevant Cube`: none
    

### [Illness History](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10406)

*   `SDA Object Class`: [HS.SDA3.IllnessHistory](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.IllnessHistory)
    
*   `Table`: [HSAA.IllnessHistory](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.IllnessHistory)
    
*   `Relevant Cube`: none
    

### [Intervention](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10415)

*   `SDA Object Class`: [HS.SDA3.Intervention](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Intervention)
    
*   `Table`: [HSAA.Intervention](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Intervention)
    
*   `Relevant Cube`: none
    

### [Lab Order](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10424)

*   `SDA Object Class`: [HS.SDA3.LabOrder](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.LabOrder)
    
*   `Table`: `HSAA.HSAAOrder`
    
*   `Relevant Cube`: `Orders`
    

### [Lab Result Items](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10434)

Lab result items are contained in the Lab Orders streamlet.

*   `SDA Object Class`: [HS.SDA3.LabResultItem](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.LabResultItem)
    
*   `Table`: [HSAA.LabResultItem](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.LabResultItem)
    
*   `Relevant Cube`: `Lab Result Items`
    

### [Lab Results](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10443)

*   `SDA Object Class`: [HS.SDA3.Result](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Result)
    
*   `Table`: [HSAA.LabResult](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.LabResult)
    
*   `Relevant Cube`: `Lab Results`
    

### [Location](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10452)

*   `SDA Object Class`: [HS.SDA3.Location](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Location)
    
*   `Table`: [HSAA.Location](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Location)
    
*   `Relevant Cube`: none
    

### [Medical Claim](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10461)

*   `SDA Object Class`: [HS.SDA3.MedicalClaim](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.MedicalClaim)
    
*   `Table`: [HSAA.MedicalClaim](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MedicalClaim)
    
*   `Relevant Cube`: `Medical Claims`
    

### [Medical Claim Lines](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10471)

This data originates from X12 post-adjudicated 837 messages. Represents distinct line items for MedicalClaims. Each MedicalClaim has a one to many relationship to MedicalClaimLines.

*   `SDA Object Class`: [HS.SDA3.MedicalClaimLine](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.MedicalClaimLine)
    
*   `Table`: [HSAA.MedicalClaimLine](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MedicalClaimLine)
    
*   `Relevant Cube`: `Medical Claim Lines`
    

### [Medical Explanation of Benefit](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10480)

*   `SDA Object Class`: [HS.SDA3.MedicalExplanationOfBenefit](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.MedicalExplanationOfBenefit)
    
*   `Table`: [HSAA.MedicalExplanationOfBenefit](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MedicalExplanationOfBenefit)
    
*   `Relevant Cube`: none
    

### [Medical Explanation of Benefit Line](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10490)

Represents distinct line items for MedicalExplanationofBenefits. Each MedicalExplanationofBenefit has a one to many relationship to MedicalEOBLines.

*   `SDA Object Class`: [HS.SDA3.MedicalEOBLine](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.MedicalEOBLine)
    
*   `Table`: [HSAA.MedicalEOBLine](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MedicalEOBLine)
    
*   `Relevant Cube`: none
    

### [Medication](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10499)

*   `SDA Object Class`: [HS.SDA3.Medication](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Medication)
    
*   `Table`: [HSAA.Medication](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Medication)
    
*   `Relevant Cube`: `Medications`
    

### [Medication Administration](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10508)

*   `SDA Object Class`: [HS.SDA3.Administration](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Administration)
    
*   `Table`: [HSAA.MedicationAdministration](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MedicationAdministration)
    
*   `Relevant Cube`: `Medication Administrations`
    

### [Medication Order](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10517)

*   `SDA Object Class`: [HS.SDA3.Medication](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Medication)
    
*   `Table`: `HSAA.HSAAOrder`
    
*   `Relevant Cube`: `Orders`
    

### [Member Enrollment](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10527)

This data originates from X12 834 Member Enrollment messages.

*   `SDA Object Class`: [HS.SDA3.MemberEnrollment](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.MemberEnrollment)
    
*   `Table`: [HSAA.MemberEnrollment](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MemberEnrollment)
    
*   `Relevant Cube`: `Member Enrollment`
    

### [Member/PCP/Site](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10536)

*   `SDA Object Class`: [HS.SDA3.CodeTableDetail.FamilyDoctor](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.CodeTableDetail.FamilyDoctor)
    
*   `Table`: [HSAA.MemberPCPSite](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MemberPCPSite)
    
*   `Relevant Cube`: `Member/PCP/Sites`
    

### [Member Policy Amount](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10545)

*   `SDA Object Class`: [HS.SDA3.MemberPolicyAmount](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.MemberPolicyAmount)
    
*   `Table`: [HSAA.MemberPolicyAmount](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MemberPolicyAmount)
    
*   `Relevant Cube`: none
    

### [Message Header](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10554)

*   `SDA Object Class`: [HS.SDA3.MessageHeader](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.MessageHeader)
    
*   `Table`: [HSAA.MessageHeader](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MessageHeader)
    
*   `Relevant Cube`: none
    

### [Microbiology Sensitivities](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10565)

If needed, this data is computed from the data in the [HSAA.LabResultItem](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.LabResultItem) table.

*   `SDA Object Class`: not applicable
    
*   `Table`: [HSAA.MicrobiologyDetail](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.MicrobiologyDetail)
    
*   `Relevant Cube`: `Microbiology Lab Results`
    

By default, this data is not computed. Health Insight provides an option to compute it while data is being loaded, as well as an option to compute it after data has been loaded. See “[Specifying Additional Settings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional)” in the Health Insight Deployment and Configuration Guide, or see “Specifying Additional Settings” for systems with System Index-based feeds.

### [Observation](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10574)

*   `SDA Object Class`: [HS.SDA3.Observation](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Observation)
    
*   `Table`: [HSAA.Observation](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Observation)
    
*   `Relevant Cube`: `Observations`
    

### [ObservationGroup](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10584)

*   `SDA Object Class`: [HS.SDA3.ObservationGroup](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.ObservationGroup)
    
*   `Table`: [HSAA.ObservationGroup](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ObservationGroup)
    
*   `Relevant Cube`: none
    

For more information on ObservationGroups, see [Grouping Observations](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEFLW_ch_observation_group) in Data Flow and Message Processing in Unified Care Record.

### [Oral Explanation of Benefit](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10593)

*   `SDA Object Class`: [HS.SDA3.OralExplanationOfBenefit](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.OralExplanationOfBenefit)
    
*   `Table`: [HSAA.OralExplanationOfBenefit](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.OralExplanationOfBenefit)
    
*   `Relevant Cube`: none
    

### [Oral Explanation of Benefit Line](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10603)

Represents distinct line items for OralExplanationOfBenefits. Each OralExplanationOfBenefit has a one-to-many relationship to OralEOBLines.

*   `SDA Object Class`: [HS.SDA3.OralEOBLine](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.OralEOBLine)
    
*   `Table`: [HSAA.OralEOBLine](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.OralEOBLine)
    
*   `Relevant Cube`: none
    

### [Other Order](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10613)

Other orders refers to orders other than lab and radiology orders.

*   `SDA Object Class`: [HS.SDA3.OtherOrder](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.OtherOrder)
    
*   `Table`: `HSAA.HSAAOrder`
    
*   `Relevant Cube`: `Orders`
    

### [Other Results](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10622)

*   `SDA Object Class`: [HS.SDA3.Result](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Result)
    
*   `Table`: [HSAA.OtherResult](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.OtherResult)
    
*   `Relevant Cube`: `Other Results`
    

### [Outcome](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10631)

*   `SDA Object Class`: [HS.SDA3.Outcome](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Outcome)
    
*   `Table`: [HSAA.Outcome](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Outcome)
    
*   `Relevant Cube`: none
    

### [Patient Languages](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10640)

*   Serial object in `SDA Object Class`: [HS.SDA3.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Patient)
    
*   `Table`: none
    
*   `Relevant Cube`: none
    

### [Patient Number](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10649)

*   Serial object in `SDA Object Class`: [HS.SDA3.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Patient)
    
*   `Table`: [HSAA.PatientNumber](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.PatientNumber)
    
*   `Relevant Cube`: none
    

### [Pharmacy Claim](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10658)

*   `SDA Object Class`: [HS.SDA3.PharmacyClaim](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.PharmacyClaim)
    
*   `Table`: [HSAA.PharmacyClaim](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.PharmacyClaim)
    
*   `Relevant Cube`: none
    

### [Pharmacy Claim Line](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10668)

Represents distinct line items for PharmacyClaims. Each PharmacyClaim has a one to many relationship to PharmacyClaimLines.

*   `SDA Object Class`: [HS.SDA3.PharmacyClaimLine](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.PharmacyClaimLine)
    
*   `Table`: [HSAA.PharmacyClaimLine](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.PharmacyClaimLine)
    
*   `Relevant Cube`: none
    

### [Pharmacy Explanation of Benefit](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10677)

*   `SDA Object Class`: [HS.SDA3.PharmacyExplanationOfBenefit](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.PharmacyExplanationOfBenefit)
    
*   `Table`: [HSAA.PharmacyExplanationOfBenefit](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.PharmacyExplanationOfBenefit)
    
*   `Relevant Cube`: none
    

### [Pharmacy Explanation of Benefit Line](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10687)

Represents distinct line items for PharmacyExplanationofBenefits. Each PharmacyExplanationofBenefit has a one to many relationship to PharmacyEOBLines.

*   `SDA Object Class`: [HS.SDA3.PharmacyEOBLine](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.PharmacyEOBLine)
    
*   `Table`: [HSAA.PharmacyEOBLine](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.PharmacyEOBLine)
    
*   `Relevant Cube`: none
    

### [Physical Exam](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10696)

*   `SDA Object Class`: [HS.SDA3.PhysicalExam](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.PhysicalExam)
    
*   `Table`: [HSAA.PhysicalExam](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.PhysicalExam)
    
*   `Relevant Cube`: none
    

### [Problem](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10706)

This data typically comes from CCD documents.

*   `SDA Object Class`: [HS.SDA3.Problem](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Problem)
    
*   `Table`: [HSAA.Problem](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Problem)
    
*   `Relevant Cube`: `Problems`
    

### [Process Note](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10715)

*   `SDA Object Class`: [HS.SDA3.ProcessNote](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.ProcessNote)
    
*   `Table`: [HSAA.ProcessNote](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ProcessNote)
    
*   `Relevant Cube`: none
    

### [Procedure](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10724)

*   `SDA Object Class`: [HS.SDA3.Procedure](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Procedure)
    
*   `Table`: [HSAA.Procedure](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Procedure)
    
*   `Relevant Cube`: `Procedures`
    

### [Provenance](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10733)

*   `SDA Object Class`: [HS.SDA3.Provenance](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Provenance)
    
*   `Table`: [HSAA.Provenance](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Provenance)
    
*   `Relevant Cube`: none
    

### [Provenance Agent](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10742)

*   `SDA Object Class`: [HS.SDA3.ProvenanceAgent](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.ProvenanceAgent)
    
*   `Table`: [HSAA.ProvenanceAgent](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ProvenanceAgent)
    
*   `Relevant Cube`: none
    

### [Questionnaire Response](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10751)

*   `SDA Object Class`: [HS.SDA3.QuestionnaireResponse](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.QuestionnaireResponse)
    
*   `Table`: [HSAA.QuestionnaireResponse](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.QuestionnaireResponse)
    
*   `Relevant Cube`: none
    

### [Radiology Order](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10760)

*   `SDA Object Class`: [HS.SDA3.RadOrder](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.RadOrder)
    
*   `Table`: `HSAA.HSAAOrder`
    
*   `Relevant Cube`: `Orders`
    

### [Rad Results](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10769)

*   `SDA Object Class`: [HS.SDA3.Result](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Result)
    
*   `Table`: [HSAA.RadResult](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.RadResult)
    
*   `Relevant Cube`: `Rad Results`
    

### [Recommendation](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10778)

*   Serial object inside `SDA Object Class`: [HS.SDA3.Encounter](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Encounter)
    
*   `Table`: none
    
*   `Relevant Cube`: none
    

### [Referral](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10787)

*   `SDA Object Class`: [HS.SDA3.Referral](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Referral)
    
*   `Table`: [HSAA.Referral](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Referral)
    
*   `Relevant Cube`: `Referrals`
    

### [Related Claim](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10796)

*   `SDA Object Class`: [HS.SDA3.RelatedClaim](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.RelatedClaim)
    
*   `Table`: [HSAA.RelatedClaim](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.RelatedClaim)
    
*   `Relevant Cube`: none
    

### [Site](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10806)

A site is a location or department within a facility, although for a small facility, the site might be the same as the facility. Also see Healthcare Facility.

*   `SDA Object Class`: none
    
*   `Table`: [HSAA.Site](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Site)
    
*   `Relevant Cube`: `Sites`
    

### [Social Determinant of Health](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10815)

*   `SDA Object Class`: [HS.SDA3.SocialDeterminant](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.SocialDeterminant)
    
*   `Table`: [HSAA.SocialDeterminant](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.SocialDeterminant)
    
*   `Relevant Cube`: none
    

### [Social History](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10824)

*   `SDA Object Class`: [HS.SDA3.SocialHistory](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.SocialHistory)
    
*   `Table`: [HSAA.SocialHistory](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.SocialHistory)
    
*   `Relevant Cube`: `Social Histories`
    

### [Support Contact](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10833)

*   Serial object in `SDA Object Class`: [HS.SDA3.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Patient)
    
*   `Table`: none
    
*   `Relevant Cube`: none
    

### [Survey](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10842)

*   `SDA Object Class`: [HS.SDA3.Survey](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Survey)
    
*   `Table`: HSAA.Survey
    
*   `Relevant Cube`: none
    

### [Vaccination](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_C10852)

A vaccination is a special kind of medication.

*   `SDA Object Class`: [HS.SDA3.Vaccination](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Vaccination)
    
*   `Table`: [HSAA.Vaccination](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Vaccination)
    
*   `Relevant Cube`: `Vaccinations`
    

### [Table Relationships](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_intro_available_data_tables)

The following diagram describes the relationships between the Orders, Results, Medications, and Vaccinations tables:

Orders has a one-to-many relationship with Lab Results, Rad Results, Other Results, Medications, and Lab Result Items. Lab Results has a one-to-many relationship with Lab Result Items, and Medications has one with Vaccinations.
