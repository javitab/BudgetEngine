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
    "StartDate": bb.date("2021-8-19")
    
    }
]

dateToExclude = bb.date('2021-08-27')
revNameToUpdate = 'revName'

query = {'Name': revNameToUpdate}
addExclusionDate = { '$push': { 'ExclusionDates': dateToExclude}}

x = bb.revenues.update_one(query, addExclusionDate)