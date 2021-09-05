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

print("Available actions:")
print("1: Print expenses for account")
print("2: Add exclusion date")
action = input("What would you like to do? ")    

if action == '1':
    bb.printAsDataFrame(bb.listCollection("accounts"))
    inputacctID = input("Please enter account: ")
    bb.printAsDataFrame(bb.listRevenue(inputacctID))
if action == '2':
    dateToExcludeinput = input("Please input date to exclude (YYY-MM-DD) : ")
    revName = input ("Please input name of revenue to add exclusion date to: ")
    dateToExclude = bb.convDate('2021-08-27')
    query = {'Name': revName}
    addExclusionDate = { '$push': { 'ExclusionDates': dateToExclude}}
    x = bb.revenues.update_one(query, addExclusionDate)