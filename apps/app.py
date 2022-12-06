from flask import Flask
from flask import render_template, redirect

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder=None)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='mysql://root:kyuri0515@localhost/twitter_porn',
        SQLALCHEMY_TRACK_MODIFICATION=False
    )

    db.init_app(app)
    Migrate(app, db)
    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix='')
    return app