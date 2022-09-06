"""
Initiating connection to database and pulling base dependencies
"""


from datetime import datetime as dt
from datetime import timedelta
import calendar as cal
import os
from mongoengine import *
from bson import ObjectId
from flask_login import UserMixin

#Importing Configuration File
import BudgetEngine.config as config


#getting environment variables
evars = config.Vars()

#defining verbose function
verboseON=0

def verbose(object):
    if verboseON == 1:
        print(object)
    elif verboseON == 0:
        pass

#Connect to database
register_connection(alias='default',name=evars.DBName, host=evars.MongoDBIP, port=evars.MongoDBPort)

#defining dates
def dtfunc(period,component,fmt='dt'):
    """compiles various common date strings for use

    Args:
        period (str): Options: 
            [today],
                component (str): Options:
                    ['fulldate'],
                    ['day'],
                    ['month'],
                    ['year']
            [current]
                component (str): Options: 
                    ['last_day_month'],
                    ['last_date_month'],
                    ['first_day_month']
        fmt(str): Options:
            ['dt'],
            ['str']
    """
    if period=="today":
        if component=="fulldate":
            dateout = dt.datetime(dt.datetime.today().year, dt.datetime.today().month, dt.datetime.today().day)
        if component=="day":
            dateout = dt.datetime.today().day
        if component=="month":
            dateout = dt.datetime.today().month
        if component=="year":
            dateout = dt.datetime.today().year
    
    if period=="current":
        if component=="last_day_month":
            dateout = cal.monthrange(dtfunc('current','year'),dtfunc('current','month'))[1]
        if component=="last_date_month":
            dateout = dt.datetime(dtfunc('current','year'),dtfunc('current','month'),dtfunc('current','last_day_month'))
        if component=="first_date_month":
            dateout = dt.datetime(dtfunc('current','year'),dtfunc('current','month'),1)
    
    if fmt=='str':
        return dateout.strftime('%Y-%m-%d')
    if fmt=='int':
        return int(dateout.strftime('%Y%m%d'))
    else:
        return dt.datetime.strptime(dateout.strftime('%Y-%m-%d'), '%Y-%m-%d')

def convDate(inputdate: str):
    """This function takes an input of a string and formats as a datetime value and strips the time

    Args:
        inputdate (str): input date string

    Returns:
        _type_: date as datetime object
    """
    x = dt.strptime(inputdate,"%Y-%m-%d")
    return x

def txIterate(frequency: str, inputdate: dt):
    """Given a frequency and input date, this function will calculate the next date based on the frequency

    Args:
        frequency (str): 
            "daily",
            "weekly",
            "biweekly",
            "monthly",
            "quarterly",
            "yearly"
        inputdate (dt.date): input date as datetime object

    Returns:
        dt.date: new date as datetime object
    """
    startdate = inputdate
    if frequency == "daily": delta = timedelta(days=1)
    if frequency == 'weekly': delta = timedelta(weeks=1)
    if frequency == 'biweekly': delta = timedelta(weeks=2)
    if frequency == 'monthly': delta = timedelta(weeks=4)
    if frequency == 'quarterly': delta = timedelta(weeks=12)
    if frequency == 'yearly': delta = timedelta(years=1)
    if isinstance(startdate,str):
        startdate=convDate(startdate)
    x = startdate + delta
    return x

#defining how to handle monies

def nm(input: float):
    """NiceMoney, takes a float input, rounds to 2 decimal places, returns as float

    Args:
        input (float): input numerical value

    Returns:
        float: return float rounded to .00
    """
    x = round(input,2)
    return x

#defining internal functions
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def menuGen(actions: list,mnuName: str,clear=1):
    """This function takes an input of a list of actions and generates a menu with am output of action

    Args:
        actions (list): actions to perform
        mnuName (str): name of menu to display
        clear (int, optional): If 1, clears the screen before and after showing menu. Defaults to 1.
    """
    if clear == 1: cls()
    print("\n")
    print(("=== Printing available options for %s===") % mnuName)
    for i in actions:
        print(i)
    print("Q: Quit")
    action = input("What would you like to do? ")
    print("\n")
    if action == "Q" or action == 'q': action = 'Q'
    if clear == 1: cls()
    return action

###                      ###
### Defining data models ###
###                      ###

class Exp(Document):
    """exp class for creating new and updating existing accounts
    """
    display_name=StringField(max_length=50, required=True)
    amount=DecimalField(required=True)
    frequency=StringField(max_length=10, required=True, choices=["weekly","biweekly","monthly","quarterly","yearly"])
    start_date=DateField(required=True)
    end_date=DateField()
    last_posted_date=DateField()
    time_created=DateTimeField(required=True,default=dt.utcnow())

    def next_date(self):
        """This function calculates the next date for the expense and returns it as a datetime object
        """
        if self.last_posted_date == None:
            return txIterate(self.frequency,self.start_date).strftime('%Y-%m-%d')
        else:
            return txIterate(self.frequency,self.last_posted_date).strftime('%Y-%m-%d')

    
class Rev(Document):
    display_name=StringField(max_length=50, required=True)
    amount=DecimalField(required=True)
    frequency=StringField(max_length=10, required=True, choices=["weekly","biweekly","monthly","quarterly","yearly"])
    start_date=DateField(required=True)
    end_date=DateField()
    last_posted_date=DateField()
    time_created=DateField(required=True,default=dt.utcnow())

    def  next_date(self):
        """This function calculates the next date for the revenue and returns it as a datetime object
        """
        if self.last_posted_date == None:
            return txIterate(self.frequency,self.start_date).strftime('%Y-%m-%d')
        else:
            return txIterate(self.frequency,self.last_posted_date).strftime('%Y-%m-%d')

class Tx(EmbeddedDocument):
    txID=ObjectIdField(required=True)
    date=DateTimeField(required=True)
    memo=StringField(max_length=100, required=True)
    amount=DecimalField(required=True)
    tx_type=StringField(max_length=10, required=True,choices=["debit","credit"])
    ad_hoc=BooleanField(required=True)
    balance=DecimalField(required=True)
    categories=ListField((StringField(max_length=50)))

class PtxLog(Document):
    date_created=DateTimeField(required=True,default=dt.utcnow())
    posted_txs=EmbeddedDocumentListField(Tx)

class Acct(Document):
    """
    acct class for creating new and updating existing accounts
    """
    bank_name=StringField(max_length=50, required=True)
    bank_routing_number=StringField(max_length=50, required=True)
    bank_account_number=StringField(max_length=50, required=True)
    account_display_name=StringField(max_length=50, required=True)
    current_balance=DecimalField(required=True)
    low_balance_alert=DecimalField()
    tx_last_posted=DateTimeField()
    rev_ids=ListField((ReferenceField(Rev)))
    exp_ids=ListField((ReferenceField(Exp)))
    active_ptx_log_id=ReferenceField(PtxLog)
    history_ptx_log_ids=ListField((ReferenceField(PtxLog)))

    meta = {
        'indexes': ['rev_ids','exp_ids','active_ptx_log_id','history_ptx_log_ids']
    }

class User(UserMixin, Document):
    userid = StringField(max_length=30, required=True, unique=True)
    email = EmailField(unique=True, required=True)
    first_name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50, required=True)
    password = StringField(max_length=250, required=True)
    timezone = StringField(max_length=50, required=True)
    acctIds = ListField((ReferenceField(Acct)))

    meta = {
        'indexes': ['userid', 'email']
    }

    def UserList():
        return User.objects.get()
