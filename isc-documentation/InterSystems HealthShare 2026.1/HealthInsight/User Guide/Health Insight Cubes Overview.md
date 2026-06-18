# [Orientation to the Health Insight Cubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube)

This chapter introduces the HealthShare Health Insight cubes, which are the data structures that support your analytics queries. Use this information if you are going to create custom pivot tables or simply explore the data.

Cubes are optional in Health Insight, though some areas of the Health Insight documentation set assume the use of cubes. In general, if you are not using cubes, you can skip cube-related instructions that you encounter in the documentation.

This chapter focuses on the core cubes available for direct use in queries. However, Health Insight also includes a distinct set of specialized cubes, which are designed to support disease-specific dashboards. These specialized cubes use a different structure and data pipeline than the core cubes. For information about how to work with them, see the Working with Specialized Cubes documentation.

> **Note:**
> 
> InterSystems maintains a document in Microsoft Excel format that provides detailed information on the source or potential sources of data for each element in the cubes. This document is available for download here.

## [Introduction to Health Insight Terminology](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_intro)

Health Insight represents patient data as a set of related cubes. A cube is a data structure that can be queried via the MDX (multidimensional expressions) query language. To use Health Insight, it is not generally necessary to be familiar with MDX, but it is very useful to understand the contents and organization of the cubes that it uses.

To understand what a cube is, let us consider an example pivot table. A pivot table refers to a cube. The pivot table selects and aggregates data from that cube, making the data available in a format like the following example:

[Image: Pivot table displaying counts of diabetic and non-diabetic patients, as well as the number of outpatient visits for each type]

The `Is Diabetic: No` row provides information on patients who are not diabetic, and the `Is Diabetic: Yes` row provides information on patients who are diabetic. That is, each of these rows represents a specific set of patients.

The `Count` column indicates the count of patients in the given group, and the `Outpatient Visits` column indicates the total number of outpatient visits for those patients.

Using this example as a reference, let us discuss some of the key concepts in a cube definition:

*   Each cube refers to a source table and represents data aggregated across records of that table. While it is not important to be familiar with the source table, it is important to understand what the table represents.
    
    In this example, this cube refers to a source table that contains one record for each patient. This means that the cube represents patients.
    
*   A level is used to group the source records (the core table to which the cube refers). A level has members. Each member, in turn, represents a set of records in that table.
    
    For example, the `Is Diabetic` level has the members `No` and `Yes`. Each of these represents a set of patients.
    
    More formally, levels are contained within dimensions. The primary purpose of a dimension is to serve as a container for one or more levels.
    
*   A measure is a value displayed in the body of the pivot table; it is based on values in the source data. For a given context, a measure aggregates the values for all applicable source records and represents them with a single value.
    
    For example, the `Count` and `Outpatient Visits` columns display measures. In any context, these measures are aggregated across sets of patients. These measures represent aggregate values for patients.
    
*   A related cube is similar to a dimension. It contains a set of dimensions, which in turn contain levels.
    

## [Guided Tour of the Patients Cube](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_exploring_patient)

To better understand the terminology, it is useful to explore a cube directly in the Analyzer. This section provides a brief guided tour.

1.  Click the InterSystems Launcher and then click `Management Portal`.
    
    Enter a username and password when prompted.
    
2.  Switch to the appropriate namespace as follows:
    
    1.  Click `Switch`.
        
    2.  Click your analytics namespace.
        
    3.  Click `OK`.
        
3.  Click `HealthShare`.
    
    > **Note:**
    > 
    > Do not use the options in the `Analytics` menu.
    
