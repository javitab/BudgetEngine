"""
Module for acct data model
"""
from datetime import date
import BudgetEngine as be
import BudgetEngine.data as data
import BudgetEngine.users as u
from bson import ObjectId

class Acct:
    """acct class for creating new and updating existing accounts
    """
    def __init__(self, oid):
        self.data = data.col_accounts.find_one({'_id':oid})
        self.id = self.data['_id']
        self.bank_name = self.data['bank_name']
        self.bank_routing_number = self.data['bank_routing_number']
        self.bank_account_number = self.data['bank_account_number']
        self.account_display_name = self.data['account_display_name']
        self.current_balance = data.nm(self.data['current_balance'])
        self.low_balance_alert = self.data['low_balance_alert']
        self.tx_last_posted = self.data['tx_last_posted']
        self.rev_ids = self.getRevIds
        self.exp_ids = self.getExpIds
    
    
    def reset(self):
        """Reinitializes the current instance of the class. This should be done every time a new value is written to the DB.
        """
        self.__init__(self.id)
    
    def setCurrentBalance(self, new_balance):
        """Sets the accounts current balance without transactions
        """
        if new_balance == None:
            new_balance=data.NiceMoney(input)
            data.col_accounts.update_one(
                { '_id': self.id},
                { '$set':
                    {
                        'current_balance': new_balance
                    }}
                )
        self.reset(self)

    def setTxLastPosted(self, tx_last_posted: date):
        """Sets the accounts current balance without transactions
        """
        if tx_last_posted == None:
            pass
            data.col_accounts.update_one(
                { '_id': self.id},
                { '$set':
                    {
                        'tx_last_posted': tx_last_posted
                    }}
                )
        self.reset(self)

    def create(bank_name: str, account_display_name: str, owning_user: str, low_balance_alert=100.00, bank_routing_number=None, bank_account_number=None, current_balance=0, tx_last_posted=None):
        """Create a new account after confirming no conflicts

        Args:
            bank_name (str): Name of bank holding account
            account_display_name (str): Display name of account
            owning_user (ObjectId): user account to give privileges to
            low_balance_alert (float): Level at which to alert for a low balance
            bank_routing_number (str, optional): Bank routing number
            bank_account_number (str, optional): Bank account number
            current_balance (_type_, optional): updated by postedtx
            tx_last_posted (_type_, optional): updated by postedtx
        """
        if (data.col_accounts.count_documents({"bank_account_number":bank_account_number}, limit=1) > 0) and (data.col_accounts.count_documents({"bank_routing_number":bank_routing_number}, limit=1) > 0):
            return "Error: account with same bank_account_number and bank_routing_number already exists"
        else:
            new_acct = {
                "bank_name": bank_name,
                "account_display_name": account_display_name,
                "low_balance_alert": low_balance_alert,
                "bank_routing_number": bank_routing_number,
                "bank_account_number": bank_account_number,
                "current_balance": current_balance,
                "tx_last_posted": tx_last_posted
                }
            x = data.col_accounts.insert_one(new_acct)
            if x.inserted_id == None: return "DB Error: Account not created"
            if x.inserted_id != None: 
                be.u.User(ObjectId(owning_user)).addAcctIds(x.inserted_id)
                return x.inserted_id

    def addRevIds(self,rev_id):
        """This function will add to a list of revenues that are associated with an account by revenue _id

        Args:
            rev_id (ObjectId): ObjectId of revene record
        """
        acct_filter = {"_id": self.id}
        rev_Ids = {'$push':
            {
              'revIds': ObjectId(rev_id)}}
        x = data.col_accounts.update_one(acct_filter,rev_Ids)
        self.reset()
        return x

    def getRevIds(self):
        """Gets subarray of revIds that are associated with this account
        """
        revIds_array = []
        for i in self.data['revIds']:
          revIds_array.append(i)
        return revIds_array

    def addExpIds(self,exp_id):
        """This function will add to a list of expense that are associated with an account by expense _id

        Args:
            exp_id (ObjectId): ObjectId of expense record
        """
        acct_filter = {"_id": self.id}
        exp_Ids = {'$push':
            {
              'expIds': ObjectId(exp_id)}}
        x = data.col_accounts.update_one(acct_filter,exp_Ids)
        self.reset()
        return x

    def getExpIds(self):
        """Gets subarray of expIds that are associated with this account
        """
        expIds_array = []
        for i in self.data['expIds']:
            expIds_array.append(i)
        return expIds_array

    