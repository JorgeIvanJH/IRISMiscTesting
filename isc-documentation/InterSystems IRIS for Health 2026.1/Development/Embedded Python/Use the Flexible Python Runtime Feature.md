# Use the Flexible Python Runtime Feature

## Overview of the Flexible Python Runtime Feature

When you run Embedded Python, InterSystems IRIS expects that you are using the default version of Python for your operating system. However, Microsoft Windows does not come with Python by default, and the current InterSystems IRIS installer on Windows does not install Python for you. Also, there may be times when you might want to upgrade to a later version of Python or switch to an alternate distribution like Anaconda.

The Flexible Python Runtime feature enables you to choose what version of Python you want to use with Embedded Python in InterSystems IRIS.

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

> **Note:**
> 
> The Flexible Python Runtime feature is not supported on all operating systems. See Embedded Python Support for a complete list of platforms that support the feature.

Preparing to use the Flexible Python Runtime feature involves three basic steps:

1.  Install the version of Python you want to use.
    
2.  Set the `PythonRuntimeLibrary` configuration setting to specify the location of the Python runtime library to use when running Embedded Python.
    
    This location will vary based on your operating system, Python version, and other factors.
    
    Windows example: `C:\Program Files\Python311\python3.dll` (Python 3.11 on Windows)
    
    Linux example: `/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0` (Python 3.11 on Ubuntu 22.04 on the x86 architecture)
    
    See PythonRuntimeLibrary for more information.
    
3.  Set the `PythonRuntimeLibraryVersion` configuration setting to specify the version number of the Python runtime library to use when running Embedded Python. Use the major version only.
    
    For example: `3.11` (not `3.11.x`)
    
    See PythonRuntimeLibraryVersion for more information.
    
4.  Ensure that the `sys.path` variable in Embedded Python includes the correct directories needed to import Python packages.
    
    See Embedded Python and sys.path.
    

See the following sections for step-by-step instructions for some common Flexible Python Runtime scenarios:

*   Example: Python 3.11 on Windows
    
*   Example: Python 3.11 on Ubuntu 22.04
    
*   Example: Anaconda on Windows
    
*   Example: Anaconda on Ubuntu 22.04
    

### Embedded Python and sys.path

After you launch Embedded Python, it uses the directories contained in the `sys.path` variable to locate any Python packages you want to import.

When you use Embedded Python with the default version of Python for your operating system, or on Microsoft Windows, `sys.path` already includes the correct directories, for example.

*   `<installdir>/lib/python` (Python packages reserved for InterSystems IRIS)
    
*   `<installdir>/mgr/python` (Python packages installed by the user)
    
*   Global package repositories for the default Python version
    
    This location will vary based on your operating system, Python version, and other factors.
    
    Windows example: `C:\Program Files\Python311\Lib\site-packages` (Python 3.11 on Windows)
    
    Linux example: `/usr/local/lib/python3.10/dist-packages` (Python 3.10 on Ubuntu 22.04)
    

On Microsoft Windows with Python 3.11, `sys.path` in Embedded Python might look something like this:

```objectscript
USER>do ##class(%SYS.Python).Shell()

Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
Type quit() or Ctrl-D to exit this shell.
>>> import sys
>>> sys.path
['C:\\Program Files\\Python311\\python311.zip', 'C:\\Program Files\\Python311\\DLLs',
'C:\\Program Files\\Python311\\Lib', 'c:\\intersystems\\IRIS\\bin',
'c:\\intersystems\\IRIS\\mgr\\python', 'c:\\intersystems\\IRIS\\lib\\python',
'C:\\Program Files\\Python311', 'C:\\Program Files\\Python311\\Lib\\site-packages']
```

> **Important:**
> 
> On Microsoft Windows, if `sys.path` contains a directory that is within your user directory, such as `C:\Users\<username>\AppData\Local\Programs\Python\Python311`, it indicates that you have installed Python for the current user only. InterSystems recommends installing Python for all users to avoid unexpected results.

On Ubuntu 22.04, with the default version of Python (3.10), `sys.path` in Embedded Python might look something like this:

```objectscript
USER>do ##class(%SYS.Python).Shell()

Python 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] on linux
Type quit() or Ctrl-D to exit this shell.
>>> import sys
>>> sys.path
['/usr/lib/python310.zip', '/usr/lib/python3.10', '/usr/lib/python3.10/lib-dynload', '/InterSystems/IRIS/lib/python',
'/InterSystems/IRIS/mgr/python', '/usr/local/lib/python3.10/dist-packages', '/usr/lib/python3/dist-packages',
'/usr/lib/python3.10/dist-packages']
```

