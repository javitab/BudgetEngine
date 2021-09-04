import bbdata as bb
import matplotlib.pyplot as plt


projEnd = '2022-12-31'
acctName = 'Joint'
acct = bb.acct(acctName)

proj = acct.projRev(projEnd)

expDf = proj[2]

print(acctName,"account projected balance for",projEnd,"will be $",proj[0])

expDf.plot(kind='line',x='Date',y='Balance',title=('%s account projected balances, $%s' % (acctName, proj[0])))
plt.savefig('/projoutput/output.png')