from datetime import datetime
from os import read
from pprint import PrettyPrinter
from faker import Faker
import random

from BudgetEngine.data import *
from prettytable import PrettyTable
from bson.objectid import ObjectId



fake=Faker()
Faker.seed(random.Random().randint(1,1000))

if __name__=='__main__':

    for _ in range(1):
        """
        Create a new test user
        """
        newUser = User(
            userid=fake.user_name(), 
            email=fake.email(), 
            first_name=fake.first_name(), 
            last_name=fake.last_name(), 
            password=fake.password(), 
            timezone=fake.timezone()
        )
        newUser.save()

        """
        Create test accounts for newUser
        """
        for _ in range(1):
            newAcct = Acct(
                bank_name=fake.random_element(elements=['Chase','Wells Fargo','Citi','Bank of America','PNC','US Bank','USAA','Capital One','Connex Credit Union']),
                bank_routing_number=fake.aba(), 
                bank_account_number=fake.bban(), 
                account_display_name=fake.random_element(elements=['Checking','Savings','Joint','Expense']),
                current_balance=fake.pydecimal(positive=True, min_value=1, max_value=100000, left_digits=6, right_digits=2),
                low_balance_alert=fake.pydecimal(positive=True, min_value=1, max_value=1000, left_digits=4, right_digits=2), 
                tx_last_posted=fake.date_time_between(start_date="-30d",end_date="now",tzinfo=None))
            newAcct.save()
            newUser.acctIds.append(newAcct.id)
            newUser.save()
            newPtxLog = PtxLog()
            newPtxLog.save()
            newAcct.history_ptx_log_ids.append(newPtxLog.id)
            newAcct.active_ptx_log_id = newPtxLog.id
            newAcct.save()
            newRev = Rev(
                display_name=fake.random_element(elements=['Day Job','Uber','Lyft','Instacart']),
                amount=fake.pydecimal(positive=True, min_value=1, max_value=100000, left_digits=6, right_digits=2),
                frequency="weekly",
                start_date=fake.date_time_between(start_date="+2d",end_date="+30d",tzinfo=None)

            )
            newRev.save()
            newAcct.rev_ids.append(newRev.id)
            newAcct.save()
            
            for _ in range(5):
                newExp = Exp(
                    display_name=fake.random_element(elements=['Rent','Netflix','Spotify','Cellphone','Electric','Gas','Water','Mortgage','Car Loan']),
                    amount=fake.pydecimal(positive=True, min_value=1, max_value=100, left_digits=3, right_digits=2),
                    frequency="monthly",
                    start_date=fake.date_time_between(start_date="-30d",end_date="now",tzinfo=None)
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

            for _ in range(30):
                _date=dt.utcnow().__add__(timedelta(days=_)).strftime("%Y-%m-%d")
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