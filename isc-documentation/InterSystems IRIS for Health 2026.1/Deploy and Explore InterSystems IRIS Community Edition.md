# Deploy and Explore InterSystems IRIS Community Edition

This document explains how to use publicly available images to deploy InterSystems IRIS Community Edition in a container either locally or in the cloud, and provides instructions for connecting to and using your Community Edition instance.

*   For detailed information on using InterSystems IRIS in containers, see Running InterSystems Product in Containers.
    
*   For the full range of InterSystems IRIS deployment options, see Deploying InterSystems IRIS.
    

*   To learn all about the capabilities and advantages of InterSystems IRIS data platform, see the InterSystems Developer Hub.
    

## Try InterSystems IRIS!

Want to take InterSystems IRIS for a test drive? Try InterSystems IRIS Community Edition! Community Edition comes with a free license and a few limitations, and is ideal for evaluation and testing. You can deploy it in any of the following fast and easy ways:

*   Download an image from the InterSystems Container Registry or Docker Hub and deploy your own Community Edition container on the host of your choice.
    
*   Deploy a Community Edition container on a public cloud node.
    
*   Deploy an InterSystems IRIS Community Edition instance on the web, with an integrated IDE and sample data to work with; for more information, see InterSystems IRIS on the Web.
    

> **Note:**
> 
> For simplicity, all Community Edition images referred to in this document have the tag `latest-em`; the image you are working with may be different.
> 
> The InterSystems IRIS container provided on a Community Edition cloud node is always named `iris`; for this reason, all examples in this document assume the container involved is named `iris`, although a container you deploy on your own cloud or hardware system can have any name you choose.
> 
> Container images from InterSystems comply with the Open Container Initiative (OCI) specification and are therefore supported on any OCI-compliant runtime engine on Linux-based operating systems, both on premises and in public clouds. The specific instructions and procedures in this document are intended to be used with Docker on Linux.

## Deploy InterSystems IRIS Community Edition on Your Own System

You can deploy a containerized instance of InterSystems IRIS Community Edition on your own public cloud, private cloud, or hardware system from the Community Edition image, using the following steps.

1.  Ensure that an OCI-compliant container runtime engine, such as Docker or Podman, is installed on your servers. (The specific instructions and procedures in this document are intended to be used with Docker on Linux.)
    
2.  Browse the InterSystems Container Registry (ICR) portal, as described in Using the InterSystems Container Registry, to locate the Community Edition image you want (because they are publicly available, no InterSystems or Docker login is required to view or download them). You can download images from the `iris-community` (InterSystems IRIS Community Edition) and`irishealth-community` (InterSystems IRIS for Health Community Edition) repositories. When you select a tag within a repository, the main panel displays one or two `docker pull` commands, which you can copy and paste onto your Linux command line to download the image. (Two `docker pull` commands are displayed when an image is available for both amd64 and arm64 architecture.) For example, if you selected the amd64 version of the `latest-em` image in the `iris-community` repository, your `docker pull` command would look like this:
    
    ```
    $ docker pull containers.intersystems.com/intersystems/iris-community:latest-em
    5c939e3a4d10: Pull complete
    c63719cdbe7a: Pull complete
    19a861ea6baf: Pull complete
    651c9d2d6c4f: Pull complete
    $ docker images
    REPOSITORY                  TAG         IMAGE ID     CREATED     SIZE
    intersystems/iris-community latest-em  15627fb5cb76 1 month ago 1.33GB
    ```
    
    > **Important:**
    > 
    > Do not copy the command in the example above, but rather copy the command for the image you want from the ICR portal.
    
    > **Note:**
    > 
    > The image tags shown in this document are examples only. Please go to the ICR portal, as noted above, to browse current repositories and tags.
    > 
    > You can also download any of the Community Edition images described here from Docker Hub by removing `containers.intersystems.com/` from the appropriate pull command or replacing it with `hub.docker.com/`.
    
