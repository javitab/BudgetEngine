from datetime import datetime as dt
from datetime import timedelta
from typing import Sequence
from mongoengine import *


from .acct import *
from .exp import *
from .rev import *
from .func import *

class PTx(EmbeddedDocument):
    seq=IntField(required=True)
    item_id=StringField()
    date=DateTimeField(required=True)
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
    projection_acct=ReferenceField(Acct,required=True)
    start_date=DateField(required=True,default=dt.utcnow)
    end_date=DateField(required=True)
    projected_txs=EmbeddedDocumentListField(PTx)
    balance=DecimalField()
    rev_txs=EmbeddedDocumentListField(ProjectionRevTx)
    exp_txs=EmbeddedDocumentListField(ProjectionExpTx)
    meta={
        'index': ['projection_acct']
    }

    def iterateRevs(self):
        """
        Iterate through all revenue objects and create a list of projected revenue transactions
        """
        #Create list of revenues for each day
        for rev in self.projection_acct.rev_ids:
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

    def iterateExps(self):
        """
        Iterate through all expense objects and create a list of projected expense transactions
        """        
        #Create list of revenues for each day
        for exp in self.projection_acct.exp_ids:
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

    def runProjection(self):
        """
        Iterate through all expense and revenue objects and create a list of projected transactions
        """
        self.iterateRevs()
        self.iterateExps()
        self.balance=self.projection_acct.current_balance
        iterDate=self.start_date
        print("Starting iterDate loop for projecting transactions")
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

