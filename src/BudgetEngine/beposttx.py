from re import search
from pandas.io import json
import BudgetEngine as BudgetEngine 
import bson

actions = [
    "1: View all posted transactions for account",
    "2: View posted transactions for account since date",
    "3: Post transactions",
    "4: Create posted transaction log for account",
    "5: Search for transactions by memo and TxType in account"
]

def postTxMenu():
    continuePostLoop = 1

    while continuePostLoop == 1:
        action = BudgetEngine.menuGen(actions,"Post Transactions Menu",0)
        if action == 'Q':
            continuePostLoop = 0
        if action == '1':
            print("View all posted transactions")
            BudgetEngine.printAsDataFrame(BudgetEngine.listCollection("accounts"))
            acctName = input("What account would you like to get transactions for? ")
            output = getTxData(acctName)
            dfTxData = BudgetEngine.mongoArrayDf(output,'PostedTxs')
            BudgetEngine.printDf(dfTxData)
        if action == '2':
            print("View all posted transacations since date, work in progress")
        if action == '3':
            print("Post transactions, work in progress")
            BudgetEngine.printAsDataFrame(BudgetEngine.listCollection("accounts"))
            TxAccount = input("What account should the transaction be posted to? ")
            currAcct = BudgetEngine.acct(TxAccount)
            TxType = input("What type of transaction is this? (credit/debit) ")
            if TxType == 'credit':
                BudgetEngine.printAsDataFrame(BudgetEngine.listRevenue(TxAccount))
                KnownRev = input("Is the transaction in the above list? If yes, please enter name, else, enter AdHoc ({Enter Name}/ AdHoc ) ")
                if KnownRev == 'AdHoc':
                    TxMemo = input("Please enter name of AdHoc transaction: ")
                    IsAdhoc = True
                    TxDate = BudgetEngine.convDate(input("Please enter the date of the transaction (YYYY-MM-DD) "))
                    TxAmount = float(input("Please enter the amount of the transaction (XX.XX) "))
                elif KnownRev != 'AdHoc':
                    IsAdhoc = False
                    revName = KnownRev
                    currTx = BudgetEngine.revenue(revName)
                    TxMemo = currTx.name
                    TxAmountConf = input("Is the transaction amount $%s (y/n) " % currTx.amount)
                    if TxAmountConf == 'y': TxAmount = currTx.amount
                    if TxAmountConf == 'n': TxAmount = float(input("Please enter the amount of the transaction (XX.XX) "))
                    TxDateNext = BudgetEngine.txIterate(currTx.Frequency,currTx.LastDatePosted)
                    TxDateConf = input("Is the date of the transaction %s?: (y/n)" % TxDateNext)
                    if TxDateConf == 'y': TxDate = TxDateNext
                    if TxDateConf == 'n': TxDate = BudgetEngine.convDate(input("Please enter the date of the transaction (YYYY-MM-DD) "))
                    currTx.setLastPostedDate(TxDate)
                NewBalance = currAcct.CurrBalance + TxAmount
                currAcct.setCurrBalance(NewBalance)
            if TxType == 'debit':
                BudgetEngine.printAsDataFrame(BudgetEngine.listExpenses(TxAccount))
                KnownExp = input("Is the transaction in the above list? If yes, please enter name, else, enter AdHoc ({Enter Name}/ AdHoc ) ")
                if KnownExp == 'AdHoc':
                    TxMemo = input("Please enter name of AdHoc transaction: ")
                    IsAdhoc = True
                    TxDate = BudgetEngine.convDate(input("Please enter the date of the transaction (YYYY-MM-DD) "))
                    TxAmount = float(input("Please enter the amount of the transaction (XX.XX) "))
                elif KnownExp != 'AdHoc':
                    IsAdhoc = False
                    expName = KnownExp
                    currTx = BudgetEngine.expense(expName)
                    TxMemo = currTx.name
                    TxAmountConf = input("Is the transaction amount $%s (y/n) " % currTx.amount)
                    if TxAmountConf == 'y': TxAmount = currTx.amount
                    if TxAmountConf == 'n': TxAmount = float(input("Please enter the amount of the transaction (XX.XX) "))
                    TxDateNext = BudgetEngine.txIterate('Monthly',currTx.LastPostedDate)
                    TxDateConf = input("Is the date of the transaction %s?: (y/n)" % TxDateNext)
                    if TxDateConf == 'y': TxDate = TxDateNext
                    if TxDateConf == 'n': TxDate = BudgetEngine.convDate(input("Please enter the date of the transaction (YYYY-MM-DD) "))
                    currTx.setLastPostedDate(TxDate)
                NewBalance = round((currAcct.CurrBalance - TxAmount),2)
                currAcct.setCurrBalance(NewBalance)
            print("Account: %s Type: %s Date: %s Amount: $%s Memo: %s Adhoc: %s Balance: %s" % (TxAccount,TxType,TxDate,TxAmount,TxMemo,IsAdhoc,NewBalance))
            writeTx(TxAccount,TxType,TxDate,TxAmount,TxMemo,IsAdhoc,NewBalance)
        if action == '4':
            print("Create blank transaction log")
            acctName = input("What account would you like to create a transaction log for? ")
            CreateBlankTxLog(acctName)
        if action == '5':
            print("Search for transactions in specified account by TxType and Memo")
            acctName = input("Please enter name of account to search: ")
            TxType = input("Please enter TxType to search (credit/debit) : ")
            Memo = input("Please enter Memo to search : ")
            output = searchTxData(acctName,Memo,TxType)
            dfsearchTxData = BudgetEngine.mongoArrayDf(output,'PostedTxs')
            BudgetEngine.printDf(dfsearchTxData)
        


