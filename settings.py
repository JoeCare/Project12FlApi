from flask import Flask
import os

app = Flask(__name__)

# Two ways to correctly create db file: 1 with import os and relative path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(BASE_DIR, 'database.db')
app.config['FLASK_ENV'] = 'development'
# or: 2. with absolute path
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/morfina/PycharmProjects/P12FlApi/database.db'

# number of :/ is the key...

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True
app.config['CSRF_SESSION_KEY'] = "43g4vh368ds58!645fdg583t76e"
app.config['SECRET_KEY'] = "345fdghg4vh368ds5f!45fdg"
