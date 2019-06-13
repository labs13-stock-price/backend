from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.contrib.fixers import ProxyFix



app = Flask(__name__)
app.config.from_object(Config)

app.wsgi_app = ProxyFix(app.wsgi_app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'


from app import views, models