def getTxData(acctName):
    "This function will get all transactions for a given account"
    #Get data for account
    acctTxData = BudgetEngine.postedtx.aggregate([
    {
        '$match': {
            'acctName': acctName
        }
    }, {
        '$unwind': {
            'path': '$PostedTxs'
        }
    },  {
        '$group': {
            '_id': '$acctName', 
            'PostedTxs': {
                '$push': {
                    'txID': '$PostedTxs.txID',
                    'Memo': '$PostedTxs.Memo', 
                    'Amount': '$PostedTxs.Amount', 
                    'Date': {
                        '$dateToString': {
                            'format': '%Y-%m-%d', 
                            'date': '$PostedTxs.Date'}}, 
                    'TxType': '$PostedTxs.TxType', 
                    'AdHoc': '$PostedTxs.AdHoc', 
                    'Balance': '$PostedTxs.Balance'
                }
            }
        }
    }
])

    return acctTxData

def writeTx(TxAccount,TxType,TxDate,TxAmount,TxMemo,IsAdhoc,TxBalance):
    "This function will write posted transactions"
    postedTxAcctQuery = { 'acctName': TxAccount }
    postedTxToWrite = {'$push':
            {'PostedTxs':
                {   "txID": bson.ObjectId(),
                    "Memo": TxMemo,
                    "Amount": TxAmount,
                    "Date": BudgetEngine.convDate(TxDate),
                    "TxType": TxType,
                    "AdHoc": IsAdhoc,
                    "Balance": TxBalance
                }}
        }
    x = BudgetEngine.postedtx.update_one(postedTxAcctQuery,postedTxToWrite)

def CreateBlankTxLog(acctName):
    "This function will create a blank transaction log if it does not already exist"
    filter = { "acctName": acctName }
    TxLogCheck =  BudgetEngine.postedtx.count_documents(filter, limit=1)
    if TxLogCheck == 1:
        print("TxLog already exists, please review for validity")
    if TxLogCheck < 1:
        print("TxLog does not exist, creating.")
        BudgetEngine.postedtx.insert_one(
            {
                "acctName": acctName
            }
        )

def searchTxData(acctName,Memo,TxType):
    "This function will get all transactions in a given account matching a search on memo"
    searchTxData = BudgetEngine.postedtx.aggregate([
    {
        '$match': {
            'acctName': acctName
        }
    }, {
        '$unwind': {
            'path': '$PostedTxs'
        }
    }, {
        '$match': {
            'PostedTxs.Memo': {
                '$regex': Memo
            }, 
            'PostedTxs.TxType': TxType
        }
    }, {
        '$group': {
            '_id': '$acctName', 
            'PostedTxs': {
                '$push': {
                    'txID': '$PostedTxs.txID',
                    'Memo': '$PostedTxs.Memo', 
                    'Amount': '$PostedTxs.Amount', 
                    'Date': {
                        '$dateToString': {
                            'format': '%Y-%m-%d', 
                            'date': '$PostedTxs.Date'}}, 
                    'TxType': '$PostedTxs.TxType', 
                    'AdHoc': '$PostedTxs.AdHoc', 
                    'Balance': '$PostedTxs.Balance'
                }
            }
        }
    }
])
    return searchTxData