---
description: Guide from a tutorial about how to create REST services in InterSystems IRIS with steps using the management portal UI
argument-hint: "[extra constraints]"
---
Task 1Open your virtual machine
Start by opening your virtual machine and familiarizing yourself with its contents.

Terminal sessions can be opened using the left hand Favorites bar.
Your instance of InterSystems IRIS is bookmarked within Google Chrome.
Postman is installed and available via the Favorites bar. This will be used to send REST requests in the exercise.
Task 2Build the sample code
To build the sample code, follow this procedure:

Open a new terminal window via the left-hand bar on your virtual machine.
Run the following command to open a command line session on the container running your InterSystems IRIS server:
docker exec -it iris bash
Run the following command to open an InterSystems IRIS Terminal session within the container:
iris session iris
Set the current namespace to the INTEROP namespace:
set $namespace = "INTEROP"
Enter the following two commands to load and build the sample classes from your downloaded repository:
do $system.OBJ.Load("/external/FirstLook-REST/buildsample/Build.RESTSample.cls","ck")
do ##class(Build.RESTSample).Build()
When prompted, enter the full path of the directory to which you downloaded this sample:
/external/FirstLook-REST
The method then loads and compiles the code and performs other needed setup steps.

Task 3Define a web application
Now that you have compiled the sample code with the REST interfaces on your server, follow these steps to define a web application:

Open Google Chrome and navigate to the IRIS bookmark in your browser.
Log in using username tech and password demo7.
Click System Administration > Security > Applications > Web Applications.
Click Create New Web Application, and enter the following settings:
Name: /rest/coffeemakerapp
This specifies the URLs that will be handled by this web application. InterSystems IRIS will direct all URLs that begin with /rest/coffeemakerapp to this web application.
Namespace: INTEROP
Enable: Select REST.
Dispatch Class: Demo.CoffeeMakerRESTServer
This class names all the routes in the REST API and associates each one with a function.
Security Settings/Allowed Authentication Methods: Select both Unauthenticated and Password.
To allow unauthenticated access for this sample, you must give the web application the %All role. To do this:
Click Save, then the Application Roles tab.
Select the %All role from the Available roles.
Click the right arrow (select) button to move the %All role to the Selected roles.
Click the Assign button.
The %All role is now listed as an Application Role. This ensures that a REST call from an unauthenticated user will have the privileges needed to access the coffeemakerapp data. Without this role, the REST call would have to specify authentication for a user who has sufficient privileges.

Task 4Access the REST interfaces
The coffeemaker application is now functional, with a data table, an InterSystems IRIS web application, and exposed endpoints. Finally, you can test your API to make sure that these work as expected. You will submit API requests to access the coffee maker database. In the Postman application on your virtual machine (the orange icon in your left hand bar), follow these steps:

Send a REST POST request to add a new coffee maker.
HTTP Action: POST
URL: http://localhost:52773/rest/coffeemakerapp/newcoffeemaker.
Authorization: Basic Authorization, using tech / demo7.
Body (select raw as the body type):
Begin code:
{"img":"img/coffee3.png", "coffeemakerID":"99", "name":"Double Dip", "brand":"Coffee+", "color":"Blue", "numcups":2, "price":71.73}
End code.Although the data contains a value for coffeemakerID, that is a calculated field and a new value is assigned when the record is added. The call returns a success status: {"Status":"OK"}
Send another REST POST request to add the following coffee maker:Begin code:
{"img":"img/coffee4.png", "coffeemakerID":"99", "name":"French Press", "brand":"Coffee For You", "color":"Blue", "numcups":4, "price":50.00}
End code.
