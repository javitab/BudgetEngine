##
##TODO: Model after be-importexpenses.py
##
import BudgetEngine as BudgetEngine
from bson import ObjectId

revenueImport = [
    { 

    "revName": "Name's Expense", 
    "Institution": "Organization", 
    "Account": "Expense", 
    "Frequency": "Biweekly", 
    "Amount": 500, 
    "StartDate": BudgetEngine.convDate("2021-8-19")
    
    }
]

actions = [
    "1: Print revenue for account",
    "2: Print revenue for all accounts",
    "3: Add exclusion date",
    "4: Set LastPostedDate",
    "5: Enter New Revenue",
    "6: Delete revenue"

]

def revMenu():
    continueRevLoop = 1
    while continueRevLoop == 1:
        action = BudgetEngine.menuGen(actions,"Revenue menu",0)
        if action == 'Q':
            continueRevLoop = 0
        if action == '1':
            BudgetEngine.printAsDataFrame(BudgetEngine.listCollection("accounts"))
            inputacctID = input("Please enter account: ")
            BudgetEngine.printAsDataFrame(BudgetEngine.listRevenue(inputacctID))
        if action == '2':
            BudgetEngine.printAsDataFrame(BudgetEngine.listCollection('revenue'))
        if action == '3':
            dateToExcludeinput = input("Please input date to exclude (YYY-MM-DD) : ")
            revName = input ("Please input name of revenue to add exclusion date to: ")
            dateToExclude = BudgetEngine.convDate(dateToExcludeinput)
            query = {'Name': revName}
            addExclusionDate = { '$push': { 'ExclusionDates': dateToExclude}}
            x = BudgetEngine.revenues.update_one(query, addExclusionDate)
        if action == '4':
            currRev = BudgetEngine.revenue(input("Please enter the name of the revenue you would like to update: "))
            iterNextDate = BudgetEngine.txIterate(currRev.Frequency,currRev.LastDatePosted)
            newDateConf = input("Is the new LastPostedDate %s? (y/n)" % iterNextDate)
            if newDateConf == 'y': currRev.setLastPostedDate(iterNextDate)
            if newDateConf == 'n': currRev.setLastPostedDate(BudgetEngine.convDate(input("Please enter the new LastPostedDate (YYYY-MM-DD)")))
        if action == '5':
            NewRevName = input("Please input name for new revenue: ")
            NewRevInst = input("Please input name of Institution for new revenue: ")
            NewRevAcct = input("Please input account for new revnue: ")
            NewRevAmount = float(input("Please input amount for new revenue: "))
            NewRevFreq = input("Please input frequency for new revenue: ")
            NewRevStartDate = input("Please input start date for new revenue (YYYY-MM-DD): ")
            NewRevStartDate = BudgetEngine.convDate(NewRevStartDate)
            NewRevEnd = input("Please input end date for new revenue (YYYY-MM-DD): ")
            if NewRevEnd == "":
                NewRevEnd = None
            else:
                NewRevEnd = BudgetEngine.convDate(NewRevEnd)
            insertRevenue(NewRevName, NewRevInst, NewRevAcct, NewRevAmount, NewRevFreq, NewRevStartDate, NewRevEnd)
        if action == '6':
            BudgetEngine.printAsDataFrame(BudgetEngine.listCollection('revenue'))
            delRevID = input("Please enter _id of revenue to delete: ")
            deleteRevenue(delRevID)


def insertRevenue(NewRevName, NewRevInst, NewRevAcct, NewRevAmount, NewRevFreq, NewRevStartDate, NewRevEnd):
    filter = {"Name":NewRevName}
    revCheck =  BudgetEngine.revenues.count_documents(filter, limit=1)
    if revCheck == 1:
        print("Revenue already exists, please review for validity")
    elif revCheck < 1:
        print("Revenue does not exist. Will write to DB.")
        revenueToWrite = {
        "Institution": NewRevInst,
        "Account": NewRevAcct,
        "Frequency": NewRevFreq,
        "Amount": NewRevAmount,
        "StartDate": NewRevStartDate,
        "Name": NewRevName,
        "EndDate": NewRevEnd,
        "ExclusionDates": [''],
        "LastDatePosted": NewRevStartDate
        }
        x = BudgetEngine.revenues.insert_one(revenueToWrite)
        print(x.inserted_id)

def deleteRevenue(delRevID):
    x = BudgetEngine.revenues.delete_one({"_id":ObjectId(delRevID)})
    print(x.deleted_count, " documents deleted.")