"""This is a docstring"""

import pymongo
import BudgetEngine as be
import matplotlib.pyplot as plt
from bson import ObjectId

accountImport = [
    { "name": "Joint", "Institution": "BankName"},
    { "name": "Expense", "Institution": "BankName"},
]

actions = [
            "1: Print all accounts",
            "2: Update current balance",
            "3: Set low balance level",
            "4: Project balance",
            "5: Enter New Account",
            "6: Delete account"
        ]


def acctMenu():
    """Defining account menu options"""
    continueAcctLoop = 1
    while continueAcctLoop == 1:
        action = be.menuGen(actions,"Account menu",0)
        if action == '1':
            be.printAsDataFrame(be.listCollection("accounts"))
        if action == '2':
            acctToUpdate = input("Please enter account to update: ")
            acct = be.acct(acctToUpdate)
            print(acct.name,"has been selected")
            newBalance = float(input("Please input new balance (XX.XX) : "))
            acct.setCurrBalance(newBalance)
        if action == '3':
            acctToUpdate = input("Please enter account to update: ")
            acct = be.acct(acctToUpdate)
            print(acct.name,"has been selected")
            newLowBalance = float(input("Please enter new low balance alert level: (XXXX.XX)"))
            acct.setLowBalAlertLevel(newLowBalance)
        if action == '4':
            projEndInput = input("Enter end date for projection: ")
            projAcctInput = input("Enter account for projection: ")
            acct = be.acct(projAcctInput)
            proj = acct.projRev(projEndInput)
            projDf = proj[2]
            print(projAcctInput,"account projected balance for",projEndInput,"will be $",proj[0])
            projDf.plot(kind='line',x='Date',y='Balance',title=('%s account projected balances, $%s' % (projAcctInput, proj[0])))
            plt.savefig('/projoutput/output.png')
            print("Projection graph available at: http://%s:8080/output.png" % be.v.envVars('HostExternalIP'))
        if action == '5':
            newAcctName = input("Enter name for new account: ")
            newAcctInst = input("Enter name of institution for new account: ")
            newAcctBalance = float(input("Enter current balance for new account: "))
            newAcctLowBalance = float(input("Enter low balance alert threshold for new account: "))
            insertAccount(newAcctName, newAcctInst, newAcctBalance, newAcctLowBalance)
        if action == '6':
            be.printAsDataFrame(be.listCollection('accounts'))
            delAcctID = input("Enter _id for account to delete: ")
            deleteAcct(delAcctID)
        if action == 'Q':
            continueAcctLoop = 0

def insertAccount(newAcctName, newAcctInst, newAcctBalance, newAcctLowBalance):
    """Function to create a new account and generate blank TxLog"""
    acctFilter = {"Name":newAcctName}
    acctCheck =  be.accts.count_documents(acctFilter, limit=1)
    if acctCheck == 1:
        print("Account already exists, please review for validity")
    elif acctCheck < 1:
        print("Account does not exist. Will write to DB.")
        if (newAcctName!=None) or (newAcctInst!=None) or (newAcctBalance!=None) or (newAcctLowBalance!=None):
            accountToWrite = {
            "Institution": newAcctInst,
            "Name": newAcctName,
            "CurrBalance": newAcctBalance,
            "LowBalance": newAcctLowBalance,
            "TxLastPosted": None
            }
            x = be.accts.insert_one(accountToWrite)
            print(x.inserted_id)
            be.CreateBlankTxLog(newAcctName)

def listRevenue(acctName):
    "This function returns all expenses for an account for he entire month regardless of day"
    x = be.revenues.find({ 'Account': acctName}).sort('StartDate')

def deleteAcct(delAcctID):
    """Function to delete an account based on mongodb _id"""
    x = be.accts.delete_one({"_id":ObjectId(delAcctID)})
    print(x.deleted_count, " documents deleted.")

