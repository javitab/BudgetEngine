from re import I, L, S, X
from pandas.core.indexes.range import RangeIndex
import pymongo
import datetime as dt
import calendar as cal
import pprint
import pandas as pd
from tabulate import tabulate
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from bson import ObjectId, json_util
import os
import bson
import json
from BudgetEngine.bevars import *

#connecting to db
myclient = pymongo.MongoClient(("mongodb://%s:27017/") % envVars("MongoDBIP"))
bedb = myclient["BudgetEngine"]

#defining collection cursors
accts = bedb["accounts"]
expenses = bedb["expenses"]
revenues = bedb["revenue"]
projection = bedb["projections"]
postedtx = bedb['postedtx']
users = bedb['users']

#defining dates
CurrDay = dt.datetime.today().day
CurrMonth = dt.datetime.today().month
CurrYear = dt.datetime.today().year
CurrDate = dt.datetime(CurrYear, CurrMonth, CurrDay)
CurrInst = dt.datetime.today()
LastDayCurr = cal.monthrange(CurrYear, CurrMonth)[1]
LastDate = dt.datetime(CurrYear,CurrMonth,LastDayCurr)
FirstDayCurr = dt.datetime(CurrYear,CurrMonth,1)

verboseON = 0

def verbose(object):
    if verboseON == 1:
        print(object)
    elif verboseON == 0:
        pass

def pause():
    programPause = input("Press the <ENTER> key to continue...")

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def mongoArrayDf(mongo_data,arrayName):
    sanitized = json.loads(json_util.dumps(mongo_data))
    normalized = pd.json_normalize(sanitized, arrayName)
    df = pd.DataFrame(normalized)
    return df

def menuGen(actions,mnuName,clear=1):
    "This function takes an input of an array of actions and generates a menu with an output of action"
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

def convDate(inputdate):
    "This function takes an input convDate and formats as datetime value and strips time"
    X = dt.datetime.strptime(inputdate,"%Y-%m-%d")
    return X

def findExp(expName):
    "This function returns and prints expenses info for expenses name input"
    x = expenses.find_one({"Name": expName})
    pprint.pprint(x)
    return x

def listCollection(collection):
    "This funtion returns the contents of an entire collection as input by name"
    listColData = bedb[collection]
    x = listColData.find()
    return x

def printRecord(collection, name):
    data = bedb[collection].find({ 'Name': name})
    return data

def getExpenses(acctName):
    "This function returns all expenses that have not yet occurred based on convDate by acctName input"
    x = expenses.find({ "DayOfMonth": { "$lte": CurrDay}, 'acctID': acctName}).sort('DayOfMonth').sort('acct')
    return x

def listExpenses(acctName):
    "This function returns all expenses for an account for the entire month regardless of day"
    x = expenses.find({ 'acctID': acctName}).sort('LastPostedDate')
    return x

def dfMonthlyExpenses(acctName):
    "This function returns all expenses for an account for the entire month regardless of day as a dataframe"
    X = pd.DataFrame(list(getExpenses(acctName)))
    return X

def convDf(object):
    "This function converts an array/object to a dataframe"
    X = pd.DataFrame(list(object))
    return X

def printAsDataFrame(object):
    "This function uses the convDf function to convert an array to a dataframe and then print to console"
    df = convDf(object)
    print(tabulate(df, headers='keys'))

def printDf(dataframe):
    print(tabulate(dataframe, headers='keys'))

def totalExpenses(acctName):
    "This function totals all expenses for an account each month by a dataframe and returns value"
    data = listExpenses(acctName)
    df = convDf(data)
    X = df['Amount'].sum()
    return X


def txIterate(frequency, inputdate):
    "This function will accept an input of frequency and calculate the next convDate of iteration based on an inputdate"
    startdate = inputdate
    if frequency == 'Biweekly':
        delta = dt.timedelta(weeks=2)
    elif frequency == 'Weekly':
        delta = dt.timedelta(weeks=1)
    elif frequency == 'Monthly':
        delta = relativedelta(months=1)
    elif frequency == 'Daily':
        delta = dt.timedelta(days=1)
    X = startdate + delta
    return X

class expense:

    def __init__(self, expName,expID=None):
        if expName != 'ID':
            self.data = expenses.find_one({"Name": expName})
        elif expName == 'ID' and expID is not None:
            self.data = expenses.find_one({"_id": expID})
        self.amount = self.data['Amount']
        self.name = self.data['Name']
        self.acct = self.data['acctID']
        self.startDate = self.data['StartDate']
        self.endDate = self.data['EndDate']
        self.dayOfMonth = self.data['DayOfMonth']
        self.LastPostedDate = self.data['LastPostedDate']
        self.DateThisMonth = dt.datetime(CurrYear,CurrMonth,self.dayOfMonth)
        self.expID = self.data['_id']

    def reset(self):
        "Reinitializes the current instance of the class. Intended for use after new values have been written to the DB"
        self.__init__(self.name)
    
    def display(self):
        print("Exp name: ", self.name, end=', ')
        print("Exp Amount: $", self.amount, end=', ')
        print("Exp Account: ", self.acct, end=', ')
        print("Exp Start Date: ", self.startDate, end=', ')
        print("Exp End Date: ", self.endDate, end=', ')
        print("Exp Day of Month: ", self.dayOfMonth)

    def changeAmount(self, expNewAmount):
        expenses.update_one(
            { 'Name': self.name },
            { '$set': {'Amount': expNewAmount}}
        )
        self.reset()
    def changeName(self, expNewName):
        expenses.update_one(
            { 'Name': self.name},
            { '$set': { 'Name': expNewName}}
        )
        self.reset()
    def addEndDate(self, expEndDateInput):
        expEndDate = convDate(expEndDateInput)
        expenses.update_one(
            { 'Name': self.name},
            { '$set': { 'EndDate': expEndDate}}
        )
        self.reset()
    def setLastPostedDate(self, LastPostedDate):
        expenses.update_one(
            { 'Name': self.name},
            { '$set': { 'LastPostedDate': LastPostedDate}}
        )
        self.reset()
    def changeAmount(self, newAmount):
        expenses.update_one(
            { 'Name': self.name},
            { '$set': { 'Amount': newAmount}}
        )