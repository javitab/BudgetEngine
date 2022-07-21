"""
Module for acct data model
    general account creation, maintenance, etc.
    also contains class for the txLog associated with the acct
        (transaction data model is in tx module)
"""
import datetime

import BudgetEngine as be
import BudgetEngine.data as data
import BudgetEngine.users as u
from BudgetEngine.ptxLog import *
from bson import ObjectId

class Acct:
    """acct class for creating new and updating existing accounts
    """
    def __init__(self, oid):
        self.data = data.bedb['accounts'].find_one({'_id':oid})
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
        self.ptx_log_id = self.data['ptx_log_id']
    
    
    def reset(self):
        """Reinitializes the current instance of the class. This should be done every time a new value is written to the DB.
        """
        self.__init__(self.id)
    
    def setCurrentBalance(self, new_balance):
        """Sets the accounts current balance without transactions
        """
        if new_balance == None:
            new_balance=data.NiceMoney(input)
            data.bedb['accounts'].update_one(
                { '_id': self.id},
                { '$set':
                    {
                        'current_balance': new_balance
                    }}
                )
        self.reset()

    def setTxLastPosted(self, tx_last_posted: datetime):
        """Sets the accounts current balance without transactions
        """
        if tx_last_posted == None:
            pass
            data.bedb['accounts'].update_one(
                { '_id': self.id},
                { '$set':
                    {
                        'tx_last_posted': tx_last_posted
                    }}
                )
        self.reset()

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
        if (data.bedb['accounts'].count_documents({"bank_account_number":bank_account_number}, limit=1) > 0) and (data.bedb['accounts'].count_documents({"bank_routing_number":bank_routing_number}, limit=1) > 0):
            return "Error: account with same bank_account_number and bank_routing_number already exists"
        else:
            new_acct = {
                "bank_name": bank_name,
                "account_display_name": account_display_name,
                "low_balance_alert": low_balance_alert,
                "bank_routing_number": bank_routing_number,
                "bank_account_number": bank_account_number,
                "current_balance": current_balance,
                "tx_last_posted": tx_last_posted,
                "ptx_log_id": None

                }
            x = data.bedb['accounts'].insert_one(new_acct)
            if x.inserted_id == None: return "DB Error: Account not created"
            if x.inserted_id != None:
                ptx_log_id=ptxLog.create(account=x.inserted_id)
                new_acct=Acct(x.inserted_id)
                be.u.User(ObjectId(owning_user)).addAcctIds(x.inserted_id)
                new_acct.setPtxLogId(new_ptx_log_id=ptx_log_id,newacct=True)
                return x.inserted_id
    def setPtxLogId(self,new_ptx_log_id,newacct=False):
        """
        setPtxLogId on account. Check for existing ptx_log_id, if exists, take current, append to inactive_ptx_log_ids, write new to ptx_log_id.
        """
        if newacct == True:
            acct_filter = {'_id': self.id}
            new_ptx_log_id = {'$set':
                {
                    'ptx_log_id': new_ptx_log_id
                }}
            try:
                data.bedb['accounts'].update_one(acct_filter,new_ptx_log_id)
            except:
                return "DB Error"
        else:
            inactive_ptx_log_ids={'$push':
                {
                    'inactive_ptx_log_ids': self.ptx_log_id
                }}
            try:
                data.bedb['accounts'].update_one(acct_filter,inactive_ptx_log_ids)
                data.bedb['accounts'].update_one(acct_filter,new_ptx_log_id)
            except:
                return "DB Error"    
    def addRevIds(self,rev_id):
        """This function will add to a list of revenues that are associated with an account by revenue _id

        Args:
            rev_id (ObjectId): ObjectId of revene record
        """
        acct_filter = {"_id": self.id}
        rev_Ids = {'$push':
            {
              'revIds': ObjectId(rev_id)}}
        x = data.bedb['accounts'].update_one(acct_filter,rev_Ids)
        self.reset()
        return x

    def getRevIds(self):
        """Gets subarray of revIds that are associated with this account
        """
        revIds_array = []
        revIds_array_len = 0
        for i in self.data['revIds']:
          revIds_array.append(i)
          revIds_array_len+1
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
        x = data.bedb['accounts'].update_one(acct_filter,exp_Ids)
        self.reset()
        return x
    def addRevIds(self,rev_id):
        """This function will add to a list of revenue that are associated with an account by revenue _id

        Args:
            rev_id (ObjectId): ObjectId of revenue record
        """
        acct_filter = {"_id": self.id}
        rev_Ids = {'$push':
            {
              'revIds': ObjectId(rev_id)}}
        x = data.bedb['accounts'].update_one(acct_filter,rev_Ids)
        self.reset()
        return x
    def getExpIds(self):
        """Gets subarray of expIds that are associated with this account
        """
        expIds_array = []
        for i in self.data['expIds']:
            expIds_array.append(i)
        return expIds_array
    def createExp(self, expense_display_name: str,start_date: datetime,end_date: datetime,frequency: int,amount=0.00):
        """calls to the Exp class to create a new expense
        """
        try:
            x = be.e.Exp.create(linked_account=self.id,expense_display_name=expense_display_name,start_date=start_date,end_date=end_date,frequency=frequency,amount=amount)
            return x
        except:
            return "Unable to create expense from Acct class"

    def createRev(self, revenue_display_name: str,start_date: datetime,end_date: datetime,frequency: int,amount=0.00):
        """calls to the Rev class to create a new revenue
        """
        try:
            x = be.r.Rev.create(linked_account=self.id,revenue_display_name=revenue_display_name,start_date=start_date,end_date=end_date,frequency=frequency,amount=amount)
            return x
        except:
            return "Unable to create revenue from Acct class"

    def writePtx(self,memo: str,amount: float,date: datetime,tx_type: int,ad_hoc: False,balance: float,seq=None,categories=None):
        """
        Posts a transaction to the txLog
        """
        AcctPtxLog=ptxLog(self.ptx_log_id)
        AcctPtxLog.writePtx(memo=memo,amount=amount,date=date,tx_type=tx_type,ad_hoc=ad_hoc,balance=balance,seq=seq,categories=categories)