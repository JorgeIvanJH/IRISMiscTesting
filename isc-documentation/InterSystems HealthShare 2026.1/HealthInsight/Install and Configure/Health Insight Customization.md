# [Customizing Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_extendcube)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

This chapter describes how to customize HealthShare Health Insight. It discusses the following topics related to customizing the behavior of the Health Insight source tables, as well as some general customization options:

*   [How to specify which data are sent to and/or stored in Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_data)
    
*   [How to add custom indices](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_indices)
    
*   [How to register custom container classes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_customcontainer)
    
*   [How to define source data overrides](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_source_data_overrides)
    
*   [How to specify additional settings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional)
    
*   [How to handle conflicting code descriptions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_code_descriptions)
    
*   [How to run analytics queries outside of batch processing](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch)
    
*   [Additional steps when customizing Health Insight in a mirrored environment](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_customize_mirror)
    

It also discusses the following topics related to customizing the behavior of the Health Insight cubes:

*   [How to define custom listings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_listings)
    
*   [How to define cube overrides](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_overrides)
    
*   [How to remove cube overrides](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_cubeoverride_removing)
    
*   [How to define custom cubes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_cubes)
    
*   [How to disable cubes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_cube_disable)
    
*   [How to use cube inheritance](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_inherit)
    
*   [How to customize codes used in the Patients Current Conditions cube](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_calccode)
    
*   [Example calculated measures and calculated members](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_calc_member)
    

For information on the cubes, see “[Orientation to the Cubes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_cube)” in the [Health Insight User Guide](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA).

Before using this chapter, be sure to read “[Ensuring That Your Customizations Support Mirroring and Easier Upgrades](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_customization_approach),” earlier in this book.

> **Note:**
> 
> InterSystems supports one additional form of customization, not documented here specifically. You can add a relationship to a Health Insight cube, to connect it to a custom cube. InterSystems does not support adding new relationships between the standard cubes. For information on defining relationships, see “[Defining Cube-Cube Relationships](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODADV_rel)” in [Advanced Modeling for InterSystems IRIS Business Intelligence](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODADV). Because this change modifies a Health Insight class, you must make the changes while in the `HSAALIB` namespace. Also, when you later upgrade Health Insight, you will need to reapply your changes.
> 
> If you choose to define [a one-way relationship](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODADV_rel#D2MODADV_multicube_rel_defining_one_way) or a [two-way relationship](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODADV_rel#D2MODADV_multicube_rel_defining_two_way) between a Health Insight cube and a custom cube, [make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write) prior to beginning each procedure. After completing the procedures for defining a one-way or two-way relationship, return HSAALIB to read-only by following the procedure to [make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write), but select the `Mount Read-Only` option instead of clearing it.

## [Specifying Which Data Are Sent to and/or Stored in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_data)

Health Insight provides a mechanism that enables you to specify which streamlets are sent from HealthShare Unified Care Record to Health Insight and what streamlet types to process into Health Insight once the data have been received from Unified Care Record. The granularity of both sending and processing is at the streamlet level.

You can specify the data you want to send to and/or store in Health Insight using the `Streamlets to Send` page and the `Streamlets to Process` page, respectively.

> **Caution:**
> 
> Check for relationships on any streamlets that you plan to filter. Breaking relationships can lead to inconsistent data or ingestion errors. For example, if you filter out Observation streamlets, you must also filter out ObservationGroup streamlets.

### [Specifying Which Streamlets to Send](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_data_send)

The following example demonstrates how to exclude the Diagnosis streamlet from being sent from Unified Care Record to Health Insight:

1.  Navigate to the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page).
    
2.  Select `Customization` > `Streamlets to Send`.
    
3.  Select `Diagnosis` from the `Sent Streamlets` column.
    
4.  Click the `Add >>` button. This transfers `Diagnosis` from the `Sent Streamlets` column to the `Unsent Streamlets` column.
    
5.  Click `Save Customization`.
    

If you want to revert this change and send the Diagnosis streamlet to Health Insight, select `Diagnosis` in the `Unsent Streamlets` column, click `<< Remove`, and then click `Save Customization`.

### [Specifying Which Streamlets to Process](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_data_process)

The following example demonstrates how to exclude the Diagnosis streamlet from being processed into Health Insight:

1.  Navigate to the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page).
    
2.  Select `Customization` > `Streamlets to Process`.
    
3.  Select `Diagnosis` from the `Processed Streamlets` column.
    
4.  Click the `Add >>` button. This transfers `Diagnosis` from the `Processed Streamlets` column to the `Unprocessed Streamlets` column.
    
5.  Click `Save Customization`.
    

If you want to revert this change and process the Diagnosis streamlet into Health Insight, select `Diagnosis` in the `Unprocessed Streamlets` column, click `<< Remove`, and then click `Save Customization`.

## [Adding Custom Indexes to Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_indices)

Health Insight provides a mechanism that enables you to add indices to `HSAA` source tables. To do so:

1.  [Edit](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides) the corresponding `Indices` class for the source table that you want to add an index to. For example, to add an index to [HSAA.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Patient), edit the `HSAA.Indices.Patient` class.
    
    > **Caution:**
    > 
    > Do not change the inheritance of these classes.
    
2.  In the corresponding `Indices` class, add an index such as the following:
    
    ```
    Index ZTestIndex on Occupation;
    ```
    
    Save the class. Note that custom indices should have names starting with “Z”.
    
3.  [Make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write).
    
4.  Compile the [HSAA.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Patient) class.
    
5.  Return HSAALIB to read-only by following the procedure to [make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write), but select the `Mount Read-Only` option instead of clearing it.
    
