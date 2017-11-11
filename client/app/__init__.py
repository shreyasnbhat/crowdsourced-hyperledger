from flask import Flask

app = Flask(__name__)
app.secret_key = "secret_key"

CLIENT_PORT = '9898'
ORGANIZATION_PORT = '9899'

from client.app import views
