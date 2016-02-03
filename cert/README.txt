Sources on links:

GENERATE CERT:
http://blogs.msdn.com/b/ericnel/archive/2009/09/22/using-iis-to-generate-a-x509-certificate-for-use-with-the-windows-azure-service-management-api-step-by-step.aspx

GET CREDENTIALS:
http://blogs.msdn.com/b/exchangedev/archive/2015/01/21/building-demon-or-service-apps-with-office-365-mail-calendar-and-contacts-apis-oauth2-client-credential-flow.aspx



Step 0: (If you do not have an X.509 certificate already) Create a self-issued certificate
You can easily generate a self-issued certificate with the makecert.exe tool.
 
1.      From the command line, run: makecert -r -pe -n "CN=MyCompanyName MyAppName Cert" -b 12/15/2014 -e 12/15/2016 -ss my -len 2048
2.      Open the Certificates MMC snap-in and connect to your user account. Find the new certificate in the Personal folder and export it to a base64-encoded CER file.
 
Note: Make sure the key length is at least 2048 when generating the X.509 certificate. Shorter key length are not accepted as valid keys.
 
 
Step 1:  Get the base64 encoded cert value and thumbprint from a .cer X509 public cert file using PowerShell
 
Note: The instructions below show using Windows PowerShell to get properties of a x.509 certificate. Other platforms provide similar tools to retrieve properties of certificates.
 
$cer = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2
$cer.Import("mycer.cer")
$bin = $cer.GetRawCertData()
$base64Value = [System.Convert]::ToBase64String($bin)
 
$bin = $cer.GetCertHash()
$base64Thumbprint = [System.Convert]::ToBase64String($bin)
 
$keyid = [System.Guid]::NewGuid().ToString()
 
Store the values for $base64Thumbprint, $base64Value and $keyid, to be used in the next step.


Step 2:  Upload cert through the manifest file
 
3.      Log in to the Azure Management Portal (https://manage.windowsazure.com)
4.      Go to the AAD snap-in and there navigate to the application that you want to configure with an X.509 certificate
5.      Download the application manifest file through the Azure Management Portal
 Machine generated alternative text:
VIEW 
Manifest 
MANAGE 
MANIFEST 
UPLOAD Lca 
 
6.      Replace the empty “KeyCredentials”: [], property with the following JSON.  NOTE:  The KeyCredentials complex type is documented here:  http://msdn.microsoft.com/en-us/library/azure/dn151681.aspx
 
  "keyCredentials": [
    {
      "customKeyIdentifier": "$base64Thumbprint_from_above",
      "keyId": "$keyid_from_above",
      "type": "AsymmetricX509Cert",
      "usage": "Verify",
      "value":  "$base64Value_from_above"
     }
   ],
 
e.g.
 
  "keyCredentials": [
    {
      "customKeyIdentifier": "ieF43L8nkyw/PEHjWvj+PkWebXk=",
      "keyId": "2d6d849e-3e9e-46cd-b5ed-0f9e30d078cc",
      "type": "AsymmetricX509Cert",
      "usage": "Verify",
      "value": "MIICWjCCAgSgAwIBA***omitted for brevity***qoD4dmgJqZmXDfFyQ"
    }
  ],
 
7.      Save the change to the application manifest file.
8.      Upload the edited application manifest file through the Azure Management Portal.
9.      Optional:  Download the manifest again, and see your X.509 cert is present on the application.
 
Note:  KeyCredentials is a collection, so it’s totally possible to upload multiple X.509 certificates for rollover scenarios, or delete certs for compromise scenarios.