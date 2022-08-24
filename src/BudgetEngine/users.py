"""
Module for users data model
"""

from BudgetEngine.data import *

class User(Document):
    userid = StringField(max_length=30, required=True, unique=True)
    email = EmailField(unique=True, required=True)
    first_name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50, required=True)
    password = StringField(max_length=50, required=True)
    timezone = StringField(max_length=50, required=True)
    timezone = StringField(max_length=50, required=True)
    acctIds = ListField((ReferenceField("acct")))

    def create(userid: str, email: str, first_name: str, last_name: str, password: str, timezone: str):
        """Create new user account after confirming no conflicts
        Args:
            userid (str): userid for login
            email (str): user's email address
            first_name (str): users's First Name
            last_name (str): user's Last Name
            password (str): users' hashed password
            timezone (str): user's timezone
        """
        if data.bedb['users'].count_documents({"userid":userid}, limit=1) > 0:
            return "Error: UserID already in use"
        elif data.bedb['users'].count_documents({"email":email}, limit=1) > 0:
            return "Error: Email already in use"
        else:
            new_user={
                "userid": userid,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
                "timezone": timezone
            }
            x = data.bedb['users'].insert_one(new_user)
            if x.inserted_id == None:
                return "DB Error: Account not created"
            if x.inserted_id != None:
                return x.inserted_id