from flask import Flask
from flask import render_template, redirect

from get_tweets import get_tweets
app = Flask(__name__)

@app.route('/')
def index():
    urls = get_tweets()
    
    return render_template(
        'index.html',
        urls=urls
    )