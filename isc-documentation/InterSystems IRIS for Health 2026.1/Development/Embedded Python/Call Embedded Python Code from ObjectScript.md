# Call Embedded Python Code from ObjectScript

The section details several ways to call Embedded Python code from ObjectScript:

*   Use a Python package
    
*   Call a method in an InterSystems IRIS class written in Python
    
*   Run an SQL function or stored procedure written in Python
    
*   Run an arbitrary Python command
    

In some cases, you can call the Python code much the same way as you would call ObjectScript code, while sometimes you need to use the %SYS.Python class to bridge the gap between the two languages. For more information, see Bridge the Gap Between ObjectScript and Embedded Python.

## Use a Python Package

Embedded Python gives you easy access to thousands of useful libraries. Commonly called “packages,” these need to be installed from the Python Package Index (PyPI) into the `<installdir>/mgr/python` directory before they can be used. (For information on how to install a package, see Install Python Packages.)

For example, the ReportLab Toolkit is an open source library for generating PDFs and graphics.

After installing a package, you can use the `Import()` method of the %SYS.Python class to use it in your ObjectScript code.

Given a file location, the following ObjectScript method, `CreateSamplePDF()`, creates a sample PDF file and saves it to that location.

```objectscript
Class Demo.PDF
{

ClassMethod CreateSamplePDF(fileloc As %String) As %Status
{
    set canvaslib = ##class(%SYS.Python).Import("reportlab.pdfgen.canvas")
    set canvas = canvaslib.Canvas(fileloc)
    do canvas.drawImage("C:\Sample\isc.png", 150, 600)
    do canvas.drawImage("C:\Sample\python.png", 150, 200)
    do canvas.setFont("Helvetica-Bold", 24)
    do canvas.drawString(25, 450, "InterSystems IRIS & Python. Perfect Together.")
    do canvas.save()
}

}
```

The first line of the method imports the `canvas.py` file from the `pdfgen` subpackage of ReportLab. The second line of code instantiates a Canvas object and then proceeds to call its methods, much the way it would call the methods of any InterSystems IRIS object.

You can then call the method in the usual way:

```
do ##class(Demo.PDF).CreateSamplePDF("C:\Sample\hello.pdf")
```

The following PDF is generated and saved at the specified location:

[Image: One page PDF with the InterSystems logo, the Python logo, and the text: InterSystems IRIS and Python. Perfect Together.]

If you have written your own Python packages or modules, you can put them in `<installdir>/mgr/python` and import them from ObjectScript in the same way.

## Call a Method of an InterSystems IRIS Class Written in Python

You can write a method in an InterSystems IRIS class using Embedded Python and then call it from ObjectScript in the same way you would call a method written in ObjectScript.

The next example uses the `usaddress-scourgify` package. (For information on how to install a package, see Install Python Packages.)

The demo class below contains properties for the parts of a U.S. address and a method, written in Python, that uses `usaddress-scourgify` to normalize an address according to the U.S. Postal Service standard.

```
Class Demo.Address Extends %Library.Persistent
{

Property AddressLine1 As %String;

Property AddressLine2 As %String;

Property City As %String;

Property State As %String;

Property PostalCode As %String;

Method Normalize(addr As %String) [ Language = python ]
{

    from scourgify import normalize_address_record
    normalized = normalize_address_record(addr)

    self.AddressLine1 = normalized['address_line_1']
    self.AddressLine2 = normalized['address_line_2']
    self.City = normalized['city']
    self.State = normalized['state']
    self.PostalCode = normalized['postal_code']
}

}
```

Given a address string as input, the `Normalize()` instance method of the class normalizes the address and stores each part in the various properties of a `Demo.Address` object.

You can call the method as follows:

```objectscript
USER>set a = ##class(Demo.Address).%New()

USER>do a.Normalize("One Memorial Drive, 8th Floor, Cambridge, Massachusetts 02142")

USER>zwrite a
a=3@Demo.Address  <OREF>
+----------------- general information ---------------
|      oref value: 3
|      class name: Demo.Address
| reference count: 2
+----------------- attribute values ------------------
|       %Concurrency = 1  <Set>
|       AddressLine1 = "ONE MEMORIAL DR"
|       AddressLine2 = "FL 8TH"
|               City = "CAMBRIDGE"
|         PostalCode = "02142"
|              State = "MA"
+-----------------------------------------------------
```

## Run an SQL Function or Stored Procedure Written in Python

When you create a SQL function or stored procedure using Embedded Python, InterSystems IRIS projects a class with a method that can be called from ObjectScript as you would any other method.

For example, the SQL function from the example earlier in this document generates a class `User.funcrandomletter`, which has a `randomletter()` method. Call it from ObjectScript as follows:

```objectscript
USER>zwrite ##class(User.funcrandomletter).randomletter()
"K"
```

## Run an Arbitrary Python Command

Sometimes, when you are developing or testing Embedded Python code, it can be helpful to run an arbitrary Python command from ObjectScript. You can do this with the `Run()` method of the %SYS.Python class.

Perhaps you want to test the `normalize_address_record()` function from the `usaddress_scourgify` package used earlier in this document, and you don’t remember how it works. You can use the `%SYS.Python.Run()` method to output the help for the function from the Terminal as follows:

```objectscript
USER>set rslt = ##class(%SYS.Python).Run("from scourgify import normalize_address_record")

USER>set rslt = ##class(%SYS.Python).Run("help(normalize_address_record)")
Help on function normalize_address_record in module scourgify.normalize:
normalize_address_record(address, addr_map=None, addtl_funcs=None, strict=True)
    Normalize an address according to USPS pub. 28 standards.

    Takes an address string, or a dict-like with standard address fields
    (address_line_1, address_line_2, city, state, postal_code), removes
    unacceptable special characters, extra spaces, predictable abnormal
    character sub-strings and phrases, abbreviates directional indicators
    and street types.  If applicable, line 2 address elements (ie: Apt, Unit)
    are separated from line 1 inputs.
.
.
.
```

The `%SYS.Python.Run()` method returns 0 on success or -1 on failure.