> **Important:**
> 
> On Linux, if `sys.path` contains a directory that is within your home directory, such as `/home/<username>/.local/lib/python3.10/site-packages`, it could indicate that you have installed packages in your local package repository. For example, if you install a package without the `--target` attribute (and without using `sudo`), Python will install it into the local package repository within your home directory. If any other user tries to import the package, it will fail.
> 
> Although InterSystems recommends using the `--target <installdir>/mgr/python` option, installing packages using `sudo` and omitting the `--target` attribute installs the packages into the global package repository. These packages can also be imported by any user.

If you switch to an alternate distribution of Python, InterSystems IRIS may not know where its package repositories are located. InterSystems IRIS provides you with a tool that can help you tailor your `sys.path` to include the correct directories, namely the `iris_site.py` file in the directory `<installdir>/lib/python`.

The `iris_site.py` file covers the most common use cases, but if you need to customize the file, copy it to the `<installdir>/mgr/python` directory. This will ensure that your configuration is not wiped out when you upgrade to a later version of InterSystems IRIS. Read the comments in the file for helpful tips.

If you are using Anaconda, InterSystems IRIS comes with examples you can edit to your needs. For example, if you are using Anaconda on Linux, copy the file `iris_site_anaconda_ubuntu_linux_example.py` from the `<installdir>/lib/python` directory to the `<installdir>/mgr/python` directory and rename it `iris_site.py`. Then edit the path names in the file to match your installation.

For Anaconda on Ubuntu 22.04, for example, edit the last few lines of your `iris_site.py` file to substitute your actual username:

```
    sys.path = sys.path + __sitegetsitepackages(['/home/<username>/anaconda3'])
    sys.path = sys.path + ["/home/<username>/anaconda3/lib/python3.11/lib-dynload"]
    sys.path = ["/home/<username>/anaconda3/lib/python3.11"] + sys.path
    sys.path = ["/home/<username>/anaconda3/lib/python311.zip"] + sys.path
```

With the `iris_site.py` above, `sys.path` in Embedded Python might look something like this:

```objectscript
USER>do ##class(%SYS.Python).Shell()

Python 3.11.7 (main, Dec 15 2023, 18:24:52) [GCC 11.2.0] on linux
Type quit() or Ctrl-D to exit this shell.
>>> import sys
>>> sys.path
['/home/<username>/anaconda3/lib/python311.zip', '/home/<username>/anaconda3/lib/python3.11',
'/home/<username>/anaconda3/lib/python311.zip', '/home/<username>/anaconda3/lib/python3.11',
'/home/<username>/anaconda3/lib/python3.11/lib-dynload', '/InterSystems/IRIS/mgr/python',
'/InterSystems/IRIS/lib/python', '/home/<username>/anaconda3/lib/python3.11/site-packages',
'/home/<username>/anaconda3/lib/python3.11/lib-dynload']
```

Again, the `<username>` in the above example will reflect your actual username.

It may take you a few iterations to get your `sys.path` correct for Flexible Python Runtime. It may be helpful to launch Python outside of InterSystems IRIS and compare its `sys.path` with the `sys.path` inside Embedded Python to make sure you have all of the expected directories.

> **Note:**
> 
> Changes to the `PythonRuntimeLibrary` and `PythonRuntimeLibraryVersion` configuration settings or `iris_site.py` take effect on starting a new session. Restarting InterSystems IRIS is not required.

### Check Python Version Information

If you are using the Flexible Python Runtime feature, it can be useful to check the version of Python that Embedded Python is using versus the default version that your system is using. An easy way to do this is by calling the `GetPythonInfo()` method of the %SYS.Python class.

The following example, on Ubuntu 22.04 on the x86 architecture, shows that the Python runtime library being used is `/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0`, the running version of Embedded Python is `3.11.0rc1`, and the system version is `3.10.12`.

