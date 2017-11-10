from flask import Flask

app = Flask(__name__)
app.secret_key = 'secret_key'

from app import views

