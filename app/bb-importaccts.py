##
##TODO: Model after bb-importexpenses.py
##

import pymongo
import pprint
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
bbdb = myclient["BudgetBalancer"]
accts = bbdb["accounts"]

accountImport = [
    { "name": "Joint", "Institution": "BankName"},
    { "name": "Expense", "Institution": "BankName"},
]

x = accts.insert_many(accountImport)

print(x.inserted_ids)