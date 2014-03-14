from main import db, app
from main.models.ArticlesModel import Articles
from main.models.UserImagesModel import UserImages
from main.models.UsersModel import Users
from main.models.UserProjectsModel import UserProjects



for field in (Articles, UserImages, Users, UserProjects):

    if not field.table_exists():
        raise Exception("table %s doesn\'t exist" % repr(field))


print "All tables are OK"

