"""
Module for transaction log data model
"""

from BudgetEngine.accts import Acct
from BudgetEngine.data import *

class PtxLog(Document):
    account_id=ReferenceField(Acct)
    posted_txs=ListField((ReferenceField("tx")))

    meta = {
        'indexes': ['account_id']
    }

    def createPtxLog(self, account_id):
        """
        Create a new transaction log
        """
        ptx_log = PtxLog(account_id=account_id)
        ptx_log.save()
        ptxAcct=Acct.objects.get(account_id=account_id)
        ptxAcct.ptx_log_ids.append(ptx_log.id)
        return ptx_log