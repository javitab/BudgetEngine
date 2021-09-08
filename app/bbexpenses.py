import bbdata as bb
import pprint as pp

def insertExpense(acctID, DayOfMonth, Name, Amount, StartDate, EndDate):
    filter = {"Name":Name}
    expCheck =  bb.expenses.count_documents(filter, limit=1)
    if expCheck == 1:
        print("Expense already exists, please review for validity")
    elif expCheck < 1:
        print("Expense does not exist. Will write to DB.")
        expenseToWrite = {
        "acctID" : acctID,
        "DayOfMonth" : DayOfMonth,
        "Name" : Name,
        "Amount" : Amount,
        "StartDate" : StartDate,
        "EndDate" : EndDate,
        "LastPostedDate": StartDate
        }
        x = bb.expenses.insert_one(expenseToWrite)
        print(x.inserted_id)


actions = [
    "1: Print all expenses for account",
    "2: Print expenses for all accounts",
    "3: Set LastPostedDate",
    "4: Create new expense",
    "5: Add end date to expense",
    "6: Change amount"
]

def expMenu():
    continueExpLoop = 1
    while continueExpLoop == 1:
        action = bb.menuGen(actions,"Expense menu",0)
        if action == 'Q':
            continueExpLoop = 0
        if action == '1':
            bb.printAsDataFrame(bb.listCollection("accounts"))
            inputacctID = input("Please enter account: ")
            bb.printAsDataFrame(bb.listExpenses(inputacctID))
        if action == '2':
            bb.printAsDataFrame(bb.listCollection('expenses'))
        if action == '3':
            currExp = bb.expense(input("Please enter the name of the expense you would like to update: "))
            iterNextDate = bb.txIterate('Monthly',currExp.LastPostedDate)
            newDateConf = input("Is the new LastPostedDate %s? (y/n)" % iterNextDate)
            if newDateConf == 'y': currExp.setLastPostedDate(iterNextDate)
            if newDateConf == 'n': currExp.setLastPostedDate(bb.convDate(input("Please enter the new LastPostedDate (YYYY-MM-DD)")))
        if action == '4':
            print("Please enter info for new expense:")
            bb.printAsDataFrame(bb.listCollection("accounts"))
            inputacctID = input("Please enter account: ")
            inputName = input("Please enter name of new expense: ")
            inputAmount = input("Please enter the amount: ")
            AmountInt = float(inputAmount)
            inputStartDate = input("Please enter a start date (YYYY-MM-DD): ")
            StartDateFormatted = bb.convDate(inputStartDate)
            DayOfMonth = StartDateFormatted.day
            print("Interpreting DayOfMonth as %s from StartDate " % StartDateFormatted.day)
            inputEndDate = input("Please enter the EndDate (if applicable): ")
            if inputEndDate == "":
                EndDateFormatted = None
            elif inputEndDate != "":
                EndDateFormatted = bb.convDate(inputEndDate)
            insertExpense(inputacctID,DayOfMonth,inputName,AmountInt,StartDateFormatted,EndDateFormatted)
        if action == '5':
            currExp =  bb.expense(input("Please enter name of expense that you wish to modify: "))
            print("Expense selected: ",currExp.name)
            EndDate = input("Please enter the desired end date for expense (YYYY-MM-DD) : ")
            currExp.addEndDate(EndDate)
        if action == '6':
            currExp =  bb.expense(input("Please enter name of expense that you wish to modify: "))
            print("Expense selected: ",currExp.name)
            newAmount = input("Please enter the new amount for the expense (XX.XX) : ")
            currExp.changeAmount(newAmount)