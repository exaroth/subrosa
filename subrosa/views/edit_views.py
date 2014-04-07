# -*- coding: utf-8 -*-
"""

    subrosa.views.edit_views
    ===============


    Implements views related to updating projects and articles

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.

"""

from flask import (render_template, request,
                   session, url_for, redirect, flash, abort)
from subrosa import app, cache
from subrosa.models.UsersModel import Users
from subrosa.models.ArticlesModel import Articles
from subrosa.models.UserProjectsModel import UserProjects
from subrosa.helpers import logger
from subrosa.views.base_views import ScratchpadView, ArticleView


class UpdateView(ScratchpadView):

    """
    Basic class implementing update
    functionality for articles and projects
    """

    def get_model(self):
        raise NotImplementedError()

    def create_method(self):
        raise NotImplementedError()

    def get_object(self):
        raise NotImplementedError()

    def get(self, id):
        obj = self.get_object(id)
        if not obj or obj.author.username != session["user"]:
            abort(404)

        context = dict(title=obj.title, body=obj.body)

        if self.ARTICLE:
            context.update(dict(series=obj.series,
                                categories=[cat.name for cat in
                                            obj.get_article_categories().iterator()],
                                article_image=obj.article_image,
                                article_thumbnail=obj.article_thumbnail))

        return self.render_template(context)

    def post(self, id):
        title = request.form.get("title").strip()
        body = request.form.get("body").strip()
        context = dict(title=title, body=body)
        context.update(self.process_additional_fields())
        if not title or not body:
            error = "Entry can\'t have empty title or body"
            context.update(dict(error=error))
            return self.render_template(context)
        model = self.get_model()
        check = model.check_exists(title, id)
        if check:
            error = "Entry with this title\
                    already exists, please choose another"
            context.update(dict(error=error))
            return self.render_template(context)
        else:
            try:
                obj = self.get_object(id)
                func = getattr(model, self.create_method())
                func(obj, **context)
                with app.app_context():
                    cache.clear()
                    return redirect(url_for("account", username=session["user"]))
            except Exception as e:
                logger.debug(e)
                error = "Error processing request, see error.log for details"
                context.update(dict(error=error))
                return self.render_template(context)


class UpdateArticleView(ArticleView, UpdateView):

    def get_model(self):
        return Articles

    def get_object(self, id):
        return Articles.get_article(id)

    def get_context(self):
        return dict(additional_controls=True,
                    title_placeholder="Title of your article",
                    body_placeholder="and content here...")

    def create_method(self):
        return "update_article"


class UpdateProjectView(UpdateView):

    def get_model(self):
        return UserProjects

    def get_object(self, id):
        return UserProjects.get_project(id)

    def get_context(self):
        return dict(additional_controls=False,
                    title_placeholder="Title of the project",
                    body_placeholder="and content here...")

    def create_method(self):
        return "update_project"
