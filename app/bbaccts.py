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
            "3: Set low balance level",
            "4: Project balance"
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
        if action == 'Q':
            continueAcctLoop = 0