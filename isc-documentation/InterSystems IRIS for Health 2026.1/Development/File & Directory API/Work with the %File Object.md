# Work with the %File Object

If you want to manipulate a file itself, you need to instantiate a %File object using the `%New()` method of the %Library.File class. The class also provides instance methods that allow you to work with the file.

> **Note:**
> 
> This section provides a few examples of using the %File object for illustrative purposes.
> 
> For simple reading and writing of files, use the %Stream.FileCharacter and %Stream.FileBinary classes, as these provide additional functionality, for example, automatically opening files in the correct mode.

> **Note:**
> 
> If you specify a partial filename or directory name, most of these methods assume that you are referring to an item relative to the directory that contains the default globals database for the namespace you are working in. This directory is referred here as the “default directory.” Any exceptions to this rule are noted.
> 
> Also, these methods treat the file or directory name as case-sensitive only if the underlying operating system treats file and directory names as case-sensitive. That is, file or directory names are case-sensitive on UNIX but not case-sensitive on Windows.

## Create an Instance of a %File Object

To work with a file, you need to instantiate a %File object that represents that file using the `%New()` method. This file may or may not already exist on disk.

The following example instantiates a %File object for the file `export.xml` in the default directory.

```
set fileObj = ##class(%File).%New("export.xml")
```

## Open and Close Files

Once you have instantiated a %File object, you need to open the file using the `Open()` method to read from it or write to it:

```objectscript
USER>set status = fileObj.Open()

USER>write status
1
```

When you open a file, you can specify one or more parameters, for example, `"R"` to allow read access to the file or `"W"` to allow write access to the file. These are the same parameters used for the ObjectScript `OPEN` command. See OPEN Mode Parameters for a list of available parameters and their descriptions.

Use the `Close()` method to close the file:

```objectscript
USER>do fileObj.Close()
```

## Examine Properties of a %File Object

Once you have instantiated the file, you can examine the properties of the file directly.

```objectscript
USER>write fileObj.Name
export.xml
USER>write fileObj.Size
2512
USER>write $zdate(fileObj.DateCreated)
11/18/2020
USER>write $zdate(fileObj.DateModified)
11/18/2020
USER>write fileObj.LastModified
2020-11-18 14:24:38
USER>write fileObj.IsOpen
0
```

Note that `LastModified` is a human readable timestamp, not a date in `$H` format.

The properties `Size`, `DateCreated`, `DateModified`, and `LastModified` are calculated at the time they are accessed. Accessing these properties for a file that does not exist returns `-2`, indicating that the file could not be found.

> **Note:**
> 
> Windows is the only platform that currently tracks the actual created date. Other platforms store the date of the last file status change.

```objectscript
USER>write ##class(%File).Exists("foo.xml")
0
USER>set fooObj = ##class(%File).%New("foo.xml")

USER>write fooObj.Size
-2
```

If a file is open, you can view its canonical name, which is the full path from the root directory, by accessing the `CanonicalName` property.

```objectscript
USER>write fileObj.CanonicalName

USER>set status = fileObj.Open()

USER>write fileObj.IsOpen
1
USER>write fileObj.CanonicalName
c:\intersystems\IRIS\mgr\user\export.xml
```

## Read from Files

To read from a file, you can open the file and then use the `Read()` method.

The following example reads the first 200 characters of `messages.log`.

```objectscript
USER>set messages = ##class(%File).%New(##class(%File).ManagerDirectory() _ "messages.log")

USER>set status =  messages.Open("RU")

USER>write status
1
USER>set text = messages.Read(200, .sc)

USER>write text

*** Recovery started at Mon Dec 09 16:42:01 2019
     Current default directory: c:\intersystems\IRIS\mgr
     Log file directory: .\
     WIJ file spec: c:\intersystems\IRIS\mgr\IR
USER>write sc
1
USER>do messages.Close()
```

To read an entire line from a file, use the `ReadLine()` method, which is inherited from %Library.File’s parent class, %Library.AbstractStream.

The following example reads the first line of `C:\temp\shakespeare.txt`.

```objectscript
USER>set fileObj  = ##class(%File).%New("C:\temp\shakespeare.txt")

USER>set status =  fileObj.Open("RU")

USER>write status
1
USER>set text = fileObj.ReadLine(,.sc)

USER>write text
Shall I compare thee to a summer's day?
USER>write sc
1
USER>do fileObj.Close()
```

## Write to Files

To write to a file, you can open the file and then use the `Write()` or `WriteLine()` methods.

The following example writes a line of text to a new file.

```objectscript
USER>set fileObj = ##class(%File).%New("C:\temp\newfile.txt")

USER>set status = fileObj.Open("WSN")

USER>write status
1
USER>set status = fileObj.WriteLine("Writing to a new file.")

USER>write status
1
USER>write fileObj.Size
24
```

## Rewind Files

After reading from or writing to a file, you may wish to rewind the file using the `Rewind()` method so that you can perform operations from the beginning of the file.

Taking up from where the previous example left off, `fileObj` is now positioned at its end. Rewinding the file and using `WriteLine()` again has the effect of overwriting the file.

```objectscript
USER>set status = fileObj.Rewind()

USER>write status
1
USER>set status = fileObj.WriteLine("Rewriting the file from the beginning.")

USER>write status
1
USER>write fileObj.Size
40
```

Closing the file and reopening it also rewinds the file.

```objectscript
USER>do fileObj.Close()

USER>set status = fileObj.Open("RU")

USER>write status
1
USER>set text = fileObj.ReadLine(,.sc)

USER>write sc
1
USER>write text
Rewriting the file from the beginning.
```

## Clear Files

To clear a file, you can open the file and then use the `Clear()` method. This removes the file from the file system.

The following example clears the file `junk.xml` in the default directory.

```objectscript
USER>write ##class(%File).Exists("junk.xml")
1
USER>set fileObj = ##class(%File).%New("junk.xml")

USER>set status = fileObj.Open()

USER>write status
1
USER>set status = fileObj.Clear()

USER>write status
1
USER>write ##class(%File).Exists("junk.xml")
0
```
