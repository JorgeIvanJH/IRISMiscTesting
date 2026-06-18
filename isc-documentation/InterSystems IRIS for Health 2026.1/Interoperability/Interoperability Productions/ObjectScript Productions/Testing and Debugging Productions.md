# Testing and Debugging Productions

This topic explains the facilities available for testing and debugging productions. The information is also useful for troubleshooting and tuning production software that is already in use at the enterprise.

## Correcting Production Problem States

If a production is Suspended or Troubled, read this section.

### Suspended Productions

A suspended production occurs when a production is stopped before all asynchronous messages in the queue can be processed. If you do not manually clear these asynchronous messages, they are automatically processed when the production is started back up. If you want the messages to be processed, no other steps are required before starting a suspended production.

### Recovering a Troubled Production

A production acquires a status of Troubled if InterSystems IRIS is stopped but the production did not shut down properly. This can happen if you restarted InterSystems IRIS data platform or rebooted the machine without first stopping the production.

In this case the `Recover` command appears on the `Production Configuration` page. Click `Recover` to shut down and clean up the troubled instance of the production so that you can run a new instance when you are ready.

Or you may need to use the command line to recover the production. See Using Ens.Director to Start and Stop a Production.

### Resetting Productions in a Namespace

During development, you might want to be absolutely sure that all queues for a production have been cleared or to remove all information about a production before starting another one. The `CleanProduction()` method clears the queues.

> **Caution:**
> 
> Never use this procedure on a live, deployed production. The `CleanProduction()` method removes all messages from queues and removes all current information about the production. Use this procedure only on a production that is still under development.

To use the `CleanProduction()` method:

1.  Change to the appropriate namespace:
    
    ```objectscript
     set $namespace = "EnsSpace"
    ```
    
    Where `EnsSpace` is the name of the production-enabled namespace where the production runs.
    
2.  Enter the following command:
    
    ```objectscript
     do ##class(Ens.Director).CleanProduction()
    ```
    

## Testing from the Management Portal

You can use the Management Portal to perform several tasks as you develop, test, and debug your productions:

*   Ability to view and modify system configuration.
    
*   Ability to start and stop a production.
    
*   Ability to view queues and their contents; messages and their details; adapters and actors and their status; business processes and their status; code and graphical representations of configured items.
    
*   Ability to view, sort, and selectively purge Event Log entries.
    
*   Ability to suspend (and later resend) messages whose connectivity is temporarily blocked.
    
*   Ability to filter and search the message warehouse for specific messages, by category or message content, using a graphical user interface or by entering SQL SELECT commands.
    
*   Ability to visually trace message activity using a graphical user interface.
    
*   Ability to create and view statistical reports.
    

Portal features that are most useful for developers are the Monitor Service, which constantly collects runtime data, the Testing Service, which you can use to issue simulated requests into a production that you are developing, and the Event Log, which logs the status messages issued by business hosts. Use these features together to generate test data and study the results.

For information on using the portal, see Managing Productions.

The Management Portal has a Test menu where you can test both business hosts and data transformations. It contains the following items:

*   Business Hosts—The `Interoperability` > `Test` > `Business Hosts` page allows you to test business processes and business operations.
    
*   Data Transformations—This option brings you to another page, where you can select a data transformation and click Test. For details, see the Testing Data Transformations section.
    

### Using the Testing Service

The Testing Service allows you to test a business process or business operation of a running production in the active namespace.

Before testing a business process or business operation:

*   Make sure the appropriate production is running. See Starting and Stopping Productions.
    
*   Make sure that testing is enabled for this production. From the `Production Configuration` page:
    
    1.  Select the `Production Settings` link.
        
    2.  On the `Settings` tab, open the `Development and Debugging` property list and check the `Testing Enabled` check box.
        
    3.  Select `Apply`.
        

You can navigate to the Testing Service from the following locations in the Management Portal:

*   Select `Interoperability` > `Test` and then select either `Business Hosts` or `Data Transformation`.
    
