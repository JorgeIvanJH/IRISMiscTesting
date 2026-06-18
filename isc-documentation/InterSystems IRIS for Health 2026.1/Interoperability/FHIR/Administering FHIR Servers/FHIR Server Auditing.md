# FHIR Server Auditing

The following FHIR-related events, which occur when accessing a FHIR endpoint with an OAuth token, can be logged in the audit log:

## Login

Generated from any valid requests against the FHIR Server.

*   Event Type
    
    ```
    %Login
    ```
    
*   Description
    
    ```
    FHIRServer <endpoint> login
    ```
    
*   Event Data
    
    ```
    <HTTP METHOD>:<REQUEST URL>
    Token: {<bearer token>}
    ```
    
    The `Token` block is optional, included only if available.
    

Audit logging for Login events is disabled by default.

## Login Failure

Generated from any unauthenticated requests against the FHIR Server (returning 401 status).

*   Event Type
    
    ```
    %Login
    ```
    
*   Description
    
    ```
    FHIRServer <endpoint> login failure
    ```
    
*   Event Data
    
    ```
    <HTTP METHOD>:<REQUEST URL>
    Failure Reason: <failure reason>
    Token: {<bearer token>}
    ```
    
    The `Token` block is optional, included only if available.
    

Audit logging for Login Failure events is enabled by default.

## Access Denied

Generated from any unauthorized requests against the FHIR Server (returning 403 status).

*   Event Type
    
    ```
    %Security
    ```
    
*   Description
    
    ```
    FHIRServer <endpoint> access denied
    ```
    
*   Event Data
    
    ```
    <HTTP Method>:<REQUEST URL>
    Failure Reason: <failure reason>
    Token: {<bearer token>}
    ```
    
    The `Token` block is optional, included only if available.
    

Audit logging for Access Denied events is enabled by default.

> **Note:**
> 
> You change the enablement status of audit logging events at `System > Security Management > System Audit Events`. For full details of InterSystems IRIS audit logging, see Auditing.
