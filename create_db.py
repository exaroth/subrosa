from main.models import Users, Articles, UserImages
from main import db, app


db.connect()


app.config["DEBUG"] = False

Users.create_table()
Articles.create_table()
UserImages.create_table()

print "database created"

