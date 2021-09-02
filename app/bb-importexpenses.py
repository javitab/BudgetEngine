import bbdata as bb

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