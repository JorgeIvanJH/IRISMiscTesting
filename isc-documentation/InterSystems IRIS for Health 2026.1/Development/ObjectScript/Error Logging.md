# Error Logging

Each namespace can have an application error log, which records errors encountered when running code in that namespace. Some system code automatically writes to this log, and your code can do so as well.

## Logging Application Errors

To log an exception to the application error log, use the %Exception.AbstractException.Log() method. Typically you would do this within the CATCH block of a TRY-CATCH.

## Using Management Portal to View Application Error Logs

From the Management Portal, select `System Operation`, then `System Logs`, then `Application Error Log`. This displays the `Namespace` list of those namespaces that have application error logs. You can use the header to sort the list.

Select `Dates` for a namespace to display those dates for which there are application error logs, and the number of errors recorded for that date. You can use the headers to sort the list. You can use `Filter` to match a string to the Date and Quantity values.

Select `Errors` for a date to display the errors for that date. Error # integers are assigned to errors in chronological order. Error # `*COM` is a user comment applied to all errors for that date. You can use the headers to sort the list. You can use `Filter` to match a string.

Select `Details` for an error to open an `Error Details` window that displays state information at the time of the error including special variables values and `Stacks` details. To see the stack trace corresponding to the error, click the `Stacks` or scroll to the bottom of the page. Then click the + icon in the row of this table and look for the `%objlasterror` variable, which (if present) contains information about the error.

You can specify a user comment for an individual error.

The `Namespaces`, `Dates`, and `Errors` listings include check boxes that allow you to delete the error log for the corresponding error or errors. Check what you wish to delete, then select the `Delete` button.

## Using ^%ERN to View Application Error Logs

The `^%ERN` utility examines application errors and lets you see all errors logged for the current namespace. This is an alternative to using the Management Portal.

Take the following steps to use the `^%ERN` utility:

1.  In an ObjectScript shell, enter `DO ^%ERN`. The name of the utility is case-sensitive; responses to prompts within the utility are not case-sensitive.
    
    At any prompt you may enter `?` to list syntax options for the prompt, or `?L` to list all of the defined values. You may use the `Enter` key to exit to the previous level.
    
2.  At the `For Date:` prompt, enter `?L` to see a list of all the dates when errors occurred.
    
3.  Then at the same prompt, enter one of those dates (in the format mm/dd/yyyy); if you omit the year, the current year is assumed. The routine then displays the date and the number of errors logged for that date. Alternative, you can retrieve lists of errors from this prompt using the following syntax:
    
    *   `?L` lists all dates on which errors occurred, most recent first, with the number of errors logged. The `(T)` column indicates how many days ago, with `(T)` = today and `(T-7)` = seven days ago. If a user comment is defined for all of the day’s errors, it is shown in square brackets. After listing, it re-displays the `For Date:` prompt. You can enter a date or `T-n`.
        
    *   `text` lists all errors that contain the substring `text`. `<text` lists all errors that contain the substring `text` in the error name component. `^text` lists all errors that contain the substring `text` in the error location component. After listing, it re-displays the `For Date:` prompt. Enter a date.
        
4.  `Error:` at this prompt supply the integer number for the error you want to examine: 1 for the first error of the day, 2 for the second, and so on. Or enter a question mark (?) for a list of available responses. The utility displays the following information about the error: the Error Name, Error Location, time, system variable values, and the line of code executed at the time of the error.
    
    You can specify an * at the `Error:` prompt for comments. `*` displays the current user-specified comment applied to all of the errors of that day. It then prompts you to supply a new comment to replace the existing comment for all of these errors.
    
5.  `Variable:` at this prompt you can specify numerous options for information about variables. If you specify the name of a local variable (unsubscipted or subscripted), `^%ERN` returns the stack level and value of that variable (if defined), and all its descendent nodes. You cannot specify a global variable, process-private variable, or special system variable.
    
    You may enter `?` to list other syntax options for the `Variable:` prompt.
    
    *   `*A`: when specified at the `Variable:` prompt, displays the `Device:` prompt; press `Return` to display results.
        
    *   `*V`: when specified at the `Variable:` prompt, displays the `Variable(s):` prompt. At this prompt specify an unsubscripted local variable or a comma-separated list of unsubscripted local variables; subscripted variables are rejected. `^%ERN` then displays the `Device:` prompt; press `Return` to display results. `^%ERN` returns the value of each specified variable (if defined) and all its descendent nodes.
        
    *   `*L`: when specified at the `Variable:` prompt, loads the variables into the current partition. It loads all private variables (as public) and then all public variables that don't conflict with the loaded private variables.
        

## [See Also

*   %SYS.ProcessQuery.ExamStackByPid() method, which provides details on the `^mtemp` global used by `^%ERN`
