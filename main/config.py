import sys
import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(BASE_PATH + "..")

# Url adress to you page, used for linking images

URL_ADDRESS = "localhost:5000"

UPLOAD_FOLDER = os.path.dirname(os.path.join(ROOT_PATH, "uploads/")) + "/"

# path to your database

SQLALCHEMY_DATABASE_URI = "sqlite:////" + ROOT_PATH + "/test.db"

# Number of pages that shows up on page

ARTICLES_PER_PAGE = 3

# Size of longer edge of thumbnail picture

THUMBNAIL_SIZE = 300

#Allowed filenames for image upload

ALLOWED_FILENAMES = ["jpg", "jpeg", "gif", "png", "JPG", "JPEG", "GIF", "PNG"]

# Your secret key

SECRET_KEY = "\xdb\x81\xd4\xef\xeb\xf5z.\xd9\xf2\xd6R\xd7m1wv\xf34@\xb52\xe6\r\x0f\xc8r%\xdf\xb0\x06 \xc8\xd94O)\xd2\x1a\xca\x86\xc4\xf5\xce\x99\x88\xe1mn\xae&1hqO\x95~\xa7LW+\xd6Dl\xd2\x17\x93}\x0b\x0b\x06\xf6B\x88Oe@F\xef\x81\x8cqA\xd2=g\xd8\xaf\xf1p\x10$\t7\x8ch\x994m\xe5\xafY\x17)I\xc9NK{\xceb\x8c\xc8P\x885\xa5\x12^\x157&'\xdc\xc6%"

TESTING = True


