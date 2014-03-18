# -*- coding: utf-8 -*-
"""

    main.markdown_ext
    ============

        Implements class integrating markdown
        parser into Subrosa

        Inspired by Flask-Markdown extension
        by Dan Colish

        https://github.com/dcolish/flask-markdown

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.

"""

from flask import Markup
from jinja2 import evalcontextfilter, escape
import markdown


class Markdown(object):

    """

    Wrapper class for Markdown object

    Example usage:
    md = Markdown(app = app,
                        auto_escape = False,
                        extensions = ['footnotes'],
                        safe_mode = True,
                        output_format = 'html4')
    """

    def __init__(self, app = None, auto_escape = False, **markdown_options):

        self._instance = markdown.Markdown(**markdown_options)

    def __call__(self, stream):
        return Markup(self._instance.convert(stream))

    def _build_filter(self, auto_escape):
        @evalcontextfilter
        def markdown_filter(eval_ctx, stream):
            _filter = self
            if auto_escape and eval_ctx.autoescape:
                return Markup(_filter(escape(stream)))
            else:
                return Markup(_filter(stream))
        return markdown_filter
