import pymongo
import pprint
import bbdata as bb
import matplotlib.pyplot as plt
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
            "3: Project balance"
        ]


def acctMenu():
    continueAcctLoop = 1

    while continueAcctLoop == 1:
        action = bb.menuGen(actions,"Account menu",0)
        if action == '1':
            bb.printAsDataFrame(bb.listCollection("accounts"))
        if action == '2':
            acctToUpdate = input("Please enter account to update: ")
            newBalance = input("Please input new balance (XX.XX) : ")
            query = {'Name': acctToUpdate}
            updateBalance = { '$set': { 'CurrBalance': float(newBalance)}}
            x = bb.accts.update_one(query, updateBalance)
        if action == '3':
            projEndInput = input("Enter end date for projection: ")
            projAcctInput = input("Enter account for projection: ")
            acct = bb.acct(projAcctInput)
            proj = acct.projRev(projEndInput)
            projDf = proj[2]
            print(projAcctInput,"account projected balance for",projEndInput,"will be $",proj[0])
            projDf.plot(kind='line',x='Date',y='Balance',title=('%s account projected balances, $%s' % (projAcctInput, proj[0])))
            plt.savefig('/projoutput/output.png')
            print("Projection graph available at: http://localhost:8080/output.png")
        if action == 'Q':
            continueAcctLoop = 0