# Deleting a FHIR Endpoint

You can use the `FHIR Server Management` page either to delete both the FHIR server endpoint and the associated the FHIR data, or to just decommission the endpoint and retain the FHIR data.

> **Note:**
> 
> *   You can decommission a FHIR endpoint programmatically by calling the DecommissionInstance() method of HS.FHIRServer.Installer.
>     
> *   You can uninstall a FHIR endpoint programmatically by calling the UninstallInstance() method of HS.FHIRServer.Installer.
>     
> *   You can also delete or decommission a FHIR endpoint using the FHIR Server Management REST API.
>     
> *   If you prefer, you can use a command-line interface to delete or decommission a FHIR server.
>     

To delete or decommission a FHIR endpoint:

1.  Open the `FHIR Server Management` page.
    
    Either of the following paths in the Management Portal will take you to the page:
    
    *   Navigate to `Home` > `Health` (or `Home` > `HealthShare`) and click `FHIR` in the banner.
        
    *   Navigate to `Home` > `Health` > `FHIRServerNamespace` > `FHIR Server Management`.
        
2.  In the tile for the server associated with the desired endpoint, open the menu and choose `Delete`.
    
3.  Decide whether to remove all data along with the endpoint, and select the corresponding radio button. The deletion options are:
    
    *   `Remove all data from the repository, delete the endpoint and FHIR server.`
        
    *   `Decommission FHIR endpoint, don’t remove data.`
        
4.  Click `Execute`.
