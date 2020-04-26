from flask import Flask
import os
# from werkzeug.routing import BaseConverter
# from models import StrListUrl


app = Flask(__name__)

# app.url_map.converters['str_list'] = StrListUrl

# Two ways to correctly create db file: 1 with import os and relative path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(BASE_DIR, 'flapi.db')
app.config['FLASK_ENV'] = 'development'
# or: 2. with absolute path
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/morfina/PycharmProjects/P12FlApi/database.db'

# number of :/ is the key...

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True
app.config['CSRF_SESSION_KEY'] = "43g4vh368ds58!645fdg583t76e"
app.config['SECRET_KEY'] = "345fdghg4vh368ds5f!45fdg"