4.  Click `HSAA Analyzer`.
    
    The system then displays the Analyzer.
    
    If you see the message `Select a Subject Area to Display`, do the following:
    
    1.  Click the `Select Subject Area` link.
        
    2.  Click `Patients`.
        
    3.  Click `OK`.
        
    
    The left area displays the contents of the Patients cube. The drop-down list controls which kinds of items are shown. Initially this list displays `Dimensions`, and this area displays the dimensions, measures, and other basic items in the cube.
    
    To use the Analyzer, you generally drag and drop items into the upper area on the right, which initially looks like this:
    
    [Image: Screenshot showing the Rows, Columns, Measures, and Filters boxes of the Analyzer]
5.  Drag and drop each item from the `Measures` folder to the `Measures` box on the right. The `Measures` box specifies the measures that are displayed as columns. When you are done, the Analyzer displays a basic pivot table like the following:
    
    [Image: Pivot table displaying the Count, Inpatient Days, ER Visits, and Outpatient Visits measures]
    
    Each of these columns displays one measure. The value shown here is aggregated across all patients in the Patients cube.
    
6.  In the `Dimensions` folder, expand the `Address` dimension. The left area then displays the levels within this dimension. These levels are `State`, `City`, and `ZIP Code`.
    
7.  Drag `State` to the `Rows` box. The Analyzer then subdivides the one row so that the pivot table displays one row for each state. For example (partially shown):
    
    [Image: Partial pivot table displaying Count, Inpatient Days, ER Visits, Outpatient Visits for patients from states listed in alphabe]
8.  In the `Dimensions` folder, expand the `Demographics` dimension. The left area then displays the levels within this dimension. These levels include `Gender`, `Marital Status`, and others.
    
    For the next step, we will use `Gender`, which has relatively few possible variants.
    
9.  Drag and drop `Gender` to the `Columns` box.
    
    The Analyzer then subdivides each column so that the pivot table displays a set of columns for each gender, as in the following example (partially shown):
    
    [Image: The same partial pivot table as in the last graphic, but with a set of Count, Inpatient Days etc. columns for each gender]
    
    Each cell represents a set of patients and displays a specific value for that set of patients. For example, the first five cells in the top row represent female patients in Alaska. Of these, the first cell displays the patient count; the second, the cumulative count of inpatient days; the third, the cumulative count of ER visits; and so on.
    
    Next we will try another way to arrange the same data.
    
10.  In the `Columns` box, click the X in the upper right.
     
     This clears the box.
     
11.  Drag and drop `Gender` on the arrow to the right of `State` in the `Rows` box. The `Rows` box should look like this:
     
     [Image: Rows box with Gender slightly indented under State.]
     
     The pivot table now contains the same numbers as it previously did, but the layout is different:
     
     [Image: Same table as before but with Female and Male rows in each State instead of columns for each gender.]
     
     In this case, the Analyzer has subdivided each row to show results separately for each gender.
     
12.  To see another variation, click the X to the right of `Gender` in the `Rows` box.
     
13.  Drag and drop `City` on the arrow to the right of `State` in the `Rows` box. The Analyzer now divides each row to display separate values for each state. For example:
     
     [Image: Same table as before but with State separated into rows by city instead of gender]
     
     In this case, note that some cells are zero. This means that there were zero inpatient days for the cities of Aleknagik, Cantwell, Clarks Point, or Coffman Cove.
     
     In some cases (not shown here), cells are null. In this case, there is no data for those specific combinations.
     
14.  In the `Rows` box, click the X in the upper right.
     
     This clears the box.
     
15.  In the `Dimensions` folder, expand the `Allergies` folder. This folder is shown in bold italic blue font, which means that `Allergies` is a relationship to another cube. Note that usually (but not always), the name of the relationship is the same as the name of the cube to which the relationship points.
     
     The Analyzer then lists the dimensions in the related cube, as follows:
     
     [Image: List of dimensions in Allergies cube, such as Allergen, Allergy Details, Expiry Date, etc.]
16.  Expand the `Allergen` dimension. The Analyzer then lists the `All Allergen` member, followed by the levels in this dimension. `All Allergens` represents all allergens. The levels include `Allergy Category Code`, `Allergy Category Description`, `Allergy Code`, `Allergy Description`, and others.
     
