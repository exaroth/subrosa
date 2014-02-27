import sys
import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(BASE_PATH + "..")

# Set title of you site

TITLE = "Kermit's Blog"

# Set it to False if you dont want to modify filesystem,
# prevents writing images to disk, only remote links are allowed 

DYNAMIC_SITE = True

# ========== Database Configuration =================

# Define database connection

# Avaliable databases are:
# * sqlite
# * postrges
# * mysql

# Database type

DATABASE = "sqlite"

# Database name

DATABASE_NAME = "test.db"

#This options apply only if you are using postgresql or mysql

DB_USERNAME = None 

DB_PASSWORD = None 

# ===================================================

# Set this variable to your === disqus shortname === to have comments on your blog

DISQUS = "kermitsblog"

# Set this variables to adress of your liking eg "http://www.facebook.com/johndoe"

FACEBOOK = "http://www.mojfacebook.pl"

TWITTER = "http://www.twitter.com"

GITHUB = False

# Set it to True if you want gallery link on your main page

GALLERY = False

# Number of pages that shows up on index page

ARTICLES_PER_PAGE = 8 

# Number of images showing on page

IMAGES_PER_PAGE = 20

# Your secret key

SECRET_KEY = "\xdb\x81\xd4\xef\xeb\xf5z.\xd9\xf2\xd6R\xd7m1wv\xf34@\xb52\xe6\r\x0f\xc8r%\xdf\xb0\x06 \xc8\xd94O)\xd2\x1a\xca\x86\xc4\xf5\xce\x99\x88\xe1mn\xae&1hqO\x95~\xa7LW+\xd6Dl\xd2\x17\x93}\x0b\x0b\x06\xf6B\x88Oe@F\xef\x81\x8cqA\xd2=g\xd8\xaf\xf1p\x10$\t7\x8ch\x994m\xe5\xafY\x17)I\xc9NK{\xceb\x8c\xc8P\x885\xa5\x12^\x157&'\xdc\xc6%"

# =======================================================================
# ======================== Advanced Settings ============================
# =========== Change them only if you know what you're doing ============
# =======================================================================

# Allowed filenames for image upload

ALLOWED_FILENAMES = ["jpg", "jpeg", "gif", "png", "JPG", "JPEG", "GIF", "PNG"]


# Size of longer edge of thumbnail picture (in pixels)

THUMBNAIL_SIZE = 300

# Set it to True only for development purposes, outputs errors straight to the browser

DEBUG = True


# Set it to True if you want detailed error messages written to a file

LOGGING = True

# Path to upload folder

UPLOAD_FOLDER = os.path.dirname(os.path.join(ROOT_PATH, "uploads/")) + "/"

# Cache options

CACHE_TYPE = "simple"

CACHE_KEY_PREFIX = "subrosa_"

TESTING = False