*   From the configuration diagram on the `Production Configuration` page, select a business process or business operation in the left pane and select `Test` on the `Actions` tab.
    

To use the Testing Service on a Business Process or Business Operation:

1.  In the Management Portal, select `Interoperability` > `Test` > `Business Hosts` to display the `Testing Service` page.
    
    This page provides options that let you select either a `Business Process` or `Business Operation` as the target of your testing.
    
2.  Select either `Business Process` or `Business Operation` as appropriate.
    
3.  Select the testing target from the drop-down list.
    
4.  Select the type of message to send. The page displays the following fields:
    
    *   `Current Production`—The name of the currently running production (view-only).
        
    *   `Target`—The business process or business operation that you selected in the previous Testing Service page (view-only).
        
    *   `Request Type`—Select from a list of request messages. Only the request types that are valid for the `Target` are listed, including subclasses of supported types.
        
    
    The system now displays a form you can use to specify values for the properties of the message type you selected.
    
5.  Enter values for the properties of the message. If the request message type has no properties, none are displayed.
    
    By default, this table cannot display more than 99 properties. To increase the number of properties that it can display, enter the following command in the ObjectScript shell in the namespace where this maximum should be increased:
    
    ```objectscript
     set ^CSP.AutoFormMaxProperties=newmaximum
    ```
    
    Where `newmaximum` is an integer that specifies the maximum number of properties to display. (This change also affects the `Body` tab of the Message Viewer and the Visual Trace; see Controlling the Display.)
    
    If you are testing a virtual document message, there is a free-form box where you can paste test message content. Below this box you can enter object properties for the message.
    
6.  Select `Invoke` to submit the request with the values you entered and view the results.
    
    If time elapses while the Testing Service attempts the request, a Waiting page displays the following view-only information:
    
    *   `Target`—The session ID associated with the request.
        
    *   `Request Type`—The request type of the selected target.
        
    *   `Session Id`—The session ID associated with the request.
        
    *   `Request Sent`—The date and time when the request was sent.
        
    *   `Response received`—The status Waiting and a graphical progress bar, indicating that work is being done.
        
    
    Finally, the Results page displays any output values from the response generated by your request, including any errors with the full error message text.
    

You can perform one of the following commands when the test completes:

*   Select `Done` to return to the home page.
    
*   Select `Trace` to navigate to the Visual Trace page to visually follow the path of the message through the production.
    

You can also use the classes and methods in the `EnsLib.Testing` package. See EnsLib.Testing.Service for details.

## Debugging Production Code

The first step in debugging is to enable tracing as described in Enabling Tracing. If this does not reveal the problem, you can step into the code using the debugger, as follows:

1.  Edit the code in an IDE to insert the `BREAK` command where you want to start debugging.
    
2.  Enable the `Foreground` setting for the business host that uses the class you want to debug.
    
3.  Start the production. The job that you marked in Step 2 runs in the foreground in the Terminal.
    
4.  When that `BREAK` command is reached, the Terminal enters debug mode and you can step through the code.
    

For details, see Command-Line Routine Debugging.

## Enabling %ETN Logging

The Event Log automatically includes partial information about system-level exceptions (including exceptions in your code). These Event Log entries end as follows by default:

```
-- logged as '-' number - @' quit arg1/arg2 }'
```

To get more complete information about such errors:

1.  Set the `^Ens.Debug("LogETN")` global node to any value.
    
    This causes InterSystems IRIS to record additional details for system-level exceptions.
    
2.  Rerun the code that you think caused the exception (for example, resend messages).
    
3.  Recheck the Event Log, which now contains entries that end as follows:
    
    ```
    -- logged as '25 Sep 2012' number 15 @' quit arg1/arg2 }'
    ```
    
    This information refers to an entry in the Application Error Log—specifically it refers to error 15 in the Application Error Log for 25 September 2012.
    
4.  Then to examine these exceptions, you can either:
    
    *   Select `System Operation` > `System Logs` > `Application Error Log`.
        
    *   Use the `^%ERN` routine. For details, see Other Debugging Tools.
