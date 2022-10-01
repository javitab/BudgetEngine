from mongoengine import *
from datetime import datetime as dt

from .func import txIterate

class Rev(Document):
    display_name=StringField(max_length=50, required=True)
    amount=DecimalField(required=True)
    frequency=StringField(max_length=10, required=True, choices=["weekly","biweekly","monthly","quarterly","yearly"])
    start_date=DateField(required=True)
    end_date=DateField()
    exclusion_dates=ListField(DateField())
    last_posted_date=DateField()
    time_created=DateField(required=True,default=dt.utcnow())

    def  next_date(self):
        """This function calculates the next date for the revenue and returns it as a datetime object
        """
        if self.last_posted_date == None:
            return txIterate(self.frequency,self.start_date)
        else:
            return txIterate(self.frequency,self.last_posted_date)