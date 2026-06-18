# [SDA Extensions and Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_sdaext)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

HealthShare provides a mechanism to extend the SDA. If you extend the SDA in HealthShare Unified Care Record, you must make analogous extensions in HealthShare Health Insight, so that it can interpret and store the data. For any SDA extensions that you make in the `HS.Local.SDA3` extension classes in Unified Care Record, make the same changes in the analogous `HSAA.Local` extension classes in Health Insight.

This appendix discusses the details, for [non-mirrored environments](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_sdaext_nonmirror) and [mirrored environments](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_sdaext_mirror).

## [Creating SDA Extensions in a Non-Mirrored Environment](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_sdaext_nonmirror)

This section discusses how to create SDA extensions in a non-mirrored environment.

### [Extending SDA in Unified Care Record](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_extend_infoexchange)

When you install HealthShare, an `HSCUSTOM` namespace and database are automatically created. The `HSCUSTOM` database contains both the `HS.Local` and `HSAA.Local` packages that you use to extend the SDA.

The chapter “[Customizing the SDA](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HXSDA_ch_sda_custom)” in The InterSystems Clinical Data Model: SDA describes how to extend the SDA. The steps below summarize the process:

1.  Connect to the instance with [your IDE](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides) and open the `HSCUSTOM` namespace.
    
2.  Add properties to the extension class associated with the SDA class that you wish to extend. For example, to extend [HS.SDA3.Allergy](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Allergy), open [HS.Local.SDA3.AllergyExtension](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&CLASSNAME=HS.Local.SDA3.AllergyExtension).
    
    You can add properties of the following types:
    
    *   [%String](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&CLASSNAME=%25Library.String)
        
    *   Any `HS.SDA3.`<DataType> such as Boolean or Numeric
        
    *   Any existing `HS.SDA3` serial class
        
    *   Any custom serial class that you have created, which must extend [HS.SDA3.DataType](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.DataType). Any custom serial classes should not be defined in HealthShare packages that are available out of the box, like HS.Local or HS.SDA3. They should instead be defined in custom user packages. This ensures that your class names will not conflict with any future standard SDA3 class names. For example, you should name your custom serial class something like `ZUser.HS.MySDASection`, rather than `HS.SDA3.MySDASection`. If you create custom user packages, add mappings for them to HSCUSTOM.
        
    *   Any new code tables that you have created, which must extend [HS.SDA3.CodeTableTranslated](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.CodeTableTranslated); the following code tables are not translatable:
        
        #### [Code Tables that are Excluded from Translation](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_B15093)
        
        <table><tr><td>HealthCareFacility</td><td>CareProviderType</td><td>Country</td></tr><tr><td>Organization</td><td>City</td><td>County</td></tr><tr><td>User</td><td>State</td><td>Trust</td></tr><tr><td>CareProvider</td><td>Zip</td><td>&nbsp;</td></tr></table>
        
3.  Save and compile the `HS.Local.SDA3` class.
    
4.  Propagate the changes to any other HealthShare instances in your Unified Care Record instance.
    

### [Making Analogous SDA Extension Changes in Health Insight](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_extend_healthinsight)

If you have customized the SDA in Unified Care Record, use the following process to make analogous changes to the corresponding `HSAA.Local.`<SDAType>`Extension` classes in Health Insight.

1.  If you are running Health Insight in its own instance, propagate your SDA extensions to `HSCUSTOM` in the Health Insight instance. In other words, make the same changes to the `HS.Local.SDA3` classes as you made in the Registry, Edge Gateways, and Access Gateways.
    
2.  To make the `HSAA.Local` changes in Health Insight, open [your IDE](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides) and navigate to the `HSCUSTOM` namespace.
    
3.  For the SDA type you are extending, open its `HSAA` extension class. For example, if you are extending [HS.SDA3.Allergy](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Allergy) and you modified [HS.Local.SDA3.AllergyExtension](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&CLASSNAME=HS.Local.SDA3.AllergyExtension), open the [HSAA.Local.AllergyExtension](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Local.AllergyExtension) class.
    
