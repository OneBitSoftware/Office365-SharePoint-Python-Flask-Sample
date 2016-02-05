import uuid, jwt, requests
from six.moves.urllib.parse import quote

def login_url(redirect_uri, client_id, resource, authority):
    params = '?client_id='+client_id
    params += '&redirect_uri='+quote(redirect_uri)
    params += '&response_type=code+id_token'
    params += '&scope=openid'
    params += '&nonce='+str(uuid.uuid4())
    params += '&response_mode=form_post'
    params += '&resource='+quote(resource)
    return '{0}/common/oauth2/authorize{1}'.format(authority, params)

def tenant_url(id_token, authority):
    tenant_id = jwt.decode(id_token, verify=False)['tid'] 
    return '{0}/{1}/oauth2/token'.format(authority, tenant_id)

def access_token(tenant_url, redirect_uri, client_id, code, client_secret):
    data = { 'client_id': client_id,
             'client_secret': client_secret,
             'grant_type': 'authorization_code',
             'code': code,
             'redirect_uri': redirect_uri }
    return requests.post(tenant_url, data=data).json()['access_token']

def upload_file(url, fname, file, token):
    headers = { 'Content-Type':'application/json',
                'Authorization': 'Bearer {0}'.format(token) }
    r = requests.post("{0}/_api/web/lists/getbytitle('Documents')/rootfolder/files/add(url='{1}', overwrite=true)".format(url, fname), data=file, headers=headers)
    return r.status_code == 200
