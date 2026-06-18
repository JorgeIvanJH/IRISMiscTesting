# File and Directory Names

The %Library.File class provides several class methods that you can use to work with file and directory names. In most cases, the files and directories do not need to exist in order to use these methods.

> **Note:**
> 
> If you specify a partial filename or directory name, most of these methods assume that you are referring to an item relative to the directory that contains the default globals database for the namespace you are working in. This directory is referred here as the “default directory.” Any exceptions to this rule are noted.
> 
> Also, these methods treat the file or directory name as case-sensitive only if the underlying operating system treats file and directory names as case-sensitive. That is, file or directory names are case-sensitive on UNIX but not case-sensitive on Windows.

## Get File and Directory Names

The %Library.File class provides class methods that you can use to obtain parts of file and directory names.

Given a full pathname, use `GetDirectory()` and `GetFilename()` to get the directory and the short filename respectively. For this method, partial directory names are not permitted.

```objectscript
USER>set filename = "C:\temp\samples\sample.html"

USER>write ##class(%File).GetDirectory(filename)
C:\temp\samples\
USER>write ##class(%File).GetFilename(filename)
sample.html
```

Given a filename, use `CanonicalFilename()` to get the full path from the root:

```objectscript
USER>set filename = "iris.dat"

USER>write ##class(%File).CanonicalFilename(filename)
c:\intersystems\IRIS\mgr\user\iris.dat
USER>write ##class(%File).CanonicalFilename("foo.dat")
```

If the file cannot be opened, the `CanonicalFilename()` method returns an empty string.

Given a directory name, use `ComputeFullDBDir()` to construct the canonical form of the directory name.

```objectscript
USER>write ##class(%File).ComputeFullDBDir("foodirectory")
c:\intersystems\IRIS\mgr\user\foodirectory\
```

Given a directory name, use `GetDirectoryLength()` and `GetDirectoryPiece()` to get the number of pieces in the directory and a specific piece, respectively. Pieces can be delimited by slash (/) or backslash (\), depending on the operating system.

```objectscript
USER>set dir = "C:\temp\samples"

USER>write ##class(%File).GetDirectoryLength(dir)
3
USER>write ##class(%File).GetDirectoryPiece(dir,1)
C:
```

Given a filename or directory name, use `ParentDirectoryName()` to get the parent directory.

```objectscript
USER>set dir = "stream"

USER>write ##class(%File).ParentDirectoryName(dir)
C:\InterSystems\IRIS\mgr\user\
```

## Normalize File and Directory Names

The %Library.File class provides class methods that return normalized file and directory names (following the naming rules of the operating system on which the server is running). These are useful when you are creating new file and directory names by appending name pieces to existing names.

Given a filename, `NormalizeFilename()` returns the normalized filename.

Given a directory name, `NormalizeDirectory()` returns the normalized directory name.

The methods return normalized names that are appropriate for use on the underlying operating system and will attempt to normalize slash (/) or backslash (\) path delimiters.

Windows examples:

```objectscript
USER>set filename = "C:\temp//samples\myfile.txt"

USER>write ##class(%File).NormalizeFilename(filename)
C:\temp\samples\myfile.txt
USER>write ##class(%File).NormalizeDirectory("stream")
C:\InterSystems\IRIS\mgr\user\stream\
```

Unix examples:

```objectscript
USER>set filename = "/tmp//samples/myfile.txt"

USER>write ##class(%File).NormalizeFilename(filename)
/tmp/samples/myfile.txt
USER>write ##class(%File).NormalizeDirectory("stream")
/InterSystems/IRIS/mgr/user/stream/
```

Add a second argument when calling one of these methods to normalize the directory name or filename relative to a specified directory. The directory must exist.

Windows examples:

```objectscript
USER>write ##class(%File).NormalizeFilename("myfile.txt", "C:\temp\samples")
C:\temp\samples\myfile.txt
USER>write ##class(%File).NormalizeDirectory("stream", "")
C:\InterSystems\IRIS\mgr\user\stream\
```

Unix examples:

