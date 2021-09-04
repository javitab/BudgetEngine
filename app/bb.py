from re import X
import sys
import getopt
import bbdata as bb
import pprint
from tabulate import tabulate
import pandas as pd
import bbrecView

acctArg = 0
showHelp = 0
expArg = 0
Verbose = 0
list = 0
listArg = 0
listExp = 0
totExp = 0
projArg = 0
recView = 0

full_cmd_arguments = sys.argv

argument_list = full_cmd_arguments[1:]

#print(argument_list)
#print(bb.LastDate)

short_options = "ha:e:l:vpr"
long_options = ["help", "account=", "verbose", "expense=", "list=","listExpenses=","totalExpenses=","projection","recordviewer"]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)

# Evaluate given options
for current_argument, current_value in arguments:
    if current_argument in ("-v", "--verbose"):
        print ("Enabling verbose mode")
        Verbose = 1
    elif current_argument in ("-h", "--help"):
        print ("Displaying help")
        showHelp = 1
    elif current_argument in ("-a", "--account"):
        print (("Outputting details for (%s)") % (current_value))
        account = current_value
        acctArg = 1
    elif current_argument in ("-e", "--expense"):
        print (("Outputting details for (%s)") % (current_value))
        expense = current_value
        expArg = 1
    elif current_argument in ("-l", "--list"):
        print(("Outputting list of (%s)") % (current_value))
        list = current_value
        listArg = 1
    elif current_argument in ("--listExpenses"):
        print(("Outputting list of (%s) expenses") % (current_value))
        account = current_value
        listExp = 1
    elif current_argument in ("--totalExpenses"):
        print("Calculating total of all expenses of %s account" % (current_value))
        account = current_value
        totExp = 1
    elif current_argument in ("-p",'--projection'):
        print("Beginning budget projection process")
        projArg = 1
    elif current_argument in ("-r","--recordviewer"):
        print("Launching Record Viewer")
        recView = 1
    
if (showHelp == 1):
    print("Valid arguments for this script")
    print("-a or --account=#AccountName# will display account information")
    print("-e or --expense=#ExpenseName# will display expense information")

if (acctArg == 1):
    data = bb.findAcct(account)
    print(data)

if (expArg == 1):
    data = bb.findExp(expense)
    print(data)

if (Verbose == 1):
    print(bb.bbdb.list_collection_names())

if (listExp == 1):
    data = bb.listExpenses(account)
    bb.printAsDataFrame(data)
    sum = bb.totalExpenses(account)
    print("Total of expenses for account is %s" % sum)

if (listArg == 1):
    data = bb.listCollection(list)
    bb.printAsDataFrame(data)

if (totExp == 1):
    data = bb.totalExpenses(account)
    print(data)

if (projArg == 1):
   StopDate = input("What date would you like to run the projection until?(YYYY-MM-DD) # ")
   projJoint = bbproj.runProjection('Joint',StopDate)
   projExpense = bbproj.runProjection('Expense', StopDate)
   print("Joint account balance: $%s" % projJoint['EndBalance'])
   print("Expense account balalnce: $%s" % projExpense['EndBalance'])
   projTotalBalance = projJoint['EndBalance'] + projExpense['EndBalance']
   print("Total balance across accounts: $%s" % projTotalBalance)
   print("Joint Rev $%s Joint Exp $%s  Expense Rev $%s Expense Exp $%s" % (projJoint['RevTotal'], projJoint['ExpTotal'], projExpense['RevTotal'], projExpense['ExpTotal']))
if (recView == 1):
    bbrecView.recView()