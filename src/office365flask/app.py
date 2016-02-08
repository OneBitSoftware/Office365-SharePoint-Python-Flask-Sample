import os
from flask import Flask, request, redirect, session, render_template, url_for, flash
from office365 import login_url, issuance_url, access_token, upload_file

# Init the flask app.
app = Flask(__name__)

# Load confuguration variables.
app.config.from_pyfile('app.cfg')
c = app.config

# Make the WSGI interface available at the top level so wfastcgi can get it.
# The WSGI interface is needed for Azure deployment. 
wsgi_app = app.wsgi_app

# Routes and views for the flask application.
@app.route('/')
def home(): 
    # Renders the home page. 
    redirect_uri = '{0}auth'.format(request.host_url)
    # Generates Azure AD authorization endpoint url with parameters so the user authenticates and consents, if consent is required.
    url = login_url(redirect_uri, c['CLIENT_ID'], c['RESOURCE'], c['AUTHORITY'])
    # Renders the index template with additional prams for the login url and a bool is_authenticated if access token is stored in session.
    return render_template('index.html', url=url, is_authenticated='access_token' in session)

@app.route('/auth', methods=['POST'])
def auth():
    # Handles the Azure AD authorization endpoint response and sends second repsonse to get access token. 
    # Gets the token_id from the flask response form dictionary.
    token_id = request.form['id_token']
    # Gets the authorization code from the flask response form dictionary.
    code = request.form['code']
    # Constructs redirect uri to be send as query string param to Azure AD token issuance endpoint.
    redirect_uri = '{0}auth'.format(request.host_url)
    # Constructs Azure AD token issuance endpoint url.
    url = issuance_url(token_id, c['AUTHORITY'])
    # Requests access token and stores it in session.
    session['access_token'] = access_token(url, redirect_uri, c['CLIENT_ID'], code, c['CLIENT_SECRET'])
    return redirect(url_for('home'))

@app.route('/upload', methods=['POST'])
def upload():
    # Uploads file to SharePoint Tenant.
    if 'access_token' in session:
        # File from the submitted upload form.
        file = request.files['file']
        # Sends request to SharePoint api with the file.
        success = upload_file(c['RESOURCE'], file.filename, file.stream.read(), session['access_token'])
        if success:
            # Success flash message if the file is successfully uploaded.
            flash('You successfully uploaded file {0}'.format(file.filename))
        else:
            flash('Could not upload file {0}'.format(file.filename))
    return redirect(url_for('home'))


# This script runs the application using a development server.
if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)