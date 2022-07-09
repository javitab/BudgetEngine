"""
Module for users data model
"""

import BudgetEngine.data as data
from bson import ObjectId

class User:
    """acct class for creating new and updating existing accounts
    """
    def __init__(self, oid):
        self.data = data.col_users.find_one({'_id':oid})
        self.id = self.data['_id']
        self.userid = self.data['userid']
        self.email = self.data['email']
        self.first_name = self.data['first_name']
        self.last_name = self.data['last_name']
        self.password = self.data['password']
        self.acctIds = self.getAcctIds
    
    def reset(self):
        """Reinitializes the current instance of the class. This should be done every time a new value is written to the DB.
        """
        self.__init__(self.id)
    
    def create(userid: str, email: str, first_name: str, last_name: str, password: str):
        """Create new user account after confirming no conflicts

        Args:
            userid (str): userid for login
            email (str): user's email address
            first_name (str): users's First Name
            last_name (str): user's Last Name
            password (str): users' hashed password
        """
        if data.col_users.count_documents({"userid":userid}, limit=1) > 0:
            return "Error: UserID already in use"
        elif data.col_users.count_documents({"email":email}, limit=1) > 0:
            return "Error: Email already in use"
        else:
            new_user={
                "userid": userid,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": password
            }
            x = data.col_users.insert_one(new_user)
            if x.inserted_id == None:
                return "DB Error: Account not created"
            if x.inserted_id != None:
                return x.inserted_id
        
    def addAcctIds(self,acct_id):
        """This function will add to a list of acctenues that are associated with an account by acctenue _id

        Args:
            acct_id (ObjectId): ObjectId of acctene record
        """
        acct_filter = {"_id": self.id}
        acct_Ids = {'$push':
            {
            'acctIds': ObjectId(acct_id)}}
        x = data.col_users.update_one(acct_filter,acct_Ids)
        return x

    def getAcctIds(self):
        """Gets subarray of acctIds that are associated with this account
        """
        acctIds_array = []
        for i in self.data['acctIds']:
          acctIds_array.append(i)
        return acctIds_array