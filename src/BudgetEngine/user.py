from mongoengine import *
from flask_login import UserMixin
from .acct import Acct


class User(UserMixin, Document):
    userid = StringField(max_length=30, required=True, unique=True)
    email = EmailField(unique=True, required=True)
    first_name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50, required=True)
    password = StringField(max_length=250, required=True)
    timezone = StringField(max_length=50, required=True)
    acctIds = ListField((ReferenceField(Acct)))

    meta = {
        'indexes': ['userid', 'email']
    }

    def UserList():
        return User.objects.get()