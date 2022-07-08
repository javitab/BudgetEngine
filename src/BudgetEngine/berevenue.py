##
##TODO: Model after be-importexpenses.py
##
import BudgetEngine as be
from bson import ObjectId

revenueImport = [
    { 

    "revName": "Name's Expense", 
    "Institution": "Organization", 
    "Account": "Expense", 
    "Frequency": "Biweekly", 
    "Amount": 500, 
    "StartDate": be.convDate("2021-8-19")
    
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
        action = be.menuGen(actions,"Revenue menu",0)
        if action == 'Q':
            continueRevLoop = 0
        if action == '1':
            be.printAsDataFrame(be.listCollection("accounts"))
            inputacctID = input("Please enter account: ")
            be.printAsDataFrame(be.listRevenue(inputacctID))
        if action == '2':
            be.printAsDataFrame(be.listCollection('revenue'))
        if action == '3':
            dateToExcludeinput = input("Please input date to exclude (YYY-MM-DD) : ")
            revName = input ("Please input name of revenue to add exclusion date to: ")
            dateToExclude = be.convDate(dateToExcludeinput)
            query = {'Name': revName}
            addExclusionDate = { '$push': { 'ExclusionDates': dateToExclude}}
            x = be.revenues.update_one(query, addExclusionDate)
        if action == '4':
            currRev = be.revenue(input("Please enter the name of the revenue you would like to update: "))
            iterNextDate = be.txIterate(currRev.Frequency,currRev.LastDatePosted)
            newDateConf = input("Is the new LastPostedDate %s? (y/n)" % iterNextDate)
            if newDateConf == 'y': currRev.setLastPostedDate(iterNextDate)
            if newDateConf == 'n': currRev.setLastPostedDate(be.convDate(input("Please enter the new LastPostedDate (YYYY-MM-DD)")))
        if action == '5':
            NewRevName = input("Please input name for new revenue: ")
            NewRevInst = input("Please input name of Institution for new revenue: ")
            NewRevAcct = input("Please input account for new revnue: ")
            NewRevAmount = float(input("Please input amount for new revenue: "))
            NewRevFreq = input("Please input frequency for new revenue: ")
            NewRevStartDate = input("Please input start date for new revenue (YYYY-MM-DD): ")
            NewRevStartDate = be.convDate(NewRevStartDate)
            NewRevEnd = input("Please input end date for new revenue (YYYY-MM-DD): ")
            if NewRevEnd == "":
                NewRevEnd = None
            else:
                NewRevEnd = be.convDate(NewRevEnd)
            insertRevenue(NewRevName, NewRevInst, NewRevAcct, NewRevAmount, NewRevFreq, NewRevStartDate, NewRevEnd)
        if action == '6':
            be.printAsDataFrame(be.listCollection('revenue'))
            delRevID = input("Please enter _id of revenue to delete: ")
            deleteRevenue(delRevID)


def insertRevenue(NewRevName, NewRevInst, NewRevAcct, NewRevAmount, NewRevFreq, NewRevStartDate, NewRevEnd):
    filter = {"Name":NewRevName}
    revCheck =  be.revenues.count_documents(filter, limit=1)
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
        x = be.revenues.insert_one(revenueToWrite)
        print(x.inserted_id)

def deleteRevenue(delRevID):
    x = be.revenues.delete_one({"_id":ObjectId(delRevID)})
    print(x.deleted_count, " documents deleted.")

class revenue:

    def __init__(self, revName):
        self.data = be.revenues.find_one({"Name": revName})
        self.amount = self.data['Amount']
        self.name = self.data['Name']
        self.acct = self.data['Account']
        self.startDate = self.data['StartDate']
        self.endDate = self.data['EndDate']
        self.exclusionDates = self.data['ExclusionDates']
        self.Frequency = self.data['Frequency']
        self.LastDatePosted = self.data['LastDatePosted']

    def reset(self):
        "Reinitializes the current instance of the class. Intended for use after new values have been written to the DB"
        self.__init__(self.name)
    
    def display(self):
        print("Rev name: ", self.name, end=', ')
        print("Rev Amount: $", self.amount, end=', ')
        print("Rev Account: ", self.acct, end=', ')
        print("Rev Start Date: ", self.startDate, end=', ')
        print("Rev End Date: ", self.endDate)
        iterNum = 0
        for i in self.exclusionDates:
            iterNum = iterNum + 1
            print("Exclusion Date #%s %s" % (iterNum, i))

    def addExclDate(self, revExclDate):
        if revExclDate not in self.exclusionDates:
            be.revenues.update_one(
                { 'Name': self.name },
                { '$push': {'ExclusionDates': revExclDate}}
            )
            self.reset()
        elif revExclDate in self.exclusionDates:
            print("Value already exists")

    def setLastPostedDate(self, LastPostedDate):
        be.revenues.update_one(
                { 'Name': self.name },
                { '$set': {'LastDatePosted': LastPostedDate}}
            )
        self.reset()