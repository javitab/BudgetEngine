##
## Formerly bbt.py, starts process to calculate balance projections
##

import bbdata as bb
import matplotlib.pyplot as plt


jointAcct = bb.acct('Joint')
expenseAcct = bb.acct('Expense')

exeStartDate = ('2022-12-31')

jointproj = jointAcct.projRev(exeStartDate)
expenseproj = expenseAcct.projRev(exeStartDate)

print(jointproj[0])
print(expenseproj[0])

AcctsTotal = jointproj[0] + expenseproj[0]

print("Total between accounts: $%s" % AcctsTotal)

jointprojDf = jointproj[2]
expenseprojDf = expenseproj[2]

jointprojDf.plot.line( x = 'Date', y = 'Balance', title='Projection of balance in Joint, Final Balance: $%s' % round(jointproj[0],2))
expenseprojDf.plot.line( x = 'Date', y = 'Balance', title='Projection of balance in Expense, Final Balance: $%s' % round(expenseproj[0],2))
plt.show(block=True)
