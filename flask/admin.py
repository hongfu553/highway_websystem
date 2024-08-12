from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
import database as models

Users=models.Users
Log=models.Log

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        return super(MyAdminIndexView, self).index()

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

admin = Admin(index_view=MyAdminIndexView())

def init_admin(app,db):
    admin.init_app(app)
    admin.add_view(MyModelView(Users, db.session))
    admin.add_view(MyModelView(Log, db.session))
    return admin