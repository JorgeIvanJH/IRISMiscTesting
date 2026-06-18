# Work with Files

The %Library.File class provides several class methods that allow you to perform various operations on files. For information on manipulating the files themselves, see Work with the %File Object.

> **Note:**
> 
> If you specify a partial filename or directory name, most of these methods assume that you are referring to an item relative to the directory that contains the default globals database for the namespace you are working in. This directory is referred here as the “default directory.” Any exceptions to this rule are noted.
> 
> Also, these methods treat the file or directory name as case-sensitive only if the underlying operating system treats file and directory names as case-sensitive. That is, file or directory names are case-sensitive on UNIX but not case-sensitive on Windows.

## Copy Files

To copy a file, use the `CopyFile()` method, which returns a boolean value to indicate success or failure.

This method takes four arguments:

1.  `from` — Specifies the name of the source file.
    
2.  `to` — Specifies the name of the target file.
    
3.  `pDeleteBeforeCopy` — Specifies whether to delete the target file, if it exists, before the copy is performed. The default is 0.
    
4.  `return` — Output argument. If negative, contains the error code returned by the operating system in case the method fails.
    

Examples:

The first example, below, copies the file `old.txt` to `new.txt` in the directory `C:\temp`. The second example copies the same file to `new.txt` in the default directory.

```objectscript
USER>write ##class(%File).CopyFile("C:\temp\old.txt", "C:\temp\new.txt", 0, .return)
1
USER>write ##class(%File).CopyFile("C:\temp\old.txt", "new.txt", 0, .return)
1
```

This last example fails with a Windows error code of 2, or “File not found.”

```objectscript
USER>write ##class(%File).CopyFile("foo.txt", "new.txt", 0, .return)
0
USER>write return
-2
```

## Delete Files

To delete a file, use the `Delete()` method, which returns a 1 on success or 0 on failure. This method takes two arguments. The first argument is the name of the file to remove. The second argument is an output argument. If negative, it contains the error code returned by the operating system in case the method fails.

In the first example, below, the method succeeds. The second example fails with a Windows error code of 2, or “File not found.”

```objectscript
USER>write ##class(%File).Delete("C:\temp\myfile.txt", .return)
1
USER>write ##class(%File).Delete("C:\temp\myfile.txt", .return)
0
USER>write return
-2
```

To match wildcards when deleting files, use the `ComplexDelete()` method. The first argument specifies the names of the files to remove. The second argument is an output argument. If negative, it contains the error code returned by the operating system in case the method fails.

The following example deletes all files with the `.out` extension in the `C:\temp` directory.

```objectscript
USER>write ##class(%File).ComplexDelete("C:\temp\*.out", .return)
1
```

## Truncate Files

To truncate a file, use the `Truncate()` method, which returns a 1 on success or 0 on failure. This method takes two arguments. The first argument is the name of the file to truncate. The second argument is an output argument. If negative, it contains the error code returned by the operating system in case the method fails.

If you truncate an existing file, the method deletes the content from the file, but does not remove it from the file system. If you truncate a file that does not exist, the method creates a new empty file.

In the first example, below, the method succeeds. The second example fails with a Windows error code of 5, or “Access is denied.”

```objectscript
USER>write ##class(%File).Truncate("C:\temp\myfile.txt", .return)
1
USER>write ##class(%File).Truncate("C:\no access.txt", .return)
0
USER>write return
-5
```

## Rename Files

To rename a file, use the `Rename()` method, which returns a 1 on success or 0 on failure. This method takes three arguments. The first argument is the name of the file to rename, and the second is the new name. The third argument is an output argument. If negative, it contains the error code returned by the operating system in case the method fails.

In the first example, below, the method succeeds. The second example fails with a Windows error code of 183, or “Cannot create a file when that file already exists.”

```objectscript
USER>write ##class(%File).Rename("C:\temp\oldname.txt", "C:\temp\newname.txt", .return)
1
USER>write ##class(%File).Rename("C:\temp\another.txt", "C:\temp\newname.txt", .return)
0
USER>write return
-183
```

Be careful how you specify paths when using this method, as the following example has the effect of moving `C:\temp\oldname.txt` to the default directory and then renaming it `newname.txt`.

```objectscript
USER>write ##class(%File).Rename("C:\temp\oldname.txt", "newname.txt", .return)
1
```

## Compare Files

To compare two files, use the `Compare()` method, which returns a boolean value of 1 if the two files are identical and 0 otherwise. The method does not have an output argument in which to return a system error code.

In the first example, below, the two files are identical, and the method returns 1. In the second example, the two files are different, so the method returns 0.

```objectscript
USER>write ##class(%File).Compare("C:\temp\old.txt", "C:\temp\new.txt")
1
USER>write ##class(%File).Compare("C:\temp\old.txt", "C:\temp\another.txt")
0
```

If either or both file does not exist, as in the example below, the method also returns 0.

```objectscript
USER>write ##class(%File).Compare("foo.txt", "bar.txt")
0
USER>write ##class(%File).Exists("foo.txt")
0
```

## Generate Temporary Files

To generate a temporary file, use the `TempFilename()` method, which returns the name of the temporary file. This method takes three arguments. The first argument is the desired file extension of the temporary file. The second is a directory in which to generate the temporary file. If not provided, the method generates the file in the OS-provided temporary directory. The third argument is an output argument. If negative, it contains the error code returned by the operating system in case the method fails.

Windows examples:

```objectscript
USER>write ##class(%File).TempFilename("txt")
C:\WINDOWS\TEMP\GATqk8a6.txt
USER>write ##class(%File).TempFilename("txt","C:\temp")
C:\temp\WpSwuLlA.txt
```

Unix examples:

```objectscript
USER>write ##class(%File).TempFilename("", "", .return)
/tmp/filsfHGzc
USER>write ##class(%File).TempFilename("tmp", "/InterSystems/temp", .return)
/InterSystems/temp/file0tnuh.tmp
USER>write ##class(%File).TempFilename("", "/tmp1", .return)

USER>write return
-2
```

In the third example, above, the directory does not exist, and the method fails with system error code 2, or “No such file or directory.”
