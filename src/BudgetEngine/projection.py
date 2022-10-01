from datetime import datetime as dt
from datetime import timedelta
from mongoengine import *


from .acct import *
from .exp import *
from .rev import *
from.func import *


class ProjectionRevTx(EmbeddedDocument):
    ptxRevID=ObjectIdField(required=True)
    rev_id=ReferenceField(Rev),
    date=DateField(required=True),
    memo=StringField(max_length=100, required=True),
    amount=DecimalField(required=True)

class ProjectionExpTx(EmbeddedDocument):
    ptxExpID=ObjectIdField(required=True)
    exp_id=ReferenceField(Exp),
    date=DateField(required=True),
    memo=StringField(max_length=100, required=True),
    amount=DecimalField(required=True)

class Projection(Document):
    projection_acct=ReferenceField(Acct,required=True)
    start_date=DateField(required=True,default=dt.utcnow)
    end_date=DateField(required=True)
    projected_txs=EmbeddedDocumentListField(Tx)
    balance=DecimalField()
    rev_txs=EmbeddedDocumentListField(ProjectionRevTx)
    exp_txs=EmbeddedDocumentListField(ProjectionExpTx) 

    def runProjection(self):
        """
        Iterate through all expense and revenue objects and create a list of projected transactions
        """
        self.iterateRevs()
        self.iterateExps()
        self.balance=self.projection_acct.current_balance
        iterDate=self.start_date
        while iterDate<=self.end_date:
            for revtx in self.rev_txs:
                if revtx.Date==iterDate:
                    self.projected_txs.append(EmbeddedDocument(
                        txID=revtx.id,
                        date=revtx.Date,
                        memo=revtx.Memo,
                        amount=revtx.Amount,
                        tx_type="credit",
                        ad_hoc=False,
                        balance=self.balance+revtx.Amount,
                        categories=revtx.rev_id.categories
                    ))
            for exptx in self.exp_txs:
                if exptx.Date==iterDate:
                    self.projected_txs.append(EmbeddedDocument(
                        txID=exptx.id,
                        date=exptx.Date,
                        memo=exptx.Memo,
                        amount=exptx.Amount,
                        tx_type="debit",
                        ad_hoc=False,
                        balance=self.balance-exptx.Amount,
                        categories=exptx.exp_id.categories
                    ))
            iterDate=iterDate+timedelta(days=1)
        self.save()

    def iterateRevs(self):
        """
        Iterate through all revenue objects and create a list of projected revenue transactions
        """
        #Create list of revenues for each day
        for rev in self.projection_acct.rev_ids:
            iterDate=rev.next_date()
            while iterDate<=self.end_date:
                if iterDate not in rev.exclusion_dates:
                    print(("rev_id: ",rev.id,"date: ",iterDate,"memo: ",rev.display_name,"amount: :",rev.amount))
                    self.rev_txs.create(
                        rev_id=rev.id,
                        date=iterDate,
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
                    print("rev_id: ",exp.id,"date: ",iterDate,"memo: ",exp.display_name,"amount: :",exp.amount)
                    self.exp_txs.create(
                        exp_id=exp.id,
                        Date=iterDate,
                        Memo=exp.display_name,
                        Amount=exp.amount
                    )
                    self.exp_txs.save()
                iterDate=txIterate(exp.frequency,iterDate)