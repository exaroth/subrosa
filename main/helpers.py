from math import ceil
from functools import wraps
from flask import session, redirect, url_for, request
from PIL import Image
from main import app
import os
from urlparse import urljoin

def slugify(text):
    return text.strip().replace(" ", "-")

def make_external(id):
    """
    Returns external url for article based on id
    """
    return urljoin(request.url_root + "article/", str(id))

def login_required(f):

    """
    Simple authorization decorator 
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated



class Pagination(object):

    """
    Pagination class...for paginating.
    courtesy of Armin Ronacher
    """

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

def process_image(image, filename, username):
    """
    Simple image processing function 
    """
    # Base width of longer edge
    base = app.config["THUMBNAIL_SIZE"]
    square_dim = (200,200)
    try:
        print filename
        # Open an image for processing
        img = Image.open(image)

        # Check if image is vertical

        vertical = (img.size[0] < img.size[1])

        # Get a ratio for processing shorter edge

        ratio = base / float(img.size[vertical] )

        # Compute width of shorter edge

        shorter = int(img.size[not vertical] * ratio)
        dim = (shorter, base) if vertical else (base, shorter)
        thumb = img.resize(dim, Image.ANTIALIAS)
        showcase_img = img.resize(square_dim, Image.ANTIALIAS)
        img_path = os.path.join(app.config["UPLOAD_FOLDER"], username + "/")
        print img_path

        # Create thumbnail filename - extension is the same as base file

        thumb_filename = os.path.splitext(filename)[0] + ".thumbnail" + os.path.splitext(image.filename)[1]
        show_filename = os.path.splitext(filename)[0] + ".showcase" + os.path.splitext(image.filename)[1]
        full_filename = os.path.splitext(filename)[0] + os.path.splitext(image.filename)[1]
        try:
            thumb.save(os.path.join(img_path, "thumbnails/" , thumb_filename),"JPEG" )
            showcase_img.save(os.path.join(img_path, "showcase/" , show_filename),"JPEG" )
            img.save(img_path + full_filename, "JPEG")
            return (full_filename, thumb_filename, show_filename)
        except IOError, e:
                print e
                raise IOError("Could not save the file")
    except Exception as e:
        raise IOError("Could not open the file")
