# -*- coding: utf-8 -*-
"""

    subrosa.views.base-views
    ===============

    Base classes used by class-based views


    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.

"""

from flask.views import MethodView
from flask import render_template, request
from subrosa.decorators import login_required
from subrosa import cache, app
import re


class BaseView(MethodView):

    """
    Base view to be implemented by every
    other class based view
    """

    ARTICLE = False

    def get_template_name(self):
        raise NotImplementedError()

    def get_context(self):
        return dict()

    def render_template(self, context=dict()):
        with app.app_context():
            cache.clear()
        context.update(self.get_context())
        context.update(dict(show_title=True))
        return render_template(self.get_template_name(), **context)

    def process_additional_fields(self):
        return dict()

    def get(self):
        pass

    def post(self):
        pass


class ScratchpadView(BaseView):

    """
    View to be implemented
    by scratchpad views
    """

    decorators = [login_required]

    def get_template_name(self):
        return "scratchpad.html"


class ArticleView(BaseView):

    """
    Additional view implemented
    by update/create article views
    """

    ARTICLE = True

    def process_additional_fields(self):

        """
        Adds additional information needed for articles
            : categories
            : series
            : article-image
            : article-thumbnail
        """

        categories = request.form.get("categories-hidden")
        categories = categories.strip()

        if categories:
            categories = re.split(r"\s+", categories)

        series = request.form.get("series-hidden")
        article_image = request.form.get("article-image-hidden")
        article_thumbnail = request.form.get("article-image-small-hidden")

        for field in (series, article_image, article_thumbnail):
            if field:
                field = field.strip()

        return dict(categories=categories,
                    series=series,
                    article_image=article_image,
                    article_thumbnail=article_thumbnail)
