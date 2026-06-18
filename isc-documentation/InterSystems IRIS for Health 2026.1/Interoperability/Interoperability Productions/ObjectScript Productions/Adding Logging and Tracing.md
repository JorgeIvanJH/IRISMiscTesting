# Adding Logging and Tracing

This page describes how to add Event Log entries and trace messages to a production. The Event Log is intended primarily for system administrators, but which is also useful during development. Trace messages, in contrast, are primarily for use during development.

## Generating Event Log Entries

The Event Log is a table that records events that have occurred in the production running in a given namespace. The Management Portal provides a page that displays this log, which is intended primarily for system administrators, but which is also useful during development.

The primary purpose of the Event Log is to provide diagnostic information that would be useful to a system administrator in case of a problem while the production is running.

InterSystems IRIS automatically generates Event Log entries, and you can add your own entries. Any given event is one of the following types: Assert, Info, Warning, Error, and Status. (The Event Log can also include alert messages and trace items.)

To generate Event Log entries:

1.  Identify the events to log.
    
    Not all types of error or activity should necessarily generate Event Log entries. You must choose the occurrences to note, the type to use, and the information to record. For example, Event Log entries should appear in case of an external, physical problem, such as a bad network connection.
    
    The Event Log should not register program errors; these should be resolved before the production is released.
    
2.  Modify the applicable parts of the production (typically business host classes) to generate Event Log entries in ObjectScript, as described in the following subsection.
    

> **Important:**
> 
> If you need to notify users actively about certain conditions or events, use alerts, which are discussed in Generating Alerts and in Defining Alert Processors.

### Generating Event Log Entries in ObjectScript

Within business host classes or other code used by a production, you can generate Event Log entries in ObjectScript. To do so, use any of the following macros. These macros are defined in the `Ensemble.inc` include file, which is automatically included in InterSystems IRIS system classes:

<table><tr><th>Macro</th><th>Details</th></tr><tr><td><code>$$$LOGINFO(message)</code></td><td>Writes an entry of type Info. Here and later in this table, <code>message</code> is a string literal or an ObjectScript expression that evaluates to a string.</td></tr><tr><td><code>$$$LOGERROR(message)</code></td><td>Writes an entry of type Error.</td></tr><tr><td><code>$$$LOGWARNING(message)</code></td><td>Writes an entry of type Warning.</td></tr><tr><td><code>$$$LOGSTATUS(status_code)</code></td><td>Writes an entry of type Error or Info, depending on the value of the given <code>status_code</code>, which must be an instance of <a href="https://docs.intersystems.com/irisforhealthlatest/csp/documatic/%25CSP.Documatic.cls?LIBRARY=%25SYS&amp;CLASSNAME=%25Library.Status">%Status</a>.</td></tr><tr><td><code>$$$ASSERT(condition)</code></td><td>Writes an entry of type Assert, if the argument is false. <code>condition</code> is an ObjectScript expression that evaluates to true or false.</td></tr><tr><td><code>$$$LOGASSERT(condition)</code></td><td>Writes an entry of type Assert, for any value of the argument. <code>condition</code> is an ObjectScript expression that evaluates to true or false.</td></tr></table>

The following shows an example with an expression that combines static text with the values of class properties:

```objectscript
 $$$LOGERROR("Awaiting connect on port "_..Port_" with timeout "_..CallInterval)
```

The following example uses an ObjectScript function:

```objectscript
 $$$LOGINFO("Got data chunk, size="_$length(data)_"/"_tChunkSize)
```

## Adding Trace Elements

Tracing is a tool for use primarily during development. You add trace elements so that you can see the behavior of various elements in a production, for the purpose of debugging or diagnosis. To add trace elements to a production, you identify the areas in your code (typically business host classes) where you would like to see runtime information. In those areas, you add lines of code that (potentially) write trace messages. Note that these are messages only in a general sense; trace messages are simply strings and are unrelated to `Ens.Message` and its subclasses.

Tracing consists of two parts:

*   Writing trace messages in applicable parts of the production (as described here)
    
*   Enabling tracing as described in Enabling Tracing.
    

### Writing Trace Messages in ObjectScript

To write trace messages in ObjectScript, use the following lines of code:

*   To write a user trace message:
    
    ```objectscript
     $$$TRACE(trace_message)
    ```
    
    Where `trace_message` is a string containing useful information about the context in which you add this line of code.
    
*   To write a system trace message (less common):
    
    ```objectscript
     $$$sysTRACE(trace_message)
    ```
    

For example:

```objectscript
$$$TRACE("received application for "_request.CustomerName)
```

### Writing Trace Messages from BPL or DTL

To write trace messages in a BPL business process, use the BPL <trace> element.

To write trace messages in a DTL data transformation, use the DTL <trace> element.

## See Also

*   Using the Event Log
