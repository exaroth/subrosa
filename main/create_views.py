#-*- coding: utf-8 -*-
"""

    main.create_views
    ===============
    
    implements class-based views related to creating stuff

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.

"""


from flask import render_template, request, session, url_for, redirect, flash
from main.models.UsersModel import Users
from main.models.ArticlesModel import Articles
from main.models.UserProjectsModel import UserProjects
from main import app, cache
from main.base_views import ScratchpadView





class CreateView(ScratchpadView):

    def get_get_model(self):
        raise NotImplementedError()

    def create_method(self):
        raise NotImplementedError()

    def get(self):
        return self.render_template()

    def post(self):
        title = request.form.get("title").strip()
        body = request.form.get("body").strip()
        user = Users.get_user_by_username(session["user"])
        context = dict(title = title, body = body, author = user)
        if not title or not body:
            error = "Entry can\'t have empty title or body"
            context.update(dict(error = error))
            return self.render_template(context)
        model = self.get_model()
        check = model.check_exists(title)
        if check:
            error = "Entry with that title already exists, choose a new one.."
            context.update(dict(error = error))
            return self.render_template(context)

        else:
            additional = self.get_context()
            context.update(additional)
            try:
                func = getattr(model, self.create_method())
                func(**context)
                with app.app_context():
                    cache.clear()
                flash("Created")
                return redirect(url_for("account", username = session["user"]))
            except Exception as e:
                print e
                error = "Processing error see error.log for details"
                context.update(dict(error = error))
                return self.render_template(context)


class CreateArticleView(CreateView):

    def get_model(self):
        return Articles

    def create_method(self):
        return "create_article"

    def get_context(self):
        return dict(draft = True)

class CreateProjectView(CreateView):
    
    def get_model(self):
        return UserProjects

    def create_method(self):
        return "create_project"



        