```objectscript
USER>do ##class(%SYS.Python).GetPythonInfo(.info)

USER>zw info
info("AllowNonSystemPythonForIntegratedML")=0
info("CPF_PythonPath")=""
info("CPF_PythonRuntimeLibrary")="/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0"
info("CPF_PythonRuntimeLibraryVersion")=3.11
info("IRISInsidePython")=0
info("PythonInsideIRIS")=2
info("RunningLibrary")="/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0"
info("RunningVersion")="3.11.0rc1 (main, Aug 12 2022, 10:02:14) [GCC 11.2.0]"
info("SystemPath")="/usr/lib/python3.10/config-3.10-x86_64-linux-gnu"
info("SystemVersion")="3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0]"
info("SystemVersionShort")="3.10.12"
info("iris_site.py_platform")="lnxubuntu2204x64"
```

This information will vary based on your operating system, Python version, and other factors.

## Flexible Python Runtime Example: Python 3.11 on Windows

Microsoft Windows does not come with Python by default, and the current InterSystems IRIS installer for Windows does not install Python for you. You must download and install Python yourself.

> **Important:**
> 
> If you need to use OpenSSL 3 with Embedded Python, note that installing Python 3.11 or higher also installs OpenSSL 3. The version of OpenSSL used by Embedded Python is independent from any other versions used by the Windows operating system or by InterSystems IRIS itself.
> 
> The example below shows how to determine the version of OpenSSL used by Embedded Python:
> 
> ```objectscript
> USER>do ##class(%SYS.Python).Shell()
> 
> Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
> Type quit() or Ctrl-D to exit this shell.
> >>> import ssl
> >>> ssl.OPENSSL_VERSION
> 'OpenSSL 3.0.13 30 Jan 2024'
> ```

The following example shows how to install and use Python 3.11 with InterSystems IRIS on Windows:

1.  Download the Python 3.11 standalone installer from https://www.python.org/downloads/.
    
    > **Important:**
    > 
    > You must use the Python standalone installer, not the Python install manager, as you will be installing Python for all users. The Python install manager for Windows does not allow you to install Python for all users.
    
2.  Launch the Python installer.
    
3.  Click `Customize Installation`.
    
4.  Click `Next` until you reach the `Advanced Options` screen.
    
5.  Select the option to `Install Python for All Users`.
    
6.  Click `Install`.
    
7.  In the InterSystems IRIS Management Portal, go to `System Administration` > `Configuration` > `Additional Settings` > `Advanced Memory`.
    
8.  On the `Advanced Memory Settings` page, in the `PythonRuntimeLibrary` row, click `Edit`.
    
9.  Enter `C:\Program Files\Python311\python3.dll`.
    
    > **Important:**
    > 
    > If `python3.dll` is located in a folder that is within your user directory, such as `C:\Users\<username>\AppData\Local\Programs\Python\Python311`, it indicates that you have installed Python for the current user only. InterSystems recommends installing Python for all users to avoid unexpected results.
    
10.  Click `Save`.
     
11.  On the `Advanced Memory Settings` page, in the `PythonRuntimeLibraryVersion` row, click `Edit`.
     
12.  Enter `3.11`.
     
13.  Click `Save`.
     
14.  From Terminal, launch Embedded Python and verify that `sys.path` now includes the Python 3.11 package directories.
     
     ```objectscript
     USER>do ##class(%SYS.Python).Shell()
     
     Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
     Type quit() or Ctrl-D to exit this shell.
     >>> import sys
     >>> sys.path
     ['C:\\Program Files\\Python311\\python311.zip', 'C:\\Program Files\\Python311\\DLLs',
     'C:\\Program Files\\Python311\\Lib', 'c:\\intersystems\\IRIS\\bin',
     'c:\\intersystems\\IRIS\\mgr\\python', 'c:\\intersystems\\IRIS\\lib\\python',
     'C:\\Program Files\\Python311', 'C:\\Program Files\\Python311\\Lib\\site-packages']
     ```
     
15.  From Terminal, use the `GetPythonInfo()` method of the %SYS.Python class to view the Python version information.
     
     ```objectscript
     USER>do ##class(%SYS.Python).GetPythonInfo(.info)
     
     USER>zw info
     info("AllowNonSystemPythonForIntegratedML")=0
     info("CPF_PythonPath")=""
     info("CPF_PythonRuntimeLibrary")="C:\Program Files\Python311\python3.dll"
     info("CPF_PythonRuntimeLibraryVersion")=3.11
     info("IRISInsidePython")=0
     info("PythonInsideIRIS")=16
     info("RunningLibrary")="C:\Program Files\Python311\python3.dll"
     info("RunningVersion")="3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)]"
     info("SystemPath")="F:\AllPythons\python.3.9.13\tools\"
     info("SystemVersion")="3.9.13 (tags/v3.9.13:6de2ca5, May 17 2022, 16:36:42) [MSC v.1929 64 bit (AMD64)]"
     info("SystemVersionShort")="3.9.13"
     info("iris_site.py_platform")="winamd64"
     ```
     
     This example shows that the Python runtime library being used is `C:\Program Files\Python311\python3.dll` and the running version of Embedded Python is `3.11.9`. The `SystemVersion` is not relevant on Windows.
     