class acct:

    def __init__(self, acctName,acctID=None):
        if acctName != 'ID':
            self.data = be.expenses.find_one({"Name": acctName})
        elif acctName == 'ID' and acctID is not None:
            self.data = be.expenses.find_one({"_id": acctID})
        self.data = be.accts.find_one({"Name": acctName})
        self.revData = be.listRevenue(acctName)
        self.expData = be.listExpenses(acctName)
        self.institution = self.data['Institution']
        self.name = self.data['Name']
        self.acctID = self.data['_id']
        self.CurrBalance = float(self.data['CurrBalance'])
        self.LowBalAlert = self.data['LowBalance']
        self.TxLastPosted = self.data['TxLastPosted']
    
    def reset(self):
        "Reinitializes the current instance of the class. Intended for use after new values have been written to the DB"
        self.__init__(self.acctName)

    def display(self):
        print("Acct name: ", self.name, end=', ')
        print("Acct Institution: $", self.institution, end=' ')

    def name(self):
        return self.name
    
    def expenses(self):
        "This function will list all expenses for the account"
        be.printDf(self.expData)

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
        be.printDf(self.revData)


    def sumExpenses(self):
        "This function calculates the total expenses to be expected in a month"
        expTotal = 0
        for i in self.expData:
            iterExp = be.expense(i['Name'])
            expTotal = expTotal + iterExp.amount
            #print("Adding exp: ", i['Name'], "Amount: $", i['Amount'], "Balance now: ", round(expTotal,2))
        return expTotal
    def setCurrBalance(self, currBalance):
        be.accts.update_one(
            { '_id': self.acctID},
            { '$set':
                {
                    'CurrBalance': currBalance
                }
                }
        )
    def setLowBalAlertLevel(self, LowBalLevel):
        be.accts.update_one(
            { '_id': self.acctID},
            { '$set':
                {
                    'LowBalance': LowBalLevel
                }
                }
        )

    def projRev(self, projEndDateInput):
        "This function projects account balances daily for an input of projEndDateInput"
        projEndDate = be.convDate(projEndDateInput)
        #Creating shell projection record
        projID = "End: " + projEndDateInput + " Start: " + str(be.CurrInst)
        StartDate = be.CurrDate
        x = be.projection.insert_one(
            {
                "Name":         projID,
                "Acct":         self.name,     
                "StartDate":    StartDate,
                "EndDate":      be.convDate(projEndDateInput)
            }
        )
        projRecID = x.inserted_id
        projRecIDQuery = { '_id': projRecID }
        be.verbose(projRecID)
        
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
            be.projection.update_one(projRecIDQuery,writeprojTxpush)

        def writeprojTxsLdgrTx(seq,memo,amount,date,txtypeinput):
            if txtypeinput == 'Revenue': txtype = 'credit'
            if txtypeinput == 'Expenses': txtype = 'debit'
            writeprojTxpush = {'$push':
                                    {'Ledger':
                                    {   "Seq": seq,
                                        "Memo": memo,
                                        "Amount": amount,
                                        "Date": be.convDate(date),
                                        "TxType": txtype
                                    }}
                                }
            be.projection.update_one(projRecIDQuery,writeprojTxpush)
    
        def writeprojDateBalance(date,balance):
            writeprojBalancepush = {'$push':
                                    {'Balance':
                                    {   
                                        "Date": date,
                                        "Balance": balance
                                    }}
                                }
            be.projection.update_one(projRecIDQuery,writeprojBalancepush)

        #Writing Revenue transactions to projection records
        for i in self.revData:
            iRev = be.revenue(i['Name'])
            iterOccur = 0
            iterDate = iRev.LastDatePosted
            projRevTotal = 0
            be.verbose(("%s will occur on a %s basis in the amount of %s starting from the last occurrence on %s" % (iRev.name, iRev.Frequency,iRev.amount,iRev.startDate)))
            be.verbose(("Remaining Occurrences this projection:"))
            while (iterDate < projEndDate):
                iterDate = be.txIterate(iRev.Frequency,iterDate)
                if iterDate not in iRev.exclusionDates and iterDate < projEndDate and iRev.endDate == None : 
                    iterOccur = iterOccur + 1
                    projRevTotal = projRevTotal + iRev.amount
                    be.verbose(("#%s %s %s Rev Amount: %s Running Total %s" % (iterOccur,iRev.name,iterDate,iRev.amount,projRevTotal)))
                    writeprojTx(iRev.name,iRev.amount,iterDate,'Revenue')
                elif iterDate in iRev.exclusionDates: 
                    pass  
                elif iRev.endDate != None:
                    pass
        #Writing Expense transactions to projection records
        for i in self.expData:
            iExp = be.expense('ID',i['_id'])
            iterOccur = 0
            iterDate = iExp.LastPostedDate
            projExpTotal = 0
            endDateReached = 0
            be.verbose(("%s will be deducted from %s acct in the amount of %s starting from the last occurrence on %s" % (iExp.name,iExp.acct,iExp.amount,iExp.startDate)))
            while iterDate < projEndDate and endDateReached == 0:
                iterOccur = iterOccur + 1
                if iterDate < projEndDate and iExp.endDate == None:
                    projExpTotal = projExpTotal + iExp.amount
                    be.verbose(("#%s %s %s Exp Amount: %s Running Total %s" % (iterOccur,iExp.name,iterDate,iExp.amount,projExpTotal)))
                    writeprojTx(iExp.name,iExp.amount,iterDate,'Expenses')
                elif iExp.endDate != None and iExp.endDate > iterDate and iterDate < projEndDate:
                    projExpTotal = projExpTotal + iExp.amount
                    be.verbose(("#%s %s %s Exp Amount: %s Running Total %s, EndDate present" % (iterOccur,iExp.name,iterDate,iExp.amount,projExpTotal)))
                    writeprojTx(iExp.name,iExp.amount,iterDate,'Expenses')                
                elif iExp.endDate != None and iExp.endDate < iterDate and iterDate < projEndDate:
                    if iExp.endDate < iterDate:
                        be.verbose(("   %s %s End Date already reached, will not add" % (iExp.name,iterDate)))
                        endDateReached = 1
                iterDate = be.txIterate('Monthly',iterDate)
        #Outputting Data written to DB
        projTxs = be.projection.find_one(projRecIDQuery)
        for exp in projTxs['Expenses']:
            be.verbose((exp['Memo'],exp['Amount'],exp['Date']))
        for rev in projTxs['Revenue']:
            be.verbose((rev['Memo'],rev['Amount'],rev['Date']))
        projTxsIncrDate = be.CurrDate
        projTxsLdgrSeq = 1
        be.verbose("Iterating dates and finding expense and revenue records to calculate")
        ###
        ###Writing Data to Projection Ledger
        ###
        while projTxsIncrDate < projEndDate:
            #Looking for revenue to write to ledger
            be.verbose(("Searching ",str(projTxsIncrDate.strftime('%F'))," in ",projRecID))
            projRevIterData = be.projection.find(
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
                    be.verbose("Seq# %s Expese: %s Date: %s Amount %s" % (projTxsLdgrSeq,iRev,iDate,iAmount))
                    writeprojTxsLdgrTx(projTxsLdgrSeq,iRev,iAmount,iDate,'Revenue')
                    projTxsLdgrSeq = projTxsLdgrSeq + 1
            #Looking for expenses to write to ledger
            projExpIterData = be.projection.find(
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
                    be.verbose("Seq# %s Expese: %s Date: %s Amount %s" % (projTxsLdgrSeq,iExp,iDate,iAmount))
                    writeprojTxsLdgrTx(projTxsLdgrSeq,iExp,iAmount,iDate,'Expenses')
                    projTxsLdgrSeq = projTxsLdgrSeq + 1
            projTxsIncrDate = be.txIterate('Daily',projTxsIncrDate)
        ###
        ### Calculating Balances
        ###
        iterDate = StartDate
        projBalanceTotal = self.CurrBalance
        balDfCols = ['Date','Balance']
        balDf = be.pd.DataFrame(columns=balDfCols)
        while iterDate < projEndDate:
            projLdgrData = be.projection.aggregate([
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
            be.verbose("=====Searching for transactions for %s=====" % iterDate)
            for i in projLdgrData:
                Ledger = (i['Ledger'])
                iSeq = Ledger['Seq']
                iMemo = Ledger['Memo']
                iAmount = Ledger['Amount']
                iDate = Ledger['Date']
                iTxType = Ledger['TxType']
                if iDate == iterDate:
                    if iTxType == 'credit':
                        be.verbose("#Credit Transactions#")
                        projBalanceTotal = projBalanceTotal + iAmount
                        be.verbose("Seq ID: %s Date: %s Memo: %s Amonut: $%s TxType: %s Running Balance %s"% (iSeq,iDate,iMemo,iAmount,iTxType,projBalanceTotal))
                    elif iTxType == 'debit':
                        be.verbose("#Debit Transactions#")
                        projBalanceTotal = projBalanceTotal - iAmount
                        be.verbose("Seq ID: %s Date: %s Memo: %s Amonut: $%s TxType: %s Running Balance %s"% (iSeq,iDate,iMemo,iAmount,iTxType,projBalanceTotal))
            writeprojDateBalance(iterDate,projBalanceTotal)
            if projBalanceTotal < self.LowBalAlert: print(iterDate,": Balance is below Low Alert Level of %s at %s" % (self.LowBalAlert,projBalanceTotal))
            #Write balance values to dataframe
            toDfData = be.pd.DataFrame({'Date': [iterDate],
                        'Balance': [projBalanceTotal]})
            frames = [toDfData,balDf]
            balDf = be.pd.concat(frames)
            iterDate = be.txIterate('Daily',iterDate)
        numBalances = balDf[balDf.columns[0]].count()
        return round(projBalanceTotal,2),projRecID,balDf,numBalances

#Account functions pending removal
def printAcct(account):
    "(DEPRECATED): This function returns and prints acoount info for account name input"
    x = be.accts.find_one({"name": account})
    be.pprint.pprint(x)

def listAccounts():
    "(DEPRECATED): This function returns all accounts"
    x = be.accts.find()
    return x

def dfMonthlyRevenue(acctName):
    "(DEPRECATED): This function returns all expenses for an account for the entire month regardless of day as a dataframe"
    X = be.pd.DataFrame(list(be.listRevenue(acctName)))
    return X