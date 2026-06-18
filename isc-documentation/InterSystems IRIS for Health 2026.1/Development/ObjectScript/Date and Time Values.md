# Date and Time Values

This page provides an overview of date and time values in ObjectScript.

## Introduction

ObjectScript has no built-in date type; instead it includes a number of functions for operating on and formatting date values represented as strings. These date formats include:

### Date Formats

<table><tr><th>Format</th><th>Description</th></tr><tr><td>$HOROLOG</td><td>This is the format returned by the <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RCOS_vhorolog">$HOROLOG</a> ($H) special variable. It is a string containing two comma-separated integers: the first is the number of days since December 31, 1840; the second is the number of seconds since midnight of the current day. $HOROLOG does not support fractional seconds. The <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RCOS_fnow">$NOW</a> function provides $HOROLOG-format dates with fractional seconds. InterSystems IRIS provides a number of functions for formatting and validating dates in $HOROLOG format.</td></tr><tr><td>ODBC Date</td><td>This is the format used by ODBC and many other external representations. It is a string of the form: “YYYY-MM-DD HH:MM:SS”. ODBC date values will collate; that is, if you sort data by ODBC date format, it will automatically be sorted in chronological order.</td></tr><tr><td>Locale Date</td><td><p>This is the format used by the current locale. Locales differ in how they format dates as follows:</p><p>“American” dates are formatted mm/dd/yyyy (dateformat 1). “European” dates are formatted dd/mm/yyyy (dateformat 4). All locales use dateformat 1 except the following — csyw, deuw, engw, espw, eurw, fraw, itaw, mitw, ptbw, rusw, skyw, svnw, turw, ukrw — which use dateformat 4.</p><p>American dates use a period (.) as a decimalseparator for fractional seconds. European dates use a comma (,) as a decimalseparator for fractional seconds, except the following — engw, eurw, skyw — which use a period.</p><p>All locales use a slash (/) as the dateseparator character, except the following, which use a period (.) as the dateseparator character — Czech (csyw), Russian (rusw), Slovak (skyw), Slovenian (svnw), and Ukrainian (ukrw).</p></td></tr><tr><td>System Time</td><td>This is the format returned by the <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RCOS_vzhorolog">$ZHOROLOG</a> ($ZH) special variable. It is a floating point number containing the number of seconds (and parts thereof) that the system has been running. Stopping and restarting InterSystems IRIS resets this number. Typically this format is used for timing and testing operations.</td></tr></table>

The following example shows how you can use the different date formats:

```objectscript
 SET now = $HOROLOG
 WRITE "Current time and date ($H): ",now,!

 SET odbc = $ZDATETIME(now,3)
 WRITE "Current time and date (ODBC): ",odbc,!

 SET ldate = $ZDATETIME(now,-1)
 WRITE "Current time and date in current locale format: ",ldate,!

 SET time = $ZHOROLOG
 WRITE "Current system time ($ZH): ",time,!
```

## Date and Time Conversions

ObjectScript includes functions for converting date and time values.

*   Given a date in $H format, the function `$ZDATE` returns a string that represents the date in your specified format.
    
    For example:
    
    ```objectscript
    TESTNAMESPACE>WRITE $ZDATE($HOROLOG,3)
    2010-12-03
    ```
    
*   Given a date and time in $H format, the function `$ZDATETIME` returns a string that represents the date and time in your specified format.
    
    For example:
    
    ```objectscript
    TESTNAMESPACE>WRITE $ZDATETIME($HOROLOG,3)
    2010-12-03 14:55:48
    ```
    
*   Given string dates and times in other formats, the functions `$ZDATEH` and `$ZDATETIMEH` convert those to $H format.
    
*   The functions `$ZTIME` and `$ZTIMEH` convert times from and to $H format.
    

## Details of the $H Format

The $H format is a pair of numbers separated by a comma. For example: `54321,12345`

*   The first number is the number of days since December 31st, 1840. That is, day number 1 is January 1st, 1841. This number is always an integer.
    
*   The second number is the number of seconds since midnight on the given day.
    
    Some functions, such as `$NOW()`, provide a fractional part.
    

For additional details, including an explanation of the starting date, see $HOROLOG.
