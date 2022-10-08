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

    FormInputGroups=[
        {
            'input_group_name': 'Transaction Info',
            'field_name': 'id',
            'read_only': 'Always',
            'hidden': False,
            'field_friendly': '_id',
            'field_placeholder': '-',
            'field_help': 'internal record id name for transaction',
            'field_type': 'ObjectId'
        },
        {
            'input_group_name': 'Transaction Info',
            'field_name': 'date',
            'read_only': "No",
            'hidden': False,
            'field_friendly': 'Date',
            'field_placeholder': '-',
            'field_help': 'date of transaction',
            'field_type': 'Date'
        },
        {
            'input_group_name': 'Transaction Info',
            'field_name': 'memo',
            'read_only': "No",
            'hidden': False,
            'field_friendly': 'Memo',
            'field_placeholder': '-',
            'field_help': 'memo of transaction',
            'field_type': 'String'
        },
        {
            'input_group_name': 'Transaction Info',
            'field_name': 'amount',
            'read_only': "No",
            'hidden': False,
            'field_friendly': 'Amount',
            'field_placeholder': '-',
            'field_help': 'amount of transaction',
            'field_type': 'Decimal'
        },
        {
            'input_group_name': 'Transaction Info',
            'field_name': 'tx_type',
            'read_only': "No",
            'hidden': False,
            'field_friendly': 'Transaction Type',
            'field_placeholder': '-',
            'field_help': 'type of transaction',
            'field_type': 'String'
        },
        {
            'input_group_name': 'Transaction Info',
            'field_name': 'ad_hoc',
            'read_only': "No",
            'hidden': False,
            'field_friendly': 'Ad Hoc',
            'field_placeholder': '-',
            'field_help': 'ad hoc transaction',
            'field_type': 'Boolean'
        },
        {
            'input_group_name': 'Transaction Info',
            'field_name': 'balance',
            'read_only': "No",
            'hidden': False,
            'field_friendly': 'Balance',
            'field_placeholder': '-',
            'field_help': 'balance of transaction',
            'field_type': 'Decimal'
        },
        {
            'input_group_name': 'Transaction Info',
            'field_name': 'categories',
            'read_only': "No",
            'hidden': False,
            'field_friendly': 'Categories',
        }

class PtxLog(Document):
    date_created=DateTimeField(required=True,default=dt.now())
    posted_txs=EmbeddedDocumentListField(Tx)

class Acct(Document):
    """
    acct class for creating new and updating existing accounts
    """
    bank_name=StringField(max_length=50)
    bank_routing_number=StringField(max_length=50, required=False)
    bank_account_number=StringField(max_length=50, required=False)
    account_display_name=StringField(max_length=50, required=False)
    current_balance=DecimalField()
    low_balance_alert=DecimalField()
    tx_last_posted=DateTimeField()
    rev_ids=ListField((ReferenceField(Rev)))
    exp_ids=ListField((ReferenceField(Exp)))
    active_ptx_log_id=ReferenceField(PtxLog)
    history_ptx_log_ids=ListField((ReferenceField(PtxLog)))
    projections=ListField(ObjectIdField())
    notes=StringField()
    meta = {
        'indexes': ['rev_ids','exp_ids','active_ptx_log_id','history_ptx_log_ids']
    }

    TableHeaders=['txID','date','memo','amount','tx_type','ad_hoc','balance']

    FormInputGroups=[
    {
        'input_group_name': 'Account Info',
        'field_name': 'id',
        'read_only': 'Always',
        'hidden': False,
        'field_friendly': '_id',
        'field_placeholder': '-',
        'field_help': 'internal record id name for account',
        'field_type': 'ObjectId'
    },
    {
        'input_group_name': 'Account Info',
        'field_name': 'account_display_name',
        'read_only': "No",
        'hidden': False,
        'field_friendly': 'Display Name',
        'field_placeholder': 'Enter display name for account (required)',
        'field_help': 'Enter name to display for account',
        'field_type': 'text'
    },
    {
        'input_group_name': 'Account Institution',
        'field_name': 'bank_name',
        'read_only': "New",
        'hidden': False,
        'field_friendly': 'Bank Name',
        'field_placeholder': 'Enter bank account name (optional)',
        'field_help': 'Enter name of bank or institution',
        'field_type': 'text'
    },
    {
        'input_group_name': 'Account Details',
        'field_name': 'bank_routing_number',
        'read_only': "No",
        'hidden': False,
        'field_friendly': 'routing',
        'field_placeholder': 'Enter bank routing number (optional)',
        'field_help': 'Enter bank routing number',
        'field_type': 'text'
    },
    {
        'input_group_name': 'Account Details',
        'field_name': 'bank_account_number',
        'read_only': "No",
        'hidden': False,
        'field_friendly': 'acct',
        'field_placeholder': 'Enter bank account number (optional)',
        'field_help': 'Enter bank account number',
        'field_type': 'text'
    },
    {
        'input_group_name': 'Account Calculations',
        'field_name': 'current_balance',
        'read_only': "New",
        'hidden': False,
        'field_friendly': 'Current Balance',
        'field_placeholder': 'Enter the starting balance (required)',
        'field_help': 'Calculated value for current balance',
        'field_type': 'text'
    },
    {
        'input_group_name': 'Account Calculations',
        'field_name': 'low_balance_alert',
        'read_only': "No",
        'hidden': False,
        'field_friendly': 'Low Bal',
        'field_placeholder': 'Enter low balance alert level ##.## (required)',
        'field_help': 'Enter low balance alert level ##.## (required)',
        'field_type': 'text'
    },
    {
        'input_group_name': 'Account Notes',
        'field_name': 'notes',
        'read_only': "No",
        'hidden': False,
        'field_friendly': 'Notes',
        'field_placeholder': 'Enter any freetext notes here (optional)',
        'field_help': 'Enter account notes',
        'field_type': 'longtext'
    }
]