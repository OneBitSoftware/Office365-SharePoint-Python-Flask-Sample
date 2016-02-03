'Param([string]$certFilePath)'
$certFilePath = "E:\Projects\office365app\cert\office365flask.cer"
$cer = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2
$cer.Import($certFilePath)

$outFile = ".\keyCredentials.txt"
Clear-Content $outFile

Write-Host "Loading certificate from" $certFilePath

$cer = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2
$cer.Import($certFilePath)

$data = $cer.GetRawCertData()
$base64Value = [System.Convert]::ToBase64String($data)

$hash = $cer.GetCertHash()
$base64Thumbprint = [System.Convert]::ToBase64String($hash)

$keyid = [System.Guid]::NewGuid().ToString()

Add-Content $outFile '"keyCredentials": ['
Add-Content $outFile '  {'
$stringToAdd = '    "customKeyIdentifier": "' + $base64Thumbprint + '",'
Add-Content $outFile $stringToAdd
$stringToAdd = '    "keyId": "' + $keyid  + '",'
Add-Content $outFile $stringToAdd
Add-Content $outFile '    "type": "AsymmetricX509Cert",'
Add-Content $outFile '    "usage": "Verify",'
$stringToAdd = '    "value": "'  + $base64Value + '"'
Add-Content $outFile $stringToAdd
Add-Content $outFile '  }'
Add-Content $outFile '],'

Write-Host "Key Credential entry created in" $outFile