## Flexible Python Runtime Example: Python 3.11 on Ubuntu 22.04

Python 3.10 is the default version of Python on Ubuntu 22.04. This example shows how to use Python 3.11 with Embedded Python.

> **Note:**
> 
> This example is for Ubuntu 22.04 on the x86 architecture. File and directory names may vary if you are on the ARM architecture.

1.  Install Python 3.11 from the command line.
    
    `$ sudo apt install python3.11-full`
    
2.  Install the Python 3.11 `libpython.so` shared library.
    
    `$ sudo apt install libpython3.11`
    
3.  In the InterSystems IRIS Management Portal, go to `System Administration` > `Configuration` > `Additional Settings` > `Advanced Memory`.
    
4.  On the `Advanced Memory Settings` page, in the `PythonRuntimeLibrary` row, click `Edit`.
    
5.  Enter `/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0`.
    
6.  Click `Save`.
    
7.  On the `Advanced Memory Settings` page, in the `PythonRuntimeLibraryVersion` row, click `Edit`.
    
8.  Enter `3.11`.
    
9.  Click `Save`.
    
10.  From Terminal, launch Embedded Python and verify that `sys.path` now includes the Python 3.11 package directories.
     
     ```objectscript
     USER>do ##class(%SYS.Python).Shell()
     
     Python 3.11.0rc1 (main, Aug 12 2022, 10:02:14) [GCC 11.2.0] on linux
     Type quit() or Ctrl-D to exit this shell.
     >>> import sys
     >>> sys.path
     ['/usr/lib/python311.zip', '/usr/lib/python3.11', '/usr/lib/python3.11/lib-dynload', '/InterSystems/IRIS/mgr/python',
     '/InterSystems/IRIS/lib/python', '/usr/local/lib/python3.11/dist-packages', '/usr/lib/python3/dist-packages',
     '/usr/lib/python3.11/dist-packages']
     ```
     
11.  From Terminal, use the `GetPythonInfo()` method of the %SYS.Python class to view the Python version information.
     
     ```objectscript
     USER>do ##class(%SYS.Python).GetPythonInfo(.info)
     
     USER>zw info
     info("AllowNonSystemPythonForIntegratedML")=0
     info("CPF_PythonPath")=""
     info("CPF_PythonRuntimeLibrary")="/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0"
     info("CPF_PythonRuntimeLibraryVersion")=3.11
     info("IRISInsidePython")=0
     info("PythonInsideIRIS")=2
     info("RunningLibrary")="/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0"
     info("RunningVersion")="3.11.0rc1 (main, Aug 12 2022, 10:02:14) [GCC 11.2.0]"
     info("SystemPath")="/usr/lib/python3.10/config-3.10-x86_64-linux-gnu"
     info("SystemVersion")="3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0]"
     info("SystemVersionShort")="3.10.12"
     info("iris_site.py_platform")="lnxubuntu2204x64"
     ```
     
     This example shows that the Python runtime library being used is `/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0`, the running version of Embedded Python is `3.11.0rc1`, and the system version is `3.10.12`.
     

## Flexible Python Runtime Example: Anaconda on Windows

Anaconda is a Python-based platform commonly used for data science and artificial intelligence applications. This example shows how to use Anaconda with Windows. InterSystems recommends installing Anaconda for all users.

1.  Download Anaconda from https://anaconda.com/download.
    
2.  Launch the Anaconda installer, and on the `Welcome` screen, click `Next`.
    
3.  Approve the license agreement.
    
4.  Under `Select Installation Type`, install for `All Users`.
    
5.  Under `Choose Install Location`, for `Destination Folder`, leave the default: `C:\ProgramData\anaconda3`.
    
6.  Under `Advanced Installation Options`, deselect `Register Anaconda3 as the System Python`.
    
7.  Click `Install` to begin the installation process.
    