17.  Drag `Allergy Description` and drop it into the `Rows` box.
     
     The Analyzer then displays one row for each allergy. For example:
     
     [Image: Pivot table showing Count, Inpatient Days, ER and Outpatient Visits in columns, allergies in rows.]
     
     Whenever we use the Patients cube in the Analyzer, any cell in a pivot table represents a set of patients. For example, in this case, each cell in the first row represents the patients whose records indicate an allergy to adhesive tape.
     

## [Core Health Insight Cubes for Direct Use](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_core)

You can directly use any cube for queries, but a core set of the cubes represent the most interesting entities. The Health Insight pivot tables use queries that refer to these cubes. Similarly, when you use the Analyzer and you open a cube, you typically open one of these core cubes. Because the Health Insight cubes are related to each other, the other cubes are available from these cubes via relationships. The core cubes are as follows:

### [Patients](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C10975)

This cube represents the patients. It provides the following measures:

*   Count (patient count)
    
*   Inpatient Days
    
*   ER Visits
    
*   Outpatient Visits
    
*   Avg Unique Outpatient Doctors
    

### [Encounters](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C10987)

This cube represents patient encounters. A patient can have any number of encounters (zero, one, or more). This cube provides the following measures:

*   Number of Encounters
    
*   Total LOS (length of stay)
    
*   Avg LOS
    
*   Number of Discharges
    

### [Diagnoses](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C10995)

This cube represents patient diagnoses. A patient can have any number of diagnoses (zero, one, or more). This cube provides the following measures:

*   Count
    
*   Avg Days Since Diagnosis
    

### [Procedures](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11003)

This cube represents patient procedures. A patient can have any number of procedures (zero, one, or more). This cube provides the following measures:

*   Count
    
*   Avg Days Since Procedure
    

### [Healthcare Facility](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11019)

This cube represents facilities. A facility generally corresponds to a business unit such as a hospital. A facility corresponds to one or more sites. See “[Patients, Facilities, and Sites](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_patients_facilities_sites),” later in this chapter. This cube provides the following measure:

*   Count
    

Note that facilities data comes from four different parts of an SDA, as follows:

*   If the facility data is derived from an `Appointment`, then the facility code is set from the location code since the organization is not parsed from HL7.
    
*   If the facility data is derived from an `Encounter` and the organization of the health care facility is set, then the facility code is set from the organization code. Otherwise, the facility code is set from the healthcare facility code. In HL7 the organization comes from MSH:4, which implies that for HL7 messages, the healthcare facility is always the sending facility that is located in the MSH:4 field.
    
*   If the facility data is derived from an `Order`, then the facility code is set from the entering organization code.
    
*   If the facility data is derived from a `Referral`, then the facility code is set from the referring or referred healthcare facility code.
    

> **Note:**
> 
> The Documents cube includes the Name dimension, which provides the names of the documents. Depending on your data, this dimension could be overly selective. If documents have names such as `Discharge Summary`, then this dimension can be useful. If documents have more specific names such as `Patient X Discharge Summary for <date>`, you might prefer to disable the dimension.

## [Key Relationships Among the Health Insight Cubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_relationships)

This section provides additional details on the relationships among the cubes. It discusses the following topics:

*   [Patients and Current Conditions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_patients_current_condition)
    
*   [Patients and Other Clinical Data](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_patients_clinical)
    
*   [Patients and Care Providers](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_patients_care_providers)
    
*   [Patients, Facilities, and Sites](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_patients_facilities_sites)
    
*   [Patients and Medical Claims](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_medical_claims)
    
*   [Patients and Health Plan Enrollment](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_enrollment)
    

### [Patients and Current Conditions](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_patients_current_condition)

The Patients cube has a one-to-one relationship with the Patient Current Conditions cube.

The Patient Current Conditions cube defines a set of dimensions and levels that describe the current condition of the patients. The dimensions include:

