from mongoengine import *
from datetime import datetime as dt

from .rev import Rev
from .exp import Exp


class Tx(EmbeddedDocument):
    txID=ObjectIdField(required=True)
    date=DateTimeField(required=True)
    memo=StringField(max_length=100, required=True)
    amount=DecimalField(required=True)
    tx_type=StringField(max_length=10, required=True,choices=["debit","credit"])
    ad_hoc=BooleanField(required=True)
    balance=DecimalField(required=True)
    categories=ListField((StringField(max_length=50)))

class PtxLog(Document):
    date_created=DateTimeField(required=True,default=dt.utcnow())
    posted_txs=EmbeddedDocumentListField(Tx)

class Acct(Document):
    """
    acct class for creating new and updating existing accounts
    """
    bank_name=StringField(max_length=50, required=True)
    bank_routing_number=StringField(max_length=50, required=True)
    bank_account_number=StringField(max_length=50, required=True)
    account_display_name=StringField(max_length=50, required=True)
    current_balance=DecimalField(required=True)
    low_balance_alert=DecimalField()
    tx_last_posted=DateTimeField()
    rev_ids=ListField((ReferenceField(Rev)))
    exp_ids=ListField((ReferenceField(Exp)))
    active_ptx_log_id=ReferenceField(PtxLog)
    history_ptx_log_ids=ListField((ReferenceField(PtxLog)))

    meta = {
        'indexes': ['rev_ids','exp_ids','active_ptx_log_id','history_ptx_log_ids']
    }