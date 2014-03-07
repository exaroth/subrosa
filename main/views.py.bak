# -*- coding: utf-8 -*-

"""

    main.views
    ==========

    This module implements all the basic views of Subrosa

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for more details


"""

import os
import re
from datetime import datetime
from urlparse import urljoin
import urllib
import StringIO
from main import app, db, cache, settings
from flask import render_template, redirect, flash, request, g, abort, session, url_for, send_from_directory
from .helpers import make_external, redirect_url, handle_errors, split_filename, add_thumbnail_affix, id_generator
from .pagination import Pagination
from .decorators import dynamic_content, login_required
from werkzeug import secure_filename
from werkzeug.contrib.cache import SimpleCache
from werkzeug.contrib.atom import AtomFeed
from jinja2 import evalcontextfilter, Markup
from imgur import ImgurHandler
from models.ArticlesModel import Articles
from models.UserImagesModel import UserImages
from models.UsersModel import Users





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


@app.route("/index", defaults={"page": 1})
@app.route("/", defaults={"page": 1})
@app.route("/<int:page>")
# @cache.cached(timeout=50)
def index(page):
    articles_per_page = settings.get("articles_per_page") 
    articles = Articles.get_index_articles(page, articles_per_page)
    count = articles.wrapped_count()
    show_pagination = count > articles_per_page
    articles_written = count > 0
    if not articles_written and page != 1:
        abort(404)
    pagination = Pagination(page, articles_per_page, count)
    return render_template("index.html",\
                           pagination = pagination,\
                           articles = articles,\
                           articles_written = articles_written,\
                           show_pagination = show_pagination)

@app.route("/admin", methods = ["GET", "POST"] )
def admin_login():
    user_check = Users.check_any_exist()
    if not user_check:
        return redirect(url_for("create_account"))
    if "user" in session:
        return redirect(url_for("account", username = session["user"]))

    error = None
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        user = Users.get_user_by_username(username)
        if not user:
            error = "Incorrect Credentials"
            return render_template("login.html", error = error)
        else:
            if not user.check_password(password):
                error = "Incorrect Credentials"
                return render_template("login.html", error = error)
            else:
                session["user"] = user.username
                return redirect(url_for("account", username = user.username))
    return render_template("login.html", error = error)

@app.route("/create_account", methods = ["POST", "GET"])
def create_account():
    """
    View for creating user account
    - Checks if no users have been created - if yes redirect
    - Gets Credentials from the form
    - Writes data to db
    - Creates user directory in /uploads
    - Logs user in

    """
    error = None
    user_check = Users.check_any_exist()
    if not user_check:
        if request.method == "POST":
            username = request.form.get("username").strip()
            password = request.form.get("password").strip()
            real_name = request.form.get("real_name", None).strip()
            description = request.form.get("description", None).strip()
            if not username or not password:
                error = "All fields are required"
                return render_template("create_account.html", error = error)
            try:
                Users.create_user(username = username,\
                                  password = password,\
                                  description = description,\
                                  real_name = real_name)
            except IOError, e:
                error = "Could not write to database, check if\
                        you have proper access\n or double check configuration options"
                return render_template("create_account.html", error = error)
            session["user"] = username
            flash("Account created")
            return redirect(url_for("account", username = username))
        else:
            return render_template("create_account.html")
    else:
        return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    if "user" in session:
        session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/account/<username>", methods = ["GET","POST"])
@login_required
def account(username):
    if username is None:
        return redirect("/admin")
    user = Users.get_user_by_username(username)
    if not user:
        abort(404)
    articles = Articles.get_user_articles(user.username)
    return render_template("dashboard.html",\
                           user = user,\
                           articles = articles)


