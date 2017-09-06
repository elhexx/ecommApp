from main import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Users
from products import Product, Products

db.create_all()

admin = Admin(app, name='microblog', template_mode='bootstrap3')

admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Products, db.session))

