from flask import Flask
from flask_restful import  Api
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config())
api = Api(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

from app import routes
