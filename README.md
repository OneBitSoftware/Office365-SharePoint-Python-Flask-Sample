# Office 365 Python Flask App Authentication #

### Summary ###
This scenario shows authentication between Python Flask app and Office365 SharePoint Online site. The goal of this sample is to show how user can authenticate from Python Flask app and interact with Office365 SharePoint site.

### Applies to ###
- Office 365 Multi Tenant (MT)
- Office 365 Dedicated (D)

### Prerequisites ###
- Office 365 developer tenant
- Visual Studio 2015 installed
- Python Tools for Visual Studio installed
- Python 2.7 or 3.4 installed
- Flask, requests, PyJWT Python packages installed via pip

### Solution ###
Solution | Author(s)
---------|----------
Python.Office365.AppAuthentication | Velin Georgiev (**OneBit Software**), Radi Atanassov (**OneBit Software**)

### Version history ###
Version  | Date | Comments
---------| -----| --------
1.0  | February 9th 2016 | Initial release (Radi Atanassov)

### Disclaimer ###
**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

----------

# The Office 365 Python Flask App Authentication Sample #
This section describes the Office 365 Python Flask App Authentication sample included in the current solution.

# Prepare the scenario for the Office 365 Python Flask app authentication sample #
The Office 365 Python Flask application will:

- Use Azure AD authorization endpoints to perform authentication
- Use Office 365 SharePoint API's to show the authenticated user title

For these tasks to succeed you need to do additional setups explained below. 

- Create Azure trial account with the Office 365 account so the app can be registered. Good tutorial can be found on this link https://github.com/jasonjoh/office365-azure-guides/blob/master/RegisterAnAppInAzure.md.
- Register the app in the Azure portal and assign http://localhost:5555 to the Sign-on URL and Reply URL
- Generate client secret
- Grant the following permission the Python Flask app: Office 365 SharePoint Online > Delegated Permissions > Read user profiles

![](https://lh3.googleusercontent.com/-LxhYrbik6LQ/VrnZD-0Uf0I/AAAAAAAACaQ/jsUjHDQlmd4/s732-Ic42/office365-python-app2.PNG)

- Copy the client secret and the client id from the Azure portal and replace them into the Python Flask config file
- Assign URL to the SharePoint site you are going to access to the RESOURCE config variable.

![](https://lh3.googleusercontent.com/-ETtW5MBuOcA/VrnZDQBAxQI/AAAAAAAACaY/ppp4My1JTlE/s616-Ic42/office365-python-app-config.PNG)

- Open the sample in Visual Studio 2015
- Go to Project > Properties > Debug and dedicate 5555 for Port Number

![](https://lh3.googleusercontent.com/-M3upxeCKBN0/VrnZDSHnDoI/AAAAAAAACaA/BF4CTeKlUMs/s426-Ic42/office365-python-app-vs-config.PNG)

- Go to Python environments > your active python environment > execute "Install from requirements.txt". This will ensure all the required packages are installed.

![](https://lh3.googleusercontent.com/-At6Smrxg9DQ/VrnZD6KMvfI/AAAAAAAACaM/gcgJUATPigE/s479-Ic42/office365-python-packages.png)

## Run the Office 365 Python Flask app sample ##
When you run the sample you'll see title and login url.

![](https://lh3.googleusercontent.com/-GDdAcmYylZE/VrnZD8sVGwI/AAAAAAAACaI/1gB0jvULLBo/s438-Ic42/office365-python-app.PNG)


Once you've logged on the Office 365 API will you will be redirected to the Python Flask home screen with the logged in user title and access token shown:

![](https://lh3.googleusercontent.com/-44rsAE2uGFQ/VrnZDdJAseI/AAAAAAAACaE/70N8UX8ErIk/s569-Ic42/office365-python-app-result.PNG)
