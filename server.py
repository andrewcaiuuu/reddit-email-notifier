from os import environ
from flask import Flask

app = Flask(__name__)
app.run_server(port=environ.get('PORT'))