*   Blood Pressure Controlled
    
*   BMI
    
*   Diabetic Defect Score
    
*   Is Diabetic
    
*   30 Day Appointment
    
*   And many others
    

The Patient Current Condition cube is meant for use from within the Patients cube. For example, if you open the Patients cube in the Analyzer and you use the `Patient Current Conditions` > `Is Diabetic` > `Is Diabetic` level for rows, the Analyzer displays a pivot table like the following:

[Image: Pivot table showing two rows, one for No and one for Yes, and a Count column. The counts of No and Yes are shown.]

Note that unlike most other relationships in the Health Insight model, this relationship is one way, and you cannot access the Patients cube from the Patient Current Conditions cube.

### [Patients and Other Clinical Data](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_patients_clinical)

The following diagram shows how the Patients and Encounters cubes are connected to cubes that contain clinical information (other than current conditions, discussed in the [previous section](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_patients_current_condition)):

[Image: Patients has one-to-many relationship with Encounter. Both have one-to-many relationships with many other cubes]

Note that the cubes shown here have additional relationships. For example, the Orders cube is connected to Lab Results, Medications, and Medication Administration.

As this diagram shows, you can access most of the clinical data from either Patient or Encounters.

Notes:

*   To access information about diagnoses, you may need to look in two different locations, depending on your data. For diagnosis data from HL7 messages, use the Diagnoses cube. For diagnosis data from CCDs, use the Problems cube.
    
*   To access information about a medication order, look in Medications > Orders > Order Details or other levels in Medications > Orders.
    

See also the [Model Browser](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_exploring_browser).

### [Patients and Care Providers](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_patients_care_providers)

The following diagram shows how the Patients cube is connected to cubes that contain information on care providers:

[Image: Relationships of Patient, Encounters, Event/Care Provider/Sites, Care Provider/Site, Member/PCP/Sites, Care Provider cubes]

The Encounters cube represents encounters or visits to care providers. This cube includes the Care Providers dimension, which represent care providers for specific encounters.

Additional cubes provide access to care providers in specific contexts. In this model, any interaction with a healthcare provider is an event. The event types are Allergy (that is, diagnosis of an allergy), Diagnosis, Document (creation of a document), Encounter (a visit to a care provider), LabResult (creation of a lab result), MedicationAdministration (administration of a medication), Observation, Order, Problem (a recording of a problem), and Procedure. The Event/Care Provider/Sites cube is an intermediate cube that you can use to associate a patient with a care provider, in any of these contexts. For example, you can use this cube to access the care providers who placed orders.

(The Care Provider/Sites and Member/PCP/Sites cubes are additional intermediate cubes.)

The following list explains some possible ways to use care providers from within the Patients cube:

#### [`Encounters`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11075)

> `Care Providers` > `Admitting Care Provider` level

This level groups patients by the admitting care provider of each of their encounters.

#### [`Encounters`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11078)

> `Care Providers` > `Referring Care Provider` level

This level groups patients by the referring care provider of each of their encounters.

#### [`Member/PCP Sites`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11081)

> `Care Provider/Site` > `Care Provider` > `levels`

These levels group patients by their primary care physicians. A patient can have different primary care physicians over time. To see the patients grouped by the primary care physicians at a specific date, apply a filter that uses one or more members of a level in the `Member/PCP Sites` > `Care Provider/Site` > `End Date` dimension. For example, to select current primary care physicians, use the `No Data` member of the `End Year` level; this selects primary care physicians with no end date.

#### [`Event/Care Provider/Sites`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11084)

> `Care Provider/Sites` > `Care Providers` > `levels`

These levels group patients by the care providers associated with each of their events, which include encounters in addition to other kinds of events. For event types, see the notes before this list.

### [Patients, Facilities, and Sites](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_patients_facilities_sites)

