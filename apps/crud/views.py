from flask import Blueprint, render_template
from apps.app import db
from apps.get_tweets import get_tweets
from apps.crud.models import URLs

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="static"
)

@crud.route("/")
def index():

    urls = db.session.query(URLs).all()

    return render_template(
        'crud/index.html',
        urls=urls
    )