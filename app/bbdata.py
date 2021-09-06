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
from bson import ObjectId
import os


#connecting to db
myclient = pymongo.MongoClient("mongodb://mongo:27017/")
bbdb = myclient["BudgetBalancer"]

#defining collection cursors
accts = bbdb["accounts"]
expenses = bbdb["expenses"]
revenues = bbdb["revenue"]
projection = bbdb["projections"]
postedtx = bbdb['postedtx']

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

def printAcct(account):
    "This function returns and prints acoount info for account name input"
    x = accts.find_one({"name": account})
    pprint.pprint(x)

def findExp(expName):
    "This function returns and prints expenses info for expenses name input"
    x = expenses.find_one({"Name": expName})
    pprint.pprint(x)
    return x

def listCollection(collection):
    "This funtion returns the contents of an entire collection as input by name"
    listColData = bbdb[collection]
    x = listColData.find()
    return x

def printRecord(collection, name):
    data = bbdb[collection].find({ 'Name': name})
    return data

def getExpenses(acctName):
    "This function returns all expenses that have not yet occurred based on convDate by acctName input"
    x = expenses.find({ "DayOfMonth": { "$lte": CurrDay}, 'acctID': acctName}).sort('DayOfMonth').sort('acct')
    return x

def listExpenses(acctName):
    "This function returns all expenses for an account for the entire month regardless of day"
    x = expenses.find({ 'acctID': acctName}).sort('LastPostedDate')
    return x

def listRevenue(acctName):
    "This function returns all expenses for an account for he entire month regardless of day"
    x = revenues.find({ 'Account': acctName}).sort('StartDate')

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

def listRevenue(acctName):
    "This function returns all sources of revenue for a given acctName"
    x = revenues.find({ 'Account': acctName})
    return x
def listAccounts():
    "This function returns all accounts"
    x = accts.find()
    return x

def dfMonthlyRevenue(acctName):
    "This function returns all expenses for an account for the entire month regardless of day as a dataframe"
    X = pd.DataFrame(list(listRevenue(acctName)))
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



