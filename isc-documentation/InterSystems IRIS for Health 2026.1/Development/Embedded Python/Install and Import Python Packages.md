# Install and Import Python Packages

Embedded Python gives you easy access to thousands of useful libraries. Commonly called “packages,” these need to be installed into the InterSystems IRIS file system before they can be used. Then they need to imported to load them into memory for use by your code. There are different ways to do this, depending on how you will use Embedded Python.

## Install Python Packages

Install Python packages from the command line before using them with Embedded Python. The command you use differs depending on whether you are using InterSystems IRIS on a UNIX-based system (except AIX), on AIX, on Windows, or in a container.

### Install Python Packages on a UNIX-Based System (except AIX)

On UNIX-based systems, use the command `python3 -m pip install --target <installdir>/mgr/python <package>`.

> **Note:**
> 
> If it is not installed already, first install the package `python3-pip` with your system’s package manager.

For example, the ReportLab Toolkit is an open source package for generating PDFs and graphics. On a UNIX-based system, use a command like the following to install it:

```
$ python3 -m pip install --target /InterSystems/IRIS/mgr/python reportlab
```

> **Important:**
> 
> If you do not install the package into the correct target directory, Embedded Python may not be able to import it. For example, if you install a package without the `--target` attribute (and without using `sudo`), Python will install it into the local package repository within your home directory. If any other user tries to import the package, it will fail.
> 
> Although InterSystems recommends using the `--target <installdir>/mgr/python` option, installing packages using `sudo` and omitting the `--target` attribute installs the packages into the global package repository. These packages can also be imported by any user.

### Install Python Packages on AIX

On AIX, install packages from the AIX Toolbox for Open Source Software, if they are available.

Before installing the package, make sure the package is in the AIX Toolbox with the command `sudo dnf list | grep <package>`. Then install the package with the command `sudo dnf install <package>`.

> **Note:**
> 
> If it is not installed already, first install the package `python3.9-pip` from the AIX Toolbox.

For example, confirm that the package `psutil` is the AIX Toolbox:

```
$ sudo dnf list | grep psutil
python3-psutil.ppc                                5.9.0-2          AIX_Toolbox
python3-psutil-tests.ppc                          5.9.0-2          AIX_Toolbox
python3.9-psutil.ppc                              5.9.0-2          AIX_Toolbox
python3.9-psutil-tests.ppc                        5.9.0-2          AIX_Toolbox
```

Then install the package:

```
$ sudo dnf install python3-psutil.ppc
```

Only if a package is not in the AIX Toolbox, install it with the following command:

```
$ python3 -m pip install <package>
```

### Install Python Packages on Windows

> **Note:**
> 
> On Windows, the `irispip` command was removed in InterSystems IRIS 2024.2. If you are running an earlier version, see the installation method described in the 2024.1 documentation.

On Windows, use the command `python -m pip install --target <installdir>\mgr\python <package>`.

For example, you can install the ReportLab package on a Windows machine as follows:

```
C:\>python -m pip install --target C:\InterSystems\IRIS\mgr\python reportlab
```

If you are using the Python launcher, you can use:

```
C:\>py -m pip install --target C:\InterSystems\IRIS\mgr\python reportlab
```

### Install Python Packages in a Container

If you are running InterSystems IRIS in a container without using the durable %SYS feature, use the command `python3 -m pip install --target /usr/irissys/mgr/python <package>`.

For example, you can install the ReportLab package in the container as follows:

```
$ python3 -m pip install --target /usr/irissys/mgr/python reportlab
```

If you are running InterSystems IRIS in a container using the durable %SYS feature, use the command `python3 -m pip install --target <durable>/mgr/python <package>`, where `<durable>` is the path defined in the environment variable `ISC_DATA_DIRECTORY` when running the container.

For example, if `ISC_DATA_DIRECTORY=/durable/iris`, you can install the ReportLab package in the container as follows:

```
$ python3 -m pip install --target /durable/iris/mgr/python reportlab
```

> **Note:**
> 
> Note: If you are using a Dockerfile to create a custom Docker image for InterSystems IRIS, install Python packages in `/usr/irissys/mgr/python`. Both `/usr/irissys/mgr/python` and `<durable>/mgr/python` are included in `sys.path` by default so that the packages can be found whether or not you are using the durable %SYS feature.

For more information on creating and running containers, see Running InterSystems Products in Containers.

## Import Python Packages

After installing a package, you need to import it before you can use it from InterSystems IRIS. This loads the package into memory so that it is available for use.

### Import Python Packages from ObjectScript

To import a Python package from ObjectScript, use the `Import()` method of the %SYS.Python class. For example:

```
set pymath = ##class(%SYS.Python).Import("math")
set canvaslib = ##class(%SYS.Python).Import("reportlab.pdfgen.canvas")
```

The first line, above, imports the built-in Python math module into ObjectScript. The second line imports just the `canvas.py` file from the `pdfgen` subpackage of ReportLab.

### Import Python Packages from a Method Written in Python

You can import packages in an InterSystems IRIS method written in Python, just as you would in any other Python code, for example:

```
ClassMethod Example() [ Language = python ]
{
    import math
    import iris
    import reportlab.pdfgen.canvas as canvaslib

    # Your Python code here
}
```

### Import Python Packages via an XData Block

You can also import a list of packages using an XData block in a class, as in the following example:

```
XData %import [ MimeType = application/python ]
{
import math
import iris
import reportlab.pdfgen.canvas as canvaslib
}
```

> **Important:**
> 
> The name of the XData block must be `%import`. The MIME type can be `application/python` or `text/x-python`. Make sure to use correct Python syntax, but do not indent your code or a complier error will occur.

These packages can then be used in any method within the class that is written in Python, without needing to import them again.

```
ClassMethod Test() [ Language = python ]
{
   # Packages imported in XData block

     print('\nValue of pi from the math module:')
     print(math.pi)
     print('\nList of classes in this namespace from the iris module:')
     iris._SYSTEM.OBJ.ShowClasses()
}
```

For background information on XData blocks, see Defining and Using XData Blocks
