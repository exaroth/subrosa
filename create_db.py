from main.models import Users, Articles, UserImages
from main import db, define_db_connection, app

db = define_db_connection(app.config["DATABASE"], app.config["DATABASE_NAME"])

db.connect()


app.config["DEBUG"] = False

Users.create_table()
Articles.create_table()
UserImages.create_table()

print database created

