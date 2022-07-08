"""Initiating connection to database and pulling base dependencies
"""

import array
from ctypes import Array
import pymongo
import datetime as dt
import calendar as cal
from dateutil.relativedelta import relativedelta
import os
import bson
import json

import config

#defining verbose function
verboseON=0

def verbose(object):
    if verboseON == 1:
        print(object)
    elif verboseON == 0:
        pass

#connecting to db
dbhostcon = pymongo.MongoClient(("mongodb://%s:%s/") % config.MongoDBIP ,config.MongoDBPort)
bedb = dbhostcon["BudgetEngine"]

#defining collection cursors
col_accounts = bedb["accounts"]
col_expenses = bedb["expenses"]
col_revenues = bedb["revenues"]
col_projections = bedb["projections"]
col_postedtxs = bedb["postedtxs"]
col_users = bedb["users"]

#defining dates
def dtfunc(period: str, component: str):
    """compiles various common date strings for use

    Args:
        period (str): Options: [today],[current]
        component (str): Options: [fulldate],[day],[month],[year],[last_day_month],[last_date_month],[first_day_month]
    """
    if period=="today" or period=="current" and component=="fulldate": return dt.datetime(dtfunc('current','year'), dtfunc('current','month'), dtfunc('current','day'))
    if period=="today" or period=="current"  and component=="day": return dt.datetime.today().day
    if period=="today" or period=="current"  and component=="month": return dt.datetime.today().month
    if period=="today" or period=="current"  and component=="year": return dt.datetime.today().year
    if period=="current" and component=="last_day_month": return cal.monthrange(dtfunc('current','year'),dtfunc('current','month'))[1]
    if period=="current" and component=="last_date_month": return dt.datetime(dtfunc('current','year'),dtfunc('current','month'),dtfunc('current','last_day_month'))
    if period=="current" and component=="first_date_month": return dt.datetime(dtfunc('current','year'),dtfunc('current','month'),1)

def convDate(inputdate: str):
    """This function takes an input of a string and formats as a datetime value and strips the time

    Args:
        inputdate (str): input date string

    Returns:
        _type_: date as datetime object
    """
    x = dt.datetime.strptime(inputdate,"%Y-%m-%d")
    return x

def txIterate(frequency: int, inputdate: dt.date):
    """Given a frequency and input date, this function will calculate the next date based on the frequency

    Args:
        frequency (int): [1: biweekly],[2: weekly],[3: monthly],[4: daily]
        inputdate (dt.date): input date as datetime object

    Returns:
        dt.date: new date as datetime object
    """
    startdate = inputdate
    if frequency == 1: delta = dt.timedelta(weeks=2)
    if frequency == 2: delta = dt.timedelta(weeks=1)
    if frequency == 3: delta = dt.timedelta(months=1)
    if frequency == 4: delta = dt.timedelta(days=1)
    x = startdate + delta
    return x

#defining how to handle monies

def NiceMoney(input):
    """Will take any string, convert to double, round to 2 decimals, force to 

    Args:
        input (_type_): _description_

    Returns:
        float: _description_
    """
    

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