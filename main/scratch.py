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
            return render_template("scratchpad.html", error = error, title=title, body=body)
        article_check = Articles.check_exists(title)
        if article_check:
            error = "Entry with that title already exists, choose a new one.."
            return render_template("scratchpad.html", error = error, title = title, body = body)
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
                return render_template("scratchpad.html",\
                                       title = title,\
                                       body = body,\
                                       error = error)
    else:
        return render_template("scratchpad.html")

@app.route("/create_project", methods = ["GET", "POST"])
@login_required
def create_project():
    error = None
    if request.method == "POST":
        title = request.form.get("title").strip()
        body = request.form.get("body").strip()
        user = Users.get_user_by_username(session["user"])
        if not title or not body:
            error = "Article can\'t have empty title or body"
            return render_template("scratchpad.html", error = error, title=title, body=body)
        if project_check = UserProjects.check_exists(title):
            error = "Project with that title already exists, choose another one.."
            return render_template("scratchpad.html", error = error, title = title, body = body)
        else:
            try:
                UserProjects.create_project(title = title,\
                                           body = body,\
                                           author = author)
                with app.app_context():
                    cache.clear()
                flash("Article created")
                return redirect(url_for("account", username = session["user"]))
            except:
                error = "Error occured when writing to database"
                return render_template("scratchpad.html",\
                                       title = title,\
                                       body = body,\
                                       error = error)
    else:
        return render_template("scratchpad.html")

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
            return render_template("scratchpad.html",\
                                   error = error,\
                                   title = title,\
                                   body = body)

        article_check = Articles.check_exists(title, article.id)

        if article_check:
            error = "Article with this title already exists, please choose another"
            return render_template("scratchpad.html",\
                                   error = error,\
                                   title = title,\
                                   body = body)
        else:

            try:
                Articles.update_article(article, title, body)
                with app.app_context():
                    cache.clear()
                return redirect(url_for("account", username = session["user"]))
            except:
                error = "Error writing to database"
                return render_template("scratchpad.html",\
                                       error = error,\
                                       title = title,\
                                       body = body)
    else:
        return render_template("scratchpad.html",\
                               title = article.title,\
                               body = article.body)
