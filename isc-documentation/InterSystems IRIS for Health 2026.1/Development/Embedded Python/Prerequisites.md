# Introduction and Prerequisites

Embedded Python allows you to use Python as a native option for programming InterSystems IRIS applications. If you are new to Embedded Python, read Introduction to Embedded Python, and then read this document for a deeper dive into Embedded Python.

While this document will be helpful to anyone who is learning Embedded Python, some level of ObjectScript familiarity will be beneficial to the reader. If you are a Python developer who is new to InterSystems IRIS and ObjectScript, also see the Orientation Guide for Server-Side Programming.

## Installing Embedded Python

The version of Python recommended when using Embedded Python depends on the platform you are running. In most cases, this is the default version of Python for your operating system. On some operating systems, you can override the recommended version of Python using the Flexible Python Runtime feature. See Embedded Python Support for a complete list of operating systems and the corresponding supported version of Python.

If you need to install a version of Python for use with Embedded Python, follow the guidelines in this section.

> **Important:**
> 
> InterSystems IRIS does not support free threading in Python when used with Embedded Python. Do not disable the global interpreter lock (GIL) if you are using Embedded Python. For more information, see Python support for free threading.

Microsoft Windows does not come with a default version of Python, and the InterSystems IRIS installer for Windows no longer installs Python for you. See Flexible Python Runtime Feature for information on setting up Embedded Python for Windows.

Many flavors of UNIX-based operating systems come with Python installed. If you need to install it, use the version recommended for your operating system by your package manager, for example:

*   Ubuntu: `apt install python3`
    
*   Red Hat Enterprise Linux or Oracle Linux: `yum install python3`
    
*   SUSE: `zypper install python3`
    
*   macOS: Install Python using Homebrew.
    
    For example, the following command installs Python 3.11:
    
    `brew install python@3.11`
    
    You should also make sure you are using the current version of OpenSSL:
    
    ```
    brew unlink openssl
    brew install openssl@3
    brew link --force openssl@3
    ```
    
*   AIX: Install Python 3.9.18+ using dnf (dandified yum) from the AIX Toolbox for Open Source Software
    

If you get an error that says “Failed to load python,” it means that you either don’t have Python installed or an unexpected version of Python is detected on your system. Check Embedded Python Support and make sure you have the required version of Python installed, and if necessary, install it or reinstall it using one of the above methods. Or, override the recommended Python version by using the Flexible Python Runtime feature. (Not available on all platforms.)

If you are on a platform that does not support the Flexible Python Runtime feature, your computer has multiple versions of Python installed, and you try to run Embedded Python from the command line, `irispython` will run the first `python3` executable that it detects, as determined by your path environment variable. Make sure that the folders in your path are set appropriately so that the required version of the executable is the first one found. For more information on using the `irispython` command, see Start the Python Shell from the Command Line.

## Required Service

To prevent `IRIS_ACCESSDENIED` errors while running Embedded Python, enable `%Service_Callin`. In the Management Portal, go to `System Administration` > `Security` > `Services`, select `%Service_CallIn`, and check the `Service Enabled` box.

## Flexible Python Runtime Feature

The Flexible Python Runtime Feature allows you to choose which version of Python you want to use with Embedded Python. Flexible Python Runtime is not supported on all operating systems. See Embedded Python Support for a complete list of platforms that support the feature.

On Microsoft Windows, the InterSystems IRIS installer no longer installs a default version of Python. You can install Python from https://www.python.org/downloads/. Make sure to do a custom installation using the standalone installer and install Python for all users.

On other operating systems that support the Flexible Python Runtime feature, you can override the default version of Python. This is useful if you are writing code or using a package that depends on a version of Python other than the default version. You must use a version of Python that is the same or greater than your operating system's default version. For example, Red Hat Enterprise Linux 10 comes with Python 3.12, so on that operating system you must use version 3.12 or higher.

> **Important:**
> 
> InterSystems IRIS does not support free threading in Python when used with Embedded Python. Do not disable the global interpreter lock (GIL) if you are using Embedded Python. For more information, see Python support for free threading.

> **Important:**
> 
> If you are using Windows, you must use the Python standalone installer, not the Python install manager, as you will be installing Python for all users. The Python install manager for Windows does not allow you to install Python for all users.

> **Important:**
> 
> If you need to use OpenSSL 3 with Embedded Python on Microsoft Windows, install Python 3.11 or higher. This installs whatever version of OpenSSL 3 is included with the Python installer. (The version of OpenSSL used by Embedded Python is independent from any other versions used by the Windows operating system or by InterSystems IRIS itself.)
> 
> The AutoML feature of IntegratedML requires Python 3.11 or later.

After installing Python, follow the steps below to configure the version of Python to be used by Embedded Python:

1.  In the Management Portal, go to `System Administration` > `Configuration` > `Additional Settings` > `Advanced Memory`.
    
2.  On the `Advanced Memory Settings` page, in the `PythonRuntimeLibrary` row, click `Edit`.
    
3.  Enter the location of the Python runtime library you want to use.
    
    This location will vary based on your operating system, Python version, and other factors.
    
    Windows example: `C:\Program Files\Python311\python3.dll` (Python 3.11 on Windows)
    
    Linux example: `/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0` (Python 3.11 on Ubuntu 22.04 on the x86 architecture)
    
4.  Click `Save`.
    
5.  On the `Advanced Memory Settings` page, in the `PythonRuntimeLibraryVersion` row, click `Edit`.
    
6.  Enter the major version number of the Python runtime library you want to use.
    
    For example: `3.11` (not `3.11.x`)
    
7.  Click `Save`.
    

For more information, see PythonRuntimeLibrary and PythonRuntimeLibraryVersion.

> **Note:**
> 
> If you install a new version of Python and cannot find the Python runtime library, you may need to install it separately. For example, to install the Python 3.11 runtime library on Ubuntu 22.04: `apt install libpython3.11`.
> 
> On Microsoft Windows, if you find that the Python runtime library is located within your user directory, for example, `C:\Users\<username>\AppData\Local\Programs\Python\Python311`, it indicates that you have installed Python for the current user only. InterSystems recommends installing Python for all users to avoid unexpected results.

For more details on how to configure this feature, including step-by-step examples, see Use the Flexible Python Runtime Feature.
