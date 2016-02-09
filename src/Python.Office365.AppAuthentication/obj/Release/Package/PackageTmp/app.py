import os
from flask import Flask, request, json, redirect, session
from office365 import oauth_url, tenant_url, client_assertion, access_token, upload_file

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
c = app.config

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def hello(): 
    if 'access_token' in session:
        return '''<form method="post" action="/upload" enctype="multipart/form-data">
                    <input type="file" name="file" />
                    <input type="submit"/>
                    </form>
                '''
    redirect_uri = request.host_url + 'auth'
    url = oauth_url(redirect_uri, c['CLIENT_ID'], c['RESOURCE'], c['AUTHORITY'])
    return '<a href="' + url + '">Office365 Sign in</a>'

@app.route('/auth', methods=['POST'])
def auth():
    token_id = request.form['id_token']
    redirect_uri = request.host_url + 'auth'
    sharepoint_url = tenant_url(token_id, c['AUTHORITY'])
    assertion = client_assertion(sharepoint_url, c['CLIENT_ID'], c['CERT_THUMBPRINT'], c['CERT_PATH'])
    session['access_token'] = access_token(sharepoint_url, redirect_uri, c['CLIENT_ID'], c['RESOURCE'], assertion)
    return redirect("/")

@app.route('/upload', methods=['POST'])
def upload():
    if 'access_token' in session:
        file = request.files['file']
        success = upload_file(c['RESOURCE'], file.filename, file.stream.read(), session['access_token'])
        if success:
            result = open('success.txt', 'r')
            return '<div style="width:100px;">' + result.read() + '</div>'
    result = open('fail.txt', 'r')
    return '<div style="width:100px;">' + result.read() + '</div>'

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)