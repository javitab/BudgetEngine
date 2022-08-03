"""
Module for transaction data model
"""

from datetime import date, datetime
from bson import ObjectId

import BudgetEngine.data as data
import BudgetEngine as be
from BudgetEngine.accts import *


class postTx:
    """
    postTx class for creating and modifying transactions
    """
    def __init__(self, oid):
        self.rawdata = data.bedb['transactions'].aggregate([
            {
                '$unwind': {
                    'path': '$PostedTxs'
                }
            }, {
                '$match': {
                    'PostedTxs.txID': be.ObjectId(oid)
                }
            }, {
                '$group': {
                    '_id': '$acctName', 
                    'PostedTxs': {
                        '$push': {
                            'txID': '$PostedTxs.txID', 
                            'date': {
                                '$dateToString': {
                                    'format': '%Y-%m-%d', 
                                    'date': '$PostedTxs.date'
                                }
                            }, 
                            'account': '$acctName', 
                            'memo': '$PostedTxs.memo', 
                            'amount': '$PostedTxs.amount', 
                            'tx_type': '$PostedTxs.tx_type', 
                            'ad_hoc': '$PostedTxs.ad_hoc', 
                            'balance': '$PostedTxs.balance',
                            'categories': '$PostedTxs.categories'
                        }
                    }
                }
            }
        ])
        sanitizedData=data.json.loads(be.json_util.dumps(self.rawdata))
        normalizedData=data.pd.json_normalize(sanitizedData, 'PostedTxs')
        self.data = normalizedData
        self.txID = self.data['txID'][0]
        self.date = self.data['date'][0]
        self.account = self.data['account'][0]
        self.memo = self.data['memo'][0]
        self.amount = self.data['amount'][0]
        self.tx_type = self.data['tx_type'][0]
        self.ad_hoc = self.data['ad_hoc'][0]
        self.balance = self.data['balance'][0]
        self.categories = self.data['categories']
    def reset(self):
        """Reinitializes the current instance of the class. This should be done every time a new value is written to the DB.
        """
        self.__init__(self.id)
    
    def writePtx(memo: str,amount: float,date: datetime,tx_type: int,ad_hoc: False,balance: float,seq=None,categories=None):
        """
        Posts a transaction to the txLog
        """
        if categories==None:
            categories=[]
        tx_to_write={'$push':
            {'PostedTxs':
                {'txID': ObjectId(),
                'memo': 'memo',
                'amount': 'amount',
                'date': 'date',
                'tx_type': 'tx_type',
                'ad_hoc': 'ad_hoc',
                'balance': 'balance',
                'categories': 'categories'}}
                }
        