3.  The following `docker run` command uses the `containers.intersystems.com/intersystems/iris-community:latest-em` image to create and starts an InterSystems IRIS Community Edition container called `iris`. If you have not already pulled (downloaded) the image, Docker does that first.
    
    ```
    $ docker run --name iris -d --publish 1972:1972 --publish 52773:52773
        containers.intersystems.com/intersystems/iris-community:latest-em
    ```
    
    > **Important:**
    > 
    > Remember to replace the image specification in the above command with that of the Community Edition image you have downloaded and want to use.
    
    The argument to each `--publish` option pairs a host port (which comes first) with a container port (which follows), allowing outside entities to interact with the container port by connecting to the host port. For example, to publish container port 2730 to host port 9730, you would use the option `--publish 9730:2730`. This example shows the instance’s superserver port (1972) and web server port (52773) published to the same ports on the host, so that you can interact with InterSystems IRIS from outside the container using theses known ports. If you publish to different host ports, be sure to note them for use in connecting to the instance.
    
    > **Important:**
    > 
    > The web server port is 52773 on Community Edition instances only. The port used to connect to the Management Portal on other instances depends on their manner of deployment, as discussed in InterSystems IRIS Connection Information in InterSystems IRIS Basics: Connecting an IDE.
    
4.  Execute the `docker ps -a` command to see the status of the container, which is called named according to the `--name` option in your `docker run` command, and confirm that it is running.
    
    > **Note:**
    > 
    > If the container fails to start, with an error message indicating that your system has too many cores for the Community Edition license, first remove the stopped container with the command `docker rm iris`, then restrict a new container to 20 cores, the Community Edition limit, by inserting the options`--cpuset-cpus=0-19 --cpus=20` after the `--name` option in the above `docker run` command.
    

That’s it! You are the proud owner of an InterSystems IRIS Community Edition instance running in a container. The instance comes with a free built-in license that expires a year after the product version’s release date, as well as a production-enabled USER namespace (there are also some limitations).

Once the container is running, you can continue with the instructions in Explore Your InterSystems IRIS Instance.

> **Note:**
> 
> The provided setup instructions are valid for most Docker environments; if you encounter any problems, see Using InterSystems IRIS Containers and Additional Docker/InterSystems IRIS Considerations in Running InterSystems Products in Containers. For information specific to Docker for Windows, see Using InterSystems IRIS Containers with Docker for Windows on InterSystems Developer Community.

## Deploy InterSystems IRIS Community Edition on a Cloud Node

To deploy Community Edition on a public cloud node, do the following:

1.  Log in to your Amazon Web Services or Microsoft Azure account. If neither you nor your employer have one yet, you can go to the AWS or Azure portal page to quickly create a free account. Select or create an IAM user and credentials (AWS) or a resource group (Azure).
    
2.  Go to the cloud provider’s marketplace page and search for `InterSystems IRIS`.
    
3.  On the listing page, click `Continue to Subscribe` (AWS) or `Create` (Azure), follow the prompts and fill in the required fields, then click `Deploy` when ready.
    
    > **Note:**
    > 
    > On Azure, to simplify making SSH connections to the cloud node, find the Administrator account section at the bottom of the Basics tab on the Create a virtual machine page, select Password for Authentication type, and enter a username and password.
    > 
    > On AWS, for a more streamlined experience, choose `Launch through EC2` at the first prompt on the `Launch this software` page. (If you continue on the website, at the `Security Group Settings` drop-down, be sure to select `Create New Based On Seller Settings`.)
    

That’s it! You are the proud owner of an InterSystems IRIS Community Edition instance on a cloud node. The instance comes with a free built-in license that expires a year after the product version’s release date, as well as a production-enabled USER namespace (there are also some limitations).

Once your node is deployed, go to the page listing your nodes — `EC2` > `Running instances` (AWS) or `Virtual machines` (Azure) — then continue with the instructions in Explore Your InterSystems IRIS Instance.

## InterSystems IRIS on the Web

