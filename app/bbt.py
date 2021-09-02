import bbdata as bb

projEnd = '2021-12-31'

expenseacct = bb.acct('Expense')

expenseproj = expenseacct.projRev(projEnd)

print("Expense account projected balance for",projEnd,"will be $",expenseproj[0])