class acct:

    def __init__(self, acctName,acctID=None):
        if acctName != 'ID':
            self.data = expenses.find_one({"Name": acctName})
        elif acctName == 'ID' and acctID is not None:
            self.data = expenses.find_one({"_id": acctID})
        self.data = accts.find_one({"Name": acctName})
        self.revData = listRevenue(acctName)
        self.expData = listExpenses(acctName)
        self.institution = self.data['Institution']
        self.name = self.data['Name']
        self.acctID = self.data['_id']
        self.CurrBalance = self.data['CurrBalance']
        self.LowBalAlert = self.data['LowBalance']
        self.TxLastPosted = self.data['TxLastPosted']
    
    def reset(self):
        "Reinitializes the current instance of the class. Intended for use after new values have been written to the DB"
        self.__init__(self.acctName)

    def display(self):
        print("Acct name: ", self.name, end=', ')
        print("Acct Institution: $", self.institution, end=' ')
    
    def expenses(self):
        "This function will list all expenses for the account"
        printDf(self.expData)

    def sumRevenue(self):
        "This function calculates the total revenue to be expected in a month assuming 4 weeks."
        self.revData = listRevenue(self.name)
        revTotal = 0
        for i in self.revData:
            sumRevFrequencyInput = i['Frequency']
            sumRevAmount = i['Amount']
            if sumRevFrequencyInput == 'Biweekly': sumRevFrequency = 2
            if sumRevFrequencyInput == 'Monthly': sumRevFrequency = 1
            if sumRevFrequencyInput == 'Weekly': sumRevFrequency = 4
            revTotal = revTotal + (sumRevAmount * sumRevFrequency)
        return revTotal
    
    def revenues(self):
        "This function will list all revenues for the account"
        printDf(self.revData)


    def sumExpenses(self):
        "This function calculates the total expenses to be expected in a month"
        expTotal = 0
        for i in self.expData:
            iterExp = expense(i['Name'])
            expTotal = expTotal + iterExp.amount
            #print("Adding exp: ", i['Name'], "Amount: $", i['Amount'], "Balance now: ", round(expTotal,2))
        return expTotal
    def setCurrBalance(self, currBalance):
        accts.update_one(
            { '_id': self.acctID},
            { '$set':
                {
                    'CurrBalance': currBalance
                }
                }
        )
    def setLowBalAlertLevel(self, LowBalLevel):
        accts.update_one(
            { '_id': self.acctID},
            { '$set':
                {
                    'LowBalance': LowBalLevel
                }
                }
        )

    def projRev(self, projEndDateInput):
        "This function projects account balances daily for an input of projEndDateInput"
        projEndDate = convDate(projEndDateInput)
        #Creating shell projection record
        projID = "End: " + projEndDateInput + " Start: " + str(CurrInst)
        StartDate = CurrDate
        x = projection.insert_one(
            {
                "Name":         projID,
                "Acct":         self.name,     
                "StartDate":    StartDate,
                "EndDate":      convDate(projEndDateInput)
            }
        )
        projRecID = x.inserted_id
        projRecIDQuery = { '_id': projRecID }
        verbose(projRecID)
        
        #Defining a few functions for things that will be written to db

        def writeprojTx(memo,amount,date,txtypeinput):
            if txtypeinput == 'Revenue': txtype = 'Revenue'
            if txtypeinput == 'Expenses': txtype = 'Expenses'
            writeprojTxpush = {'$push':
                                    {txtype:
                                    {   "Memo": memo,
                                        "Amount": amount,
                                        "Date": date
                                    }}
                                }
            projection.update_one(projRecIDQuery,writeprojTxpush)

        def writeprojTxsLdgrTx(seq,memo,amount,date,txtypeinput):
            if txtypeinput == 'Revenue': txtype = 'credit'
            if txtypeinput == 'Expenses': txtype = 'debit'
            writeprojTxpush = {'$push':
                                    {'Ledger':
                                    {   "Seq": seq,
                                        "Memo": memo,
                                        "Amount": amount,
                                        "Date": convDate(date),
                                        "TxType": txtype
                                    }}
                                }
            projection.update_one(projRecIDQuery,writeprojTxpush)
    
        def writeprojDateBalance(date,balance):
            writeprojBalancepush = {'$push':
                                    {'Balance':
                                    {   
                                        "Date": date,
                                        "Balance": balance
                                    }}
                                }
            projection.update_one(projRecIDQuery,writeprojBalancepush)

        #Writing Revenue transactions to projection records
        for i in self.revData:
            iRev = revenue(i['Name'])
            iterOccur = 0
            iterDate = iRev.LastDatePosted
            projRevTotal = 0
            verbose(("%s will occur on a %s basis in the amount of %s starting from the last occurrence on %s" % (iRev.name, iRev.Frequency,iRev.amount,iRev.startDate)))
            verbose(("Remaining Occurrences this projection:"))
            while (iterDate < projEndDate):
                iterDate = txIterate(iRev.Frequency,iterDate)
                if iterDate not in iRev.exclusionDates and iterDate < projEndDate and iRev.endDate == None : 
                    iterOccur = iterOccur + 1
                    projRevTotal = projRevTotal + iRev.amount
                    verbose(("#%s %s %s Rev Amount: %s Running Total %s" % (iterOccur,iRev.name,iterDate,iRev.amount,projRevTotal)))
                    writeprojTx(iRev.name,iRev.amount,iterDate,'Revenue')
                elif iterDate in iRev.exclusionDates: 
                    pass  
                elif iRev.endDate != None:
                    pass
        #Writing Expense transactions to projection records
        for i in self.expData:
            iExp = expense('ID',i['_id'])
            iterOccur = 0
            iterDate = iExp.LastPostedDate
            projExpTotal = 0
            endDateReached = 0
            verbose(("%s will be deducted from %s acct in the amount of %s starting from the last occurrence on %s" % (iExp.name,iExp.acct,iExp.amount,iExp.startDate)))
            while iterDate < projEndDate and endDateReached == 0:
                iterOccur = iterOccur + 1
                if iterDate < projEndDate and iExp.endDate == None:
                    projExpTotal = projExpTotal + iExp.amount
                    verbose(("#%s %s %s Exp Amount: %s Running Total %s" % (iterOccur,iExp.name,iterDate,iExp.amount,projExpTotal)))
                    writeprojTx(iExp.name,iExp.amount,iterDate,'Expenses')
                elif iExp.endDate != None and iExp.endDate > iterDate and iterDate < projEndDate:
                    projExpTotal = projExpTotal + iExp.amount
                    verbose(("#%s %s %s Exp Amount: %s Running Total %s, EndDate present" % (iterOccur,iExp.name,iterDate,iExp.amount,projExpTotal)))
                    writeprojTx(iExp.name,iExp.amount,iterDate,'Expenses')                
                elif iExp.endDate != None and iExp.endDate < iterDate and iterDate < projEndDate:
                    if iExp.endDate < iterDate:
                        verbose(("   %s %s End Date already reached, will not add" % (iExp.name,iterDate)))
                        endDateReached = 1
                iterDate = txIterate('Monthly',iterDate)
        #Outputting Data written to DB
        projTxs = projection.find_one(projRecIDQuery)
        for exp in projTxs['Expenses']:
            verbose((exp['Memo'],exp['Amount'],exp['Date']))
        for rev in projTxs['Revenue']:
            verbose((rev['Memo'],rev['Amount'],rev['Date']))
        projTxsIncrDate = CurrDate
        projTxsLdgrSeq = 1
        verbose("Iterating dates and finding expense and revenue records to calculate")
        ###
        ###Writing Data to Projection Ledger
        ###
        while projTxsIncrDate < projEndDate:
            #Looking for revenue to write to ledger
            verbose(("Searching ",str(projTxsIncrDate.strftime('%F'))," in ",projRecID))
            projRevIterData = projection.find(
                { 
                    '_id': projRecID,
                    'Revenue.Date': projTxsIncrDate
                },
                {
                    'Revenue.$': 1,
                }
                )
            if projRevIterData is None:
                pass
                #print("No revenue record returned")
            elif projRevIterData is not None:
                #print("Revenue record returned")
                #pprint.pprint(projRevIterData)
                for i in projRevIterData:
                    iRev = i['Revenue'][0]['Memo']
                    iDate = i['Revenue'][0]['Date'].strftime('%F')
                    iAmount = i['Revenue'][0]['Amount']
                    verbose("Seq# %s Expese: %s Date: %s Amount %s" % (projTxsLdgrSeq,iRev,iDate,iAmount))
                    writeprojTxsLdgrTx(projTxsLdgrSeq,iRev,iAmount,iDate,'Revenue')
                    projTxsLdgrSeq = projTxsLdgrSeq + 1
            #Looking for expenses to write to ledger
            projExpIterData = projection.find(
                {
                    '_id': projRecID,
                    'Expenses.Date': projTxsIncrDate
                },
                {
                    'Expenses.$': 1
                }
            )
            #if projExpIterData.count() == 0:
                #print("No expense record returned")
            if projExpIterData is not None:
                #print("Expense record(s) returned")
                for i in projExpIterData:
                    iExp = i['Expenses'][0]['Memo']
                    iDate = i['Expenses'][0]['Date'].strftime('%F')
                    iAmount = i['Expenses'][0]['Amount']
                    verbose("Seq# %s Expese: %s Date: %s Amount %s" % (projTxsLdgrSeq,iExp,iDate,iAmount))
                    writeprojTxsLdgrTx(projTxsLdgrSeq,iExp,iAmount,iDate,'Expenses')
                    projTxsLdgrSeq = projTxsLdgrSeq + 1
            projTxsIncrDate = txIterate('Daily',projTxsIncrDate)
        ###
        ### Calculating Balances
        ###
        iterDate = StartDate
        projBalanceTotal = self.CurrBalance
        balDfCols = ['Date','Balance']
        balDf = pd.DataFrame(columns=balDfCols)
        while iterDate < projEndDate:
            projLdgrData = projection.aggregate([
            {
                '$match': {
                    '_id': ObjectId(projRecID)
                }
            }, {
                '$unwind': {
                    'path': '$Ledger'
                }
            }, {
                '$project': {
                    'Ledger.Seq': 1, 
                    'Ledger.Memo': 1, 
                    'Ledger.Amount': 1, 
                    'Ledger.Date': 1, 
                    'Ledger.TxType': 1
                }
            }, {
                '$project': {
                    '_id': 0
                }
            }
        ])
            verbose("=====Searching for transactions for %s=====" % iterDate)
            for i in projLdgrData:
                Ledger = (i['Ledger'])
                iSeq = Ledger['Seq']
                iMemo = Ledger['Memo']
                iAmount = Ledger['Amount']
                iDate = Ledger['Date']
                iTxType = Ledger['TxType']
                if iDate == iterDate:
                    if iTxType == 'credit':
                        verbose("#Credit Transactions#")
                        projBalanceTotal = projBalanceTotal + iAmount
                        verbose("Seq ID: %s Date: %s Memo: %s Amonut: $%s TxType: %s Running Balance %s"% (iSeq,iDate,iMemo,iAmount,iTxType,projBalanceTotal))
                    elif iTxType == 'debit':
                        verbose("#Debit Transactions#")
                        projBalanceTotal = projBalanceTotal - iAmount
                        verbose("Seq ID: %s Date: %s Memo: %s Amonut: $%s TxType: %s Running Balance %s"% (iSeq,iDate,iMemo,iAmount,iTxType,projBalanceTotal))
            writeprojDateBalance(iterDate,projBalanceTotal)
            if projBalanceTotal < self.LowBalAlert: print(iterDate,": Balance is below Low Alert Level of %s at %s" % (self.LowBalAlert,projBalanceTotal))
            #Write balance values to dataframe
            toDfData = pd.DataFrame({'Date': [iterDate],
                        'Balance': [projBalanceTotal]})
            frames = [toDfData,balDf]
            balDf = pd.concat(frames)
            iterDate = txIterate('Daily',iterDate)
        numBalances = balDf[balDf.columns[0]].count()
        return round(projBalanceTotal,2),projRecID,balDf,numBalances
           