@app.route("/create_article", methods = ["GET", "POST"])
@login_required
def create_article():
    error = None
    if request.method == "POST":
        title = request.form.get("title").strip()
        body = request.form.get("body").strip()
        user = Users.get_user_by_username(session["user"])
        if not title or not body:
            error = "Article can\'t have empty title or body"
            return render_template("new_article.html", error = error, title=title, body=body)
        article_check = Articles.check_exists(title)
        if article_check:
            error = "Entry with that title already exists, choose a new one.."
            return render_template("new_article.html", error = error, title = title, body = body)
        else:
            try:
                Articles.create_article(title = title,\
                                        body = body,\
                                        author = user,\
                                        draft = True)
                with app.app_context():
                    cache.clear()
                flash("Article created")
                return redirect(url_for("account", username = session["user"]))
            except:
                error = "Error occured when writing to database"
                return render_template("new_article.html",\
                                       title = title,\
                                       body = body,\
                                       error = error)
    else:
        return render_template("new_article.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_article(id):
    article = Articles.get_article(id)
    if not article:
        abort(404)
    error = None

    if article.author.username != session["user"]:
       flash("You can\'t edit other people\'s articles")
       return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title").strip()
        body = request.form.get("body").strip()
        if not title or not body:
            error = "Article can\'t have empty title or body"
            return render_template("edit_article.html",\
                                   error = error,\
                                   article = article)

        article_check = Articles.check_exists(title, article.id)

        if article_check:
            error = "Article with this title already exists, please choose another"
            return render_template("edit_article.html", error = error, article = article )
        else:

            try:
                Articles.update_article(article, title, body)
                with app.app_context():
                    cache.clear()
                return redirect(url_for("account", username = session["user"]))
            except:
                error = "Error writing to database"
                return render_template("edit_article.html",\
                                       error = error,\
                                       article = article)
    else:
        return render_template("edit_article.html", article = article)

@app.route("/articles/<string:slug>")
# @cache.cached(timeout=50)
def article_view(slug):
    article = Articles.get_article_by_slug(slug)
    if not article:
        abort(404)
    author = article.author
    next_article = Articles.get_next_article(article.id)
    previous_article = Articles.get_previous_article(article.id)
    return render_template("article_view.html",\
                            article = article,\
                            author = author,\
                            next_article = next_article,\
                            previous_article = previous_article)


@app.route("/delete_article/<int:id>")
@login_required
def delete_article(id):
    article = Articles.get_article(id)
    if not article:
        abort(404)
    if article.author.username != session["user"]:
        flash("You can\'t delete other people\'s posts")
        return redirect(url_for("index"))
    else:
        Articles.delete_article(article)
        with app.app_context():
            cache.clear()
        flash("Article has been deleted")
        return redirect(url_for("account", username = session["user"]))

@app.route("/publish_article/<int:id>")
@login_required
def publish_article(id):
    article = Articles.get_article(id)
    if not article:
        abort(404)
    if article.author.username != session["user"]:
        flash("You can\'t publish other\'s peoples posts")
        return redirect(url_for("index"))
    else:
        Articles.publish_article(article)
        with app.app_context():
            cache.clear()
        flash("Article has been published")
        return redirect(url_for("account", username = session["user"]))


@app.route("/upload_image", methods = ["GET", "POST"])
@login_required
@dynamic_content
def upload_image():
    error = None
    if request.method == "POST":
        description = request.form.get('description', None)
        if request.form.get("imgur-img"):
            user_id = settings.get("imgur_id", None)
            image = request.files["image"]
            if not image:
                error = "No image chosen"
                return render_template("upload_image.html", error = error)
            extension = split_filename(image.filename, True)
            if extension not in app.config["ALLOWED_FILENAMES"]:
                error = "Allowed extensions are %r" % (", ".join(app.config["ALLOWED_FILENAMES"]))
                return render_template("upload_image.html", error = error)
            filename = secure_filename(image.filename.strip())
            user = Users.get_user_by_username(session["user"])
            config = dict(
                image = image,
                name = filename,
                description = description
            )
            response = ImgurHandler(user_id, config).send_image()
            if not response["success"]:
                error = "Error uploading to imgur"
                return render_template("upload_image.html", error = error)
            response_data = response["data"]
            image_link = response_data["link"]
            is_vertical = response_data["width"] + 10 < response_data["height"]
            delete_hash = response_data["deletehash"]
            try:
                UserImages.add_image(image_link = image_link,\
                                    description = description,\
                                    delete_hash = delete_hash,\
                                    is_vertical = is_vertical,\
                                    imgur_img = True,\
                                    owner = user)

                return redirect(url_for("user_images", username = user.username))
            except:
                error = "Error writing to database"
                return render_template("upload_image.html", error = error)
            return render_template("upload_image.html", error = response)
        elif request.form.get('save-link'):
            link = request.form.get('image-link', None)
            if not link:
                error = "No link given"
                return render_template("upload_image.html", error = error)
            user = Users.get_user_by_username(session["user"])
            try:
                UserImages.add_image(image_link = link,\
                                    description = description,\
                                    is_vertical = True,\
                                    imgur_img = False,\
                                    owner = user)
                return redirect(url_for("user_images", username = user.username))
            except Exception as e:
                error = "Error writing to database"
                return render_template("upload_image.html", error = error)
    else:
        return render_template("upload_image.html")

@app.route("/images/<username>", defaults={"page": 1})
@app.route("/images/<username>/<int:page>")
@login_required
@dynamic_content
def user_images(username, page):
    per_page = settings.get("images_per_page", 10)
    images = UserImages.get_gallery_images(page = page,\
                                           per_page = per_page,\
                                           username = username)
    show_pagination = images.wrapped_count() > per_page
    images_uploaded = bool(tuple(images))
    if not tuple(images) and page != 1:
        abort(404)
    pagination = Pagination(page, per_page, images.wrapped_count() )
    return render_template("user_images.html",\
                           images_uploaded = images_uploaded,\
                           pagination = pagination,\
                           show_upload_btn = True,\
                           images = images,\
                           show_pagination = show_pagination)

@app.route("/delete_image/<int:id>")
@login_required
@dynamic_content
def delete_image(id):
    image = UserImages.get_image(id)
    if not image:
        abort(404)
    if image.owner.username != session["user"]:
        flash("Don't try to delete other\'s dude\'s pictures...dude")
        return redirect(url_for("index"))
    else:
        try:
            UserImages.delete_image(image)
        except:
            error = "Error occured when writing to database"
            flash(error)
            return redirect(url_for("index"))
        if image.imgur_img:
            resp = ImgurHandler(settings["imgur_id"]).delete_image(image.delete_hash)
            if not resp["success"]:
                handle_errors(resp)
        return redirect(url_for("user_images", username = session["user"]))

@app.route("/gallerify/<int:id>")
@login_required
def gallerify(id):
    """ Ads and removes image from gallery """
    image = UserImages.get_image(id)
    if not image:
        return redirect(url_for("user_images", username = session["user"]))
    UserImages.gallerify(image)
    return redirect(url_for("user_images", username = session["user"]))


@app.route("/gallery", defaults = {"page": 1})
@app.route("/gallery/<int:page>")
def gallery(page):
    if not app.config.get("GALLERY", None):
        return redirect(url_for("index"))
    per_page = settings.get("images_per_page", 10)
    images = UserImages.get_gallery_images(page = page,\
                                           per_page = per_page,\
                                           gallery = True)
    if not tuple(images) and page != 1:
        abort(404)
    count = images.wrapped_count()
    show_pagination = count > per_page
    images_uploaded = count > 0
    pagination = Pagination(page, per_page, count)
    return render_template("gallery.html",\
                           images_uploaded = images_uploaded,\
                           pagination = pagination,\
                           images = images,\
                           show_pagination = show_pagination)


@app.route("/recent.atom")
def recent_feeds():
    """
    Generates Atom feeds
    Snippet created by Armin Ronacher
    """
    feed = AtomFeed("Recent Posts", 
        feed_url = request.url, url = request.url_root)

    articles = Articles.select().limit(15)

    for article in articles:
        feed.add(article.title, unicode(article.body)[:320],
            content_type = "html",
            author = article.author,
            updated = article.date_updated,
            url = make_external(article.id),
            published = article.date_created
            )

    return feed.get_response()

@app.route("/uploads/<path:filename>")
@dynamic_content
def send_image(filename):
    """
    Allows sending images from upload folder
    """
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)



@app.context_processor
def utility_processor():
    return dict(settings = settings,\
                current_path = request.url_root + request.path[1:],
                add_thumbnail_affix = add_thumbnail_affix
        )

@app.errorhandler(404)
def http_not_found(err):
    return render_template("error.html"), 404

@app.errorhandler(500)
def server_error(err):
    return render_template('error.html'), 500


