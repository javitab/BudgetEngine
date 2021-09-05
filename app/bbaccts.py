##
##TODO: Model after bb-importexpenses.py
##

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

#x = accts.insert_many(accountImport)

#print(x.inserted_ids)

print("Available actions:")
print("1: Print all accounts")
print("2: Update current balance")
action = input("What would you like to do? ")    

if action == '1':
    bb.printAsDataFrame(bb.listCollection("accounts"))
if action == '2':
    acctToUpdate = input("Please enter account to update: ")
    newBalance = input("Please input new balance (XX.XX) : ")
    query = {'Name': acctToUpdate}
    updateBalance = { '$set': { 'CurrBalance': float(newBalance)}}
    x = bb.accts.update_one(query, updateBalance)