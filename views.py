from flask import (
    render_template,
    session,
    request,
    redirect,
    url_for,
    flash,
    abort,
    send_file,
    send_from_directory,
)
import requests

from app import app
from models import Concordance


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/concordance/<carrel>")
def concordance_view(carrel):
    c = carrel_to_concordance(carrel)
    return render_template("concordance.html", concordance=c)


def carrel_to_concordance(carrel):
    source_url = app.config['CARREL_URL'] % carrel
    r = requests.get(source_url)
    if r.status_code != 200:
        print(source_url, r.status_code)
        return None
    c = Concordance()
    c.FromText(r.text)
    return c


