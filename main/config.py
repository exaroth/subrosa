import sys
import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(BASE_PATH + "..")

# Set title of you site

TITLE = "Blog pani Kasi"

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

# If you want gallery integrated with Imgur service put your Imgur user_id here

IMGUR_ID = "2d8bf53ae7b7e27"

# Set it to True if you want gallery link on your main page

GALLERY = True

# Number of pages that shows up on index page

ARTICLES_PER_PAGE = 5 

# Number of images showing on page

IMAGES_PER_PAGE = 10

# Your secret key

SECRET_KEY = "Super secret"

# =======================================================================
# ======================== Advanced Settings ============================
# =========== Change them only if you know what you're doing ============
# =======================================================================

# Allowed filenames for image upload

ALLOWED_FILENAMES = ["jpg", "jpeg", "gif", "png", "JPG", "JPEG", "GIF", "PNG"]

# Thumbnail size for imgur images

# Available sizes :
    # s -- 90x90 square
    # b -- 160x160 square
    # t -- 160x160
    # m -- 320x320
    # l -- 640x640
    # h -- 1024x1024

THUMBNAIL_SIZE = "m"


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
