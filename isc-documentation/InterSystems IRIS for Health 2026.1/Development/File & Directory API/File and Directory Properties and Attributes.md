# File and Directory Properties and Attributes

The %Library.File class provides many class methods that you can use to obtain information about files and directories, or to view or set their properties and attributes.

> **Note:**
> 
> If you specify a partial filename or directory name, most of these methods assume that you are referring to an item relative to the directory that contains the default globals database for the namespace you are working in. This directory is referred here as the “default directory.” Any exceptions to this rule are noted.
> 
> Also, these methods treat the file or directory name as case-sensitive only if the underlying operating system treats file and directory names as case-sensitive. That is, file or directory names are case-sensitive on UNIX but not case-sensitive on Windows.

## Check File and Directory Existence

To find out whether a given file exists, use the `Exists()` method and specify the filename as the argument. For example:

```objectscript
USER>write ##class(%File).Exists("C:\temp\test.html")
1
```

Similarly, to find out whether a given directory exists, use the `DirectoryExists()` method, and specify the directory as the argument. For example:

```objectscript
USER>write ##class(%File).DirectoryExists("C:\temp")
1
```

As noted earlier, these methods treat the file or directory name as case-sensitive on Unix but not case-sensitive on Windows. Also, if you specify a partial filename or directory name, the method assumes that you are referring to a file or directory relative to the directory that contains the default globals database for the namespace you are working in. For example:

```objectscript
USER>write ##class(%File).Exists("iris.dat")
1
```

## View and Set File and Directory Permissions

The %Library.File class provides many class methods that you can use to view or set the permissions of a file or directory.

### See If a File or Directory is Read-Only or Writeable

Given a file or directory name, the `ReadOnly()` method returns 1 if the file or directory is read-only and 0 otherwise:

```objectscript
USER>write ##class(%File).ReadOnly("export.xml")
1
USER>write ##class(%File).ReadOnly("C:\temp")
0
```

Similarly, given a file or directory name, the `Writeable()` method returns 1 if the file or directory is writeable and 0 otherwise:

```objectscript
USER>write ##class(%File).Writeable("export.xml")
0
USER>write ##class(%File).Writeable("C:\temp")
1
```

### Make a File or Directory Read-Only or Writeable (Windows)

To make a file or directory on Windows read-only, use the `SetReadOnly()` method, which returns a boolean value to indicate success or failure. This method takes three arguments, the second of which is omitted in Windows. The first argument is the name of the file or directory. The third argument is an output argument. If negative, it contains the error code returned by the operating system in case the method fails.

In the example below, the call to `SetReadOnly()` successfully changes the file `C:\temp\testplan.pdf` to read-only.

```objectscript
USER>write ##class(%File).ReadOnly("C:\temp\testplan.pdf")
0
USER>write ##class(%File).SetReadOnly("C:\temp\testplan.pdf",,.return)
1
USER>write ##class(%File).ReadOnly("C:\temp\testplan.pdf")
1
```

In the example below, the call to `SetReadOnly()` fails with Windows system error code 5, which means “Access is denied.”

```objectscript
USER>write ##class(%File).SetReadOnly("C:\",,.return)
0
USER>write return
-5
```

To make a file or directory on Windows writeable, use the `SetWriteable()` method. This method takes the same three arguments, the second of which is again omitted in Windows.

```objectscript
USER>write ##class(%File).Writeable("export.xml")
0
USER>write ##class(%File).SetWriteable("export.xml",,.return)
1
USER>write ##class(%File).Writeable("export.xml")
1
```

### Make a File or Directory Read-Only or Writeable (Unix)

On Unix, the methods `SetReadOnly()` and `SetWriteable()` can be also be used, but their behavior is somewhat different, due to the presence of the second parameter. For more information, see %Library.File.SetReadOnly() or %Library.File.SetWriteable() in the class reference.

However in Unix, you may want to specify different permissions for owner, group, and user. For finer control of file and directory permissions, see the section View or Set File and Directory Attributes.

## View and Set File and Directory Attributes

To view or set the attributes of a file or directory at a more detailed level, use the `Attributes()` and `SetAttributes()` methods of %Library.File. File attributes are represented by a sequence of bits that are expressed collectively as an integer. The meaning of the individual bits depends on the underlying operating system.

