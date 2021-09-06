##
##TODO: Model after bb-importexpenses.py
##
import bbdata as bb

revenueImport = [
    { 

    "revName": "Name's Expense", 
    "Institution": "Organization", 
    "Account": "Expense", 
    "Frequency": "Biweekly", 
    "Amount": 500, 
    "StartDate": bb.convDate("2021-8-19")
    
    }
]

actions = [
    "1: Print revenue for account",
    "2: Print revenue for all accounts",
    "3: Add exclusion date",
    "4: Set LastPostedDate"

]

def revMenu():
    continueRevLoop = 1
    while continueRevLoop == 1:
        action = bb.menuGen(actions,"Revenue menu",0)
        if action == 'Q':
            continueRevLoop = 0
        if action == '1':
            bb.printAsDataFrame(bb.listCollection("accounts"))
            inputacctID = input("Please enter account: ")
            bb.printAsDataFrame(bb.listRevenue(inputacctID))
        if action == '2':
            bb.printAsDataFrame(bb.listCollection('revenue'))
        if action == '3':
            dateToExcludeinput = input("Please input date to exclude (YYY-MM-DD) : ")
            revName = input ("Please input name of revenue to add exclusion date to: ")
            dateToExclude = bb.convDate(dateToExcludeinput)
            query = {'Name': revName}
            addExclusionDate = { '$push': { 'ExclusionDates': dateToExclude}}
            x = bb.revenues.update_one(query, addExclusionDate)
        if action == '4':
            currRev = bb.revenue(input("Please enter the name of the revenue you would like to update: "))
            iterNextDate = bb.txIterate(currRev.Frequency,currRev.LastDatePosted)
            newDateConf = input("Is the new LastPostedDate %s? (y/n)" % iterNextDate)
            if newDateConf == 'y': currRev.setLastPostedDate(iterNextDate)
            if newDateConf == 'n': currRev.setLastPostedDate(bb.convDate(input("Please enter the new LastPostedDate (YYYY-MM-DD)")))
        