8.  In the InterSystems IRIS Management Portal, go to `System Administration` > `Configuration` > `Additional Settings` > `Advanced Memory`.
    
9.  On the `Advanced Memory Settings` page, in the `PythonRuntimeLibrary` row, click `Edit`.
    
10.  Enter `C:\ProgramData\anaconda3\python312.dll`.
     
11.  Click `Save`.
     
12.  On the `Advanced Memory Settings` page, in the `PythonRuntimeLibraryVersion` row, click `Edit`.
     
13.  Enter `3.12`.
     
14.  Click `Save`.
     
15.  Copy the file `iris_site_anaconda_windows_example.py` from the `<installdir>/lib/python` directory to the `<installdir>/mgr/python` directory and rename it `iris_site.py`.
     
     If you installed Anaconda in the default location, you should not need to modify the file.
     
16.  From Terminal, launch Embedded Python and verify that `sys.path` now includes the Anaconda package repositories.
     
     ```objectscript
     USER>do ##class(%SYS.Python).Shell()
     
     Python 3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 15:03:56) [MSC v.1929 64 bit (AMD64)] on win32
     Type quit() or Ctrl-D to exit this shell.
     >>> import sys
     >>> sys.path
     ['C:\\ProgramData\\anaconda3\\python312.zip', 'C:\\ProgramData\\anaconda3\\DLLs',
     'C:\\ProgramData\\anaconda3\\Lib', \'c:\\intersystems\\IRIS\\bin',
     'c:\\intersystems\\IRIS\\mgr\\python', 'c:\\intersystems\\IRIS\\lib\\python',
     'C:\\ProgramData\\anaconda3', 'C:\\ProgramData\\anaconda3\\Lib\\site-packages',
     'C:\\ProgramData\\anaconda3\\Lib\\site-packages\\win32', 'C:\\ProgramData\\anaconda3\\Lib\\site-packages\\win32\\lib',
     'C:\\ProgramData\\anaconda3\\Lib\\site-packages\\Pythonwin']
     ```
     
17.  From Terminal, use the `GetPythonInfo()` method of the %SYS.Python class to view the Python version information.
     
     ```objectscript
     USER>do ##class(%SYS.Python).GetPythonInfo(.info)
     
     USER>zw info
     info("AllowNonSystemPythonForIntegratedML")=0
     info("CPF_PythonPath")=""
     info("CPF_PythonRuntimeLibrary")="C:\ProgramData\anaconda3\python312.dll"
     info("CPF_PythonRuntimeLibraryVersion")=3.12
     info("IRISInsidePython")=0
     info("PythonInsideIRIS")=1
     info("RunningLibrary")="C:\ProgramData\anaconda3\python312.dll"
     info("RunningVersion")="3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 15:03:56) [MSC v.1929 64 bit (AMD64)]"
     info("SystemPath")="F:\AllPythons\python.3.9.13\tools\"
     info("SystemVersion")="3.9.13 (tags/v3.9.13:6de2ca5, May 17 2022, 16:36:42) [MSC v.1929 64 bit (AMD64)]"
     info("SystemVersionShort")="3.9.13"
     info("iris_site.py_platform")="winamd64"
     ```
     
     This example shows that the Python runtime library being used is `C:\ProgramData\anaconda3\python312.dll` and the running version of Embedded Python is `3.12.4`. The `SystemVersion` is not relevant on Windows.
     

## Flexible Python Runtime Example: Anaconda on Ubuntu 22.04

Anaconda is a Python-based platform commonly used for data science and artificial intelligence applications. This example shows how to use Anaconda with Ubuntu 22.04. InterSystems recommends doing an installation for your user.

> **Note:**
> 
> This example is for Ubuntu 22.04 on the x86 architecture. File and directory names may vary if you are on the ARM architecture.

1.  Download Anaconda.
    
    `curl -O https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh`
    
2.  Run the Anaconda installation script from the command line, for example:
    
    `$ sh Anaconda3-2024.02-1-Linux-x86_64.sh`
    
3.  Accept the license terms.
    
4.  When prompted for an installation directory, enter `/home/<username>/anaconda3`, where `<username>` is your Ubuntu username.
    
5.  You will be asked if you want to activate conda on startup. For this example, enter `no`.
    
6.  This will end the Anaconda installation process.
    
    You will see the message `Thank you for installing Anaconda3!`
    
