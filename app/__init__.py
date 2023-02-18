from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from config import config

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
ck = CKEditor()

from . import dbModels


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    ck.init_app(app)

    from .admin import admin
    app.register_blueprint(admin, url_prefix='/Admin')

    from .main import main
    app.register_blueprint(main)

    return app
