# [Specifying CPU Count for the RebuildIndices Utility](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAREF_rebuildindices#HSAAREF_rebuildindices)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq) (AADBQ-based feed).

This section describes the process for specifying logical CPU count for the RebuildIndices utility. The information in this section supports a step in the [upgrade procedure](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAUP_postupgrade#HSAAUP_postupgrade_index).

You can use the `^IRIS.HSAA.Internal("NumberWorkersOverride")` configuration global to specify the number of logical CPUs used for running the RebuildIndices API as a background job.

If you do not set the `^IRIS.HSAA.Internal("NumberWorkersOverride")` global, the default of 25% of the logical CPUs of the Health Insight instance's server will be used for the API. To use more or less than the default for running the API, you can set the ^IRIS.HSAA.Internal("NumberWorkersOverride") global:

*   If you set the global to a positive number, that number of logical CPUs will be used.
    
*   If you set the global to a negative value, one logical CPU will be used.
    
*   If the global is set to a value greater than the total number of CPUs, the total number of CPUs will be used.
    

> **Important:**
> 
> InterSystems strongly recommends that you do not use 100% CPU power to run the API. Ensure that other operations on the server have enough resources to run.

Before you run the API, assess the system and applications’ resource needs. Decide if you want to set the `^IRIS.HSAA.Internal("NumberWorkersOverride")` global to a different value, or if you want to use the default. You can determine the total number of CPUs of your server by running the following command in any namespace:

```
write $SYSTEM.Util.NumberOfCPUs()
```

This command returns the number of logical CPUs.

As an example, in a server where `NumberOfCPUs()` returns 20 as the number of logical CPUs:

*   If you do not set the `^IRIS.HSAA.Internal("NumberWorkersOverride")` global, 25% of the CPUs (5), will be used for running the API.
    
*   If you want to allocate 50% of the CPUs, you can set the `^IRIS.HSAA.Internal("NumberWorkersOverride")` global to 10.
    

In the latter scenario, RebuildIndices will complete more quickly than in the former.

To set the `^IRIS.HSAA.Internal("NumberWorkersOverride"`) global, run the following command in your analytics namespace:

```
set ^IRIS.HSAA.Internal("NumberWorkersOverride")=value
```

...where `value` is your chosen value for the global.
