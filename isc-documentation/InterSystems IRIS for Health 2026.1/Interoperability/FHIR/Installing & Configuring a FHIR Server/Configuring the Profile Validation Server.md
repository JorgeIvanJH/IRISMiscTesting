# Configuring the Profile Validation Server

When you create a FHIR endpoint, an external server named `FHIR_Validation_Server` is created to perform back-end functions related to profile validation.

This server requires a Java 11 development kit. If your `JAVA_HOME` environment variable does not point to a Java 11 directory, you can use the Management Portal as follows:

1.  If necessary, install a supported Java 11 JDK. Make a note of the directory where it has been installed.
    
2.  In the Management Portal, navigate to `System Administration` > `Configuration` > `Connectivity` > `External Language Servers`.
    
3.  If the `FHIR_Validation_Server` is running, click `Stop`.
    
4.  Enter edit mode by clicking `FHIR_Validation_Server`.
    
5.  On the `Edit External Language Server` page, in the `Java Home Directory` field, enter the path to your Java 11 directory.
    
6.  Click `Save`.
    
7.  Restart the `FHIR_Validation_Server` by clicking `Start`.
    
8.  To ensure good performance when you execute validation operations related to previously-imported profiles (including those that are automatically imported), in the Terminal application, switch to your FHIR-enabled namespace and execute the following command:
    
    ```
    do ##class(HS.FHIRServer.Installer).InitializeProfileValidator()
    ```
    

> **Note:**
> 
> Do not set the `JAVA_HOME` environment variable directly to enable the `FHIR_Validation_Server`; doing so could affect other applications and processes that may rely on the previous value of `JAVA_HOME`.
