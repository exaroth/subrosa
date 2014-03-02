"""

This file contains default configuration for Subrosa,
User configuration should be definedd in subrosa.cfg file

"""
import sys
import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(BASE_PATH + "..")

# Set title of you site

TITLE = "Your awesome blog"

# Set it to False if Subrosa will not modify local filesystem in any way,
# including database

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

DISQUS = False

# Set this variables to adress of your liking eg "http://www.facebook.com/johndoe"

FACEBOOK = False

TWITTER = False

GITHUB = False

# If you want gallery integrated with Imgur service put your Imgur user_id here

IMGUR_ID = False

# Set it to True if you want gallery link on your main page

GALLERY = False

# Number of pages that shows up on index page

ARTICLES_PER_PAGE = 5 

# Number of images showing on page

IMAGES_PER_PAGE = 10

# Your secret key

SECRET_KEY = "Change it"

# Default color for header text and icons

HEADER_COLOR = "#4D4D4D"

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
