# -*- coding: utf-8 -*-
"""

    main.edit_views
    ===============
    

    Implements views related to updating stuff

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.

"""

from main.base_views import ScratchpadView
from flask import render_template, request, session, url_for, redirect, flash, abort
from main.models.UsersModel import Users
from main.models.ArticlesModel import Articles
from main.models.UserProjectsModel import UserProjects
from main import app, cache


class UpdateView(ScratchpadView):

    def get_model(self):
        raise NotImplementedError()

    def create_method(self):
        raise NotImplementedError()

    def get_object(self):
        raise NotImplementedError()
    

    def get(self, id):
        object = self.get_object(id)
        if not object or object.author.username != session["user"]:
            abort(404)

        context = dict(title = object.title, body = object.body)
        return self.render_template(context)

    def post(self, id):
        title = request.form.get("title").strip()
        body = request.form.get("body").strip()
        context = dict(title = title, body = body)
        if not title or not body:
            error = "Entry can\'t have empty title or body"
            context.update(dict(error = error))
            return self.render_template(context)
        model = self.get_model()
        check = model.check_exists(title, id)
        if check:
            error = "Entry with this title already exists, please choose another"
            context.update(dict(error = error))
            return self.render_template(context)
        else:
            try:
                obj = self.get_object(id)
                func = getattr(model, self.create_method())
                func(obj, **context)
                with app.app_context():
                    cache.clear()
                return redirect(url_for("account", username = session["user"]))
            except Exception as e:
                print e
                error = "Error processing request, see error.log for details"
                context.update(dict(error = error))
                return self.render_template(context)


class UpdateArticleView(UpdateView):

    def get_model(self):
        return Articles

    def get_object(self, id):
        return Articles.get_article(id)

    def create_method(self):
        return "update_article"

class UpdateProjectView(UpdateView):

    def get_model(self):
        return UserProjects

    def get_object(self, id):
        return UserProjects.get_project(id)

    def create_method(self):
        return "update_project"
