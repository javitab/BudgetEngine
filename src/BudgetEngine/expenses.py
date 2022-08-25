"""
Module for expenses data model
"""

from BudgetEngine.data import *
from datetime import datetime
from BudgetEngine.accts import *

class Exp(Document):
    """exp class for creating new and updating existing accounts
    """
    display_name=StringField(max_length=50, required=True)
    account=ReferenceField(Acct)
    amount=DecimalField(required=True)
    frequency=StringField(max_length=10, required=True, choices=["weekly","biweekly","monthly","quarterly","yearly"])
    start_date=DateTimeField(required=True)
    end_date=DateTimeField()
    last_posted_date=DateTimeField()
    time_created=DateTimeField(required=True,default=datetime.utcnow())

    def createExp(self, display_name, account, amount, frequency, start_date, end_date, last_posted_date):
        """
        Create a new expense
        """
        exp = Exp(display_name=display_name, account=account, amount=amount, frequency=frequency, start_date=start_date, end_date=end_date, last_posted_date=last_posted_date)
        exp.save()
        return exp
    
