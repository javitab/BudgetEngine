from bson.objectid import ObjectId
from datetime import datetime as dt
from datetime import timedelta

from faker import Faker
import random


from BudgetEngine.projection import Projection
from BudgetEngine.user import User
from BudgetEngine.acct import Acct,PtxLog
from BudgetEngine.exp import Exp
from BudgetEngine.rev import Rev

from bson.objectid import ObjectId

'''
Defining test parameters
'''

#Number of test users to create
testUsers=1

#Number of test accounts per user
testAccts=1

#Number of text expenses per user
testExpenses=5

#Number of days to generate test data for
PtxLogDataDays=60

fake=Faker()
Faker.seed(random.Random().randint(1,1000))

if __name__=='__main__':

    for _ in range(testUsers):
        """
        Create a new test user
        """
        first_name=fake.first_name()
        last_name=fake.last_name()
        userid=str(first_name+"."+last_name).lower()
        email=userid+"@test.com"
        newUser = User(
            userid=userid,
            email=email, 
            first_name=first_name, 
            last_name=last_name, 
            password="pbkdf2:sha256:260000$dDxECjiuG3D25eUp$ba89e579b08c476f3db515fa9bfcd3814acc3ed6d047abff2b7fd4bb3d679e5b", 
            timezone=fake.timezone()
        )
        newUser.save()

        """
        Create test accounts for newUser
        """
        for _ in range(testAccts):
            newAcct = Acct(
                bank_name=fake.random_element(elements=['Chase','Wells Fargo','Citi','Bank of America','PNC','US Bank','USAA','Capital One','Connex Credit Union']),
                bank_routing_number=fake.aba(), 
                bank_account_number=fake.bban(), 
                account_display_name=fake.random_element(elements=['Checking','Savings','Joint','Expense']),
                current_balance=fake.pydecimal(positive=True, min_value=1, max_value=100000, left_digits=6, right_digits=2),
                low_balance_alert=fake.pydecimal(positive=True, min_value=1, max_value=1000, left_digits=4, right_digits=2), 
                tx_last_posted=fake.date_time_between(start_date="-30d",end_date="now",tzinfo=None),
                notes=fake.text(max_nb_chars=200)
                )
            newAcct.save()
            newUser.acctIds.append(newAcct.id)
            newUser.save()
            newPtxLog = PtxLog()
            newPtxLog.save()
            newAcct.history_ptx_log_ids.append(newPtxLog.id)
            newAcct.active_ptx_log_id = newPtxLog.id
            newAcct.save()
            """
            Create test revenue for newAcct
            """
            newRev = Rev(
                display_name=fake.random_element(elements=['Day Job','Uber','Lyft','Instacart']),
                amount=fake.pydecimal(positive=True, min_value=500, max_value=1000, left_digits=6, right_digits=2),
                frequency="weekly",
                start_date=fake.date_time_between(start_date="+2d",end_date="+30d",tzinfo=None),
                notes=fake.text(max_nb_chars=200)

            )
            newRev.save()
            newAcct.rev_ids.append(newRev.id)
            newAcct.save()
            """
            Create test expenses for newAcct
            """
            for _ in range(testExpenses):
                newExp = Exp(
                    display_name=fake.random_element(elements=['Rent','Netflix','Spotify','Cellphone','Electric','Gas','Water','Mortgage','Car Loan']),
                    amount=fake.pydecimal(positive=True, min_value=1, max_value=100, left_digits=3, right_digits=2),
                    frequency="monthly",
                    start_date=fake.date_time_between(start_date="+5d",end_date="now",tzinfo=None),
                    notes=fake.text(max_nb_chars=200)
                )
                newExp.save()
                newAcct.exp_ids.append(newExp.id)
                newAcct.save()
            
            print("\n###","\n### User: ",newUser.userid,"\n###","ObjectId",newAcct.id,"\n###","Account: ",newAcct.account_display_name,"\n###\n",)
            for i in newAcct.exp_ids:
                iexp=Exp.objects.get(id=i)
                print("exp: ", iexp.start_date.strftime("%Y-%m-%d"), iexp.display_name, iexp.amount, iexp.frequency, iexp.next_date())
            for i in newAcct.rev_ids:
                irev=Rev.objects.get(id=i)
                print("rev: ", irev.start_date.strftime("%Y-%m-%d"), irev.display_name, irev.amount, irev.frequency, irev.next_date())
            
            #Generate data to PtxLog with expenses and revenues

            for _ in range(PtxLogDataDays):
                _date=dt.now().__add__(timedelta(days=_))
                _date=dt.date(_date)
                for rev in newAcct.rev_ids:
                    rev=Rev.objects.get(id=rev)
                    if rev.next_date()==_date:
                        newPtxLog.posted_txs.create(
                            txID=ObjectId(),
                            date=_date,
                            memo=rev.display_name,
                            amount=rev.amount,
                            tx_type="credit",
                            ad_hoc=False,
                            balance=newAcct.current_balance+rev.amount)
                        newPtxLog.save()
                        newAcct.current_balance += rev.amount
                        newAcct.save()
                        rev.last_posted_date=_date
                        rev.save()
                for exp in newAcct.exp_ids:
                    exp=Exp.objects.get(id=exp)
                    print("_date: ",_date,"exp.next_date(): ",exp.next_date())
                    if exp.next_date()==_date:
                        newPtxLog.posted_txs.create(
                            txID=ObjectId(),
                            date=_date,
                            memo=exp.display_name,
                            amount=exp.amount,
                            tx_type="debit",
                            ad_hoc=False,
                            balance=newAcct.current_balance-exp.amount)
                        newPtxLog.save()
                        newAcct.current_balance -= exp.amount
                        newAcct.save()
                        exp.last_posted_date=_date
                        exp.save()

            #Output data written to PtxLog
            print("\n### Printing Transactions for Acct: ",newAcct.account_display_name)
            for i in newPtxLog.posted_txs:
                print(i.date, i.memo, i.amount, i.tx_type, i.balance)
            
        #Outputting account data for user
        for acct in newUser.acctIds:
            acct=Acct.objects.get(id=acct)
            print("\n###","\n### User: ",newUser.userid,"\n###","ObjectId",acct.id,"\n###","Account: ",acct.account_display_name,"\n###\n",)
            print("### Account Expenses ###")
            for expid in acct.exp_ids:
                print(expid.display_name, " ", expid.amount, " ", expid.frequency, " ", expid.next_date())
            print("\n\n### Account Revenues ###")
            for revid in acct.rev_ids:
                print(revid.display_name, " ", revid.amount, " ", revid.frequency, " ", revid.next_date())
            print("\n\n### Account Transactions ###")
            ptxLog=acct.active_ptx_log_id
            print("### Current active_ptx_log_id: ",ptxLog.id)
            for tx in ptxLog.posted_txs:
                print(tx.date, tx.memo, tx.amount, tx.tx_type, tx.balance)
        #Running projection for each account for user
        for acct in newUser.acctIds:
            projAcct=Acct.objects.get(id=acct)
            newProjection=Projection(
                disp_name=f"Projection through {dt.now().__add__(timedelta(days=90)).date()}",
                projection_acct=projAcct.id,
                start_date=dt.now(),
                end_date=dt.now().__add__(timedelta(days=90))
            )
            newProjection.save()
            newProjection.runProjection(projAcct)
            projAcct.projections.append(newProjection.id)
            projAcct.save()
            print("\n### Printing Projection for Acct: ",projAcct.account_display_name,"###")
            for i in newProjection.projected_txs:
                print(i.date, i.memo, i.amount, i.tx_type, i.balance)
            