```objectscript
USER>write ##class(%File).NormalizeFilename("myfile.txt", "/tmp/samples")
/tmp/samples/myfile.txt
USER>write ##class(%File).NormalizeDirectory("stream", "")
/InterSystems/IRIS/mgr/user/stream/
```

The `SubDirectoryName()` method is similar to the two-argument form of `NormalizeDirectory()`, except the order of the arguments is reversed. Also the directory does not need to exist. Pass a `1` in the third argument to add a trailing delimiter, or a `0` to omit it (the default).

Windows examples:

```objectscript
USER>write ##class(%File).SubDirectoryName("C:\foobar", "samples")
C:\foobar\samples
USER>write ##class(%File).SubDirectoryName("", "stream", 1)
C:\InterSystems\IRIS\mgr\user\stream\
```

Unix examples:

```objectscript
USER>write ##class(%File).SubDirectoryName("/foobar", "samples")
/foobar/samples
USER>write ##class(%File).SubDirectoryName("", "stream", 1)
/InterSystems/IRIS/mgr/user/stream/
```

## Handle File and Directory Names with Spaces

For file names and directory names that include spaces, use `NormalizeFilenameWithSpaces()`, which handles spaces in pathnames as appropriate to the host platform. Unlike `NormalizeFilename()` and `NormalizeDirectory()`, this method takes only one argument and cannot normalize a file or directory name relative to another directory, nor does it normalize partial file or directory names relative to the default directory.

On Windows systems, if the pathname contains spaces, and the file or directory does not exist, the method returns the pathname enclosed in double quotes. If the pathname contains spaces, and the file or directory does exist, the method returns the short form of the pathname. If the pathname does not contain spaces, the method returns the pathname unaltered.

```objectscript
USER>write ##class(%File).NormalizeFilenameWithSpaces("C:\temp\nonexistant folder")
"C:\temp\nonexistant folder"
USER>write ##class(%File).NormalizeFilenameWithSpaces("C:\temp\existant folder")
C:\temp\EXISTA~1
USER>write ##class(%File).NormalizeFilenameWithSpaces("iris.dat")
iris.dat
```

For further details, see %Library.File.NormalizeFilenameWithSpaces() in the class reference.

On Unix systems, if the pathname contains spaces, the method returns the pathname enclosed in double quotes. If the pathname does not contain spaces, the method returns the pathname unaltered.

```objectscript
USER>write ##class(%File).NormalizeFilenameWithSpaces("/InterSystems/my directory")
"/InterSystems/my directory"
USER>write ##class(%File).NormalizeFilenameWithSpaces("iris.dat")
iris.dat
```

## Construct and Deconstruct File and Directory Names

The %Library.File class provides class methods that let you construct a filename from an array of paths or deconstruct a filename into an array of paths.

Given an array of paths, `Construct()` assembles the paths and returns the filename. The filename constructed is appropriate to the server platform. Calling this method without arguments returns the default directory.

Given a filename, `Deconstruct()` disassembles the filename and returns an array of paths. The contents of the array is appropriate to the server platform.

The following Windows example passes an array `dirs` to `Construct()`. The empty string in the last array location indicates that the filename returned should terminate in a `\`.

```objectscript
USER>zwrite dirs
dirs=4
dirs(1)="C:"
dirs(2)="Temp"
dirs(3)="samples"
dirs(4)=""
USER>write ##class(%File).Construct(dirs...)
C:\Temp\samples\
```

The following Unix example calls `Construct()` without arguments. The method returns the default directory.

```objectscript
USER>set default = ##class(%File).Construct()

USER>write default
/InterSystems/IRIS/mgr/user
```

The following Unix example calls `Deconstruct()`, which takes the paths in the variable `default` and stores them in array `defaultdir`.

```objectscript
USER>do ##class(%File).Deconstruct(default, .defaultdir)

USER>zwrite defaultdir
defaultdir=4
defaultdir(1)="InterSystems"
defaultdir(2)="IRIS"
defaultdir(3)="mgr"
defaultdir(4)="user"
```

## Get the System Manager Directory

Use the `ManagerDirectory()` method to get the fully qualified name of the `installdir/mgr` directory. For example:

```objectscript
USER>write ##class(%File).ManagerDirectory()
C:\InterSystems\IRIS\mgr\
```