Most of the InterSystems IRIS exercises on the InterSystems Learning site provide access to a Learning Lab—a virtual machine which hosts a modified InterSystems IRIS Community Edition instance. A Learning Lab includes an integrated IDE as well as sample data which you can use to complete the exercise. Alternatively, you can create data of your own that more closely reflects the specific needs of your application. Learning Lab instances are licensed and provisioned for three days, and have functionality limitations similar to those of the Community Edition.

## Explore Your InterSystems IRIS Instance

This section describes several ways to interact with your containerized Community Edition InterSystems IRIS instance. The first step after connecting is to secure your instance by changing the instance’s default passwords.

### Change the Default Passwords

To ensure that you have immediate access after installation, InterSystems IRIS comes with several predefined user accounts, each of which has the default password `SYS`. To secure your instance, you should change these default passwords as soon as possible. The steps differ whether your container is running on your own system or a cloud node, as follows:

*   On any system other than one of the cloud nodes described above, when you connect to a Community Edition using the Management Portal, you must log in using one of the predefined accounts, for example `_SYSTEM`. If it is your first time logging in to this account, you must use the default password `SYS`, then change the password for the account when you are prompted immediately afterwards.
    
    Next, change the default passwords for all of the predefined accounts as soon as possible; it is a best practice to make them all different. You can change them in either of the following ways:
    
    *   Use one of the methods described in Authentication and Passwords in Running InterSystems Products in Containers.
        
    *   Log in to each of the predefined user accounts using the Management Portal and change the password when prompted. You can also disable one or more of these accounts .
        
*   On a cloud node, the recommended and easiest way to do this is by connecting to the node using SSH and issuing the command `iris password` at the shell prompt, because this changes the default passwords for all of the predefined accounts at the same time. The command also displays the predefined account usernames; you will use one of these with the new password you just entered when you first log in to the InterSystems IRIS instance.
    
    Even with the default password changed by the `iris password` command, all of the predefined user accounts still share a single password, which is not the best security practice. You can make them all different by logging in to each using the Management Portal and changing the password when prompted. You can also disable one or more of these accounts using the portal.
    

### Connect to the Cloud Node Using SSH

You can connect to your cloud node using SSH to change the default passwords, explore the InterSystems IRIS container, and interact with InterSystems IRIS using the InterSystems Terminal. The way in which you connect depends on the platform you are using, as follows:

*   Azure uses the credentials you provided for the administrator account on the `Create a virtual machine` page when deploying the node. To connect using a separate program such as PuTTY, follow the instructions in `Instances > Connect to Linux VMs` under Virtual machines in Azure in the Azure documentation .
    
*   AWS uses the public-private key pair you designated or created when launching the instance, and you must supply the program you use to make an SSH connection with the private key from this pair. You can connect with the popular program PuTTY using these steps:
    
    1.  Open the PuTTYgen key generator program that is installed with PuTTY and do the following:
        
        1.  Use the `Load` button to load the `.pem` private key file provided by AWS. (Remember to set the file type selector in the file browser dialog to `All files (*.*)` to display the `.pem` file you want to load.)
            
        2.  Use the `Save private key` button to save the key in `.ppk` format.
            
    2.  Open the PuTTY program itself and do the following:
        
        1.  In the `Host Name` box, enter `ubuntu@host`, where `host` is either the DNS name or the IP address, for example `ubuntu@ec2-34-000-53-213.compute-1.amazonaws.com` or `ubuntu@34.000.53.213`.
            
        2.  In the navigation tree on the left, expand `SSH` and select `Auth`, and at the `Private key file for authentication` prompt browse for the `.ppk` file you saved in the previous step.
            
        3.  Click `Open`.
            
        
        Once you have successfully connected, you can save the connection settings in PuTTY so that fewer steps will be required to connect in the future.
        
    
    For other ways to connect to an AWS cloud node, see Connect to your linux in the AWS documentation.
    

### Interact with InterSystems IRIS

Several ways to interact with your containerized InterSystems IRIS instance are listed in the following. The ones you’ll use depend on what InterSystems IRIS features you want to explore. For detailed information about using a containerized InterSystems IRIS instance, see Running InterSystems Products in Containers.

#### Interacting from the Shell