A facility generally corresponds to a business unit such as a hospital. A facility corresponds to one or more sites. The following diagram shows how the Patients cube is connected to cubes that contain information on facilities and sites:

[Image: Relationships: Patient Encounters Event/Care Provider/Sites Care Provider/Site Member/PCP/Sites, HealthCare Facilities, Site]

The following list explains possible ways to use facilities and sites from within the Patients cube:

#### [`Encounters`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11093)

> `Healthcare Facility` > `levels`

These levels enable you to group patients by the facilities associated with their encounters. A facility generally corresponds to a business unit such as a hospital. A facility corresponds to one or more sites.

The following shows some patient measures with the `Facility Name` level used as rows:

[Image: Pivot table displaying the number of ER Visits and Outpatient Visits (columns) for members of the Facility Name level (rows)]

#### [`Encounters`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11098)

> `Site` > `levels`

These levels enable you to group patients by the sites associated with their encounters. A site is a smaller unit within a facility.

The following shows some patient measures with the `Site Name` level used as rows:

#### [`Event/Care Provider/Sites`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11101)

> `Care Provider/Site` > `Site` > `levels`

These levels group patients by the sites at which they saw care providers for all types of events.

#### [`Member/PCP Sites`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11104)

> `Care Provider/Site` > `Sites` > `levels`

These levels group patients by the sites at which they saw their primary care physicians. Because a patient can have different primary care physicians over time, you might need to filter by date, as described in the [previous section](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_patients_care_providers).

### [Patients and Medical Claims](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_medical_claims)

The following diagram shows how the Patients cube is connected to cubes that contain information on medical claims:

[Image: Relationships of Patients, Medical Claims, Event/Care Provider/Sites, Medical Claim Lines cubes]

*   Medical Claims — Contains information about medical claims.
    
*   Medical Claim Lines — Contains details about line items of medical claims.
    

The following list explains possible ways to use medical claims from within the Patients cube:

#### [`Medical Claims`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11116)

> `Claim Processed Date` > `levels`

This level groups patients by the date their claim was processed.

#### [`Medical Claims`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11119)

> `Medicare Indicator` > `levels`

This level groups patients by whether records indicate that they are covered by medicare.

The following list explains possible ways to use medical claim lines from within the Patients cube:

#### [`Medical Claims`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11124)

> `Medical Claim Lines` > `LOINC Code` > `levels`

This level groups patients by LOINC code.

#### [`Medical Claims`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11127)

> `Medical Claim Lines` > `Actual Paid Date` > `levels`

This level groups patients by actual paid date.

The following list explains possible ways to use medical claim lines from within the Medical Claims cube:

#### [`Medical Claim Lines`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11132)

> `Referral Indicator` > `levels`

This level groups patients by whether records indicate that they were referred.

#### [`Medical Claim Lines`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11135)

> `Primary Procedure Code` > `levels`

This level groups patients by primary procedure code.

### [Patients and Health Plan Enrollment](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_enrollment)

The following diagram shows how the Patients cube is connected to cubes that contain information on health plan enrollment:

[Image: One-to-many relationship Patients to Member Enrollment and Enrollment Health Plans to Member Enrollment]

*   Member Enrollment — Contains information about enrollment of patients in health plans
    
*   Enrollment Health Plans — Contains details about individual health plans
    

The following list explains possible ways to use member enrollment from within the Patients cube:

#### [`Member Enrollments`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11147)

> `Coverage Level` > `levels`

This level groups patients by health plan coverage level.

#### [`Member Enrollments`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11150)

> `Primary Insurance` > `levels`

This level groups patients by primary insurance.

The following list explains possible ways to use enrollment health plans from within the Patients cube:

#### [`Member Enrollments`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11155)

> `Enrollment Health Plan` > `Plan Type` > `levels`

This level groups patients by health plan type. Note that a given patient can have multiple health plans and thus would be represented in more than one member of the Plan Type level.

#### [`Member Enrollments`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11158)

