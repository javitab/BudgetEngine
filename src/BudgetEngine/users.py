"""
Module for users data model
"""

from BudgetEngine.data import *
from BudgetEngine.accts import *
from BudgetEngine.ptxLog import *

class User(Document):
    userid = StringField(max_length=30, required=True, unique=True)
    email = EmailField(unique=True, required=True)
    first_name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50, required=True)
    password = StringField(max_length=50, required=True)
    timezone = StringField(max_length=50, required=True)
    timezone = StringField(max_length=50, required=True)
    acctIds = ListField((ReferenceField("acct")))

    meta = {
        'indexes': ['userid', 'email']
    }

    def createUser(self, userid, email, first_name, last_name, password, timezone):
        """
        Create a new user
        """
        user = User(userid=userid, email=email, first_name=first_name, last_name=last_name, password=password, timezone=timezone)
        user.save()
        return user
    def addAcctId(self, acctId):
        """
        Add an account id to the user
        """
        self.acctIds.append(acctId)
        self.save()
        return self
    def getAcctIds(self):
        """
        Get the account ids for the user
        """
        return self.acctIds
    def createAcct(self, bank_name, bank_routing_number, bank_account_number, account_display_name, current_balance, low_balance_alert, tx_last_posted):
        """
        Create a new account
        """
        acct = Acct(bank_name=bank_name, bank_routing_number=bank_routing_number, bank_account_number=bank_account_number, account_display_name=account_display_name, current_balance=current_balance, low_balance_alert=low_balance_alert, tx_last_posted=tx_last_posted)
        acct.save()
        PtxLog.createPtxLog(acct)
        self.addAcctId(acct.id)
        return acct