4.  Add properties to the `HSAA.Local.`<SDAType>`Extension` class that are analogous to the ones that you added to the `HS.Local.SDA3.`<SDAType>`Extension` class.
    
    You can add properties of the following types:
    
    *   %String
        
    *   Any `HSAA.Internal`<DataType> such as Boolean or Numeric
        
    *   Any existing HSAA serial class
        
    *   Any custom serial class that you have created, which must extend [HSAA.Internal.DataType](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Internal.DataType). Any custom serial classes should not be defined in Health Insight packages that are available out of the box, like HSAA. They should instead be defined in custom user packages. This ensures that your class names will not conflict with any future standard Health Insight class names. For example, you should name your custom serial class something like `ZUser.HSAA.MySDASection`, rather than `HSAA.MySDASection`. If you create custom user packages, add mappings for them to HSCUSTOM.
        
    *   Any new code tables that you have created, which must extend HSAA.Internal.Interface.CodeTableTranslated; the following code tables are not translatable:
        
        #### [Code Tables that are Excluded from Translation](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_B15120)
        
        <table><tr><td>HealthCareFacility</td><td>CareProviderType</td><td>Country</td></tr><tr><td>Organization</td><td>City</td><td>County</td></tr><tr><td>User</td><td>State</td><td>Trust</td></tr><tr><td>CareProvider</td><td>Zip</td><td>&nbsp;</td></tr></table>
        
5.  Save and compile the `HSAA.Local.`<SDAType>`Extension` class.
    
6.  [Make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write).
    
7.  Switch to the `HSAALIB` namespace.
    
8.  Open the `HSAA` class that is being extended. For example, if you are extending `Allergy` and changes have been made to the [HS.Local.SDA3.AllergyExtension](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&CLASSNAME=HS.Local.SDA3.AllergyExtension) and [HSAA.Local.AllergyExtension](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Local.AllergyExtension) classes, you should open the [HSAA.Allergy](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Allergy) class.
    
9.  Compile the `HSAA.`<SDAType> class ([HSAA.Allergy](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Allergy), in our example).
    
10.  Recompile the entire `HSAA` package.
     
11.  Return HSAALIB to read-only by following the procedure to [make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write), but select the `Mount Read-Only` option instead of clearing it.
     
12.  If you added any custom serial class properties in the “add properties” step of this procedure, you must also register each of these custom classes. Registering your custom serial classes sets up a mapping between the custom serial class data type in the SDA extension and the corresponding serial Health Insight class data type. This mapping is necessary for data transfer between the Unified Care Record and Health Insight.
     
     For instructions on how to do so, see the section “[Registering Custom Container Classes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_customcontainer)” in the chapter “[Customizing Health Insight](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube)”. Note that these instructions are for registering custom container classes, but can also be used to register custom serial classes in your SDA extensison classes. In order to properly register your custom serial classes, follow the existing procedure in the “[Registering Custom Container Classes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_customcontainer)” section, but enter the class name of the custom serial class in Unified Care Record for the `SDA Source Class` field and enter the class name of the serial class in Health Insight for the `Health Insight Class Name` field. For example, you might enter something like `ZUser.HS.SDA3.MySDASection` for your `SDA Source Class` field and `ZUser.HSAA.MySDASection` for your `Health Insight Class Name` field. Alternatively, you can also use the `RegisterCustomClassMapping()` method to register your custom serial classes.
     

Once you have performed the above steps, there will be new properties available in the `HSAA.`<SDAType> class. For example, if you run a query against the [HSAA.Allergy](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Allergy) table:

```sql
SELECT * FROM HSAA.Allergy
```

You will see new fields of the form: `Extension_PropertyName1`, `Extension_PropertyName2`, etc.

Note that the `HSAA.Local.Alert` and `HSAA.Local.AlertExtension` classes are not used in Health Insight. Use the equivalent `HSAA.Local.AdvancedDirective` and `HSAA.Local.AdvancedDirectiveExtension` classes instead.

### [Making HSAALIB Temporarily Writable](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write)

The `HSAALIB` database is marked read-only after installation so that Health Insight can work in containers. In some procedures, such as when creating SDA extensions, you must make `HSAALIB` temporarily writable prior to compiling changes in `HSAALIB`. To do so:

1.  In the Management Portal, navigate to `System Administration` > `Configuration` > `System Configuration` > `Local Database`.
    
2.  On the `Local Databases` page, click `HSAALIB` under the `Name` column.
    
3.  Clear the `Mount Read-Only` option.
    
4.  Click `Save`.
    

You can also make HSAALIB temporarily writable via the `SetHSAALIBWriteable()` method. To do so:

1.  Open the Terminal and navigate to your HSAALIB namespace.
    
2.  Run the following command:
    
    ```
    write sc=##class(HSAA.API.Database).SetHSAALIBWriteable(1)
    ```
    

If the command runs successfully, it returns a status of 1. Otherwise, a 0 and error messages are returned.

You can set HSAALIB to read-only via the same method if you pass in 0 instead of 1 as an argument.

### [Example](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_example)

