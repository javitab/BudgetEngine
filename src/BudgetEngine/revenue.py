"""
Module for revenue data model
"""

from datetime import datetime
from BudgetEngine.data import *
from BudgetEngine.accts import *

class Rev(Document):
    display_name=StringField(max_length=50, required=True)
    account=ReferenceField(Acct)
    amount=DecimalField(required=True)
    frequency=StringField(max_length=10, required=True, choices=["weekly","biweekly","monthly","quarterly","yearly"])
    start_date=DateTimeField(required=True)
    end_date=DateTimeField()
    last_posted_date=DateTimeField()
    time_created=DateTimeField(required=True,default=datetime.utcnow())

    def createRev(self, display_name, account, amount, frequency, start_date, end_date, last_posted_date):
        """
        Create a new revenue
        """
        rev = Rev(display_name=display_name, account=account, amount=amount, frequency=frequency, start_date=start_date, end_date=end_date, last_posted_date=last_posted_date)
        rev.save()
        return rev
