import os
from flask import Flask, request, json, redirect, session, render_template, url_for, flash
from office365 import login_url, tenant_url, client_assertion, access_token, upload_file

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
c = app.config

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def home(): 
    redirect_uri = '{0}auth'.format(request.host_url)
    url = login_url(redirect_uri, c['CLIENT_ID'], c['RESOURCE'], c['AUTHORITY'])
    return render_template('index.html', url=url, is_authenticated='access_token' in session)

@app.route('/auth', methods=['POST'])
def auth():
    token_id = request.form['id_token']
    redirect_uri = request.host_url + 'auth'
    sharepoint_url = tenant_url(token_id, c['AUTHORITY'])
    assertion = client_assertion(sharepoint_url, c['CLIENT_ID'], c['CERT_THUMBPRINT'], c['CERT_PATH'])
    session['access_token'] = access_token(sharepoint_url, redirect_uri, c['CLIENT_ID'], c['RESOURCE'], assertion)
    return redirect(url_for('home'))

@app.route('/upload', methods=['POST'])
def upload():
    if 'access_token' in session:
        file = request.files['file']
        success = upload_file(c['RESOURCE'], file.filename, file.stream.read(), session['access_token'])
        if success:
            flash('You successfully uploaded file {0}'.format(file.filename))
        else:
            flash('Could not upload file {0}'.format(file.filename))
    return redirect(url_for('home'))

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)