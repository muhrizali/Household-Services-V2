from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase

# initializing flask and related apps
app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True) # allows cookies from frontend
bcrypt = Bcrypt(app)


# configuring app level settings
app.config["SECRET_KEY"] = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"
# app.config["SESSION_TYPE"] = "filesystem"

app.config["JWT_SECRET_KEY"] = "SUPER_SECRET_JWT_KEY"

jwt = JWTManager(app)

# Session(app)