The following is an example of extending both the [HS.SDA3.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Patient) and the [HS.SDA3.Allergy](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Allergy) objects. We will add a property to `Allergy` called `Sneeziness`, measured in the number of tissues, to indicate how sneezy a patient is when reacting to the allergy. We will also add information to `Patient` indicating whether the patient is a pet owner and if so, add a comma-delimited list of pets that they own. The two properties will be named `PetOwner` and `Pets`.

Assume that both Health Insight and Unified Care Record are each running in a single instance.

#### [Unified Care Record Modifications](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_infoexchange_modifications)

1.  Connect to your Unified Care Record instance using [your IDE](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides) and go to the `HSCUSTOM` namespace.
    
2.  Open the [HS.Local.SDA3.PatientExtension](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&CLASSNAME=HS.Local.SDA3.PatientExtension) class.
    
3.  Add the following properties:
    
    ```objectscript
     Property PetOwner As HS.SDA3.Boolean;
    ```
    
4.  Save and compile the class.
    
5.  Open the [HS.Local.SDA3.AllergyExtension](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=ENSLIB&CLASSNAME=HS.Local.SDA3.AllergyExtension) class.
    
6.  Add the following property:
    
    ```objectscript
     Property Sneeziness As %String;
    ```
    
7.  Save and compile the class.
    
8.  Recompile the entire `HS.SDA3` package.
    

#### [Health Insight Modifications](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_healthinsight_modifications)

1.  Propagate the Unified Care Record modifications that you made above to Health Insight, using your source control software, your IDE, or another method of your choice.
    
2.  Connect to your Health Insight instance using [your IDE](https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_ides) and go to the `HSCUSTOM` namespace.
    
3.  Open the [HSAA.Local.PatientExtension](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Local.PatientExtension) class.
    
4.  Add the following properties:
    
    ```objectscript
     Property PetOwner As HSAA.Internal.Boolean;
    ```
    
5.  Save and compile the class.
    
6.  Open the [HSAA.Local.AllergyExtension](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Local.AllergyExtension) class.
    
7.  Add the following property:
    
    ```objectscript
     Property Sneeziness As %String;
    ```
    
8.  Save and compile the class.
    
9.  [Make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write).
    
10.  Switch to the `HSAALIB` namespace.
     
11.  Open the [HSAA.Allergy](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Allergy) class.
     
12.  Compile the class.
     
13.  Open the [HSAA.Patient](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Patient) class.
     
14.  Compile the class.
     
15.  Recompile the entire `HSAA` package.
     
16.  Return HSAALIB to read-only by following the procedure to [make HSAALIB writable](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_hsaalib_write), but select the `Mount Read-Only` option instead of clearing it.
     

## [Creating SDA Extensions in a Mirrored Environment](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_sdaext_mirror)

This steps for creating SDA extensions in a mirrored environment are the same as the steps for creating SDA extensions in a non-mirrored environment.

## [Extending CareProvider and FamilyDoctor](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_sdaext#HSAAIC_careprovider_familydoctorext)

This section discusses how to extend the `HS.SDA3.Patient.FamilyDoctor` and the [HS.SDA3.CodeTableDetail.CareProvider](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.CodeTableDetail.CareProvider) classes.

In SDA, care providers appear in many places: as properties of encounters (admitting clinician, attending clinician, consulting clinician), orders, patients (family doctor) and referrals, for example. As part of mapping care providers to the data model in Health Insight, the following transformations occur:

1.  All family doctors are stored in the [HSAA.CareProvider](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.CareProvider) table.
    
2.  All other care providers are:
    
    *   Stored as serial properties of their appropriate class. For example, the [HSAA.Encounter](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Encounter) class has a property `AttendingClinician`.
        
    *   Added to the [HSAA.CareProvider](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.CareProvider) table.
        

In order for all care provider-related SDA extensions to be stored correctly in Health Insight, do the following:

*   If you wish to extend the `FamilyDoctor` class in Unified Care Record, add properties to the `HS.SDA3.CodeTableDetail.FamilyDoctorExtension` class. In Health Insight, add the same properties to [HSAA.Local.CareProviderExtension](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Local.CareProviderExtension).
    
*   If you wish to extend the `CareProvider` class in Unified Care Record, add properties to the `HS.SDA3.CodeTableDetail.CareProviderExtension` class. In Health Insight, add the same properties to both the [HSAA.Local.CareProviderExtension](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Local.CareProviderExtension) and the [HSAA.Local.Interface.CodeTableDetail.CareProviderExtension](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Local.Interface.CodeTableDetail.CareProviderExtension) classes.
