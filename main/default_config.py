# -*- coding: utf-8 -*-
"""

    main.default_config
    ============
    
    This is the default config used by Subrosa,
    it consists of all the options in Subrosa conf
    aswell as some more advanced one
    Typically this should not be changed by user.

    :copyright: (c) 2014 by Konrad Wasowicz
    :license: MIT, see LICENSE for details.

"""

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

DATABASE = None

# Database name

DATABASE_NAME = None

#This options apply only if you are using postgresql or mysql

DB_USERNAME = None 

DB_PASSWORD = None 

# ===================================================

# Set this variable to your === disqus shortname === to have comments on your blog

DISQUS = False

# Set this variables to adress of your liking eg "http://www.facebook.com/johndoe"

EMAIL = False

FACEBOOK = False

TWITTER = False

GITHUB = False

GOOGLE_PLUS = False

# If you want gallery integrated with Imgur service put your Imgur user_id here

IMGUR_ID = False

# Set it to True if you want gallery link on your main page

GALLERY = False

PROJECTS = False

# Number of pages that shows up on index page

ARTICLES_PER_PAGE = 5 

# Number of images showing on page

IMAGES_PER_PAGE = 10

# Your secret key

SECRET_KEY = "Change it"

# Default color for header text and icons

HEADER_FONT_COLOR = "#4D4D4D"
HEADER_BG_COLOR = "#FFFFFF"

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

THUMBNAIL_SIZE = "l"


# Set it to True only for development purposes, outputs errors straight to the browser

DEBUG = False


# Set it to True if you want detailed error messages written to a file

LOGGING = False

# Cache options

CACHE_TYPE = "simple"

CACHE_KEY_PREFIX = "subrosa_"

CACHE_TIMEOUT = 50

