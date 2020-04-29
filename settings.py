from flask import Flask
import os

app = Flask(__name__)

# Two ways to correctly create db file: 1 with import os and relative path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(BASE_DIR, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True
app.config['CSRF_SESSION_KEY'] = "flapi"
app.config['SECRET_KEY'] = "flapi"
