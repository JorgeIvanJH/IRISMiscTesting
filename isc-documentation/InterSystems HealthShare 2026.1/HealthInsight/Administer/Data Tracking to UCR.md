# [Tracking Data to HealthShare Unified Care Record](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_trace#HSAAADM_trace)

> **Note:**
> 
> This page applies only to Health Insight deployments that use a [Feeder Gateway](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_health_insight_AADBQ#PAGE_health_insight_aadbq).

> **Note:**
> 
> Feeder Gateway is short for Health Insight Feeder Access Gateway. In previous releases, this gateway was known as the dedicated Access Gateway.

When customers first access their aggregated data, it is not uncommon to see unexpected values that were not previously noticed. In such cases, you might find it necessary to trace a particular element of clinical data back to the facility that sent it. If you need to do so, here is an approach:

1.  Identify the patient or patients with which the data is associated. To do this, you generally use a detail listing and find the analytics ID of the record or records in question.
    
    For example, suppose that you see a patient whose systolic blood pressure is recorded as 888. When you display a detail listing, you see that the analytics ID of the patient is `MOIKJH`.
    
    For simplicity, the following discussion assumes that the associated messages were not purged from the HealthShare Health Insight production and the Feeder Gateway production.
    
2.  In the Health Insight production, find the messages for this patient. To do so:
    
    1.  In the message viewer in the analytics namespace, expand the `Extended Criteria` section.
        
    2.  Select `Add Criterion`.
        
    3.  For `Criterion Type`, select `Search Table Field`.
        
    4.  For `Class`, select `HS.Message.AnalyticsUpdateRequest`.
        
    5.  Edit `Condition` to be `IF AnalyticsID = PatientIDHere` where `PatientIDHere` is the analytics ID.
        
        For example:
        
        [Image: Search Criteria window that appears after clicking the Add Criterion Button, with aforementioned criteria specified]
    6.  Select `OK`.
        
    7.  Select `Search`.
        
    8.  Click the messages and view the message trace and the message contents. The `AnalyticsUpdateRequest` message will contain the data of interest. For example:
        
        [Image: Message viewer's right pane Contents tab, displaying formatted XML contents of AnalyticsUpdateRequest message body]
        
        This step establishes that the Health Insight production received the data in question.
        
3.  Now look in the Feeder Gateway production, as follows:
    
    1.  Search for messages for the same analytics ID, in the same way that you did in the analytics production (see step 2).
        
    2.  View the message trace for these messages.
        
    3.  In the same session in the message trace, find the `ECRFetchResponse` messages and examine their contents.
        
        Each `ECRFetchResponse` message contains one or more streamlets from a given Edge Gateway, containing information for the patient who has this analytics ID. At least one of these messages will contain the data of interest.
        
    4.  Find the specific `ECRFetchResponse` message or messages that contain the data of interest and identify which Edge Gateway sent the data.
        
        Immediately before each `ECRFetchResponse`, there is a `StreamletRequest` message, whose contents indicate the Edge Gateway that sent the `ECRFetchResponse`. (In the message contents, see the `<Gateway>` element, which contains the URL of the web service in that Edge Gateway.)
        
4.  In the Edge Gateway production (for the Edge Gateway found in the previous step), do the following:
    
    1.  Search the streamlet table to find the record or records that contain the data of interest. To do so, in the SQL Explorer, use a query of the following form:
        
        ```sql
        select * from HS_SDA3_Streamlet.Abstract where SDAString [ 'unfamiliarvaluehere'
        ```
        
        Where `'unfamiliarvaluehere'` is the unfamiliar value that you are looking for, in single quotes.
        
        The `HS_SDA3_Streamlet.Abstract` table contains all the streamlets. If you know which kind of streamlet you are looking for, you could use a more specific table such as `HS_SDA3_Streamlet.Diagnosis` instead and thus search fewer rows. The SQL Explorer lists all the available tables. (If you are not familiar with this aspect of InterSystems IRIS data platform, note that one InterSystems IRIS table can be a superset of other tables. For the streamlet tables, you can either search in the individual tables of specific types, or you can search in `HS_SDA3_Streamlet.Abstract`, which includes all the rows of all the streamlet tables.)
        
    2.  In the results that are returned, view the SDAString field, which contains the full data of the streamlets. This data might contain information indicating which facility sent the data. Also make a note of the values of following fields:
        
        *   ID — This is the ID of the streamlet, which you can open and view in another way. The ID is also useful for further tracking of this data.
            
        *   AggregationKey— Enables you to find the MRN for the patient (see step d).
            
        *   EncounterNumber — Depending on the form of this identifier, it might indicate which facility sent the data contained in this streamlet.
            
    3.  Rather than using SQL, as described in the previous two steps, you can open the Terminal on this instance, go to the applicable Edge Gateway namespace, and enter the following commands:
        
        ```objectscript
         set streamlet=##class(HS.SDA3.Streamlet.Diagnosis).%OpenId(ID)
         write streamlet.SDAString
        ```
        
        Where `ID` is the ID found in the previous step. Instead of [HS.SDA3.Streamlet.Diagnosis](https://docs.intersystems.com/hs20261/csp/documatic/%25CSP.Documatic.cls?LIBRARY=HSAALIB&CLASSNAME=HS.SDA3.Streamlet.Diagnosis), use the name of the applicable streamlet class.
        
    4.  In the Terminal, use the following command to find the facility, assigning authority, and MRN for this streamlet:
        
        ```objectscript
         write ^HS.SDAStreamletMRN("Key",AggregationKey)
        ```
        
        Where `AggregationKey` is the aggregation key found earlier. The result has the following form:
        
        ```
        FacilityID^AA^MRN
        ```
        
        Where `FacilityID` identifies the facility, `AA` is the assigning authority, and `MRN` is the MRN for that facility and assigning authority.
        
        For example:
        
        ```objectscript
        HSEDGE1>write ^HS.SDAStreamletMRN("Key",13)
        MYMC^MYMC^504199908628
        ```
        
5.  If needed, use this information to access the patient record at that facility and confirm that it contains the data in question.
    

For general information on monitoring and managing productions, see [Managing Unified Care Record Productions](https://docs.intersystems.com/hs20261/csp/docbook/DocBook.UI.Page.cls?KEY=HEENS).

## [For Additional Information on the Health Insight Data Flow](https://docs.intersystems.com/hslatest/csp/docbook/DocBook.UI.Page.cls?KEY=HSAAADM_trace#HSAAADM_trace_back_seealso)

At [learning.intersystems.com](https://learning.intersystems.com/), you can find the online course Health Insight Data Flow ([https://learning.intersystems.com/course/view.php?name=Health%20Insight%20Data%20Flow](https://learning.intersystems.com/course/view.php?name=Health%20Insight%20Data%20Flow)). By the end of this course, you will be able to:

*   Relate a clinical scenario supported by Health Insight to its internal data structures and processes
    
*   Identify the main data management components of HealthShare Unified Care Record and Health Insight
    
*   Describe the details of the data flow between Unified Care Record and Health Insight
    
*   Differentiate between HL7 and CCD data handling in HealthShare Unified Care Record
    
*   Recognize configuration points in the system and how they affect system performance
    
*   Define the Unified Care Record internal data structures and how they are used
