from datetime import datetime as dt
from datetime import timedelta
from mongoengine import *



from .exp import *
from .rev import *
from .dtfunc import *

class PTx(EmbeddedDocument):
    seq=IntField(required=True)
    item_id=StringField()
    date=DateField(required=True)
    memo=StringField(max_length=100, required=True)
    amount=DecimalField(required=True)
    tx_type=StringField(max_length=10, required=True,choices=["debit","credit"])
    ad_hoc=BooleanField(required=True)
    balance=DecimalField(required=True)
    categories=ListField((StringField(max_length=50)))



class ProjectionRevTx(DynamicEmbeddedDocument):
    rev_id=ReferenceField(Rev),
    date=DateField(required=True),
    memo=StringField(max_length=100, required=True),
    amount=DecimalField(required=True)
    meta = {
        'strict': 'false'
    }

class ProjectionExpTx(DynamicEmbeddedDocument):
    exp_id=ReferenceField(Exp),
    date=DateField(required=True),
    memo=StringField(max_length=100, required=True),
    amount=DecimalField(required=True)
    meta = {
        'strict': 'false'
    }

class Projection(Document):
    projection_acct=ObjectIdField(required=True)
    disp_name=StringField(max_length=100)
    start_date=DateField(required=True,default=dt.now)
    end_date=DateField(required=True)
    projected_txs=EmbeddedDocumentListField(PTx)
    balance=DecimalField()
    rev_txs=EmbeddedDocumentListField(ProjectionRevTx)
    exp_txs=EmbeddedDocumentListField(ProjectionExpTx)
    notes=StringField()
    meta={
        'index': ['projection_acct']
    }



    def iterateRevs(self,Acct):
        """
        Iterate through all revenue objects and create a list of projected revenue transactions
        """
        #Create list of revenues for each day

        for rev in Acct.rev_ids:
            iterDate=rev.next_date()
            while iterDate<=self.end_date:
                if iterDate not in rev.exclusion_dates:
                    iterDateTime=dt.combine(iterDate, dt.min.time())
                    self.rev_txs.create(
                        rev_id=rev.id,
                        date=iterDateTime,
                        memo=rev.display_name,
                        amount=rev.amount
                    )
                    self.rev_txs.save()
                iterDate=txIterate(rev.frequency,iterDate)

    def iterateExps(self,Acct):
        """
        Iterate through all expense objects and create a list of projected expense transactions
        """        
        #Create list of revenues for each day
        for exp in Acct.exp_ids:
            iterDate=exp.next_date()
            while iterDate<=self.end_date:
                if iterDate not in exp.exclusion_dates:
                    iterDateTime=dt.combine(iterDate, dt.min.time())
                    self.exp_txs.create(
                        exp_id=exp.id,
                        date=iterDateTime,
                        memo=exp.display_name,
                        amount=exp.amount
                    )
                    self.exp_txs.save()
                iterDate=txIterate(exp.frequency,iterDate)

    def runProjection(self,Acct):
        """
        Iterate through all expense and revenue objects and create a list of projected transactions
        """
        self.iterateRevs(Acct)
        self.iterateExps(Acct)
        self.balance=Acct.current_balance
        iterDate=self.start_date
        seq=0
        while iterDate<=self.end_date:
            for revtx in self.rev_txs:
                revtxdate_=revtx.date
                revtxdate=revtxdate_.date()
                if revtxdate==iterDate:
                    seq=seq+1
                    self.projected_txs.create(
                        seq=seq,
                        item_id=str(revtx.rev_id),
                        date=revtx.date,
                        memo=revtx.memo,
                        amount=revtx.amount,
                        tx_type="credit",
                        ad_hoc=False,
                        balance=self.balance+revtx.amount
                    )
                    self.balance=self.balance+revtx.amount
                    self.save()
                    self.projected_txs.save()
            for exptx in self.exp_txs:
                exptxdate_=exptx.date
                exptxdate=exptxdate_.date()
                if exptxdate==iterDate:
                    seq=seq+1
                    self.projected_txs.create(
                        seq=seq,
                        item_id=str(exptx.exp_id),
                        date=exptx.date,
                        memo=exptx.memo,
                        amount=exptx.amount,
                        tx_type="debit",
                        ad_hoc=False,
                        balance=self.balance-exptx.amount
                    )
                    self.balance=self.balance-exptx.amount
                    self.save()
                    self.projected_txs.save()
            iterDate=iterDate+timedelta(days=1)
        self.save()

    TableHeaders=['txID','seq','date','memo','amount','ad_hoc','balance']

    FormInputGroups=[
    {
        'input_group_name': 'Projection Info',
        'field_name': 'id',
        'read_only': 'Always',
        'hidden': False,
        'field_friendly': '_id',
        'field_placeholder': '-',
        'field_help': 'internal record id name for account',
        'field_type': 'ObjectId'
    },
    {
        'input_group_name': 'Projection Info',
        'field_name': 'disp_name',
        'read_only': "No",
        'hidden': False,
        'field_friendly': 'Display Name',
        'field_placeholder': 'Enter display name for projection (required)',
        'field_help': 'Enter name to display for projection',
        'field_type': 'text'
    },
    {
        'input_group_name': 'Projection Inputs',
        'field_name': 'start_date',
        'read_only': "Always",
        'hidden': False,
        'field_friendly': 'Start Date',
        'field_placeholder': '-',
        'field_help': 'Start date for projection',
        'field_type': 'date'
    },
    {
        'input_group_name': 'Projection Inputs',
        'field_name': 'end_date',
        'read_only': "New",
        'hidden': False,
        'field_friendly': 'End Date',
        'field_placeholder': '[YYYY-MM-DD] (required)',
        'field_help': 'Enter end date for projection',
        'field_type': 'date'
    },
    {
        'input_group_name': 'Projection Notes',
        'field_name': 'notes',
        'read_only': "No",
        'hidden': False,
        'field_friendly': 'Notes',
        'field_placeholder': 'Enter notes for projection',
        'field_help': 'Enter notes for projection',
        'field_type': 'textarea'
    }
]
