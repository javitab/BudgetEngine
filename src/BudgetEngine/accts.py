"""
Module for acct data model
    general account creation, maintenance, etc.
    also contains class for the txLog associated with the acct
        (transaction data model is in tx module)
"""

from BudgetEngine.data import *
from BudgetEngine.ptxLog import PtxLog

class Acct(Document):
    """
    acct class for creating new and updating existing accounts
    """
    bank_name=StringField(max_length=50, required=True)
    bank_routing_number=StringField(max_length=50, required=True)
    bank_account_number=StringField(max_length=50, required=True)
    account_display_name=StringField(max_length=50, required=True)
    current_balance=DecimalField(required=True)
    low_balance_alert=DecimalField(required=True)
    tx_last_posted=DateTimeField(required=True)
    rev_ids=ListField((ReferenceField("rev")))
    exp_ids=ListField((ReferenceField("exp")))
    ptx_log_id=ReferenceField(PtxLog)

    def createAcct(self, bank_name, bank_routing_number, bank_account_number, account_display_name, current_balance, low_balance_alert, tx_last_posted):
        """
        Create a new account
        """
        acct = Acct(bank_name=bank_name, bank_routing_number=bank_routing_number, bank_account_number=bank_account_number, account_display_name=account_display_name, current_balance=current_balance, low_balance_alert=low_balance_alert, tx_last_posted=tx_last_posted)
        acct.save()
        PtxLog.createPtxLog(acct)
        return acct
    
    def addRevId(self, revId):
        """
        Add a revenue id to the account
        """
        self.rev_ids.append(revId)
        self.save()
        return self
    
    def addExpId(self, expId):
        """
        Add an expense id to the account
        """
        self.exp_ids.append(expId)
        self.save()
        return self
    
