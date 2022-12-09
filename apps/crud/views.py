from flask import Blueprint, render_template
from apps.app import db
from apps.get_tweets import get_tweets
from apps.crud.models import URLs

from sqlalchemy.dialects.mysql import insert

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="static"
)

@crud.route("/")
def index():
    new_urls = get_tweets()
    existing_urls = db.session.query(URLs).all()

    for new_url in new_urls:
        duplicate_flag = False

        for existing_url in existing_urls:
            if existing_url.url == new_url.url:
                duplicate_flag = True

        if duplicate_flag == False:
            db.session.add(new_url)
            db.session.commit()

    urls = db.session.query(URLs).all()

    return render_template(
        'crud/index.html',
        urls=urls
    )