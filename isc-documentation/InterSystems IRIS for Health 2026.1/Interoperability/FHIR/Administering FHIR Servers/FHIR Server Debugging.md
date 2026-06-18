# FHIR Server Debugging

InterSystems provides a debug mode and logging to help debug a FHIR server during development

## Debugging the FHIR Server

Putting the FHIR server in debug mode helps solve problems during development and can temporarily eliminate the need to authenticate HL7 FHIR requests. You can configure the following debugging parameters:

*   `New Service Instance` — Instantiates a new Service object for every FHIR request. Set this option when making changes to your custom architecture classes, such as your Interactions and InteractionsStrategy subclasses.
    
*   `Include Tracebacks` — When a FHIR request incurs an Internal Server Error, the FHIR server includes a stack trace in the returned OperationOutcome resource.
    

To configure the debugging parameters in a Terminal, follow these steps:

1.  In a Terminal, in your Foundation namespace, execute the following command:
    
    ```objectscript
     do ##class(HS.FHIRServer.ConsoleSetup).Setup()
    ```
    
2.  Choose option 6: `Configure a FHIRServer Endpoint`.
    
3.  When prompted, specify the desired endpoint.
    
4.  In the `Edit CSP Application Configuration` section, you can accept the defaults.
    
5.  In the `Edit FHIRService Configuration` section, set a value for `DebugMode`, according to the table below:
    
    ### DebugMode Values
    
    <table><tr><td>Value</td><td>New Service Instance</td><td>Include Tracebacks</td></tr><tr><td><code>0</code></td><td>Disabled</td><td>Disabled</td></tr><tr><td><code>1</code></td><td>Disabled</td><td>Enabled</td></tr><tr><td><code>2</code></td><td>Enabled</td><td>Disabled</td></tr><tr><td><code>3</code></td><td>Enabled</td><td>Enabled</td></tr></table>
    

> **Note:**
> 
> If you prefer, you can configure the debugging parameters using the PUT /endpoints/{serviceid} API. In the query body, inside the `service_config_data` block, set the value of `debug_mode`, using the values in the DebugMode Values table:
> 
> ```
> {
> 	...
> 	"service_config_data":{
> 		...
> 		"debug_mode":<value>
> 	}
> 	...
> }
> ```

## FHIR Server Logging

The FHIR server provides two types of logging:

*   Internal FHIR Server Logging — Provides information about how the FHIR server architecture is processing FHIR requests, including which class methods are being called.
    
*   HTTP Request Logging — Provides information about the HTTP requests coming from REST clients to the FHIR server.
    

### Internal FHIR Server Logging

The FHIR server provides basic logging information about how the architecture is processing the FHIR requests being received by the server, including which class methods are being called, SQL-related messages, and how `_include` searches are being handled. To enable this type of logging:

1.  Open the InterSystems Terminal.
    
2.  Navigate to the FHIR server’s namespace. For example, enter:
    
    ```objectscript
     set $namespace = "FHIRNamespace"
    ```
    
3.  Create a global, `^FSLogChannel`, that specifies what type of logging information should be stored. The syntax for creating the global is:
    
    ```objectscript
     set ^FSLogChannel(channelType) = 1
    ```
    
    Where `channelType` is one of the following:
    
    *   `Msg` — Logs status messages.
        
    *   `SQL` — Logs SQL-related information.
        
    *   `_include` — Logs information related to searches that use the `_include` and `_revinclude` parameters.
        
    *   `all` — Logs all three types of information.
        
    
    For example, to enable logging for all types of information, enter:
    
    ```objectscript
     set ^FSLogChannel("all") = 1
    ```
    

> **Note:**
> 
> To switch to a new type of logging information (for example, from `Msg` to `SQL`), kill the existing `^FSLogChannel` global before setting it again with the new `channelType`.

#### Viewing the Log

Once logging for the FHIR server architecture is enabled, the log entries are stored in the `^FSLOG` global. To use the Management Portal to view the log, navigate to `System Explorer` > `Globals` and view the `FSLOG` global (not `FSLogChannel)`. Make sure you are in the FHIR server’s namespace.

Each node of the global is structured like:

`CurrentMethod^CurrentClass|LogType|LogMessage`

For example, a log entry in a node of the `^FSLOG` global might be:

`"runQuery^HS.FHIRServer.Storage.JsonAdvSQL.Interactions|SQL|Parameters: (2)"`

#### Disabling Logging

To disable logging for the FHIR server architecture, simply kill the `^FSLogChannel` global or set it to `0`. For example, you can enter the following in the Terminal:

```objectscript
 kill ^FSLogChannel
```

### HTTP Request Logging

When HTTP request logging is enabled, the REST handler that is receiving requests from FHIR clients writes information about each HTTP request to the `ISCLOG` global. To enable this type of logging:

1.  Open the InterSystems Terminal.
    
2.  From any namespace, enter the following commands to configure the global `^%ISCLOG` to start logging HTTP requests:
    
    ```objectscript
     set ^%ISCLOG=5
     set ^%ISCLOG("Category","HSFHIR")=5
     set ^%ISCLOG("Category","HSFHIRServer")=5
    ```
    
    Note that the global you use to configure logging (`^%ISCLOG`) has a different name than the global to which the logging information is written (`^ISCLOG`).
    

#### Viewing the Log

Once logging for HTTP requests is enabled, the log entries are stored in the `^ISCLOG` global, which is located in the `%SYS` namespace.

To use the Management Portal to view the log, navigate to `System Explorer` > `Globals` and view the `ISCLOG` global (not `%ISCLOG)`. Make sure you are in the `%SYS` namespace.

#### Disabling Logging

To disable HTTP request logging, open the Terminal and enter the following command:

```objectscript
 set ^%ISCLOG=1
```

### FHIR Test Utility

The FHIR Test Utility that appears in the Management Portal (`Health` > `FHIR Test Utility`) does not work with the current FHIR architecture. It still works with the legacy FHIR technology.
