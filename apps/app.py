from flask import Flask
from flask import render_template, redirect

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder=None)

    app.config.from_envvar("APPLICATION_SETTINGS")

    db.init_app(app)
    Migrate(app, db)
    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix='')
    return app