7.  Activate Anaconda.
    
    `$ source /home/<username>/anaconda3/bin/activate`
    
    Substitute your actual username.
    
8.  Initialize Anaconda.
    
    `$ conda init`
    
9.  In the InterSystems IRIS Management Portal, go to `System Administration` > `Configuration` > `Additional Settings` > `Advanced Memory`.
    
10.  On the `Advanced Memory Settings` page, in the `PythonRuntimeLibrary` row, click `Edit`.
     
11.  Enter `/home/<username>/anaconda3/lib/libpython3.11.so.1.0`.
     
     Substitute your actual username.
     
12.  Click `Save`.
     
13.  On the `Advanced Memory Settings` page, in the `PythonRuntimeLibraryVersion` row, click `Edit`.
     
14.  Enter `3.11`.
     
15.  Click `Save`.
     
16.  Copy the file `iris_site_anaconda_ubuntu_linux_example.py` from the `<installdir>/lib/python` directory to the `<installdir>/mgr/python` directory and rename it `iris_site.py`.
     
17.  Edit the `iris_site.py` file to substitute your actual username in the last few lines of the file::
     
     ```
         sys.path = sys.path + __sitegetsitepackages(['/home/<username>/anaconda3'])
         sys.path = sys.path + ["/home/<username>/anaconda3/lib/python3.11/lib-dynload"]
         sys.path = ["/home/<username>/anaconda3/lib/python3.11"] + sys.path
         sys.path = ["/home/<username>/anaconda3/lib/python311.zip"] + sys.path
     ```
     
18.  From Terminal, launch Embedded Python and verify that `sys.path` now includes the Anaconda package repositories.
     
     ```objectscript
     USER>do ##class(%SYS.Python).Shell()
     
     Python 3.11.7 (main, Dec 15 2023, 18:24:52) [GCC 11.2.0] on linux
     Type quit() or Ctrl-D to exit this shell.
     >>> import sys
     >>> sys.path
     ['/home/<username>/anaconda3/lib/python311.zip', '/home/<username>/anaconda3/lib/python3.11',
     '/home/<username>/anaconda3/lib/python311.zip', '/home/<username>/anaconda3/lib/python3.11',
     '/home/<username>/anaconda3/lib/python3.11/lib-dynload', '/InterSystems/IRIS/mgr/python',
     '/InterSystems/IRIS/lib/python', '/home/<username>/anaconda3/lib/python3.11/site-packages',
     '/home/<username>/anaconda3/lib/python3.11/lib-dynload']
     ```
     
     The <username> in the above example will reflect your actual username.
     
19.  From Terminal, use the `GetPythonInfo()` method of the %SYS.Python class to view the Python version information.
     
     ```objectscript
     USER>do ##class(%SYS.Python).GetPythonInfo(.info)
     
     USER>zw info
     info("AllowNonSystemPythonForIntegratedML")=0
     info("CPF_PythonPath")=""
     info("CPF_PythonRuntimeLibrary")="/home/<username>/anaconda3/lib/libpython3.11.so"
     info("CPF_PythonRuntimeLibraryVersion")=3.11
     info("IRISInsidePython")=0
     info("PythonInsideIRIS")=3
     info("RunningLibrary")="/home/<username>/anaconda3/lib/libpython3.11.so"
     info("RunningVersion")="3.11.7 (main, Dec 15 2023, 18:24:52) [GCC 11.2.0]"
     info("SystemPath")="/usr/lib/python3.10/config-3.10-x86_64-linux-gnu"
     info("SystemVersion")="3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0]"
     info("SystemVersionShort")="3.10.12"
     info("iris_site.py_platform")="lnxubuntu2204x64"info("PythonInsideIRIS")=2
     info("RunningLibrary")="/usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0"
     info("RunningVersion")="3.11.0rc1 (main, Aug 12 2022, 10:02:14) [GCC 11.2.0]"
     info("SystemPath")="/usr/lib/python3.10/config-3.10-x86_64-linux-gnu"
     info("SystemVersion")="3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0]"
     info("SystemVersionShort")="3.10.12"
     info("iris_site.py_platform")="lnxubuntu2204x64"
     ```
     
     Again, the <username> in the above example will reflect your actual username.
     
     This example shows that the Python runtime library being used is `/home/<username>/anaconda3/lib/libpython3.11.so`, the running version of Embedded Python is `3.11.7`, and the system version is `3.10.12`.