At the shell prompt on a cloud node only, you can

*   Use the special `iris` utility, which along with `iris password` includes the following commands:
    
    *   `iris status` to display the status of the InterSystems IRIS instance.
        
    *   `iris info` to show information about connecting to the instance.
        
    *   `iris load` to load data into the instance from a specified GitHub repo.
        
    *   `iris help` to list the above commands.
        
*   Review the Docker compose file that was used to create the InterSystems IRIS container, located at `/opt/ISC/docker-compose.yml`.
    

At the shell prompt on any system hosting the InterSystems IRIS container, cloud node or otherwise, you can

*   See how containerization makes upgrades a snap by exploring the instance-specific data stored outside the InterSystems IRIS container.
    
    *   On the cloud node’s file system, it is in `/ISC/dur`.
        
    *   On the system hosting the container you ran from the downloaded image, it is on the volume you specified with the `--volume` option, in the directory you specified in the ISC_DATA_DIRECTORY environment variable. For example, suppose your `docker run` command included these options:
        
        ```
        --volume /home/user/iris_external:/external
        --env ISC_DATA_DIRECTORY=/external/dur
        ```
        
        In this case, the instance-specific data would be located in `/home/user/iris_external/dur` outside the container and `/external/dur` inside the container.
        
*   Issue Docker commands, including the following `docker execOpens in a new tab` command to open a shell within the InterSystems IRIS container, which is called `iris`. (The `-i` option makes the command interactive and `-t` allocates a text terminal.)
    
    ```
    docker exec -it iris bash
    ```
    
    Using the container command line you can interact directly with the containerized InterSystems IRIS instance, as described in the next section, and also explore the instance’s installation directory structure.
    

#### Interact Using the InterSystems Terminal

Open a shell within the container using `docker exec -it iris bash` as described in the previous section, then execute the InterSystems IRIS `iris` command to connect to and manage the instance using the InterSystems Terminal. For example, to open a Terminal session for the instance (which is called `IRIS`), issue the command `iris terminal IRIS`. You can also do this directly from the container host’s shell with the command `docker exec -it iris iris terminal IRIS`.

> **Note:**
> 
> As described in Ownership and Directories in Running InterSystems Products in Containers, commands issued from outside an InterSystems IRIS container using `docker exec` are executed inside the container as `irisowner`, and therefore do not require authentication. For this reason, you can use the commands cited above to open the InterSystems Terminal for the instance without being prompted for credentials.

You can also open the InterSystems IRIS SQL Shell by logging in as `sqluser`/`sqluser`.

#### Interact Using the Management Portal

To open the Management Portal for your Community Edition instance, load this URL in your browser.

`http://host-IP:52773/csp/sys/UtilHome.csp`

where `host-IP` is the IP address of the cloud node or other system hosting the container, for example `http://35.192.00.154:52773/csp/sys/UtilHome.csp`. 52773 is the default web server port, and this URL assumes it was published to the host as the same port. The specific link for your cloud node instance is shown when you connect to a cloud node using SSH, and you can display it at any time using the `iris info` command in the shell. If the container is running on your local system, you can use `127.0.0.1` or `localhost` in place of `host-IP`. If you published another host port for 52773 when you started the container, for example `--publish 99999:52773`, you need to use that host port instead, for example `http://localhost:99999/csp/sys/UtilHome.csp`.

> **Important:**
> 
> You can access the Management Portal using the URL described above only for a Community Edition instance. For information about accessing the Management Portal for other containerized InterSystems IRIS instances, see Web Access Using the Web Gateway Container in Running InterSystems Products in Containers; for information about noncontainerized instances, see Access the Management Portal and Other System Applications in the Web Gateway Guide.

When the portal opens, log in using `_SYSTEM` or one of the other predefined account usernames and

*   If you changed the default passwords using the `iris password` command or another method, the new password you provided.
    
*   If you have not yet changed the default passwords, and it is your first login to this user account, the default password `SYS`. You are immediately prompted to change it for that account, and should change it for the other predefined accounts as soon as possible.
    

