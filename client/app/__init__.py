from flask import Flask

app = Flask(__name__)
app.secret_key = "secret_key"

CLIENT_PORT = '5000'
ORGANIZATION_PORT = '5001'

from client.app import views
