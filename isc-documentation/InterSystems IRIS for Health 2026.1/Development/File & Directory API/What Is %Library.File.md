# What Is %Library.File?

The %Library.File class (%File for short) provides an extensive API for working with files and directories. This document describes the main features of this API, for example, listing directory and drive contents; creating, copying, and deleting directories and files; setting and getting file attributes; and reading and writing files. For a canonical list of properties, methods, and queries, see the class reference.

If you specify a partial filename or directory name when using %File, most of its methods assume that you are referring to an item relative to the directory that contains the default globals database for the namespace you are working in. This directory is referred to in this document as the “default directory.” Any exceptions to this rule are noted where applicable.

Also, %File treats the file or directory name as case-sensitive only if the underlying operating system treats file and directory names as case-sensitive. That is, file or directory names are case-sensitive on Unix but not case-sensitive on Windows.
