# %File Example

This example shows a sample class that uses several of the %Library.File methods.

In the example class `User.FileTest`, the `ProcessFile()` method accepts an input file and an output file and calls `SetUpInputFile()` and `SetUpOutputFile()` to open the files, one for reading and one for writing. It then reads the input file, line by line, and calls `ProcessLine()` to perform one or more substitutions on the contents of each line, writing the new contents of each line to the output file.

```objectscript
Include %occInclude

Class User.FileTest Extends %Persistent
{

/// Set up the input file
/// 1. Create a file object
/// 2. Open the file for reading
/// 3. Return a handle to the file object
ClassMethod SetUpInputFile(filename As %String) As %File
{
    Set fileObj = ##class(%File).%New(filename)
    Set status = fileObj.Open("RU")
    if $$$ISERR(status) {
        do $system.Status.DisplayError(status)
        quit $$$NULLOREF
    }
    quit fileObj
}

/// Set up the output file
/// 1. Create the directory structure for the file
/// 2. Create a file object
/// 3. Open the file for writing
/// 4. Return a handle to the file object
ClassMethod SetUpOutputFile(filename As %String) As %File
{
    set dir=##class(%File).GetDirectory(filename)
    do ##class(%File).CreateDirectoryChain(dir)
    Set fileObj = ##class(%File).%New(filename)
    Set status = fileObj.Open("WSN")
    If ($SYSTEM.Status.IsError(status)) {
        do $system.Status.DisplayError(status)
        quit $$$NULLOREF
    }
    quit fileObj
}

/// Process one line, using $REPLACE to perform a series of substitutions on the line
ClassMethod ProcessLine(line As %String = "") As %String
{
    set newline = line

    set newline = $REPLACE(newline, "Original", "Jamaican-Style")
    set newline = $REPLACE(newline, "traditional", "innovative")
    set newline = $REPLACE(newline, "orange juice", "lime juice")
    set newline = $REPLACE(newline, "orange zest", "ginger")
    set newline = $REPLACE(newline, "white sugar", "light brown sugar")

    quit newline
}

/// Process an input file, performing a series of substitutions on the content and
/// writing the new content to an output file
ClassMethod ProcessFile(inputfilename As %String = "", outputfilename As %String = "")
{
    // Make sure filenames were passed in
    if (inputfilename="") || (outputfilename="") {
        write !, "ERROR: missing file name"
        quit
    }

    // Open input file for reading
    set inputfile = ..SetUpInputFile(inputfilename)
    if (inputfile = $$$NULLOREF) quit

    // Open output file for writing
    set outputfile = ..SetUpOutputFile(outputfilename)
    if (outputfile = $$$NULLOREF) quit

    // Loop over each line in the input file
    // While not at the end of the file:
    // 1. Read a line from the file
    // 2. Call ProcessLine() to process the line
    // 3. Write the new contents of the line to the output file
    while (inputfile.AtEnd = 0) {
        set line = inputfile.ReadLine(,.status)
         if $$$ISERR(status) {
             do $system.Status.DisplayError(status)
         }
         else {
             set newline = ..ProcessLine(line)
             do outputfile.WriteLine(newline)
         }
    }

    // Close the input and output files
     do inputfile.Close()
     do outputfile.Close()
}

}
```

Call the `ProcessFile()` method as follows:

```objectscript
USER>do ##class(FileTest).ProcessFile("C:\temp\original cranberry sauce.txt",
"C:\temp\jamaican-style cranberry sauce.txt")
```

If the input file, `C:\temp\original cranberry sauce.txt`, contains the following:

```
Original Whole Berry Cranberry Sauce

This traditional whole berry cranberry sauce gets its distinctive flavor
from the freshly squeezed orange juice and the freshly grated orange zest.

2 tsp freshly grated orange zest
1 1/4 cups white sugar
1/4 cup freshly squeezed orange juice
3 cups cranberries (12 oz. package)

1. Grate orange zest into a bowl and set aside.
2. Combine the sugar and orange juice in a saucepan. Bring to a boil over medium-low
heat and stir until sugar is dissolved.
3. Add cranberries and cook over medium-high heat, stirring occasionally, until the
cranberries have popped.
4. Add the cranberry mixture into the bowl with the orange zest, and stir. Let cool.
5. Cover bowl and chill.
```

Then the output file, `C:\temp\jamaican-style cranberry sauce.txt`, will contain the following:

```
Jamaican-Style Whole Berry Cranberry Sauce

This innovative whole berry cranberry sauce gets its distinctive flavor
from the freshly squeezed lime juice and the freshly grated ginger.

2 tsp freshly grated ginger
1 1/4 cups light brown sugar
1/4 cup freshly squeezed lime juice
3 cups cranberries (12 oz. package)

1. Grate ginger into a bowl and set aside.
2. Combine the sugar and lime juice in a saucepan. Bring to a boil over medium-low
heat and stir until sugar is dissolved.
3. Add cranberries and cook over medium-high heat, stirring occasionally, until the
cranberries have popped.
4. Add the cranberry mixture into the bowl with the ginger, and stir. Let cool.
5. Cover bowl and chill.
```
