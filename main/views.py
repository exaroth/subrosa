# -*- coding: utf-8 -*-

"""

    main.views
    ~~~~~~~~~~

    This module implements all the basic views of Subrosa

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: BSD, see LICENSE for more details


"""

import os
from datetime import datetime
from urlparse import urljoin
import urllib
from main import app, db, cache, settings
from flask import render_template, redirect, flash, request, g, abort, session, url_for, send_from_directory
from .models import Users, Articles, UserImages
from .helpers import process_image, make_external, redirect_url, handle_errors
from .pagination import Pagination
from .decorators import dynamic_content, login_required
from werkzeug import secure_filename
from werkzeug.contrib.cache import SimpleCache
from werkzeug.contrib.atom import AtomFeed




@app.before_request
def load_vars():
    g.title = app.config["TITLE"]
    g.dynamic = app.config.get("DYNAMIC_SITE")
    g.prev = redirect_url()
    g.facebook = app.config.get("FACEBOOK", False)
    g.twitter = app.config.get("TWITTER", False)
    g.github = app.config.get("GITHUB", False)
    g.gallery = app.config.get("GALLERY", False)

@app.before_request
def db_connect():
    g.db = db
    g.db.connect()

@app.teardown_request
def db_disconnect(response):
    g.db.close()
    return response


@app.route("/", defaults={"page": 1})
@app.route("/<int:page>")
# @cache.cached(timeout=50)
def index(page):
    pages_per_page = app.config.get("ARTICLES_PER_PAGE", 5)
    articles = Articles.get_index_articles(page, pages_per_page)
    if not tuple(articles) and page != 1:
        abort(404)
    return render_template("index.html", settings = settings, articles = articles)

@app.route("/index", methods = ["GET"])
def redirect_index():
    return redirect(url_for("index"))

@app.route("/admin", methods = ["GET", "POST"] )
def admin_login():
    user_check = Users.check_any_exist()
    if not user_check:
        return redirect(url_for("create_account"))
    if "user" in session:
        return redirect(url_for("account", username = session["user"]))

    error = None
    if request.method == "POST":
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
            email = request.form.get("email").strip()
            password = request.form.get("password").strip()
            real_name = request.form.get("real_name", None).strip()
            if not username or not email or not password:
                error = "All fields are required"
                return render_template("create_account.html", error = error)
            try:
                Users.create_user(username = username, email = email,\
                             password = password, real_name = real_name)
            except IOError, e:
                error = "Could not write to database, check if\
                        you have proper access\n or double check configuration options"
                return render_template("create_account.html", error = error)
            try:
                os.mkdir(app.config["UPLOAD_FOLDER"] + username, 0755)
                os.mkdir(app.config["UPLOAD_FOLDER"] + username + "/showcase", 0755)
            except IOError, e:
                error = "Could not create user directories, check\
                        if you have proper credentials"
                handle_errors(error)
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
    return render_template("dashboard.html",user = user, articles = articles)


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
            return render_template("edit_article.html", error = error, article = article)

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
                return render_template("edit_article.html", error = error, article = article )
    else:
        return render_template("edit_article.html", article = article)

@app.route("/article/<int:id>")
@cache.cached(timeout=50)
def article_view(id):
    article = Articles.get_article(id)
    if not article:
        abort(404)
    return render_template("article_view.html", article = article)

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
        if request.form.get("upload-img"):
            image = request.files["image"]
            description = request.form.get("description", None)
            if not image:
                error = "No image chosen"
                return render_template("upload_image.html", error = error)
            if os.path.splitext(image.filename)[1][1:] not in app.config["ALLOWED_FILENAMES"]:
                error = "Allowed extensions are %r" % (", ".join(app.config["ALLOWED_FILENAMES"]))
                return render_template("upload_image.html", error = error)
            # add checkbox functionality
            filename = secure_filename(image.filename.strip())
            image_exists = UserImages.check_exists(filename)
            if image_exists:
                error = "Image with this filename already exists"
                return render_template("upload_image.html", error = error)
            # !db fn
            user = Users.get_user_by_username(session["user"])
            try:
                image_filename, show_filename, is_vertical = process_image(image = image, filename = filename , username = user.username)
                # mess
                show_path = request.url_root + "uploads/" + user.username + "/showcase/" + show_filename
                full_path = request.url_root + "uploads/" + user.username + "/" + image_filename
                try:
                    UserImages.add_image(filename = full_path,\
                                        showcase = show_path,\
                                        description = description,\
                                        is_vertical = is_vertical,\
                                        external = False,\
                                        owner = user)
                    return redirect(url_for("user_images", username = user.username))
                except:
                    error = "Error writing to database"
                    return render_template("upload_image.html", error = error)
            except Exception, e:
                error = "Error occured while processing the image"
                handle_errors(error)
                return render_template("upload_image.html", error = error)
        elif request.form.get('save-link'):
            link = request.form.get('image-link', None)
            if not link:
                error = "No link given"
                return render_template("upload_image.html", error = error)
            # check for existence
            description = request.form.get('description', None)
            user = Users.get_user_by_username(session["user"])
            try:
                UserImages.add_image(filename = link,\
                                    showcase = link,\
                                    description = description,\
                                    # mess
                                    is_vertical = True,\
                                    external = True,\
                                    owner = user)
                return redirect(url_for("user_images", username = user.username))
            except Exception as e:
                error = "Error writing to database"
                print e
                return render_template("upload_image.html", error = error)
    else:
        return render_template("upload_image.html")

@app.route("/images/<username>", defaults={"page": 1})
@app.route("/images/<username>/<int:page>")
@login_required
@dynamic_content
def user_images(username, page):
    images = UserImages.get_gallery_images(username, page, app.config.get("IMAGES_PER_PAGE"))
    url_path = urljoin(request.url_root, "uploads/")
    if not tuple(images) and page != 1:
        abort(404)
    return render_template("user_images.html", show_upload_btn = True, images = images, url_path = url_path)

@app.route("/delete_image/<int:id>")
@login_required
@dynamic_content
def delete_image(id):
    image = UserImages.get_image(id)
    if not image:
        abort(404)
    filename = image.filename.rsplit('/', 1)[-1]
    showcase = image.showcase.rsplit('/', 1)[-1]
    # prevent from deleting images by people other by the owner
    if image.owner.username != session["user"]:
        flash("Don't try to delete other\'s dude\'s pictures...dude")
        return redirect(url_for("index"))
    else:
        if not image.external:
            try:
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], image.owner.username, filename))
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], image.owner.username, 'showcase', showcase))
            except IOError, e:
                flash("Can\'t delete files from disk")
                return redirect(url_for("index"))
        try:
            UserImages.delete_image(image)
        except:
            error = "Error occured when writing to database"
            flash(error)
            return redirect(url_for("index"))
        return redirect(url_for("user_images", username = session["user"]))

@app.route("/gallerify/<int:id>")
@login_required
def gallerify(id):
    return "yes"


# probably needs auth
@app.route("/image_details/<int:id>")
@dynamic_content
def image_details(id):
    image = UserImages.get_image(id)
    if not image:
        abort(404)
    try:
        filename = image.filename.rsplit('/', 1)[1] 
    except:
        filename = image.filename
    return render_template("image_details.html",filename = filename, image = image)


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

@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.utcnow()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )
    for period, singular, plural in periods:
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)
    return default

@app.errorhandler(404)
def http_not_found(err):
    return render_template("error.html"), 404

