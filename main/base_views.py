# -*- coding: utf-8 -*-
"""

    main.base-views
    ===============
    
    Base classes used by class-based views


    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.

"""


from flask.views import MethodView
from flask import render_template
from main.decorators import login_required
from main import cache, app

class BaseView(MethodView):

    def get_template_name(self):
        raise NotImplementedError()

    def get_context(self):
        return dict()

    def render_template(self, context = dict()):
        with app.app_context():
            cache.clear()
        context.update(self.get_context())
        return render_template(self.get_template_name(), **context)

    def get(self):
        pass

    def post(self):
        pass


class ScratchpadView(BaseView):

    decorators = [login_required,]

    def get_template_name(self):
        return "scratchpad.html"

    def process_additional_fields(self):
        return dict()
