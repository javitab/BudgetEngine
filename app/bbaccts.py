import pymongo
import pprint
import bbdata as bb
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
bbdb = myclient["BudgetBalancer"]
accts = bbdb["accounts"]

accountImport = [
    { "name": "Joint", "Institution": "BankName"},
    { "name": "Expense", "Institution": "BankName"},
]

actions = [
            "1: Print all accounts",
            "2: Update current balance"
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
        if action == 'Q':
            continueAcctLoop = 0