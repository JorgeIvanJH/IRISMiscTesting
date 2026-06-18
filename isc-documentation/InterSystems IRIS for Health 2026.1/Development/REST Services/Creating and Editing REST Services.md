# Creating and Editing REST Services

There are multiple ways to create and modify REST services within InterSystems IRIS data platform. The three main methods of doing so are by invoking the `/api/mgmnt/` service, using the ^%REST routine, or using the %REST.API class. These three methods of creating REST services require creating an OpenAPI 2.0 (also called Swagger) description for the REST service to use to generate the service classes. If you are implementing a REST service defined by a third party, they may provide this OpenAPI 2.0 description. See the OpenAPI 2.0 Specification for details about the format of an OpenAPI 2.0 description.

After generating the service classes, see Modifying the Implementation Class and Modifying the Specification Class for further instructions on building a REST service.

## Using the /api/mgmnt/ Service

One of the methods of creating, updating, and deleting REST services involves calling the `/api/mgmnt/` service.

This service also provides options you can use to list and document web services.

### Creating REST Services with /api/mgmnt

#### Generating Services Classes with /api/mgmnt/

In the first step, generate the REST service classes, as follows:

1.  Create or obtain the OpenAPI 2.0 description of the REST service, in JSON format.
    
2.  Obtain a REST testing tool such as PostMan (https://www.getpostman.com/).
    
3.  In the testing tool, create an HTTP request message as follows:
    
    *   For the HTTP action, select or specify POST.
        
    *   For the URL, specify a URL of the following form, using the <baseURL> for your instance:
        
        `https://<baseURL>/api/mgmnt/v2/namespace/myapp`
        
        Where `namespace` is the namespace where you want to create the REST service and `myapp` is the name of the package where you want to create the classes.
        
    *   For the request body, paste the OpenAPI 2.0 description of your web service, in JSON format.
        
    *   Specify the request body type as `JSON (application/json)`
        
    *   Provide values for the `IRISUsername` and `IRISPassword` parameters. For `IRISUsername`, specify a user that is a member of the %Developer role and that has read/write access to the given namespace.
        
4.  Send the request message.
    
    If the call is successful, InterSystems IRIS creates the `disp`, `impl`, and `spec` classes in the given package and namespace.
    
5.  In the testing tool, check the response message. If the request was successful, the response message will look like the following example:
    
    ```
    {
        "msg": "New application myapp created"
    }
    ```
    

To complete the basic REST service, create an InterSystems web application and define the implementation (see Modifying the Implementation Class). You can do these steps in either order.

#### Creating the Web Application

In this step, you create a web application that provides access to your REST service. In the Management Portal, complete the following steps:

1.  Click `System Administration > Security > Applications > Web Applications`.
    
2.  Click `Create New Web Application`.
    
3.  Specify the following values:
    
    *   `Name` — Name for the web application; this must be unique within this instance of InterSystems IRIS. The most common name is based on the namespace in which the web application runs: `/csp/namespace`
        
    *   `Namespace` — Select the namespace in which you generated the classes.
        
    *   `Enable Application` — Select this check box.
        
    *   `Enable` — Select `REST`.
        
    *   `Dispatch Class` — Type the fully qualified name of the dispatch class. This should always be `package.disp` where `package` is the name of the package that contains the generated classes.
        
    
    For information on other options on this page, see Create an Application.
    
4.  Click `Save`.
    

### Updating REST Services with /api/mgmnt/

The InterSystems API management tools enable you to update the generated classes without making changes to your edits in the implementation class. The class is regenerated if necessary, but your edits are preserved.

If the update was successful, InterSystems IRIS regenerates the `disp` and `spec` classes in the given package and updates the `impl` class, preserving edits you made to that class. The response message will look like the following example:

```
{
    "msg": "Application myapp updated"
}
```

#### How InterSystems Updates the Implementation Class

If you previously edited the `impl` class, InterSystems preserves those edits as follows:

*   The implementations of all methods are left as is.
    
*   Any new class members you added are left as is.
    

However, InterSystems regenerates the description (the `///` comments) of the class and of each generated method. If the signature of any implementation method changes (for example, because the specification has changed), InterSystems updates the signature and adds the following comment to that class method:

```
/// WARNING: This method's signature has changed.
```

### Deleting REST Services with /api/mgmnt/

The InterSystems API management tools also enable you to delete a REST service easily. To do so:

1.  Using a REST testing tool, create an HTTP request message as follows:
    
    *   For the HTTP action, select or specify DELETE.
        
    *   For the URL, specify a URL of the following form, using the <baseURL> for your instance:
        
        `http://<baseURL>/api/mgmnt/v2/namespace/myapp`
        
        Where `localhost` is the name of the server, 52773 is the web server port that InterSystems IRIS is using, `namespace` is the namespace where you want to create the REST service, and `myapp` is the name of the package that contains the REST service classes.
        
    *   Provide values for the `IRISUsername` and `IRISPassword` parameters. For `IRISUsername`, specify a user that is a member of the %Developer role and that has read/write access to the given namespace.
        
2.  Send the request message.
    
    If the call is successful, InterSystems IRIS deletes the `disp` and `spec` classes within the given package and namespace.
    
    InterSystems IRIS does not, however, delete the `impl` class.
    
3.  In the testing tool, check the response message. If the request was successful, the response message will look like the following example:
    
    ```
    {
        "msg": "Application myapp deleted"
    }
    ```
    
4.  Manually delete the implementation class.
    
    For safety, the `/api/mgmnt` service does not automatically delete the implementation class, because that class can potentially contain a significant amount of customization.
    
5.  Delete the web application you created previously (if any) for this REST service. To do so:
    
    1.  In the Management Portal, click `System Administration > Security > Applications > Web Applications`.
        
    2.  Click `Delete` in the row that lists the web application.
        
    3.  Click `OK` to confirm the deletion.
        

## Using the ^%REST Routine

The `^%REST` routine is a simple command-line interface. At any prompt, you can enter the following answers:

<table><tr><td><code>^</code></td><td>Causes the routine to skip back to the previous question.</td></tr><tr><td><code>?</code></td><td>Causes the routine to display a message that lists all the current options.</td></tr><tr><td><code>q</code> or <code>quit</code> (not case-sensitive)</td><td>Ends the routine.</td></tr></table>

Also, each question displays, in parentheses, the default answer to that question.

### Using ^%REST to Create a Service

The recommended way to create a REST service is to start with the OpenAPI 2.0 specification of the REST service and use that to generate the REST service classes. To use the `^%REST` routine to do this:

1.  Obtain the OpenAPI 2.0 specification for the REST service, in JSON format. Either save the specification as a file or make a note of the URL where the specification can be accessed.
    
2.  In the Terminal, change to the namespace where you want to define the REST service.
    
3.  Enter the following command to start the `^%REST` routine:
    
    ```
    do ^%REST
    ```
    
4.  At the first prompt, enter a name for the REST service. This name is used as the package name for the generated classes; use a valid package name. If you want to use the name `list`, `l`, `quit`, or `q` (in any case variation), enclose the name in double quotes. For example: `"list"`
    
5.  At the next prompt, enter `Y` (not case-sensitive) to confirm that you want to create this service.
    
    The routine then prompts you for the location of the OpenAPI 2.0 specification to use. Enter either a full pathname or a URL.
    
6.  At the next prompt, enter `Y` (not case-sensitive) to confirm that you want to use this specification.
    
    The routine creates the `disp`, `impl`, and `spec` classes within the specified package in this namespace. The routine then displays output like the following:
    
    ```
    -----Creating REST application: myapp-----
    CREATE myapp.spec
    GENERATE myapp.disp
    CREATE myapp.impl
    REST application successfully created.
    ```
    
    Next the routine asks if you also want to create a web application. You will use this web application to access the REST service.
    
7.  At this point, you can do the following:
    
    *   Enter `Y` (not case-sensitive) to create the web application now.
        
    *   Enter `N` (not case-sensitive) to end the routine.
        
        You can create the web application separately as described in Creating the Web Application.
        
8.  If you entered `Y`, the routine then prompts you for the name of the web application.
    
    The name must be unique within this instance of InterSystems IRIS. The default name is based on the namespace in which the web application runs: `/csp/namespace`.
    
    Enter the name of the web application or press return to accept the default name.
    
    The routine then displays output like the following:
    
    ```
    -----Deploying REST application: myapp-----
    Application myapp deployed to /csp/myapp
    ```
    
9.  Define the implementation as described in Modifying the Implementation Class.
    

### Using ^%REST to Delete a Service

To use the `^%REST` routine to delete a REST service:

1.  In the Terminal, change to the namespace where the REST service can be found.
    
2.  Enter the following command to start the `^%REST` routine:
    
    ```
    do ^%REST
    ```
    
3.  At the first prompt, enter a name for the REST service.
    
    If you are not sure of the name of the REST service, enter `L` (not case-sensitive). The routine lists all the REST services and then prompts you again for the name of the REST service.
    
4.  If the routine finds a REST service with the given name, it displays a prompt like the following:
    
    ```
    REST application found: petstore
    Do you want to delete the application? Y or N (N):
    ```
    
5.  Enter `Y` (not case-sensitive) to confirm that you want to delete this service.
    
6.  (Optionally) Manually delete the implementation class.
    
    For safety, the routine does not automatically delete the implementation class, because that class can potentially contain a significant amount of customization.
    

## Using the %REST.API Class

This section describes how to use the %REST.API class to create, update, and delete REST services.

### Using the %REST.API Class to Create or Update a Service

The recommended way to create a REST service is to start with the OpenAPI 2.0 specification of the REST service and use that to generate the REST service classes. To use the %REST.API class to do this:

1.  Obtain the OpenAPI 2.0 specification for the REST service, in JSON format, and save the specification as a file.
    
    The file must be UTF-8 encoded.
    
2.  In the namespace where you want to define the REST service, use the file to create an instance of %DynamicObject.
    
3.  Then call the `CreateApplication()` method of the %REST.API class. This method has the following signature:
    
    ```
    classmethod CreateApplication(applicationName As %String,
                                  swagger As %DynamicObject = "",
                                  ByRef features,
                                  Output newApplication As %Boolean,
                                  Output internalError As %Boolean)
                                  as %Status
    ```
    
    Where:
    
    *   `applicationName` is the name of the package where you want to generate the classes.
        
    *   `swagger` is the instance of %DynamicObject that represents the OpenAPI 2.0 specification.
        
        You can also specify this argument as the URL of a specification, the pathname of a file that contains a specification, or as an empty string.
        
    *   `features`, which must be passed by reference, is a multidimensional array that holds any additional options:
        
        *   If `features("addPing")` is 1 and if `swagger` is an empty string, then the generated classes include a `ping()` method for testing purposes.
            
        *   If `features("strict")` is 1 (the default), then InterSystems checks all the properties in the specification. If `features("strict")` is 0, then only the properties that are needed for code generation are checked.
            
    *   `newApplication`, which is returned as output, is a boolean value that indicates whether the method created a new application (true) or updated an existing application.
        
    *   `internalError`, which is returned as output, is a boolean value that indicates whether an internal error occurred.
        
    
    If the method generates a new application, InterSystems IRIS creates the `disp`, `impl`, and `spec` classes in the given package.
    
    If the method updates an existing application, InterSystems IRIS regenerates the `disp` and `spec` classes in the given package and updates the `impl` class, preserving edits you made to that class.
    
    If the OpenAPI 2.0 specification is invalid, the method does not make any change.
    
4.  Create a web application that access the REST service, as described in Creating and Editing REST Services.
    
5.  Define the implementation as described in Modifying the Implementation Class.
    

The following shows an example of the first steps:

```
 set file="c:/2downloads/petstore.json"
 set obj = ##class(%DynamicAbstractObject).%FromJSONFile(file)
 do ##class(%REST.API).CreateApplication("petstore",.obj,,.new,.error)
 //examine error and decide how to proceed...
 ...
```

### Using the %REST.API Class to Delete a Service

To use the %REST.API class to delete a REST service:

1.  In the namespace where the REST service can be found, call the `DeleteApplication()` method of the %REST.API class. This method has the following signature:
    
    ```
    classmethod DeleteApplication(applicationName As %String) as %Status
    ```
    
    Where `applicationName` is the name of the package that contains the REST service classes.
    
2.  (Optionally) Manually delete the implementation class.
    
    For safety, the class method does not automatically delete the implementation class, because that class can potentially contain a significant amount of customization.
    
3.  Delete the web application you created previously (if any) for this REST service. To do so:
    
    1.  In the Management Portal, click `System Administration > Security > Applications > Web Applications`.
        
    2.  Click `Delete` in the row that lists the web application.
        
    3.  Click `OK` to confirm the deletion.
