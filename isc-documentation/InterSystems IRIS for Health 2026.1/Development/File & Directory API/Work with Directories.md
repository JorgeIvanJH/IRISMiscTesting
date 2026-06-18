# Work with Directories

The %Library.File class provides several class methods that allow you to perform various operations on directories.

> **Note:**
> 
> If you specify a partial filename or directory name, most of these methods assume that you are referring to an item relative to the directory that contains the default globals database for the namespace you are working in. This directory is referred here as the “default directory.” Any exceptions to this rule are noted.
> 
> Also, these methods treat the file or directory name as case-sensitive only if the underlying operating system treats file and directory names as case-sensitive. That is, file or directory names are case-sensitive on UNIX but not case-sensitive on Windows.

## Create Directories

To create a directory, use the `CreateDirectory()` method, which returns a boolean value to indicate success or failure. This method takes two arguments. The first argument is the name of the directory to create. The second argument is an output argument. If negative, it contains the error code returned by the operating system in case the method fails.

If `C:\temp` already exists, the following command fails with Windows system error code 183, which means “Cannot create a file when that file already exists.”

```objectscript
USER>write ##class(%File).CreateDirectory("C:\temp", .return)
0
USER>write return
-183
```

If `C:\temp` already exists, but `C:\temp\test` does not exist, the following command fails because `CreateDirectory()` creates, at most, the last directory in the given directory path. So the returned Windows system error code is 3, or “The system cannot find the path specified.”

```objectscript
USER>write ##class(%File).CreateDirectory("C:\temp\test\this", .return)
0
USER>write return
-3
```

The following example succeeds with Windows system code 0, or “The operation completed successfully.”

```objectscript
USER>write ##class(%File).CreateDirectory("C:\temp\test", .return)
1
USER>write return
0
```

The similar `CreateNewDir()` method creates a new directory within the specified parent directory. This method takes three arguments. The first argument is the name of the parent directory. The second argument is the name of the directory to create. The third argument is an output argument. If negative, it contains the error code returned by the operating system in case the method fails.

The first example, below, creates a directory called `newdir` in the parent directory `C:\temp`. The second example creates a new directory called `newdir` in the default directory.

```objectscript
USER>write ##class(%File).CreateNewDir("C:\temp", "newdir", .return)
1
USER>write ##class(%File).CreateNewDir("", "newdir", .return)
1
```

Another related method, `CreateDirectoryChain()`, creates all the directories on the given directory path (if possible).

The first example, below, creates three nested directories in the parent directory `C:\temp`. The second example creates three nested directories in the default directory.

```objectscript
USER>write ##class(%File).CreateDirectoryChain("C:\temp\one\two\three", .return)
1
USER>write ##class(%File).CreateDirectoryChain("one\two\three", .return)
1
```

## Copy Directories

To copy a directory, use the `CopyDir()` method, which returns a boolean value to indicate success or failure.

This method takes five arguments:

1.  `pSource` — Specifies the name of the source directory.
    
2.  `pTarget` — Specifies the name of the target directory.
    
3.  `pOverlay` — Specifies whether to overwrite the target directory, if it exists. The default is 0.
    
4.  `pCreated` — Output argument that contains the number of files or directories created during the copy process.
    
5.  `pDeleteBeforeCopy` — Specifies whether to delete any file that exists in the target directory before the copy is performed. The default is 0.
    

Partial directory names for either `pSource` or `pTarget` are calculated relative to the directory that contains the default globals database for the namespace you are working in.

Unlike the directory creation methods, `CopyDir()` does not have an output argument in which to return a system error code.

In the first example, below, the copy operation is successful, and 46 files and directories are copied from `C:\temp` to `C:\temp2`. In the second example, the copy operation is successful, and 46 files and directories are copied from `C:\temp` to a directory `temp2` within the default directory.

```objectscript
USER>write ##class(%File).CopyDir("C:\temp", "C:\temp2", 0, .pCreated, 0)
1
USER>write pCreated
46
USER>write ##class(%File).CopyDir("C:\temp", "temp2", 0, .pCreated, 0)
1
USER>write pCreated
46
```

In the final example, below, `pOverlay` is set to 0, so the copy fails due to the target directory already existing.

```objectscript
USER>write ##class(%File).CopyDir("C:\temp", "C:\temp2", 0, .pCreated, 0)
0
USER>write pCreated
0
```

## Delete Directories

To delete a non-empty directory, use the `RemoveDirectory()` method, which returns a 1 on success or 0 on failure. This method takes two arguments. The first argument is the name of the directory to remove. The second argument, which is an output argument, contains the error code returned by the operating system in case the method fails.

In the first example, below, the method succeeds. The second example fails with a Windows error code of 145, or “Directory not empty.”

```objectscript
USER>write ##class(%File).RemoveDirectory("C:\temp2\newdir", .return)
1
USER>write ##class(%File).RemoveDirectory("C:\temp2", .return)
0
USER>write return
-145
```

To delete a directory, including any subdirectories, use the `RemoveDirectoryTree()` method, which returns a 1 on success or 0 on failure. Unlike the `RemoveDirectory()` method, `RemoveDirectoryTree()` does not have an output argument in which to return a system error code.

`RemoveDirectoryTree()` succeeds even if the directory and any subdirectories are not empty.

```objectscript
USER>write ##class(%File).RemoveDirectoryTree("C:\temp2")
1
```

## Rename Directories

To rename a directory, use the `Rename()` method, which returns a 1 on success or 0 on failure. This method takes three arguments. The first argument is the name of the directory to rename, and the second is the new name. The third argument is an output argument. If negative, it contains the error code returned by the operating system in case the method fails.

Using `Rename()` to rename a directory works only if the directory is on the same file system as you are working on.

In the first example, below, the method succeeds. In the second example, `C:\nodir` does not exist, so the method fails with a Windows error code of 3, or “The system cannot find the path specified.”

```objectscript
USER>write ##class(%File).Rename("C:\temp\oldname", "C:\temp\newname", .return)
1
USER>write ##class(%File).Rename("C:\nodir\oldname", "C:\nodir\newname", .return)
0
USER>write return
-3
```

Be careful how you specify paths when using this method, as the following example has the effect of moving `C:\temp\oldname` to the default directory and then renaming it `newname`.

```objectscript
USER>write ##class(%File).Rename("C:\temp\oldname", "newname", .return)
1
```
