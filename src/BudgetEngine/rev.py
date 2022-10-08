from mongoengine import *
from datetime import datetime as dt

from .dtfunc import txIterate

class Rev(Document):
    display_name=StringField(max_length=50, required=True)
    amount=DecimalField(required=True)
    frequency=StringField(max_length=10, required=True, choices=["weekly","biweekly","monthly","quarterly","yearly"])
    start_date=DateField(required=True)
    end_date=DateField()
    exclusion_dates=ListField(DateField())
    last_posted_date=DateField()
    time_created=DateField(required=True,default=dt.now())
    notes=StringField()

    def  next_date(self):
        """This function calculates the next date for the revenue and returns it as a datetime object
        """
        try:
            if self.last_posted_date == None:
                return self.start_date
            else:
                return txIterate(self.frequency,self.last_posted_date)
        except:
            pass

    FormInputGroups=[
        {
            'input_group_name': 'Revenue Info',
            'field_name': 'id',
            'read_only': 'Always',
            'hidden': False,
            'field_friendly': '_id',
            'field_placeholder': '-',
            'field_help': 'internal record id name for Revenue',
            'field_type': 'ObjectId'
        },
        {
            'input_group_name': 'Revenue Info',
            'field_name': 'display_name',
            'read_only': "No",
            'hidden': False,
            'field_friendly': 'Display Name',
            'field_placeholder': '-',
            'field_help': 'name of Revenue',
            'field_type': 'String'
        },
        {
            'input_group_name': 'Revenue Details',
            'field_name': 'amount',
            'read_only': "No",
            'hidden': False,
            'field_friendly': 'Amount',
            'field_placeholder': '-',
            'field_help': 'amount of Revenue',
            'field_type': 'Decimal'
        },
        {
            'input_group_name': 'Revenue Details',
            'field_name': 'frequency',
            'read_only': "No",
            'hidden': False,
            'field_friendly': 'Frequency',
            'field_placeholder': '-',
            'field_help': 'frequency of Revenue',
            'field_type': 'dropdown',
            'field_choices': ['weekly','biweekly','monthly','quarterly','yearly']
        },
        {
            'input_group_name': 'Revenue Dates',
            'field_name': 'start_date',
            'read_only': "No",
            'hidden': False,
            'field_friendly': 'Start Date',
            'field_placeholder': '-',
            'field_help': 'date Revenue starts',
            'field_type': 'Date'
        },
        {
            'input_group_name': 'Revenue Dates',
            'field_name': 'end_date',
            'read_only': "No",
            'hidden': False,
            'field_friendly': 'End Date',
            'field_placeholder': '-',
            'field_help': 'date Revenue ends',
            'field_type': 'Date'
        },
        {
            'input_group_name': 'Revenue Calculations',
            'field_name': 'next_date',
            'read_only': "Always",
            'hidden': False,
            'field_friendly': 'Next Date',
            'field_placeholder': '-',
            'field_help': 'next date Revenue will be posted',
            'field_type': 'method'

        },
        {
            'input_group_name': 'Revenue Calculations',
            'field_name': 'last_posted_date',
            'read_only': "Always",
            'hidden': False,
            'field_friendly': 'Last Posted Date',
            'field_placeholder': '-',
            'field_help': 'last date Revenue was posted',
            'field_type': 'Date'
        },
        {
            'input_group_name': 'Revenue Dates',
            'field_name': 'time_created',
            'read_only': "Always",
            'hidden': False,
            'field_friendly': 'Time Created',
            'field_placeholder': '-',
            'field_help': 'time Revenue was created',
            'field_type': 'DateTime'
        },{
        'input_group_name': 'Revenue Notes',
        'field_name': 'notes',
        'read_only': "No",
        'hidden': False,
        'field_friendly': 'Notes',
        'field_placeholder': '-',
        'field_help': 'Enter account notes',
        'field_type': 'longtext'
    }]

