import bbdata as bb
import matplotlib.pyplot as plt
import pandas as pd

projEnd = '2021-12-31'

expenseacct = bb.acct('Expense')

expenseproj = expenseacct.projRev(projEnd)

expDf = expenseproj[2]

print("Expense account projected balance for",projEnd,"will be $",expenseproj[0])

expDf.plot(kind='line',x='Date',y='Balance',title='Expense account projected balances')
plt.savefig('./proj_output/output.png')