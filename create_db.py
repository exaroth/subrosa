from main import db, app
from main.models.ArticlesModel import Articles
from main.models.UserImagesModel import UserImages
from main.models.UsersModel import Users


db.connect()


app.config["DEBUG"] = False

Users.create_table()
Articles.create_table()
UserImages.create_table()

print "database created"

