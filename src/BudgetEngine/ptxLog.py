"""
Module for transaction data model
"""

from datetime import date, datetime
from pprint import pprint
from threading import activeCount
import bson
from bson.json_util import loads,dumps

import BudgetEngine.data as data
import BudgetEngine as be
from BudgetEngine.accts import *


class ptxLog:
    """
    ptxLog class for creating and modifying posted transaction logs
    """
    def __init__(self, oid):
        self.data = data.bedb['transactions'].find_one({'_id': oid})
        self.transactions = data.bedb['transactions'].aggregate([
            {
                '$unwind': {
                    'path': '$PostedTxs'
                }
            }, {
                '$match': {
                    'account': self.data['account']
                }
            }, {
                '$group': {
                    '_id': '$PostedTxs.txID'
                }
            }
        ])
        self.currAcct = be.a.Acct(self.data['account'])
    def reset(self):
        """Reinitializes the current instance of the class. This should be done every time a new value is written to the DB.
        """
        self.__init__(self.id)
    
    def create(account: bson.ObjectId):
        """
        Creates new ptxlog, does not handle writing new id to acct
        """
        PostedTxs=[]
        new_ptxlog = {
            "account": account,
            "last_seq": int(0),
            "PostedTxs": PostedTxs
        }
        x = data.bedb['transactions'].insert_one(new_ptxlog)
        return x.inserted_id
    def writePtx(self,memo: str,amount: float,date: datetime,tx_type: int,ad_hoc: False,balance: float,seq=None,categories=None):
        """
        Posts a transaction to the txLog
        """
        ptxLog_filter={'_id': self.data['_id']}
        if categories==None:
            categories=[]
        if seq==None:
            #Calculate value for sequence
            data.bedb['transactions'].update_one(
                ptxLog_filter,
                {'$inc': {'last_seq': 1}} )
            newSeq=data.bedb['transactions'].find_one(ptxLog_filter,{'last_seq':1})
            newSeq=newSeq['last_seq']
        tx_to_write = {'$push':
            {'PostedTxs':
                {   "txID": bson.ObjectId(),
                    "seq": newSeq,
                    "amount": amount,
                    "memo": memo,
                    "date": date,
                    "tx_type": tx_type,
                    "ad_hoc": ad_hoc,
                    "balance": balance,
                    "categories": categories
                }}
        }
        pTx = data.bedb['transactions'].update_one(ptxLog_filter,tx_to_write)
        self.currAcct.setTxLastPosted(tx_last_posted=date)
        return pTx.acknowledged

class pTx:
    def __init__(self,ptx_log_oid,tx_oid):
        self.rawdata = data.bedb['transactions'].aggregate([
        {
            '$match': {
                '_id': ptx_log_oid
            }
        }, {
            '$unwind': {
                'path': '$PostedTxs'
            }
        }, {
            '$project': {
                '_id': '$PostedTxs.txID', 
                'seq': '$PostedTxs.seq', 
                'amount': '$PostedTxs.amount', 
                'memo': '$PostedTxs.memo', 
                'date': '$PostedTxs.date', 
                'tx_type': '$PostedTxs.tx_type', 
                'ad_hoc': '$PostedTxs.ad_hoc', 
                'balance': '$PostedTxs.balance', 
                'categories': '$PostedTxs.categories'
            }
        }, {
            '$match': {
                '_id': tx_oid
            }
        }, {
            '$sort': {
                'seq': 1
            }
        }
        ])
        sanitizedData=data.json.loads(dumps(self.rawdata))
        self.data = sanitizedData
        self.txID = self.data[0]['_id']
        self.date = self.data[0]['date']
        self.memo = self.data[0]['memo']
        self.amount = self.data[0]['amount']
        self.tx_type = self.data[0]['tx_type']
        self.ad_hoc = self.data[0]['ad_hoc']
        self.balance = self.data[0]['balance']
        self.categories = self.data[0]['categories']