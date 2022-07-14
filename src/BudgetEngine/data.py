"""
Initiating connection to database and pulling base dependencies
"""

import array
from ctypes import Array
from tokenize import Double
import pymongo
import datetime as dt
import calendar as cal
from dateutil.relativedelta import relativedelta
import os
import bson
import json
import BudgetEngine.config as config
import pandas as pd

#getting environment variables
evars = config.Vars()

#defining verbose function
verboseON=0

def verbose(object):
    if verboseON == 1:
        print(object)
    elif verboseON == 0:
        pass

#connecting to db
dbclient = pymongo.MongoClient(("mongodb://%s:%s/" % (evars.MongoDBIP, evars.MongoDBPort)))
bedbcurs = dbclient[evars.DBName]

#defining collection cursors

collections=['accounts','expenses','revenue','projections','transactions','users']
bedb={}
for i in collections:
    bedb[i] = bedbcurs[i]
    if bedb[i].count_documents({},limit=1) < 1:
        bedb[i].insert_one({
            'init_record': True,
            'init_time': dt.datetime.utcnow()
        })



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
        output(float): Options:
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
    x = dt.datetime.strptime(inputdate,"%Y-%m-%d")
    return x

def txIterate(frequency: int, inputdate: dt.date):
    """Given a frequency and input date, this function will calculate the next date based on the frequency

    Args:
        frequency (int): 
            [1: biweekly],
            [2: weekly],
            [3: monthly],
            [4: daily]
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