from math import ceil
from functools import wraps
from flask import session, redirect, url_for, request
from PIL import Image
from main import app
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



def process_image(image, filename, username):
    """
    Simple image processing function 
    """
    # Base width of longer edge
    base = app.config["THUMBNAIL_SIZE"]
    try:
        # Open an image for processing
        img = Image.open(image)

        # Check if image is vertical

        vertical = (img.size[0] < img.size[1])

        # Get a ratio for processing shorter edge

        ratio = base / float(img.size[vertical] )

        # Compute width of shorter edge

        shorter = int(img.size[not vertical] * ratio)
        dim = (shorter, base) if vertical else (base, shorter)
        showcase_img = img.resize(dim, Image.ANTIALIAS)
        img_path = os.path.join(app.config["UPLOAD_FOLDER"], username + "/")

        # Create thumbnail filename - extension is the same as base file

        show_filename = os.path.splitext(filename)[0] + ".showcase" + os.path.splitext(image.filename)[1]
        full_filename = os.path.splitext(filename)[0] + os.path.splitext(image.filename)[1]
        try:
            showcase_img.save(os.path.join(img_path, "showcase/" , show_filename),"JPEG" )
            img.save(img_path + full_filename, "JPEG")
            return (full_filename, show_filename, int(vertical))
        except IOError, e:
                handle_errors(e)
                raise 
    except Exception as e:
        handle_errors(e)
        raise 