The Management Portal is the comprehensive web-based user interface to an InterSystems IRIS instance. Load it in your browser to configure and manage the instance and to access the InterSystems IRIS data platform features you are interested in. For example, you can create a custom namespace and database, create resources, roles, and users for authorization and manage other InterSystems IRIS security and encryption features, and configure connectivity, national language support, and other settings. You can also explore the pages used to create and manage interoperability productions, and use the System Explorer page to examine tables, views, and stored procedures on the instance, execute SQL queries and review query plans, and review the code on the instance and the globals that provide direct programmatic access to its data. You might want to search the documentation to review everything InterSystems IRIS has to offer on a topic of interest to you.

#### Connect an Integrated Development Environment (IDE)

To connect an IDE to your Community Edition instance, you’ll need some or all of the following information:

*   The hostname or external IP address of the container’s host (as in the Management Portal link).
    
*   The host port the instance’s superserver port, 1972, was published to.
    
*   Credentials to log in to the instance, either one of the predefined account usernames with the default or new password as explained above for the Management Portal, or a new user account you have created using the Management Portal.
    

#### Develop Applications

You can develop applications on your InterSystems IRIS instance using any or all of these tools:

*   ObjectScript
    
*   Java
    
*   .NET
    
*   Python
    
*   Node.js
    
*   REST and JSON
    
*   SOAP/Web Services
    

InterSystems IRIS features multi-model databases, providing object, SQL, multidimensional, and document data access. Use the InterSystems JDBC driver or the InterSystems ODBC driver to load data into a database on your InterSystems IRIS instance.

The InterSystems IRIS Native SDKs are lightweight interfaces that let you directly access globals, the tree-based sparse arrays that form the basis of the multimodel data access capabilities of InterSystems IRIS, from your .NET, Java, Python, or Node.js code. The Java and .NET Native SDKs also enable your Java or .NET application to work with InterSystems IRIS objects as easily as if they were native Java or .NET objects.

The InterSystems API Manager (IAM) supports microservices-based applications by enabling you to monitor and direct traffic to and from your web-based APIs.

## Next Steps

Where to go from here? Take your choice of a wide range of destinations. And remember, you can always contact us for information about or help with InterSystems IRIS and other InterSystems products.

### InterSystems IRIS Learning Services

InterSystems IRIS data platform is supported by an extensive set of learning materials.

#### Introduction to InterSystems IRIS

For high-level views of InterSystems IRIS and its capabilities, see the Learn InterSystems IRIS Data Platform resource guide and the What is InterSystems IRIS? video.

#### InterSystems IRIS Online Learning

InterSystems provides a wide range of online learning materials, including introductory videos, hands-on exercises, and courses that show you how InterSystems IRIS data platform can be used to improve your systems and benefit your applications.

### InterSystems Developer Community

On the InterSystems Developer Community, you can read about and discuss InterSystems products and technologies, including InterSystems IRIS. Posts include articles, questions and answers, announcements, new feature descriptions, and videos. Both InterSystems employees and community members participate. Register on the Developer Community to ask questions about InterSystems IRIS functionality and architecture and get answers from the people who know!

### Worldwide Response Center

The Worldwide Response Center (WRC) provides expert technical assistance with InterSystems products. The center is on call 24x7x365 with staff fluent in 15 languages.

## InterSystems IRIS Community Edition Limitations

The InterSystems IRIS instance on the Community Edition cloud node is subject to certain limitations, as follows:

*   All InterSystems IRIS functionality is included except the following:
    
    *   Mirroring
        
    *   Enterprise Cache Protocol (ECP) and distributed caching
        
    *   Sharding
        
    *   InterSystems API Manager
        
*   Resource usage is limited to the following:
    
    *   Total data: 10 GB
        
    *   Connections: 8
        
    *   Cores: 20
        
*   The license for the instance expires a year after the release date for the instance’s product version.
    

> **Note:**
> 
> When upgrading InterSystems IRIS from Community Edition to another edition, installation of the new InterSystems IRIS edition is required. A change of license key is also necessary.