> `Enrollment Health Plan` > `Plan Name` > `levels`

This level groups patients by health plan name. Note that a given patient can have multiple health plans and thus would be represented in more than one member of the Plan Name level.

The following list explains possible ways to use enrollment health plans from within the Member Enrollment cube:

#### [`Enrollment Health Plan`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11163)

> `Plan Type` > `Plan Type` > `levels`

This level groups member enrollments by health plan type.

#### [`Enrollment Health Plan`](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_C11166)

> `Plan Name` > `levels`

This level groups member enrollments by health plan name.

## [Exploring the Health Insight Cubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_exploring)

This section introduces tools that you can use to examine the cubes: the [Cube Info dashboard](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_exploring_cubeinfo_db), the [Model Browser](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_exploring_browser), and the [Analyzer](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_exploring_analyzer).

### [Cube Info Dashboard](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_exploring_cubeinfo_db)

Health Insight provides a dashboard (`InterSystems/System/Cube Info`) that displays summary information on the Health Insight cubes. To see this dashboard:

1.  In a [supported browser](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ISP_technologies#ISP_webbrowsers), go to the following URL:
    
    [<baseURL>](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GCGI_intro#GCGI_intro_howitworks_url)`/csp/healthshare/analytics/_DeepSee.UserPortal.Home.zen`
    
    Where `analytics` is the namespace in which you deployed Health Insight. When prompted, enter your HealthShare username and password.
    
2.  Scroll to the bottom and click the arrow in the `Cube Info` dashboard.
    

This dashboard displays two areas. The left table displays a list of all the cubes. By default, they are sorted in descending order by `Fact Count`, which is the number of records in a cube. (Use `Sort By` to sort by cube name instead.) The right area displays a graph of the same information.

### [The Analyzer](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_exploring_analyzer)

With the Analyzer, you can create pivot tables and perform ad hoc analysis. For a brief tour, see the section “[Guided Tour of the Patients Cube](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_exploring_patient),” earlier in this chapter. For details, see [Using the Analyzer](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2ANLY).

### [Model Browser](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube#HSAA_cube_exploring_browser)

The Model Browser enables you to view and navigate the cube relationships, as well as see the measures and levels in a given cube. To access this tool:

*   If HealthShare is built on a later core, access the Model Browser in the Management Portal. In the namespace where Health Insight is running, click `HealthShare`, and then click `Model Browser`.
    
    If this menu option is not listed, see the next bullet item.
    
    > **Note:**
    > 
    > Do not use the Model Browser option in the `Analytics` menu.
    
*   If HealthShare is built on an earlier core, use the sample Model Browser. To access this, use the following URL:
    
    [<baseURL>](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GCGI_intro#GCGI_intro_howitworks_url)`/csp/healthshare/namespace/HSAA.UI.ModelBrowser.cls`
    
    Where `namespace` is the namespace in which Health Insight is running.
    

In either case, once you access the Model Browser, use the drop-down list on the right and select the name of a cube. The Model Browser then displays a diagram like the following:

The yellow circle at the center represents the cube that you selected. The label on the top gives the name of this cube (in this case, `Patients`), followed by the number of related cubes (23) in parentheses. Each of the circles around the central circle represents one cube that is related to the selected cube. For these circles, the label indicates the cube name and the number of related cubes. For example, the circle labeled `Referrals` represents the Referrals cube. There are three cubes that are related to Referrals.

When you select any circle, the diagram changes so that the center shows the newly selected cube, and a green circle shows the previously selected cube. For example:

[Image: Measures and dimensions of Patients cube]

In all cases, the right side of the page displays details for the selected cube. For example, if you select the Patients cube, the right side displays the following:

[Image: generated description: model browser patients contents]

This area displays the contents of the cube in exactly the same way as the left area of the Analyzer. For details, see “[Creating Pivot Tables](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2ANLY_ch_analyzer)” in [Using the Analyzer](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2ANLY).
