from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from celery import Celery
from celery.schedules import crontab
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase

# initializing flask and related apps
app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

CORS(app, supports_credentials=True) # allows cookies from frontend


# configuring app level settings
app.config["SECRET_KEY"] = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"
app.config["JWT_SECRET_KEY"] = "SUPER_SECRET_JWT_KEY"
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"


celery_app = Celery(
    "tasks", 
    backend=app.config["CELERY_RESULT_BACKEND"], 
    broker=app.config["CELERY_BROKER_URL"],
)
celery_app.autodiscover_tasks()
# celery_app.conf.beat_schedule = {
#     'generate-report-every-min': {
#         'task': 'fns.generate_csv_report_task',
#         'schedule': crontab(minute=1),
#     }
# }


jwt = JWTManager(app)
