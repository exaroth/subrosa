# -*- coding: utf-8 -*-
"""

    main.base-views
    ===============
    
    Base classes used by class-based views


    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.

"""


from flask.views import MethodView
from flask import render_template, request
from main.decorators import login_required
from main import cache, app
import re

class BaseView(MethodView):

    ARTICLE = False

    def get_template_name(self):
        raise NotImplementedError()

    def get_context(self):
        return dict()

    def render_template(self, context = dict()):
        with app.app_context():
            cache.clear()
        context.update(self.get_context())
        return render_template(self.get_template_name(), **context)

    def process_additional_fields(self):
        return dict()

    def get(self):
        pass

    def post(self):
        pass


class ScratchpadView(BaseView):

    decorators = [login_required,]

    def get_template_name(self):
        return "scratchpad.html"



class ArticleView(BaseView):

    ARTICLE = True


    def process_additional_fields(self):
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
                
        return dict(categories = categories, series = series,\
                    article_image = article_image, article_thumbnail = article_thumbnail)
