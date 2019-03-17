from flask import Flask
app = Flask(__name__)
from models import recent_rankings


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/entry/<entry_name>")
def entry(entry_name):
    return recent_rankings()
