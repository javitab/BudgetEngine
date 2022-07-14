"""
Module for expenses data model
"""

from datetime import date, datetime
import BudgetEngine.data as data
import BudgetEngine as be
from BudgetEngine.accts import *
from bson import ObjectId

class Exp:
    """exp class for creating new and updating existing accounts
    """
    def __init__(self, oid):
        self.data = data.bedb['expenses'].find_one({'_id':oid})
        self.id = self.data['_id']
        self.expense_display_name = self.data['expense_display_name']
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

    def create(expense_display_name: str,linked_account: ObjectId,start_date: datetime,last_posted_date=None,end_date=None,frequency=3,amount=0.00,):
        """
        Create a new expense

        This function is also referenced from the account class, any changes here should also take in to consider the account class
        """

        new_exp = {
            "expense_display_name": expense_display_name,
            "linked_account": linked_account,
            "frequency": frequency,
            "amount": data.nm(amount),
            "start_date": start_date,
            "end_date": end_date,
            "last_posted_date": last_posted_date
        }
        if (
            data.bedb['expenses'].count_documents({
                "linked_account": ObjectId(linked_account),
                "expense_display_name": expense_display_name
                })) < 1:
                    try:
                        x = data.bedb['expenses'].insert_one(new_exp)
                        Acct(linked_account).addExpIds(x.inserted_id)
                        return x.inserted_id
                    except:
                        return "DB Error: Unable to write expense"
        else:
            return "Error: expense with same display name already exists for same account"