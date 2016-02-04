import uuid, jwt, base64, json, requests, time
from urllib import quote_plus

def login_url(redirect_uri, client_id, resource, authority):
    params = '?client_id='+client_id
    params += '&redirect_uri='+quote_plus(redirect_uri)
    params += '&response_type=id_token'
    params += '&scope=openid'
    params += '&nonce='+str(uuid.uuid4())
    params += '&prompt=admin_consent'
    params += '&response_mode=form_post'
    params += '&resource='+quote_plus(resource)
    return '{0}/common/oauth2/authorize{1}'.format(authority, params)

def tenant_url(id_token, authority):
    tenant_id = jwt.decode(id_token, verify=False)['tid'] 
    return '{0}/{1}/oauth2/token'.format(authority, tenant_id)

def client_assertion(tenant_url, client_id, cert_tprint, cert_path):
    now = int(time.time()) - 300 #time skew between two machines
    header =  { 'alg': 'RS256', 'x5t': cert_tprint }
    payload = { 'sub': client_id,
                'iss': client_id,
                'jti': str(uuid.uuid4()),
                'exp': now + 900,
                'nbf': now,
                'aud': tenant_url }
    key = open(cert_path, 'r').read()
    return jwt.encode(payload, key, 'RS256', header)

def access_token(tenant_url, redirect_uri, client_id, resource, client_assertion):
    data = { 'resource': resource,
             'client_id': client_id,
             'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
             'client_assertion': client_assertion,
             'grant_type': 'client_credentials',
             'redirect_uri': redirect_uri }
    r = requests.post(tenant_url, data=data)
    return r.json()['access_token']

def upload_file(url, fname, file, token):
    headers = { 'Content-Type':'application/json',
                'Authorization': 'Bearer {0}'.format(token),
                'User-Agent': 'python_clientcred/1.0',
                'Accept': 'application/json'
               }
    r = requests.post("{0}/_api/web/lists/getbytitle('Documents')/rootfolder/files/add(url='{1}', overwrite=true)".format(url, fname), data=file, headers=headers)
    return r.status_code == 200