6.  Use the [BUILD INDEX](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSOD_indexes#GSOD_indexes_build_comm) SQL command to build the index. For example:
    
    ```
    BUILD INDEX FOR TABLE HSAA.Patient INDEX ZTestIndex
    ```
    

Indices will persist through upgrades as long as you follow these procedures.

Be sure to choose your indexing strategy wisely - too many indices will slow down the ingestion process. Tables that you run frequent queries against with fields that are used for filtering (i.e. those that appear in the WHERE clause of SQL statements) or that you need to search for specific criteria on are generally the best candidates for indices.

For more information on creating indices, see [Defining and Building Indices](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=GSOD_indexes).

> **Note:**
> 
> Note that the above steps for adding custom indices do not apply to certain properties of `HSAA.X` classes, where X is the name of any of the `HSAA` source table classes.
> 
> For example, if a property (such as a relationship) in an `HSAA.X` class is not visible from the corresponding `HSAA.Indices.X` class, attempting to add a custom index to that property in the `HSAA.Indices.X` class will result in a compilation error.
> 
> As a more specific example, attempting to add an index to [HSAA.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Patient)'s `OrderRel` relationship in the `HSAA.Indices.Patient` class will result in an error when compiling the `HSAA.Indices.Patient` class. This is because `HSAA.Indices.Patient` is a parent class of [HSAA.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Patient) and because the `OrderRel` relationship is defined in [HSAA.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Patient). As a result, the `OrderRel` relationship isn't visible from `HSAA.Indices.Patient`.

## [Registering Custom Container Classes in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_customcontainer)

Health Insight includes a customization mechanism for SDA: custom container classes; see “[Customizing the SDA by Creating a Custom SDA Container](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HXSDA_ch_sda_custom#HXSDA_sda_custom_container)” in the chapter “[Customizing the SDA](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HXSDA_ch_sda_custom)” in The InterSystems Clinical Data Model: SDA.

> **Note:**
> 
> Note that you can also use the following procedure to register custom serial classes that are added as properties to an [SDA extension class](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_extend_healthinsight).

If you register your custom container classes for use by Health Insight, then custom data that you add via this mechanism is stored in the Health Insight database. To register a custom container class:

1.  Navigate to the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page).
    
2.  Select `Customization` > `Custom Container Class Registration`.
    
3.  In the `SDA Source Class` field, enter the name of the class in the `HS.SDA3` package that represents the desired SDA object.
    
    For a list of the data available in Health Insight, see “[Data Available in Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_intro_available_data)” in the [Health Insight User Guide](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_intro_available_data).
    
4.  In the `Health Insight Class Name` field, enter the full name of the associated custom container class.
    
    To register multiple classes at one time, select `New Class Registration` to create additional blank fields.
    
5.  When you are finished registering classes, select `Save Registered Classes`. To clear all classes you have registered (but not yet saved), select `Reload Registered Classes`.
    

Or register your custom classes by using class methods in [HSAA.TransferSDA3.Utils](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Utils). See the class reference documentation for details.

Health Insight transfers data to your custom container classes as part of the data feed process, but does not modify any cube definitions to use this new data.

## [Defining Source Data Overrides in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_source_data_overrides)

During the Unified Care Record implementation process, you typically normalize much of the data coming into Unified Care Record. In certain cases, it may still be necessary to normalize the data that Unified Care Record sends to Health Insight. Health Insight enables you to use custom logic to override certain code/description mappings as well as to perform validation on certain clinical results.

A source data override will only work if Health Insight is able to successfully save the incoming `HSAA.*` object, because Health Insight needs to do processing on the object before calling source data override methods. For example, if incoming data causes a `MAXLEN` error, you can't use source data overrides to truncate the long string. The properties must be truncated on the Feeder Gateway using anonymization transforms.

(Note that Health Insight can also record any changes made to the source data during the data feed process, and you can define custom processing to run after the data is loaded. See the section “[Specifying Additional Settings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional).”)

For each SDA type that want to customize, complete the following steps:

1.  Create a class to contain the class method or class methods that you will define. For information on where to place this class, see “[Ensuring That Your Customizations Support Mirroring and Easier Upgrades](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_customization_approach).”
    
2.  In the class from step 1, create and compile a class method with the following signature:
    
    ```
    ClassMethodName(source As HS.SDA3.type, target As HSAA.type) As %Status
    ```
    
    Where `HS.SDA3.type` is the full name of a class in the `HS.SDA3` package, and `HSAA.type` is the full name of a class in the `HSAA` package.
    
    Your method should accept as input an instance of the `HS.SDA3.type` and should set (as output) an instance of `HSAA.type`, modified in the way that meets your needs. The method should return a status value.
    
    > **Warning:**
    > 
    > Be sure to fully test your custom methods as they can potentially corrupt your patient data. Any error reporting or logging must be defined within your custom code.
    
3.  Navigate to the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page).
    
4.  Select `Customization` > `Source Data Overrides`.
    
5.  From the left drop-down list, select the name of the class to which you want to add an override.
    
6.  On the right, enter a value in the form `classname:methodname` where `classname` is the fully qualified name of the class, and `methodname` is the name of the method to execute. For example:
    
    ```
    MyRhio.SourceDataOverrides:ObservationOverride
    ```
    
    After making this change, select `Save Overrides`.
    
7.  [Reset](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkload_resetting) Health Insight and then reload all the data. Note that if you only want the override to affect new data coming into Health Insight, it is not necessary to reset Health Insight.
    

> **Warning:**
> 
> Use these options carefully, because they affect the data as it is loaded into the Health Insight tables.

> **Note:**
> 
> While you can remove MPIIDs when using source data overrides on Patient objects, HSAAIDs must always be retained to ensure ingestion works properly.

### [Example](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_source_data_overrides_example)

The following example method performs a source data override. Specifically, this method removes blood pressure observations that fall outside of a specified range and replaces them with the string `"invalid"`.

```objectscript
 ClassMethod ObservationOverride(
                 source As HS.SDA.Observation,
                 target As HSAA.Observation
                                 ) As %Status
 {
    Try {
        Set sc = $$$OK

        // Only do something if this is a BP observation
        // (diastolic or systolic)
        Set code = source.ObservationCode.Code
        If ((code="8462-4")||(code="8480-6")) {
            Set value = source.ObservationValue
            If (code="8462-4") {
                // Diastolic
                // Anything between 0 and 500 is valid
                If (($IsValidNum(value) = 0) || ((value < 0) || (value > 500))) {
                    Set newValue = "invalid"
                    Set target.ObservationValue = newValue
                }
            }
            Else {
                // Systolic
                // Anything between 0 and 500 is valid
                If (($IsValidNum(value) = 0) || ((value < 0) || (value > 500))) {
                    Set newValue = "invalid"
                    Set target.ObservationValue = newValue
                }
            }
        }
    }
    Catch(ex) {
        #dim ex As %Exception.AbstractException
        Set sc = ex.AsStatus()
    }
    Return sc
 }
```

> **Note:**
> 
> This example is provided for demonstration purposes only.

## [Specifying Additional Settings in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional)

To perform additional customizations:

1.  Navigate to the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page).
    
2.  Select `Customization` > `Additional Settings`.
    
3.  Specify options as needed; see the following list.
    
4.  Click `Save Configuration`.
    

> **Warning:**
> 
> Be sure to fully test your custom methods as they can potentially corrupt your patient data. Any error reporting or logging must be defined within your custom code.

### [Patient Actions](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_C14347)

