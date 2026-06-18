# Query Directories and Drives

The %Library.File class provides class queries that can query drives and directories.

## List the Contents of a Directory

The `FileSet()` class query lists the contents of a directory. This query accepts the following parameters, in order:

1.  `directory` — Specifies the name of the directory to examine.
    
2.  `wildcards` — Specifies the filename pattern to match, if any. For details, see the section “Wildcards” in the reference for $ZSEARCH.
    
3.  `sortby` — Specifies how to sort the results. Use one of the following values:
    
    *   `Name` — Name of the file (the default)
        
    *   `Type` — Item type
        
    *   `DateCreated` — Date and time when the file was created
        
    *   `DateModified` — Date and time when the file was last modified
        
    *   `Size` — File size
        
4.  `includedirs` — Specifies how to handle directories within the given directory. If this argument is true (1), the query returns all directories before any files, and the directory names ignore the `wildcards` argument. If this argument is false (0), the `wildcards` argument applies to both files and directories. The default is 0.
    
5.  `delimiter` — Specifies the delimiter between wildcards in the `wildcards` argument. The default is `;`
    

The result set returned by this query provides the following fields:

*   Name — Full pathname of the item.
    
*   Type — Type of the item: `F` indicates a file, `D` indicates a directory, and `S` indicates a symbolic link.
    
*   Size — File size, in bytes. This field is null for directories and symbolic links.
    
*   DateCreated — Date and time, in the format yyyy-mm-dd hh:mm:ss, when the item was created.
    
*   DateModified — Date and time, in the format yyyy-mm-dd hh:mm:ss, when the item was last modified.
    
*   ItemName — Short name of the item. For a file, this is the filename alone, without the directory. For a directory, this is just the last part of the directory path.
    

> **Note:**
> 
> Windows is the only platform that currently tracks the actual created date. Other platforms store the date of the last file status change.

Here is a simple example that uses this class query:

```objectscript
ClassMethod ShowDir(dir As %String = "", wildcard As %String = "", sort As %String = "Name")
{
  set stmt = ##class(%SQL.Statement).%New()
  set status = stmt.%PrepareClassQuery("%File", "FileSet")
  if $$$ISERR(status) {write "%Prepare failed:" do $SYSTEM.Status.DisplayError(status) quit}

  set rset = stmt.%Execute(dir, wildcard, sort)
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  while rset.%Next()
  {
    write !, rset.%Get("Name")
    write " ", rset.%Get("Type")
    write " ", rset.%Get("Size")
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
}
```

Assuming the method is within the `User.FileTest` class, running this method from the Terminal on a specified directory, filtering for log files, and sorting by file size gives something like:

```objectscript
USER>do ##class(FileTest).ShowDir("C:\InterSystems\IRIS\mgr", "*.log", "Size")

C:\InterSystems\IRIS\mgr\alerts.log F 380
C:\InterSystems\IRIS\mgr\FeatureTracker.log F 730
C:\InterSystems\IRIS\mgr\journal.log F 743
C:\InterSystems\IRIS\mgr\ensinstall.log F 12577
C:\InterSystems\IRIS\mgr\iboot.log F 40124
C:\InterSystems\IRIS\mgr\SystemMonitor.log F 483865
C:\InterSystems\IRIS\mgr\messages.log F 4554535
```

For another example, the following method examines a directory and all its subdirectories, recursively, and writes out the name of each file that it finds:

```objectscript
ClassMethod ShowFilesInDir(directory As %String = "")
{
  set stmt = ##class(%SQL.Statement).%New()
  set status = stmt.%PrepareClassQuery("%File", "FileSet")
  if $$$ISERR(status) {write "%Prepare failed:" do $SYSTEM.Status.DisplayError(status) quit}

  set rset = stmt.%Execute(directory)
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  while rset.%Next()
  {
    set name = rset.%Get("Name")
    set type = rset.%Get("Type")

    if (type = "F") {
      write !, name
     } elseif (type = "D"){
      do ..ShowFilesInDir(name)
    }
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
}
```

Running this method in the Terminal on the default directory gives something like:

```objectscript
USER>do ##class(FileTest).ShowFilesInDir()

C:\InterSystems\IRIS\mgr\user\IRIS.DAT
C:\InterSystems\IRIS\mgr\user\iris.lck
C:\InterSystems\IRIS\mgr\user\userenstemp\IRIS.DAT
C:\InterSystems\IRIS\mgr\user\userenstemp\iris.lck
C:\InterSystems\IRIS\mgr\user\usersecondary\IRIS.DAT
C:\InterSystems\IRIS\mgr\user\usersecondary\iris.lck
```

## List the Drives or Mounted File Systems

The `DriveList()` class query lists the available drives (on Windows) or the mounted file systems (on UNIX). This query accepts one parameter:

1.  fullyqualified — If this argument is 1, the query includes a trailing backslash on each Windows drive name. This argument has no effect on other platforms. The default is 0.
    

The result set returned by this query provides one field:

*   Drive — Name of a drive (on Windows) or name of a mounted file system (on UNIX).
    

The following example shows how you might use this query:

```
ClassMethod ShowDrives()
{
  set stmt = ##class(%SQL.Statement).%New()
  set status = stmt.%PrepareClassQuery("%File","DriveList")
  if $$$ISERR(status) {write "%Prepare failed:" do $SYSTEM.Status.DisplayError(status) quit}

  set rset = stmt.%Execute(1)
  if (rset.%SQLCODE '= 0) {write "%Execute failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}

  while rset.%Next()
  {
    write !, rset.%Get("Drive")
  }
  if (rset.%SQLCODE < 0) {write "%Next failed:", !, "SQLCODE ", rset.%SQLCODE, ": ", rset.%Message quit}
}
```

Again assuming the method is within the `User.FileTest` class, running the method in the Terminal gives something like:

```objectscript
USER>do ##class(FileTest).ShowDrives()

c:\
x:\
```
