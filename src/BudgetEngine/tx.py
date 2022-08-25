"""
Module for transaction data model
"""

from datetime import date
from random import choices
from BudgetEngine.data import *

class Tx(Document):
    txID=SequenceField()
    date=DateTimeField(required=True)
    memo=StringField(max_length=100, required=True)
    amount=DecimalField(required=True)
    tx_type=StringField(max_length=10, required=True,choices=["debit","credit"])
    ad_hoc=BooleanField(required=True)
    balance=DecimalField(required=True)
    categories=ListField((StringField(max_length=50)))