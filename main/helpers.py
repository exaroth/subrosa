from math import ceil
from functools import wraps
from flask import session, redirect, url_for, request
from main import app, settings
import os
from urlparse import urljoin


def make_external(id):
    """
    Returns external url for article based on id
    """
    return urljoin(request.url_root + "article/", str(id))
    
def redirect_url():
    """
    simple function for getting back_button
    functionality in request context
    """
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

def split_filename(filename, extension_only = False):
    if "." in filename:
        parts = os.path.splitext(filename)
        if extension_only:
            return parts[1][1:]
        return parts
    return ""

def add_thumbnail_affix(url, affix = settings.get("thumbnail_size", "m")):
    url_parts = url.rpartition("/")
    parts = split_filename(url_parts[2])
    return url_parts[0] + "/" + parts[0] + affix + parts[1]





def handle_errors(mess = "Unknown Error"):
    """
    Small function that logs exceptions
    """
    if app.config.get("LOGGING", False):
        import logging, inspect, datetime, sys

        # Get the function that called it
        func = inspect.currentframe().f_back.f_code
        exc_type, exc_value, exc_traceback = sys.exc_info()


        logger = logging.getLogger("errors")
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler("errors.log")
        formatter = logging.Formatter("%(asctime)s : %(levelname)s ::: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.debug("==============================")
        logger.debug("Error occured on line %i in file %s" % (func.co_firstlineno, func.co_filename))
        logger.debug("Message: %s" % mess)
        logger.debug("Details:")
        logger.debug("--------")
        logger.debug("Type: %s" % exc_type)
        logger.debug("Value: %s" % exc_value)
        logger.debug("Traceback: %s" % exc_traceback)
    return

