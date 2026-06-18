# [Keeping the Health Insight Cubes Current](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent#HSAAIC_cubescurrent)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

This chapter describes your options for keeping the HealthShare Health Insight cubes current.

## [Cube Build Overview](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent#HSAAIC_cubescurrent_overview)

After you load data into Health Insight, before you can use the cubes, it is necessary to build them, which creates the fact table and indexes that each cube uses. Note that it can take a considerable amount of time to build a cube and no queries can be executed until the cube is completely built. To build cubes, use the methods provided in the [HSAA.API.Cubes](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.API.Cubes) [API](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api), such as `RebuildAllCubes()`.

For a live system (where smaller amounts of data arrive frequently) that uses cubes, you typically build the clinical and reporting cubes once after the initial data feed. This initial build can be resource-intensive and time-consuming, especially with large data volumes. Ensure that you have appropriate resources and time allocated. After that, if you enable automatic cube synchronization, the clinical and reporting cubes are automatically synchronized after subsequent data feeds as part of the batch process. When Health Insight synchronizes cubes, it makes incremental changes to the fact tables and indexes; this process is quicker than performing a complete rebuild, and queries can be executed during the process. Note that before you can synchronize the cubes, it is necessary to build them all at least once.

If you need to use cubes, you should enable automatic cube synchronization as described in the [next section](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent#HSAAIC_cubescurrent_sync_enable); in this case, Health Insight automatically synchronizes the cubes after receiving data. You can also manually synchronize the cubes periodically via methods provided in the [HSAA.API.Cubes](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.API.Cubes) [API](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_api), such as `SynchronizeAllCubes()`. Note that you cannot ingest data into Health Insight while using API methods to sync or build cubes. The build and sync API methods will build and sync the cubes in the correct order.

Cubes are an optional feature in Health Insight. You can turn off the Health Insight cubes, as [described below](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent#HSAAIC_cubescurrent_disable).

Consistency Check cubes are built by scheduled tasks that are suspended by default.

Also see the [last section](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent#HSAAIC_cubescurrent_age) for information on the special case of keeping patient ages current.

## [Enabling Automatic Cube Synchronization](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent#HSAAIC_cubescurrent_sync_enable)

Health Insight organizes cubes into cube groups, which are collections of cubes that need to be updated together. You can manage cube groups and cube synchronization settings on the `Cube Sync Settings` page.

To enable automatic cube synchronization for a specific cube group:

1.  Navigate to the `Cube Sync Settings` page. To do so, first access the [Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_home_page), then click `Cube Management` > `Cube Sync Settings`.
    
2.  Select the check box next to the cube group.
    
3.  Click `Save Settings`.
    

The `Cube Sync Settings` page displays cube groups in the currently active cube registry. A cube registry defines a set of cube groups.

You can rename custom cube groups using the `Rename Cube Group` button. For information on how to create a custom cube and include it in the Health Insight sync process, see [Defining Custom Cubes](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_cubes).

## [Turning Off the Cubes](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent#HSAAIC_cubescurrent_disable)

Cubes are optional in Health Insight. You can turn off cubes in Health Insight by doing the following:

1.  Do not perform an initial cube build if you are working with a new Health Insight system and have not built the cubes for the first time.
    
2.  Disable automatic cube synchronization for all cubes on the `Cube Sync Settings` page ([Health Insight home page](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAA_intro#HSAA_home_page) > `Cube Management` > `Cube Sync Settings`).
    
3.  Set up a task in the Task Manager to periodically clear the `^OBJ.DSTIME` global. For more information on setting up such a task, see the [Business Intelligence documentation](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=D2IMP_ch_current).
    
4.  Remove your [post-sychronization processing method](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_additional), if you have one.
    

If you ever re-enable your cubes, you must remove the task that you created to clear the `^OBJ.DSTIME` global.

## [Keeping Patient Age Current](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent#HSAAIC_cubescurrent_age)

The calculation of patient age takes patient death date into consideration such that if a patient dies, the patient’s age is no longer updated. This calculation requires that the `Age` dimension be handled in a unique way. Consequently, `Age` is only accurate as of build time. The following is a suggested method for handling this:

### [Use Birth Date Instead of Age](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_cubescurrent#HSAAIC_cubescurrent_age_birthdate)

You can instead do age-related analysis by using the `Birth Day` level within the `Birth Date` dimension.

If you do not rebuild the patient cube and all its dependent cubes daily, InterSystems recommends that you disable the `Age` dimension. To do so, create a cube override. See “[Using Cube Overrides](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAIC_extendcube#HSAAIC_custom_overrides)” for more details.
