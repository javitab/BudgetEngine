import pymongo
import pprint
import bbdata as bb
import bbposttx as bbt
import matplotlib.pyplot as plt
from bson import ObjectId
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
bbdb = myclient["BudgetBalancer"]
accts = bbdb["accounts"]

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
    continueAcctLoop = 1

    while continueAcctLoop == 1:
        action = bb.menuGen(actions,"Account menu",0)
        if action == '1':
            bb.printAsDataFrame(bb.listCollection("accounts"))
        if action == '2':
            acctToUpdate = input("Please enter account to update: ")
            acct = bb.acct(acctToUpdate)
            print(acct.name,"has been selected")
            newBalance = float(input("Please input new balance (XX.XX) : "))
            acct.setCurrBalance(newBalance)
        if action == '3':
            acctToUpdate = input("Please enter account to update: ")
            acct = bb.acct(acctToUpdate)
            print(acct.name,"has been selected")
            NewLowBalance = float(input("Please enter new low balance alert level: (XXXX.XX)"))
            acct.setLowBalAlertLevel(NewLowBalance)
        if action == '4':
            projEndInput = input("Enter end date for projection: ")
            projAcctInput = input("Enter account for projection: ")
            acct = bb.acct(projAcctInput)
            proj = acct.projRev(projEndInput)
            projDf = proj[2]
            print(projAcctInput,"account projected balance for",projEndInput,"will be $",proj[0])
            projDf.plot(kind='line',x='Date',y='Balance',title=('%s account projected balances, $%s' % (projAcctInput, proj[0])))
            plt.savefig('/projoutput/output.png')
            print("Projection graph available at: http://%s:8080/output.png" % bb.extIP)
        if action == '5':
            NewAcctName = input("Enter name for new account: ")
            NewAcctInst = input("Enter name of institution for new account: ")
            NewAcctBalance = float(input("Enter current balance for new account: "))
            NewAcctLowBalance = float(input("Enter low balance alert threshold for new account: "))
            insertAccount(NewAcctName, NewAcctInst, NewAcctBalance, NewAcctLowBalance)
        if action == '6':
            bb.printAsDataFrame(bb.listCollection('accounts'))
            delAcctID = input("Enter _id for account to delete: ")
            deleteAcct(delAcctID)
        if action == 'Q':
            continueAcctLoop = 0

def insertAccount(NewAcctName, NewAcctInst, NewAcctBalance, NewAcctLowBalance):
    filter = {"Name":NewAcctName}
    acctCheck =  bb.accts.count_documents(filter, limit=1)
    if acctCheck == 1:
        print("Account already exists, please review for validity")
    elif acctCheck < 1:
        print("Account does not exist. Will write to DB.")
        if (NewAcctName!=None) or (NewAcctInst!=None) or (NewAcctBalance!=None) or (NewAcctLowBalance!=None):
            accountToWrite = {
            "Institution": NewAcctInst,
            "Name": NewAcctName,
            "CurrBalance": NewAcctBalance,
            "LowBalance": NewAcctLowBalance,
            "TxLastPosted": None
            }
            x = bb.accts.insert_one(accountToWrite)
            print(x.inserted_id)
            bbt.CreateBlankTxLog(NewAcctName)

def deleteAcct(delAcctID):
    x = bb.accts.delete_one({"_id":ObjectId(delAcctID)})
    print(x.deleted_count, " documents deleted.")