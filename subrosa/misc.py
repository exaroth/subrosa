# -*- coding: utf-8 -*-


from subrosa import app, settings, db
from flask import request, render_template, g
from .helpers import redirect_url


@app.errorhandler(404)
def http_not_found(err):
    return render_template("error.html"), 404


@app.before_request
def load_vars():
    g.prev = redirect_url()


@app.before_request
def db_connect():
    g.db = db
    g.db.connect()


@app.teardown_request
def db_disconnect(response):
    g.db.close()
    return response
