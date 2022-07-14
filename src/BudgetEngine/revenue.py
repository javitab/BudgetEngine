"""
Module for revenue data model
"""

from datetime import date, datetime
import BudgetEngine.data as data
import BudgetEngine as be
from BudgetEngine.accts import *
from bson import ObjectId

class Rev:
    """rev class for creating new and updating existing accounts
    """
    def __init__(self, oid):
        self.data = data.bedb['revenue'].find_one({'_id':oid})
        self.id = self.data['_id']
        self.revenue_display_name = self.data['revenue_display_name']
        self.linked_account = self.data['linked_account']
        self.amount = data.nm(self.data['amount'])
        self.frequency = self.data['frequency']
        self.start_date = self.data['start_date']
        self.end_date = self.data['end_date']
        self.last_posted_date = self.data['last_posted_date']
        self.time_created = self.data['time_created']

    def reset(self):
        """Reinitializes the current instance of the class. This should be done every time a new value is written to the DB.
        """
        self.__init__(self.id)

    def create(revenue_display_name: str,linked_account: ObjectId,start_date: datetime,last_posted_date=None,end_date=None,frequency=3,amount=0.00,):
        """
        Create a new revenue

        This function is also referenced from the account class, any changes here should also take in to consider the account class
        """

        new_rev = {
            "revenue_display_name": revenue_display_name,
            "linked_account": linked_account,
            "frequency": frequency,
            "amount": data.nm(amount),
            "start_date": start_date,
            "end_date": end_date,
            "last_posted_date": last_posted_date
        }
        if (
            data.bedb['revenue'].count_documents({
                "linked_account": ObjectId(linked_account),
                "revenue_display_name": revenue_display_name
                })) < 1:
                    try:
                        x = data.bedb['revenue'].insert_one(new_rev)
                        Acct(linked_account).addRevIds(x.inserted_id)
                        return x.inserted_id
                    except:
                        return "DB Error: Unable to write revenue"
        else:
            return "Error: revenue with same display name already exists for same account"