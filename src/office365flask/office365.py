import uuid, jwt, requests
from six.moves.urllib.parse import quote

def login_url(redirect_uri, client_id, resource, authority):
    # Generates Azure AD authorization endpoint url with parameters so the user authenticates and consents, if consent is required.
    params = '?client_id='+client_id
    params += '&redirect_uri='+quote(redirect_uri)
    # Will request id_token and also authorization code.
    params += '&response_type=code+id_token'
    params += '&scope=openid'
    params += '&nonce='+str(uuid.uuid4())
    params += '&response_mode=form_post'
    params += '&resource='+quote(resource)
    # Azure AD authorization endpoint url.
    return '{0}/common/oauth2/authorize{1}'.format(authority, params)

def issuance_url(id_token, authority):
    # id_token is JSON Web Token and it can be decoded with PyJWT.
    # Extracting 'tid' from the decoded id_token dictionary would provide the tenant id.
    tenant_id = jwt.decode(id_token, verify=False)['tid'] 
    # The tenant id is used to construct the Azure AD token issuance endpoint url.
    return '{0}/{1}/oauth2/token'.format(authority, tenant_id)

def access_token(issuance_url, redirect_uri, client_id, code, client_secret):
    # Initialize access token request payload
    data = { 'client_id': client_id,
             'client_secret': client_secret,
             'grant_type': 'authorization_code',
             'code': code,
             'redirect_uri': redirect_uri }
    # Sends post request to the Azure AD token issuance endpoint with the payload included in the body.
    # Access token to be aquired on successful response.
    return requests.post(issuance_url, data=data).json()['access_token']

def upload_file(url, fname, file, access_token):
    # Sets request headers with the access token included
    headers = { 'Content-Type':'application/json',
                'Authorization': 'Bearer {0}'.format(access_token) }
    # Post requrest to the SharePoint api with OData query for document upload.
    r = requests.post("{0}/_api/web/lists/getbytitle('Documents')/rootfolder/files/add(url='{1}', overwrite=true)".format(url, fname), data=file, headers=headers)
    return r.status_code == 200
