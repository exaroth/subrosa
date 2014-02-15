import sys
import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(BASE_PATH + "..")

# Set title of you site

TITLE = "Kermit's Blog"

# Path to upload folder

UPLOAD_FOLDER = os.path.dirname(os.path.join(ROOT_PATH, "uploads/")) + "/"

# Set it to False if you dont want to modify filesystem

DYNAMIC_SITE = True

# path to your database

SQLALCHEMY_DATABASE_URI = "sqlite:////" + ROOT_PATH + "/test.db"

# Number of pages that shows up on page

ARTICLES_PER_PAGE = 3

# Size of longer edge of thumbnail picture (in pixels)

THUMBNAIL_SIZE = 300

# Allowed filenames for image upload

ALLOWED_FILENAMES = ["jpg", "jpeg", "gif", "png", "JPG", "JPEG", "GIF", "PNG"]

# Your secret key

SECRET_KEY = "\xdb\x81\xd4\xef\xeb\xf5z.\xd9\xf2\xd6R\xd7m1wv\xf34@\xb52\xe6\r\x0f\xc8r%\xdf\xb0\x06 \xc8\xd94O)\xd2\x1a\xca\x86\xc4\xf5\xce\x99\x88\xe1mn\xae&1hqO\x95~\xa7LW+\xd6Dl\xd2\x17\x93}\x0b\x0b\x06\xf6B\x88Oe@F\xef\x81\x8cqA\xd2=g\xd8\xaf\xf1p\x10$\t7\x8ch\x994m\xe5\xafY\x17)I\xc9NK{\xceb\x8c\xc8P\x885\xa5\x12^\x157&'\xdc\xc6%"


# Set it to True only for development purposes

DEBUG = True

# Set it to True if you want detailed error messages written to a file

LOGGING = True