For a full listing of attribute bits, see %Library.File.Attributes() in the class reference.

For tips on working with strings of attribute bits, see Manipulating Bitstrings Implemented as Integers.

### View File and Directory Attributes

The `Attributes()` method of %Library.File expects the file or directory name as the argument and returns a sequence of attribute bits expressed as an integer.

The following examples were run on a Windows system:

```objectscript
USER>write ##class(%File).Attributes("iris.dat")
32
USER>write ##class(%File).Attributes("C:\temp")
16
USER>write ##class(%File).Attributes("secret.zip")
35
```

In the first example, 32 means that `iris.dat` is an archive file. In the second example, 16 means that `C:\temp` is a directory. In the third example, more than one bit is set, and 35 indicates that `secret.zip` is an archive (32) that is hidden (2) and read-only (1). Adding 32 + 2 + 1 = 35.

The following example was run on a Unix system:

```
write ##class(%File).Attributes("/home")
16877
```

In this example, 16877 means that `/home` is a directory (16384) with read (256), write (128), and execute (64) permission for owner; read (32) and execute (8) permission for group; and read (4) and execute (1) permission for others. Adding 16384 + 256 + 128 + 64 + 32 + 8 + 4 + 1 = 16877.

### Set File and Directory Attributes

Conversely, the `SetAttributes()` method sets a file or directory’s attributes (where possible) and returns a boolean value to indicate success or failure. This method takes three arguments. The first argument is the name of the file or directory. The second argument is an integer that represents the desired attributes you would like the file or directory to have. The third argument is an output argument. If negative, it contains the error code returned by the operating system in case the method fails.

The following example, on Windows, makes the file `C:\temp\protectme.txt` read-only by setting the 1 bit:

```objectscript
USER>write ##class(%File).Attributes("C:\temp\protectme.txt")
32
USER>write ##class(%File).SetAttributes("C:\temp\protectme.txt",33,.return)
1
USER>write ##class(%File).Attributes("C:\temp\protectme.txt")
33
```

The following example, on Unix, changes permissions on the file `myfile` in the default directory from 644 to full permissions (777):

```objectscript
USER>write ##class(%File).Attributes("myfile")
33188
USER>write ##class(%File).SetAttributes("myfile",33279,.return)
1
USER>write ##class(%File).Attributes("myfile")
33279
```

The desired attribute value is calculated by adding the value for a regular file (32768) with the masks for owner (448), group (56), and others (7).

## View Other File and Directory Properties

Other class methods of %Library.File allow you to examine various other properties of files and directories.

The `GetFileDateCreated()` method returns the date a file or directory was created in `$H` format:

```objectscript
USER>write $zdate(##class(%File).GetFileDateCreated("stream"))
12/09/2019
```

> **Note:**
> 
> Windows is the only platform that currently tracks the actual created date. Other platforms store the date of the last file status change.

The `GetFileDateModified()` method returns the date a file or directory was modified in `$H` format:

```objectscript
USER>write $zdate(##class(%File).GetFileDateModified("iris.dat"))
08/20/2020
```

The `GetFileSize()` method returns the size of a file, in bytes:

```objectscript
USER>write ##class(%File).GetFileSize("export.xml")
2512
```

The `GetDirectorySpace()` method returns the amount of free space and total space in a drive or directory. The space can be returned in bytes, MB (the default), or GB, depending on the value of the fourth argument, which can be 0, 1, or 2. In this example, 2 indicates that the space is returned in GB:

```objectscript
USER>set status = ##class(%File).GetDirectorySpace("C:", .FreeSpace, .TotalSpace, 2)

USER>write FreeSpace
182.87
USER>write TotalSpace
952.89
```

On Windows, if you pass a directory name to this method, the amount of space returned is for the entire drive.

For the `GetDirectorySpace()` method, any error status returned is the operating system-level error. In the example below, Windows system error code 3 indicates “The system cannot find the path specified.”

```objectscript
USER>set status = ##class(%File).GetDirectorySpace("Q:", .FreeSpace, .TotalSpace, 2)

USER>do $system.Status.DisplayError(status)

ERROR #83: Error code = 3
```