See “[Defining Custom Actions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_actions#HSAAIC_actions_defining),” later in this book.

### [Post-transfer processing method](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_C14352)

Use this option to specify code that will run right after Health Insight has finished writing to the source tables (but before it synchronizes the cubes). For an overview of the processing, see “[Phase 3: Health Insight Production Processes the Data in the Staging Table](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_phase3)” in the first chapter. Also see “[Key Processing Steps in the Health Insight Production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_details#HSAAREF_details_insightprod),” at the end of this book.

Enter a value in the form `classname:methodname` where `classname` is the fully qualified name of the class, and `methodname` is the name of the method to execute. The method should return a status value.

For information on the recommended location of the containing class, see “[Ensuring That Your Customizations Support Mirroring and Easier Upgrades](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_customization_approach),” earlier in this book.

### [Post-synchronization processing method](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_C14358)

Use this option to specify code that will run right after Health Insight has finished synchronizing the cubes (but before it has finished processing the batch). For an overview of the processing, see “[Phase 3: Health Insight Production Processes the Data in the Staging Table](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_phase3)” in the first chapter. Also see “[Key Processing Steps in the Health Insight Production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_details#HSAAREF_details_insightprod),” at the end of this book.

Enter a value in the form `classname:methodname` where `classname` is the fully qualified name of the class, and `methodname` is the name of the method to execute. The method should return a status value.

Depending on what else your method does, it may be necessary for your method to rebuild relevant cubes. See “[API for Monitoring and Managing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api).”

For information on the recommended location of the containing class, see “[Ensuring That Your Customizations Support Mirroring and Easier Upgrades](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_customization_approach),” earlier in this book.

### [Post-batch processing method](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_C14364)

Use this option to specify code that will run right after Health Insight has finished processing a batch. For an overview of the processing, see “[Phase 3: Health Insight Production Processes the Data in the Staging Table](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_phase3)” in the first chapter. Also see “[Key Processing Steps in the Health Insight Production](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_details#HSAAREF_details_insightprod),” at the end of this book.

Enter a value in the form `classname:methodname` where `classname` is the fully qualified name of the class, and `methodname` is the name of the method to execute. The method should return a status value.

Depending on what else your method does, it may be necessary for your method to rebuild relevant cubes. See “[API for Monitoring and Managing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api).”

For information on the recommended location of the containing class, see “[Ensuring That Your Customizations Support Mirroring and Easier Upgrades](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_customization_approach),” earlier in this book.

### [Do not transfer EventCareProviderSite info](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_C14367)

To disable the transfer of event/care provider/site information, select this checkbox. This option is provided because there can be a very large number of event/care provider/site combinations, one for each interaction with a care provider at each site. These records are used by the Event/Care Provider/Sites cube. If you do not need this cube, you can save space by suppressing the creation of the records that it uses.

### [Do not transfer Document stream info](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_C14370)

To disable the transfer of document streams, select this checkbox.

### [Calculate readmissions periodically in a background task](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_C14382)

Health Insight optionally tracks whether an encounter is a potential readmission for a previous encounter. The `ReadmitForEncounter` field in the `HSAA.Encounter` table is a relationship between an encounter and the encounter for which it is a readmission. This field contains the ID of the encounter for which the current encounter is a readmission, and indicates whether readmission encounters are found for the current encounter. If this field is `NULL`, the Encounter cube will set the readmission level flag to “`No`”. Otherwise, the level is set to “`Yes`”.

If you select the `Calculate readmissions periodically in a background task` checkbox, Health Insight will create two tasks:

*   Calculate Readmissions Using ChangedObjects: Runs daily at 3 AM by default and processes readmissions for patients with encounters that have been changed via streamlet ingestion or deleted since the last run. This task uses either the default method or a custom method to calculate readmissions across all inpatient encounters for each patient that requires an update. Writes output to [`<durable-install-dir>`](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSDEPLOY_directories#HSDEPLOY_directories_durable-install-dir)`/mgr/HSANALYTICS/CalculateReadmissionsUsingChangedObjects.txt`.
    
    This task relies on the `Enable source data tracking` option to identify the patients that require updates. If `Enable source data tracking` is not selected, this task will produce an error.
    
*   Calculate All Readmissions: Runs on demand and computes readmissions for all patients using either the default method or a custom method. This task is intended for use when enabling source data tracking for the first time or when calculating readmissions for existing data. Writes output to [`<durable-install-dir>`](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSDEPLOY_directories#HSDEPLOY_directories_durable-install-dir)`/mgr/HSANALYTICS/CalculateAllReadmissions.txt`.
    

Clearing this checkbox removes both tasks.

The Calculate Readmissions Using ChangedObjects task applies only to new or modified data that has been tracked since `Enable source data tracking` was turned on. For existing data already in the system before source tracking was enabled—or before this task was activated—use the Calculate All Readmissions task to recompute readmissions for all patients.

### [Custom calculation for readmissions](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_C14394)

The default method that looks for readmissions, `HSAA.Readmission.DefaultCalculation.CalculateOnePatient()`, searches for all inpatient encounters for a given patient and updates the`ReadmitForEncounter` field of each encounter to point to the patient’s previous inpatient encounter if:

*   The encounter starts more than one day after the end of the previous encounter.
    
*   The encounter starts within 30 days after the end of the previous encounter.
    

The Calculate Readmissions Using ChangedObjects and Calculate All Readmissions tasks call `CalculateOnePatient()` by default on the patients they are calculating readmissions for.

You can also apply your own logic for determining whether to consider one encounter a potential readmission of a previous encounter. To do so, enter a custom method to call as an override in the `Custom calculation for readmissions` field. The custom method must have the following signature:

```
ClassMethod ClassMethodName(HSAAID As %String) As %Status
```

Where `ClassMethodName` is the name of your custom method. For example queries and logic, see the class comments of `HSAA.Readmission.DefaultCalculation.CalculateOnePatient()`.

### [Enable processing of microbiology sensitivities](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_C14397)

Select this checkbox to enable Health Insight to process microbiology sensitivities while loading data. If you enable this processing, Health Insight links lab results through the `MicrobiologyDetail` table and cube. You must test any data you plan to send and ensure that all microbiology data contains an organism, because it is possible for warning messages about incomplete data to overwhelm the log table. Note that Health Insight also provides a method you can use process microbiology sensitivities for the data that has already been loaded; see “[Performing a Bulk Load](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkload_howto),” earlier in this book.

### [Enable source data tracking](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_C14401)

Select this checkbox to enable Health Insight to track changes to source data. When enabled, Health Insight writes change information to the [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) table.

Purging of [HSAA.ChangedObjects](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.ChangedObjects) is handled by the Purge ChangedObjects task.

### [Enable logging of cube and dashboard access and activity to the ATNA repository](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_C14404)

Select this checkbox to enable auditing for cube and dashboard access and activity. Activity is logged to the HealthShare ATNA repository, which is usually located on the HealthShare Registry. Once auditing is enabled in your analytics namespace, all analytics activities (both on HSAA cubes and custom cubes) will be audited. For example, access to Analyzer, dashboards, pivot tables, MDX queries, and detail listings are audited and logged to the HealthShare ATNA Repository. If auditing is not enabled, no analytics activities will be audited in this namespace.

### [Transmit batch size](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_C14407)

Use this option to specify the transmit batch size of the Feeder Gateway. This setting specifies the maximum number of patients per batch that the Feeder Gateway retrieves from the Registry for processing into Health Insight. The default value of `-1` indicates that all available patients in the transmit queue should be retrieved. As an example, you might temporarily lower the maximum batch size when resending a group of [high-priority patients](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_intro_data_feed_phase2_priority) so that those patients are processed by themselves during the next batch.

## [Handling Conflicting Code Descriptions in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_code_descriptions)

In Health Insight, each code, such as an ICD-9 code, is paired with a description. However, when your data comes from multiple sources, there can be conflicting code-description pairs. Health Insight provides ways to manage conflicting gender code-description pairs, see “[Source Data Overrides](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_source_data_overrides)” earlier in this chapter. For handling other scenarios, use the techniques listed below.

### [Using the Default Behavior](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_code_descriptions_default_behavior)

By default, Health Insight will choose from the source tables the first description paired with a given code as the description to be displayed within Health Insight. For each code, a code-description pair is “first” when it is within the row with the lowest SQL index relative to other pairs with the same code.

[Image: Source table showing two rows. Both have DosageForm_Code of C. Top row has DosageForm_Description Caplet and bottom has Cap]

In the example above, the Dosage Form Code “C” has two conflicting descriptions, “Caplet” and “Cap”. Because “Caplet” is the first description, Health Insight will only display “Caplet” as the description of DosageForm_Code “C”.

If the default behavior is not ideal for your implementation, use one of the two methods to manually change the code description listed in the following sections.

### [Using SQL to Modify the Data within Source Tables](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_code_descriptions_sql_modify)

To ensure that only one description per code exists within the underlying data, you can modify the source table data with an SQL statement. There are multiple points at which you can modify the source table data. Unless you have a reason to do otherwise, it is better to modify the data as early as you can. Standardizing the codes within Unified Care Record is the ideal solution. See “[Managing Coded Fields in Unified Care Record](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HETRM_ch_coded_fields#HETRM_coded_fields_options)”, within [Translating Terminology in Unified Care Record](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HETRM) for more details. If you only want Health Insight to have modified source table data, use a [custom method](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional) on the analytics server after all the data have been stored in the source tables.

### [Using a Custom Override on the Cube](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_code_descriptions_custom_override)

You can display a user defined code description while maintaining unaltered source tables. You can achieve this by using [cube overrides](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_overrides). In this scenario, drilling down on the data within Health Insight will display the original description values as they appear in the source tables.

## [Configuring Analytics Query Execution Outside of Batch Processing](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch)

By default, analytics queries run during Health Insight batch processing. However, you can configure analytics queries of SQL type to run outside of batch processing using the Execute Queries task. This provides greater flexibility and avoids interruptions to data ingestion.

If you enable this feature, analytics queries are run via the schedulable Execute Queries task and supporting business hosts in the analytics production, rather than as part of the batch.

As an example, you could use this feature if you have many analytics queries for notifications or DDMs and running them during batch processing significantly extends batch duration and interrupts data ingestion.

> **Note:**
> 
> This feature has been validated with analytics queries of SQL type. Other types of analytics queries may also be compatible with the Execute Queries task; however, these have not yet been formally validated. Customers using additional query types are advised to test thoroughly in non-production environments before relying on this feature in production workflows.

### [Setting Up the Execute Queries Task](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch_setup)

To enable query execution outside batch processing, open the Terminal and run the following method in your analytics namespace:

```
set sc=##class(HSAA.API.Config).SetExecuteQueries(0,1) write !,sc
```

In the output, a final 1 confirms the operation succeeded. This command creates and schedules the Execute Queries task, which by default runs once daily starting at midnight.

When the Execute Queries task runs, the following steps occur:

*   The task starts the ExecuteQueries business service in the analytics production.
    
*   The service sends analytics query execution requests to the ExecuteQueries business process.
    
*   The process forwards those requests to [HSAA.Query.Process](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Query.Process), which executes the queries.
    

### [Configuring Analytics Query Execution Frequency](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch_freq)

When configuring the frequency of analytics query execution outside of batch processing, there are two key settings to understand:

*   The [Execute Queries task schedule](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch_freq_task) controls how often that process is triggered.
    
*   [MaxNumQuery](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch_freq_maxnum) controls how many queries run each time the process is triggered.
    

#### [Adjusting Task Frequency](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch_freq_task)

You can modify the Execute Queries task schedule in the Task Manager. When adjusting the schedule, consider:

*   How often your analytics queries expire
    
*   The schedule of the Run Expired Queries task on your Registry instance, which sends expired analytics query requests to Health Insight
    
*   How quickly those requests are acted on depends on how often the Execute Queries task is scheduled
    

#### [Setting Up MaxNumQuery](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch_freq_maxnum)

The `MaxNumQuery` in the `Settings` of [HSAA.TransferSDA3.Process.ExecuteQueries](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.TransferSDA3.Process.ExecuteQueries) controls how many expired analytics queries are executed each time the process is triggered — either via batch processing or the Execute Queries task.

This value can be adjusted to match the expected volume and expiration rate of analytics queries in your environment. The default value is 5, meaning that only the first 5 expired queries are executed. Set to –1 to execute all expired analytics queries at once.

### [Verifying the Configuration](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch_verify)

To check whether analytics queries are configured to run inside or outside Health Insight batch processing, run the following command in your analytics namespace:

```
d ##class(HSAA.API.Config).CheckExecuteQueries(.inBatch,1) write !, inBatch
```

An output of 0 indicates that queries will run outside Health Insight batch processing. A 1 indicates that queries will run within batch processing.

### [Reverting to Analytics Query Execution During Batch Processing](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_querybatch_revert)

If you later decide to revert to running analytics queries within Health Insight batch processing, run the following command in your analytics namespace:

```
set sc=##class(HSAA.API.Config).SetExecuteQueries(1,1) write !,s
```

## [Additional Steps When Customizing Health Insight in a Mirrored Environment](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_customize_mirror)

This section describes additional steps that apply if the Health Insight instance is mirrored.

### [When Additional Steps Are Needed](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_customize_mirror_when)

The additional steps in this section are needed when you implement any Health Insight customizations that affect InterSystems code. The relevant customizations are as follows:

*   Editing Health Insight cube classes to modify the DependsOn option
    
*   Adding cube relationships to Health Insight cubes
    
*   When adding custom indices
    

### [Promoting Customizations from the Development Environment](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_implement_sda_mirrored)

For background, see “[Managing and Deploying Changes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_intro_changemgmt),” earlier in this book.

To promote your customizations from the development environment (which is not a mirrored environment) to a mirrored environment:

1.  Make the changes in your development environment. Once you are ready to promote your code to a mirrored environment, determine which classes have been modified in the `HSAALIB` namespace. InterSystems recommends using source control software to manage these changes.
    
2.  [Make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write) on the backup mirror member, server B.
    
3.  Return HSAALIB to read-only on server B by following the procedure to [make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write), but select the `Mount Read-Only` option instead of clearing it.
    
4.  Import the modified classes to the backup mirror member, server B, and then compile them.
    
5.  Return HSAALIB to read-only on server B by following the procedure to [make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write), but select the `Mount Read-Only` option instead of clearing it.
    
6.  Perform a controlled failover from the primary server (server A) to the backup server (server B). Now server B is the primary server and server A is the backup server.
    
7.  [Make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write) on server A.
    
8.  Import the modified classes to server A, and then compile them.
    
9.  Return HSAALIB to read-only on server A by following the procedure to [make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write), but select the `Mount Read-Only` option instead of clearing it.
    

The goal is for both mirror members to contain the same code that is in the development environment. The steps above are needed when you implement any Health Insight customizations that affect InterSystems code.

## [Defining Custom Listings in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_listings)

The Custom Listings page enables you to define new listings for the Health Insight cubes, disable listings, and reapply changes after recompiling cubes (see the note at the end of this section).

To define a new listing:

1.  Navigate to the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page).
    
2.  Select `Cube Management` > `Listings`.
    
3.  Select `Select a Cube`, select a cube name, and then select `OK`.
    
4.  Select `New`.
    
5.  Enter the following details:
    
    *   `Listing name` — Name of the listing.
        
    *   `Listing Type` — Select either `SQL` (to provide custom SQL) or `FieldList` (to provide just a list of fields).
        
    *   `Listing Definition` — If you selected `SQL`, enter a complete SQL SELECT statement. If you selected `FieldList`, enter a comma-separated list of fields in the source table used by the given cube.
        
    *   `Order By listing fields` — Optionally specify how to order the listing. Enter a comma-separated list of fields in the source table used by the given cube. This option applies only if you selected `FieldList`.
        
    
    If you are providing custom SQL (that is, if you selected `SQL`), see “[Defining an SQL Custom Listing](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODEL_ch_listing#D2MODEL_listing_custom)” in the chapter “[Defining Listings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODEL_ch_listing)” in [Defining Models for InterSystems IRIS Business Intelligence](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODEL).
    

You can also use this page to disable listings provided by InterSystems. To do so, select a listing from the `Listings` drop-down, select `Disabled`, and then select `Save`.

> **Important:**
> 
> If you make changes on this page and later recompile cubes, your listing changes are no longer available. In this case, select `Reapply Custom Listings For All Cubes`. This option forces the listing customizations to take effect.

## [Defining Cube Overrides in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_overrides)

Health Insight provides an override mechanism that enables you to redefine the Health Insight cubes without modifying the internals of classes provided by InterSystems. This mechanism enables you, for example, to hide or disable parts where you have no data. Note that Health Insight uses the same mechanism internally, as you will see in the [first subsection](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_cubedefs).

This mechanism enables you to modify existing structures but does not enable you to add new items. (To add new items, use cube inheritance, which is discussed [later](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_inherit) in this chapter.)

To define an override for a given cube:

1.  Identify the parts of the cube definition that you want to override, in XML format. Specifically, you must identify the XML elements and attributes that you want to override.
    
    The [first subsection](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_cubedefs) describes how to identify the parts of the Health Insight cube definitions.
    
2.  Create a class to contain the class method or class methods that you will define. For information on where to place this class, see “[Ensuring That Your Customizations Support Mirroring and Easier Upgrades](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_customization_approach).”
    
3.  Write a class method that applies your override information. This method must write values to the `^DeepSee.Overrides` global. These values describe how to override the parts of the XML structure.
    
    The following example overrides parts of the Allergies cube:
    
    ```
    set ^DeepSee.Overrides("HSAAALLERGY", "NULLREPLACEMENT")="My Null Replacement"
    set ^DeepSee.Overrides("HSAAALLERGY", "DIMENSIONS", "ALLERGEN", "DISPLAYNAME") = "My Allergens"
    ```
    
    The first line redefines the `nullReplacement` attribute of the cube to be `My Null Replacement`. The second line redefines the `displayName` attribute of the Allergens dimension to be `My Allergens`
    
    The [second subsection](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_overrides_method) provides the details for the override method.
    
4.  Navigate to the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page).
    
5.  Select `Cube Management` > `Cube Overrides`.
    
6.  For `Cube to Override`, select the name of the cube you want to override.
    
7.  For `Cube override class and method`, enter the name of the override class and method (as defined in step two). Use the following format:
    
    ```
    classname:classmethodname
    ```
    
    Where `classname` is the full package and class name, and `classmethodname` is the name of the class method.
    
    You can override additional cubes by selecting `New Override`.
    
8.  When you are finished, select `Save Overrides`.
    
9.  In each applicable Health Insight cube class, edit the [DependsOn](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=ROBJ_class_dependson) list to include the name of the class that contains the utility method that defines overrides for this cube. For example:
    
    ```
    Class HSAA.AllergyCube Extends %DeepSee.CubeDefinition
    [ DependsOn = (HSAA.Allergy, HSAA.AllergyOverrides, HSAA.PatientCube, MyOverrides.Utils) ]
    ```
    
    Because this change modifies a Health Insight class, you must make the changes while in the `HSAALIB` namespace. Also, when you later upgrade Health Insight, you will need to reapply your changes.
    
10.  [Make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write).
     
11.  Recompile the Health Insight cube class.
     
     When you do so, the system first compiles the classes on which it depends and then compiles the cube class. During this process, Health Insight applies its own internal overrides and then applies your overrides. The compiler issues a series of messages indicating these steps.
     
12.  Return HSAALIB to read-only by following the procedure to [make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write), but select the `Mount Read-Only` option instead of clearing it.
     
13.  If you created any custom listings or made any other changes on the Health Insight Custom Listing page, return to that page and select `Reapply Custom Listings for All Cubes`. See “[Defining Custom Listings](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_listings),” earlier in this chapter.
     
14.  Rebuild the Health Insight cubes.
     
     See “[API for Monitoring and Managing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api).”
     

> **Important:**
> 
> If you want to disable one or more cubes, see “[Disabling Cubes with Relationships](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_cube_disable),” later in this chapter. Disabling a cube is a special case that requires different handling.

### [Understanding the Health Insight Cube Definitions](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_cubedefs)

If you apply cube overrides (or if you use cube inheritance, discussed later in this chapter), it is necessary to understand the XML format of the Health Insight cube definitions.

As background, see the appendix “[Reference Information for Cube Classes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODEL_appx_cubeclass)” in [Defining Models for InterSystems IRIS Business Intelligence](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODEL). This appendix describes the XML format of cube definitions. It is important to be moderately familiar with the `<cube>`, `<measure>`, `<dimension>`, and other elements.

To find the XML definition of a Health Insight cube, use the following process:

1.  Connect to the instance with [your IDE](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides) and go to the `HSANALYTICS` namespace.
    
2.  Find the class that contains the Health Insight cube definition.
    
    Each Health Insight cube is in a separate class, in the package `HSAA`. (Ignore the subpackages, which mostly contain generated classes.) The class name is based on the cube name that you see in the Analyzer, with `Cube` at the end. For example, the Allergies cube is defined in the class [HSAA.AllergyCube](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.AllergyCube).
    
3.  Examine the `Cube` XData block in this class.
    
    This XData block contains one `<cube>` element, which in turn contains the cube definition.
    
4.  Make a note of the value of the `name` attribute of the `<cube>`. In this example, `name` is `HSAAAllergy`. This attribute defines the logical name of the cube, as used in all the internal structures.
    
5.  Make a note of the value of the `inheritsFrom` attribute (`AllergyDetails` in this case). This attribute specifies the logical name of an abstract cube defined elsewhere.
    
    The abstract cube contains the basic definition of this cube. The inheritance mechanism works as follows:
    
    1.  When this cube (for example, `HSAAAllergy`) is compiled, the compiler copies the definitions from the abstract cube (`AllergyDetails`) into the internal structures used by this cube (`HSAAAllergy`).
        
    2.  The compiler merges in the rest of the XML definition in this cube class (`HSAAAllergy`), overriding any definitions from the abstract cube if there are conflicts.
        
    3.  The compiler applies cube overrides, as defined in the `%OnApplyOverrides()` method in this class.
        
        This code does not generally change the logical names of any parts of the cube, so you do not need to see it to determine the logical names that you want to override. But it can be useful to examine this code in other scenarios.
        
6.  Find the class that contains the corresponding abstract cube definition.
    
    Each abstract cube is in a separate class, in the package `Analytics`. The class name is based on the cube name. For example, the `AllergyDetails` cube is defined in the class [Analytics.AllergyDetails](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=Analytics.AllergyDetails).
    
7.  Examine the `Cube` XData block in this class. Use the appendix “[Reference Information for Cube Classes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODEL_appx_cubeclass)” in [Defining Models for InterSystems IRIS Business Intelligence](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODEL) as a reference to understanding this structure.
    
    In particular, when you want to override something, make a note of the following:
    
    *   The kind of XML element to override (`<measure>`, `<level>`, or other element).
        
    *   The `name` attribute of that item. This XML attribute specifies the logical name of the item, which you need when you define overrides.
        
    *   The logical names of all parent items. For example, a `<level>` is contained in a `<hierarchy>`, which is contained in a `<dimension>`.
        
    
    You will also use the logical name of the Health Insight cube, which you determined in a previous step.
    
8.  Use the appendix “[Reference Information for Cube Classes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODEL_appx_cubeclass)” in [Defining Models for InterSystems IRIS Business Intelligence](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODEL) to determine the names of the XML attribute or attributes that you want to override for the given XML element.
    

### [Defining a Class Method to Apply Cube Overrides](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_overrides_method)

To create a class method to apply cube overrides, create a class method with the following signature:

```
ClassMethod MethodName(cubeName As %String) As %Status
```

Where `MethodName` is the name of the method, and `cubeName` is the logical name of a Health Insight cube. For a given value of `cubeName`, the method can define overrides for that cube. To define overrides, the method must set nodes of the `^DeepSee.Overrides` global, as shown in the example [previously given](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_overrides).

> **Warning:**
> 
> Be sure to fully test your custom methods as they can potentially corrupt your patient data. Any error reporting or logging must be defined within your custom code.

The following table describes how to override the XML attributes of each XML element of a `<cube>` definition. In all cases, set the node equal to the new value for the given attribute. See the example in the previous section.

<table><tr><th>To override an attribute of ...</th><th>Set the node...</th></tr><tr><td><code>&lt;cube&gt;</code></td><td><p><code>^DeepSee.Overrides(CUBE</code>, <code>ATTR)</code></p><ul><li><p><code>CUBE</code> is the logical name of a Health Insight cube.</p></li><li><p><code>ATTR</code> is the XML attribute to override.</p></li></ul><p>All subscripts must be in uppercase (even if the logical names are not defined in uppercase). Also all subscripts must be in quotes.</p></td></tr><tr><td><code>&lt;measure&gt;</code></td><td><p><code>^DeepSee.Overrides(CUBE</code>, <code>"MEASURES"</code>, <code>MEAS, ATTR)</code></p><ul><li><p><code>MEAS</code> is the logical name of the measure to override.</p></li><li><p><code>ATTR</code> is the XML attribute of that measure to override.</p></li></ul></td></tr><tr><td><code>&lt;dimension&gt;</code></td><td><p><code>^DeepSee.Overrides(CUBE</code>, <code>"DIMENSIONS"</code>, <code>DIM</code>, <code>ATTR)</code></p><ul><li><p><code>DIM</code> is the logical name of the dimension to override.</p></li><li><p><code>ATTR</code> is the XML attribute of that dimension to override.</p></li></ul></td></tr><tr><td><code>&lt;hierarchy&gt;</code></td><td><p><code>^DeepSee.Overrides(CUBE</code>, <code>"DIMENSIONS"</code>, <code>DIM</code>, <code>"HIERARCHIES"</code>, <code>HIER</code>, <code>ATTR)</code></p><ul><li><p><code>HIER</code> is the logical name of the hierarchy to override.</p></li><li><p><code>ATTR</code> is the XML attribute of that hierarchy to override.</p></li></ul></td></tr><tr><td><code>&lt;level&gt;</code></td><td><p><code>^DeepSee.Overrides(CUBE</code>, <code>"DIMENSIONS"</code>, <code>DIM</code>, <code>"HIERARCHIES"</code>, <code>HIER</code>, <code>"LEVELS"</code>, <code>LEV</code>, <code>ATTR)</code></p><ul><li><p><code>LEV</code> is the logical name of the level to override</p></li><li><p><code>ATTR</code> is the XML attribute of that level to override.</p></li></ul></td></tr><tr><td><code>&lt;property&gt;</code></td><td><p><code>^DeepSee.Overrides(CUBE</code>, <code>"DIMENSIONS"</code>, <code>DIM</code>, <code>"HIERARCHIES"</code>, <code>HIER</code>, <code>"LEVELS"</code>, <code>LEV</code>, <code>"PROPERTIES"</code>, <code>PROP</code>, <code>ATTR)</code></p><ul><li><p><code>PROP</code> is the logical name of the property to override</p></li><li><p><code>ATTR</code> is the XML attribute of that property to override.</p></li></ul></td></tr><tr><td><code>&lt;member&gt;</code></td><td><p><code>^DeepSee.Overrides(CUBE</code>, <code>"DIMENSIONS"</code>, <code>DIM</code>, <code>"HIERARCHIES"</code>, <code>HIER, "LEVELS"</code>, <code>LEV</code>, <code>"MEMBERS"</code>, <code>MEM</code>, <code>ATTR)</code></p><ul><li><p><code>MEM</code> is the logical name of the member to override</p></li><li><p><code>ATTR</code> is the XML attribute of that member to override.</p></li></ul></td></tr><tr><td><code>&lt;calculatedMember&gt;</code></td><td><p><code>^DeepSee.Overrides(CUBE</code>, <code>"CALCULATEDMEMBERS"</code>, <code>CALCMEM</code>, <code>ATTR)</code></p><ul><li><p><code>CALCMEM</code> is the logical name of the calculated member to override</p></li><li><p><code>ATTR</code> is the XML attribute of that calculated member to override.</p></li></ul></td></tr><tr><td><code>&lt;listing&gt;</code></td><td><p><code>^DeepSee.Overrides(CUBE</code>, <code>"LISTINGS"</code>, <code>LISTING</code>, <code>ATTR)</code></p><ul><li><p><code>LISTING</code> is the logical name of the listing to override</p></li><li><p><code>ATTR</code> is the XML attribute of that listing to override.</p></li></ul></td></tr><tr><td><code>&lt;listingField&gt;</code></td><td><p><code>^DeepSee.Overrides(CUBE</code>, <code>"LISTINGFIELDS"</code>, <code>FIELD</code>, <code>ATTR)</code></p><ul><li><p><code>FIELD</code> is the logical name of the listing field to override</p></li><li><p><code>ATTR</code> is the XML attribute of that listing field to override.</p></li></ul></td></tr><tr><td><code>&lt;namedSet&gt;</code></td><td><p><code>^DeepSee.Overrides(CUBE</code>, <code>"NAMEDSETS"</code>, <code>SET</code>, <code>ATTR)</code></p><ul><li><p><code>SET</code> is the logical name of the named set to override</p></li><li><p><code>ATTR</code> is the XML attribute of that named set to override.</p></li></ul></td></tr></table>

> **Important:**
> 
> All subscripts must be in uppercase (even if the logical names are not defined in uppercase). Also all subscripts must be in quotes.

### [Disabling a Cube via Override](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_overrides_disable)

You can disable a cube via cube override. To do so, include code such as the following in your override method:

```objectscript
 set ^DeepSee.Overrides("HSAAALLERGY", DISABLED) = 1
```

This example disables the Allergy cube.

## [Removing a Cube Override in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_cubeoverride_removing)

To remove a cube override:

1.  Navigate to the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page).
    
2.  Select `Cube Management` > `Cube Overrides`.
    
3.  From the left drop-down list, select the name of the cube.
    
4.  On the right, clear the value in the text box.
    
5.  Select `Save Overrides`.
    
6.  [Reset](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_bulkload#HSAAIC_bulkload_resetting) Health Insight and then reload all the data.
    

## [Defining Custom Cubes in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_cubes)

The following example demonstrates how to create a custom cube and include it in the Health Insight synchronization process:

1.  Navigate to your Health Insight namespace.
    
2.  From the Management Portal, click `Analytics` > `Architect`.
    
3.  Click `New` and select the `Cube` radio button under `Definition Type`.
    
4.  Create a new cube with `Cube Name` as `TestCube` and `Cube Source` as `Class`. For `Source Class`, click `Browse` and select `Persistent` > `HSAA` > `Patient`.
    
5.  Click `OK`, then click `OK` again.
    
6.  In the `Source Class` column, drag the `Age` property to the `Measures` heading in the middle area of the page. This creates a measure named `Age`, based on the class property with that name. To create an example dimension, expand the `Primary Language` drop down in the `Source Class` column and drag the `Code` property to the `Dimensions` drop down in the middle area of the page.
    
7.  Click `Save`, then `Compile` and `Build`.
    
8.  Next, navigate to the `Cube Sync Settings` page ([Health Insight Home Page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_intro#HSAAIC_home_page) > `Cube Management` > `Cube Sync Settings`).
    
9.  Click `Refresh Active Cube Registry`, then reload the page.
    
10.  Under `Cube Group Settings`, select the checkbox next to the new cube group that contains your custom cube.
     
11.  Click `Save Settings`. This will include your new custom cube in the Health Insight cube sync process.
     

If you create a custom cube that is related to an existing, [deprecated](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAARN_ch_new_features_HSAA_20261#HSAARN_20261_cube_deprecate) Health Insight clinical cube, using the `Refresh Active Cube Registry` button will automatically add that cube to the Health Insight Clinical Group.

You can rename cube groups using the `Rename Cube Groups` button. Note that cube groups may not have names of the form “`Group N`”, where `N` is a natural number. For example, a cube group cannot be named “`Group 1`”.

## [Disabling Cubes with Relationships in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_cube_disable)

If you disable a cube, follow these guidelines to ensure that other cubes are appropriately updated:

*   First see “[Additional Steps When Customizing Health Insight in a Mirrored Environment](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_customize_mirror).”
    
*   [Make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write).
    
*   Disable the cube via cube override. See [Disabling a Cube via Override](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_overrides_disable). Cubes that are disabled via cube override will remain disabled after upgrades.
    
*   If the disabled cube has relationships, use cube overrides to disable all those relationships. That is, modify each cube that has a relationship to the disabled cube by using a cube override to disable that relationship. For example, use the following:
    
    ```
    set ^DeepSee.Overrides(cubeName,"RELATIONSHIPS","ALLERGIES", "DISABLED") = 1
    ```
    
    Then compile the override class and then compile the cube class.
    
*   Return HSAALIB to read-only by following the procedure to [make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write), but select the `Mount Read-Only` option instead of clearing it.
    
*   After disabling the cube and the relationships, rebuild all modified cubes.
    
    See “[API for Monitoring and Managing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api).”
    

## [Using Cube Inheritance in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_inherit)

A more advanced form of customization is to use the cube inheritance feature. In this case, you do not use the standard Health Insight cubes directly. Instead, you create cubes that inherit from these cubes, and then use your cubes instead.

Each subcube has its own fact table and indices, and (at run time) these are independent of the parent cube. The inheritance mechanism is used only at build time, and affects only the definitions in the cubes.

To use cube inheritance:

1.  Determine the logical name of the cube that you want to inherit from.
    
    To do so, find the class that contains the cube definition. Each Health Insight cube is in a separate class, in the package `HSAA`. (Ignore the subpackages, which mostly contain generated classes.) In this class, the logical name of the cube is specified in the `name` attribute of the `<cube>` element in the `Cube` XData block.
    
2.  Create a new cube class as described in [Using Cube Inheritance](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODADV_ch_cube_inheritance) in Advanced Modeling for InterSystems IRIS Business Intelligence.
    
    For information on the recommended location of the class, see [Ensuring That Your Customizations Support Mirroring and Easier Upgrades](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_planning#HSAAIC_customization_approach), earlier in this book.
    
3.  In your class, specify the `inheritsFrom` attribute for the cube. For the value of this attribute, specify the logical name of the parent cube.
    
4.  In the Architect or in [your IDE](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides), optionally create additional definitions (dimensions, measures, listings, and so on).
    
    Note that neither the Architect nor the IDE provides a merged view of the new cube. That is, each of these shows only the definitions in this class, not the inherited parts.
    
5.  Optionally redefine any dimension, measure, or other top-level element specified in the parent cube. To do so, specify a definition in the child cube and use the same logical name as in the parent cube. The new definition completely replaces the corresponding definition from parent cube. For [additional notes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_inherit_notes), see the subsection.
    
    Also, for information on determining these logical names, see “[Understanding the Health Insight Cube Definitions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_cubedefs)”.
    
6.  Optionally disable the relationships in this cube or create new relationships between this cube and other cubes. See “[Defining Cube-Cube Relationships](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODADV_rel)” in [Advanced Modeling for InterSystems IRIS Business Intelligence](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODADV).
    
    > **Important:**
    > 
    > If the subcube uses a build restriction, it is necessary to disable the relationships in the cube, because the inherited relationships will not provide correct data.
    
    If the parent cube has any relationships, note that those relationships are inherited, but necessarily not in a useful way, because the relationships always point to the original cubes.
    
    For example, suppose that two cubes (Patient and Encounter) are related to each other, and you create subcubes (CustomPatient and CustomEncounter) for each of them. By default, CustomPatient has a relationship that points to the original Encounter cube. Similarly, the CustomEncounter cube has a relationship that points to the Patient cube. If you want a relationship between CustomPatient and CustomEncounter, you must define that relationship explicitly in the subcubes.
    
7.  Optionally define cube overrides for your cubes. See “[Defining Cube Overrides](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_overrides).”
    
8.  Compile your classes.
    
9.  Build your cubes. For details, see the chapter “[Compiling and Building Cubes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODEL_ch_build_etc)” in [Defining Models for InterSystems IRIS Business Intelligence](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2MODEL).
    

### [Notes on Cube Inheritance](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_inherit_notes)

It might be necessary for your cube class to include the parent cube class in its superclass list, in addition to using the cube inheritsFrom feature. This is necessary if any source expression in the cube class (or any of its parent cubes) uses the `%cube` variable to refer to a method. For example, if the parent cube defines a level via the source expression `%cube.GetLevelData()`, and if the subcube does not redefine this level to use a different source, then the subcube class must extend the parent cube class.

Note that the `disabled` attribute has no effect in the subcube. That is, you cannot use this attribute to disable items that are defined in the parent cube. It is still possible, however, to remove or hide levels and measures, as the following discussion shows.

To redefine a dimension, create a `<dimension>` element in the subcube and use the same logical name for the dimension as in the parent cube. In the `<dimension>` element, define all the hierarchies and levels that this dimension should contain. This `<dimension>` element completely replaces the `<dimension>` of the parent cube. The new dimension can, for example, define fewer or more levels than the corresponding dimension in the parent cube.

You can use the `hidden` attribute to hide a measure. The measure is still created but is not shown in the Analyzer. This attribute is ignored for other items.

## [Customizing the Codes Used in Patient Current Conditions](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_calccode)

Health Insight provides a central table, `HSAA.CalculationCode`, that stores all codes used in defining the Patient Current Conditions cube. If you use the following guidelines, you can add your own data directly to the `HSAA.CalculationCode`, and your data will be preserved on upgrades. For any row that you add:

*   Specify the IsISC column to 0.
    
*   Specify the IsActive column as 1 (if the row should be used) or as 0 (if the row should be ignored).
    

> **Tip:**
> 
> To see how some of the current conditions are defined, open the [HSAA.CubeQueries](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.CubeQueries) class in [your IDE](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides), if you have access.

## [Example Calculated Measures and Members in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_calc_member)

Below are some examples of useful calculated measures and members. For information on creating calculated measures and members, see “[Creating Calculated Measures and Members](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2GMDX_ch_calculated_members)” in [Using InterSystems MDX](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2GMDX).

### [Distinct Patient Count](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_patient_count)

One common calculated measure displays a count of distinct patients (that is, eliminating duplicates) in a given context. For example, from within the allergies cube, you might want to see how many distinct patients have allergies. To do so, create (in the allergies cube) a calculated measure with the following MDX query:

```
Count([PATIENT].[PATIENTID].[H1].[HSAAID].Members,EXCLUDEEMPTY)
```
