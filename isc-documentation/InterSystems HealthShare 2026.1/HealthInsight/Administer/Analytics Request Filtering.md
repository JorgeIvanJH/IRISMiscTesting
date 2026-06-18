# [Filtering Analytics Update Requests](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_filter#HSAAADM_filter)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq).

You can filter incoming `AnalyticsUpdateRequest` messages in HealthShare Health Insight.

## [Health Insight Filter Overview](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_filter#HSAAADM_filter_over)

In HealthShare Health Insight, you can create filters to filter incoming `AnalyticsUpdateRequest` messages using user-defined code. A Health Insight Operator can use methods from the [HSAA.Config.AnalyticsUpdateRequestFilter.API.Service](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HSAA.Config.AnalyticsUpdateRequestFilter.API.Service) class to register, unregister, and retrieve the active filter on a Health Insight instance. The filter is a separate class which contains code that evaluates whether a record should be filtered. The input to the filter class is the HSAAID from Health Insight.

## [Working with the Health Insight Filtering Mechanism](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_filter#HSAAADM_filter_work)

In order to filter incoming `AnalyticsUpdateRequest` messages, do the following:

1.  Create a new user-defined class method with the following signature:
    
    ```
    ClassMethod UserFilter(HSAAID As %String, Output filterResult As %Boolean = 0) As %String
    ```
    
    where `UserFilter` is the name of your filter method. This method should accept a patient’s HSAAID as input and determine if that patient should be filtered out of Health Insight.
    
    The following is an example filter method:
    
    ```objectscript
    ClassMethod TestFilter(AnalyticsID As %String, Output filterResult As %Boolean = 0) As %Status
    {
      set sc = $$$OK
      try {
        set filterResult = $Data(^CustomerFilterGlobal(AnalyticsID))
      }
    
      catch (ex) {
        set sc = ex.AsStatus()
      }
    
      quit sc
    }
    ```
    
2.  Register this filter method with a call such as the following:
    
    ```
    do ##class(HSAA.Config.AnalyticsUpdateRequestFilter.API.Service).Instance().Register
                                                 (
                                                   UserFilterClassName:UserFilterMethodName
                                                 )
    ```
    
    where `UserFilterClassName` is the class name of your class method, and `UserFilterMethodName` is the name of your filter method.
    
3.  Health Insight will now invoke the filtering method upon ingestion. If an `AnalyticsUpdateRequest` is filtered, Health Insight will log the event in the Health Insight logger as an INFO level message. If the user method throws an error, Health Insight will treat the error as a patient error.
    

You can use the `Get()` method to return the class and class method names of the currently registered custom filter, if there is one:

```objectscript
 do ##class(HSAA.Config.AnalyticsUpdateRequestFilter.API.Service).Instance().Get()
```

You can also unregister the current custom filter with the `Unregister()` method:

```objectscript
 do ##class(HSAA.Config.AnalyticsUpdateRequestFilter.API.Service).Instance().Unregister()
```

## [Testing the Health Insight Filtering System](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_filter#HSAAADM_filter_test)

Prior to deploying a test filter onto a system, a Health Insight Operator can test the custom filter by passing in an HSAAID that should be filtered. In this case, the `filterResult` output should have a value of `1`. If you pass in an HSAAID that should not be filtered, `filterResult` should have a value of `0.`

You should also register the filter with the `Register()` method to ensure that it has the correct signature. If you are not ready to deploy your filter, you can immediately unregister the filter afterwards.

Additionally ensure that you test any custom code prior to use in production, as custom code may impact system performance.
