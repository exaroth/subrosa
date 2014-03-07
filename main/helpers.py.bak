# -*- coding: utf-8 -*-
"""

    main.helpers
    ============
    
    Helper files used by other Subrosa components

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.

"""

from math import ceil
from functools import wraps
from flask import session, redirect, url_for, request
import os
from urlparse import urljoin
import string, random
import unicodedata
import re



def slugify(value, separator="-"):

    """ Slugify a string, to make it URL friendly. """

    if isinstance(value, unicode):
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = re.sub('[^\w\s-]', '', value.decode('ascii')).strip().lower()
    return re.sub('[%s\s]+' % separator, separator, value)

def make_external(id):

    """
    Returns external url for article based on id
    """

    return urljoin(request.url_root + "article/", str(id))

def generate_csrf_token():

    """ Generates random string for login screen"""

    if '_csrf_token' not in session:
        session['_csrf_token'] = id_generator()
    return session['_csrf_token']
    
def redirect_url():

    """
    Simple function for getting back_button
    functionality in request context
    """

    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

def split_filename(filename, extension_only = False):

    """ split filename into <filename> <extension> parts """

    if "." in filename:
        parts = os.path.splitext(filename)
        if extension_only:
            return parts[1][1:]
        return parts
    return ""

def add_thumbnail_affix(url, affix):

    """ Add thumbnail affix to gallery picture """

    url_parts = url.rpartition("/")
    parts = split_filename(url_parts[2])
    return url_parts[0] + "/" + parts[0] + affix + parts[1]

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):

    """ Generate random string """

    return ''.join(random.choice(chars) for _ in range(size))



def handle_errors(mess = "Unknown Error"):

    """
    Small function that logs exceptions
    """
    
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
    logger.debug("Exception Details:")
    logger.debug("--------")
    logger.debug("Type: %s" % exc_type)
    logger.debug("Value: %s" % exc_value)
    logger.debug("Traceback: %s" % exc_traceback)
    return