class revenue:

    def __init__(self, revName):
        self.data = revenues.find_one({"Name": revName})
        self.amount = self.data['Amount']
        self.name = self.data['Name']
        self.acct = self.data['Account']
        self.startDate = self.data['StartDate']
        self.endDate = self.data['EndDate']
        self.exclusionDates = self.data['ExclusionDates']
        self.Frequency = self.data['Frequency']
        self.LastDatePosted = self.data['LastDatePosted']

    def reset(self):
        "Reinitializes the current instance of the class. Intended for use after new values have been written to the DB"
        self.__init__(self.name)
    
    def display(self):
        print("Rev name: ", self.name, end=', ')
        print("Rev Amount: $", self.amount, end=', ')
        print("Rev Account: ", self.acct, end=', ')
        print("Rev Start Date: ", self.startDate, end=', ')
        print("Rev End Date: ", self.endDate)
        iterNum = 0
        for i in self.exclusionDates:
            iterNum = iterNum + 1
            print("Exclusion Date #%s %s" % (iterNum, i))

    def addExclDate(self, revExclDate):
        if revExclDate not in self.exclusionDates:
            revenues.update_one(
                { 'Name': self.name },
                { '$push': {'ExclusionDates': revExclDate}}
            )
            self.reset()
        elif revExclDate in self.exclusionDates:
            print("Value already exists")

    def setLastPostedDate(self, LastPostedDate):
        revenues.update_one(
                { 'Name': self.name },
                { '$set': {'LastDatePosted': LastPostedDate}}
            )
        self.reset()

